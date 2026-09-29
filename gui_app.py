import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import customtkinter as ctk
import requests
import json
from packaging import version
from collections import defaultdict

class CodeSafeGuardian(ctk.CTk):
    def __init__(self):
        super().__init__()

        # App Configuration
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.title("CodeSafe Guardian v1.0")
        self.geometry("1200x800")
        self.minsize(1000, 700)

        # Main Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_rowconfigure(5, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar, text="CodeSafe", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.scan_button = ctk.CTkButton(self.sidebar, text="Scan Project", command=self.initiate_scan)
        self.scan_button.grid(row=1, column=0, padx=20, pady=10)

        self.dashboard_button = ctk.CTkButton(self.sidebar, text="Dashboard", command=self.show_dashboard)
        self.dashboard_button.grid(row=2, column=0, padx=20, pady=10)

        self.secrets_button = ctk.CTkButton(self.sidebar, text="Secrets", command=self.show_secrets)
        self.secrets_button.grid(row=3, column=0, padx=20, pady=10)

        self.dependencies_button = ctk.CTkButton(self.sidebar, text="Dependencies", command=self.show_dependencies)
        self.dependencies_button.grid(row=4, column=0, padx=20, pady=10)

        self.settings_button = ctk.CTkButton(self.sidebar, text="Settings", command=self.show_settings)
        self.sidebar_buttons = [self.scan_button, self.dashboard_button, self.secrets_button, self.dependencies_button, self.settings_button]

        self.appearance_mode = ctk.StringVar(value="Dark")
        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.sidebar, values=["Light", "Dark", "System"],
            command=self.change_appearance_mode, variable=self.appearance_mode
        )
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # Main Content Area
        self.main_content = ctk.CTkFrame(self, corner_radius=0)
        self.main_content.grid(row=0, column=1, sticky="nsew")
        self.main_content.grid_rowconfigure(0, weight=1)
        self.main_content.grid_columnconfigure(0, weight=1)

        # Dashboard Tab
        self.dashboard_frame = ctk.CTkFrame(self.main_content)
        self.dashboard_frame.grid(row=0, column=0, sticky="nsew")

        # Status Indicators
        self.status_frame = ctk.CTkFrame(self.dashboard_frame)
        self.status_frame.pack(fill="x", padx=10, pady=10)

        self.secrets_status = self.create_status_card(self.status_frame, "Secrets Found", "0", "High Risk")
        self.deps_status = self.create_status_card(self.status_frame, "Vulnerable Dependencies", "0", "Medium Risk")
        self.files_scanned = self.create_status_card(self.status_frame, "Files Scanned", "0", "Safe")

        # Risk Overview Chart (simplified for example)
        self.chart_frame = ctk.CTkFrame(self.dashboard_frame)
        self.chart_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.chart_label = ctk.CTkLabel(self.chart_frame, text="Security Risk Distribution", font=ctk.CTkFont(weight="bold"))
        self.chart_label.pack(pady=(10, 5))

        self.chart_canvas = tk.Canvas(self.chart_frame, bg="#2b2b2b", height=300)
        self.chart_canvas.pack(fill="both", expand=True)

        # Other tabs (initially hidden)
        self.secrets_frame = ctk.CTkFrame(self.main_content)
        self.dependencies_frame = ctk.CTkFrame(self.main_content)
        self.settings_frame = ctk.CTkFrame(self.main_content)

        # Sample data
        self.detected_secrets = []
        self.vulnerable_deps = []

        # Show dashboard by default
        self.current_frame = self.dashboard_frame
        self.draw_sample_chart()

    def create_status_card(self, parent, title, value, status):
        frame = ctk.CTkFrame(parent, width=200, height=100)
        frame.pack_propagate(False)
        frame.pack(side="left", padx=10, pady=10, fill="y")

        title_label = ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(weight="bold"))
        title_label.pack(pady=(10, 0))

        value_label = ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(size=24))
        value_label.pack(pady=10)

        status_text = "● " + status
        status_label = ctk.CTkLabel(frame, text=status_text, text_color=self.get_status_color(status))
        status_label.pack(pady=(0, 10))

        return {"frame": frame, "value": value_label, "status": status_label}

    def get_status_color(self, status):
        if "High" in status: return "#ff5555"
        if "Medium" in status: return "#ffaa00"
        return "#55ff55"

    def draw_sample_chart(self):
        self.chart_canvas.delete("all")
        width = self.chart_canvas.winfo_width()
        height = self.chart_canvas.winfo_height()

        # Background
        self.chart_canvas.create_rectangle(0, 0, width, height, fill="#2b2b2b", outline="")

        # Sample bars - would be replaced with real data
        risks = [
            ("Hardcoded Secrets", 3, "high"),
            ("Outdated Dependencies", 5, "medium"),
            ("Vulnerable Libraries", 2, "high"),
            ("Permission Issues", 1, "low"),
        ]

        bar_width = (width - 100) / len(risks)
        max_val = max(r[1] for r in risks)

        for i, (label, value, risk) in enumerate(risks):
            x0 = 50 + i * bar_width + 5
            bar_height = (value / max_val) * (height - 120)
            y0 = height - 50 - bar_height
            x1 = x0 + bar_width - 10
            y1 = height - 50

            color = "#ff5555" if risk == "high" else "#ffaa00" if risk == "medium" else "#55ff55"
            self.chart_canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

            # Label below bar
            self.chart_canvas.create_text(x0 + (bar_width-10)/2, height - 30, text=label, fill="white", angle=45, anchor="nw")

    def initiate_scan(self):
        # In a real app, this would scan the actual codebase
        messagebox.showinfo("Scan Started", "Scanning codebase for secrets and vulnerable dependencies...")

        # Simulate scan results
        self.detected_secrets = [
            {"type": "API Key", "file": "/src/config.py", "line": 42, "severity": "High"},
            {"type": "Database URL", "file": "/tests/test_config.py", "line": 15, "severity": "Medium"},
        ]

        self.vulnerable_deps = [
            {"name": "lodash", "version": "4.17.15", "vulnerability": "CVE-2021-23337", "severity": "High"},
            {"name": "axios", "version": "0.21.1", "vulnerability": "CVE-2021-3749", "severity": "Medium"},
        ]

        self.secrets_status["value"].configure(text=str(len(self.detected_secrets)))
        self.deps_status["value"].configure(text=str(len(self.vulnerable_deps)))
        self.files_scanned["value"].configure(text="42")  # Sample

        self.update_secrets_table()
        self.update_dependencies_table()
        self.draw_sample_chart()
        messagebox.showinfo("Scan Complete", f"Found {len(self.detected_secrets)} secrets and {len(self.vulnerable_deps)} vulnerable dependencies")

    def show_dashboard(self):
        self.hide_current_frame()
        self.dashboard_frame.grid(row=0, column=0, sticky="nsew")
        self.current_frame = self.dashboard_frame

    def show_secrets(self):
        self.hide_current_frame()
        self.secrets_frame.grid(row=0, column=0, sticky="nsew")
        self.current_frame = self.secrets_frame

        # Build secrets table if not already built
        if not hasattr(self.secrets_frame, 'table_built'):
            self.build_secrets_table()
            self.secrets_frame.table_built = True

    def show_dependencies(self):
        self.hide_current_frame()
        self.dependencies_frame.grid(row=0, column=0, sticky="nsew")
        self.current_frame = self.dependencies_frame

        # Build dependencies table if not already built
        if not hasattr(self.dependencies_frame, 'table_built'):
            self.build_dependencies_table()
            self.dependencies_frame.table_built = True

    def show_settings(self):
        self.hide_current_frame()
        self.settings_frame.grid(row=0, column=0, sticky="nsew")
        self.current_frame = self.settings_frame

    def hide_current_frame(self):
        self.current_frame.grid_forget()

    def change_appearance_mode(self, new_mode):
        ctk.set_appearance_mode(new_mode)

    def build_secrets_table(self):
        for widget in self.secrets_frame.winfo_children():
            widget.destroy()

        frame = ctk.CTkFrame(self.secrets_frame, corner_radius=0)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Table header
        header = ctk.CTkFrame(frame)
        header.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(header, text="Type", width=150, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left")
        ctk.CTkLabel(header, text="File", width=300, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left")
        ctk.CTkLabel(header, text="Line", width=80, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left")
        ctk.CTkLabel(header, text="Severity", width=100, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left")
        ctk.CTkLabel(header, text="Actions", width=150, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left")

        # Scrollable area for table content
        canvas = tk.Canvas(frame, bg="#2b2b2b", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add sample data
        self.update_secrets_table(scrollable_frame)

    def update_secrets_table(self, scrollable_frame=None):
        if scrollable_frame is None and hasattr(self.secrets_frame, 'table_built'):
            for widget in self.secrets_frame.winfo_children():
                if isinstance(widget, tk.Canvas):
                    scrollable_frame = widget.winfo_children()[0]
                    break

        if scrollable_frame:
            # Clear existing rows
            for widget in scrollable_frame.winfo_children():
                widget.destroy()

            # Add new rows
            for secret in self.detected_secrets:
                row = ctk.CTkFrame(scrollable_frame)
                row.pack(fill="x", padx=5, pady=2)

                ctk.CTkLabel(row, text=secret["type"], width=150, anchor="w").pack(side="left")
                ctk.CTkLabel(row, text=secret["file"], width=300, anchor="w").pack(side="left")
                ctk.CTkLabel(row, text=str(secret["line"]), width=80, anchor="w").pack(side="left")
                
                severity_label = ctk.CTkLabel(
                    row, 
                    text=secret["severity"], 
                    width=100, 
                    anchor="w", 
                    text_color=self.get_status_color(secret["severity"])
                )
                severity_label.pack(side="left")

                actions_frame = ctk.CTkFrame(row, width=150)
                actions_frame.pack_propagate(False)
                actions_frame.pack(side="left")

                ctk.CTkButton(actions_frame, text="View", width=50, command=lambda s=secret: self.view_secret(s)).pack(side="left")
                ctk.CTkButton(actions_frame, text="Fix", width=50, command=lambda s=secret: self.fix_secret(s)).pack(side="left", padx=5)

    def build_dependencies_table(self):
        for widget in self.dependencies_frame.winfo_children():
            widget.destroy()

        frame = ctk.CTkFrame(self.dependencies_frame, corner_radius=0)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Table header
        header = ctk.CTkFrame(frame)
        header.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(header, text="Package", width=200, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left")
        ctk.CTkLabel(header, text="Version", width=100, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left")
        ctk.CTkLabel(header, text="Vulnerability", width=200, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left")
        ctk.CTkLabel(header, text="Severity", width=100, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left")
        ctk.CTkLabel(header, text="Actions", width=150, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left")

        # Scrollable area for table content
        canvas = tk.Canvas(frame, bg="#2b2b2b", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add sample data
        self.update_dependencies_table(scrollable_frame)

    def update_dependencies_table(self, scrollable_frame=None):
        if scrollable_frame is None and hasattr(self.dependencies_frame, 'table_built'):
            for widget in self.dependencies_frame.winfo_children():
                if isinstance(widget, tk.Canvas):
                    scrollable_frame = widget.winfo_children()[0]
                    break

        if scrollable_frame:
            # Clear existing rows
            for widget in scrollable_frame.winfo_children():
                widget.destroy()

            # Add new rows
            for dep in self.vulnerable_deps:
                row = ctk.CTkFrame(scrollable_frame)
                row.pack(fill="x", padx=5, pady=2)

                ctk.CTkLabel(row, text=dep["name"], width=200, anchor="w").pack(side="left")
                ctk.CTkLabel(row, text=dep["version"], width=100, anchor="w").pack(side="left")
                ctk.CTkLabel(row, text=dep["vulnerability"], width=200, anchor="w").pack(side="left")
                
                severity_label = ctk.CTkLabel(
                    row, 
                    text=dep["severity"], 
                    width=100, 
                    anchor="w", 
                    text_color=self.get_status_color(dep["severity"])
                )
                severity_label.pack(side="left")

                actions_frame = ctk.CTkFrame(row, width=150)
                actions_frame.pack_propagate(False)
                actions_frame.pack(side="left")

                ctk.CTkButton(actions_frame, text="Details", width=70, command=lambda d=dep: self.show_dep_details(d)).pack(side="left")
                ctk.CTkButton(actions_frame, text="Update", width=70, command=lambda d=dep: self.update_dep(d)).pack(side="left", padx=5)

    def view_secret(self, secret):
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Secret in {secret['file']}")
        dialog.geometry("800x600")
        dialog.transient(self)
        dialog.grab_set()

        header = ctk.CTkFrame(dialog)
        header.pack(fill="x", padx=10, pady=(10, 0))

        ctk.CTkLabel(header, text=f"Type: {secret['type']}", font=ctk.CTkFont(weight="bold")).pack(side="left")
        ctk.CTkLabel(header, text=f"Severity: {secret['severity']}", text_color=self.get_status_color(secret["severity"])).pack(side="right")

        file_frame = ctk.CTkFrame(dialog)
        file_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(file_frame, text=f"File: {secret['file']}", anchor="w").pack(fill="x")

        # Simulated code viewer
        editor = scrolledtext.ScrolledText(dialog, wrap=tk.WORD, width=80, height=20, bg="#1e1e1e", fg="white", insertbackground="white")
        editor.pack(fill="both", expand=True, padx=10, pady=5)

        # Sample code with highlighted line
        sample_code = "\n".join(f"Line {i}: Some code here" for i in range(secret["line"]-5, secret["line"]+6) if i > 0)
        editor.insert(tk.END, sample_code)
        editor.config(state=tk.DISABLED)

        # Highlight the line with the secret
        editor.tag_config("highlight", background="#ff5555")
        editor.tag_add("highlight", f"{secret['line']-(secret['line']-6)}.0", f"{secret['line']-(secret['line']-6)}.end")
        editor.see(f"{secret['line']-(secret['line']-6)}.0")

        # Action buttons
        button_frame = ctk.CTkFrame(dialog)
        button_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkButton(
            button_frame, 
            text="Fix Automatically", 
            command=lambda: self.fix_secret_auto(secret, dialog)
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame, 
            text="Copy to Clipboard", 
            command=lambda: self.copy_secret_info(secret)
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame, 
            text="Mark as False Positive", 
            command=lambda: self.mark_false_positive(secret, dialog)
        ).pack(side="right", padx=5)

    def show_dep_details(self, dep):
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Vulnerability: {dep['name']}")
        dialog.geometry("800x600")
        dialog.transient(self)
        dialog.grab_set()

        # Header with package info
        header = ctk.CTkFrame(dialog)
        header.pack(fill="x", padx=10, pady=(10, 0))

        ctk.CTkLabel(
            header, 
            text=f"{dep['name']} {dep['version']}", 
            font=ctk.CTkFont(weight="bold", size=15)
        ).pack(side="left")

        ctk.CTkLabel(
            header, 
            text=f"Severity: {dep['severity']}", 
            text_color=self.get_status_color(dep['severity'])
        ).pack(side="right")

        # Vulnerability details
        details_frame = ctk.CTkFrame(dialog)
        details_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(
            details_frame, 
            text=f"{dep['vulnerability']}", 
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            details_frame, 
            text="This package version contains known security vulnerabilities that could be exploited.\n\n"
                "Attackers could potentially execute arbitrary code, gain elevated privileges, or cause a denial of service."
        ).pack(anchor="w")

        # Recommended versions
        rec_frame = ctk.CTkFrame(dialog)
        rec_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(
            rec_frame, 
            text="Recommended Versions:", 
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w")

        versions = ["4.17.21 (latest stable)", "4.17.19 (LTS)"]
        for v in versions:
            ver_row = ctk.CTkFrame(rec_frame, height=30)
            ver_row.pack(fill="x", pady=2)
            
            ctk.CTkLabel(ver_row, text=v).pack(side="left")
            ctk.CTkButton(
                ver_row, 
                text="Update", 
                width=80, 
                command=lambda d=dep, v=v: self.confirm_update(d, v)
            ).pack(side="right")

        # Action buttons
        button_frame = ctk.CTkFrame(dialog)
        button_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkButton(
            button_frame, 
            text="Ignore for Now", 
            command=dialog.destroy
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            button_frame, 
            text="Open Advisory", 
            command=lambda: self.open_web_link()
        ).pack(side="left", padx=5)

    def fix_secret(self, secret):
        self.view_secret(secret)  # In real app would implement actual fixing

    def fix_secret_auto(self, secret, dialog):
        messagebox.showinfo("Fixed", "Secret has been removed from the code (simulated)")
        dialog.destroy()

    def copy_secret_info(self, secret):
        self.clipboard_clear()
        self.clipboard_append(f"{secret['type']} in {secret['file']}:{secret['line']}")
        messagebox.showinfo("Copied", "Secret info copied to clipboard")

    def mark_false_positive(self, secret, dialog):
        messagebox.showinfo("Marked", "Secret marked as false positive (simulated)")
        dialog.destroy()

    def update_dep(self, dep):
        messagebox.showinfo("Updated", f"Updated {dep['name']} to latest version (simulated)")

    def confirm_update(self, dep, version):
        if messagebox.askyesno("Confirm Update", f"Update {dep['name']} to {version}?"):
            messagebox.showinfo("Updated", f"Updated {dep['name']} to {version} (simulated)")

    def open_web_link(self):
        messagebox.showinfo("Browser", "Would open browser to advisory page (simulated)")

if __name__ == "__main__":
    app = CodeSafeGuardian()
    app.mainloop()