Cellular Network Coverage Analyzer
This Python program analyzes the coverage of a cellular network provider based on data stored in a JSON file (test.json). The JSON file represents base stations, antennas, and coverage points in a specific geographical area.

Functionality
Upon execution, the program provides a menu interface for users to choose from the following options:

Display Global Statistics:

Provides overall statistics about the coverage area and base stations.
Display Base Station Statistics:

Submenu options:
2.1. Statistics for a random station: Displays statistics for a randomly selected base station.
2.2. Choose a station by Id: Allows the user to input a specific base station Id to display detailed statistics.
Check Coverage:

Allows users to check coverage by entering coordinates (latitude and longitude). The program determines which base station's antenna covers those coordinates and displays the received power.
Exit:

Terminates the program.
JSON File Format (test.json)
The test.json file contains:

A list of base stations (baseStations), each with:
id: Unique identifier.
location: Geographic coordinates.
ants: List of antennas, each with:
id: Unique identifier.
points: List of square points (coordinates and received power).


Example Structure:
{
  "baseStations": [
    {
      "id": 1,
      "location": [45.05, -75.05],
      "ants": [
        {
          "id": 1,
          "points": [[45.01, -73.00, -63.216], [45.02, -74.00, -64.123]]
        },
        {
          "id": 2,
          "points": [[45.03, -75.00, -65.432], [45.04, -75.10, -66.789]]
        }
      ]
    },
    {
      "id": 2,
      "location": [45.08, -73.10],
      "ants": [
        {
          "id": 3,
          "points": [[45.06, -73.05, -67.901], [45.07, -73.00, -68.345]]
        }
      ]
    }
  ]
}


Usage
To run the program, ensure you have Python installed and execute the following command in your terminal:

python main.py test.json

Replace test.json with the name of your JSON file containing the cellular network coverage data. This file should be in the same directory as main.py or you should provide the full path to the file.

Upon execution, the program will display a menu interface allowing you to interact with the cellular network coverage analyzer based on the data provided in the JSON file.

