from urllib.request import urlopen
import pykml
from pykml import parser
import os
from os import path
import csv
#####Open KML file#######################
pathfile='data/history-2018-12-27.kml'

def openkml(pathfile) :
    with open (pathfile) as f:
        doc=parser.parse(f)
    root=doc.getroot()

    return root


def KMLParser (Placemark) :
    # Declaration
    coord = [[["" for _ in range(len(Placemark))] for _ in range(len(Placemark))] for _ in range(len(Placemark))]
    time = [["" for _ in range(len(Placemark))] for _ in range(len(Placemark))]
    name = ["" for _ in range(len(Placemark))]
    category = [""] * len(Placemark)

    ######Reading KML file

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
                            #print("in loop")
                            #print(extend)
                            #print(extend[1].getchildren())
                            category[i]=extend[1].getchildren()
                            #print('print')
                            #print(category[i])
                        if child[5].tag=="{http://www.opengis.net/kml/2.2}TimeSpan" :
                            time[i] = child[5].getchildren()
            #if e.tag=="{http://www.opengis.net/kml/2.2}TimeSpan" :
                #time[i]=e.getchildren()
    return name,coord,time,category


#########Categorization ###################
def make_category(name,category,namefile):
    nc = []
    cc = []
    with open(namefile) as listcat:
        list_cat = csv.reader(listcat, delimiter=';')

        for row in list_cat:
            nc.append(row[0])
            cc.append(row[1])

    #print("nc",nc)
    #print("name",name, len(name))
    ncategory=[None]*len(name)
    for i in range(len(name)):
        #print("i= ",i)
        #print(type(name[i]),str(name[i]))
        # Read category from google maps and categorize them
        if "Magasin" in str(category[i]) or "Shop" in str(category[i]):
            ncategory[i] = 'Shopping'
        elif "Mus" in str(category[i]):
            ncategory[i] = "Socialization and Entertainment"
        elif str(category[i]) == "Bar":
            ncategory[i] = "Socialization and Entertainment"
        elif "Universtit" in str(category[i]):
            ncategory[i] = "Study Place"
        else:
            # categorize others place using a 'dictionary'
           # print(i,name[i])
            for j in range(len(nc)):
                if nc[j] in str(name[i]):
                    ncategory[i] = cc[j]
                    #print(ncategory[i])
            if ncategory[i] is None and i != 0:
                ncategory[i] = "Socialization and Entertainment"
    return ncategory

def clean(name,coord,time,category) :
     nn=[]
     cd=[]
     tt=[]
     cat=[]
     #print(len(coord))
     for i in range (len(coord)):
         if type(coord[i][0])!=list :
             nn.append(name[i])
             cd.append(coord[i])
             tt.append(time[i])
             cat.append(category[i])
     #print(cd)
     return nn,cd,tt,cat

###Writing CSV file
def Writefile(filename, name, coord, time, category):
    with open(filename, mode='w') as history_file:
        history_file = csv.writer(history_file, lineterminator='\n')

        # print(len(Placemark))
        # print(type(coord[2][0]))
        header = ["name", "x", "y", "z", "begin", "end", "category"]
        history_file.writerows([header])
        for i in range(len(name)):
            row = [str(name[i]), str(coord[i][0]), str(coord[i][1]), str(coord[i][2]), str(time[i][0]), str(time[i][1]),
                   str(category[i])]
            # print(row)
            history_file.writerow(row)

####Open several file
list_file=[]
path="data\\"
outputpath="csv\\"
files=os.listdir(path)


#make a list of kml file
for file in files :
    if file.endswith(".kml"):
        list_file.append(file)

count=0


for file in list_file :

    pathfile=path+file
    pathfile=os.path.abspath(pathfile)
    #print('working directory',os.getcwd())
    #print('path',pathfile)
    root=openkml(pathfile)

    Placemark = root.Document.Placemark
    [name, coord, time, category] = KMLParser(Placemark)
    [name, coord, time, category] = clean(name, coord, time, category)
    ncat = make_category(name, category, "listcategoryM.csv")
    #print("new category", ncat)

    output=outputpath+file.split('.')[0]+'.csv'
    Writefile(output, name, coord, time, ncat)
    count+=1
    print(count,output)

