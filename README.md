# <u>Country Explorer CLI</u>
Country Explorer is an interactive Python command-line application.

The application retrieves country information from a public [Countries API](https://countries.dev/countries), transforms the JSON response into list of dictionaries, and allows users to explore and compare countries. The application retrieves information including: Country name, Region, Capital, Population, Area (km²)

Open Library and Pokémon are future options and are not implemented.

### <u>Features</u>
1. Filter countries by region and display the number of matching countries.
2. Search for a country by name.
3. Sort countries by population.
4. Sort countries by area.
5. Find the largest country by area.
6. Find the most populated country.
7. Compare two countries side by side, including population and area ratios.
8. Navigate interactive menus and exit the application.


### <u>Installation and Usage</u>
1. Clone the repository
2. Install dependencies
3. Run the application

Choose the Countries API or press Enter to use the default. Then select a Country Explorer menu option.

### <u>Error Handling</u>
The program includes HTTP status-code checks, exception handling for network errors and invalid JSON, and messages for unsupported API selections and invalid menu choices.


