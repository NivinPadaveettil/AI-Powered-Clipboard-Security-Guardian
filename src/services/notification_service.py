import sys
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QStyle


class NotificationService:

    _tray_icon = None

    @classmethod
    def get_tray_icon(cls):
        if cls._tray_icon is None and QApplication.instance():
            app = QApplication.instance()
            cls._tray_icon = QSystemTrayIcon(app)
            style = app.style()
            icon = style.standardIcon(QStyle.StandardPixmap.SP_MessageBoxWarning)
            cls._tray_icon.setIcon(icon)
            cls._tray_icon.show()
        return cls._tray_icon

    @classmethod
    def show_notification(cls, risk):
        try:
            category = getattr(risk, "category", "Unknown")
            risk_level = getattr(risk, "risk_level", "Medium")
            risk_score = getattr(risk, "risk_score", 0)
            explanation = getattr(risk, "explanation", "")

            title = f"⚠ Sensitive Clipboard Data ({risk_level} Risk)"
            message = (
                f"Category: {category}\n"
                f"Risk Score: {risk_score}/100\n"
                f"{explanation}"
            )

            tray = cls.get_tray_icon()
            if tray and QSystemTrayIcon.isSystemTrayAvailable():
                tray.showMessage(
                    title,
                    message,
                    QSystemTrayIcon.MessageIcon.Warning,
                    5000
                )
            else:
                try:
                    from plyer import notification
                    notification.notify(
                        title=title,
                        message=message,
                        timeout=8,
                        app_name="AI Security Clipboard Guardian",
                    )
                except Exception:
                    print(f"Notification fallback error: {message}", file=sys.stderr)
        except Exception as e:
            print(f"Notification Error: {e}", file=sys.stderr)
