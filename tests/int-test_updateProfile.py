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
			isCompany:false
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
			updateProfile(
				birthDate:"{}",
				firstName:"{}",
				gender:"{}",
				lastName:"{}",
				phoneNumber:"{}",
				shortBio:"{}"
			)
			{{
				updatedProfile{{
						birthDate,
						firstName,
						gender,
						lastName,
						phoneNumber,
						shortBio
				}}
			}}
		}}
	""".format(arguments["birthDate"]["valid"][0],
			   arguments["firstName"]["valid"][0],
			   arguments["gender"]["valid"][0],
			   arguments["lastName"]["valid"][0],
			   arguments["phoneNumber"]["valid"][0],
			   arguments["shortBio"]["valid"][0]))


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

# all arguments for the mutation updateProfile
# includes equivalence classes valid and invalid that are filled with edge values

arguments = {
	"birthDate": {
	# dates according to iso 8601
	# YYYY-MM-DD
	# Y: [0001-9999]
	# M: [01-12]
	# D: [01-31]
		"valid":	["0001-01-01", "9999-12-31"],
		"invalid":	["","0000-01-01", "0001-00-01", "0001-01-00", "10000-12-31", "9999-13-31", "9999-12-32"]
	},

	"firstName": {
	# [a-Z] + special chars - and ' length: 1-50
		"valid":	["a", "Z"*50, "-", "'"],
		"invalid":	["", "*", "0", "a"*51]
	},

	"gender": {
	# only male, female, diverse
		"valid":	["m", "f", "d"],
		"invalid":	["", "z"]
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

	"shortBio": {
	# [a-Z] + special characters, length: 1-100
		"valid":	["a", "Z"*100, "*"],
		"invalid":	["", "Z"*101]
	}
}

################################################## MUTATION ##################################################

mutation = Mutation("updateProfile",
					{"birthDate": True,
					 "firstName": True,
					 "gender": True,
					 "lastName": True,
					 "phoneNumber": True,
					 "shortBio": True},
					"{updatedProfile{birthDate firstName gender lastName phoneNumber shortBio}}")



################################################## TEST FUNCTIONS ##################################################

# tests if all valid values of all arguments get the expected response
def test_valids():
	'''
	tests the mutation with all valid argument values
	fails if the any mutation fails
	'''


	print("testing all valids")

	valid_birthdates	= arguments["birthDate"]["valid"]
	valid_firstnames	= arguments["firstName"]["valid"]
	valid_genders		= arguments["gender"]["valid"]
	valid_lastnames		= arguments["lastName"]["valid"]
	valid_phonenumbers	= arguments["phoneNumber"]["valid"]
	valid_shortbios		= arguments["shortBio"]["valid"]

	maxlength = max(len(valid_birthdates),
		len(valid_firstnames),
		len(valid_genders),
		len(valid_lastnames),
		len(valid_phonenumbers),
		len(valid_shortbios))

	for i in range(maxlength):

		current_values = {"birthDate":	valid_birthdates[min(i, len(valid_birthdates)-1)],
				  		 "firstName":	valid_firstnames[min(i, len(valid_firstnames)-1)],
				  		 "gender":		valid_genders[min(i, len(valid_genders)-1)],
				  		 "lastName":	valid_lastnames[min(i, len(valid_lastnames)-1)],
				  		 "phoneNumber":	valid_phonenumbers[min(i, len(valid_phonenumbers)-1)],
				  		 "shortBio":	valid_shortbios[min(i, len(valid_shortbios)-1)]}

		filled_mutation = mutation.fill(current_values)

		token = helper.request_token(helper, payload = payload_token_auth)
		header = helper.build_header(helper, token = token)
		response = helper.run_payload(helper, payload = filled_mutation, header = header)


		if response.json() != None and list(response.json())[0] == 'data':
			response_values = response.json()["data"]["updateProfile"]["updatedProfile"]

			for arg_name in response_values:
				if current_values[arg_name] != response_values[arg_name]:
					log.test_failed(arg_name, current_values[arg_name], response_values[arg_name], filled_mutation)




def test_all_invalids():
	'''
	tests all invalid argument values
	fails if any mutations do not fail
	'''

	print("testing all invalids")
	for invalid_argument in list(arguments):
		test_invalid_cases_of(invalid_argument)





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

	log.start("updateProfile")
	create_test_user()
	test_valids()
	test_all_invalids()
	delete_test_user()

# from helper import logger
# test(logger)
