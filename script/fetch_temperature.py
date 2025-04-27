import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://api.open-meteo.com/v1/forecast?latitude=35.8254&longitude=10.637&current_weather=true&hourly=temperature_2m,relativehumidity_2m"

try:
    response = requests.get(url, verify=False)  # SSL verification disabled
    print(f"Response Status: {response.status_code}")
    print("Response JSON:", response.text)  # Print raw response

    if response.status_code == 200:
        data = response.json()  # Convert response to JSON
        print("Formatted JSON:", data)
    else:
        print(f"Failed to fetch data: {response.status_code}")

except Exception as e:
    print(f"Error fetching weather data: {e}")
