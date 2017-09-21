""" This script pulls powerlifting csv data from remote server and parses it """

import csv
import io
import re
import urllib.request

from bs4 import BeautifulSoup 
from lift import Lift

#url = 'http://uspa.net/uspa_national_records.html';
#req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
#con = urllib.request.urlopen( req )
#soup = BeautifulSoup(con, 'html.parser')

""" Main entry point function """
def main():
    # TODO: parse the links from the web page, and do it in a separate module
    junior_men_raw = "https://docs.google.com/spreadsheets/d/1ZYDAv0uU9TONzAu1KPNWZPh6_44fa_SvapqJv1qTPUk/pub?output=csv";
    subopen_men_raw = "https://docs.google.com/spreadsheets/d/1uaxcPZKgNDQPBV0xd3cNmM0860rM2uznq-U4JDPLqBE/pub?output=csv";
    master_men_raw = "https://docs.google.com/spreadsheets/d/1wzK4fxhAni4mX6L95AOtpYfpV6SoGHv7z1TeLsbbEss/pub?output=csv";
    benchonly_men_raw = "https://docs.google.com/spreadsheets/d/1DLYJ0fT72TwjhUaCQzh-1AnUKb20TxH64NwSK-ApW4E/pub?output=csv";
    deadliftonly_men_raw = "https://docs.google.com/spreadsheets/d/1mVS2NVw52RQDGPg4RuX4xzu8S_ZGhW022XcLAt_-pbY/pub?output=csv";
    junior_women_raw = "https://docs.google.com/spreadsheets/d/1KQUj7y2zYlqr89-uK7GwxALzYwtaeRlLTJJ8C_voVqE/pub?output=csv";
    subopen_women_raw = "https://docs.google.com/spreadsheets/d/1HV9ZGk0wEwVWdy4AXzV5LVAtxhtbPx67Htn1j7gIGWg/pub?output=csv";
    master_women_raw = "https://docs.google.com/spreadsheets/d/1_L1jJKuVRKp2-1lAVP_gooN8TgF2mAa-6NeN6aVYeo8/pub?output=csv";
    benchonly_women_raw = "https://docs.google.com/spreadsheets/d/1RstHK4fL7CRMNoywgSU_j7hcVCiW-3-eKVPBEMPUcJg/pub?output=csv";
    deadliftonly_women_raw = "https://docs.google.com/spreadsheets/d/1CpGjuONPMR-16jXDKfojBcgNoOMhIpZdr5CxfglYA4E/pub?output=csv";

    # 2) Load each html document and parse each record
    parse_junior_csv(junior_men_raw, "RAW Men")
    parse_open_csv(subopen_men_raw, "RAW Men")
    print("end")

"""
Scan the list of CSV values, at specified cell, starting from specified index,
until a cell is found that contains each of the specified search terms

@param csv_list: List of CSV values, format: list of string arrays
@param search_values: List of strings to search for
@param start_index: The index of CSV list to start the search from
@param cell_index: The cell index of the CSV value to search
@param section_name: Text we are searching for, to report a relevant error in case it is not found.
@return: The index of the first matching CSV row
@raise ValueError: If no matches found
"""
def scan_csv_until(csv_list, search_values, start_index, cell_index, section_name):
    result = start_index
    found = False
    while result < len(csv_list):
        cell = csv_list[result][cell_index].lower()
        result = result + 1
        # if all of the search values are found in cell string
        if all(value in cell for value in search_values):
            found = True
            break
    if (not found): raise ValueError("\"{}\" header not found".format(section_name))
    return result

