import time
import threading
import pyperclip

from src.predict import predict
from src.core.risk_scoring import calculate_risk
from src.database.sqlite_logger import logger
from src.services.clipboard_service import clear_clipboard


class ClipboardMonitor:

    def __init__(self):

        self.last_text = ""
        self.running = False

        # Prevent multiple clear timers
        self.clear_scheduled = False

        # Text currently waiting to be cleared
        self.pending_clear_text = None

        # Protect shared state
        self.lock = threading.Lock()

    # =========================================================
    # Process Clipboard
    # =========================================================

    def process_clipboard(self, text):

        try:

            if not text or not text.strip():
                return

            # -------------------------------------------------
            # Prevent duplicate processing while a sensitive
            # clipboard value is waiting to be cleared.
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
            # Log detection
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

            if risk.timeout > 0:

                print(
                    "Auto Clear    :",
                    risk.timeout,
                    "seconds"
                )

            print("=" * 60)

            # -------------------------------------------------
            # Schedule Clear
            # -------------------------------------------------

            if risk.timeout > 0:

                with self.lock:

                    # Another clear is already running
                    if self.clear_scheduled:

                        print(
                            "Clipboard clear already scheduled."
                        )

                        return

                    self.clear_scheduled = True

                    self.pending_clear_text = text

                threading.Thread(
                    target=self.clear_after_delay,
                    args=(risk.timeout, text),
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
            # Only clear if the clipboard still contains the
            # sensitive value that triggered the timer.
            # -------------------------------------------------

            current_text = self.get_clipboard_text()

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

            clipboard_text = self.get_clipboard_text()

            # -------------------------------------------------
            # Ignore empty clipboard
            # -------------------------------------------------

            if not clipboard_text:

                time.sleep(0.5)

                continue

            # -------------------------------------------------
            # Check whether clipboard changed
            # -------------------------------------------------

            if clipboard_text != self.last_text:

                self.last_text = clipboard_text

                # -------------------------------------------------
                # Don't start another processing thread for the
                # same sensitive value while a timer is active.
                # -------------------------------------------------

                with self.lock:

                    already_pending = (
                        self.clear_scheduled
                        and clipboard_text
                        == self.pending_clear_text
                    )

                if not already_pending:

                    threading.Thread(
                        target=self.process_clipboard,
                        args=(clipboard_text,),
                        daemon=True
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