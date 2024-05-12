package main

import (
	"encoding/csv"
	"fmt"
	"os"
)

func main() {
	// Load user credentials from CSV
	creds, err := loadCredentials("credentials.csv")
	if err != nil {
		fmt.Println("Error loading credentials:", err)
		return
	}

	// Process each credential
	for _, cred := range creds {
		processCredential(cred)
	}
}

func loadCredentials(filepath string) ([][4]string, error) {
	// Open the CSV file
	file, err := os.Open(filepath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	// Read CSV file
	reader := csv.NewReader(file)
	records, err := reader.ReadAll()
	if err != nil {
		return nil, err
	}

	return records, nil
}

func processCredential(cred [4]string) {
	// Here we will log in and book tickets
	fmt.Println("Processing:", cred)
	// Placeholder for actual processing logic
}
