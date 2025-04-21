import os
import time
import json
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import psutil
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from cryptography.fernet import Fernet

PROFILE_FILE = "profiles.json"  # Profile file for storing and retrieving profiles (encrypted)
KEY_FILE = "key.key"  # Encryption key for encrypting and decrypting profile data
MULTIBLOXY = os.path.join("MultiBloxy", "MultiBloxy.exe")  # MultiBloxy executable file for multi-instance support
CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def generate_key():
    """
    Generates and save a key for encryption. This should only be done once and the key is stored in the KEY_FILE.

    :raises OSError: If the app doesn't have permission to write the file, the directory is read-only, or there is insufficient space on the device.
    """
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)

def load_key():
    """
    Checks if the encryption key file exists. If it does, the key is loaded from the KEY_FILE and returned. If the file does not exist, a new encryption key is generated, saved to the file, and then returned.

    :return: The encryption key loaded from the KEY_FILE.
    :rtype: bytes
    """
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as key_file:
            return key_file.read()
    else:
        generate_key()  # Generate the key if it doesn't exist
        return load_key()

# Create a Fernet cipher instance using the loaded key
cipher = Fernet(load_key())

def encrypt_data(data):
    """
    Encrypt the profile data.

    :param data: The data to be encrypted (string format).
    :type data: str
    :return: The encrypted data.
    :rtype: bytes
    :raises TypeError: If the input data is not a string.
    """
    return cipher.encrypt(data.encode())

def decrypt_data(encrypted_data):
    """
    Decrypt the profile data.

    :param encrypted_data: The encrypted data.
    :type encrypted_data: bytes
    :return: The decrypted string data.
    :rtype: str
    """
    return cipher.decrypt(encrypted_data).decode()

def load_profiles():
    """
    Load profiles from the stored profiles file (decrypted).

    :return: A dictionary of profiles, where keys are profile names and values are their associated ROBLOSECURITY tokens.
    :rtype: dict
    :raises json.JSONDecodeError: If the profiles file contains invalid JSON data.
    """
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, 'rb') as f:
            encrypted_data = f.read()
            decrypted_data = decrypt_data(encrypted_data)
            return json.loads(decrypted_data)
    return {}

def save_profiles(profiles):
    """
    Save the current profiles to the profiles file (encrypted).

    :param profiles: A dictionary of profiles to be saved.
    :type profiles: dict
    """
    encrypted_data = encrypt_data(json.dumps(profiles))
    with open(PROFILE_FILE, 'wb') as f:
        f.write(encrypted_data)

def launch_multibloxy():
    """
    Launch MultiBloxy.exe if it is not already running.

    :return: None if MultiBloxy is already running.
    """
    for proc in psutil.process_iter(['pid', 'name']):
        if 'MultiBloxy.exe' in proc.info['name']:
            messagebox.showerror("Launcher", "MultiBloxy is already running.")
            return

    if os.path.exists(MULTIBLOXY):
        os.startfile(MULTIBLOXY)
        messagebox.showinfo("Launcher", "MultiBloxy is now running in the system tray.")
    else:
        messagebox.showerror("Error", f"MultiBloxy not found. Please ensure it is at {MULTIBLOXY} and try again.")

