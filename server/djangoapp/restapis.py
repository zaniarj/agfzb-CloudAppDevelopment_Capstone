import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, SentimentOptions


def get_request(url, **kwargs):
    print("GET from {} ".format(url))
    json_data={}
    try:
        if "apikey" in kwargs:
            response = requests.get(url, headers={'Content-Type':'application/json'}, params=kwargs, auth=HTTPBasicAuth("apikey", kwargs["apikey"]))
        else:
            response = requests.get(url, headers={'Content-Type':'application/json'}, params=kwargs)

        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        #print(json_data)
    except Exception as e:
        print("Error " ,e)
    
    return json_data
    

def post_request(url, json_payload, **kwargs):
    try:
        response  = requests.post(url,params = kwargs, json = json_payload)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
    except Exception as e:
        print("error",e)


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealerId):
    result = []
    payload = {"dealerId":dealerId}
    url = url + f"?dealerId={dealerId}"
    json_result = get_request(url)


    if json_result:
        review = json_result["review"]
        for rev in review:
            review_obj = DealerReview(car_make = rev['car_make'],car_model = rev['car_model'],
                        car_year = rev['car_year'],dealership = rev['dealership'],
                        name = rev['name'],purchase_date = rev['purchase_date'],review = rev['review']
                        ,purchase = rev['purchase'],id = rev['id'],sentiment = analyze_review_sentiments(rev['review']))
            result.append(review_obj)
    print("get_dealer_reviews_from_cf passed")
    return result


def get_dealers_by_state(url, state):
    result = []
    json_result = get_request(url,{"state":state})
    
    if json_result:
        for dealer_doc in json_result:
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            result.append(dealer_obj)
    
    return result


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text,**kwargs):
    params = dict()
    api_key = "2qDzVvpxG_Yhy33Sl9I6uBHedhtjlEJk0C3KI9ikydfP"
    url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/6832cd69-0f27-4e35-b5d3-b66990453d6d"
    authenticator = IAMAuthenticator(f'{api_key}')
    natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2022-04-07',
    authenticator=authenticator)

    natural_language_understanding.set_service_url(f'{url}')

    response = natural_language_understanding.analyze(text=text,features=Features(sentiment=SentimentOptions(document=True))).get_result()
    print("analyze_review_sentiments passed")
    response = response['sentiment']['document']['label']
    return json.dumps(response, indent=2)
    



