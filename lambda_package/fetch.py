import json
import requests
import urllib3

# Disable SSL warnings (use with caution)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def lambda_handler(event, context):
    # Get latitude and longitude from the event (or use default if not present)
    latitude = event.get("queryStringParameters", {}).get("latitude", "35.8245")
    longitude = event.get("queryStringParameters", {}).get("longitude", "10.6346")
    
    # API URL (Replace lat/lon with the desired location)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m"

    try:
        # Fetch data from Open-Meteo API
        response = requests.get(url, verify=False)  # SSL verification disabled
        response.raise_for_status()  # Raise error if response is not 200 OK

        data = response.json()

        # Return the weather data as a JSON string
        return {
            "statusCode": 200,
            "body": json.dumps(data)  # Ensure the body is a JSON string
        }

    except requests.RequestException as e:
        return {
            "statusCode": 500,
            "body": f"Error fetching weather data: {str(e)}"
        }