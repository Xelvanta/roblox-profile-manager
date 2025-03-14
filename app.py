import os
import time
import json
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# IMPORTANT: Recommended to use with https://github.com/Zgoly/MultiBloxy to allow multiple Roblox instances to run concurrently.

# Profile file for storing and retrieving profiles
PROFILE_FILE = "profiles.json"

def load_profiles():
    """
    Load profiles from the stored profiles file.

    :return: A dictionary of profiles, where keys are profile names and values are their associated ROBLOSECURITY tokens.
    """
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_profiles(profiles):
    """
    Save the current profiles to the profiles file.

    :param profiles: A dictionary of profiles to be saved. Each key is a profile name and the value is the ROBLOSECURITY token.
    """
    with open(PROFILE_FILE, 'w') as f:
        json.dump(profiles, f)

def set_roblosecurity_cookie(driver, roblosecurity_token):
    """
    Set the .ROBLOSECURITY cookie in the browser session using the provided token.

    :param driver: The WebDriver instance that will be used to interact with the browser.
    :param roblosecurity_token: The ROBLOSECURITY token to be set in the browser session.
    """
    driver.add_cookie({'name': '.ROBLOSECURITY', 'value': roblosecurity_token, 'domain': 'roblox.com'})
    driver.refresh()

def initialize_driver():
    """
    Initialize and return a new Chrome WebDriver instance.

    :return: A new WebDriver instance configured with default options.
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
    :param listbox: The listbox widget in the GUI that displays profile names.
    """
    listbox.delete(0, tk.END)
    for profile in profiles:
        listbox.insert(tk.END, profile)

def create_gui():
    """
    Create the main GUI window for managing Roblox profiles, including buttons to create, delete, and launch profiles.

    This function sets up the profile management interface and starts the Tkinter event loop.
    """
    profiles = load_profiles()

    # Create the main window
    root = tk.Tk()
    root.title("Roblox Profile Manager")

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
    btn_create = tk.Button(root, text="Create Profile", width=20, command=lambda: create_profile(profiles, listbox))
    btn_create.grid(row=1, column=0, padx=10, pady=10)

    btn_delete = tk.Button(root, text="Delete Profile", width=20, command=lambda: delete_profile(profiles, listbox))
    btn_delete.grid(row=2, column=0, padx=10, pady=10)

    # Start the GUI event loop
    root.mainloop()

if __name__ == '__main__':
    create_gui()
