import urllib.request
from bs4 import BeautifulSoup 

url = 'http://uspa.net/uspa_national_records.html';
req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"}) 
con = urllib.request.urlopen( req )
soup = BeautifulSoup(con, 'html.parser')

def main():
    # 1) store google doc link for each record set
    # TODO: if it turns out these links change often, add code to parse the links from the records page
    junior_men_raw = "https://docs.google.com/spreadsheets/d/1ZYDAv0uU9TONzAu1KPNWZPh6_44fa_SvapqJv1qTPUk/pub?output=html";
    subopen_men_raw = "https://docs.google.com/spreadsheets/d/1uaxcPZKgNDQPBV0xd3cNmM0860rM2uznq-U4JDPLqBE/pub?output=html";
    master_men_raw = "https://docs.google.com/spreadsheets/d/1wzK4fxhAni4mX6L95AOtpYfpV6SoGHv7z1TeLsbbEss/pub?output=html";
    benchonly_men_raw = "https://docs.google.com/spreadsheets/d/1DLYJ0fT72TwjhUaCQzh-1AnUKb20TxH64NwSK-ApW4E/pub?output=html";
    deadliftonly_men_raw = "https://docs.google.com/spreadsheets/d/1mVS2NVw52RQDGPg4RuX4xzu8S_ZGhW022XcLAt_-pbY/pub?output=html";
    junior_women_raw = "https://docs.google.com/spreadsheets/d/1KQUj7y2zYlqr89-uK7GwxALzYwtaeRlLTJJ8C_voVqE/pub?output=html";
    subopen_women_raw = "https://docs.google.com/spreadsheets/d/1HV9ZGk0wEwVWdy4AXzV5LVAtxhtbPx67Htn1j7gIGWg/pub?output=html";
    master_women_raw = "https://docs.google.com/spreadsheets/d/1_L1jJKuVRKp2-1lAVP_gooN8TgF2mAa-6NeN6aVYeo8/pub?output=html";
    benchonly_women_raw = "https://docs.google.com/spreadsheets/d/1RstHK4fL7CRMNoywgSU_j7hcVCiW-3-eKVPBEMPUcJg/pub?output=html";
    deadliftonly_women_raw = "https://docs.google.com/spreadsheets/d/1CpGjuONPMR-16jXDKfojBcgNoOMhIpZdr5CxfglYA4E/pub?output=html";
    # TODO: classic raw, single ply, multi ply

    # 2) Load each html document and parse each record (TODO: define data schema)
    # TODO: can replace url query string value for 'output' variable to be 'csv', which is probably easier to parse...
    parseFullPowerPage(junior_men_raw, "RAW - Junior Men")
    
    print("end")

def parseFullPowerPage(url, name):
    try:
        print("parsing: {}".format(url))
        req = urllib.request.Request(url, headers={})
        con = urllib.request.urlopen(req)
        soup = BeautifulSoup(con, "html.parser")

        # Find table
        table = soup.find("table")
        if(table == None): raise ValueError("html table not found")

        # Find table rows
        rows = soup.findAll("tr");
        if(rows == None or rows.count == 0): raise ValueError("html table rows not found")

        # TODO: search for section header "USPA AMERICAN JUNIOR - MEN             AGE 13-15" (determine reliable way to match that tag)
        # Following rows are records for that division, parse them

        # TODO: search for section header "USPA AMERICAN JUNIOR - MEN             AGE 16-17" (determine reliable way to match that tag)
        # Following rows are records for that division, parse them

        #USPA AMERICAN JUNIOR - MEN             AGE 18-19
        #USPA AMERICAN JUNIOR - MEN             AGE 20-23
        #

    except Exception as e:
        print("Error parsing \"{}\": {}".format(name, e))

def parseFullPowerCsv(url, name):
    try:
        print("parsing: {}".format(url))
        # TODO
    except Exception as e:
        print("Error parsing \"{}\": {}".format(name, e))

def parseSingleLiftPage(url):
    # TODO
    print("parsing: {}".format(url))

# entry point
main()