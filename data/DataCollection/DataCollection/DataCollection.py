import csv
import io
import re
import urllib.request

from bs4 import BeautifulSoup 

#url = 'http://uspa.net/uspa_national_records.html';
#req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"}) 
#con = urllib.request.urlopen( req )
#soup = BeautifulSoup(con, 'html.parser')

def main():
    # 1) store google doc link for each record set
    # TODO: if it turns out these links change often, add code to parse the links from the records page
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
    parseJuniorCsv(junior_men_raw, "RAW - Junior Men")
    #parseFullPowerCsv("C:\\temp\\pl-data\\junior.csv", "RAW - Junior Men")
    print("end")


def parseJuniorCsv(url, name):
    try:
        print("parsing: {}".format(url))
        response = urllib.request.urlopen(url)
        csvList = list(csv.reader(io.TextIOWrapper(response)))
        
        # 1) loop thru rows and find "Junior Age 13-15 section"
        startIdx1 = 0 # stores start index for "age 13-15" section
        found = False
        while (startIdx1 < len(csvList)):
            cell = csvList[startIdx1][0]
            startIdx1 = startIdx1 + 1
            if ("13" in cell and "15" in cell):
                found = True
                break
        if (not found): raise ValueError("\"Junior Age 13-15 section header not found\"")

        # 2) loop thru rows and find "Junior Age 16-17 section"
        startIdx2 = startIdx1 + 1 # stores start index for "age 16-17" section
        found = False
        while(startIdx2 < len(csvList)):
            cell = csvList[startIdx2][0]
            startIdx2 = startIdx2 + 1
            if("16" in cell and "17" in cell):
                found = True
                break
        if (not found): raise ValueError("\"Junior Age 16-17 section header not found\"")

        # 3) loop thru rows and find "Junior Age 18-19 section"
        startIdx3 = startIdx2 + 1 # starts start index for "age 18-19" section
        found = False
        while(startIdx3 < len(csvList)):
            cell = csvList[startIdx3][0]
            startIdx3 = startIdx3 + 1
            if ("18" in cell and "19" in cell):
                found = True
                break
        if (not found): raise ValueError("\"Junior Age 18-19 section header not found\"")

        # 4) loop thru rows and find "Junior Age 20-23 section"
        startIdx4 = startIdx3 + 1 # starts start index for "age 20-23" section
        found = False
        while(startIdx4 < len(csvList)):
            cell = csvList[startIdx4][0]
            startIdx4 = startIdx4 + 1
            if ("20" in cell and "23" in cell):
                found = True
                break
        if (not found): raise ValueError("\"Junior Age 20-23 section header not found\"")

        # 5) with knowledge of the start,end of each section, parse each section, skipping column headers, and stopping before next section
        parseFullPowerCsv(csvList, startIdx1+1, startIdx2-1)

    except Exception as e:
        print("Error parsing \"{}\": {}".format(name, e))

def parseFullPowerCsv(csvList, startIdx, endIdx):
    # column format: (Weight, <empty>, Lift, Kgs, Lbs, <empty>, Name, Date)

    for i in range(startIdx, endIdx):
        row = csvList[i]
        weightText = str(row[0]).strip()

        # if we have reached the next weight class
        if (weightText):
            match = re.search(r"(\d*\.?\d+)kg", weightText)
            if (match):
                weight = match.group(1)
            elif ("SHW" in weightText):
                weight = "SHW"
            else:
                raise ValueError("Weight class not recognized from \"{}\"".format(weightText))
        
        # TODO: now we know the weight class. this line and the next 3 lines will contain a record (Squat|Bench|Deadlift|Total)
        # TODO: parse it

def matchWeightClass(value):
    weightClasses = [""]



# entry point
main()