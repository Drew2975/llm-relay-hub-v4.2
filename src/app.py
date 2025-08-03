import tkinter as tk
from tkinter import messagebox, filedialog
import pyperclip
from datetime import datetime
from .models.session import SessionManager
from .models.settings import SettingsManager
from .views.main_window import UIManager
from .services.logger import setup_logger

class App:
    """The main Controller class for the application."""
    def __init__(self):
        self.logger = setup_logger()
        self.settings = SettingsManager('settings.json', self.logger)
        self.session = SessionManager()

        self.root = tk.Tk()
        self.ui = UIManager(self.root, self)

        # Bind keyboard shortcuts
        self.root.bind('<F9>', lambda e: self.capture_from_clipboard())
        self.root.bind('<Control-r>', lambda e: self.reset_session())

        self.logger.info("Application initialized.")
        self.ui.update_status_bar("Ready - Phase 1 MVR Active")

    def send_to_model(self, model_id: str):
        """Handles the logic for sending a message to a model."""
        prompt = self.ui.get_input_text()
        if not prompt:
            self.ui.update_status_bar("⚠️ Cannot send empty message.")
            return

        try:
            pyperclip.copy(prompt)
            word_count = len(prompt.split())
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            self.session.add_entry(
                content=prompt,
                model=model_id.upper(),
                direction="SENT TO",
                timestamp=timestamp
            )
            
            self.ui.update_log_display(self.session.get_all_entries())
            self.ui.clear_input_text()
            self.ui.update_status_bar(f"✅ Copied to {model_id.upper()} ({word_count} words)")
            
        except Exception as e:
            self.ui.update_status_bar(f"❌ Failed to send to {model_id}")
            messagebox.showerror("Error", f"Failed to send: {e}")

    def send_to_all(self):
        """Handles sending a message to all models."""
        prompt = self.ui.get_input_text()
        if not prompt:
            self.ui.update_status_bar("⚠️ Cannot send empty message.")
            return

        try:
            pyperclip.copy(prompt)
            word_count = len(prompt.split())
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            models = ["ChatGPT", "Claude", "Gemini"]
            for model in models:
                self.session.add_entry(
                    content=prompt,
                    model=model.upper(),
                    direction="SENT TO",
                    timestamp=timestamp
                )
            
            self.ui.update_log_display(self.session.get_all_entries())
            self.ui.clear_input_text()
            self.ui.update_status_bar(f"✅ Copied for ALL MODELS ({word_count} words)")
            
        except Exception as e:
            self.ui.update_status_bar("❌ Failed to send to all models")
            messagebox.showerror("Error", f"Failed: {e}")

    def capture_from_clipboard(self):
        """Handles capturing a response from the clipboard."""
        model_id = self.ui.get_capture_model()
        
        try:
            response = pyperclip.paste().strip()
            if not response:
                self.ui.update_status_bar("⚠️ Clipboard is empty")
                return
            
            word_count = len(response.split())
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            self.session.add_entry(
                content=response,
                model=model_id.upper(),
                direction="RECEIVED FROM",
                timestamp=timestamp
            )
            
            self.ui.update_log_display(self.session.get_all_entries())
            self.ui.update_status_bar(f"✅ Captured {word_count} words from {model_id.upper()}")
            
        except Exception as e:
            self.ui.update_status_bar(f"❌ Failed to capture")
            messagebox.showerror("Error", f"Failed to capture: {e}")

    def clear_input(self):
        """Clears the input text box."""
        self.ui.clear_input_text()
        self.ui.update_status_bar("Input cleared.")

    def reset_session(self):
        """Resets the current session log."""
        if not self.session.get_all_entries():
            self.ui.update_status_bar("No session to reset")
            return
            
        if messagebox.askyesno("Reset Session", 
                             "Clear all conversation data?",
                             icon="warning"):
            self.session.reset_session()
            self.ui.update_log_display(self.session.get_all_entries())
            self.ui.update_status_bar("🔄 Session reset")

    def export_txt(self):
        """Handles exporting the log to a .txt file."""
        entries = self.session.get_all_entries()
        if not entries:
            messagebox.showwarning("Nothing to Export", "No conversation data to export")
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            initialname=f"LLM_Relay_{timestamp}.txt"
        )
        
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"LLM Relay Hub Export\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")
                f.write("\n\n".join(entries))
            
            messagebox.showinfo("Export Complete", f"Saved!")
            self.ui.update_status_bar(f"✅ Exported {len(entries)} turns")

    def run(self):
        """Starts the Tkinter main loop."""
        self.root.mainloop()