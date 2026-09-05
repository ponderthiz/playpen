import os
import re


def search_keyword_in_file():
    # Get user input
    input_file = input("Enter the input file name: ")
    keyword = input("Enter the keyword to search for: ")
    output_file = input("Enter the output file name: ")

    # Check if input file exists
    if not os.path.exists(input_file):
        print("Input file does not exist.")
        return

    matches = []

    try:
        # Read the input file
        with open(input_file, "r", encoding="utf-8") as file:
            text = file.read()

        # Split text into sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)

        # Search for keyword
        for sentence in sentences:
            if keyword.lower() in sentence.lower():
                matches.append(sentence.strip())

        # Write results to output file
        with open(output_file, "w", encoding="utf-8") as file:
            for sentence in matches:
                file.write(sentence + "\n")

        print(f"Search complete. {len(matches)} matching sentences written to {output_file}.")

    except Exception as e:
        print(f"An error occurred: {e}")


# Run program
if __name__ == "__main__":
    search_keyword_in_file()