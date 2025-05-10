# Contributing to Roblox Profile Manager

Thank you for your interest in contributing to **Roblox Profile Manager**! 🎉 This project is licensed under the **GPL 3.0** license, meaning all contributions must also be open-source under the same license.  

We welcome all kinds of contributions, including **bug reports, feature requests, documentation improvements, and code contributions**. Please follow the guidelines below to ensure a smooth collaboration process.  

---

## 🛠 How to Contribute  

### 1️⃣ Fork the Repository  
Click the **"Fork"** button on the top-right of the repository page to create your own copy.  

### 2️⃣ Clone Your Fork  
```bash
git clone https://github.com/your-username/roblox-profile-manager.git
cd roblox-profile-manager
```

### 3️⃣ Create a New Branch  
Make sure to create a branch for your work rather than working directly on `main`.  
```bash
git checkout -b feature/your-feature-name
```

### 4️⃣ Make Your Changes  
Modify the codebase, fix bugs, or improve documentation as needed.  

### 5️⃣ Format Your Code (Style Guidelines)

Ensure your code follows the project's formatting and style conventions before committing.  

#### 🐍 Python Formatting  
- Use **4 spaces for indentation** (no tabs).  
- Keep **imports grouped**:  
  - Standard library imports (e.g., `json`, `os`) go first.  
  - Third-party libraries (e.g., `selenium`) next.  
  - Local imports last.  
- Follow **PEP 8** style guidelines.  
- Run **Black** to auto-format:  
  ```bash
  black .
  ```  
- Keep **docstrings** for functions. Follow **PEP 257** docstring guidelines:  
  ```python
    def login_to_roblox(driver, roblosecurity_token, timeout=5):
        """
        Log into Roblox by setting the .ROBLOSECURITY token cookie and waiting for the home page to load.
    
        :param driver: The WebDriver instance used to interact with the browser.
        :param roblosecurity_token: The ROBLOSECURITY token to be set in the browser session for login.
        :param timeout: Maximum wait time (in seconds) to wait for the home page to load. Defaults to 5 seconds.
        :return: True if login is successful (i.e., the page contains "/home"), False otherwise.
        :rtype: bool
        """
  ```
- Use **f-strings** for formatted output instead of `format()` or `+` concatenation.  
- Avoid **hardcoding paths**, use `os.path.join()` when working with files.  

Make sure all files are formatted before committing to maintain consistency! 🚀
- Ensure all tests pass before committing.  

### 6️⃣ Commit Your Changes  
Write **clear, concise commit messages**:  
```bash
git commit -m "Fix issue with loading profiles"
```

### 7️⃣ Push Your Branch  
```bash
git push origin feature/your-feature-name
```

### 8️⃣ Open a Pull Request  
- Go to your fork on GitHub.  
- Click **"Compare & pull request"**.  
- Provide a **clear description** of your changes.  
- **Link any relevant issues** (e.g., `Fixes #42`).  

---

## 📜 License  

By contributing, you agree that your code will be **licensed under GPL-3.0**.  

📌 **You must ensure your contributions comply with GPL-3.0, meaning all modifications remain open-source under the same license.**  

---

Thank you for contributing! 🚀
