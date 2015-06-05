# -*- coding: utf-8 -*-
from googleplaces import GooglePlaces, types, lang
# See https://github.com/slimkrazy/python-google-places
import csv

YOUR_API_KEY = ''

google_places = GooglePlaces(YOUR_API_KEY)

def geocode(name, province):
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



with open('artisanal-cheese.csv','rU') as csvinput:
    with open('output.csv', 'w') as csvoutput:
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
                    coord_dict = geocode(dairyname,province)
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




# def csv_writer(data, path):
#     with open(path, "wb") as csv_file:
#         writer = csv.writer(csv_file, delimiter=',')
#         for line in data:
#             writer.writerow(line)
#
#
# raw = open("canadianCheeseDirectory.csv", "rU")
# cooked = csv.reader(raw)
#
# data = []
#
# for row in cooked:
#     geoloc = geocode(row[0],row[1])
#     #geoloc = 0
#     data.append([row[0],row[1],geoloc])
#
# print data
#
# path = "out.csv"
# csv_writer(data,path)

