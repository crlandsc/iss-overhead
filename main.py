import requests
from datetime import datetime
import smtplib
import time

# lat/long constants
MY_LAT = 41.956820
MY_LONG = -87.677890
parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

# Email constants
sender_email = "SENDER_EMAIL_ADDRESS"
recipient_email = "RECIPIENT_EMAIL_ADDRESS"  # Grab email from current selection
sender_password = "SENDER_PASSWORD"


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()  # Returns the response code from the API

    data = response.json()
    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])

    # Check if my position is within +5 or -5 degrees of the ISS position.
    if MY_LONG-5 < iss_longitude < MY_LONG+5 and MY_LAT-5 < iss_latitude < MY_LAT+5:
        return True
    else:
        return False


def is_night():
    # Get Sunrise & Sunset Times
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])  # Get sunrise hour
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])  # Get sunset hour

    time_now = datetime.now().hour

    if sunset < time_now < sunrise:
        return True


# Send an email to myself if the ISS is overhead and it is nighttime. The code will run every 60 sec
while True:  # Always run code
    time.sleep(60)  # run code every 60 seconds
    if is_night() and is_iss_overhead():  # Check if it is nighttime and if the ISS is overhead
        # Email a note to look up
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:  # address and port number
            connection.starttls()  # start security TLS protocol
            connection.login(user=sender_email, password=sender_password)  # Connect to email
            # Send mail
            connection.sendmail(
                from_addr=sender_email,
                to_addrs=recipient_email,
                msg=f"Subject:Look Up 👆\n\nThe ISS is above you in the sky right now!"
            )
