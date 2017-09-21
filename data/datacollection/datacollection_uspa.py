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
    # TODO: classic raw, single ply, multi ply

    # 2) Load each html document and parse each record
    # TODO: can replace url query string value for 'output' variable to be 'csv', which is probably easier to parse...
    parse_junior_csv(junior_men_raw, "RAW - Junior Men")
    #parse_fullpower_csv("C:\\temp\\pl-data\\junior.csv", "RAW - Junior Men")
    print("end")

""" Parses a csv file """
def parse_junior_csv(url, name):
    try:
        print("parsing: {}".format(url))
        response = urllib.request.urlopen(url)
        csv_list = list(csv.reader(io.TextIOWrapper(response)))

        # 1) loop thru rows and find "Junior Age 13-15 section"
        start_index1 = 0 # stores start index for "age 13-15" section
        found = False
        while start_index1 < len(csv_list):
            cell = csv_list[start_index1][0]
            start_index1 = start_index1 + 1
            if ("13" in cell and "15" in cell):
                found = True
                break
        if (not found): raise ValueError("\"Junior Age 13-15 section header not found\"")

        # 2) loop thru rows and find "Junior Age 16-17 section"
        start_index2 = start_index1 + 1 # stores start index for "age 16-17" section
        found = False
        while(start_index2 < len(csv_list)):
            cell = csv_list[start_index2][0]
            start_index2 = start_index2 + 1
            if("16" in cell and "17" in cell):
                found = True
                break
        if (not found): raise ValueError("\"Junior Age 16-17 section header not found\"")

        # 3) loop thru rows and find "Junior Age 18-19 section"
        start_index3 = start_index2 + 1 # starts start index for "age 18-19" section
        found = False
        while(start_index3 < len(csv_list)):
            cell = csv_list[start_index3][0]
            start_index3 = start_index3 + 1
            if ("18" in cell and "19" in cell):
                found = True
                break
        if (not found): raise ValueError("\"Junior Age 18-19 section header not found\"")

        # 4) loop thru rows and find "Junior Age 20-23 section"
        start_index4 = start_index3 + 1 # starts start index for "age 20-23" section
        found = False
        while(start_index4 < len(csv_list)):
            cell = csv_list[start_index4][0]
            start_index4 = start_index4 + 1
            if ("20" in cell and "23" in cell):
                found = True
                break
        if (not found): raise ValueError("\"Junior Age 20-23 section header not found\"")

        # 5) with knowledge of the start,end of each section, parse each section, skipping column headers, and stopping before next section
        parse_fullpower_csv(url, csv_list, start_index1 + 1, start_index2 - 1)

    except Exception as e:
        print("Error parsing \"{}\": {}".format(name, e))

def parse_fullpower_csv(url, csv_list, start_index, endIdx):
    # column format: (Weight, <empty>, Lift, Kgs, Lbs, <empty>, Name, Date)
    lift_col_index = 2
    weight_col_index = 3
    name_col_index = 6
    date_col_index = 7

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
            lift_type = row[lift_col_index]

            # if (string is null) or (string is empty)
            if (lift_type == None) or (not lift_type.strip()):
                # blank line, skip
                continue

            # Parse the lift
            lift = Lift()
            lift.weight_class = weight_class
            lift.lift_type = row[lift_col_index]
            lift.weight_lifted = row[weight_col_index]
            lift.name = row[name_col_index]
            lift.date = row[date_col_index]
            lift.source = url
            print(lift)

        # TODO: now we know the weight class. this line and the next 3 lines will contain a record (Squat|Bench|Deadlift|Total)
        # TODO: parse it

def parse_open_csv()
    # TODO
    raise NotImplementedError

def parse_master_csv()
    # TODO
    raise NotImplementedError

def parse_singlelift_csv()
    # TODO
    raise NotImplementedError

# entry point
main()