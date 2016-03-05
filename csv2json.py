#Script to convert the csv output of cheesemap.py into a geoJSON file, for mapping.
#Inspired from http://www.andrewdyck.com/how-to-convert-csv-data-to-geojson/

import csv
import sys


def csv2json(infile, outfile):

    # Read in raw data from csv
    rawData = csv.reader(open(infile, 'rb'))

    # the template. where data from the csv will be formatted to geojson
    template = \
        ''' \
        { "type" : "Feature",
            "geometry" : {
                    "type" : "Point",
                    "coordinates" : ["%s","%s"]},
            "properties" : { "dairy" : "%s", "cheese" : "%s"}
            },
        '''

    # the head of the geojson file
    output = \
        ''' \
    { "type" : "Feature Collection",
        {"features" : [
        '''

    # loop through the csv by row skipping the first
    iter = 0
    for row in rawData:
        iter += 1
        if iter >= 2:
            lat = row[30]
            lon = row[31]
            
            dairyname = row[3]
            if not dairyname:
                dairyname = row[4]
            
            cheesename = row[1]
            if not cheesename:
                cheesename = row[2]
            
            # only write out geolocated records
            if len(lat)>0:
                output += template % (lat,lon,dairyname,cheesename)
        
    # the tail of the geojson file
    output += \
        ''' \
        ]
    }
        '''
    
    # opens an geoJSON file to write the output to
    outFileHandle = open(outfile, "w")
    outFileHandle.write(output)
    outFileHandle.close()

if len(sys.argv) < 3:
    print "Please provide both input and output files."
    print "Usage: csv2json.py <INPUTFILE.csv> <OUTPUTFILE.geojson>"
else:
    csv2json(sys.argv[1],sys.argv[2])