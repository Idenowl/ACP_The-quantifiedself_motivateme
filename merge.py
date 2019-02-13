import csv
import datetime
import os
import json
import sys, getopt
import subprocess

#####import and process rescue time
def import_rescue(date):
    '''
    Import rescue time data
    :param date: string year-month-day
    :return: header(list of string) of rescue time data, list rescue data time
    '''
    file_rescue='data/rescuetime/csv/'+date+'.csv'
    rescue_data_header=['Utilities','Entertainment','Communication & Scheduling','Social Networking','Reference & Learning','Software Development','News & Opinion','Shopping','Uncategorized','Design & Composition']
    rescue_data_time=[None]*len(rescue_data_header)
    if (os.path.isfile(file_rescue)) == True :
        with open(file_rescue) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row['Time Spent (seconds)']=int(row['Time Spent (seconds)'])/60 #put in minutes
                for i in range(len(rescue_data_header)):
                    if rescue_data_header[i]==row['Category']:
                        rescue_data_time[i]=int(row['Time Spent (seconds)'])/60

    else :
        print('Rescue time file not found for',date,file_rescue)

    return rescue_data_header,rescue_data_time


def import_rescueAlt(date):
    '''
    Alternative version with less category
    categories Software Development,Design & Composition and Reference & Learning are
    in a new category called Work and Learning
    News & Opinion and Shopping are in Entertainment
    :param date: text format year-month-day
    :return: list(string) :  header(rescue_data_header) for final file , list(string) data (rescue_data_time)
    '''
    file_rescue='data/rescuetime/csv/'+date+'.csv'
    rescue_data_header=['Work and learning(min)','Entertainment','Utilities','Communication & Scheduling','Social Networking','Uncategorized']
    rescue_data_time=[None]*len(rescue_data_header)
    save_work=0
    save_ent=0
    with open(file_rescue) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['Time Spent (seconds)']=int(row['Time Spent (seconds)'])/60 #put in minutes
            #print (row['Category'], row['Time Spent (seconds)'])
            if row['Category']=='Software Development' or row['Category']=='Design & Composition' or row['Category']=='Reference & Learning' :
                save_work+=row['Time Spent (seconds)']
            elif row['Category']=='News & Opinion' or row['Category']=='Shopping' or row['Category']=='Entertainment' :
                save_ent+=row['Time Spent (seconds)']
            else :
                for i in range(2,len(rescue_data_header)):
                    if rescue_data_header[i]==row['Category']:
                        rescue_data_time[i]=int(row['Time Spent (seconds)'])/60
        rescue_data_time[0]=save_work
        rescue_data_time[1]=save_ent
    return rescue_data_header,rescue_data_time

def import_sleep(date) :
    '''
    import sleep data
    :param date: string year-month-day
    :return:list of header of sleep data, list of data
    '''
    header=['From','To','Hours','DeepSleep']
    data=[None]*4
    date=date.split('-')
    new_date_format=date[2]+'. '+date[1]+'. '+date[0]
    test=False
    file_sleep = 'data/sleep/sleep.csv'
    with open(file_sleep) as csvfile :
        reader=csv.DictReader(csvfile)

        for row in reader :
            #check the date when the sleep finished
            if new_date_format in row['To']:
                data[0]=row['From']
                data[1]=row['To']
                data[2]=row['Hours']
                data[3]=row['DeepSleep']
                test= True
    if not test :
        print('Warning, sleep data if empty')
    return header,data

