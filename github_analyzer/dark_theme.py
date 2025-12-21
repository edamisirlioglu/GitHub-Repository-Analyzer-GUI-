import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import json
from datetime import datetime


class GitHubRepoAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub Repo Analyzer — Modern UI")
        self.root.geometry("760x650")
        self.root.resizable(False, False)

        # DARK THEME COLORS
        self.bg_color = "#1e1e1e"       # Main background
        self.card_color = "#252526"     # Panel background
        self.accent = "#00e5ff"         # Neon cyan
        self.text_color = "#e0e0e0"     # Light text
        self.button_normal = "#007b8a"
        self.button_hover = "#00acc1"

        self.root.configure(bg=self.bg_color)

        self.create_widgets()

    # HOVER EFFECT FOR BUTTONS
    
    def add_hover(self, widget, normal, hover):
        widget.bind("<Enter>", lambda e: widget.config(bg=hover))
        widget.bind("<Leave>", lambda e: widget.config(bg=normal))

    # GUI WIDGETS
    
    def create_widgets(self):

        # TITLE
        title = tk.Label(
            self.root,
            text="🔍 GitHub Repo Analyzer",
            bg=self.bg_color,
            fg=self.accent,
            font=("Segoe UI", 22, "bold")
        )
        title.pack(pady=20)

        # FRAME (CARD STYLE)
        card = tk.Frame(self.root, bg=self.card_color, bd=2, relief="ridge")
        card.pack(padx=20, pady=10, fill="x")

        # INFO LABEL
        info = tk.Label(
            card,
            text="Repo format:   username/repository",
            bg=self.card_color,
            fg="#bbbbbb",
            font=("Segoe UI", 10)
        )
        info.pack(pady=(10, 5))

        # INPUT FIELD
        input_frame = tk.Frame(card, bg=self.card_color)
        input_frame.pack(pady=10)

        tk.Label(
            input_frame,
            text="Repository:",
            bg=self.card_color,
            fg=self.text_color,
            font=("Segoe UI", 12)
        ).grid(row=0, column=0, padx=5)

        # ENTRY
        self.repo_entry = tk.Entry(
            input_frame,
            font=("Segoe UI", 12),
            width=30,
            bg="#333333",
            fg="#ffffff",
            insertbackground="white",
            relief="flat"
        )
        self.repo_entry.grid(row=0, column=1, padx=5)
        self.repo_entry.insert(0, "microsoft/vscode")

        # ANALYZE BUTTON
        analyze_btn = tk.Button(
            card,
            text="▶ Analyze Repository",
            bg=self.button_normal,
            fg="white",
            activebackground=self.button_hover,
            font=("Segoe UI", 12, "bold"),
            cursor="hand2",
            padx=10,
            pady=8,
            relief="flat"
        )
        analyze_btn.pack(pady=15)

        analyze_btn.config(command=self.analyze_repo)

        self.add_hover(analyze_btn, self.button_normal, self.button_hover)

        # LOADING LABEL
        self.loading_label = tk.Label(
            self.root,
            text="Fetching data...",
            bg=self.bg_color,
            fg=self.accent,
            font=("Segoe UI", 12)
        )

        # RESULTS LABEL
        result_title = tk.Label(
            self.root,
            text="📄 Analysis Results",
            bg=self.bg_color,
            fg=self.accent,
            font=("Segoe UI", 16, "bold")
        )
        result_title.pack(pady=10)

        # SCROLLED TEXT AREA
        self.result_text = scrolledtext.ScrolledText(
            self.root,
            width=85,
            height=22,
            bg="#111111",
            fg="#00e5ff",
            font=("Consolas", 10),
            insertbackground="white",
            relief="flat",
            wrap=tk.WORD
        )
        self.result_text.pack(padx=20, pady=10)

    # API FUNCTIONS
    
    def fetch_repo_data(self, repo_name):
        api_url = f"https://api.github.com/repos/{repo_name}"

        try:
            response = requests.get(api_url, timeout=10)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                messagebox.showerror("Error", "Repository not found.")
                return None
            else:
                messagebox.showerror("Error", f"API Error: {response.status_code}")
                return None

        except Exception as e:
            messagebox.showerror("Error", str(e))
            return None

    def fetch_contributors_count(self, repo_name):
        api_url = f"https://api.github.com/repos/{repo_name}/contributors"

        try:
            response = requests.get(api_url, timeout=10)

            if response.status_code == 200:
                return len(response.json())
        except:
            return 0

        return 0

    def format_date(self, text):
        try:
            dt = datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ")
            return dt.strftime("%d/%m/%Y %H:%M")
        except:
            return text

    def create_report(self, data, contributor_count):

        report = {
            "Repository": {
                "name": data.get("name"),
                "full_name": data.get("full_name"),
                "owner": data.get("owner", {}).get("login"),
                "description": data.get("description")
            },
            "Stats": {
                "Stars": data.get("stargazers_count"),
                "Forks": data.get("forks_count"),
                "Watchers": data.get("watchers_count"),
                "Open Issues": data.get("open_issues_count"),
                "Contributors": contributor_count
            },
            "Dates": {
                "Created": self.format_date(data.get("created_at", "")),
                "Updated": self.format_date(data.get("updated_at", "")),
                "Pushed": self.format_date(data.get("pushed_at", "")),
            },
            "Meta": {
                "Language": data.get("language"),
                "License": data.get("license", {}).get("name") if data.get("license") else None,
                "URL": data.get("html_url")
            }
        }

        return json.dumps(report, indent=2, ensure_ascii=False)

    # ANALYZE BUTTON FUNCTION
    
    def analyze_repo(self):

        repo_name = self.repo_entry.get().strip()

        if "/" not in repo_name:
            messagebox.showwarning("Warning", "Correct format:\nusername/repository")
            return

        self.result_text.delete(1.0, tk.END)
        self.loading_label.pack(pady=5)
        self.root.update()

        repo_data = self.fetch_repo_data(repo_name)

        if repo_data:
            contributors = self.fetch_contributors_count(repo_name)
            report = self.create_report(repo_data, contributors)
            self.result_text.insert(1.0, report)
            messagebox.showinfo("Success", "Repository analyzed successfully!")

        self.loading_label.pack_forget()

# MAIN

def main():
    root = tk.Tk()
    GitHubRepoAnalyzer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
