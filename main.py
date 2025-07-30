import smtplib
import requests
from bs4 import BeautifulSoup

AMAZON_URL = "URL"

MY_EMAIL = "SENDER EMAIL"
PASSWORD = "SENDER PASSWORD"
RECIPIENT_EMAIL = "RECIPIENT EMAIL"
# --------------------------------------------------------------
def send_mail(msg):
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=RECIPIENT_EMAIL, msg=msg)

# -------------------------------------------------------------
response = requests.get(AMAZON_URL)

soup = BeautifulSoup(response.content, "html.parser")
price = soup.find(name="span", class_="a-offscreen").get_text()

price_without_symbol = float(price.split("$")[1])
print(price_without_symbol)
target_price = 100

title = soup.find(id="productTitle").get_text().strip()
print(title)

if price_without_symbol <= target_price:
    message = f"{title} is on sale for {price}!"
    msg = f"Subject:Amazon Price Discount!\n\n{message}\n{AMAZON_URL}".encode("utf-8")
    send_mail(msg)

