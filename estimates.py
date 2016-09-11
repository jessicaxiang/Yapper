
import requests 
import requests.auth
import json
import find_dest

LYFT_CLIENT_ID = 'a83m8aY1GflS'
LYFT_CLIENT_SECRET = 'NqGnOBR6IybCJ5_wgopl2rYSXlaYroVU'

latitude = 37.7833
longitude = -122.4167

friends = 2
end_lat = 37.7833
end_lng = -122.4167

def get_access_token():

    client_auth = requests.auth.HTTPBasicAuth(LYFT_CLIENT_ID, LYFT_CLIENT_SECRET)
    post_data = {"Content-Type": "application/json",
                 "grant_type": "client_credentials",
                 "scope": "public"}

    response = requests.post("https://api.lyft.com/oauth/token",
                             auth=client_auth,
                             data=post_data)
    token_json = response.json()
    access_token = token_json["access_token"]
    
    return access_token

def get_ride_type():

    num_friends = friends

    if num_friends <= 1:
        ride_type = "Lyft Line"
    elif num_friends <= 3:
        ride_type = "Lyft"
    else:
        ride_type = "Lyft Plus"

    return ride_type

def get_duration():

    response = get_cost()

    cost_estimates = response.json()["cost_estimates"]
    duration = cost_estimates[0]["estimated_duration_seconds"]
    print(duration)
    duration_min = duration/60

    return duration_min

def get_distance():

    response = get_cost()

    cost_estimates = response.json()["cost_estimates"]
    distance = cost_estimates[0]["estimated_distance_miles"]

    return distance

def get_price_min():

    response = get_cost()

    cost_estimates = response.json()["cost_estimates"]
    price = cost_estimates[0]["estimated_cost_cents_min"]
    dollars = price/100

    return dollars

def get_price_max():

    response = get_cost()

    cost_estimates = response.json()["cost_estimates"]
    price = cost_estimates[0]["estimated_cost_cents_max"]
    dollars = price/100

    return dollars

def get_cost():

    access_token = get_access_token()

    ride = get_ride_type()

    if ride == "Lyft Line":
        ride_type = "lyft_line"
    elif ride == "Lyft":
        ride_type = "lyft"
    else:
        ride_type = "lyft_plus"

    print(latitude)
    print(longitude)
    print(end_lat)
    print(end_lng)
    headers = {"Authorization": "bearer " + access_token}
    url = "https://api.lyft.com/v1/cost?start_lat={sa}&start_lng={so}&end_lat={ea}&end_lng={eo}&ride_type={rt}".format(sa=latitude, so=longitude, ea=end_lat, eo=end_lng, rt=ride_type)
    print(url)
    response = requests.get(url, headers=headers)

    return response

def get_response():

    access_token = get_access_token()

    ride = get_ride_type()

    if ride == "Lyft Line":
        ride_type = "lyft_line"
    elif ride == "Lyft":
        ride_type = "lyft"
    else:
        ride_type = "lyft_plus"

    headers = {"Authorization": "bearer " + access_token}
    url = "https://api.lyft.com/v1/eta?lat={lat}&lng={lng}&ride_type={rt}".format(lat=latitude, lng=longitude, rt=ride_type)

    response = requests.get(url, headers=headers)

    return response

def set_trip_info(my_friends, my_end_lat, my_end_lng):

    global friends
    friends = my_friends
    global end_lat
    end_lat = my_end_lat
    global end_lng 
    end_lng = my_end_lng

def get_eta():

    response = get_response()

    eta_estimates = response.json()["eta_estimates"]
    eta = eta_estimates[0]["eta_seconds"]

    eta_min = eta/60
    
    return eta_min


def get_location():

    new_dict = {
        'lat': latitude,
        'lng': longitude,
    }

    return new_dict

def set_eta(mylat, mylng):

    global latitude
    latitude = mylat

    global longitude
    longitude = mylng

    print(latitude)
    print(longitude)