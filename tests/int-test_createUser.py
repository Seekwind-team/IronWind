from importlib import __import__
Mutation = __import__("helper").Mutation
helper = __import__("helper").GraphQLHelper

################################################## GET ARGUMENTS ##################################################

arguments = __import__("int-test-arguments").get("email",
                                                 "isCompany",
                                                 "password")


################################################## MUTATION ##################################################

mutation = Mutation("createUser",
					{"email": True,
					 "isCompany": False,
					 "password": True},
					"{user{email isCompany}}")

################################################## HELPER FUNCTIONS ##################################################

def delete_user(email, password):
	'''
	deletes a user with the given email and password
	'''
	payload_token_auth = """mutation{{
								tokenAuth(
									email:"{}",
									password: "{}"
									)
									{{
										token
									}}
							}}""".format(email,
				 						 password)

	token = helper.request_token(helper, payload = payload_token_auth)
	header = helper.build_header(helper, token = token)
	payload = """
			mutation {{
				deleteUser(
					password:"{}"
				){{
					ok
				}}
			}}
			""".format(password)
	response = helper.run_payload(helper, header = header, payload = payload)

	if response.json() != None:
		if str(response.json()["data"]["deleteUser"]["ok"]).lower() != "true":
			log.test_failed("ok", "True", response.json()["data"]["deleteUser"]["ok"], payload)


################################################## TEST FUNCTIONS ##################################################


def test_valids():
	'''
	tests the mutation with all valid argument values
	fails if the any mutation fails
	'''
	print("testing all valids of createUser")

	valid_emails = arguments["email"]["valid"]
	valid_isCompanies = arguments["isCompany"]["valid"]
	valid_passwords = arguments["password"]["valid"]


	maxlength = max(len(valid_emails),
		len(valid_isCompanies),
		len(valid_passwords))

	for i in range(maxlength):

		current_values = {"email":		valid_emails[min(i, len(valid_emails)-1)],
				  		  "isCompany":	valid_isCompanies[min(i, len(valid_isCompanies)-1)],
				  		  "password":	valid_passwords[min(i, len(valid_passwords)-1)]}

		filled_mutation = mutation.fill(current_values)


		response = helper.run_payload(helper, payload = filled_mutation)

		if response.json() != None and list(response.json())[0] == 'data':
			delete_user(current_values["email"], current_values["password"])
			response_values = response.json()["data"]["createUser"]["user"]

			for arg_name in response_values:
				if str(current_values[arg_name]).lower() != str(response_values[arg_name]).lower():
					log.test_failed(arg_name, current_values[arg_name], response_values[arg_name], filled_mutation)





def test_all_invalids():
	'''
	tests all invalid argument values
	fails if any mutations do not fail
	'''
	print("testing all invalids of createUser")
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

		response = helper.run_payload(helper, payload = filled_mutation)

		if response.json() != None and list(response.json())[0] != 'errors':
			delete_user(test_values["email"], test_values["password"])
			log.expected_error(invalid_argument, invalid_value, filled_mutation)


def test(logger):
	global log
	log = logger

	log.start("createUser")
	test_valids()
	test_all_invalids()

# test(Logger())