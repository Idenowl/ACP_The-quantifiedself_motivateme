from urllib.request import urlopen
import pykml
from pykml import parser
from os import path
import csv

#####Open KML file#######################
kml_file=path.join('data/history-2018-12-27.kml')
with open (kml_file) as f:
    doc=parser.parse(f)

root=doc.getroot()
Placemark=root.Document.Placemark

#Declaration
coord=[[["" for _ in range(len(Placemark))] for _ in range(len(Placemark))] for _ in range(len(Placemark))]
time=[["" for _ in range(len(Placemark))]for _ in range (len(Placemark))]
name=["" for _ in range(len(Placemark))]
category=[""]*len(Placemark)


print('len cat',len(category))
#Test zone
#print(root.Document.Placemark.Point.coordinates)
#print (Placemark[2].Point.coordinates)
child3=list(Placemark[2].getchildren())
#print(child3)
#n=3
print(child3[2].getchildren())
extend=child3[2].getchildren()
category2=extend[1].getchildren()
print(category2)
#print(Placemark[0].Point.coordinates)


######Reading KML file
print("Reading KML file.....")
for i in range (len(Placemark)):
    child=Placemark[i].getchildren()
    #print("i=",i)
    #print(child)
    for e in child :
        #Test if Point exist
        #print(e.tag)
        if e.tag == "{http://www.opengis.net/kml/2.2}Point":
            point_child=e.getchildren()
            #Test if coordinates for the point exist
            for pi in point_child :
                if pi.tag=='{http://www.opengis.net/kml/2.2}coordinates' :
                    coord[i]=pi.text.split(',')

                    #Search the parents for name and category
                    parent=pi.getparent().getparent()
                    #print(parent.getchildren())
                    #print(parent[0].tag)
                    name[i]=parent.getchildren()[0]

                    #Category
                    #Category is in extend data (child of Placemark in position 3)
                    #Category data is a child of extend data in position 2
                    child=parent.getchildren()
                    #print(child[2].tag)
                    if child[2].tag=="{http://www.opengis.net/kml/2.2}ExtendedData" :
                            #print(child[2].tag)
                            extend=child[2].getchildren()
                            #print(i)
                            print("in loop")
                            print(extend)
                            print(extend[1].getchildren())
                            category[i]=extend[1].getchildren()
                            print('print')
                            print(category[i])
                    if child[5].tag=="{http://www.opengis.net/kml/2.2}TimeSpan" :
                        time[i] = child[5].getchildren()
        #if e.tag=="{http://www.opengis.net/kml/2.2}TimeSpan" :
            #time[i]=e.getchildren()




###Writing CSV file

with open('test.csv', mode='w') as history_file :
    history_file=csv.writer(history_file,lineterminator='\n')
    #row=zip(name,coord[0],coord[1],coord[3],time[0],time[1],category)

    #print(len(row))

    #for r in row :
        #history_file.writerows(["name","x","y","z","begin","end","category"])
        #history_file.writerows(r)
    print(len(Placemark))
    print(type(coord[2][0]))
    header=["name", "x", "y", "z", "begin", "end", "category"]
    history_file.writerows([header])
    for i in range(len(Placemark)) :
        if type(coord[i][0])!=list :
            row =[str(name[i]), str(coord[i][0]), str(coord[i][1]),str(coord[i][2]), str(time[i][0]),str(time[i][1]), str(category[i])]
            print(row)
            history_file.writerow(row)
        #history_file.writerow('\n')