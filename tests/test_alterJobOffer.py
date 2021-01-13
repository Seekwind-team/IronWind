from importlib import __import__

from django.core.validators import DecimalValidator
Mutation = __import__("helper").Mutation
helper = __import__("helper").GraphQLHelper

################################################## GET ARGUMENTS ##################################################

arguments = __import__("int-test-arguments").get("city",
                                                 "highlights",
                                                 "isActive",
                                                 "jobTitle",
                                                 "jobType",
                                                 "location",
                                                 "mustHave",
                                                 "niceHave",
                                                 "payPerHour",
                                                 "payPerYear",
                                                 "publicEmail",
                                                 "startDate",
                                                 "trade")

# add description separately because description is used twice
arguments["description"] = __import__("int-test-arguments").get("jobOfferDescription")["jobOfferDescription"]

arguments["removeHashtags"] = {"valid": 	['["b", "'+"Y"*100+'", "9", "!"]', "[]"],
                               "invalid":	[]}
arguments["addHashtags"] = __import__("int-test-arguments").get("hashtags")["hashtags"]

JOB_ID = 0


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
	'''adds the test user to the database and adds userdata
 	   also creates a jobOffer to test alterJobOffer on
    '''

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

	print("creating test jobOffer")

	filled_mutation = __import__("test_createJobOffer").mutation.fill(
     								{"description":	"description",
                                  	 "hashtags":	'[]',
                                     "highlights":	"highlights",
                                     "jobTitle":	"jobTitle",
                                     "jobType":		"Vollzeit",
                                     "location":	"location",
                                     "city":		"city",
                                     "mustHave":	"mustHave",
                                     "niceHave":	"niceHave",
                                     "payPerHour":	0,
                                     "payPerYear":	"[\"payPerYear\"]",
                                     "publicEmail":	"email@public.de",
                                     "startDate":	"0001-01-01",
                                     "trade":		"trade"})


	token = helper.request_token(helper, payload = payload_token_auth)
	header = helper.build_header(helper, token = token)
	response = helper.run_payload(helper, payload = filled_mutation, header = header)
	global JOB_ID
	JOB_ID = response.json()["data"]["createJobOffer"]["jobOffer"]["id"]



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

mutation = Mutation("alterJobOffer",
                    {"addHashtags": False,
                     "city": True,
                     "description": True,
                     "highlights": True,
                     "isActive": False,
                     "jobId": False,
                     "jobTitle": True,
                     "jobType": True,
                     "location": True,
                     "mustHave": True,
                     "niceHave": True,
                     "payPerHour": False,
                     "payPerYear": False,
                     "publicEmail": True,
                     "removeHashtags": False,
                     "startDate": True,
                     "trade": True},
                    "{jobOffer{city description highlights jobTitle jobType location mustHave niceHave payPerHour payPerYear publicEmail startDate trade}}")


################################################## TEST FUNCTIONS ##################################################

# def all_valids():
# 	'''
# 	tests the mutation with all valid argument values
# 	fails if the any mutation fails
# 	'''

# 	print("testing all valids of alterJobOffer")

# 	addHashtags = arguments["addHashtags"]["valid"]
# 	city = arguments["city"]["valid"]
# 	descriptions = arguments["description"]["valid"]
# 	highlights = arguments["highlights"]["valid"]
# 	isActive = arguments["isActive"]["valid"]
# 	jobTitle = arguments["jobTitle"]["valid"]
# 	jobType = arguments["jobType"]["valid"]
# 	location = arguments["location"]["valid"]
# 	mustHave = arguments["mustHave"]["valid"]
# 	niceHave = arguments["niceHave"]["valid"]
# 	payPerHour = arguments["payPerHour"]["valid"]
# 	payPerYear = arguments["payPerYear"]["valid"]
# 	publicEmail = arguments["publicEmail"]["valid"]
# 	removeHashtags = arguments["removeHashtags"]["valid"]
# 	startDate = arguments["startDate"]["valid"]
# 	trade = arguments["trade"]["valid"]


# 	maxlength = max(len(descriptions),
#                   	len(highlights),
#                    	len(jobTitle),
#                     len(jobType),
#                     len(location),
#                     len(mustHave),
#                     len(niceHave),
#                     len(payPerHour),
#                     len(payPerYear),
#                     len(publicEmail))

# 	for i in range(maxlength):

