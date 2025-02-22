#new version

import os
from dotenv import load_dotenv
# from pymongo import MongoClient
import requests

# Load environment variables
load_dotenv()

import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'djangoproj')))

from settings import mongo_client, db_on_mongo

#load models
from .models import car_make_collection, car_model_collection, reviews_collection

# Connect to MongoDB


# Collections
# car_make_collection = db['car_make']
# car_model_collection = db['car_model']


backend_url = os.getenv('backend_url', default="http://localhost:3030/")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")


def get_car_makes():
    car_makes = car_make_collection.find()
    return [{"name": cm['name'], "description": cm['description']} for cm in car_makes]

def get_car_models():
    car_models = car_model_collection.aggregate([
        {
            "$lookup": {
                "from": "car_make",
                "localField": "car_make_name",
                "foreignField": "name",
                "as": "car_make_details"
            }
        },
        {
            "$unwind": "$car_make_details"
        }
    ])
    return [{"CarModel": cm['name'], "CarMake": cm['car_make_details']['name']} for cm in car_models]


# def analyze_review_sentiments(text):
#     request_url = sentiment_analyzer_url + "analyze/" + text
#     try:
#         response = requests.get(request_url)
#         return response.json()
#     except Exception as err:
#         print(f"Unexpected {err=}, {type(err)=}")
#         print("Network exception occurred")

def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + text
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")


def post_review(data_dict):
    print("post review data: ", data_dict)
    print("data_dict: ", data_dict)
    try:
        # Find or create CarMake
        car_make = car_make_collection.find_one({"name": data_dict['car_make']})
        if not car_make:
            car_make = {
                "name": data_dict['carMake'],
                "description": data_dict.get('description', '')
            }
            car_make_collection.insert_one(car_make)

        # Create and save a new CarModel document
        car_model = car_model_collection.find_one({"name": data_dict['car_model']})
        if not car_model:
            car_model = {
            "name": data_dict['carModel'],
            "car_make_name": car_make['name'],
            "type": data_dict['type'],
            "year": data_dict['year']
        }
            car_model_collection.insert_one(car_model)
        
        
        # Create review data dictionary
        review_data = { 
            "name": data_dict['name'],
            "dealership": data_dict['dealership'],
            "review": data_dict['review'],
            "purchase": data_dict['purchase'],
            "purchase_date": data_dict['purchase_date'],
            "car_make": car_make['name'],
            "car_model": car_model['name'],
            "car_year": car_model['year']
        }        

        # Save review to MongoDB
        reviews_collection.insert_one(review_data)
        
        print("Review saved successfully")

        return {"status": "success"}
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
        return {"status": "error", "message": str(err)}

def get_request(endpoint, **kwargs):
    print("GET request to endpoint: ", endpoint, " with params: ", kwargs)
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"

    request_url = backend_url + endpoint + "?" + params
    print("GET from {} ".format(request_url))
    try:
        print("request_url: ", request_url)
        response = requests.get(request_url)
        print("response fro get response: ", response)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
