from importlib import __import__
Mutation = __import__("helper").Mutation
helper = __import__("helper").GraphQLHelper

################################################## GET ARGUMENTS ##################################################

arguments = __import__("int-test-arguments").get("message", "meta")

################################################## TEST USERS ##################################################

EMAIL_SENDER = "test@sender.de"
EMAIL_RECEIVER = "test@receiver.de"
PASSWORD = "123"

payload_token_auth = """
mutation{{
	tokenAuth(
		email:"{}",
		password: "{}"
		)
		{{
			token
		}}
}}""".format(EMAIL_SENDER, PASSWORD)

def create_test_users():
    '''adds the test users to the database'''

    print("creating test users")

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
	""".format(EMAIL_SENDER, PASSWORD))

    response = helper.run_payload(helper, payload = """
	mutation {{
		createUser(
			email:"{}"
			isCompany:false
			password:"{}"
		){{
			user{{id}}
		}}
	}}
	""".format(EMAIL_RECEIVER, PASSWORD))

    global RECEIVER_ID
    RECEIVER_ID = response.json()["data"]["createUser"]["user"]["id"]

def delete_test_users():
	'''deletes the test users from the database'''

	print("deleting test users")

	payload_token_auth = """
	mutation{{
		tokenAuth(
			email:"{}",
			password: "{}"
			)
			{{
				token
			}}
	}}""".format(EMAIL_SENDER, PASSWORD)

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

	payload_token_auth = """
	mutation{{
		tokenAuth(
			email:"{}",
			password: "{}"
			)
			{{
				token
			}}
	}}""".format(EMAIL_RECEIVER, PASSWORD)

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

mutation = Mutation("sendMessage",
                    {"message": 	True,
                     "meta":		True,
                     "receiverId":	False},
                    "{ok}")


################################################## TEST FUNCTIONS ##################################################

def all_valids():
	'''
	tests the mutation with all valid argument values
	fails if the any mutation fails
	'''

	print("testing all valid of sendMessage")

	valid_messages	= arguments["message"]["valid"]
	valid_meta		= arguments["meta"]["valid"]

	global RECEIVER_ID

	maxlength = max(len(valid_messages), len(valid_meta))

	for i in range(maxlength):

		current_values = {"message":	valid_messages[min(i, len(valid_messages)-1)],
                    	  "meta":		valid_meta[min(i, len(valid_meta)-1)],
                          "receiverId":	RECEIVER_ID}

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


		try:
			assert response.json()["data"]["sendMessage"]["ok"] == True
		except AssertionError as e:
			print(filled_mutation + "\n" + str(response.json()))
			raise e


def all_invalids():
	'''
	tests all invalid argument values
	fails if any mutations do not fail
	'''

	print("testing all invalids of sendMessage")
	for invalid_argument in list(arguments):
		invalid_cases_of(invalid_argument)


def invalid_cases_of(invalid_argument):
	'''
	tests all invalid values for one argument
	fails if any mutations do not fail
	'''

	print("testing invalids of " + invalid_argument)

	cases = arguments[invalid_argument]["invalid"]

	test_values = {}

	test_values["receiverId"] = RECEIVER_ID

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
	'''
	creates test users and tests the mutation sendMessage on those users. deletes the users after
	'''

	create_test_users()
	try:
		all_valids()
		all_invalids()
	finally:
		delete_test_users()