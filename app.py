import os
import time
import json
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# IMPORTANT: Recommended to use with https://github.com/Zgoly/MultiBloxy to allow multiple Roblox instances to run at once.

# Profile file to store and retrieve profiles
PROFILE_FILE = "profiles.json"

def load_profiles():
    """Load profiles from the profiles file."""
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_profiles(profiles):
    """Save profiles to the profiles file."""
    with open(PROFILE_FILE, 'w') as f:
        json.dump(profiles, f)

def set_roblosecurity_cookie(driver, roblosecurity_token):
    """
    Sets the .ROBLOSECURITY cookie in the browser session.
    
    :param driver: The WebDriver instance.
    :param roblosecurity_token: The ROBLOSECURITY token to be set.
    """
    driver.add_cookie({'name': '.ROBLOSECURITY', 'value': roblosecurity_token, 'domain': 'roblox.com'})
    driver.refresh()

def initialize_driver():
    """
    Initializes and returns a new Chrome WebDriver instance.
    
    :return: A WebDriver instance.
    """
    options = webdriver.ChromeOptions()
    return webdriver.Chrome(options=options)

def login_to_roblox(driver, roblosecurity_token, timeout=5):
    """
    Logs into Roblox using the .ROBLOSECURITY token by setting the cookie and refreshing the page.
    
    :param driver: The WebDriver instance.
    :param roblosecurity_token: The ROBLOSECURITY token to be set.
    :param timeout: Maximum wait time for the URL to change (default 5 seconds).
    :return: True if login is successful, False otherwise.
    """
    driver.get('https://www.roblox.com/')
    set_roblosecurity_cookie(driver, roblosecurity_token)

    try:
        WebDriverWait(driver, timeout).until(EC.url_contains("/home"))
        return True
    except:
        return False

def launch_profile(profiles, profile_name, listbox):
    """Launches a profile by using the associated ROBLOSECURITY token."""
    if profile_name in profiles:
        roblosecurity_token = profiles[profile_name]
        
        # Initialize the WebDriver
        driver = initialize_driver()

        # Try to log in
        if login_to_roblox(driver, roblosecurity_token):
            print(f"Successfully logged in using profile '{profile_name}'!")
        else:
            print("Login failed.")
        
        # Comment out or remove the driver.quit() to keep the browser open
        # driver.quit()   # This line is now removed to keep the browser open
    else:
        messagebox.showerror("Error", "Profile not found.")

def create_profile(profiles, listbox):
    """Creates a new profile."""
    profile_name = simpledialog.askstring("Profile Name", "Enter the profile name:")
    if not profile_name:
        return
    
    # Check if profile name already exists
    if profile_name in profiles:
        messagebox.showerror("Error", f"Profile '{profile_name}' already exists.")
        return
    
    roblosecurity_token = simpledialog.askstring("Token", "Enter the ROBLOSECURITY token:")
    if not roblosecurity_token:
        return
    
    profiles[profile_name] = roblosecurity_token
    save_profiles(profiles)

    # Update listbox immediately after adding the new profile
    update_profile_list(profiles, listbox)
    messagebox.showinfo("Success", f"Profile '{profile_name}' created successfully.")

def delete_profile(profiles, listbox):
    """Deletes a profile."""
    profile_name = simpledialog.askstring("Profile Name", "Enter the profile name to delete:")
    if profile_name in profiles:
        del profiles[profile_name]
        save_profiles(profiles)

        # Update listbox immediately after deleting the profile
        update_profile_list(profiles, listbox)
        messagebox.showinfo("Success", f"Profile '{profile_name}' deleted successfully.")
    else:
        messagebox.showerror("Error", "Profile not found.")

def update_profile_list(profiles, listbox):
    """Update the listbox with the latest profiles."""
    listbox.delete(0, tk.END)
    for profile in profiles:
        listbox.insert(tk.END, profile)

def create_gui():
    """Creates the main GUI window for profile management."""
    profiles = load_profiles()

    # Create the main window
    root = tk.Tk()
    root.title("Roblox Profile Manager")

    # Create and place the listbox
    listbox = tk.Listbox(root, width=50, height=15)
    listbox.grid(row=0, column=0, padx=10, pady=10)
    update_profile_list(profiles, listbox)

    def on_select_profile(event):
        """Handles profile selection in the listbox."""
        selected_profile = listbox.get(listbox.curselection())
        launch_profile(profiles, selected_profile, listbox)

    listbox.bind("<Double-1>", on_select_profile)

    # Create buttons
    btn_create = tk.Button(root, text="Create Profile", width=20, command=lambda: create_profile(profiles, listbox))
    btn_create.grid(row=1, column=0, padx=10, pady=10)

    btn_delete = tk.Button(root, text="Delete Profile", width=20, command=lambda: delete_profile(profiles, listbox))
    btn_delete.grid(row=2, column=0, padx=10, pady=10)

    # Start the GUI event loop
    root.mainloop()

if __name__ == '__main__':
    create_gui()