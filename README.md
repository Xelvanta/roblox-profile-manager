# 🚀 Roblox Profile Manager

![GitHub License](https://img.shields.io/github/license/Xelvanta/roblox-profile-manager?label=License&color=orange)
![GitHub Release](https://img.shields.io/github/v/release/Xelvanta/roblox-profile-manager?include_prereleases&label=Release&color=green)

**Roblox Profile Manager** is a **Python-based application** that enables users to easily manage and switch between multiple Roblox profiles. It uses **Selenium** for browser automation and **Tkinter** for creating a graphical interface. The application allows users to save, load, create, delete, and log into multiple profiles using **ROBLOSECURITY tokens**. It is recommended to use this script in combination with **MultiBloxy** for running multiple Roblox instances simultaneously.

### ⚠️ Disclaimers:  
- Please note that profiles are encrypted using Fernet encryption, with a key generated and stored in the root directory upon the program's first launch. While Fernet provides strong encryption, it is important to understand that the security of your encrypted data depends on the safety of the encryption key. If an attacker gains access to profiles.json and the key.key files, they could potentially decrypt your profiles. The user assumes full responsibility for any risks associated with storing tokens and using this program. The code is provided "as-is," and the author disclaims all liability for any damages, losses, or issues arising from its use. By proceeding, you acknowledge and accept these risks.

- This application includes **MultiBloxy** as an optional feature, allowing you to run multiple Roblox instances simultaneously. Please note that **Xelvanta** is **not** affiliated with **MultiBloxy**, and **MultiBloxy** does not endorse **Xelvanta** or this project in any capacity. **MultiBloxy** is distributed under the [MIT License](MultiBloxy/LICENSE).

---

## 📋 Requirements

Before running the application, ensure you have the following:

- **Google Chrome** (for Selenium WebDriver)
  - [Download Google Chrome](https://www.google.com/intl/en_ca/chrome/)
- **Python 3.x**
  - [Download Python](https://www.python.org/downloads/)
- **Pip** (Python package manager, included with Python)

---

## ⚙️ Installation

### 1. Clone the Repository:

```bash
git clone https://github.com/Xelvanta/roblox-profile-manager
cd roblox-profile-manager
```

### 2. Install Dependencies:

Ensure you have all required Python dependencies installed:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

To run the **Roblox Profile Manager** application:

1. Open a terminal and navigate to the project folder:

    ```bash
    cd roblox-profile-manager
    ```

2. Run the script:

    ```bash
    python app.py
    ```

3. **Access the GUI**: A **Tkinter GUI** will open, where you can manage Roblox profiles, create new profiles, delete them, or launch them for use.

---

## ⚠️ Common Issues

Here are some common issues you may encounter during setup:

- **Launching a new instance of Roblox closes the previous instance**: Ensure that **MultiBloxy.exe** is running before attempting to manage multiple instances of Roblox.

- **Selenium WebDriver issues**: If you're having trouble with the browser automation, ensure that **Google Chrome** is installed and properly configured for Selenium to interact with.

---

## 🛠️ Troubleshooting

### MultiBloxy Not Found

If **MultiBloxy.exe** is not found, make sure the executable exists in the **MultiBloxy/** folder under the project directory. If not, download it from the [MultiBloxy GitHub repository](https://github.com/Zgoly/MultiBloxy).

### Issues with the Selenium WebDriver

If you're having issues with Selenium not launching Chrome, ensure that you have the **correct version** of **Google Chrome** and **chromedriver** for your operating system.

---

## 💡 Contributing

Feel free to fork the project and submit pull requests to improve the **Roblox Profile Manager**. Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for more information.

---

## 📝 License

**Roblox Profile Manager** is open source and available under the GPL-3.0 license. See the [LICENSE](LICENSE) for more details.
**MultiBloxy** (in the MultiBloxy/ folder) is licensed under the MIT License. See the [MIT LICENSE](MultiBloxy/LICENSE) for more details.

---

By **Xelvanta**  
For support or inquiries, please contact us at [Xelvanta@proton.me](mailto:Xelvanta@proton.me).  
GitHub: [https://github.com/Xelvanta](https://github.com/Xelvanta)  
