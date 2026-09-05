import tkinter as tk
from datetime import datetime, timedelta

# Function to calculate the number of days between two dates
def calculate_days():
    date1_str = entry_date1.get()
    date2_str = entry_date2.get()

    try:
        # Convert the input date strings to datetime objects
        date1 = datetime.strptime(date1_str, '%m/%d/%Y')
        date2 = datetime.strptime(date2_str, '%m/%d/%Y')

        # Calculate the absolute difference in days between the two dates and subtract 1
        delta = abs(date2 - date1) + timedelta(days=1)

        # Update the result label with the number of days
        result_label.config(text=f'Number of Days: {delta.days}')
    except ValueError:
        result_label.config(text='Invalid date format. Use mm/dd/yyyy.')

# Create the main window
root = tk.Tk()
root.title('Date Calculator')

# Create and place labels and entry fields for date input
label_date1 = tk.Label(root, text='Enter Date 1 (mm/dd/yyyy):')
label_date1.pack()
entry_date1 = tk.Entry(root)
entry_date1.pack()

label_date2 = tk.Label(root, text='Enter Date 2 (mm/dd/yyyy):')
label_date2.pack()
entry_date2 = tk.Entry(root)
entry_date2.pack()

# Create a button to calculate the days between the dates
calculate_button = tk.Button(root, text='Calculate', command=calculate_days)
calculate_button.pack()

# Create a label to display the result
result_label = tk.Label(root, text='')
result_label.pack()

# Start the GUI main loop
root.mainloop()