import smtplib
import requests
import os

api_key = os.getenv("OWM_API_KEY") # security, or modifying recepients of mail lists, etc.
lat = 51.690090
long = 5.303690

url = "https://api.openweathermap.org/data/2.5/forecast"
params = {
    "lat": lat,
    "lon": long,
    "appid": api_key,
    "units": "metric",
    "cnt": 4,
}

response = requests.get(url, params=params)
response.raise_for_status()
data = response.json()
print(f"Status code: {data["cod"]}\n")

no_intervals = len(data["list"])
will_rain = False
descriptions = []
for interval in range(no_intervals):
    for condition in range(len(data["list"][interval]["weather"])):
        descriptions.append([data["list"][interval]["weather"][0][
                  "description"]," ",f"({str(data["list"][interval]["dt_txt"].split()[1].split(":")[0])}h)"]) # second 0 can also have higher indices for additional conditions
        if interval != no_intervals-1:
            descriptions.append(", ")
        if int(data["list"][interval]["weather"][condition]["id"]) < 700:
            will_rain = True

descriptions_n = ["".join(i) for i in descriptions] # joins each interval to a full string
print("\n")

my_email = os.getenv("MY_EMAIL")
password = os.getenv("EMAIL_PASSWORD")

if will_rain:
    with smtplib.SMTP("smtp.gmail.com",
                      port=587) as connection:  # this code belongs to the email of the SENDER, not recipient
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs=my_email,
                            msg=f"Subject:Rain predicted\n\nBring an umbrella today!\nForecast: {"".join(descriptions_n)}")
