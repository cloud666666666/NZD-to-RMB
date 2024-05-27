import json
import smtplib
from email.mime.text import MIMEText
import requests
from bs4 import BeautifulSoup
def get_nzd_to_cny_rate():
    url = "https://www.xe.com/currencyconverter/convert/?Amount=1&From=NZD&To=CNY"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    rate_element = soup.find("p", {"class": "sc-1c293993-1 fxoXHw"})
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
def get_weather_focast():
    url = "https://www.msn.com/en-nz/weather/forecast/in-AUK,Albert-Eden-Local-Board-Area?ocid=ansmsnweather&cvid=f4fa2003db5c4019bc116bdb2b423d94&loc=eyJsIjoi5aWn5YWL6JitIiwiciI6IkFVSyIsInIyIjoiQWxiZXJ0LUVkZW4gTG9jYWwgQm9hcmQgQXJlYSIsImMiOiLmlrDopb%2FlhbAiLCJpIjoiTloiLCJnIjoiemgtY24iLCJ4IjoiMTc0Ljc2NjY2MjU5NzY1NjI1IiwieSI6Ii0zNi44NjY2NjEwNzE3NzczNDQifQ%3D%3D&weadegreetype=C"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    weather_element = soup.find("div", {"class": "summaryCaptionCompact-E1_1"})
    low_temp_element= soup.find("div", {"class": "temp-E1_1 tempSelected-E1_1"})
    high_temp_element=soup.find("div", {"class": "topTemp-E1_1 temp-E1_1 tempSelected-E1_1"})
    script_tag = soup.find('script',{'id': 'redux-data'}, type='application/json')
    if script_tag:
        json_text = script_tag.string.strip()  # Remove any surrounding whitespace
        data = json.loads(json_text)  # Parse JSON
        probablity=data['entryPoint']['WeatherPageV2_default__WeatherPageV2']['_@STATE@_']['currentWeatherCondition']['precipitation']['children']

    message='Weather: '+weather_element.text.strip()+'\nLow: '+low_temp_element.text+'\nHigh: '+high_temp_element.text+'\nProbablity of rain is '+probablity
    return message




def send_email(subject, message, to_email):
    SMTP_SERVER = 'smtp.qq.com'
    SMTP_PORT = 587
    SMTP_USERNAME = '2353493891@qq.com'  # 更改为您的Email地址
    SMTP_PASSWORD = 'gswqhdstochteceh'  # 更改为您的Email密码授权码
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
def start_nzd_to_cny_rate():
    if float(rate):
        message = f"Today's NZD to CNY rate is: {rate}"
        send_email("NZD to CNY " + rate, message, to_email="2353493891@qq.com")
        send_email("NZD to CNY " + rate, message=message, to_email="3475157643@qq.com")
    else:
        message = '网页结构已发生更改，请联系作者重新更新脚本'
        send_email(subject='Notice', message=message, to_email="2353493891@qq.com")
        send_email(subject='Notice', message=message, to_email="3475157643@qq.com")
def start_weather_focast():
    message = get_weather_focast()
    if message:
        send_email("Today Weather", message=message, to_email="2353493891@qq.com")
        send_email("Today Weather", message=message, to_email="3475157643@qq.com")
    else:
        message = '网页结构已发生更改，请联系作者重新更新脚本'
        send_email(subject='Notice', message=message, to_email="2353493891@qq.com")
        send_email(subject='Notice', message=message, to_email="3475157643@qq.com")

if __name__ == "__main__":
    rate = get_nzd_to_cny_rate()
    start_weather_focast()
    start_nzd_to_cny_rate()



