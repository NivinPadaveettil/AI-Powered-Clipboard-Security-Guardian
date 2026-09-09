from plyer import notification


class NotificationService:

    @staticmethod
    def show_notification(risk):

        title = f"AI Clipboard Guardian - {risk.risk_level}"

        message = (
            f"Category: {risk.category}\n"
            f"Risk Score: {risk.risk_score}\n"
            f"{risk.explanation}"
        )

        notification.notify(
            title=title,
            message=message,
            timeout=8,
            app_name="AI Clipboard Guardian",
        )