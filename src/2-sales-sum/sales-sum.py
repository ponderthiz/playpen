import os
import shutil
from datetime import datetime


def sum_sales_files():
    # Current date in YYYYMMDD format
    date_string = datetime.now().strftime("%Y%m%d")

    # Folder paths
    input_folder = "input"
    output_folder = "output"
    processed_folder = os.path.join(output_folder, f"processed-{date_string}")

    # Output file name
    output_file = os.path.join(
        output_folder,
        f"sales-sum-{date_string}.txt"
    )

    # Create required folders if they do not exist
    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(processed_folder, exist_ok=True)

    results = []

    # Process every text file in the input directory
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):

            file_path = os.path.join(input_folder, filename)
            total = 0

            # Read file and sum valid numbers
            with open(file_path, "r") as file:
                for line in file:
                    try:
                        number = int(line.strip())
                        total += number
                    except ValueError:
                        # Ignore lines that are not numbers
                        continue

            results.append((total, filename))

            # Move processed file
            destination = os.path.join(processed_folder, filename)
            shutil.move(file_path, destination)

    # Nothing to write if no files were processed
    if not results:
        return

    # Determine longest sum length for alignment
    max_sum_length = max(len(str(total)) for total, _ in results)

    # Append results to output file
    with open(output_file, "a") as file:
        for total, filename in results:
            spacing = "\t\t"

            # Add extra tab if needed to align filenames
            padding = max_sum_length - len(str(total))

            file.write(
                f"{total}{' ' * padding}{spacing}{filename}\n"
            )


if __name__ == "__main__":
    sum_sales_files()