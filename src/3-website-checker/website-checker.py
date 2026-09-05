import requests

# Function to check if a website is up
def is_website_up(url):
    try:
        response = requests.get(url)
        # print(url, response.status_code)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# Function to add 'http://' or 'https://' to a URL if missing
def format_url(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    return url

# Read addresses from the text file
with open('addresses.txt', 'r') as file:
    addresses = file.read().splitlines()

# Check the status of each website
for address in addresses:
    formatted_address = format_url(address)
    if is_website_up(formatted_address):
        print(formatted_address, "up")
    else:
        print(formatted_address, "down")