import time
import threading
import pyperclip

from src.predict import predict
from src.core.risk_scoring import calculate_risk
from src.database.sqlite_logger import logger
from src.services.clipboard_service import clear_clipboard
from src.services.notification_service import NotificationService
from src.config.settings_manager import settings_manager


class ClipboardMonitor:

    def __init__(self, on_notification=None):
        self.last_text = ""
        self.running = False

        # Optional notification callback (e.g. Qt signal for main thread execution)
        self.on_notification = on_notification

        # Prevent duplicate clear timers
        self.clear_scheduled = False

        # Text currently waiting to be cleared
        self.pending_clear_text = None

        # Protect shared state
        self.lock = threading.Lock()

        # Persistent settings
        self.settings = settings_manager

    # =========================================================
    # Process Clipboard
    # =========================================================

    def process_clipboard(self, text):

        try:

            if not text or not text.strip():
                return

            # -------------------------------------------------
            # Prevent duplicate processing of the same value
            # while it is waiting for automatic clearing.
            # -------------------------------------------------

            with self.lock:

                if (
                    self.clear_scheduled
                    and text == self.pending_clear_text
                ):
                    return

            # -------------------------------------------------
            # AI Prediction
            # -------------------------------------------------

            label, confidence = predict(text)

            risk = calculate_risk(
                label,
                confidence
            )

            # -------------------------------------------------
            # Log Detection
            # -------------------------------------------------

            try:

                logger.log_detection(risk)

            except Exception as e:

                print(
                    "Logging Error:",
                    e
                )

            # -------------------------------------------------
            # Display Detection
            # -------------------------------------------------

            print()
            print("=" * 60)
            print("Clipboard Detection")
            print("=" * 60)

            print(
                "Category      :",
                risk.category
            )

            print(
                f"Confidence    : {risk.confidence:.4f}"
            )

            print(
                "Risk Level    :",
                risk.risk_level
            )

            print(
                "Risk Score    :",
                risk.risk_score
            )

            print(
                "Explanation   :",
                risk.explanation
            )

            print(
                "Action        :",
                risk.action
            )

            print("=" * 60)

            # -------------------------------------------------
            # Desktop Notification
            # -------------------------------------------------

            notifications_enabled = self.settings.get(
                "notifications_enabled"
            )

            if notifications_enabled and risk.category != "safe":
                try:
                    if callable(self.on_notification):
                        self.on_notification(risk)
                    else:
                        NotificationService.show_notification(risk)
                except Exception as e:
                    print("Notification Dispatch Error:", e)

            # -------------------------------------------------
            # Read Settings
            # -------------------------------------------------

            auto_clear_enabled = self.settings.get(
                "auto_clear_enabled"
            )

            configured_timeout = self.settings.get(
                "clear_timeout"
            )

            # -------------------------------------------------
            # Automatic Clear Disabled
            # -------------------------------------------------

            if not auto_clear_enabled:

                print(
                    "Automatic clipboard clearing is disabled."
                )

                return

            # -------------------------------------------------
            # Validate Timeout
            # -------------------------------------------------

            if configured_timeout <= 0:

                print(
                    "Automatic clipboard clearing disabled "
                    "because timeout is invalid."
                )

                return

            # -------------------------------------------------
            # Schedule Clear
            # -------------------------------------------------

            with self.lock:

                # Another clear is already running
                if self.clear_scheduled:

                    print(
                        "Clipboard clear already scheduled."
                    )

                    return

                self.clear_scheduled = True

                self.pending_clear_text = text

            print(
                "Auto Clear    :",
                configured_timeout,
                "seconds"
            )

            threading.Thread(
                target=self.clear_after_delay,
                args=(
                    configured_timeout,
                    text
                ),
                daemon=True
            ).start()

        except Exception as e:

            print(
                "Processing Error:",
                e
            )

    # =========================================================
    # Clear Clipboard After Delay
    # =========================================================

    def clear_after_delay(
        self,
        seconds,
        scheduled_text
    ):

        print(
            f"Clipboard will be cleared in "
            f"{seconds} seconds..."
        )

        time.sleep(seconds)

        try:

            # -------------------------------------------------
            # Check Auto Clear Setting Again
            # -------------------------------------------------

            if not self.settings.get(
                "auto_clear_enabled"
            ):

                print(
                    "Auto Clear disabled. "
                    "Clear operation skipped."
                )

                return

            # -------------------------------------------------
            # Read Current Clipboard
            # -------------------------------------------------

            current_text = self.get_clipboard_text()

            # -------------------------------------------------
            # Only Clear Original Content
            # -------------------------------------------------

            if current_text == scheduled_text:

                success = clear_clipboard()

                if success:

                    print(
                        "Clipboard cleared successfully."
                    )

            else:

                print(
                    "Clipboard content changed. "
                    "Clear operation skipped."
                )

        except Exception as e:

            print(
                "Clipboard Clear Error:",
                e
            )

        finally:

            with self.lock:

                self.clear_scheduled = False
                self.pending_clear_text = None
                self.last_text = ""

    # =========================================================
    # Safe Clipboard Read
    # =========================================================

    def get_clipboard_text(self):

        try:

            text = pyperclip.paste()

            if text is None:
                return ""

            return str(text)

        except Exception:

            return ""

    # =========================================================
    # Clipboard Monitoring Loop
    # =========================================================

    def monitor(self):

        self.running = True

        print()
        print("=" * 60)
        print("Clipboard Monitor Started")
        print("=" * 60)
        print("Copy any text...")
        print()

        while self.running:

            # -------------------------------------------------
            # Check Monitoring Setting
            # -------------------------------------------------

            if not self.settings.get(
                "monitoring_enabled"
            ):

                self.last_text = ""

                time.sleep(0.5)

                continue

            # -------------------------------------------------
            # Read Clipboard
            # -------------------------------------------------

            clipboard_text = self.get_clipboard_text()

            if not clipboard_text:

                time.sleep(0.5)

                continue

            # -------------------------------------------------
            # Detect Clipboard Change
            # -------------------------------------------------

            if clipboard_text != self.last_text:

                self.last_text = clipboard_text

                threading.Thread(
                    target=self.process_clipboard,
                    args=(clipboard_text,),
                    daemon=True,
                ).start()

            time.sleep(0.5)

    # =========================================================
    # Stop Monitor
    # =========================================================

    def stop(self):

        self.running = False

        print()
        print(
            "Clipboard Monitor Stopped"
        )


# =============================================================
# Main
# =============================================================

if __name__ == "__main__":

    monitor = ClipboardMonitor()

    try:

        monitor.monitor()

    except KeyboardInterrupt:

        monitor.stop()