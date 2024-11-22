from datetime import datetime

# Get the current date and time
current_time = datetime.now()

print("Current Date and Time:", current_time)

from datetime import datetime
from zoneinfo import ZoneInfo

# Get the system's timezone
local_timezone = datetime.now().astimezone().tzinfo

print("Local Timezone:", local_timezone)

from geopy.geocoders import Nominatim
import requests

def get_location():
    # Get public IP address
    response = requests.get("https://ipinfo.io/")
    if response.status_code == 200:
        data = response.json()
        location = data.get("loc")  # Format: "latitude,longitude"
        city = data.get("city")
        region = data.get("region")
        country = data.get("country")
        return f"Location: {location} ({city}, {region}, {country})"
    else:
        return "Unable to get location."

print(get_location())


