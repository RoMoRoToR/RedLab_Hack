# src/notification.py

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, body, to_addrs):
    """
    Отправляет email с указанной темой и телом на указанные адреса.
    """
    from_addr = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")

    # Настройка SMTP сервера
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))

    # Формирование сообщения
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = ", ".join(to_addrs)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Подключение к серверу и отправка письма
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_addr, password)
        text = msg.as_string()
        server.sendmail(from_addr, to_addrs, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

def notify_anomalies(anomalies):
    """
    Отправляет уведомление о найденных аномалиях.
    """
    subject = "Anomalies Detected in IT System"
    body = f"The following anomalies have been detected:\n\n{anomalies}"
    to_addrs = os.getenv("RECIPIENTS").split(',')
    send_email(subject, body, to_addrs)

if __name__ == "__main__":
    # Пример использования
    anomalies = "1. Throughput anomaly on 2024-04-19 07:15:00 - 08:00:00 UTC\n" \
                "2. Web Response anomaly on 2024-04-20 07:20:00 - 07:40:00 UTC"
    notify_anomalies(anomalies)