# 		current_values = {	"description": 	descriptions[min(i, len(descriptions)-1)],
# 		                     "highlights": 	highlights[min(i, len(highlights)-1)],
# 		                     "jobTitle": 	jobTitle[min(i, len(jobTitle)-1)],
# 		                     "jobType": 	jobType[min(i, len(jobType)-1)],
# 		                     "location": 	location[min(i, len(location)-1)],
# 		                     "mustHave": 	mustHave[min(i, len(mustHave)-1)],
# 		                     "niceHave": 	niceHave[min(i, len(niceHave)-1)],
# 		                     "payPerHour": 	payPerHour[min(i, len(payPerHour)-1)],
# 		                     "payPerYear": 	payPerYear[min(i, len(payPerYear)-1)],
# 		                     "trade": 		trade[min(i, len(trade)-1)]}

# 		filled_mutation = mutation.fill(current_values)

# 		token = helper.request_token(helper, payload = payload_token_auth)
# 		header = helper.build_header(helper, token = token)
# 		response = helper.run_payload(helper, payload = filled_mutation, header = header)

# 		if response.json() != None and list(response.json())[0] == 'data':
# 			response_values = response.json()["data"]["createJobOffer"]["jobOffer"]

# 			for arg_name in response_values:
# 				if arg_name == "hashtags":
# 					for tag in response_values["hashtags"]:
# 						if not tag["name"] in current_values["hashtags"]:
# 							log.test_failed("hashtags", current_values["hashtags"], tag["name"])
# 						assert tag["name"] in current_values["hashtags"]
# 				else:
# 					if current_values[arg_name] != response_values[arg_name]:
# 						log.test_failed(arg_name, current_values[arg_name], response_values[arg_name], filled_mutation)
# 					assert current_values[arg_name] == response_values[arg_name]
# 		assert list(response.json())[0] == 'data'


def all_valids():

	print("testing all valids of alterJobOffer")

	all_valids = {}

	for arg_name in list(arguments):
		all_valids[arg_name] = arguments[arg_name]["valid"]

	maxlength = 0
	for arg_name in all_valids:
		if len(all_valids[arg_name]) > maxlength:
			maxlength = len(all_valids[arg_name])

	for i in range(maxlength):

		current_values = {}

		current_values["jobId"] = JOB_ID

		for arg_name in list(all_valids):
			current_values[arg_name] = all_valids[arg_name][min(i, len(all_valids[arg_name])-1)]

		filled_mutation = mutation.fill(current_values)

		token = helper.request_token(helper, payload = payload_token_auth)
		header = helper.build_header(helper, token = token)
		response = helper.run_payload(helper, payload = filled_mutation, header = header)

		try:
			assert response.json() != None
		except AssertionError as e:
			print(filled_mutation + "\n response.json() == None")
			raise e

		try:
			assert "errors" not in response.json()
		except AssertionError as e:
			print(filled_mutation + "\n" + str(response.json()))
			raise e

		response_values = response.json()["data"]["alterJobOffer"]["jobOffer"]

		for arg_name in response_values:
			try:
				if arg_name == "hashtags":
					for tag in response_values["hashtags"]:
						assert tag["name"] in current_values["addHashtags"]
						assert tag["name"] not in current_values["removeHashtags"]
				elif arg_name == "payPerYear":
					assert current_values[arg_name].replace('"', "'") == response_values[arg_name]
				elif arg_name == "id":
					pass
				else:
					assert current_values[arg_name] == response_values[arg_name]
			except AssertionError as e:
				print("expected: " + arg_name + ": " + str(current_values[arg_name]))
				print("actual: " + arg_name + ": " + str(response_values[arg_name]))
				print(filled_mutation + "\n" + str(response.json()))
				raise e

def all_invalids():
	print("testing all invalids of alterJobOffer")
	for invalid_argument in list(arguments):
		invalid_cases_of(invalid_argument)


def invalid_cases_of(invalid_argument):
	print("testing invalids of "+ invalid_argument)

	cases = arguments[invalid_argument]["invalid"]

	test_values = {}

	valid_arguments = arguments.copy()
	valid_arguments.pop(invalid_argument)
	valid_arguments = list(valid_arguments)

	for a in valid_arguments:
		test_values[a] = arguments[a]["valid"][0]

	for invalid_value in cases:
		test_values[invalid_argument] = invalid_value
		filled_mutation = mutation.fill(test_values)

		token = helper.request_token(helper, payload = payload_token_auth)
		header = helper.build_header(helper, token = token)
		response = helper.run_payload(helper, payload = filled_mutation, header = header)

		try:
			assert response.json() != None
		except AssertionError as e:
			print(filled_mutation + "\n response.json() == None")
			raise e

		try:
			assert "errors" in response.json()
		except AssertionError as e:
			print("expected error from sending:")
			print(filled_mutation + "\n" + str(response.json()))
			print("because of " + invalid_argument + ": " + str(invalid_value))
			raise e


def test():
	create_test_user()
	try:
		all_valids()
		all_invalids()
	finally:
		delete_test_user()