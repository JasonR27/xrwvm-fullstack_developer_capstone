# new only mongo version

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from .populate import initiate
import requests
# from .models import car_make_collection, car_model_collection
from .restapis import get_request, post_review, analyze_review_sentiments
from .models import car_make_collection, car_model_collection
from .models import car_make_collection, car_model_collection, reviews_collection

logger = logging.getLogger(__name__)

def health_check(request):
    return JsonResponse({'status': 'ok'})


def get_cars(request):
    count = car_make_collection.count_documents({})
    logger.info(f"car_make_collection count: {count}")
    if count == 0:
        initiate()
    
    car_models = car_model_collection.find()
    cars = []
    for car_model in car_models:
        car_make_name = car_model.get('car_make_name')
        if car_make_name:
            car_make = car_make_collection.find_one({"name": car_make_name})
            if car_make:
                cars.append({
                    "car_model_collection": car_model['name'], 
                    "car_make_collection": car_make['name']
                })
            else:
                logger.warning(f"No car_make found for car_make_name: {car_make_name}")
        else:
            logger.warning(f"car_make_name not found in car_model: {car_model['_id']}")
    
    logger.info(f"Cars views.py: {cars}")
    return JsonResponse({"car_model_collections": cars})


@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    response_data = {"userName": username}
    if user is not None:
        login(request, user)
        response_data["status"] = "Authenticated"
    return JsonResponse(response_data)

def logout_request(request):
    logout(request)
    response_data = {
        "userName": request.user.username if
        request.user.is_authenticated else ""}
    return JsonResponse(response_data)

@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    try:
        User.objects.get(username=username)
        response_data = {"userName": username, "error": "Already Registered"}
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password, email=email)
        login(request, user)
        response_data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(response_data)

def get_dealerships(request, state="All"):
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})

def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status": 200, "reviews": reviews})
    return JsonResponse({"status": 400, "message": "Bad Request"})

def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    return JsonResponse({"status": 400, "message": "Bad Request"}) 

# def add_review(request):
#     if not request.user.is_anonymous:
#         data = json.loads(request.body)
#         try:
#             print('add_review data', data)
#             reviews_collection.insert_one(data)
#             post_review(data)
#             return JsonResponse({"status": 200})
#         except Exception:
#             return JsonResponse({"status": 401,
#                                  "message": "Error in posting review"})
#     return JsonResponse({"status": 403,
#                          "message": "Unauthorized"})

def add_review(request):
    print('add_review request', request)
    if not request.user.is_anonymous:
        try:
            # Parse the request body
            data = json.loads(request.body)
            print('add_review data', data)

            # Define the URL of the /insertReview endpoint
            insert_review_url = "http://localhost:3030/insertReview"  # Replace with the actual URL

            # Get the CSRF token from the request cookies
            csrf_token = request.COOKIES.get('csrftoken')
            if not csrf_token:
                return JsonResponse(
                    {"status": 403, "message": "CSRF token missing"},
                    status=403
                )

            # Send a POST request to the /insertReview endpoint with the CSRF token
            response = requests.post(
                insert_review_url,
                json=data,  # Send the data as JSON
                headers={
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrf_token  # Include the CSRF token in the headers
                },
                # cookies={"csrftoken": csrf_token}  # Include the CSRF token in the cookies
            )

            # Check if the request was successful
            if response.status_code == 200:
                return JsonResponse({"status": 200})
            else:
                # If the request failed, return an error message
                return JsonResponse(
                    {"status": 401, "message": "Error in posting review"},
                    status=401
                )

        except Exception as e:
            print(f"Error in add_review: {e}")
            return JsonResponse(
                {"status": 401, "message": "Error in posting review"},
                status=401
            )

    # If the user is anonymous, return unauthorized
    return JsonResponse(
        {"status": 403, "message": "Unauthorized"},
        status=403
    )