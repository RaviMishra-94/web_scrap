# pip3 install opencage
# then make an account on opencage and get an api key

from opencage.geocoder import OpenCageGeocode

key = '' # You can use your own key.
geocoder = OpenCageGeocode(key)

latitude = 44.8303087
longitude = -0.5761911

results = geocoder.reverse_geocode(latitude, longitude)

# Print information from the results
for result in results:
    print("Formatted Address:", result['formatted'])
    print("City:", result['components']['city'])
    print("Country:", result['components']['country'])
    print("Postcode:", result['components']['postcode'])
    print("---------")
