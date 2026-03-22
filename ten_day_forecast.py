import sys
try:
    import requests
except ImportError:
    print("Error: the 'requests' library is not installed.")
    print("Install it in your environment and rerun:")
    print("    pip install requests")
    sys.exit(1)


def get_location_coordinates(city, state):
    """Return (latitude, longitude, resolved_city, resolved_state) for a US city/state."""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city,
        "country": "US",
        "count": 20,
        "language": "en",
        "format": "json",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        raise RuntimeError("Request timed out while looking up location.")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Network error during geocoding lookup: {e}")
    except ValueError:
        raise RuntimeError("Invalid response from geocoding service.")

    if not data or "results" not in data or not data["results"]:
        raise ValueError("Location not found.")

    state_normalized = state.strip().lower()
    results = data["results"]

    # Filter exact state match by admin1 field
    candidates = [r for r in results if r.get("admin1") and r.get("admin1").strip().lower() == state_normalized]
    if not candidates:
        # Also accept if admin1 abbreviates the state (e.g., "AL")
        candidates = [r for r in results if r.get("admin1") and r.get("admin1").strip().lower().startswith(state_normalized)]

    if not candidates:
        raise ValueError(f"Location not found for city '{city}' in state '{state}'.")

    best = candidates[0]

    return (
        best["latitude"],
        best["longitude"],
        best.get("name", city),
        best.get("admin1", state),
    )


def get_ten_day_forecast(latitude, longitude):
    """Fetch 10-day forecast in Fahrenheit and inches."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "temperature_unit": "fahrenheit",
        "precipitation_unit": "inch",
        "timezone": "auto",
        "forecast_days": 10,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        raise RuntimeError("Request timed out while fetching forecast.")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Network error during forecast retrieval: {e}")
    except ValueError:
        raise RuntimeError("Invalid response from forecast service.")

    daily = data.get("daily")
    if not daily:
        raise ValueError("No daily forecast data found.")

    dates = daily.get("time", [])
    maxes = daily.get("temperature_2m_max", [])
    mins = daily.get("temperature_2m_min", [])
    rain = daily.get("precipitation_sum", [])

    if not (dates and maxes and mins and rain):
        raise ValueError("Incomplete forecast data returned.")

    forecast = []
    for d, h, l, p in zip(dates, maxes, mins, rain):
        forecast.append({
            "date": d,
            "max": h,
            "min": l,
            "rain": p,
        })
    return forecast


def display_forecast(city, state, forecast):
    title = f"--- 10-Day Forecast for {city}, {state} ---"
    print(title)
    print("Date | Max Temp | Min Temp | Rain")
    print("-" * 50)

    for item in forecast:
        print(
            f"{item['date']} | "
            f"{item['max']:.1f}°F | "
            f"{item['min']:.1f}°F | "
            f"{item['rain']:.3f}inch"
        )


def main():
    print("US 10-Day Weather Forecast (open-meteo)")

    city = input("City: ").strip()
    state = input("State: ").strip()

    if not city or not state:
        print("City and state are required.")
        sys.exit(1)

    try:
        lat, lon, resolved_city, resolved_state = get_location_coordinates(city, state)
        forecast = get_ten_day_forecast(lat, lon)
        display_forecast(resolved_city, resolved_state, forecast)

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nCancelled by user.")
        sys.exit(1)


if __name__ == "__main__":
    main()
