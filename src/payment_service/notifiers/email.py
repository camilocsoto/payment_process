from commons import CustomerData

from .notifier import NotifierProtocol


class EmailNotifier(NotifierProtocol):
    def send_confirmation(self, customer_data: CustomerData):
        from email.mime.text import MIMEText

        msg = MIMEText("Thank you for your payment.")
        msg["Subject"] = "Payment Confirmation"
        msg["From"] = "no-reply@example.com"
        msg["To"] = customer_data.contact_info.email  # type: ignore

        # server = smtplib.SMTP("localhost")
        # server.send_message(msg)
        # server.quit()
        print("Email sent to", customer_data.contact_info.email)
