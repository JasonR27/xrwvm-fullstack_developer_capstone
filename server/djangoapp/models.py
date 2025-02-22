# new version
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'djangoproj')))

from settings import mongo_client, db_on_mongo

car_make_collection = db_on_mongo['CarMake']
car_model_collection = db_on_mongo['CarModel']
reviews_collection = db_on_mongo['reviews']

# Insert a CarMake document
def insert_car_make(name, description):
    car_make = {
        'name': name,
        'description': description
    }
    car_make_collection.insert_one(car_make)
    return car_make

# Insert a CarModel document
def insert_car_model(name, car_make_name, car_type, year):
    car_model = {
        'name': name,
        'car_make_name': car_make_name,
        'type': car_type,
        'year': year
    }
    car_model_collection.insert_one(car_model)
    return car_model


def insert_review(name, dealership, review, purchase, purchase_date, car_make, car_model, car_year):
    review = {
        'name': name,
        'dealership': dealership,
        'review': review,
        'purchase': purchase,
        'purchase_date': purchase_date,
        'car_make': car_make,
        'car_model': car_model,
        'car_year': car_year
    }
    reviews_collection.insert_one(review)
    return car_make