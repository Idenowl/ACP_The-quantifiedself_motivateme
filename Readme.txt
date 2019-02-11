
Need : pyKML, xlml, urllib

urllib can cause an error, have to modify a line in the urllib lib code

The kmlparser.py take all the kml file in the data folder

Put KML file in data folder
Run kml parser.py 
The output files will be in csv folder 
json function to do
How works the category
	first it check the category given by google and label our category with this information. (I put both French/english some case because for the moment my kml filse are a mix of french and english)
	then, it compare with the file listcategoryM who give category to name place.(We have different home,different work place..., we can have each one list) 
	After theses steps if no category it took the hypothese that we are in a friend places or spend time somewhere/socializing.

