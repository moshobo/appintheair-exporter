"""
App in the Air Exporter

This script is written to allow you to convert your data from the now-defunct 
"AppintheAir" (AITA) mobile app into a csv file.
"""

import argparse
import csv
import json
import logging

def timestamp_to_date(timestamp):
    date = timestamp.split("T")[0]
    return date

def timestamp_to_time(timestamp):
    time = timestamp.split("T")[1]
    return time

def get_aircraft_type(aircraft_code):
    """
    Takes the AppInTheAir aircraft code and returns the name of the aircraft as
    specified by IATA. These typically are 2-4 character IATA codes, but
    occasionally there is a need to use custom AppInTheAir overrides.

    Parameters:
    aircraft_code (str): 3-4 letter aircraft code from AppInTheAir
    """

    aita_overrides = {
        "7S8": "Boeing 737 (Scimitar Winglets)",
        "757": "Boeing 757",
    }

    with open('iata_aircraft_types.json', 'r') as json_file:
        type_data = json.load(json_file)

    type_data = {**type_data, **aita_overrides}

    if aircraft_code in [None, "None"]:
        return "Not specified"
    elif aircraft_code in type_data.keys():
        return type_data[aircraft_code]
    else:
        return "Error"
    
def convert_type_iata_to_icao(aircraft_code):
    if aircraft_code == "None":
        return aircraft_code
    else:
        with open('iata_icao_map.json', 'r') as json_file:
            map = json.load(json_file)
        try:
            return map[aircraft_code]
        except KeyError:
            return 'None'
    
def parse_flight_data(flight_objects, additional_fields):
    """
    Parse a line of data from the input file about a flight, and convert it to 
    dictionary of identified items. If the `additional_fields` argument is
    passed in, extra calculated fields will also be added.

    Parameters:
    flight_objects (list): List of strings containing information about a flight
    additional_fields (bool): If True, additional calculated fields will be 
    added to the dictionary

    Returns:
    flight_dict: A dictionary containing parsed flight data with relevant fields.
    """
    flight_dict = {
        "airline": flight_objects[7],
        "flight_code": flight_objects[8],
        "aircraft_type": flight_objects[9],
        "departure_airport": flight_objects[10],
        "arrival_airport": flight_objects[11],
        "departure_timestamp_gmt": flight_objects[12],
        "arrival_timestamp_gmt": flight_objects[13],
        "departure_timestamp_local": flight_objects[14],
        "arrival_timestamp_local": flight_objects[15]
    }
    if additional_fields:
        addons = {
            "flight_number": flight_objects[7] + flight_objects[8],
            "aircraft_type_name": get_aircraft_type(flight_objects[9]),
            "aircraft_type_icao": convert_type_iata_to_icao(flight_objects[9]),
            "departure_date_local": flight_objects[14][0:10],
            "arrival_date_local": flight_objects[15][0:10],
            "departure_time_local": flight_objects[14][11:],
            "arrival_time_local": flight_objects[15][11:]
        }
    
        flight_dict = {**flight_dict, **addons}

    return flight_dict

def main():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a', 
        '--additional_fields',
        action='store_true',
        help="Include additional fields in exported file"
    )
    parser.add_argument(
        '-f',
        '--filename',
        type=str,
        help="File name used for outputted csv. Should include .csv extension"
    )
    args = parser.parse_args()
    additional_fields = args.additional_fields

    with open('data.txt', 'r') as file:
        finput = [line.rstrip() for line in file]

    flights = []
    parse_next = False
    for i in range(len(finput)):
        if parse_next == True:
            if finput[i].split(":")[0] != "hotels":
                flight_objects = finput[i].split(";")
                data = parse_flight_data(flight_objects, additional_fields)
                flights.append(data)
            else:
                parse_next = False
                continue
        elif finput[i].split(":")[0] == "flights":
            parse_next = True
            continue

    logging.info(f"{str(len(flights))} flights found")

    filename = 'output.csv'
    if args.filename:
        filename = args.filename

    with open(filename, 'w', newline='') as outfile:
        fieldnames = flights[0].keys()
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(flights)

    logging.info(f"Data successfully saved in {filename}")

if __name__ == "__main__":
    main()
