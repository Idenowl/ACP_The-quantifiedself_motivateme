This project contains :  
* Script for extracting data from Rescuetime extractrescuetime.py
* Script for extracting data from Drive, sleep data and questionaire extractsleep.py
* Script for converting KML file and make category : timelineprocess.py
* Script for merge the data: merge.py 

All these scripts were made in Python36
# Libraries
## PyKML

Library: pyKML
```
pip install pyKML
```

urllib will cause an error on python 3

For python 3 you will need to modify parser.py in the library pyKML.
### Modify parser.py on python36
Modify parser.py from the library pykml

Replace 
```
import urllib2
```
by 
```
 import urllib.request
```
#### In a Virtual environnement 
I recommand to use a virtualenv.

After cloning the repository :
```
virtualenv ACP_The-quantifiedself_motivateme
cd ACP_The-quantifiedself_motivateme
Scripts\activate 
pip install pykml
```
And also install other librairies :
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
You will find the file to modify in : 
```
ACP_The-quantifiedself_motivateme\Lib\site-packages\pykml\parser.py
```
You will need to activate it, each session you want to use your virtualenv
```
Scripts\activate 
```

#### Find parser.py on windows 
If you don't use virtualenv.
The path of the file to modify parser.py may be the following path :
```
C:\Users\username\AppData\Local\Programs\Python\Python36\Lib\site-packages\pykml\parser.py
```

[For more information](https://hk.saowen.com/a/842ebc6395113594f3132b11c04f46c77f74ffd55e6c85f5d3063d8d36eb7314)

## Google drive API 
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

# TimelineProcess 
This script convert the KML file into CSV and Json file. It also make new categorization. 

## How to use it 

* Put KML file in data/timeline/kml
*Run timelineprocess 
```
python timelineprocess.py
```
*The output files will be in data/timeline/csv and data/timeline/json 

### How works the category

* First it check the category given by google and label new category with this information. (to improve)
* Then, it compare with the file listcategoryM who give category to name place. We have different home,different work place..., we can have each one list
* After theses steps if no category it took the hypothese that we are in a friend places or spend time somewhere/socializing.

You should edit the listcategoryM.csv and place your home, workplace etc

# Extract data from Google Drive 
## OAuth 
### Client ID
Test with the actual credentials.json should work or try with a new client ID for OAuth.
#### Make a new Client ID
* [Go on google API console](https://console.developers.google.com/) 
* Create a new project and allow drive API
* Identifiants(key symbol) 
* Create ID OAuth and download it in json format
* Rename it in credentials.json and put in the root of the working directory. 

## Get the data from Sleep app 
* Allow the synchronization with google drive on Sleep App
* findfileid_sleep() return the file ID of the Sleep

## Get the data from questionaires 
The file ID link to result of the form copy on our google drive project
This will be update if we changes it.

The script can be run individially 
```
python pythonextractsleep.py
```
# Extract data from Rescue Time : 
Note if your use python 2 : change import urllib.request to import urllib2

[Create an API key](https://www.rescuetime.com/anapi/manage) 
Copy the value of your API key in key/APIkey.txt 
The script will read your API key in this text file.

The script can be run individially 
```
python extractrescuetime.py -d <year-month-day>
python extractrescuetime.py -d 2019-02-08
```


# Merge script 
Merge call the others scripts and merge the data. 
To run merge
```
python merge.py -d <year-month-day> -p <participant_number>
```
Example
```
python merge.py 2019-02-08 -p 4
```



 

