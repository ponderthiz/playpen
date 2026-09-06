import wikipediaapi

# Create a Wikipedia API object
wiki_wiki = wikipediaapi.Wikipedia(
    user_agent="CoffeeSalesResearch/1.0 (student@example.com)",
    language="en"
)

# Function to check if a page has a section containing specific keywords
def has_keywords_section(page, keywords):
    for section in page.sections:
        section_title = section.title.lower()
        for keyword in keywords:
            if keyword in section_title:
                return True, section.text
    return False, None

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

                # Retrieve the Wikipedia page for the brand
                page = wiki_wiki.page(brand_name)

                # Check if the page has a section with the keywords
                has_keywords, section_text = has_keywords_section(page, keywords)

                if has_keywords:
                    # Write the brand name, section title, and section text to strategies.txt
                    strategies_file.write(f"Brand Name: {brand_name}\n")
                    strategies_file.write(f"Section Title: {keywords}\n")
                    strategies_file.write(f"Section Text:\n{section_text}\n\n")

if __name__ == "__main__":
    main()