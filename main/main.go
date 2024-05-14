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
	"time"

	"github.com/sneakypanda17/fixr" // Update this import path
)

type Event struct {
	ID      int
	Name    string
	Date    string
	Tickets []Ticket
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
	eventID, numTickets, ticketType, err := promptForEventAndTicket(events)
	if err != nil {
		fmt.Println("Error selecting event or ticket:", err)
		return
	}

	// Load credentials
	creds, err := loadCredentials("credentials.csv")
	if err != nil {
		fmt.Println("Error loading credentials:", err)
		return
	}

	// Channel to collect successful bookings
	successChan := make(chan [7]string)

	// Attempt to book tickets
	go bookTickets(creds, eventID, numTickets, ticketType, successChan)

	// Collect successful bookings and write to a new CSV
	writeSuccessesToFile(successChan)
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

func promptForEventAndTicket(events []Event) (int, int, string, error) {
	reader := bufio.NewReader(os.Stdin)

	fmt.Println("Available Events:")
	for i, event := range events {
		fmt.Printf("[%d] %s (ID: %d, Date: %s)\n", i+1, event.Name, event.ID, event.Date)
	}
	fmt.Print("Enter the number of the event you want to book: ")
	eventIndexStr, err := reader.ReadString('\n')
	if err != nil {
		return 0, 0, "", err
	}
	eventIndex, err := strconv.Atoi(strings.TrimSpace(eventIndexStr))
	if err != nil {
		return 0, 0, "", err
	}
	if eventIndex < 1 || eventIndex > len(events) {
		return 0, 0, "", fmt.Errorf("invalid event selection")
	}
	selectedEvent := events[eventIndex-1]

	fmt.Print("Enter the number of tickets to book: ")
	ticketsStr, err := reader.ReadString('\n')
	if err != nil {
		return 0, 0, "", err
	}
	numTickets, err := strconv.Atoi(strings.TrimSpace(ticketsStr))
	if err != nil {
		return 0, 0, "", err
	}

	fmt.Println("Available Tickets:")
	for i, t := range selectedEvent.Tickets {
		fmt.Printf("[%d] %s - £%.2f (Max: %d)\n", i+1, t.Name, t.Price+t.BookingFee, t.Max)
	}
	fmt.Print("Select the number of the ticket you want to purchase: ")
	ticketIndexStr, err := reader.ReadString('\n')
	if err != nil {
		return 0, 0, "", err
	}
	ticketIndex, err := strconv.Atoi(strings.TrimSpace(ticketIndexStr))
	if err != nil {
		return 0, 0, "", err
	}
	if ticketIndex < 1 || ticketIndex > len(selectedEvent.Tickets) {
		return 0, 0, "", fmt.Errorf("invalid ticket selection")
	}
	selectedTicket := selectedEvent.Tickets[ticketIndex-1]

	return selectedEvent.ID, numTickets, selectedTicket.Name, nil
}

func bookTickets(creds [][6]string, eventID, numTickets int, ticketType string, successChan chan [7]string) {
	for _, cred := range creds {
		go func(cred [6]string) {
			client := fixr.NewClient(cred[2])             // cred[2] is the email
			if err := client.Logon(cred[3]); err != nil { // cred[3] is the password
				fmt.Printf("Logon failed for %s: %v\n", cred[2], err)
				return
			}

			event, err := client.Event(eventID)
			if err != nil {
				fmt.Printf("Failed to fetch event %d: %v\n", eventID, err)
				return
			}

			var ticket *fixr.Ticket
			for _, t := range event.Tickets {
				if t.Name == ticketType {
					ticket = &t
					break
				}
			}
			if ticket == nil {
				fmt.Printf("Ticket type %s not found for event %d\n", ticketType, eventID)
				return
			}

			// Retry mechanism until the first successful booking
			for {
				booking, err := client.Book(ticket, 1, nil)
				if err == nil {
					fmt.Printf("Successfully booked 1 ticket for %s\n", cred[2])
					successChan <- [7]string{cred[0], cred[1], cred[2], cred[4], cred[5], ticketType, booking.PDF}
					break
				}
				fmt.Printf("Retrying booking for %s: %v\n", cred[2], err)
				time.Sleep(5 * time.Second) // Adjust retry interval as needed
			}

			// Attempt to book the remaining tickets
			remainingTickets := numTickets - 1
			if remainingTickets > 0 {
				booking, err := client.Book(ticket, remainingTickets, nil)
				if err == nil {
					fmt.Printf("Successfully booked %d tickets for %s\n", remainingTickets, cred[2])
					successChan <- [7]string{cred[0], cred[1], cred[2], cred[4], cred[5], ticketType, booking.PDF}
				} else {
					fmt.Printf("Failed to book remaining %d tickets for %s: %v\n", remainingTickets, cred[2], err)
				}
			}
		}(cred)
	}
}

func writeSuccessesToFile(successChan chan [7]string) {
	file, err := os.Create("successful_purchases.csv")
	if err != nil {
		fmt.Println("Error creating successful_purchases.csv:", err)
		return
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	// Write header
	writer.Write([]string{"First Name", "Last Name", "Email", "Birthday", "Phone Number", "Ticket Type", "PDF URL"})

	for success := range successChan {
		writer.Write(success[:])
	}
}
