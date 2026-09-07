from datetime import datetime
from zoneinfo import available_timezones

from nicegui import ui


from timezone_converter import convert_timezone


# Get available time zones
timezones = sorted(available_timezones())


def convert_button_click():
    try:
        # Get the values from the GUI
        entered_time = time_input_box.value
        source_timezone = from_timezone_box.value
        destination_timezone = to_timezone_box.value

        # Convert the entered text to a datetime object
        parsed_datetime = datetime.strptime(
            entered_time,
            "%Y-%m-%d %H:%M:%S"
        )

        # Convert the time
        converted_datetime = convert_timezone(
            parsed_datetime,
            source_timezone,
            destination_timezone
        )

        # Display the result
        output_label.set_text(
            f"Converted Time: "
            f"{converted_datetime.strftime('%Y-%m-%d %H:%M:%S %Z')}"
        )

    except ValueError:
        output_label.set_text(
            "Invalid input. Please use YYYY-MM-DD HH:MM:SS."
        )

    except Exception as error:
        output_label.set_text(
            f"Error: {error}"
        )


# Page title
ui.label("Time Zone Converter").classes(
    "text-3xl font-bold mb-4"
)


# Date and time input
time_input_box = ui.input(
    label="Enter Date and Time",
    placeholder="YYYY-MM-DD HH:MM:SS",
    value="2026-09-06 10:30:00"
).classes("w-full")


# From time zone
from_timezone_box = ui.select(
    options=timezones,
    label="From Time Zone",
    value="UTC"
).classes("w-full")


# To time zone
to_timezone_box = ui.select(
    options=timezones,
    label="To Time Zone",
    value="America/New_York"
).classes("w-full")


# Convert button
ui.button(
    "Convert",
    on_click=convert_button_click
).classes("mt-4")


# Output
output_label = ui.label(
    "Converted Time:"
).classes("text-lg mt-4")


# Start the NiceGUI web server
ui.run(
    host="0.0.0.0",
    port=8080
)
