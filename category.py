import csv

tab=[]
name=[]
category=[]
time=[]
nc=[]
cc=[]
with open('test.csv') as file :
    read=csv.reader(file,delimiter=',')

    for row in read:
        # print(row)
        name.append(row[0])
        time.append([row[4], row[5]])
        category.append(row[6])

with open("listcategoryM.csv") as listcat :
    list_cat=csv.reader(listcat,delimiter=';')

    for row in list_cat :
        nc.append(row[0])
        cc.append(row[1])

print (name)
#print(time)
#print(type(cc),nc)

#print(nc)
#print(len(cc))
#print(len(name))
ncategory=[None]*len(name)


print(len(ncategory))
for i in range(1,len(name)):
    if "Magasin" in category[i] or "Shop" in category[i] :
        ncategory[i]='Shopping'
    elif "Mus" in category[i] :
        ncategory[i]="Socialization and Entertainment"
    elif category[i]=="Bar":
        ncategory[i]="Socialization and Entertainment"
    elif "universtit" in category[i]:
        category[i]="Study Place"
    else :
        #print(name[i],nc)
        for j in range(len(nc)):
            if nc[j] in name[i]:
                ncategory[i]=cc[j]
                print(ncategory[i])
        if ncategory[i]==None and i!=0 :
            ncategory[i]="Socialization and Entertainment"

print(ncategory)