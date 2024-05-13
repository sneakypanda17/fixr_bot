package main

import (
	"bufio"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"

	"github.com/sneakypanda17/fixr" // Adjust the import path based on your project structure
)

type Event struct {
	ID     int    `json:"id"`
	Name   string `json:"name"`
	IDDate string `json:"date"`
}

func main() {
	// Update FIXR version at startup
	if err := fixr.UpdateVersion(); err != nil {
		fmt.Printf("Error updating FIXR version: %v\n", err)
	}
	fmt.Printf("Using FIXR API version: %s\n", fixr.FixrVersion)

	// Load user credentials from a CSV file
	creds, err := loadCredentials("../credential_generator/credentials.csv")
	if err != nil {
		fmt.Printf("Error loading credentials: %v\n", err)
		return
	}

	// Load event data from a JSON file
	events, err := loadEvents("../web_scraper/events.json")
	if err != nil {
		fmt.Printf("Error loading events: %v\n", err)
		return
	}

	// User selects an event and specifies the number of tickets
	eventID, numTickets, err := promptForEvent(events)
	if err != nil {
		fmt.Printf("Error selecting event: %v\n", err)
		return
	}

	// Process each user credential
	for _, cred := range creds {
		processCredential(cred, eventID, numTickets)
	}
}

func loadCredentials(filepath string) ([][4]string, error) {
	file, err := os.Open(filepath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	reader := csv.NewReader(file)
	rawRecords, err := reader.ReadAll()
	if err != nil {
		return nil, err
	}

	// Convert [][]string to [][4]string
	records := make([][4]string, len(rawRecords))
	for i, record := range rawRecords {
		if len(record) != 4 {
			return nil, fmt.Errorf("record on line %d does not have exactly 4 elements", i+1)
		}
		records[i] = [4]string{record[0], record[1], record[2], record[3]}
	}

	return records, nil
}

func loadEvents(filepath string) ([]Event, error) {
	data, err := ioutil.ReadFile(filepath)
	if err != nil {
		return nil, err
	}
	var events []Event
	err = json.Unmarshal(data, &events)
	if err != nil {
		return nil, err
	}
	return events, nil
}

func promptForEvent(events []Event) (int, int, error) {
	reader := bufio.NewReader(os.Stdin)
	for i, event := range events {
		fmt.Printf("[%d] %s (ID: %d, Date: %s)\n", i+1, event.Name, event.ID, event.IDDate)
	}
	fmt.Print("Enter the number of the event you want to book: ")
	indexStr, err := reader.ReadString('\n')
	if err != nil {
		return 0, 0, err
	}
	index, err := strconv.Atoi(strings.TrimSpace(indexStr))
	if err != nil {
		return 0, 0, err
	}

	fmt.Print("Enter the number of tickets to book: ")
	ticketsStr, err := reader.ReadString('\n')
	if err != nil {
		return 0, 0, err
	}
	tickets, err := strconv.Atoi(strings.TrimSpace(ticketsStr))
	if err != nil {
		return 0, 0, err
	}
	return events[index-1].ID, tickets, nil
}

func processCredential(cred [4]string, eventID int, numTickets int) {
	// Initialize the client with the user's email
	client := fixr.NewClient(cred[2]) // cred[2] is assumed to be the email
	if err := client.Logon(cred[3]); err != nil {
		fmt.Printf("logon failed (%v)\n", err)
	}
	// Fetch event details
	event, err := client.Event(eventID)
	if err != nil {
		fmt.Printf("Failed to fetch event %d: %v\n", eventID, err)
		return
	}

	// Allow the user to select the type of ticket
	ticket, err := selectTicket(event.Tickets)
	if err != nil {
		fmt.Printf("Ticket selection error: %v\n", err)
		return
	}

	// Attempt to book the selected number of tickets
	booking, err := client.Book(ticket, numTickets, nil)
	if err != nil {
		fmt.Printf("Failed to book tickets: %v\n", err)
		return
	}

	// Output booking confirmation
	fmt.Printf("Successfully booked tickets: %s\nPDF Ticket: %s\n", booking.Event.Name, booking.PDF)
}

func selectTicket(tickets []fixr.Ticket) (*fixr.Ticket, error) {
	reader := bufio.NewReader(os.Stdin)
	fmt.Println("Available Tickets:")
	for i, t := range tickets {
		fmt.Printf("[%d] %s - £%.2f (Max: %d)\n", i+1, t.Name, t.Price+t.BookingFee, t.Max)
	}

	fmt.Print("Select the number of the ticket you want to purchase: ")
	input, err := reader.ReadString('\n')
	if err != nil {
		return nil, err
	}
	choice, err := strconv.Atoi(strings.TrimSpace(input))
	if err != nil {
		return nil, err
	}
	if choice < 1 || choice > len(tickets) {
		return nil, fmt.Errorf("invalid ticket selection")
	}
	return &tickets[choice-1], nil
}
