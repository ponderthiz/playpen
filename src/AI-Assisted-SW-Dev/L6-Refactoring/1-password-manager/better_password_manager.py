import json
import secrets
import string

from cryptography.fernet import Fernet
from nicegui import ui


class PasswordManager:
    def __init__(self):
        self.load_encryption_key()
        self.load_passwords()

        self.create_widgets()

    def load_encryption_key(self):
        # Check if the key file exists
        try:
            with open("key.key", "rb") as key_file:
                self.encryption_key = key_file.read()

        except FileNotFoundError:
            # Generate a new key if it doesn't exist
            self.encryption_key = Fernet.generate_key()

            with open("key.key", "wb") as key_file:
                key_file.write(self.encryption_key)

        self.cipher_suite = Fernet(self.encryption_key)

    def load_passwords(self):
        try:
            with open("passwords.json", "r") as f:
                self.passwords = json.load(f)

        except (json.JSONDecodeError, FileNotFoundError):
            self.passwords = {}

    def save_passwords(self):
        with open("passwords.json", "w") as f:
            json.dump(self.passwords, f, indent=4)

    def generate_password(self):
        password_length = 12

        characters = (
            string.ascii_letters
            + string.digits
            + string.punctuation
        )

        # Generate a secure random password
        password = "".join(
            secrets.choice(characters)
            for _ in range(password_length)
        )

        # Encrypt the password
        encrypted_password = self.cipher_suite.encrypt(
            password.encode()
        )

        # Get URL and username from the GUI
        url = self.url_input.value
        username = self.username_input.value

        # Make sure the user entered both fields
        if not url or not username:
            ui.notify(
                "Please enter both a URL and username.",
                type="warning"
            )
            return

        # Save the password
        self.passwords[url] = {
            "username": username,
            "password": encrypted_password.decode()
        }

        self.save_passwords()

        # Close the dialog
        self.create_dialog.close()

        # Refresh the URL list
        self.update_url_list()

        ui.notify(
            f"Password created for {url}",
            type="positive"
        )

    def open_screen2(self):
        # Clear previous values
        self.url_input.value = ""
        self.username_input.value = ""

        # Open the create-password dialog
        self.create_dialog.open()

    def open_screen3(self, url):
        try:
            # Retrieve the encrypted password
            encrypted_password = (
                self.passwords[url]["password"].encode()
            )

            # Decrypt the password
            decrypted_password = (
                self.cipher_suite
                .decrypt(encrypted_password)
                .decode()
            )

            username = self.passwords[url]["username"]

            # Update the dialog contents
            self.password_url_label.set_text(
                f"URL: {url}"
            )

            self.password_username_label.set_text(
                f"Username: {username}"
            )

            self.password_value_label.set_text(
                f"Password: {decrypted_password}"
            )

            # Open the password dialog
            self.password_dialog.open()

        except Exception as error:
            ui.notify(
                f"Error opening password: {error}",
                type="negative"
            )

    def update_url_list(self):
        # Remove the existing URL buttons
        self.url_list.clear()

        if not self.passwords:
            with self.url_list:
                ui.label(
                    "No saved passwords."
                ).classes("text-gray-500")

            return

        # Create a button for each saved URL
        with self.url_list:
            for url in self.passwords:
                ui.button(
                    url,
                    on_click=lambda url=url:
                        self.open_screen3(url)
                ).classes(
                    "w-full justify-start"
                )

    def create_widgets(self):
        # -------------------------------------------------
        # Main page
        # -------------------------------------------------

        ui.label(
            "Password Manager"
        ).classes(
            "text-3xl font-bold mb-6"
        )

        ui.label(
            "Saved Passwords"
        ).classes(
            "text-xl font-bold mb-2"
        )

        # Container for saved URLs
        self.url_list = ui.column().classes(
            "w-full gap-2"
        )

        self.update_url_list()

        # Main buttons
        with ui.row().classes("mt-6"):

            ui.button(
                "Create New",
                on_click=self.open_screen2
            )

            ui.button(
                "Close",
                on_click=self.close_application
            )

        # -------------------------------------------------
        # Create New Password Dialog
        # -------------------------------------------------

        with ui.dialog() as self.create_dialog:

            with ui.card().classes("w-96"):

                ui.label(
                    "Create New Password"
                ).classes(
                    "text-xl font-bold mb-4"
                )

                self.url_input = ui.input(
                    label="URL",
                    placeholder="https://example.com"
                ).classes("w-full")

                self.username_input = ui.input(
                    label="Username"
                ).classes("w-full")

                with ui.row().classes("mt-4"):

                    ui.button(
                        "Generate Password",
                        on_click=self.generate_password
                    )

                    ui.button(
                        "Cancel",
                        on_click=self.create_dialog.close
                    )

        # -------------------------------------------------
        # View Password Dialog
        # -------------------------------------------------

        with ui.dialog() as self.password_dialog:

            with ui.card().classes("w-96"):

                ui.label(
                    "Password Details"
                ).classes(
                    "text-xl font-bold mb-4"
                )

                self.password_url_label = ui.label(
                    "URL:"
                )

                self.password_username_label = ui.label(
                    "Username:"
                )

                self.password_value_label = ui.label(
                    "Password:"
                )

                ui.button(
                    "Close",
                    on_click=self.password_dialog.close
                ).classes("mt-4")

    def close_application(self):
        ui.notify(
            "You can close this browser tab."
        )


# Create the password manager
app = PasswordManager()


# Start the NiceGUI server
ui.run(
    host="0.0.0.0",
    port=8080
)
