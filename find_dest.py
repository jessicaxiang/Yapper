from random import randint
import rauth
import time
import yelp
import requests
import os
import estimates

def main_function(oneDollar, twoDollar, threeDollar, fourDollar, distanceHigh, friends):
    prices = []
    prices.append(oneDollar)
    prices.append(twoDollar)
    prices.append(threeDollar)
    prices.append(fourDollar)
    loc = estimates.get_location()
    return get_results(loc['lat'], loc['lng'], prices, distanceHigh, friends)

def get_results(start_lat,start_lng, price, rad, friends):
    #price is a boolean array

    new_price = []
    for i in range(1,5):
        if price[i-1]:
            new_price.append(i)

    new_price = ','.join([str(x) for x in new_price])

    resp = requests.post('https://api.yelp.com/oauth2/token',
                         data={'grant_type': 'client_credentials',
                               'client_id': 'T6V81F2O5GgfcANv12kRdA',
                               'client_secret': 'Gj0dTHO7d9wQh4OfQmHRgbGseQjRlOn17yZW6hZ2qKJtyZfxeNz3SkkuqhuSii4M'})

    yelp_access_token = resp.json()['access_token']

    yelp_search_url = ('https://api.yelp.com/v3/businesses/search?'
        'latitude=%s&longitude=%s&sort_by=rating&'
        'price=%s&open_now_filter=True&categories=%s&radius=%i&limit=%i')
    results = requests.get(
        yelp_search_url % (start_lat, start_lng, new_price, "food,restaurants", rad, 20),
        headers={ 'Authorization': 'Bearer %s' % yelp_access_token })

    results = results.json()['businesses']
    output = []
    for b in results:
        to_add = {}
        to_add['name'] = b['name']
        to_add['coordinates'] = b['coordinates']
        to_add['rating'] = b['rating']
        to_add['price'] = b['price']
        output.append(to_add)

    r = randint(0, len(output)-1)
    output = output[r]
    estimates.set_trip_info(friends, output['coordinates']['latitude'], output['coordinates']['longitude'])

    return output