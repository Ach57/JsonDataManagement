import json
import sys
import random
import math
'''
    Full Name: Achraf Cheniti 
    Student ID: 40244865
    Assignment 02

'''

#Constants:
MAX_DISTANCE_THRESHOLD =0.1

def distance_between_points(point1, point2):
    # Calculate the Euclidean distance between two points in 2D space
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
def print_Menu(): # main menu
    '''
    Prints the main menu to the console.

    The menu options include:
    1. Display Global Statistics
    2. Display Base Station Statistics
    3. Check Coverage
    4. Exit
    '''
    print('----------- Menu -------------')
    print('1. Display Global Statistics')
    print('2. Display Base Station Statistics')
    print('3. Check Coverage')
    print('4. Exit')
    print('------------------------------')

def print_sub_menu():
    """
    Prints the submenu for Base Station Statistics to the console.

    The submenu options include:
    2.1. Statistics for a random station
    2.2. Choose a station by Id
    2.3. Back to Menu
    """
    print('2. Display Base Station Statistics')
    print('     2.1. Statistics for a random station')
    print('     2.2. Choose a station by Id.')
    print('     2.3. Back to Menu')


def handle_sub_menu(data):
    """
    Handles the submenu for Base Station Statistics.

    Displays the submenu options, takes user input, and performs actions based on the selected option.
    Allows the user to choose a random station, select a station by ID, or return to the main menu.

    The submenu options include:
    1. Display statistics for a random station
    2. Choose a station by ID
    3. Back to Menu

    Raises:
    ValueError: If the input is not a valid integer within the specified range.
    Exception: If an unspecified error occurs during input validation.
    """
    while True:
        print_sub_menu()
        try:
            input2 = int(input("Select an option: "))
            if input2 < 1 or input2 > 3:
                print("The number has to be within the range [1,3]\n")
            elif input2 == 1:
                print("Displaying Random Statistics for a station. . .")
                display_stats_for_random_station(data= data)
                #Randomly display information of a station
                # Add the function call or code to display statistics for a random station here
            elif input2 == 2:
                index = get_id_from_user(data=data) # id of the base station from the user 
                choose_station_by_id(index= index, data=data)
                # Add the function call or code to choose a station by ID here
            elif input2 == 3:
                break
        except ValueError:
            print("You must enter a number!\n")
        except Exception as e:
            print(f'Different exception occurred in validating number option 2. Message: {e}')
            exit(1)  # Exiting when a different exception occurs to fix it



def handle_main_menu_choice(choice, data) -> bool:
    """
    Handles the user's choice from the main menu.

    Based on the user's input, performs the corresponding action:
    1. Display Global Statistics
    2. Display Base Station Statistics (which leads to a submenu)
    3. Check Coverage
    4. Exit

    Parameters:
    choice (int): The user's menu selection.

    Returns:
    bool: True if the user chose to exit (option 4), False otherwise.
    """
    
    if choice == 1:
        print("Displaying Global Statistics...")
        handle_option1(data = data)
    elif choice == 2:
        handle_sub_menu(data= data)
    elif choice == 3:
        print("Checking Coverage...")
        handle_coverage(data=data)
        # Add the function call or code to check coverage here
    elif choice == 4:
        print("Thank you and see you again!")
        return True
    return False

