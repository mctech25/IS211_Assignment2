import argparse
import logging
import urllib.request
import csv
import datetime

# Set up logging
def setup_logger():
    logger = logging.getLogger('assignment2')
    logger.setLevel(logging.ERROR)
    handler = logging.FileHandler('errors.log')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

# Function to download data from a URL
def downloadData(url):
    response = urllib.request.urlopen(url)
    return response.read().decode('utf-8')

# Function to process the CSV data
def processData(csv_data, logger):
    reader = csv.reader(csv_data.splitlines())
    person_data = {}
    for line_number, row in enumerate(reader, start=1):
        person_id, name, birthday = row
        try:
            # Attempt to parse the birthday
            birthday_date = datetime.datetime.strptime(birthday, '%d/%m/%Y').date()
            person_data[person_id] = (name, birthday_date)
        except ValueError:
            logger.error(f"Error processing line {line_number} for ID {person_id}")
    return person_data

# Function to display a person's information
def displayPerson(person_id, person_data):
    if person_id in person_data:
        name, birthday = person_data[person_id]
        print(f"Person {person_id} is {name} with a birthday of {birthday.isoformat()}")
    else:
        print("No user found with that id")

# Main function to orchestrate the program
def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Process some CSV data.")
    parser.add_argument('--url', required=True, help='URL of the CSV data')
    args = parser.parse_args()

    # Set up logging
    logger = setup_logger()

    # Download data
    try:
        csv_data = downloadData(args.url)
    except Exception as e:
        print(f"Error downloading data: {e}")
        return

    # Process data
    person_data = processData(csv_data, logger)

    # User input loop
    while True:
        user_input = input("Enter an ID to look up (or 0 to exit): ")
        try:
            person_id = int(user_input)
            if person_id <= 0:
                print("Exiting the program.")
                break
            displayPerson(str(person_id), person_data)
        except ValueError:
            print("Please enter a valid integer.")

if __name__ == "__main__":
    main()
