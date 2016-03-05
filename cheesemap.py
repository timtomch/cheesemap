# -*- coding: utf-8 -*-
#
# cheesemap.py
# Maps Canadian artisanal cheese producers (csv from http://open.canada.ca/data/en/dataset/3c16cd48-3ac3-453f-8260-6f745181c83b)
# using the Google Places API or the YellowAPI (Yellow Pages).
# Hackathon-type project by Sara Allain (@archivalistic) and Thomas Guignard (@timtomch) for code4lib north 2015.
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

from fuzzywuzzy import fuzz
# Library to do fuzzy text comparison - used to check if results found are what we are looking for (sort of)

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
YELLOW_API_KEY    = ''
yellow_base_url   = 'http://api.sandbox.yellowapi.com/FindBusiness/?what={what}&where={where}' +\
                    '&pgLen=5&pg=1&dist=1&fmt=JSON&lang=en&UID=cheesemap&apikey={key}'


def geocode_yellow(name, province):
    # Replace placeholders in base url with actual values
    query = yellow_base_url.format(what=name,where=province,key=YELLOW_API_KEY)
    # Run the API call
    response = requests.get(query)
    # Decode the returned JSON data
    decoded = response.json()
    
    # Delay for 2 seconds to comply with API developer requirements
    time.sleep(2)
    
    for listing in decoded['listings']:
        # Check if the name of the listing matches the one searched
        print "Looking for '" + name + "', found '" + listing['name']
        match_score = fuzz.partial_ratio(listing['name'], name)
        print "Match score: " + str(match_score)
        if match_score > 80:
            # We feel confident enough that this is the right business
            # Still have to address this kind of situation:
            # Looking for 'Blancs d'Arcadie (Les)', found 'Les Blancs D'Arcadie
            # Match score: 75
            # Also deal with accents, which throw error
            # 'ascii' codec can't decode byte 0xc3 in position 33: ordinal not in range(128)
            # But we need to check that there are coordinates associated with it
            if listing['geoCode'] != None:
                # Put longitude and latitude data into a dict matching the format returned by the Google API
                # (so that either API can be used in run_geocode below)
                geo_coords = {'lat': listing['geoCode']['latitude'], 'lng': listing['geoCode']['longitude']}
                # Get out of the for loop and return the results
                return geo_coords
    
    # If nothing was found, we get out of the for loop and return nothing
    return False

# Run through inputfile and geocode all entries
def run_geocode(inputfile,outputfile="output.csv"):
    with open(inputfile,'rU') as csvinput:
        with open(outputfile, 'w') as csvoutput:
            writer = csv.writer(csvoutput, lineterminator='\n')
            reader = csv.reader(csvinput)
            #all will contain the output file
            all = []
            #Create header row from the input file
            row = next(reader)
            
            #If there's no Lat/Lon columns in the input file, append them
            if 'Lat' not in row:
                row.append('Lat')
                row.append('Lng')
                existinglatlng = False
            else:
                existinglatlng = True
            #Add header row to the output variable
            all.append(row)
            previousname = ""
            
            for row in reader:
                #Check if the Lat/Lon pair is already filled. If so, skip row.
                #This allows the same file to be run multiple times
                
                if not(existinglatlng and len(row[30])>0):
            
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
                        except Exception as e:
                            print e
                            coord_lat = ""
                            coord_lng = ""
                            
                    if existinglatlng:
                        row[30] = coord_lat
                        row[31] = coord_lng
                    else:
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

