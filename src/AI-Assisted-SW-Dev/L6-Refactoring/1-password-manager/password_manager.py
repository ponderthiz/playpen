import json

from cryptography.fernet import Fernet
from nicegui import ui


# Encryption key
# NOTE: In a real password manager, this key should NOT be hard-coded.
encryption_key = b"ipq-LBY9YAMjiM-V_PPAxIOD5elZso09Yg0UhjUVUNY="
cipher_suite = Fernet(encryption_key)


# Load existing passwords
try:
    with open("password.txt", "r") as f:
        passwords = json.load(f)
except (json.JSONDecodeError, FileNotFoundError):
    passwords = {}


def save_password(url, username, password):
    """
    Save a password entry to password.txt.
    """

    passwords[url] = {
        "username": username,
        "password": password.decode()
    }

    with open("password.txt", "w") as f:
        json.dump(passwords, f, indent=4)


def generate_password():
    """
    Encrypt and save the new password.
    """

    url = url_input.value
    username = username_input.value

    # This preserves the behavior of the original exercise.
    password = b"generated_password_here"

    encrypted_password = cipher_suite.encrypt(password)

    save_password(
        url,
        username,
        encrypted_password
    )

    # Close the create-password dialog
    create_dialog.close()

    # Refresh the URL list
    update_url_list()

    ui.notify(
        f"Password saved for {url}",
        type="positive"
    )


def open_create_dialog():
    """
    Open the dialog for creating a new password.
    """

    url_input.value = ""
    username_input.value = ""

    create_dialog.open()


def open_password_dialog(url):
    """
    Decrypt and display the password for the selected URL.
    """

    try:
        encrypted_password = passwords[url]["password"].encode()

        decrypted_password = cipher_suite.decrypt(
            encrypted_password
        ).decode()

        username = passwords[url]["username"]

        password_url_label.set_text(
            f"URL: {url}"
        )

        password_username_label.set_text(
            f"Username: {username}"
        )

        password_value_label.set_text(
            f"Password: {decrypted_password}"
        )

        password_dialog.open()

    except Exception as error:
        ui.notify(
            f"Error opening password: {error}",
            type="negative"
        )


def update_url_list():
    """
    Rebuild the list of saved URLs.
    """

    url_list.clear()

    if not passwords:
        ui.label("No saved passwords yet.").classes(
            "text-gray-500"
        )
        return

    for url in passwords:
        with url_list:
            ui.button(
                url,
                on_click=lambda url=url: open_password_dialog(url)
            ).classes("w-full justify-start")


# ---------------------------------------------------------
# Main page
# ---------------------------------------------------------

ui.label("Password Manager").classes(
    "text-3xl font-bold mb-6"
)


# Saved URLs
ui.label("Saved Passwords").classes(
    "text-xl font-bold"
)

url_list = ui.column().classes(
    "w-full gap-2"
)


# Buttons
with ui.row().classes("mt-6"):
    ui.button(
        "Create New",
        on_click=open_create_dialog
    )

    ui.button(
        "Close",
        on_click=lambda: ui.notify(
            "You can close this browser tab."
        )
    )


# ---------------------------------------------------------
# Create New Password Dialog
# ---------------------------------------------------------

with ui.dialog() as create_dialog:
    with ui.card().classes("w-96"):

        ui.label(
            "Create New Password"
        ).classes("text-xl font-bold")

        url_input = ui.input(
            label="URL"
        ).classes("w-full")

        username_input = ui.input(
            label="Username"
        ).classes("w-full")

        ui.button(
            "Generate Password",
            on_click=generate_password
        ).classes("mt-4")


# ---------------------------------------------------------
# View Password Dialog
# ---------------------------------------------------------

with ui.dialog() as password_dialog:
    with ui.card().classes("w-96"):

        ui.label(
            "Password Details"
        ).classes("text-xl font-bold")

        password_url_label = ui.label(
            "URL:"
        )

        password_username_label = ui.label(
            "Username:"
        )

        password_value_label = ui.label(
            "Password:"
        )

        ui.button(
            "Close",
            on_click=password_dialog.close
        ).classes("mt-4")


# Populate the URL list
update_url_list()


# Start NiceGUI
ui.run(
    host="0.0.0.0",
    port=8080
)