# appintheair-exporter
Scripts to convert exported data from the defunct App in the Air into other formats

## Installation

### With Github
Run the following commands in your terminal to install this repository

```bash
git clone https://github.com/moshobo/appintheair-exporter.git
cd appintheair-exporter/
```

## Usage
1. Export your data from App in the Air [using their instructions](https://appintheair.com/shutdown/). You should receive a `data.txt` file in your email inbox
2. Put the `data.txt` in the directory for this repository
3. Run the script, which will automatically look for this `data.txt` file (unless you use the `--data_file` argument)

`python3 appintheair_exporter.py`

4. Review your data in the `output.csv` file

## Arguments
*additional_fields*: Use the `-a` or `--additional_fields` argument to export the following additional data when the output file is created
* `flight_number`: Combination of the airline code (ex: AA) and flight code (ex: 1234) 
* `aircraft_type_name`: English name of the aircraft type (ex: Boeing 737-800)
* `aircraft_type_icao`: 3-4 character ICAO code for the aircraft type
* `departure_date_local`: Date of departure in the departure airport's time zone in `YYYY-MM-DD` format
* `arrival_date_local`: Date of arrival in the arrival airport's time zone in `YYYY-MM-DD` format
* `departure_time_local`: Time of departure in the departure airport's time zone in `hh:mm:ss` format
* `arrival_time_local`: Time of arrival in the arrival airport's time zone in `hh:mm:ss` format
* `entry_method`: The method used to add flight data to AITA (manual or search)

Example Usage:
`python3 appintheair_exporter.py -a`

*data_file*: Use the `-d` or `--data_file` argument to specify the filename of the imported TXT file from App In The Air. Make sure to include the `.txt` extension. If you do not pass in this argument, the script will automatically look for a `data.txt` file.

Example Usage:
`python3 appintheair_exporter.py -d my_data.txt`

*filename*: Use the `-f` or `--filename` argument to specify the filename of the exported CSV file. Make sure to include the `.csv` extension

Example Usage:
`python3 appintheair_exporter.py -f exported_data_final.csv`
