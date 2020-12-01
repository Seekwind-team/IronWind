import pytest
## Create User
## Get Token
## Verify Token
## Create Joboffers
## Delete Joboffer
## Delete User

# upload jobs from file into database
import requests
import json
headers = {"Autorization": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InB5dGhvbkBib3QuZ2ciLCJleHAiOjE2MDY3MzkzMzAsIm9yaWdJYXQiOjE2MDY3MzkwMzB9.e5w9l3bjdyUgNG5W9DRreAde-uYPr5zMtz_REt1KwvM"}

# read file
with open('IronWind/recommenders/jobs.json', 'r') as file:
    data=file.read()

# parse file
jobs = json.loads(data)

def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('http://localhost:8000/', json={'query':me}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

        
# The GraphQL query (with a few aditional bits included) itself defined as a multi-line string.       
query = """
mutation{
  createJobOffer(
      jobType:"Vollzeit",
      description:"test autojob 1",
  )
  {ok}
}
"""
me = "{me{id}}"

#http://localhost:8000/#query=mutation%7B%0A%20%20createJobOffer(%0A%20%20%20%20%20%20jobType%3A%22Vollzeit%22%0A%20%20%20%20%20%20description%3A%22test%20autojob%201%22%0A%20%20)%20%7B%0A%20%20%20%20ok%0A%20%20%7D%0A%7DK
result = run_query(query) # Execute the query
print(result)