import tkinter as tk
from tkinter import ttk

class UIManager:
    """Manages all UI components of the main application window."""
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller # Reference to the App (Controller)
        self.root.title("LLM Relay Hub v4.2 - Refactored")
        self.root.geometry("850x750")

        self._create_widgets()

    def _create_widgets(self):
        """Creates and lays out all the widgets in the window."""
        # --- Input Frame ---
        input_frame = tk.LabelFrame(self.root, text="📝 Your Message")
        input_frame.pack(fill='x', padx=15, pady=10)
        self.input_text = tk.Text(input_frame, height=4)
        self.input_text.pack(fill='x')

        # --- Send Frame (Buttons built dynamically) ---
        send_frame = tk.LabelFrame(self.root, text="📤 Send to Model")
        send_frame.pack(fill='x', padx=15, pady=5)
        button_container = tk.Frame(send_frame)
        button_container.pack()

        models = self.controller.settings.get_models()
        for model in models:
            btn = tk.Button(
                button_container,
                text=f"→ {model['name']}",
                bg=model['button_color'],
                fg="white",
                command=lambda m=model: self.controller.send_to_model(m['id'])
            )
            btn.pack(side='left', padx=5, pady=5)

        # --- Log Display ---
        log_frame = tk.LabelFrame(self.root, text="💬 Conversation Log")
        log_frame.pack(fill='both', expand=True, padx=15, pady=10)
        self.log_display = tk.Text(log_frame, wrap='word', state='disabled')
        self.log_display.pack(fill='both', expand=True)

        # --- Status Bar ---
        self.status_var = tk.StringVar()
        status_bar = tk.Label(self.root, textvariable=self.status_var, relief='sunken', anchor='w')
        status_bar.pack(side='bottom', fill='x')

    def update_log_display(self, entries):
        """Updates the log display with the current session entries."""
        self.log_display.config(state='normal')
        self.log_display.delete('1.0', tk.END)
        self.log_display.insert(tk.END, "\n\n---\n\n".join(entries))
        self.log_display.see(tk.END)
        self.log_display.config(state='disabled')

    def get_input_text(self):
        """Gets text from the input box."""
        return self.input_text.get("1.0", tk.END).strip()

    def clear_input_text(self):
        """Clears the input box."""
        self.input_text.delete("1.0", tk.END)

    def update_status_bar(self, message):
        """Updates the text in the status bar."""
        self.status_var.set(message)