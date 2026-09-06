import os
import requests
from bs4 import BeautifulSoup

# Function to retrieve Wikipedia page content
def get_wikipedia_page(brand_name):
    # Construct the URL for the Wikipedia page
    url = f"https://en.wikipedia.org/wiki/{brand_name}"

    # Send an HTTP GET request to the URL
    response = requests.get(url, headers={"User-Agent": "WikipediaHTMLExample/1.0 (https://example.com)"})

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Function to check if a section title contains specific words
def contains_keywords(section_title, keywords):
    section_title = section_title.lower()
    for keyword in keywords:
        if keyword in section_title:
            return True
    return False

# Main function
def main():
    # Define the keywords to look for in section titles
    keywords = ["advertising", "marketing"]

    # Create or open the strategies.txt file for writing
    with open("strategies.txt", "w", encoding="utf-8") as strategies_file:
        # Open the coffees.txt file for reading
        with open("coffees.txt", "r", encoding="utf-8") as coffees_file:
            # Iterate through each brand name in coffees.txt
            for brand_name in coffees_file:
                brand_name = brand_name.strip()  # Remove leading/trailing whitespace

                # Retrieve the Wikipedia page content
                page_content = get_wikipedia_page(brand_name)

                if page_content:
                    # Parse the HTML content using BeautifulSoup
                    soup = BeautifulSoup(page_content, "html.parser")

                    # Find all section titles (usually enclosed in <span> tags with class "mw-headline")
                    section_titles = soup.find_all("h2")

                    # Iterate through section titles and check for keywords
                    for title in section_titles:
                        section_title = title.text
                        if contains_keywords(section_title, keywords):
                            # Write the brand name and section text to strategies.txt
                            strategies_file.write(f"Brand Name: {brand_name}\n")
                            strategies_file.write(f"Section Title: {section_title}\n")
                            strategies_file.write(f"Section Text: {title.parent.text}\n\n")

if __name__ == "__main__":
    main()