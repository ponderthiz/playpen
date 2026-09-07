import pytz
from datetime import datetime

def convert_timezone(input_time, from_timezone, to_timezone):
    try:
        # Check if input_time is a valid datetime object
        if not isinstance(input_time, datetime):
            raise ValueError("Invalid input time")

        # Create a datetime object from the input time in the 'from_timezone'
        from_timezone_obj = pytz.timezone(from_timezone)
        input_time = from_timezone_obj.localize(input_time)

        # Convert the datetime object to the 'to_timezone'
        to_timezone_obj = pytz.timezone(to_timezone)
        converted_time = input_time.astimezone(to_timezone_obj)

        return converted_time

    except pytz.exceptions.UnknownTimeZoneError:
        return "Invalid time zone provided"
    except ValueError as e:
        return str(e)

# Example usage:
if __name__ == "__main__":
    # Input time in 'from_timezone' (UTC)
    input_time = datetime(2023, 9, 18, 12, 0, 0)  # Replace with your desired time

    # Convert from UTC to US/Pacific time zone
    from_timezone = 'UTC'
    to_timezone = 'US/Pacific'

    converted_time = convert_timezone(input_time, from_timezone, to_timezone)
    print(f"Converted time: {converted_time}")