def handle_option1(data):
    """
    Handles displaying global statistics based on the provided data.

    This function calculates and prints various statistics about the base stations and antennas:
    - Total number of base stations
    - Total number of antennas
    - Max, min, and average number of antennas per base station
    - Number of points covered by exactly one antenna
    - Number of points covered by more than one antenna
    - Number of points not covered by any antenna
    - Maximum number of antennas covering one point
    - Average number of antennas covering a point
    - Percentage of the covered area

    Additionally, it identifies the base station and antenna covering the maximum number of points.

    Parameters:
    data (dict): The JSON data containing base station and antenna information.

    Raises:
    KeyError: If there is a missing key in the JSON data.
    Exception: For any other unexpected errors.
    """
    try:
        base_station_data = data["baseStations"]
        num_base_stations = len(base_station_data)
        min_lat = data["min_lat"]
        max_lat = data["max_lat"]
        min_lon = data['min_lon']
        max_lon = data["max_lon"]
        step = data["step"]

        print(f"The total number of base stations = {num_base_stations}")

        num_of_antennas = 0
        num_of_antennalist = []
        point_count = {}

        point_list = [point[:2] for station in base_station_data for antenna in station["ants"] for point in antenna["pts"]]
        
        for station in base_station_data:
            num_of_antennas += len(station["ants"])
            num_of_antennalist.append(len(station["ants"]))
            
        print(f'The total number of antennas = {num_of_antennas}')
        num_of_antennalist.sort()
        print(f'The max, min and average of antennas per BS = {num_of_antennalist[-1]}, {num_of_antennalist[0]}, {sum(num_of_antennalist)/len(num_of_antennalist)}')

        for point in point_list:
            point_tuple = tuple(point)
            if point_tuple in point_count:
                point_count[point_tuple] += 1
            else:
                point_count[point_tuple] = 1
        
        unique_points = [point for point, count in point_count.items() if count == 1] 
        num_unique_points = len(unique_points)
        print(f"The total number of points covered by exactly one antenna = {num_unique_points}")
        
        
        max_count = max(point_count.values())
        max_points = len([point for point, count in point_count.items() if count == max_count])

        print(f"The total number of points covered by more than one antenna = {max_points}")
        Number_of_latitude_points = abs(max_lat- min_lat)/ step +1
        Number_of_longitude_points= abs(max_lon- min_lon)/step +1
        total_number_of_points = Number_of_latitude_points*Number_of_longitude_points
        covered_points = len(point_count)
        print(f"The total number of points not covered by any antenna = {round(total_number_of_points-covered_points)}")
        
        print(f"The maximum number of antennas that cover one point = {max_count}")
        
        print(f"The average number of antennas covering a point = {round(covered_points/num_unique_points,1)}")
        
        print(f"The percentage of the covered area = 100 x {covered_points}/{round(total_number_of_points)} = {round(100* covered_points/total_number_of_points,2)}")
        # Initialize tracking variables
        max_points = 0
        best_station_antenna = []

        # Iterate over each base station
        for station in base_station_data:
            # Iterate over each antenna in the current base station
            for antenna in station['ants']:
                # Get the number of points covered by the current antenna
                num_points = len(antenna['pts'])
                
                # Check if this antenna covers more points than the current maximum
                if num_points > max_points:
                    # Update the maximum points
                    max_points = num_points
                    
                    # Update the best station and antenna information
                    best_station_antenna = [station['id'], antenna['id']]

        # The result is stored in best_station_antenna
        print(f"The id of the base station and antenna covering the maximum number of points = base station {best_station_antenna[0]}, antenna {best_station_antenna[1]}")
    except KeyError as e:
        print(f"KeyError: {e}")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

