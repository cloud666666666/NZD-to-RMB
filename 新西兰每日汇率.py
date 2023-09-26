import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import requests
def get_nzd_to_cny_rate():
    url = "https://www.xe.com/currencyconverter/convert/?Amount=1&From=NZD&To=CNY"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    rate_element = soup.find("p", {"class": "result__BigRate-sc-1bsijpp-1 iGrAod"})
    if rate_element:
        main_rate = rate_element.contents[0].strip()
        faded_digits_element = rate_element.find("span", {"class": "faded-digits"})
        if faded_digits_element:
            faded_digits = faded_digits_element.text.strip()
            rate = f"{main_rate}{faded_digits}"
        else:
            rate = main_rate
        return rate
    else:
        return None

def send_email(subject, message, to_email):
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    SMTP_USERNAME = 'yunhaowang326@gmail.com'  # 更改为您的Gmail地址
    SMTP_PASSWORD = 'loqnvapabnniauey'  # 更改为您的Gmail密码

    msg = MIMEText(message, 'plain', 'utf-8')
    msg['From'] = SMTP_USERNAME
    msg['To'] = to_email
    msg['Subject'] = subject

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    rate = get_nzd_to_cny_rate()
    if float(rate)<4.3:
        message = f"Today's NZD to CNY rate is: {rate}"
        send_email("NZD to CNY "+rate, message, "2353493891@qq.com")  # 更改为收件人的邮箱地址
