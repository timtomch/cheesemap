# cheesemap

This code maps artisanal cheeses extracted from the [Canadian Cheese Directory](http://open.canada.ca/data/en/dataset/3c16cd48-3ac3-453f-8260-6f745181c83b#comments)
open data. It was developed in collaboration with [Sara Alain](https://twitter.com/archivalistic) as a Hackfest project at
the [Code4Lib North meeting 2015](http://wiki.code4lib.org/North#Code4Lib_North:_the_Sixth._St._Catharines_Public_Library.2C_June_4_.26_5.2C_2015).

The result is [a geoJSON file](https://github.com/timtomch/cheesemap/blob/master/ca-artisanal-cheeses.geojson) with geolocated
cheese specialities and dairy farms.

## How does it work?

The CSV file downloaded from the Canadian Open Data portal is first filtered to only contain "artisanal" cheese specialities.
It is then run through [cheesemap.py](https://github.com/timtomch/cheesemap/blob/master/cheesemap.py), which uses the
YellowPages [Places API](http://www.yellowapi.com/docs/places/) to try and find the address of each dairy farm. Only the name
of the farm and the province code is available in the source file, so sadly only about 50% of entries can be thus mapped.
The result is another CSV file that contains extra columns for latitude and longitude. Since the free API only allows
300 queries per day, the same CSV file can be re-run through the script. Only rows where the lat and lon pair is missing will then
be queried. This allows the list to be gelolocated in batches.

      An earlier version of the script used the Google Places API instead, but this was found to be even less reliable.
      Note that an API key needs to be obtained from the YellowAPI service for the script to work.

The resulting CSV file is then run through [csv2json.py](https://github.com/timtomch/cheesemap/blob/master/csv2json.py) to be
turned into a geoJSON file, to be mapped by GitHub's built-in geoJSON engine.

## Issues
1. This is obviously just for fun and not very useful. The map does not display URLs, many producers fail to be mapped and are
thus not displayed. Also, we still haven't tasted all the cheese!
1. To check if the YellowPages API returned the right farm, a fuzzy text comparison ([using fuzzywuzzy](http://chairnerd.seatgeek.com/fuzzywuzzy-fuzzy-string-matching-in-python/))
is done between the name that was in the input data and the one returned by the API. This does not currently work very well,
especially with French names. So more entries fail to be mapped because of this.
1. I'm pretty sure at some point the latitude was substitued with the longitude and vice-versa. The result is fine, but don't
trust the variable names.
1. It would be nice not having to filter the input CSV file manually.
1. It would also be nice to embed this map in an actual website and start playing around with leaflet.js so that it looks nicer.

## Resources
* We found [this geoJSON validator tool](http://geojsonlint.com/) useful for debugging. 
