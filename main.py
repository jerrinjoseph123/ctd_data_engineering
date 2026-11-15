import requests


# Fetch JSON data from the chosen public API.
# The function returns None when the request or JSON decoding fails.
def api_request(api_endpoint):
    try:
        # Stop waiting after 10 seconds if the server does not respond.
        response = requests.get(api_endpoint, timeout=10)

        # HTTP 200 means the API returned a successful response.
        if response.status_code == 200:
            api_data = response.json()
            return api_data
        else:
            print(
                f"API call failed: {response.status_code} "
                f"- {response.reason}"
            )
            return None

    except requests.exceptions.RequestException as error:
        print(f"Network or request error: {error}")
        return None

    except ValueError:
        print("Error: API returned invalid JSON.")
        return None



# Keep only the country fields used by our CLI menus.
def transform_data(api_data):
    countries = []

    for country in api_data:
        countries.append({
            "name": country.get("name", "Unknown"),
            "region": country.get("region", "Unknown"),
            "population": country.get("population", 0),
            "area": country.get("area", 0),
            "capital": country.get("capital", "Unknown")
        })

    print(f"Successfully loaded {len(countries)} countries.")
    return countries


# Ask which API to use and return its URL, None, or "exit".
def api_explorer():
    api = input("""
Welcome to API Explorer!
1. Countries (Complete)
2. Open Library (Incomplete)
3. Pokemon (Incomplete)
4. Exit

Choose an API (1/2/3/4). Press Enter for default: """).strip()

    if api == "4":
        print("Thank you for using API Explorer!")
        return "exit"

    elif api == "1" or not api:
        api_endpoint = "https://countries.dev/countries"
        print("\nReading data from", api_endpoint, "...")
        return api_endpoint

    elif api == "2":
        print("Open Library API is not supported yet.")
        return None

    elif api == "3":
        print("Pokemon API is not supported yet.")
        return None

    else:
        print("Invalid choice.")
        return None
  

# Show country-related commands until the user chooses to go back.
def country_explorer(countries):
    while True:
        choice = input("""
Welcome to Country Explorer!
1. Filter countries by region
2. Find a country by name
3. Sort countries by population
4. Sort countries by area
5. Find the largest country by area
6. Find the largest country by population
7. Compare 2 countries side by side
8. Exit

Enter your choice (1-8): """).strip()

        if choice == "1":
            region = input("Enter a region: ").strip()
            filter_by_region(countries, region)

        elif choice == "2":
            country_name = input("Enter a country name: ").strip()
            filter_by_country(countries, country_name)

        # Sort highest-to-lowest using the population field.
        elif choice == "3":
            sorted_countries = sorted(
                countries,
                key=lambda x: x["population"],
                reverse=True
            )
            for country in sorted_countries:
                display_country(country)

        # Sort highest-to-lowest using the area field.
        elif choice == "4":
            sorted_countries = sorted(
                countries,
                key=lambda x: x["area"],
                reverse=True
            )
            for country in sorted_countries:
                display_country(country)

        elif choice == "5":
            largest_country = max(
                countries,
                key=lambda x: x["area"]
            )
            display_country(largest_country)

        elif choice == "6":
            largest_country = max(
                countries,
                key=lambda x: x["population"]
            )
            display_country(largest_country)

        # Look up both countries before comparing their values.
        elif choice == "7":
            country1_input = input("Enter the first country name: ").strip()
            country2_input = input("Enter the second country name: ").strip()

            country1 = filter_by_country(countries, country1_input)
            country2 = filter_by_country(countries, country2_input)

            if country1 and country2:
                compare_countries(country1, country2)
            else:
                print("One or both countries not found.")

        elif choice == "8":
            print("Thank you for using Country Explorer!")
            break

        else:
            print("Invalid choice. Enter a number from 1 to 8.")

def display_country(country):
    """Print information about one country."""
    print(
        f"{country['name']} - Region: {country['region']}, "
        f"Capital: {country['capital']}, "
        f"Population: {country['population']:,}, "
        f"Area: {country['area']:,} km²"
    )

def filter_by_region(countries, region):
    count = 0

    # Step 1: Count matching countries
    for country in countries:
        if country["region"].strip().lower() == region.strip().lower():
            count += 1

    # Step 2: Display the count first
    if count > 0:
        print(f"\nDisplaying {count} countries in {region}:\n")

        # Step 3: Display matching countries
        for country in countries:
            if country["region"].strip().lower() == region.strip().lower():
                display_country(country)
    else:
        print("No countries found in that region.")



# Find a country by name, ignoring case and extra surrounding spaces.
def filter_by_country(countries, country_name):
    for country in countries:
      if country["name"].strip().lower() == country_name.strip().lower():
        display_country(country)
        return country

    print("Country not found.")
    return None

def compare_countries(country1, country2):
    """Display two countries side by side and compare their sizes."""
    print("\nCountry Comparison")
    print(f"{'Category':<15} {country1['name']:<30} {country2['name']:<30}")
    print("-" * 78)

    for label, key in (
    ("Region", "region"),
    ("Capital", "capital"),
    ("Population", "population"),
    ("Area (km²)", "area")
    ):

      value1 = country1[key]
      value2 = country2[key]

      # Format numeric columns with commas for readability.
      if key in ("population", "area"):
          value1 = f"{value1:,}"
          value2 = f"{value2:,}"

      print(f"{label:<15} {str(value1):<30} {str(value2):<30}")

    # Only calculate a ratio if its denominator is greater than zero.
    if country2["population"] > 0:
        ratio = country1["population"] / country2["population"]
        print(f"\nPopulation ratio (first / second): {ratio:.2f}")
    else:
        print("\nPopulation ratio unavailable (second population is zero or missing).")

    if country2["area"] > 0:
        ratio = country1["area"] / country2["area"]
        print(f"Area ratio (first / second): {ratio:.2f}")
    else:
        print("Area ratio unavailable (second area is zero or missing).")



# Coordinate API selection, loading, and the country commands.
def main():
  while True:
    api_endpoint = api_explorer()

    if api_endpoint == "exit":
        break

    if api_endpoint is None:
        continue

    api_data = api_request(api_endpoint)

    # Check if its a list of records.
    if not isinstance(api_data, list):
        print("Unable to load data.")
        continue

    countries = transform_data(api_data)

    # Return here when the user exits the Country Explorer submenu.
    country_explorer(countries)


# Run main() only when this file is executed directly.
if __name__ == "__main__":
    main()
