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

	"github.com/sneakypanda17/fixr" // Update this import path
)

type Event struct {
	ID      int
	Name    string
	Date    string
	Tickets []fixr.Ticket
}

type Ticket struct {
	ID         int
	Name       string
	Price      float64
	BookingFee float64
	Max        int
	SoldOut    bool
	Expired    bool
	Invalid    bool
}

func main() {
	// Load events from a JSON file
	events, err := loadEvents("../web_scraper/events.json")
	if err != nil {
		fmt.Println("Error loading events:", err)
		return
	}

	// Prompt user for event and ticket selection
	eventID, ticketType, err := promptForEventAndTicket(events)
	if err != nil {
		fmt.Println("Error selecting event or ticket:", err)
		return
	}

	// Prompt user for ticket quantity
	numTickets, err := promptForTicketQuantity()
	if err != nil {
		fmt.Println("Error selecting ticket quantity:", err)
		return
	}

	// Load credentials
	creds, err := loadCredentials("../account_creation/unused_accounts.csv")
	if err != nil {
		fmt.Println("Error loading credentials:", err)
		return
	}

	// Log in with the first account to fetch ticket ID
	ticketID, err := fetchTicketID(creds[0], eventID, ticketType)
	if err != nil {
		fmt.Println("Error fetching ticket ID:", err)
		return
	}

	// Attempt to book tickets using the fetched ticket ID
	bookTickets(creds, eventID, numTickets, ticketID)
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

func loadCredentials(filepath string) ([][6]string, error) {
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

	var records [][6]string
	for i, record := range rawRecords {
		if len(record) != 6 {
			return nil, fmt.Errorf("record on line %d does not have exactly 6 elements, got %d", i+1, len(record))
		}
		records = append(records, [6]string{record[0], record[1], record[2], record[3], record[4], record[5]})
	}

	return records, nil
}

func promptForEventAndTicket(events []Event) (int, string, error) {
	reader := bufio.NewReader(os.Stdin)

	fmt.Println("Available Events:")
	for i, event := range events {
		fmt.Printf("[%d] %s (ID: %d, Date: %s)\n", i+1, event.Name, event.ID, event.Date)
	}
	fmt.Print("Enter the number of the event you want to book: ")
	eventIndexStr, err := reader.ReadString('\n')
	if err != nil {
		return 0, "", err
	}
	eventIndex, err := strconv.Atoi(strings.TrimSpace(eventIndexStr))
	if err != nil {
		return 0, "", err
	}
	if eventIndex < 1 || eventIndex > len(events) {
		return 0, "", fmt.Errorf("invalid event selection")
	}
	selectedEvent := events[eventIndex-1]

	fmt.Println("Available Tickets:")
	for i, t := range selectedEvent.Tickets {
		fmt.Printf("[%d] %s - £%.2f (Max: %d)\n", i+1, t.Name, t.Price+t.BookingFee, t.Max)
	}
	fmt.Print("Select the number of the ticket you want to purchase: ")
	ticketIndexStr, err := reader.ReadString('\n')
	if err != nil {
		return 0, "", err
	}
	ticketIndex, err := strconv.Atoi(strings.TrimSpace(ticketIndexStr))
	if err != nil {
		return 0, "", err
	}
	if ticketIndex < 1 || ticketIndex > len(selectedEvent.Tickets) {
		return 0, "", fmt.Errorf("invalid ticket selection")
	}
	selectedTicket := selectedEvent.Tickets[ticketIndex-1]

	return selectedEvent.ID, selectedTicket.Name, nil
}

func promptForTicketQuantity() (int, error) {
	reader := bufio.NewReader(os.Stdin)
	fmt.Print("Enter the number of tickets to book: ")
	ticketsStr, err := reader.ReadString('\n')
	if err != nil {
		return 0, err
	}
	numTickets, err := strconv.Atoi(strings.TrimSpace(ticketsStr))
	if err != nil {
		return 0, err
	}
	return numTickets, nil
}

func fetchTicketID(cred [6]string, eventID int, ticketType string) (int, error) {
	client := fixr.NewClient(cred[2])             // cred[2] is the email
	if err := client.Logon(cred[3]); err != nil { // cred[3] is the password
		return 0, fmt.Errorf("logon failed for %s: %v", cred[2], err)
	}

	event, err := client.Event(eventID)
	if err != nil {
		return 0, fmt.Errorf("failed to fetch event %d: %v", eventID, err)
	}

	for _, t := range event.Tickets {
		if t.Name == ticketType && !t.SoldOut && !t.Expired && !t.Invalid {
			return t.ID, nil
		}
	}
	return 0, fmt.Errorf("ticket type %s not found or unavailable for event %d", ticketType, eventID)
}

func bookTickets(creds [][6]string, eventID, numTickets, ticketID int) {
	for i, cred := range creds {
		if i >= numTickets {
			break // Only book as many tickets as requested
		}
		client := fixr.NewClient(cred[2])             // cred[2] is the email
		if err := client.Logon(cred[3]); err != nil { // cred[3] is the password
			fmt.Printf("Logon failed for %s: %v\n", cred[2], err)
			continue
		}

		ticket, err := client.GetTicket(ticketID)
		if err != nil {
			fmt.Printf("Failed to fetch ticket %d: %v\n", ticketID, err)
			continue
		}

		_, err = client.Book(ticket, 1, nil)
		if err != nil {
			fmt.Printf("Failed to book ticket for %s: %v\n", cred[2], err)
		} else {
			fmt.Printf("Successfully booked ticket for %s\n", cred[2])
		}
	}
}
