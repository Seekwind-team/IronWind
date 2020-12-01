import pytest

import requests
import json

# Helper functions
def run_query(query, header=''): # A simple function to use requests.post to make the API call. Note the json= section.
    response = requests.post('http://localhost:8000', json={'query':query}, headers=header)
    return response


def build_header(token):
    return {'Authorization': 'JWT %s' %token}


## Create User
query_create_user = """
mutation {
    createUser(
        email:"api@test.xx"
        isCompany:true
        password:"123"
    ){
        user{id}
    }
}
"""

## Request token for created User #TODO save token 
query_token_auth = """
mutation{
    tokenAuth(
        email:"api@test.xx"
        password:"123"
    ){
        token
    }
}
"""

## Verify Token
def build_verify_token(token):
    query_verify_token = "mutation{verifyToken(token:%s){payload}}" %(token)
    return query_verify_token

## Create Joboffers #TODO save jobOffer id 
query_create_job_offer = """
mutation{
    createJobOffer(
        city:"Mannheim"
        description:"ein guter Job"
        highlights:"liste,aus,highlights"
            jobTitle:"generischer job"
            jobType:"Ausbildung"
        mustHave:"Führerschein"
        niceHave:"alle Sprachen"
            payPerHour:12
        publicEmail:"chef@gewerbe.mail"
            startDate:"1.1.2222"
        trade:"Gewerbe"
    ){
        jobOffer{id}
    }
}
"""

## Delete Joboffer
def build_delete_job_offer(job_offer_id):
    query_delete_job_offer = "mutation{deleteJobOffer(jobId: %s){ok}}" %(job_offer_id)


## Delete User
query_delete_user = """
mutation{
    deleteUser(
        password:"123"
    ){
        ok
    }
}
"""

headers = {}
token = ''

#ping
def test_ping():
    response = run_query("{ping}")
    #assert response.status_code == 200
    assert response.json() == {'data': {'ping': 'Pong'}}

def test_create_user():
    response = run_query(query_create_user)
    assert response.status_code == 200

def test_token_auth():
    response = run_query(query_token_auth)
    assert response.status_code == 200
    token_json = response.json()
    token = token_json.get('data').get('tokenAuth').get('token')
    print(token)

# TODO fix
def test_verify_token():
    token = run_query(query_token_auth).json().get('data').get('tokenAuth').get('token')
    query = build_verify_token(token)
    response = run_query(query)
    assert response.status_code == 200

def test_create_job_offer():
    pass

def test_delete_job_offer():
    pass

def test_delete_user():
    pass
