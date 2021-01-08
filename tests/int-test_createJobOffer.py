from importlib import __import__
Mutation = __import__("helper").Mutation
helper = __import__("helper").GraphQLHelper

################################################## GET ARGUMENTS ##################################################

arguments = __import__("int-test-arguments").get("hashtags",
                                                 "highlights",
                                                 "jobTitle",
                                                 "jobType",
                                                 "location",
                                                 "mustHave",
                                                 "niceHave",
                                                 "payPerHour",
                                                 "payPerYear",
                                                 "trade")

# add description separately because description is used twice
arguments["description"] = __import__("int-test-arguments").get("jobOfferDescription")["jobOfferDescription"]


################################################## TEST USER ##################################################

# email and password used for test user
EMAIL = "email@test.de"
PASSWORD = "123"

# mutation to get token for test user
payload_token_auth = """
mutation{{
	tokenAuth(
		email:"{}",
		password: "{}"
		)
		{{
			token
		}}
}}""".format(EMAIL, PASSWORD)


def create_test_user():
	'''adds the test user to the database and adds userdata'''

	print("creating test user")
	helper.run_payload(helper, payload = """
	mutation {{
		createUser(
			email:"{}"
			isCompany:true
			password:"{}"
		){{
			user{{id}}
		}}
	}}
	""".format(EMAIL, PASSWORD))


def delete_test_user():
	'''deletes the test user from the database'''

	print("deleting test user")
	token = helper.request_token(helper, payload = payload_token_auth)
	header = helper.build_header(helper, token = token)
	helper.run_payload(helper, header=header, payload = """
	mutation {{
		deleteUser(
			password:"{}"
		){{
			ok
		}}
	}}
	""".format(PASSWORD))


################################################## MUTATION ##################################################

mutation = Mutation("createJobOffer",
                    {"description": True,
                     "hashtags": False,
                     "highlights": True,
                     "jobTitle": True,
                     "jobType": True,
                     "location": True,
                     "mustHave": True,
                     "niceHave": True,
                     "payPerHour": False,
                     "payPerYear": False,
                     "trade": True},
                    """{
					    jobOffer{
					      description
					      hashtags{
					        name
					      }
					      highlights
					      jobTitle
					      jobType
					      location
					      mustHave
					      niceHave
					      payPerHour
					      payPerYear
					      publicEmail
					      startDate
					      trade
					    }
					  }""")


################################################## TEST FUNCTIONS ##################################################

def all_valids():
	'''
	tests the mutation with all valid argument values
	fails if the any mutation fails
	'''

	print("testing all valid of createJobOffer")

	descriptions = arguments["description"]["valid"]
	hashtags = arguments["hashtags"]["valid"]
	highlights = arguments["highlights"]["valid"]
	jobTitle = arguments["jobTitle"]["valid"]
	jobType = arguments["description"]["valid"]
	location = arguments["description"]["valid"]
	mustHave = arguments["description"]["valid"]
	niceHave = arguments["description"]["valid"]
	payPerHour = arguments["description"]["valid"]
	payPerYear = arguments["description"]["valid"]
	publicEmail = arguments["description"]["valid"]