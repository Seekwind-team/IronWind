from importlib import __import__
Mutation = __import__("helper").Mutation
helper = __import__("helper").GraphQLHelper

################################################## GET ARGUMENTS ##################################################

arguments = __import__("int-test-arguments").get("email",
                                                 "isCompany",
                                                 "password")

active_email = arguments["email"]["valid"][0]
active_password = arguments["password"]["valid"][0]


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
	helper.run_payload(helper, header = header, payload = payload)

def user_exists(email, password):
	payload_token_auth = """
	mutation{{
		tokenAuth(
			email:"{}",
			password: "{}"
			)
			{{
				token
			}}
	}}""".format(email, password)

	try:
		helper.request_token(helper, payload = payload_token_auth)
		return True
	except:
		return False


################################################## TEST FUNCTIONS ##################################################


def all_valids():
	'''
	tests the mutation with all valid argument values
	fails if the any mutation fails
	'''
	print("testing all valids of createUser")

	all_valids = {}

	for arg_name in list(arguments):
		all_valids[arg_name] = arguments[arg_name]["valid"]

	maxlength = 0
	for arg_name in all_valids:
		if len(all_valids[arg_name]) > maxlength:
			maxlength = len(all_valids[arg_name])

	for i in range(maxlength):

		current_values = {}

		for arg_name in list(all_valids):
			current_values[arg_name] = all_valids[arg_name][min(i, len(all_valids[arg_name])-1)]

		filled_mutation = mutation.fill(current_values)

		response = helper.run_payload(helper, payload = filled_mutation)

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

		global active_email
		global active_password

		active_email = current_values["email"]
		active_password = current_values["password"]

		response_values = response.json()["data"]["createUser"]["user"]

		for arg_name in response_values:
			try:
				if arg_name == "isCompany":
					assert current_values[arg_name] == str(response_values[arg_name]).lower()
				else:
					assert current_values[arg_name] == response_values[arg_name]
			except AssertionError as e:
				print("expected: " + arg_name + ": " + str(current_values[arg_name]))
				print("actual: " + arg_name + ": " + str(response_values[arg_name]))
				print(filled_mutation + "\n" + str(response.json()))
				raise e

		delete_user(active_email, active_password)


def all_invalids():
	'''
	tests all invalid argument values
	fails if any mutations do not fail
	'''
	print("testing all invalids of createUser")
	for a in list(arguments):
		invalid_cases_of(a)


def invalid_cases_of(invalid_argument):
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

		if  user_exists(test_values["email"], test_values["password"]):
			delete_user(test_values["email"], test_values["password"])

		response = helper.run_payload(helper, payload = filled_mutation)

		try:
			assert response.json() != None
		except AssertionError as e:
			print(filled_mutation + "\n response.json() == None")
			raise e

		try:
			assert "errors" in response.json()
		except AssertionError as e:
			global active_email
			global active_password
			active_email = test_values["email"]
			active_password = test_values["password"]
			print("expected error from sending:")
			print(filled_mutation + "\n" + str(response.json()))
			print("because of " + invalid_argument + ": " + str(invalid_value))
			raise e


def test():
	try:
		all_valids()
		all_invalids()
	finally:
		if user_exists(active_email, active_password):
			delete_user(active_email, active_password)