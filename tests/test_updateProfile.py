from importlib import __import__
Mutation = __import__("helper").Mutation
helper = __import__("helper").GraphQLHelper
import yaml

################################################## GET ARGUMENTS ##################################################

arguments = __import__("int-test-arguments").get("birthDate",
                                                 "firstName",
                                                 "gender",
                                                 "lastName",
                                                 "phoneNumber",
                                                 "shortBio",
                                                 "softSkills")

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


################################################## MUTATION ##################################################

mutation = Mutation("updateProfile",
					{"birthDate": True,
					 "firstName": True,
					 "gender": True,
					 "lastName": True,
					 "phoneNumber": True,
					 "shortBio": True,
      				 "softSkills": False},
					"""{
					    updatedProfile{
					      birthDate
					      firstName
					      gender
					      lastName
					      phoneNumber
					      shortBio
					      softSkills{
					        artistic
					        socialActivity
					        customerOrientated
					        motorskills
					        planning
					        creativity
					        innovativity
					        routine
					        communicativity
					      }
					    }
         			  }"""
					)



################################################## TEST FUNCTIONS ##################################################

# tests if all valid values of all arguments get the expected response
def all_valids():
	'''
	tests the mutation with all valid argument values
	fails if the any mutation fails
	'''


	print("testing all valids of updateProfile")

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

		response_values = response.json()["data"]["updateProfile"]["updatedProfile"]

		for arg_name in response_values:
			try:
				if arg_name == "softSkills":
					for skill in response_values["softSkills"]:
						softSkills = yaml.load(current_values["softSkills"])
						assert softSkills[skill] == response_values["softSkills"][skill]
				else:
					assert current_values[arg_name] == response_values[arg_name]
			except AssertionError as e:
				print("expected: " + arg_name + ": " + str(current_values[arg_name]))
				print("actual: " + arg_name + ": " + str(response_values[arg_name]))
				print(filled_mutation + "\n" + str(response.json()))
				raise e




def all_invalids():
	'''
	tests all invalid argument values
	fails if any mutations do not fail
	'''

	print("testing all invalids of updateProfile")
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
	creates a user and tests the mutation updateProfile on that user. deletes the user after
	'''

	create_test_user()
	try:
		all_valids()
		all_invalids()
	finally:
		delete_test_user()

test()