def import_emotion(date,participant) :
    '''
    :param date: string year-month-day
    :param participant: integer between 1 and 4
    :return: list of header (string) for emotion data, and list of data
    '''
    positive_score=0
    negative_score=0
    negative_list=['Upset','Hostile','Ashamed','Nervous','Afraid']
    positive_list=['Alert','Inspired','Determined','Attentive','Active']

    file_emotion='data/questionaires/emotion.csv'
    with open(file_emotion) as csvfile :
        reader=csv.DictReader(csvfile)
        fieldname=reader.fieldnames
        date = date.split('-')
        data=[None]*len(fieldname)
        if fieldname[0] == 'Horodateur' :
            # Format day-month-year
            new_date = date[2] + "/" + date[1] + "/" + date[0]
        else :
            # Format month-day-year
            new_date = date[1] + "/" + date[2] + "/" + date[0]
        for row in reader :
            #check the corresponding date
            if new_date in str(row[fieldname[0]]):
                #check the corresponding participant
                if int(row[fieldname[1]]) == int(participant):
                    for i in range(2,22):
                        #split the fieldname for processing
                        header_temp = fieldname[i].split('[')
                        header_temp = header_temp[1].split(']')
                        header_temp = header_temp[0]
                        #check the value for activities
                        if 'Event Happened During Day' in fieldname[i] :
                            #if the activity was selected value 1 else 0
                            if row[fieldname[i]]== 'Select' :
                                data[i]=1
                            else :
                                data[i]=0
                            fieldname[i] = header_temp  # make a better header for final file

                        #check the value for emotional state
                        if "Emotional State Survey" in fieldname[i]:
                            #Remove ? for processing
                            header_temp=header_temp.split('?')
                            header_temp=header_temp[0]
                            #check if the value correspond to a positive score or negative score
                            if header_temp in positive_list :
                                value_temp=row[fieldname[i]].split(' ') #split just keeping the numeric value, maximal value have the form "5 Always"
                                positive_score+=int(value_temp[0])
                            elif header_temp in negative_list :
                                value_temp = row[fieldname[i]].split(' ')
                                negative_score+=int(value_temp[0])
            else:
                for i in range (2,12):
                    header_temp = fieldname[i].split('[')
                    header_temp = header_temp[1].split(']')
                    header_temp = header_temp[0]
                    fieldname[i] = header_temp
                print('No emotion data for the date',date)

        ratio=positive_score-negative_score
        fieldname=fieldname[2:12]
        data=data[2:12]
        fieldname.append('Emotional score')
        data.append(ratio)

    return fieldname,data

def import_stress(date,participant) :
    '''

    :param date: string format year-month-day
    :param participant: integer between 1 and 4
    :return: string for header and integer for stress_score
    '''
    file_stress = 'data/questionaires/stress.csv'
    stress_score=None
    with open(file_stress) as csvfile :
        reader=csv.DictReader(csvfile)
        fieldname=reader.fieldnames
        date = date.split('-')
        if fieldname[0] == 'Horodateur':
            # Format day-month-year
            new_date = date[2] + '/' + date[1] + '/' + date[0]
        else:
            # Format month-day-year
            new_date = date[1] + '/' + date[2] + '/' + date[0]

        for row in reader:
            # check the corresponding date
            if new_date in row[fieldname[0]]:
                # check the corresponding participant
                if int(row[fieldname[1]]) == int(participant) :
                    stress_score = 0
                    for i in range (2,len(fieldname)) :
                        value_temp = row[fieldname[i]].split(' ')
                        value_temp=value_temp[0]
                        stress_score+=int(value_temp)
    if stress_score :
        return 'Stress_score', stress_score
    else:
        print('No value in stress_score for ',date)
        return 'Stress_score', None

def import_location(date) :
    '''
    :param date: string format : year-month-day
    :return: list(string) header, list(string) data
    '''
    file_location = 'data/timeline/csv/history-'+date+'.csv'
    work=0
    food=0
    home=0
    social=0
    shopping=0
    header = ['Studying and working', 'Food', 'Socialization and Entertainment', 'Shopping', 'Home']
    if (os.path.isfile(file_location))==True :
        with open(file_location) as csvfile :
            reader=csv.DictReader(csvfile)
            for row in reader :
                datetime_begin=datetime.datetime.strptime(row['begin'], "%Y-%m-%dT%H:%M:%S.%fZ")
                datetime_end = datetime.datetime.strptime(row['end'], "%Y-%m-%dT%H:%M:%S.%fZ")
                timespent=datetime_end-datetime_begin
                timespent=int(timespent.seconds)/3600

                #make category
                if row['category']==header[0]:
                    work+=timespent
                elif row['category']==header[1]:
                    food+=timespent
                elif row['category'] ==header[2]:
                    social+=timespent
                elif row['category'] ==header[3]:
                    shopping+=timespent
                elif row['category']==header[4]:
                    home+=timespent
    else:
        print('No kml file for', date)
    data=[]
    data.append(work)
    data.append(food)
    data.append(social)
    data.append(shopping)
    data.append(home)
    return header, data

