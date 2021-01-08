from importlib import __import__
Mutation = __import__("helper").Mutation
helper = __import__("helper").GraphQLHelper

################################################## GET ARGUMENTS ##################################################

passwords = __import__("int-test-arguments").get("password")["password"]

#to keep track of which password the user currently has, so that we can delete the user with that password
active_password = passwords["valid"][0]



################################################## MUTATION ##################################################

mutation = Mutation("changePassword",
					{"oldPassword": True,
					 "newPassword": True},
					"{ok}")


################################################## TEST USER ##################################################
# email and password used for test user
EMAIL = "email@test.de"

def exists(email, password):
	payload_token_auth = """
	mutation{{
		tokenAuth(
			email:"{}",
			password: "{}"
			)
			{{
				token
			}}
	}}""".format(EMAIL, password)

	try:
		helper.request_token(helper, payload = payload_token_auth)
		return True
	except:
		return False

def create_user(password):
	'''
	creates deletes a user with the given email and password
	'''
	if not exists(EMAIL, password):

		payload = """
		mutation {{
		    createUser(
		        email:"{}"
		        isCompany:false
		        password:"{}"
		    )
	     	{{
		        user{{id}}
		    }}
		}}
		""".format(EMAIL, password)
		helper.run_payload(helper, payload)


def delete_user(password):
	'''
	deletes a user with the given email and password
	'''
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
	}}""".format(EMAIL, password)

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


def all_valids():
	'''
	tests the mutation with all valid argument values
	fails if any mutation fails
	'''
	print("testing all valids of changePassword")

	global active_password

	valid_passwords = passwords["valid"][1:]

	for i in range(len(valid_passwords)):

		current_values = {"oldPassword":	active_password,
                          "newPassword":	valid_passwords[i]}

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
		}}""".format(EMAIL, active_password)

		token = helper.request_token(helper, payload = payload_token_auth)
		header = helper.build_header(helper, token = token)
		response = helper.run_payload(helper, payload = filled_mutation, header = header)

		if response.json() != None and list(response.json())[0] == 'data':
			response_value = response.json()["data"]["changePassword"]["ok"]
			if str(response_value).lower() != "true":
				log.test_failed("ok", "true", "false", filled_mutation)
			else:
				active_password = valid_passwords[i]
		assert list(response.json())[0] == 'data'
		assert str(response.json()["data"]["changePassword"]["ok"]).lower() == "true"


def all_invalids():
	'''
	tests all invalid argument values
	fails if any mutations do not fail
	'''
	print("testing all invalids of changePassword")

	invalid_passwords = passwords["invalid"]

	global active_password

	for inv_password in invalid_passwords:

		current_values = {"oldPassword":	active_password,
                          "newPassword":	inv_password}

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
		}}""".format(EMAIL, active_password)

		token = helper.request_token(helper, payload = payload_token_auth)
		header = helper.build_header(helper, token = token)
		response = helper.run_payload(helper, payload = filled_mutation, header = header)

		if response.json() != None and list(response.json())[0] != 'errors':
			log.expected_error("new_password", inv_password, filled_mutation)
			active_password = inv_password
		assert list(response.json())[0] == 'errors'





def test():

    global log
    log = __import__("testhub").logger
    log.start("changePassword")
    try:
	    create_user(passwords["valid"][0])
	    all_valids()
	    all_invalids()
    finally:
    	delete_user(active_password)