def display_stats_for_random_station(data):
    """
    Display statistics for a randomly selected base station.

    This function calculates and prints various statistics for a randomly chosen base station:
    - Base station ID
    - Total number of antennas
    - Number of points covered by exactly one antenna
    - Number of points covered by more than one antenna
    - Number of points not covered by any antenna
    - Maximum number of antennas covering one point
    - Average number of antennas covering a point
    - Percentage of the covered area

    Additionally, it identifies the base station and antenna covering the maximum number of points.

    Parameters:
    data (dict): The JSON data containing base station and antenna information.

    Raises:
    KeyError: If there is a missing key in the JSON data.
    Exception: For any other unexpected errors.
    """
    try:
        base_station_data = data['baseStations']
        min_lat = data["min_lat"]
        max_lat = data["max_lat"]
        min_lon = data['min_lon']
        max_lon = data["max_lon"]
        step = data["step"]
        point_count = {}

        # Select a random base station from the list
        random_base_station = random.choice(base_station_data)
        number_of_antennas = len(random_base_station['ants'])
        print(f"Base Station Id selected: {random_base_station['id']}")
        print(f"The total number of antennas = {number_of_antennas}")

        # Create a list of points covered by antennas in the random base station
        point_list = [point[:2] for antenna in random_base_station['ants'] for point in antenna['pts']]

        # Count the occurrences of each point
        for point in point_list:
            point_tuple = tuple(point)
            if point_tuple in point_count:
                point_count[point_tuple] += 1
            else:
                point_count[point_tuple] = 1

        # Calculate statistics based on the point coverage
        unique_points = [point for point, count in point_count.items() if count == 1]
        num_unique_points = len(unique_points)
        print(f"The total number of points covered by exactly one antenna = {num_unique_points}")

        max_count = max(point_count.values())
        max_points = len([point for point, count in point_count.items() if count == max_count and max_count != 1])
        print(f"The total number of points covered by more than one antenna = {max_points}")

        Number_of_latitude_points = abs(max_lat - min_lat) / step + 1
        Number_of_longitude_points = abs(max_lon - min_lon) / step + 1
        total_number_of_points = Number_of_latitude_points * Number_of_longitude_points
        covered_points = len(point_count)
        print(f"The total number of points not covered by any antenna = {round(total_number_of_points - covered_points)}")
        print(f"The maximum number of antennas that cover one point = {max_count}")
        print(f"The average number of antennas covering a point = {round(covered_points / num_unique_points, 1)}")
        print(f"The percentage of the covered area = 100 x {covered_points}/{round(total_number_of_points)} = {round(100 * covered_points / total_number_of_points, 2)}")

        # Find the antenna covering the maximum number of points in the random base station
        max_points = 0
        best_station_antenna = []
        for antenna in random_base_station['ants']:
            num_points = len(antenna['pts'])
            if num_points > max_points:
                max_points = num_points
                best_station_antenna = [random_base_station['id'], antenna['id']]

        # Print the ID of the base station and antenna covering the maximum number of points
        print(f"The id of the base station and antenna covering the maximum number of points = base station {best_station_antenna[0]}, antenna {best_station_antenna[1]}")
    except KeyError as e:
        print(f"KeyError: {e}")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)


def get_id_from_user(data) -> int:
    """
    Prompts the user to select a base station ID from a specified range and returns its index in the `baseStations` list.

    Parameters:
    data (dict): The JSON data containing base station information.

    Returns:
    int: Index of the selected base station ID in the `baseStations` list.

    Raises:
    KeyError: If there is a missing key in the JSON data.
    Exception: For any other unexpected errors.
    """
    try:
        base_station_data = data['baseStations']
        dictionary_of_ids = {}

        # Create a dictionary mapping index to station ID
        for i, station in enumerate(base_station_data):
            dictionary_of_ids[i] = station['id']

        # Find the minimum and maximum station IDs
        min_id = dictionary_of_ids[0]
        max_id = dictionary_of_ids[len(dictionary_of_ids) - 1]

        # Create an inverted dictionary mapping station ID to index
        inverted_dictionary_of_ids = {station_id: index for index, station_id in dictionary_of_ids.items()}

        # Prompt the user to select an ID within the specified range
        while True:
            try:
                id = int(input(f"Select the id from the following range: [{min_id},{max_id}]: "))
                if id < min_id or id > max_id:
                    print("Range was not respected!")
                else:
                    # Return the index of the selected ID
                    return inverted_dictionary_of_ids[id]
            except ValueError as e:
                print(f"{e} - for id")
            except Exception as e:
                print(f"Different exception occurred - {e}")
                print("Exiting . . . ")
                exit(1)

    except KeyError as e:
        print(f"KeyError: {e}")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
