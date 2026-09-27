from pathlib import Path
import json
import threading


BASE_DIR = Path(__file__).resolve().parents[2]
CONFIG_DIR = BASE_DIR / "config"
SETTINGS_FILE = CONFIG_DIR / "settings.json"


DEFAULT_SETTINGS = {
    "monitoring_enabled": True,
    "auto_clear_enabled": True,
    "clear_timeout": 15,
    "notifications_enabled": True,
    "start_monitoring_automatically": True,
}


class SettingsManager:

    def __init__(self):
        self._lock = threading.RLock()
        self.settings = self.load()

    def load(self):
        with self._lock:

            CONFIG_DIR.mkdir(parents=True, exist_ok=True)

            if not SETTINGS_FILE.exists():
                settings = DEFAULT_SETTINGS.copy()

                with open(
                    SETTINGS_FILE,
                    "w",
                    encoding="utf-8"
                ) as file:
                    json.dump(settings, file, indent=4)

                return settings

            try:
                with open(
                    SETTINGS_FILE,
                    "r",
                    encoding="utf-8"
                ) as file:
                    data = json.load(file)

                settings = DEFAULT_SETTINGS.copy()

                for key in DEFAULT_SETTINGS:
                    if key in data:
                        settings[key] = data[key]

                return settings

            except (
                json.JSONDecodeError,
                OSError,
                TypeError
            ):
                return DEFAULT_SETTINGS.copy()

    def save(self, settings=None):

        with self._lock:

            if settings is not None:
                updated = DEFAULT_SETTINGS.copy()
                updated.update(settings)
                self.settings = updated

            CONFIG_DIR.mkdir(parents=True, exist_ok=True)

            with open(
                SETTINGS_FILE,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    self.settings,
                    file,
                    indent=4
                )

    def get(self, key):

        with self._lock:
            return self.settings.get(
                key,
                DEFAULT_SETTINGS.get(key)
            )

    def set(self, key, value):

        if key not in DEFAULT_SETTINGS:
            raise KeyError(
                f"Unknown setting: {key}"
            )

        with self._lock:
            self.settings[key] = value
            self.save()

    def get_all(self):

        with self._lock:
            return self.settings.copy()

    def reload(self):

        with self._lock:
            self.settings = self.load()
            return self.settings.copy()


settings_manager = SettingsManager()
