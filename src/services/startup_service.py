import sys
from pathlib import Path
from src.utils.app_logger import app_logger

APP_NAME = "AISecurityClipboardGuardian"
REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"


class StartupService:

    @staticmethod
    def get_executable_path():
        if getattr(sys, "frozen", False):
            return f'"{sys.executable}"'
        else:
            main_script = Path(__file__).resolve().parents[2] / "src" / "gui" / "app.py"
            return f'"{sys.executable}" "{main_script}"'

    @classmethod
    def set_autostart(cls, enable: bool) -> bool:
        if sys.platform != "win32":
            app_logger.warning("Autostart setting is only supported on Windows.")
            return False

        try:
            import winreg

            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                REG_PATH,
                0,
                winreg.KEY_SET_VALUE
            )

            if enable:
                cmd = cls.get_executable_path()
                winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, cmd)
                app_logger.info(f"Windows Autostart enabled: {cmd}")
            else:
                try:
                    winreg.DeleteValue(key, APP_NAME)
                    app_logger.info("Windows Autostart disabled.")
                except FileNotFoundError:
                    pass

            winreg.CloseKey(key)
            return True

        except Exception as e:
            app_logger.error(f"Failed to update Windows Autostart: {e}")
            return False

    @classmethod
    def is_autostart_enabled(cls) -> bool:
        if sys.platform != "win32":
            return False

        try:
            import winreg

            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                REG_PATH,
                0,
                winreg.KEY_READ
            )

            try:
                val, _ = winreg.QueryValueEx(key, APP_NAME)
                winreg.CloseKey(key)
                return bool(val)
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False

        except Exception as e:
            app_logger.error(f"Failed to check Windows Autostart status: {e}")
            return False
