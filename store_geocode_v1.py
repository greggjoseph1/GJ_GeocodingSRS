#!/usr/bin/python
# -*- coding: utf8 -*-

#Bring in resources
import googlemaps, base64, ibm_db, smtplib

#Encode your password here and place the encoded results in the below lan_pass variable
#print 'This is my encoded password: '+base64.b64encode('XXXXXX') 
lan_user = 't820560'
lan_pass = base64.b64decode('VTk5WnFldWQ=')

#prep the database insert with base64 encoded password.
sql_conn = ibm_db.connect('database=bcudb;hostname=10.231.250.32;port=50000;protocol=tcpip;uid='+ lan_user +';pwd='+ lan_pass +';', '', '')

sql_insert_q = 'insert into customer_analytics.gj_geocoded_srs (dealer_code,address,lat,lng) values(?,?,?,?)'
sql_insert_stmt = ibm_db.prepare(sql_conn, sql_insert_q)

def api_call_geocode(address):
    gmaps = googlemaps.Client(key='AIzaSyDA-IfaBH36LojL7Xwugxq0wcj1sLyfrf8')
    data = gmaps.geocode(address)
    result = data[0]['geometry']['location']
    return result

#CHANGE TO EXCLUDE ALREADY PROCESSED RECORDS IN THE SQL QUERY!!
sql_select_q = "select delivery_id,formatted_address from customer_analytics.gj_active_dealers where delivery_type = 'CONSUMER' and channel_l1 = 'Spark' and channel_l2 = 'Spark Retail Stores'"
sql_select_stmt = ibm_db.exec_immediate(sql_conn, sql_select_q)

dealers = list()

dealer_dict = ibm_db.fetch_both(sql_select_stmt)

while dealer_dict != False:
    print"****NEW DEALER****"
    dealers.append(dealer_dict[0])
    dealer_dict = ibm_db.fetch_both(sql_select_stmt)
    print "dealer_dict #0: " + dealer_dict[0]
    print "dealer_dict #1: " + dealer_dict[1]
    print "Lat: "+str(api_call_geocode(dealer_dict[1])['lat'])
    print "Lng: "+str(api_call_geocode(dealer_dict[1])['lng'])


print "****LOOP FINISHED****"

#TODO
#Make SQL query to return the dealer_codes and addresses for stores than need geocoding
##How will this identify records that need geocoding versus ones that have already been processed?
#Loop through the gmaps API to get lat/lng for changed/new addresses
#Insert results into DB2 table

api_call_geocode('187/189 STAFFORD STREET, TIMARU, TIMARU, 7910, NZ')





print 'Lat: '+str(api_call_geocode('187/189 STAFFORD STREET, TIMARU, TIMARU, 7910, NZ')['lat'])
print 'Lat: '+str(api_call_geocode('187/189 STAFFORD STREET, TIMARU, TIMARU, 7910, NZ')['lng'])

