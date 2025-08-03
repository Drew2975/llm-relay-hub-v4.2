class SessionManager:
    """Manages the conversation session data and turn counter."""
    
    def __init__(self):
        self.entries = []
        self.turn_counter = 1
    
    def add_entry(self, content: str, model: str, direction: str, timestamp: str):
        """Adds a new entry to the session log."""
        entry = f"TURN {self.turn_counter:03d} – {direction} {model} @ {timestamp}\n{content}"
        self.entries.append(entry)
        self.turn_counter += 1
    
    def get_all_entries(self):
        """Returns all entries in the session."""
        return self.entries
    
    def reset_session(self):
        """Clears all entries and resets the turn counter."""
        self.entries = []
        self.turn_counter = 1
    
    def get_turn_count(self):
        """Returns the current turn counter."""
        return self.turn_counter