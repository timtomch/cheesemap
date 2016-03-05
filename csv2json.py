#Script to convert the csv output of cheesemap.py into a geoJSON file, for mapping.
#Inspired from http://www.andrewdyck.com/how-to-convert-csv-data-to-geojson/

import csv
import sys
import geojson


def csv2json(infile, outfile):

    # Read in raw data from csv
    rawData = csv.reader(open(infile, 'rb'))
    
    # Create empty list to contain all entries
    featureslist=[]

    # loop through the csv by row skipping the first
    iter = 0
    for row in rawData:
        iter += 1
        if iter >= 2:
            
            # only write out geolocated records
            if (len(row[30])>0 and len(row[31])>0):
            
                lat = float(row[31])
                lon = float(row[30])
            
                dairyname = row[3]
                if not dairyname:
                    dairyname = row[4]
            
                cheesename = row[1]
                if not cheesename:
                    cheesename = row[2]
            
                newfeature = geojson.Feature(geometry=geojson.Point((lat, lon)),properties={"dairy":dairyname, "cheese":cheesename})
                featureslist.append(newfeature)
                
    # Group all features into a collection
    collection = geojson.FeatureCollection(featureslist);
    
    # Export collection as geoJSON file
    with open(outfile, 'w') as jsonout:
         geojson.dump(collection, jsonout)


if len(sys.argv) < 3:
    print "Please provide both input and output files."
    print "Usage: csv2json.py <INPUTFILE.csv> <OUTPUTFILE.geojson>"
else:
    csv2json(sys.argv[1],sys.argv[2])