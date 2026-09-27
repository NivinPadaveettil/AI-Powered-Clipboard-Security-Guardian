import sys
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ENTRY_POINT = BASE_DIR / "src" / "gui" / "app.py"

def build():
    print("=" * 60)
    print("Building AI Security Clipboard Guardian Windows Executable")
    print("=" * 60)

    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--name=AI_Security_Clipboard_Guardian",
        "--add-data", f"{BASE_DIR / 'models'};models",
        "--add-data", f"{BASE_DIR / 'config'};config",
        "--add-data", f"{BASE_DIR / 'database'};database",
        str(ENTRY_POINT),
    ]

    print("Command:", " ".join(cmd))
    result = subprocess.run(cmd, cwd=BASE_DIR)

    if result.returncode == 0:
        print()
        print("=" * 60)
        print("BUILD SUCCESSFUL!")
        print(f"Executable output: {BASE_DIR / 'dist' / 'AI_Security_Clipboard_Guardian'}")
        print("=" * 60)
    else:
        print()
        print(f"Build failed with exit code {result.returncode}")

if __name__ == "__main__":
    build()