def set_roblosecurity_cookie(driver, roblosecurity_token):
    """
    Set the .ROBLOSECURITY cookie in the browser session using the provided token.

    :param driver: The WebDriver instance that will be used to interact with the browser.
    :param roblosecurity_token: The .ROBLOSECURITY token to be set in the browser session.
    """
    driver.add_cookie({'name': '.ROBLOSECURITY', 'value': roblosecurity_token, 'domain': 'roblox.com'})
    driver.refresh()

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def add_profile_via_browser(profiles, listbox):
    """
    Launches a browser for the user to log in and captures the .ROBLOSECURITY cookie.

    :param profiles: Dictionary of existing profiles.
    :param listbox: The listbox widget in the GUI.
    """
    config = load_config()
    skip_warning = config.get("skip_security_warning", False)

    def proceed_with_browser():
        profile_name = simpledialog.askstring("Profile Name", "Enter a name for this profile:")
        if not profile_name or profile_name in profiles:
            messagebox.showerror("Error", "Invalid or duplicate profile name.")
            return

        driver = None
        try:
            driver = initialize_driver()
            driver.get("https://www.roblox.com/login")

            # Wait until redirected to home after login
            WebDriverWait(driver, 120).until(EC.url_contains("/home"))

            cookies = driver.get_cookies()
            roblosecurity = next((c['value'] for c in cookies if c['name'] == '.ROBLOSECURITY'), None)

            if not roblosecurity:
                messagebox.showerror("Error", "Failed to retrieve .ROBLOSECURITY token.")
                return

            profiles[profile_name] = roblosecurity
            save_profiles(profiles)
            update_profile_list(profiles, listbox)

        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")
            return
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass

        # Show success message after browser is closed
        messagebox.showinfo("Success", f"Profile '{profile_name}' added successfully.")

    if not skip_warning:
        warning_window = tk.Toplevel()
        warning_window.title("Security Warning")
        warning_window.geometry("420x250")
        warning_window.resizable(False, False)
        warning_window.grab_set()

        try:
            warning_window.iconbitmap("assets/RobloxProfileManagerIcon.ico")
        except tk.TclError:
            pass

        warning_label = tk.Label(
            warning_window,
            text=(
                "⚠️ You are about to generate a persistent .ROBLOSECURITY token.\n\n"
                "Anyone with access to this token can fully control your account.\n\n"
                "To revoke all tokens, visit Roblox settings > Security > "
                "'Sign out of all other sessions'."
            ),
            wraplength=380,
            justify="left",
            anchor="w"
        )
        warning_label.pack(padx=20, pady=(20, 10))

        var_dont_show = tk.BooleanVar()
        check = tk.Checkbutton(
            warning_window,
            text="Don't show this message again",
            variable=var_dont_show
        )
        check.pack()

        btn_frame = tk.Frame(warning_window)
        btn_frame.pack(pady=20)

        def on_yes():
            if var_dont_show.get():
                config["skip_security_warning"] = True
                save_config(config)
            warning_window.destroy()
            proceed_with_browser()

        def on_no():
            warning_window.destroy()

        tk.Button(btn_frame, text="Continue", width=12, command=on_yes).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Cancel", width=12, command=on_no).grid(row=0, column=1, padx=10)

    else:
        proceed_with_browser()

def initialize_driver():
    """
    Initialize and return a new Chrome WebDriver instance.

    :return: A new WebDriver instance configured with default options.
    :rtype: webdriver.Chrome
    """
    options = webdriver.ChromeOptions()
    return webdriver.Chrome(options=options)

def login_to_roblox(driver, roblosecurity_token, timeout=5):
    """
    Log into Roblox by setting the .ROBLOSECURITY token cookie and waiting for the home page to load.

    :param driver: The WebDriver instance used to interact with the browser.
    :param roblosecurity_token: The ROBLOSECURITY token to be set in the browser session for login.
    :param timeout: Maximum wait time (in seconds) to wait for the home page to load. Defaults to 5 seconds.
    :return: True if login is successful (i.e., the page contains "/home"), False otherwise.
    :rtype: bool
    """
    driver.get('https://www.roblox.com/')
    set_roblosecurity_cookie(driver, roblosecurity_token)

    try:
        WebDriverWait(driver, timeout).until(EC.url_contains("/home"))
        return True
    except:
        return False

def launch_profile(profiles, profile_name, listbox):
    """
    Launch a profile by using the associated ROBLOSECURITY token to log in.

    :param profiles: A dictionary of profiles where keys are profile names and values are ROBLOSECURITY tokens.
    :param profile_name: The name of the profile to be launched.
    :param listbox: The listbox widget in the GUI where profiles are displayed.
    :raises KeyError: If the profile_name is not found in the profiles.
    """
    if profile_name in profiles:
        roblosecurity_token = profiles[profile_name]
        
        # Initialize the WebDriver
        driver = initialize_driver()

        # Attempt to log in using the provided ROBLOSECURITY token
        if login_to_roblox(driver, roblosecurity_token):
            print(f"Successfully logged in using profile '{profile_name}'!")
        else:
            print("Login failed.")
         # Uncomment or modify the driver.quit() as needed to keep the browser open after login
         # driver.quit()  # Commented out to keep the browser open
    else:
        messagebox.showerror("Error", "Profile not found.")

