import requests
from datetime import datetime
import smtplib
import time


MY_EMAIL="sena@gmail.com"
MY_PASSWORD="abcd1234"
MY_LAT = 39.896519 
MY_LONG = 32.861969 
def iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    #Your position is within +5 or -5 degrees of the ISS position.
    if  35<=iss_latitude<=44 and 27<=iss_longitude<=37:
        return True
    else:
        return False

    
def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour
    if time_now>= sunset or time_now<=sunrise:
        return True
while True:
    time.sleep(60)
    if iss_overhead() and is_night():
        connection=smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(MY_EMAIL,MY_PASSWORD)
        connection.sendmail(
            from_addr="sena@email.com",
            to_addrs="sena@gmail.com",
            msg="Subject:ISS Overhead Notifier\n\n ISS is above you in the sky. "
        )

