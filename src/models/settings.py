import json
import os

class SettingsManager:
    """Manages application settings and model configuration."""
    
    def __init__(self, settings_file: str, logger):
        self.settings_file = settings_file
        self.logger = logger
        self.settings = self._load_settings()
    
    def _load_settings(self):
        """Loads settings from file or creates defaults."""
        default_settings = {
            "models": [
                {"id": "chatgpt", "name": "ChatGPT", "button_color": "#10A37F"},
                {"id": "claude", "name": "Claude", "button_color": "#FF6B35"},
                {"id": "gemini", "name": "Gemini", "button_color": "#4285F4"}
            ],
            "vault_path": "",
            "auto_save": True,
            "dark_mode": False
        }
        
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    loaded = json.load(f)
                    default_settings.update(loaded)
            return default_settings
        except Exception as e:
            self.logger.warning(f"Could not load settings: {e}")
            return default_settings
    
    def get_models(self):
        """Returns the list of configured models.