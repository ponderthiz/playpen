import re  # Import the regular expression module

# Define a function to perform email validation
def validate_email(email):
    # Define a regular expression pattern for a valid email address
    pattern = r'^[\w\.-]+@[\w\.-]+$'
    
    # Create a regular expression object and set the IgnoreCase flag to True
    myReg = re.compile(pattern, re.IGNORECASE)
    
    # Use the regular expression's search method to check if the email matches the pattern
    if myReg.search(email):
        return True  # Email is valid
    else:
        return False  # Email is not valid

# Prompt the user to enter an email address
email = input("Enter an email address: ")

# Call the validate_email function with the user-provided email and display the result
result = validate_email(email)
print("The result of validation checking:", result)