def choose_station_by_id(index, data):
    """
    Selects a base station by index, retrieves its information, and displays various statistics about its antennas and coverage.

    Parameters:
    index (int): Index of the base station in the `baseStations` list.
    data (dict): The JSON data containing base station information.

    Raises:
    KeyError: If there is a missing key in the JSON data.
    Exception: For any other unexpected errors.
    """
    try:
        base_station_data = data['baseStations']
        min_lat = data["min_lat"]
        max_lat = data["max_lat"]
        min_lon = data['min_lon']
        max_lon = data["max_lon"]
        step = data["step"]
        
        # Retrieve the selected base station by index
        selected_station = base_station_data[index]
        point_count = {}
        
        # Calculate and display the number of antennas in the selected base station
        number_of_antennas = len(selected_station['ants'])
        print(f"Base Station Id selected: {selected_station['id']}") 
        print(f"The total number of antennas = {number_of_antennas}")
        
        # Extract all points covered by antennas in the selected base station
        point_list = [point[:2] for antenna in selected_station['ants'] for point in antenna['pts']]
        
        # Count occurrences of each point
        for point in point_list:
            point_tuple = tuple(point)
            if point_tuple in point_count:
                point_count[point_tuple] += 1
            else:
                point_count[point_tuple] = 1
        
        # Calculate statistics based on point coverage
        unique_points = [point for point, count in point_count.items() if count == 1] 
        num_unique_points = len(unique_points)
        print(f"The total number of points covered by exactly one antenna = {num_unique_points}")
        
        # Determine the number of points covered by more than one antenna
        max_count = max(point_count.values())
        max_points = len([point for point, count in point_count.items() if count == max_count and max_count != 1])
        print(f"The total number of points covered by more than one antenna = {max_points}")
        
        # Calculate total number of points, covered points, and not covered points
        Number_of_latitude_points = abs(max_lat - min_lat) / step + 1
        Number_of_longitude_points = abs(max_lon - min_lon) / step + 1
        total_number_of_points = Number_of_latitude_points * Number_of_longitude_points
        covered_points = len(point_count)
        print(f"The total number of points not covered by any antenna = {round(total_number_of_points - covered_points)}")
        
        # Display maximum antennas covering one point, average antennas covering points, and percentage of coverage
        print(f"The maximum number of antennas that cover one point = {max_count}")
        print(f"The average number of antennas covering a point = {round(covered_points / num_unique_points, 1)}")
        print(f"The percentage of the covered area = 100 x {covered_points}/{round(total_number_of_points)} = {round(100 * covered_points / total_number_of_points, 2)}")
        
        # Determine the base station and antenna covering the maximum number of points
        max_points = 0
        best_station_antenna = []
        for antenna in selected_station['ants']:
            num_points = len(antenna['pts'])
            if num_points > max_points:
                max_points = num_points
                best_station_antenna = [selected_station['id'], antenna['id']]
        
        # Display the base station and antenna ID covering the maximum number of points
        print(f"The id of the base station and antenna covering the maximum number of points = base station {best_station_antenna[0]}, antenna {best_station_antenna[1]}")
    
    except KeyError as e:
        print(f"KeyError: {e}")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)