def Writecsv(date,participant):
    '''
    Write the data in one csv file
    :param date: string year-month-day
    :param participant: integer between 1 and 4
    :return:
    '''
    rescue_header, rescue_data=import_rescue(date)
    sleep_header, sleep_data = import_sleep(date)
    emotion_header,emotion_data=import_emotion(date, participant)
    stress_header,stress_data=import_stress(date, participant)
    location_header,location_data=import_location(date)
    file_path='data/all.csv'

    header=[]
    header.append('date')
    header.append('participant')
    header.append(stress_header)
    header=header+sleep_header+emotion_header+location_header+rescue_header
    data=[]
    data.append(date)

    data.append(participant)

    data.append(stress_data)
    data=data+sleep_data+emotion_data+location_data+rescue_data

    if (os.path.isfile(file_path))==True:
        with open(file_path, 'a')as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(data)
        print('expand ', file_path)
    else :
        with open (file_path,'w')as csvfile:
            writer=csv.writer(csvfile, delimiter=',')
            writer.writerow(header)
            writer.writerow(data)
        print('Write new ', file_path)

    return 0
def listtodictionary (head,data) :
    dict={}
    for i in range(len(head)):
        head_temp=head[i]
        dict[head_temp]=data[i]
    return dict
def make_data_dict(date,participant):
    rescue_header, rescue_data = import_rescue(date)
    sleep_header, sleep_data = import_sleep(date)
    emotion_header, emotion_data = import_emotion(date, participant)
    stress_header, stress_data = import_stress(date, participant)
    location_header, location_data = import_location(date)
    # Join the lists
    header = []
    header.append('Date')
    header.append('UserID')
    header.append(stress_header)
    header = header + sleep_header + emotion_header + rescue_header + location_header
    data = []
    data.append(date)
    data.append(int(participant))
    data.append(stress_data)
    data = data + sleep_data + emotion_data + rescue_data + location_data
    dict = listtodictionary(header, data)
    return dict
def WriteJson_date(date,participant) :
    '''
    Write 1 Json file per date
    :param date: string year-month-day
    :param participant: integer between (1 and 4)
    :return:
    '''
    #Join the lists

    #make json file
    pathjson='data/json/'+participant+'_'+date+'.json'
    dict=make_data_dict(date,participant)

    with open(pathjson,'w',encoding='utf8') as jsonfile :
        json.dump(dict,jsonfile,indent=4)
    return 0
def Create_update_json_all(date,participant) :
    '''
    Create one Json file for all the data and update it if already exist
    :param date: string year-month-day
    :param participant: participant: integer between 1 and 4
    :return:
    '''
    dict={}
    key=participant+'_'+date
    dict[key]=make_data_dict(date,participant)

    path='data/all.json'
    if (os.path.isfile(path)) == False:
        with open(path, 'w') as jsonfile:
            json.dump(dict, jsonfile)
        print("json file created : ",path)
    if (os.path.isfile(path))==True :
        with open(path) as jsonfile:
            data = json.load(jsonfile)
            data.update(dict)
            #data[date]=dict
        with open(path, 'w') as jsonfile:
            json.dump(data, jsonfile,indent=4)
        print("update",path)
if __name__ == '__main__':
    '''
    if len(sys.argv) > 1 :
        print(sys.argv[1])
        date=str(sys.argv[1])
    if len(sys.argv) == 1 :
        date = '2019-02-09'
    '''
    argv=sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "hd:p:", ["idate=","ipart"])
    except getopt.GetoptError:
        print
        'test.py -d <year-month-day> -p <participant_number>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print
            'test.py -d <year-month-day> -p <participant_number>'
            sys.exit()
        elif opt in ("-d", "--idate"):
            date = arg
        elif opt in ("-p", "--ipart"):
            participant = arg
    print('Execution : ',date,'Participant',participant)
    date=str(date)

    rescuecommand='python extractrescuetime.py '+'-d '+date
    timelinecommand='python timelineprocess.py'
    extractsleep='python extractsleep.py'

    p1=subprocess.Popen(rescuecommand)
    p2=subprocess.Popen(timelinecommand)
    p3=subprocess.Popen(extractsleep)

    p1.wait()
    p2.wait()
    p3.wait()

    Writecsv(date, participant)
    WriteJson_date(date, participant)
    Create_update_json_all(date, participant)