""" 
Parses a csv file containing JUNIOR class records 

@param url: url pointing to remote CSV file
@param name: name of the type of junior record sheet being parsed e.g. "RAW MEN", "SINGLE PLY WOMEN", ...
"""
def parse_junior_csv(url, name):
    try:
        print("parsing: {} at {}".format(name, url))
        response = urllib.request.urlopen(url)
        csv_list = list(csv.reader(io.TextIOWrapper(response)))

        # Find the starting index for each division section 
        start_index_13to15 = scan_csv_until(csv_list, ["13", "15"], 0, 0, "{} Junior Age 13-15".format(name))
        start_index_16to17 = scan_csv_until(csv_list, ["16", "17"], start_index_13to15 + 1, 0, "{} Junior Age 16-17".format(name))
        start_index_18to19 = scan_csv_until(csv_list, ["18", "19"], start_index_16to17 + 1, 0, "{} Junior Age 18-19".format(name))
        start_index_20to23 = scan_csv_until(csv_list, ["20", "23"], start_index_18to19 + 1, 0, "{} Junior Age 20-23".format(name))

        # With knowledge of the start,end of each section, parse each section, skipping column headers, and stopping before next section
        # TODO: store lift objects
        lifts_13to15 = parse_fullpower_csv(url, csv_list, start_index_13to15 + 1, start_index_16to17 - 1)
        lifts_16to17 = parse_fullpower_csv(url, csv_list, start_index_16to17 + 1, start_index_18to19 - 1)
        lifts_18to19 = parse_fullpower_csv(url, csv_list, start_index_18to19 + 1, start_index_20to23 - 1)
        lifts_20to23 = parse_fullpower_csv(url, csv_list, start_index_20to23 + 1, len(csv_list))
        
        print(*lifts_13to15, sep='\n')

    # catch all exceptions so parsing can continue if a failure occurs (format may have changed)
    except Exception as e:
        print("Error parsing \"{}\": {}".format(name, e))

""" Parse a CSV file containing OPEN and SUBMASTER class records """
def parse_open_csv(url, name):
    try:
        print("parsing: {} at {}".format(name, url))
        response = urllib.request.urlopen(url)
        csv_list = list(csv.reader(io.TextIOWrapper(response)))

        # Find the starting index for each division section (open, submaster)
        start_index_open = scan_csv_until(csv_list, ["open"], 0, 0, "{} Open".format(name))
        start_index_submaster = scan_csv_until(csv_list, ["submaster"], start_index_open + 1, 0, "{} Submaster".format(name))

        # With knowledge of the start,end of each section, parse each section, skipping column headers, and stopping before next section
        # TODO: store lift objects
        lifts_open = parse_fullpower_csv(url, csv_list, start_index_open + 1, start_index_submaster - 1)
        lifts_submaster = parse_fullpower_csv(url, csv_list, start_index_submaster + 1, len(csv_list))

    # catch all exceptions so parsing can continue if a failure occurs (format may have changed)
    except Exception as e:
        print("Error parsing \"{}\"".format(name, e))

""" Parse a CSV file containing MASTER class records """
def parse_master_csv(url, name):
    print("parsing: {} at {}".format(name, url))
    # TODO
    raise NotImplementedError

""" Parse a subset of a CSV record file, in the format of full power """
def parse_fullpower_csv(url, csv_list, start_index, endIdx):
    # column format: (Weight, <empty>, Lift, Kgs, Lbs, <empty>, Name, Date)
    lift_col_index = 2
    weight_col_index = 3
    name_col_index = 6
    date_col_index = 7

    result = []

    weight_class = None
    for i in range(start_index, endIdx):
        row = csv_list[i]
        weight_class_text = str(row[0]).strip()

        # if we have reached the next weight class
        if (weight_class_text):
            match = re.search(r"(\d*\.?\d+)kg", weight_class_text)
            if (match):
                weight_class = match.group(1)
            elif ("SHW" in weight_class_text):
                weight_class = "SHW"
            else:
                raise ValueError("Weight class not recognized from \"{}\"".format(weight_class_text))

        if (weight_class == None):
            raise ValueError("Weight class could not be determined")
        else:
            name = row[name_col_index]

            # if (string is null) or (string is empty)
            if (name == None) or (not name.strip()):
                # blank line or empty record, skip
                continue

            # Parse the lift
            lift = Lift()
            lift.weight_class = weight_class
            lift.lift_type = row[lift_col_index]
            lift.weight_lifted = row[weight_col_index]
            lift.name = row[name_col_index]
            lift.date = row[date_col_index]
            lift.source = url
            result.append(lift)

    return result

""" Parse a subset of a CSV record file, in the format of single lift """
def parse_singlelift_csv():
    # TODO
    raise NotImplementedError

# entry point
main()