def create_profile(profiles, listbox):
    """
    Create a new profile and add it to the profile list.

    :param profiles: A dictionary of existing profiles.
    :param listbox: The listbox widget in the GUI where profiles are displayed.
    """
    profile_name = simpledialog.askstring("Profile Name", "Enter the profile name:")
    if not profile_name:
        return
    
    # Check if the profile name already exists in the profiles
    if profile_name in profiles:
        messagebox.showerror("Error", f"Profile '{profile_name}' already exists.")
        return
    
    roblosecurity_token = simpledialog.askstring("Token", "Enter the ROBLOSECURITY token:")
    if not roblosecurity_token:
        return
    
    # Add the new profile to the profiles dictionary
    profiles[profile_name] = roblosecurity_token
    save_profiles(profiles)

    # Update the listbox immediately after adding the new profile
    update_profile_list(profiles, listbox)
    messagebox.showinfo("Success", f"Profile '{profile_name}' created successfully.")

def delete_profile(profiles, listbox):
    """
    Delete a profile and remove it from the profile list.

    :param profiles: A dictionary of existing profiles.
    :param listbox: The listbox widget in the GUI where profiles are displayed.
    """
    profile_name = simpledialog.askstring("Profile Name", "Enter the profile name to delete:")
    if profile_name in profiles:
        del profiles[profile_name]
        save_profiles(profiles)

        # Update the listbox immediately after deleting the profile
        update_profile_list(profiles, listbox)
        messagebox.showinfo("Success", f"Profile '{profile_name}' deleted successfully.")
    else:
        messagebox.showerror("Error", "Profile not found.")

def update_profile_list(profiles, listbox):
    """
    Update the listbox to reflect the current list of profiles.

    :param profiles: A dictionary of existing profiles.
    :param listbox: The listbox widget in the GUI where profiles are displayed.
    """
    listbox.delete(0, tk.END)
    for profile in profiles:
        listbox.insert(tk.END, profile)

def create_gui():
    """
    Create the main GUI window for managing Roblox profiles, including buttons to create, delete, and launch profiles.
    """
    profiles = load_profiles()

    # Create the main window
    root = tk.Tk()
    root.title("Roblox Profile Manager")

    try:
        root.iconbitmap("assets/RobloxProfileManagerIcon.ico")
    except tk.TclError:
        pass

    # Create and place the listbox to display profile names
    listbox = tk.Listbox(root, width=50, height=15)
    listbox.grid(row=0, column=0, padx=10, pady=10)
    update_profile_list(profiles, listbox)

    def on_select_profile(event):
        """
        Handle profile selection by double-clicking a profile in the listbox.

        :param event: The event object triggered by the double-click.
        """
        selected_profile = listbox.get(listbox.curselection())
        launch_profile(profiles, selected_profile, listbox)

    listbox.bind("<Double-1>", on_select_profile)

    # Create buttons for profile management
    btn_create = tk.Button(root, text="Create Profile via .ROBLOSECURITY", width=30, command=lambda: create_profile(profiles, listbox))
    btn_create.grid(row=1, column=0, padx=10, pady=5)

    btn_add_browser = tk.Button(root, text="Create Profile via Browser Login", width=30, command=lambda: add_profile_via_browser(profiles, listbox))
    btn_add_browser.grid(row=2, column=0, padx=10, pady=5)

    btn_delete = tk.Button(root, text="Delete Profile", width=30, command=lambda: delete_profile(profiles, listbox))
    btn_delete.grid(row=3, column=0, padx=10, pady=5)

    # Create a button to launch MultiBloxy
    btn_launch_multibloxy = tk.Button(root, text="Launch MultiBloxy", width=30, command=launch_multibloxy)
    btn_launch_multibloxy.grid(row=4, column=0, padx=10, pady=5)

    # Start the GUI event loop
    root.mainloop()

if __name__ == '__main__':
    create_gui()
