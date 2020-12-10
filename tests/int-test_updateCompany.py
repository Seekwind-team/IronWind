from helper import GraphQLHelper as helper
from helper import Mutation



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
	token = helper.request_token(helper, payload = payload_token_auth)
	header = helper.build_header(helper, token = token)
	helper.run_payload(helper, header=header, payload= """
	mutation {{
			updateCompany(
				companyName: "{}",
				description: "{}",
				firstName: "{}",
				lastName: "{}",
				phoneNumber: "{}")
			{{
				updatedProfile {{
					companyName
					description
					firstName
					lastName
					phoneNumber
				}}
			}}
		}}
	""".format(arguments["companyName"]["valid"][0],
			   arguments["description"]["valid"][0],
			   arguments["firstName"]["valid"][0],
			   arguments["lastName"]["valid"][0],
			   arguments["phoneNumber"]["valid"][0]))


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

################################################## TEST CASE ARGUMENTS ##################################################

arguments = {
	"companyName": {
	# [a-Z] + special characters, length: 1-50
		"valid":	["a", "Z"*50, "*"],
		"invalid":	["", "Z"*51]
	},

	"description": {
	# [a-Z] + special characters, length: 1-2000
		"valid":	["a", "Z"*2000, "*"],
		"invalid":	["", "Z"*2001]
	},

	"firstName": {
	# [a-Z] + special chars - and ' length: 1-50
		"valid":	["a", "Z"*50, "-", "'"],
		"invalid":	["", "*", "0", "a"*51]
	},

	"lastName": {
	# same as firstName + can be empty
		"valid":	["", "a", "Z"*50, "-", "'"],
		"invalid":	["*", "0", "a"*51]
	},

	"phoneNumber": {
	# telephone number according to e.165-format
	# [0-9], length: 3-15
		"valid":	["000", "9"*15],
		"invalid":	["", "00", "9"*16]
	},
}

################################################## MUTATION ##################################################

mutation = Mutation("updateCompany",
					{"companyName": True,
					 "description": True,
					 "firstName": True,
					 "lastName": True,
					 "phoneNumber": True},
					"{updatedProfile{companyName description firstName lastName phoneNumber}}")

################################################## TEST FUNCTIONS ##################################################

# tests if all valid values of all arguments get the expected response
def test_valids():
	'''
	tests the mutation with all valid argument values
	fails if the any mutation fails
	'''

	print("testing all valids")

	valid_companyNames	= arguments["companyName"]["valid"]
	valid_firstnames	= arguments["firstName"]["valid"]
	valid_lastnames		= arguments["lastName"]["valid"]
	valid_phonenumbers	= arguments["phoneNumber"]["valid"]
	valid_descriptions	= arguments["description"]["valid"]

	maxlength = max(len(valid_companyNames),
		len(valid_firstnames),
		len(valid_lastnames),
		len(valid_phonenumbers),
		len(valid_descriptions))

	for i in range(maxlength):

		current_values = {"companyName":	valid_companyNames[min(i, len(valid_companyNames)-1)],
				  		 "firstName":	valid_firstnames[min(i, len(valid_firstnames)-1)],
				  		 "lastName":	valid_lastnames[min(i, len(valid_lastnames)-1)],
				  		 "phoneNumber":	valid_phonenumbers[min(i, len(valid_phonenumbers)-1)],
				  		 "description":	valid_descriptions[min(i, len(valid_descriptions)-1)]}

		filled_mutation = mutation.fill(current_values)

		token = helper.request_token(helper, payload = payload_token_auth)
		header = helper.build_header(helper, token = token)
		response = helper.run_payload(helper, payload = filled_mutation, header = header)

		if response.json() != None and list(response.json())[0] == 'data':
			response_values = response.json()["data"]["updateCompany"]["updatedProfile"]

			for arg_name in response_values:
				if current_values[arg_name] != response_values[arg_name]:
					log.test_failed(arg_name, current_values[arg_name], response_values[arg_name], filled_mutation)


def test_all_invalids():
	'''
	tests all invalid argument values
	fails if any mutations do not fail
	'''
	print("testing all invalids")
	for a in list(arguments):
		test_invalid_cases_of(a)

def test_invalid_cases_of(invalid_argument):
	'''
	tests all invalid values for one argument
	fails if any mutations do not fail
	'''

	print("testing invalids of " + invalid_argument)

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

		if response.json() != None and list(response.json())[0] != 'errors':
			log.expected_error(invalid_argument, invalid_value, filled_mutation)


def test(logger):
	'''
	creates a user and tests the mutation updateProfile on that user. deletes the user after
	'''
	global log
	log = logger

	log.start("updateCompany")
	create_test_user()
	test_valids()
	test_all_invalids()
	delete_test_user()

from helper import logger
test(logger)