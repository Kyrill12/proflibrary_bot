# from openai import OpenAI
import sql_for_bot
import smtplib
from email.mime.text import MIMEText
import schedule
import time

def email_sending(msg):
    sender_email = "jvastroi@mail.ru"
    sender_pass = "IGKMnUkJgjuqqwonil7t"

    message_to_admin = MIMEText(msg)
    message_to_admin["Subject"] = "Статистика о часто задаваемых вопросах"
    message_to_admin["From"] = sender_email
    message_to_admin["To"] = "kyrill.sobolevskiy10@gmail.com"

    try:
        with smtplib.SMTP_SSL("smtp.mail.ru", 465) as server:  # Для Gmail
            server.login(sender_email, sender_pass)
            server.sendmail(sender_email, "kyrill.sobolevskiy10@gmail.com", message_to_admin.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")


def email_every_monday():
    schedule.every().monday.at("08:30").do(email_sending, sql_for_bot.get_statistics())
    print("Скрипт запущен. Ожидание понедельника 8:30...")
    while True:
        schedule.run_pending()
        time.sleep(60)




# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders
#
# server_address = "smtp.mail.ru"
# server_port = 465
# login, password = "jvastroi@mail.ru", "IGKMnUkJgjuqqwonil7t"
#
# msg = MIMEMultipart()
# msg['From'], msg['To'], msg['Subject'] = "jvastroi@mail.ru", "kyrill.sobolevskiy10@gmail.com", "Тема вашего письма"
# msg.attach(MIMEText("Содержимое письма", 'plain'))
#
# file_path = "aaa.txt"
# with open(file_path, "rb") as file:
#     part = MIMEBase('application', 'octet-stream')
#     part.set_payload(file.read())
#     encoders.encode_base64(part)
#     part.add_header('Content-Disposition', f"attachment; filename={file_path}")
#
# msg.attach(part)
# server = smtplib.SMTP_SSL(server_address, server_port)
# server.login(login, password)
# server.send_message(msg)

# def create_answer():
#     statistics = sql_for_bot.get_statistics()
#
#     prompt = f"""
#         Проанализируй статистику вопросов чат-бота и предоставь аналитику:
#         {statistics}
#
#         В аналитике должно быть:
#         1. Топ-5 самых частых вопросов
#         2. Общее количество заданных вопросов
#         3. Рекомендации по улучшению бота на основе популярных запросов
#         """
#
#     client = OpenAI(api_key="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")
#     completion = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {"role": "developer", "content": "Рассуждай как аналитик"},
#             {
#                 "role": "user",
#                 "content": prompt,
#             },
#         ],
#     )
#
#     print(completion.choices[0].message.content)
#
#
# create_answer()

