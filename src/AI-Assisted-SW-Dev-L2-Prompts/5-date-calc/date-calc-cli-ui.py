from datetime import datetime, timedelta


# Function to calculate the number of days between two dates
def calculate_days():
    # Get dates from the user
    date1_str = input("Enter Date 1 (mm/dd/yyyy): ")
    date2_str = input("Enter Date 2 (mm/dd/yyyy): ")

    try:
        # Convert input strings into datetime objects
        date1 = datetime.strptime(date1_str, '%m/%d/%Y')
        date2 = datetime.strptime(date2_str, '%m/%d/%Y')

        # Calculate the difference between dates and add 1 to include both dates
        delta = abs(date2 - date1) + timedelta(days=1)

        # Display result
        print(f"Number of Days: {delta.days}")

    except ValueError:
        print("Invalid date format. Please use mm/dd/yyyy.")


# Start the program
if __name__ == "__main__":
    calculate_days()