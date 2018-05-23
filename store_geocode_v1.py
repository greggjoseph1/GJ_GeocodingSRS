#!/usr/bin/python

print "****SCRIPT STARTING****"

# Bring in resources
import googlemaps, base64, ibm_db, smtplib

# Encode your password here and place the encoded results in the below lan_pass variable
# print 'This is my encoded password: '+base64.b64encode('XXXXXX')
lan_user = 't820560'
lan_pass = base64.b64decode('VTk5WnFldWQ=')

# prep the database insert with base64 encoded password.
sql_conn = ibm_db.connect('database=bcudb;hostname=10.231.250.32;port=50000;protocol=tcpip;uid=' + lan_user + ';pwd=' + lan_pass + ';', '', '')

sql_insert_q = 'insert into customer_analytics.gj_geocoded_srs (delivery_id,address,lat,lng) values(?,?,?,?)'
sql_insert_stmt = ibm_db.prepare(sql_conn, sql_insert_q)

def geocode(address):
    gmaps = googlemaps.Client(key='AIzaSyDA-IfaBH36LojL7Xwugxq0wcj1sLyfrf8')
    data = gmaps.geocode(address)
    result = {
      "lat": data[0]['geometry']['location']['lat'],
      "lng": data[0]['geometry']['location']['lng']
    }
    return result

print "****MAKING SQL SELECT QUERY****"

# CHANGE TO EXCLUDE ALREADY PROCESSED RECORDS IN THE SQL QUERY!!
sql_select_q = "select delivery_id,formatted_address from customer_analytics.gj_active_dealers where delivery_type = 'CONSUMER' and channel_l1 = 'Spark' and channel_l2 = 'Spark Retail Stores'"
sql_select_stmt = ibm_db.exec_immediate(sql_conn, sql_select_q)

dealer_dict = ibm_db.fetch_assoc(sql_select_stmt)
while dealer_dict != False:
    print "****NEW DEALER****"
    print "The delivery_id is : ", dealer_dict["DELIVERY_ID"]
    print "The formatted_address is : ", dealer_dict["FORMATTED_ADDRESS"]

    loc = geocode(dealer_dict["FORMATTED_ADDRESS"])

    print "The Lat is : ", loc['lat']
    print "The Lng is : ", loc['lng']

    ibm_db.bind_param(sql_insert_stmt, 1, dealer_dict["DELIVERY_ID"])
    ibm_db.bind_param(sql_insert_stmt, 2, dealer_dict["FORMATTED_ADDRESS"])
    ibm_db.bind_param(sql_insert_stmt, 3, loc['lat'])
    ibm_db.bind_param(sql_insert_stmt, 4, loc['lng'])
    ibm_db.execute(sql_insert_stmt)

    dealer_dict = ibm_db.fetch_assoc(sql_select_stmt)
    print "****LOOP FINISHED****"

# TODO
# Make SQL query to return the dealer_codes and addresses for stores
# Loop through the gmaps API to get lat/lng for changed/new addresses
# Insert results into DB2 table

ibm_db.close

print "****SQL CONNECTION CLOSED****"

