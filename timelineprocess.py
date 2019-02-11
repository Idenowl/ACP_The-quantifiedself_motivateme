
import pykml
from pykml import parser
import os
from os import path
import csv
import json

def openkml(pathfile) :
    '''
    Open the kml file
    :param pathfile: path to the kml file
    :return: root of the kml file
    '''
    with open (pathfile) as f:
        doc=parser.parse(f)
    root=doc.getroot()

    return root


def KMLParser (Placemark) :
    '''

    :param Placemark: Placemark of KML file
    :return:list of name(string) of the place visited, list of coordinate of the place(list), list of begin and end time (list),list of google category
    '''
    # Declaration
    coord = [[["" for _ in range(len(Placemark))] for _ in range(len(Placemark))] for _ in range(len(Placemark))]
    time = [["" for _ in range(len(Placemark))] for _ in range(len(Placemark))]
    name = ["" for _ in range(len(Placemark))]
    category = [""] * len(Placemark)

    ######Reading KML file

    for i in range (len(Placemark)):
        child=Placemark[i].getchildren()

        for e in child :
            #Test if Point exist
            if e.tag == "{http://www.opengis.net/kml/2.2}Point":
                point_child=e.getchildren()
                #Test if coordinates for the point exist
                for pi in point_child :
                    if pi.tag=='{http://www.opengis.net/kml/2.2}coordinates' :
                        coord[i]=pi.text.split(',')

                        #Search the parents for name and category
                        parent=pi.getparent().getparent()
                        name[i]=parent.getchildren()[0]

                        #Category
                        #Category is in extend data (child of Placemark in position 3)
                        #Category data is a child of extend data in position 2
                        child=parent.getchildren()
                        if child[2].tag=="{http://www.opengis.net/kml/2.2}ExtendedData" :
                            extend=child[2].getchildren()
                            category[i]=extend[1].getchildren()
                        if child[5].tag=="{http://www.opengis.net/kml/2.2}TimeSpan" :
                            time[i] = child[5].getchildren()
            #if e.tag=="{http://www.opengis.net/kml/2.2}TimeSpan" :
                #time[i]=e.getchildren()
    return name,coord,time,category


#########Categorization ###################
def make_category(name,category,namefile):
    '''
    :param name: name of the place(list of string)
    :param category: list of google category (list of string)
    :param namefile: path of the file to read places labelled(string)
    :return:list of newcategory(list of string)
    '''
    nc = []
    cc = []
    with open(namefile) as listcat:
        list_cat = csv.reader(listcat, delimiter=';')

        for row in list_cat:
            nc.append(row[0])
            cc.append(row[1])

    ncategory=[None]*len(name)
    for i in range(len(name)):
        # Read category from google maps and categorize them with our categories
        if "Magasin" in str(category[i]) or "Shop" in str(category[i]):
            ncategory[i] = 'Shopping'
        #For Museum/Musee
        elif "Mus" in str(category[i]):
            ncategory[i] = "Socialization and Entertainment"
        elif str(category[i]) == "Bar":
            ncategory[i] = "Socialization and Entertainment"
        elif "Universtit" in str(category[i]):
            ncategory[i] = "Studying and working"
        else:
            # categorize others place by comparison with a list
            for j in range(len(nc)):
                if nc[j] in str(name[i]):
                    ncategory[i] = cc[j]
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
    '''
    Write the csv file
    :param filename: name and path of the file (string)
    :param name: list of name place (list of string)
    :param coord: list of coordinates (list of(list size3 of string))
    :param time: list of begin and end time (list of (list size2 of string))
    :param category: list of new category (list of string)
    :return:
    '''
    with open(filename, mode='w') as history_file:
        history_file = csv.writer(history_file, lineterminator='\n')
        header = ["name", "x", "y", "z", "begin", "end", "category"]
        history_file.writerows([header])
        for i in range(len(name)):
            row = [str(name[i]), str(coord[i][0]), str(coord[i][1]), str(coord[i][2]), str(time[i][0]), str(time[i][1]),
                   str(category[i])]
            history_file.writerow(row)

def WriteJsonfile(filename,name,coord,time,category) :
    ######TO DOOOO
    for i in range (len(name)):
        out=json.dumps({'name': str(name[i]), 'x': float(coord[i][0]), 'y':float(coord[i][1]),'begin':str(time[i][0]),'end' :str(time[i][1]),'category': str(category[i])})
        file=open(filename,'w')
        file.write(out)


if __name__ == '__main__':

    ####Open several file
    list_file=[]
    path="data/timeline/kml/"
    outputpath="data/timeline/csv/"
    outjson="data/timeline/json/"
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
        ncat = make_category(name, category, "data/timeline/listcategoryM.csv")
        #print("new category", ncat)

        output=outputpath+file.split('.')[0]+'.csv'
        json_file=outjson+file.split('.')[0]+'.json'
        Writefile(output, name, coord, time, ncat)
        WriteJsonfile(json_file, name, coord, time, ncat)
        count+=1
        print(count,output,json_file)

