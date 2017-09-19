import urllib.request
from bs4 import BeautifulSoup 



url = 'http://uspa.net/uspa_national_records.html';
req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"}) 
con = urllib.request.urlopen( req )
soup = BeautifulSoup(con, 'html.parser')
anchor_tags = soup.findAll('a');

# TODO 1) enumerate the anchor link text for each section raw, classic raw, single ply, multi ply
rawDivisions = [
	'Junior - MEN'
]
classicRawDivisions = []
singlePlyDivisions = []
multiPlyDivisions = []

# TODO 2) find <ul> list tag for each section
# TODO 3) for each list, find each division ('Junior - MEN', 'Master - MEN', etc..) and load html document
# TOOD 4) for each html document containing records, parse the data and save it

#for anchor in soup.findAll('a', text = 'Master - MEN'):
	#print(anchor)

print("end")