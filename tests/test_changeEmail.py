from importlib import __import__
Mutation = __import__("helper").Mutation
helper = __import__("helper").GraphQLHelper

################################################## GET ARGUMENTS ##################################################

emails = __import__("int-test-arguments").get("email")["email"]

active_email = emails["valid"][0]


################################################## TEST USER ##################################################

PASSWORD = "123"

def create_test_user():
	'''adds the test user to the database'''

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
	""".format(active_email, PASSWORD))


def delete_test_user():
	'''deletes the test user from the database'''

	print("deleting test user")

	payload_token_auth = """
	mutation{{
		tokenAuth(
			email:"{}",
			password: "{}"
			)
			{{
				token
			}}
	}}""".format(active_email, PASSWORD)

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

mutation = Mutation("changeEmail",
					{"newEmail": True,
    				 "password": True},
					"{ok}")


################################################## TEST FUNCTIONS ##################################################

def all_valids():
	'''
	tests the mutation with all valid argument values
	fails if the any mutation fails
	'''

	print("testing all valids of changeEmail")

	global active_email

	valid_emails = emails["valid"]

	for i in range(len(valid_emails)):

		current_values = {"newEmail":	valid_emails[i],
                    	  "password":	PASSWORD}

		filled_mutation = mutation.fill(current_values)

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
		}}""".format(active_email, PASSWORD)

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
			assert response.json()["data"]["changeEmail"]["ok"] == True
		except AssertionError as e:
			print("expected: ok: " + str(current_values["ok"]))
			print("actual: ok: " + str(response.json()["data"]["changeEmail"]["ok"]))
			print(filled_mutation + "\n" + str(response.json()))
			raise e

		active_email = valid_emails[i]


def all_invalids():
	'''
	tests all invalid argument values
	fails if any mutations do not fail
	'''
	print("testing all invalids of changeEmail")

	global active_email

	invalid_emails = emails["invalid"]

	for inv_email in invalid_emails:

		current_values = {"newEmail":	inv_email,
                          "password":	PASSWORD}

		filled_mutation = mutation.fill(current_values)

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
		}}""".format(active_email, PASSWORD)

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
			print("because of newEmail: " + inv_email)
			active_email = inv_email
			raise e

def test():

	try:
		create_test_user()
		all_valids()
		all_invalids()
	finally:
		delete_test_user()
