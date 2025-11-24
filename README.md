# 🔍 GitHub Repository Analyzer (GUI)

This project is a simple Desktop Application built with Python's Tkinter library. It retrieves data from the GitHub API by entering the user's GitHub repository name (in the user/repo format) and provides a detailed JSON report showing basic repository statistics (stars, forks, contributors, creation date, etc.).

The project has two different user interface themes: Classic (Light Theme) and Modern (Dark Theme - Neon).

## 🌟 Features
Basic Information: Repository name, owner, and description.

Statistics: Stars, Forks, Watchers, Open Issues, and Contributors count.

Date Information: Creation, last update, and last push dates.

Metadata: Main programming language and license information.

API Integration: The requests library is used for real-time data extraction.

Two Different Interfaces: Classic (github_analyzer.py) and Modern, Dark Theme (dark_theme.py).

## 💻 Installation and Run
Follow the steps below to run the project on your local machine.

Prerequisites
This application requires Python 3 and depends on the requests library.

Bash

pip install requests
Running the Application
Run the file corresponding to your preferred interface theme:

1. Classic (Light) Theme:

Bash

python github_analyzer.py
2. Modern (Dark) Theme:

Bash

python dark_theme.py

## 💡 Usage
After the application opens, enter the full name of the GitHub repository you want to analyze in the Repo Name field, in the username/repo_name format (for example: microsoft/vscode).

Click the Analyze button.

The application will retrieve data from the API and display the results in JSON format in the report box.

🖼️ Sample Interface (Dark Theme)
📜 License
This project is licensed under the MIT License. See the LICENSE file for details (Keep this line if you're adding a license file; otherwise, remove it).
