import pytest

import requests
import json
from helper import GraphQLHelper as helper

EMAIL = "api@test.xx"
PASSWORD = "123"

# Querys and Mutations
# Delete Joboffer
def build_delete_job_offer(job_offer_id):
    return "mutation{deleteJobOffer(jobId: %s){ok}}" %(job_offer_id)


## Verify Token
def build_verify_token(token):
    payload = """
    mutation{
        verifyToken(
            token: "JWT %s"
        ){
            payload
        }
    }""" %(token)
    return payload


# Create User
payload_create_user = """
mutation {
    createUser(
        email:"%s"
        isCompany:true
        password:"%s"
    ){
        user{id}
    }
}
""" %(EMAIL, PASSWORD)


# Request token for created User #TODO save token 
payload_token_auth = """
mutation{
    tokenAuth(
        email:"%s"
        password:"%s"
    ){
        token
    }
}
""" %(EMAIL, PASSWORD)


# Create Joboffers #TODO save jobOffer id 
payload_create_job_offer = """
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
            startDate:"2022-11-11"
        trade:"Gewerbe"
    ){
        jobOffer{id}
    }
}
"""


# Delete User
payload_delete_user = """
mutation{
    deleteUser(
        password:"%s"
    ){
        ok
    }
}
""" %(PASSWORD)

# job offer ids
payload_job_offers = """
{jobOffers{
    id
    }
}"""


#ping
def test_ping():
    response = helper.run_payload(helper, payload = "{ping}")
    assert response.status_code == 200
    assert response.json() == {'data': {'ping': 'Pong'}}

def test_create_user():
    response = helper.run_payload(helper, payload = payload_create_user)
    assert response.status_code == 200

def test_token_auth():
    response = helper.run_payload(helper, payload = payload_token_auth)
    assert response.status_code == 200

def test_verify_token():
    token = helper.request_token(helper, payload = payload_token_auth)
    payload = build_verify_token(token = token)
    response = helper.run_payload(helper, payload = payload)
    assert response.status_code == 200

def test_create_job_offer():
    token = helper.request_token(helper, payload = payload_token_auth)
    header = helper.build_header(helper, token = token)
    response = helper.run_payload(helper, payload = payload_create_job_offer, header = header)
    assert response.status_code == 200

def test_delete_job_offer():
    token = helper.request_token(helper, payload = payload_token_auth)
    header = helper.build_header(helper, token = token)
    job_id = helper.request_job_id(helper, payload = payload_job_offers, header = header)
    payload = build_delete_job_offer(job_offer_id = job_id)
    response = helper.run_payload(helper, payload = payload, header = header)
    assert response.status_code == 200

def test_delete_user():
    token = helper.request_token(helper, payload = payload_token_auth)
    header = helper.build_header(helper, token = token)
    response = helper.run_payload(helper, payload = payload_delete_user, header = header)
    assert response.status_code == 200
