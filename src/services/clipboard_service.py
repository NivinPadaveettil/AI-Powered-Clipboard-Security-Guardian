import subprocess


def clear_clipboard():
    """
    Clear the Windows clipboard from WSL.
    """

    try:

        command = (
            "Add-Type -AssemblyName System.Windows.Forms; "
            "[System.Windows.Forms.Clipboard]::Clear()"
        )

        subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-Command",
                command,
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )

        return True

    except Exception as e:

        print(
            "Clipboard clearing error:",
            e
        )

        return False


def get_clipboard():
    """
    Read the Windows clipboard from WSL.
    """

    try:

        result = subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-Command",
                "Get-Clipboard",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        return result.stdout.strip()

    except Exception:

        return ""