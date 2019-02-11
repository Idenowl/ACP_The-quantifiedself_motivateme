This project contains :  
	-Script for extracting data from Rescuetime 
	-Script for extracting data from Drive, sleep data and questionaire
	-Script for converting KML file and make category : timelineprocess.py
	-Script for merge the data: merge.py 

# Libraries
## PyKML

Library: pyKML
```
pip install pyKML
```

If you use python 3, urllib may cause an error. 
Use python 2 or modify parser.py in the library pyKML.

If you use python 3, in parser.py (in PML lib) replace 
```
import urllib2
```
by 
```
urllib.request
```
[For more information](https://hk.saowen.com/a/842ebc6395113594f3132b11c04f46c77f74ffd55e6c85f5d3063d8d36eb7314)

## Google drive API 
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```


# TimelineProcess 
This script convert the KML file into CSV and Json file. It also make new categorization. 

## How to use it 

Put KML file in data/timeline/kml
Run kml parser.py 
The output files will be in data/timeline/csv and data/timeline/json 

### How works the category

First it check the category given by google and label new category with this information. (to improve)
Then, it compare with the file listcategoryM who give category to name place. We have different home,different work place..., we can have each one list
After theses steps if no category it took the hypothese that we are in a friend places or spend time somewhere/socializing.

You should edit the listcategoryM.csv and place your home, workplace etc

# Extract data from Google Drive 
## OAuth 
### Client ID
Test with credentials.json our project drive in part 2 design and implementation and put in in the root of working directory or make a new one
#### Make a new Client ID
[go on google API console](https://console.developers.google.com/) 
Create a new project and allow drive API
Identifiants(key symbol) 
create ID OAuth and download it in json format
rename it in credentials.json and put in the root of the working directory. 

## Get the data from Sleep app 
Allow the synchronization with google drive on Sleep App
findfileid_sleep() return the file ID of the Sleep  
## Get the data from questionnaire 
The file ID link to result of the form copy on our google drive project
This will be update if changes.

# Extract data from Rescue Time : 
Note if your use python 2 : change import urllib.request to import urllib2

[Create an API key](https://www.rescuetime.com/anapi/manage) 
Copy the value of your API key in key/APIkey.txt 
The script will read your API key in this text file.

# Merge script 

Merge all the data in csv and json file 

