package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"strconv"
	"strings"

	"github.com/andlabs/ui"
)

type TicketType struct {
	Date string
}

func main() {
	// Call the function from the script
	getEvents()

	// Run the application with a path to the JSON
	jsonFilePath := "../web_scraper/events.json"
	app := NewTicketApp(jsonFilePath)
	app.Run()
}

func getEvents() {
	modulePath := "../web_scraper"
	if !strings.Contains(os.Getenv("GOPATH"), modulePath) {
		os.Setenv("GOPATH", filepath.Join(os.Getenv("GOPATH"), modulePath))
	}
	// Call the function from the script
	// get_events.main()
}

type TicketApp struct {
	window         *ui.Window
	ticketTypes    []TicketType
	ticketQuantity int
}

func NewTicketApp(jsonPath string) *TicketApp {
	app := &TicketApp{}

	// Read dates from JSON at a given path
	app.ticketTypes = app.readTicketTypes(jsonPath)

	// Create widgets
	app.createWidgets()

	return app
}

func (app *TicketApp) readTicketTypes(filepath string) []TicketType {
	var types []TicketType
	data, err := ioutil.ReadFile(filepath)
	if err != nil {
		log.Printf("Error reading file: %v", err)
		return types
	}

	var jsonData []map[string]interface{}
	err = json.Unmarshal(data, &jsonData)
	if err != nil {
		log.Printf("Error decoding JSON: %v", err)
		return types
	}

	for _, item := range jsonData {
		if date, ok := item["date"].(string); ok {
			types = append(types, TicketType{Date: date})
		}
	}

	return types
}

func (app *TicketApp) createWidgets() {
	// Create the main window
	app.window = ui.NewWindow("Ticket Purchase App", 300, 200, false)
	app.window.SetMargined(true)

	// Create the ticket type dropdown
	ticketTypeBox := ui.NewVerticalBox()
	ticketTypeLabel := ui.NewLabel("Select Date:")
	ticketTypeBox.Append(ticketTypeLabel, false)

	ticketTypeCombo := ui.NewCombobox()
	for _, ticketType := range app.ticketTypes {
		ticketTypeCombo.Append(ticketType.Date)
	}
	ticketTypeBox.Append(ticketTypeCombo, false)

	// Create the ticket quantity entry
	quantityBox := ui.NewVerticalBox()
	quantityLabel := ui.NewLabel("Enter Quantity:")
	quantityBox.Append(quantityLabel, false)

	quantityEntry := ui.NewEntry()
	quantityBox.Append(quantityEntry, false)

	// Create the purchase button
	purchaseButton := ui.NewButton("Purchase")
	purchaseButton.OnClicked(func(*ui.Button) {
		selectedType := ticketTypeCombo.Selected()
		quantity, _ := strconv.Atoi(quantityEntry.Text())
		message := fmt.Sprintf("You have purchased %d tickets for the date %s.", quantity, app.ticketTypes[selectedType].Date)
		ui.MsgBox(app.window, "Purchase Confirmation", message)
	})

	// Add the widgets to the main window
	mainBox := ui.NewVerticalBox()
	mainBox.Append(ticketTypeBox, false)
	mainBox.Append(quantityBox, false)
	mainBox.Append(purchaseButton, false)
	app.window.SetChild(mainBox)
}

func (app *TicketApp) Run() {
	ui.Main(func() {
		app.window.Show()
	})
}
