import logging
import os
import requests
from dotenv import load_dotenv
import asyncio
from aiohttp import ClientSession

load_dotenv()


# this url's were giving me an error
# where the container couldn't access localhost
# so well so I changed to the below option
# where they communicate through a docker
# network and it works fine

# backend_url = os.getenv(
#     'backend_url', default="http://localhost:3030")

# sentiment_analyzer_url = os.getenv(
#     'sentiment_analyzer_url',
#     default="http://localhost:5050/")


# This urls are to work with the version of the project
# where all services run in different containers within
# the same network
backend_url = os.getenv(
    'backend_url', default="http://api:3030")

sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://sentiment_analyzer:5000/")

# this is the async version for the get_request function
# I will migrate everything to async in the near future
# for now this is the only async functionality

async def get_request(endpoint, **kwargs):
    print("GET request to endpoint: ", endpoint, " with params: ", kwargs)
    params = ""
    if (kwargs):
        for key, value in kwargs.items():
            params = params+key+"="+value+"&"

    request_url = backend_url+endpoint+"?"+params

    print("GET from {} ".format(request_url))
    try:
        async with ClientSession() as session:
            async with session.get(request_url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Request failed with status: {response.status}")
    except ConnectionError as ce:
        print(f"Connection Error: {ce}")
        logging.error(f"Failed to connect to {request_url}: {ce}")
        return None
    except Exception as err:
        print(f"Unexpected error: {err}")
        logging.error(f"An unexpected error occurred: {err}")
        return None

# Example usage
async def main():
    dealerships = await get_request('/fetchdealers')
    if dealerships:
        print("Dealerships:", dealerships)
    else:
        print("Failed to retrieve dealerships")

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)

    asyncio.run(main())

# code for get requests to back end (synchronous)

# def get_request(endpoint, **kwargs):
#     print("GET request to endpoint: ", endpoint, " with params: ", kwargs)
#     params = ""
#     if (kwargs):
#         for key, value in kwargs.items():
#             params = params+key+"="+value+"&"

#     request_url = backend_url+endpoint+"?"+params

#     print("GET from {} ".format(request_url))
#     try:
#         # Call get method of requests library with URL and parameters
#         print('entered get_request try')
#         response = requests.get(request_url)
#         print('get_request response: ', response)
#         print('get_request response.json(): ', response.json())
#         return response.json()
#     except Exception as err:
#         print(f"Unexpected {err=}, {type(err)=}")
#         # If any error occurs
#         print("Network exception occurred")

# def get_request(endpoint, **kwargs):
#     print("GET request to endpoint: ", endpoint, " with params: ", kwargs)
#     params = ""
#     if (kwargs):
#         for key, value in kwargs.items():
#             params = params+key+"="+value+"&"

#     request_url = backend_url+endpoint+"?"+params
    
#     logging.info(f"GET from {request_url}")

#     print("(print)GET from {} ".format(request_url))
#     try:
#         # Call get method of requests library with URL and parameters
#         response = requests.get(request_url)
#         return response.json()
#     except ConnectionError as ce:
#         print(f"Connection Error: {ce}")
#         logging.error(f"Failed to connect to {request_url}: {ce}")
#         return None
#     except Exception as err:
#         print(f"Unexpected error: {err}")
#         logging.error(f"An unexpected error occurred: {err}")
#         return None


# Code for retrieving sentiments
def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url+"analyze/"+text
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")

# Add code for posting review


def post_review(data_dict):
    request_url = backend_url+"/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
