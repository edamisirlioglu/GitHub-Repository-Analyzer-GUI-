import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import json
from datetime import datetime

class GitHubRepoAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub Repo Analyzer")
        self.root.geometry("700x600")
        self.root.resizable(True, True)

        # Theme colors
        self.bg_color = "#f0f0f0"
        self.button_color = "#4CAF50"
        self.root.configure(bg=self.bg_color)

        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(
            self.root,
            text="GitHub Repo Analyzer",
            font=("Arial", 18, "bold"),
            bg=self.bg_color,
            fg="#333"
        )
        title_label.pack(pady=20)

        info_label = tk.Label(
            self.root,
            text="Repo format: user_name/repo_name (ex: torvalds/linux)",
            font=("Arial", 10),
            bg=self.bg_color,
            fg="#666"
        )
        info_label.pack(pady=5)

        input_frame = tk.Frame(self.root, bg=self.bg_color)
        input_frame.pack(pady=10)

        repo_label = tk.Label(
            input_frame,
            text="Repo Name:",
            font=("Arial", 12),
            bg=self.bg_color
        )
        repo_label.grid(row=0, column=0, padx=5)

        self.repo_entry = tk.Entry(
            input_frame,
            font=("Arial", 12),
            width=30
        )
        self.repo_entry.grid(row=0, column=1, padx=5)
        self.repo_entry.insert(0, "microsoft/vscode")

        analyze_button = tk.Button(
            self.root,
            text="🔍︎ Analyze",
            font=("Arial", 12, "bold"),
            bg=self.button_color,
            fg="white",
            command=self.analyze_repo,
            cursor="hand2",
            padx=20,
            pady=10
        )
        analyze_button.pack(pady=15)

        self.loading_label = tk.Label(
            self.root,
            text="⌛︎ Analyzing...",
            font=("Arial", 10),
            bg=self.bg_color,
            fg="#FF5722"
        )

        result_label = tk.Label(
            self.root,
            text="🗠 Analysis Results:",
            font=("Arial", 12, "bold"),
            bg=self.bg_color
        )
        result_label.pack(pady=10)

        self.result_text = scrolledtext.ScrolledText(
            self.root,
            font=("Courier", 10),
            width=70,
            height=18,
            wrap=tk.WORD
        )
        self.result_text.pack(pady=10, padx=20)

    def fetch_repo_data(self, repo_name):
        api_url = f"https://api.github.com/repos/{repo_name}"

        try:
            response = requests.get(api_url, timeout=10)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                messagebox.showerror("Error!", "❌ Repo not found! Please use the correct format!")
                return None
            else:
                messagebox.showerror("Error!", f"❌ API Error: {response.status_code}")
                return None

        except requests.exceptions.Timeout:
            messagebox.showerror("Error!", "🕙︎ The request has timed out!")
            return None
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error!", "🌐 Internet connection error!")
            return None
        except Exception as e:
            messagebox.showerror("Error!", f"❌ Unexpected error: {str(e)}")
            return None

    def fetch_contributors_count(self, repo_name):
        api_url = f"https://api.github.com/repos/{repo_name}/contributors"

        try:
            response = requests.get(api_url, timeout=10)

            if response.status_code == 200:
                contributors = response.json()
                return len(contributors)
            return 0
        except:
            return 0

    def format_date(self, date_string):
        try:
            date_obj = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
            return date_obj.strftime("%d/%m/%Y %H:%M")
        except:
            return date_string

    def create_report(self, data, contributor_count):
        report = {
            "repo_informations": {
                "name": data.get("name", "N/A"),
                "full_name": data.get("full_name", "N/A"),
                "owner": data.get("owner", {}).get("login", "N/A"),
                "description": data.get("description", "No description!")
            },
            "statistics": {
                "stars_count": data.get("stargazers_count", 0),
                "forks_count": data.get("forks_count", 0),
                "watchers_count": data.get("watchers_count", 0),
                "open_issues_count": data.get("open_issues_count", 0),
                "contributor_count": contributor_count
            },
            "dates": {
                "created_date": self.format_date(data.get("created_at", "")),
                "last_update": self.format_date(data.get("updated_at", "")),
                "last_push": self.format_date(data.get("pushed_at", ""))
            },
            "language_and_license": {
                "main_language": data.get("language", "Unspecified"),
                "license": data.get("license", {}).get("name", "Unspecified") if data.get("license") else "Unspecified"
            },
            "link": data.get("html_url", "N/A")
        }

        return json.dumps(report, indent=2, ensure_ascii=False)

    def analyze_repo(self):
        repo_name = self.repo_entry.get().strip()

        if not repo_name:
            messagebox.showwarning("Warning!", "⚠️ Please enter a repo name!")
            return

        if "/" not in repo_name:
            messagebox.showwarning("Warning!", "⚠️ Repo format: user_name/repo_name")
            return

        self.result_text.delete(1.0, tk.END)

        self.loading_label.pack(pady=5)
        self.root.update()

        repo_data = self.fetch_repo_data(repo_name)

        if repo_data:
            contributor_count = self.fetch_contributors_count(repo_name)
            report = self.create_report(repo_data, contributor_count)
            self.result_text.insert(1.0, report)
            messagebox.showinfo("Success!", "✅ Analysis completed!")

        self.loading_label.pack_forget()


def main():
    root = tk.Tk()
    app = GitHubRepoAnalyzer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
