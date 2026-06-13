# By 💜 Hexa Studios 🌐 discord.gg/ezGvtVJvWk
import json
import os

SETTINGS_FILE = "log_settings.json"

class LogManager:
    def __init__(self):
        self.settings = self.load_settings()
    
    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        return {}
    
    def save_settings(self):
        with open(SETTINGS_FILE, "w") as f:
            json.dump(self.settings, f, indent=4)
    
    def set_logs(self, guild_id, channel_id, log_types):
        key = f"{guild_id}_{channel_id}"
        self.settings[key] = {
            "guild_id": guild_id,
            "channel_id": channel_id,
            "log_types": log_types
        }
        self.save_settings()
    
    def get_logs(self, guild_id, channel_id):
        key = f"{guild_id}_{channel_id}"
        return self.settings.get(key, {}).get("log_types", [])
    
    def get_all_channels_for_guild(self, guild_id):
        channels = []
        for key, value in self.settings.items():
            if value["guild_id"] == guild_id:
                channels.append(value["channel_id"])
        return channels