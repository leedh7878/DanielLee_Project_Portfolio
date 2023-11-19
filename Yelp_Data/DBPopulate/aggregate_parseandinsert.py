#CptS 451 - Spring 2022
# https://www.psycopg.org/docs/usage.html#query-parameters
#  if psycopg2 is not installed, install it using pip installer :  pip install psycopg2  (or pip3 install psycopg2) 
import json
from datetime import datetime
import psycopg2
import collections.abc
from dotenv import load_dotenv

load_dotenv()

import os

password = os.getenv("password")


def cleanStr4SQL(s):
    return s.replace("'","`").replace("\n"," ")

def int2BoolStr (value):
    if value == 0:
        return 'False'
    else:
        return 'True'

def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.abc.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def insert2BusinessTable():
    #reading the JSON file
    with open('../yelp_CptS451_2022/yelp_business.JSON','r') as f:    #TODO: update path for the input file  //COMPLETE
        outfile =  open('./yelp_business_out.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.   //COMPLETE
        line = f.readline()
        count_line = 0
        #connect to yelpdb database on postgres server using psycopg2
        try:
            #TODO: update the database name, username, and password     //COMPLETE
            conn = psycopg2.connect("dbname='project_451' user='postgres' host='localhost' password='{}'".format(password))
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()


        while line:
            
            data = json.loads(line)

            # Generate the INSERT statement for the current business
            # TODO: The below INSERT statement is based on a simple (and incomplete) businesstable schema. Update the statement based on your own table schema and
            # include values for all businessTable attributes
            try:

                '''working'''
                cur.execute("INSERT INTO business (business_id, name, address, state, city, zipcode, latitude, longitude, stars, numCheckins, numTips, is_open)"
                       + " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                        (data['business_id'],cleanStr4SQL(data['name']), 
                        cleanStr4SQL(data["address"]), data["state"], data["city"], data["postal_code"], 
                        data["latitude"], data["longitude"], data["stars"], 0 , 0 , [False, True][data['is_open']] ) ) 

                '''working'''  
                attribute_dictionary = data["attributes"]
                flatten_attribute = flatten(attribute_dictionary)

                for x in flatten_attribute:
                    
                    cur.execute("INSERT INTO Attributes(business_id, attr_name, value) VALUES (%s, %s, %s)" ,(data['business_id'], x, flatten_attribute[x]) )

                '''working '''
                string_a = data["categories"]
                list_a = string_a.split(", ")
                
                for x in list_a:
                    cur.execute("INSERT INTO Categories(business_id, category_name)"
                            + "Values  (%s, %s)", (data['business_id'], x))
                
                '''working'''
                hours_dictionary = data["hours"]
                flatten_hours = flatten(hours_dictionary)

                for x in flatten_hours:
                    hours_day = flatten_hours[x].split("-")
                    
                    cur.execute("INSERT INTO Hours(dayofweek, open, close, business_id)"
                        + "Values  (%s, %s, %s, %s)", (x, hours_day[0], hours_day[1], data['business_id']))

                
            except Exception as e:
                print("Insert to businessTABLE failed!",e)

            conn.commit()

            line = f.readline()
            count_line +=1
        cur.close()
        conn.close()
    print(count_line)
    f.close()

def insert2CheckinTable():
    #reading the JSON file
    with open('../yelp_CptS451_2022/yelp_checkin.JSON','r') as f:    #TODO: update path for the input file
        #outfile =  open('./checkin_out.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0
        #connect to yelpdb database on postgres server using psycopg2
        try:
            #TODO: update the database name, username, and password
            conn = psycopg2.connect("dbname='project_451' user='postgres' host='localhost' password='{}'".format(password))
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()
        while line:
            data = json.loads(line)
            # Generate the INSERT statement for the current business checkin
            # TODO: The below INSERT statement is based on a simple (and incomplete) businesstable schema. Update the statement based on your own table schema and
            # include values for all businessTable attributes
            categories_list = data["date"]
            list_categories = categories_list.split(",")
            try:
                for x in list_categories:
                    cur.execute("INSERT INTO Checkins (business_id, cdate)"
                        + " VALUES (%s, %s)", 
                            (data['business_id'],  x))    
            except Exception as e:
                print("Insert to checkinTable failed!",e)
            conn.commit()

            line = f.readline()
            count_line +=1
        cur.close()
        conn.close()
    print(count_line)
    f.close()