def handle_coverage(data):
    """
    Function to handle coverage analysis based on user-provided latitude and longitude coordinates.

    Parameters:
    data (dict): JSON data containing base station information.

    Raises:
    KeyError: If there is a missing key in the JSON data.
    Exception: For any other unexpected errors.
    """
    try:
        # Get latitude and longitude from user input
        while True:
            try:
                lat = float(input("Enter the latitude: "))
                lon = float(input("Enter the longitude: "))
                break
            except ValueError as e:
                print(f"Error: {e}. Please enter a valid number.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}. Exiting...")
                exit(1)
        
        # User's coordinate
        user_point = [lat, lon]
        print(f"\nCoordinate (lat, lon): ({lat}, {lon})")
        
        # Initialize variables
        i = 1
        nearest_antenna = None
        nearest_distance = float('inf')
        covered_antennas = []
        
        # Retrieve base station data
        base_station_data = data['baseStations']
        
        # Iterate through each base station and its antennas
        for station in base_station_data:
            base_station_id = station['id']
            
            for antenna in station['ants']:
                antenna_id = antenna['id']
                frequency = antenna['frq']
                bandwidth = antenna['bw']
                
                for point in antenna['pts']:
                    antenna_point = point[:2]
                    received_power = point[2]
                    
                    # Check if user's point matches current antenna's coverage
                    if user_point == antenna_point:
                        # Add covered antenna information
                        covered_antennas.append({
                            'base_station_id': base_station_id,
                            'antenna_id': antenna_id,
                            'frequency': frequency,
                            'bandwidth': bandwidth,
                            'received_power': received_power,
                            'coordinates': antenna_point
                        })
                        i += 1
                    else:
                        # Calculate distance to find the nearest antenna
                        dist = distance_between_points(user_point, antenna_point)
                        if dist < nearest_distance:
                            nearest_distance = dist
                            nearest_antenna = {
                                'base_station_id': base_station_id,
                                'antenna_id': antenna_id,
                                'frequency': frequency,
                                'bandwidth': bandwidth,
                                'received_power': received_power,
                                'coordinates': antenna_point
                            }
        
        # If user's point is explicitly covered by any antenna, display covered antennas
        if covered_antennas:
            print("Coordinate is explicitly covered by the following antennas:")
            i = 1
            for antenna in covered_antennas:
                print(f"{i}. Base Station ID: {antenna['base_station_id']}")
                print(f"   Antenna ID: {antenna['antenna_id']}")
                print(f"   Frequency: {antenna['frequency']} MHz")
                print(f"   Bandwidth: {antenna['bandwidth']} MHz")
                print(f"   Received Power: {antenna['received_power']} dB")
                print(f"   Coordinates: ({antenna['coordinates'][0]}, {antenna['coordinates'][1]})\n")
                i += 1
            
        else:
            # If user's point is not explicitly covered, check and display the nearest antenna
            if nearest_antenna is not None and nearest_distance <= MAX_DISTANCE_THRESHOLD:
                print(f"{i}. Nearest Antenna:")
                print(f"   Base Station ID: {nearest_antenna['base_station_id']}")
                print(f"   Antenna ID: {nearest_antenna['antenna_id']}")
                print(f"   Frequency: {nearest_antenna['frequency']} MHz")
                print(f"   Bandwidth: {nearest_antenna['bandwidth']} MHz")
                print(f"   Received Power: {nearest_antenna['received_power']} dB")
                print(f"   Coordinates: ({nearest_antenna['coordinates'][0]}, {nearest_antenna['coordinates'][1]})\n")
            else:
                print("Coordinate is not explicitly covered by any base station.")
    
    # Handle potential errors
    except KeyError as e:
        print(f"KeyError: {e}. Please check the structure of your data.")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}. Exiting...")
        exit(1)


def main():
    if(len(sys.argv)!= 2):
        print("Usage: python3 your_code.py <json_file>")
        sys.exit(1)
    json_file= sys.argv[1]
    try:
        with open(file=json_file,mode="r") as f:
            data = json.load(f)
    except FileNotFoundError as e:
            print(f"{e}")
            print("Program existing. . .")
            exit(1)
    except Exception as e:
            print(f"Different exception occured - {e}")
            exit(1)
    while True:
        print_Menu()
        try:
            user_input = int(input("Select an option: "))
            if user_input < 1 or user_input > 4:
                print("The number has to be within range [1,4]\n")
            else:
                if handle_main_menu_choice(user_input, data):
                    break
        except ValueError:
            print("You must enter a number!\n")
        except Exception as e:
            print(f'Different exception occurred in validating number. Message: {e}')
            exit(1)  # Exiting when a different exception occurs to fix it
            
if __name__ == "__main__":
    """
    Main execution block that displays the main menu and handles user input.

    Continuously displays the menu and prompts the user to select an option.
    Validates the user's input and handles the selected option.
    Exits the loop and program if the user chooses to exit.

    Raises:
    ValueError: If the input is not a valid integer.
    Exception: If an unspecified error occurs during input validation.
    """
    
    main()
    
    
    

            
        
        
        

