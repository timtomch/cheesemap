# -*- coding: utf-8 -*-
#
# cheesemap.py
# Maps Canadian artisanal cheese producers (csv from http://open.canada.ca/data/en/dataset/3c16cd48-3ac3-453f-8260-6f745181c83b)
# using the Google Places API or the YellowAPI (Yellow Pages).
# Hackathon-type project by Sara Alain (@archivalistic) and Thomas Guignard (@timtomch) for code4lib north 2015.
# 

from googleplaces import GooglePlaces, types, lang
# Library needed if using the Google Places API
# See https://github.com/slimkrazy/python-google-places

import requests
# The requests library lets us make easier RESTful API calls to the YellowAPI
# The json library lets us access the returned json data

import csv
# Library to read the input CSV file and output results as CSV

import sys
# This library lets us access arguments passed to this script, namely the file that needs to be processed.

import time
# To be able to sleep for 2 seconds between two YellowAPI calls, as per requirements.

# Google Places API stuff
GOOGLE_API_KEY = ''
google_places = GooglePlaces(GOOGLE_API_KEY)

def geocode_google(name, province):
    query = name + " " + province + " Canada"
    query_result = google_places.text_search(query)
    
    result_places = query_result.places
    #print result_places
    #print len(result_places)
    
    if len(result_places)>0:
        # Just get first result (we're feeling lucky)
        result = query_result.places[0]
        return result.geo_location
    else:
        return False
    #print result.geo_location
    #print result.place_id

# YellowAPI stuff
YELLOW_API_KEY = ''
yellow_base_url = 'http://api.sandbox.yellowapi.com/FindBusiness/?what={what}&where={where}' +\
                  '&pgLen=5&pg=1&dist=1&fmt=JSON&lang=en&UID=cheesemap&apikey={key}'


def geocode_yellow(name, province):
    # Replace placeholders in base url with actual values
    query = yellow_base_url.format(what=name,where=province,key=YELLOW_API_KEY)
    # Run the API call
    response = requests.get(query)
    # Decode the returned JSON data
    decoded = response.json()
    # Put longitude and latitude data into a dict matching the format returned by the Google API
    # (so that either API can be used in run_geocode below)
    geo_coords = {'lat': decoded['summary']['latitude'], 'lng': decoded['summary']['longitude']}
    # Delay for 2 seconds to comply with API developer requirements
    time.sleep(2)
    # Return the results
    return geo_coords

# Run through inputfile and geocode all entries
def run_geocode(inputfile,outputfile="output.csv"):
    with open(inputfile,'rU') as csvinput:
        with open(outputfile, 'w') as csvoutput:
            writer = csv.writer(csvoutput, lineterminator='\n')
            reader = csv.reader(csvinput)

            all = []
            row = next(reader)
            row.append('Lat')
            row.append('Lng')
            all.append(row)
            previousname = ""

            for row in reader:
            
                #Check if English name (4th row) is set, if not use French name (5th row)
                dairyname = row[3]
                if not dairyname:
                    dairyname = row[4]
            
                province = row[5]
                
                # Run the geocoder only once per dairy, to minimize API calls
                # If dairy name is the same as the previous one, reuse the coordinates    
                if previousname != dairyname:
                    previousname = dairyname
                    try:
                        coord_dict = geocode_yellow(dairyname,province)
                        #print coord_dict
                        if coord_dict:
                            coord_lat = coord_dict['lat']
                            coord_lng = coord_dict['lng']
                        else:
                            coord_lat = ""
                            coord_lng = ""
                    except:
                        coord_lat = ""
                        coord_lng = ""

                row.append(coord_lat)
                row.append(coord_lng)
            
                print dairyname
                print coord_lat, coord_lng
            
                all.append(row)

            writer.writerows(all)
      

if len(sys.argv) < 3:
    print "Please provide both input and output files."
    print "Usage: cheesemap.py <INPUTFILE.csv> <OUTPUTFILE.csv>"
else:
    run_geocode(sys.argv[1],sys.argv[2])