def insert2TipTable():
    #reading the JSON file
    with open('../yelp_CptS451_2022/yelp_tip.JSON','r') as f:    #TODO: update path for the input file
        #outfile =  open('./yelp_tip_out.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        try:
            #TODO: update the database name, username, and password
            conn = psycopg2.connect("dbname='project_451' user='postgres' host='localhost' password='{}'".format(password))
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            
            # Generate the INSERT statement for the current tip
            # TODO: The below INSERT statement is based on a simple (and incomplete) tip table schema. Update the statement based on your own table schema and
            # include values for all tip Table attributes
            try:
                cur.execute("INSERT INTO tip (business_id, user_id, tipDate, likes, tipText)"
                       + " VALUES (%s, %s, %s, %s, %s)", 
                         (data['business_id'], data['user_id'], cleanStr4SQL(data["date"]), data["likes"], cleanStr4SQL(data["text"])   ))            
            except Exception as e:
                print("Insert to tipTABLE failed!",e)
            conn.commit()
            # optionally you might write the INSERT statement to a file.
            # sql_str = ("INSERT INTO businessTable (business_id, date, likes, text)"
            #           + " VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')").format(data['business_id'], data["date"], data["likes"], cleanStr4SQL(data["text"]))            
            # outfile.write(sql_str+'\n')

            line = f.readline()
            count_line +=1
    print(count_line)
    f.close()

def insert2UserTable():
    #reading the JSON file
    with open('../yelp_CptS451_2022/yelp_user.JSON','r') as f:    #TODO: update path for the input file
        #outfile =  open('./yelp_tip_out.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        try:
            #TODO: update the database name, username, and password
            conn = psycopg2.connect("dbname='project_451' user='postgres' host='localhost' password='{}'".format(password))
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            
            try:
                cur.execute("INSERT INTO Users (user_id, avg_stars, cool, funny, useful, yelping_since, name, fans, tipCount, totalLikes, user_latitude, user_longitude)"
                       + " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                         (data['user_id'], data["average_stars"], data["cool"], data["funny"], data["useful"], data["yelping_since"], data["name"], data["fans"], 0, 0, 0,0 ))    

           
            except Exception as e:
                print("Insert to userTABLE failed!",e)
            conn.commit()
            # optionally you might write the INSERT statement to a file.
            # sql_str = ("INSERT INTO businessTable (business_id, date, likes, text)"
            #           + " VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')").format(data['business_id'], data["date"], data["likes"], cleanStr4SQL(data["text"]))            
            # outfile.write(sql_str+'\n')

            line = f.readline()
            count_line +=1
    print(count_line)
    f.close()

def insert2FriendTable():
    #reading the JSON file
    with open('../yelp_CptS451_2022/yelp_user.JSON','r') as f:    #TODO: update path for the input file
        #outfile =  open('./yelp_tip_out.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        try:
            #TODO: update the database name, username, and password
            conn = psycopg2.connect("dbname='project_451' user='postgres' host='localhost' password='{}'".format(password))
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            
            try:
                for friend_x in data["friends"]:
                    
                    cur.execute("INSERT INTO friend (friend_id, user_id, avg_stars, cool, funny, useful, yelping_since, name, fans, tipCount, totalLikes, user_latitude, user_longitude)"
                       + " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                         (friend_x, data['user_id'], data["average_stars"], data["cool"], data["funny"], data["useful"], data["yelping_since"], data["name"], data["fans"], 0, 0, 0,0 ))
           
            except Exception as e:
                print("Insert to userTABLE failed!",e)
            conn.commit()

            line = f.readline()
            count_line +=1
    print(count_line)
    f.close()

if __name__ =="__main__":
    insert2BusinessTable()
    insert2UserTable()
    insert2FriendTable()
    insert2CheckinTable()
    insert2TipTable()

    # 29 minutes