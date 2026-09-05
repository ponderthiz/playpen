import os
import sys
import pandas as pd


def get_valid_file(prompt: str) -> str:
    """Prompt user until a valid existing file path is entered."""
    while True:
        filepath = input(prompt).strip().strip("'\"")
        if os.path.isfile(filepath):
            return filepath
        print(f"Error: File '{filepath}' not found. Please try again.\n")


def display_columns(columns: list[str], label: str):
    """Display numbered list of column headers."""
    print(f"\n--- Column Headers for {label} ---")
    for idx, col in enumerate(columns, start=1):
        print(f"  [{idx}] {col}")
    print()


def choose_column(columns: list[str], label: str) -> str:
    """Prompt user to choose a column by number or exact name."""
    display_columns(columns, label)
    while True:
        choice = input(f"Select column to merge on for {label} (number or name): ").strip()

        # Check if choice is a valid number index
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(columns):
                return columns[idx - 1]

        # Check if choice is an exact column name match
        if choice in columns:
            return choice

        print(f"Invalid selection: '{choice}'. Enter a valid number between 1 and {len(columns)} or exact column name.")


def main():
    print("=== Excel File Merger ===\n")

    # 1. Ask the user for the names of the files
    file1 = get_valid_file("Enter the path for the first Excel file: ")
    file2 = get_valid_file("Enter the path for the second Excel file: ")

    try:
        print("\nLoading spreadsheets...")
        df1 = pd.read_excel(file1)
        df2 = pd.read_excel(file2)
    except Exception as e:
        print(f"Error reading Excel files: {e}")
        sys.exit(1)

    cols1 = list(df1.columns)
    cols2 = list(df2.columns)

    if not cols1 or not cols2:
        print("Error: One of the files has no columns to merge on.")
        sys.exit(1)

    # 2 & 3. List column headers and ask user to select merge column from each sheet
    key1 = choose_column(cols1, f"File 1 ({os.path.basename(file1)})")
    key2 = choose_column(cols2, f"File 2 ({os.path.basename(file2)})")

    # Optional: Select join type (defaults to inner)
    print("\nSelect join type:")
    print("  [1] Inner  - Keep only rows with matching keys in both files (default)")
    print("  [2] Left   - Keep all rows from File 1")
    print("  [3] Right  - Keep all rows from File 2")
    print("  [4] Outer  - Keep all rows from both files")
    join_choice = input("Enter choice (1-4, press Enter for Inner): ").strip()

    how_map = {"1": "inner", "2": "left", "3": "right", "4": "outer"}
    how = how_map.get(join_choice, "inner")

    # 4. Perform the merge
    print(f"\nMerging on '{key1}' (File 1) and '{key2}' (File 2) using a '{how}' join...")
    merged_df = pd.merge(
        df1,
        df2,
        left_on=key1,
        right_on=key2,
        how=how,
        suffixes=("_file1", "_file2")
    )

    # Ask for output filename
    default_out = "merged_output.xlsx"
    out_name = input(f"\nEnter output filename (press Enter for '{default_out}'): ").strip()
    if not out_name:
        out_name = default_out
    if not out_name.endswith(".xlsx"):
        out_name += ".xlsx"

    # Export
    try:
        merged_df.to_excel(out_name, index=False)
        print(f"\nSuccess! Merged spreadsheet written to: {os.path.abspath(out_name)}")
        print(f"Total rows in merged file: {len(merged_df)}")
    except Exception as e:
        print(f"Error saving output file: {e}")


if __name__ == "__main__":
    main()