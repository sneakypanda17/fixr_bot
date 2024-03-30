import csv
import os

# Assuming __file__ is defined in this context; if not, you might need to adjust this
input_file = os.path.join(os.path.dirname(__file__), "raw_data/surnames.csv")
output_file = os.path.join(os.path.dirname(__file__), "raw_data/surnames2.csv")

# Verify input file exists and is accessible
if not os.path.exists(input_file):
    print(f"Error: The file {input_file} does not exist.")
else:
    # Open the input file in read mode and the output file in write mode
    with open(input_file, mode='r', newline='') as infile, open(output_file, mode='w', newline='') as outfile:
        # Create a CSV reader and writer
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=[field for field in reader.fieldnames if field != 'perct2013'])
        
        # Write the header (field names) to the output file
        writer.writeheader()
        
        # Keep track of the number of rows processed
        rows_processed = 0
        
        # Iterate over each row in the input file
        for row in reader:
            # Remove the 'perct2013' data from the row, if present
            row.pop('perct2013', None)
            # Write the modified row to the output file
            writer.writerow(row)
            rows_processed += 1
        
        if rows_processed > 0:
            print(f"Finished removing the 'perct2013' column. Processed {rows_processed} rows.")
        else:
            print("No rows were processed. Please check the format of your input file.")
