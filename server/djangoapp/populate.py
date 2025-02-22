#     print("Data populated successfully")


# version using pymongo

# populate/populate.py
from settings import mongo_client, db_on_mongo
import sys
import os

# Collections

from .models import car_make_collection, car_model_collection, reviews_collection

# Add the settings folder to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'djangoproj')))


# car_make_collection = db_on_mongo['CarMake']
# car_model_collection = db_on_mongo['CarModel']


def initiate():
    car_make_data = [
        {"name": "NISSAN", "description": "Great cars. Japanese technology"},
        {"name": "Mercedes", "description": "Great cars. German technology"},
        {"name": "Audi", "description": "Great cars. German technology"},
        {"name": "Kia", "description": "Great cars. Korean technology"},
        {"name": "Toyota", "description": "Great cars. Japanese technology"},
    ]

    car_make_instances = []
    for data in car_make_data:
        if not car_make_collection.find_one({"name": data["name"]}):
            car_make_collection.insert_one(data)
        car_make_instances.append(data)  # Keep track of inserted documents

    # Create CarModel instances with the corresponding CarMake instances
    car_model_data = [
        {"name": "Pathfinder", "type": "SUV", "year": 2023,
            "car_make_name": car_make_instances[0]['name']},
        {"name": "Qashqai", "type": "SUV", "year": 2023,
            "car_make_name": car_make_instances[0]['name']},
        {"name": "XTRAIL", "type": "SUV", "year": 2023,
            "car_make_name": car_make_instances[0]['name']},
        {"name": "A-Class", "type": "SUV", "year": 2023,
            "car_make_name": car_make_instances[1]['name']},
        {"name": "C-Class", "type": "SUV", "year": 2023,
            "car_make_name": car_make_instances[1]['name']},
        {"name": "E-Class", "type": "SUV", "year": 2023,
            "car_make_name": car_make_instances[1]['name']},
        {"name": "A4", "type": "SUV", "year": 2023,
            "car_make_name": car_make_instances[2]['name']},
        {"name": "A5", "type": "SUV", "year": 2023,
            "car_make_name": car_make_instances[2]['name']},
        {"name": "A6", "type": "SUV", "year": 2023,
            "car_make_name": car_make_instances[2]['name']},
        {"name": "Sorrento", "type": "SUV", "year": 2023,
            "car_make_name": car_make_instances[3]['name']},
        {"name": "Carnival", "type": "SUV", "year": 2023,
            "car_make_name": car_make_instances[3]['name']},
        {"name": "Cerato", "type": "Sedan", "year": 2023,
            "car_make_name": car_make_instances[3]['name']},
        {"name": "Corolla", "type": "Sedan", "year": 2023,
            "car_make_name": car_make_instances[4]['name']},
        {"name": "Camry", "type": "Sedan", "year": 2023,
            "car_make_name": car_make_instances[4]['name']},
        {"name": "Kluger", "type": "SUV", "year": 2023,
            "car_make_name": car_make_instances[4]['name']},
        # Add more CarModel instances as needed
    ]

    for data in car_model_data:
        # Check if the document already exists
        if not car_model_collection.find_one({"name": data["name"], "year": data["year"], "type": data["type"], "car_make_name": data["car_make_name"]}):
            car_model_collection.insert_one(data)

    print("Data populated successfully")
    print(reviews_collection)
    reviews_collection.insert_one({
        "name": "name2",
        "id": "51",
        "dealership": "id2",
        "review": "review2",
        "purchase": "true2",
        "purchase_date": "date2",
        "car_make": "make_chosen2",
        "car_model": "model_chosen2",
        "car_year": "year2",
    })


# Run the initiate function to populate the data
initiate()
