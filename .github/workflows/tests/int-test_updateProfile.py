from helper_functions import GraphQLHelper as helper
backend_tests = __import__('int-test_backend-api')
import pytest
import json


# email and password used for test user
EMAIL = "email@test.de"
PASSWORD = "123"

# mutation to get token for test user
payload_token_auth = """
mutation{{
    tokenAuth(
        email:"{e}",
        password: "{p}"
        )
        {{
            token
        }}
}}""".format(e=EMAIL, p=PASSWORD)

# adds the test user to the database and adds userdata
def create_test_user():
	print("creating test user")
	helper.run_payload(helper, payload = """
	mutation {{
	    createUser(
	        email:"{e}"
	        isCompany:false
	        password:"{p}"
	    ){{
	        user{{id}}
	    }}
	}}
	""".format(e=EMAIL, p=PASSWORD))
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

# deletes the test user from the database
def delete_test_user():
	print("deleting test user")
	token = helper.request_token(helper, payload = payload_token_auth)
	header = helper.build_header(helper, token = token)
	helper.run_payload(helper, header=header, payload = """
	mutation {{
	    deleteUser(
	        password:"{p}"
	    ){{
	        ok
	    }}
	}}
	""".format(p=PASSWORD))


# all arguments for the mutation updateProfile
# includes equivalence classes valid and invalid that are filled with edge values
arguments = {
		"birthDate": {
		    "valid":	["0001-01-01", "9999-12-31"],
		    "invalid":	["","0000-01-01", "0001-00-01", "0001-01-00", "10000-12-31", "9999-13-31", "9999-12-32"]
	    },

		"firstName": {
			"valid":	["a", "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ", "-", "'"],
			"invalid":	["", "*", "0", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"]
		},

		"gender": {
			"valid":	["m", "f", "d"],
			"invalid":	["", "z"]
		},

		"lastName": {
			"valid":	["", "a", "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ", "-", "'"],
			"invalid":	["*", "0", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"]
		},

		"phoneNumber": {
			"valid":	["000", "999999999999999"],
			"invalid":	["", "00", "9999999999999999"]
		},

		"shortBio": {
			"valid":	["a", "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ", "*"],
			"invalid":	["", "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ"]
		}
	}



# builds the mutation with a given dictionary
# the dictionary should contain all argument names of updateProfile as keys and argument values as values
# also returns the response that is expected if the mutation is valid
def build_mutation(value_dict):

	request = helper.build_empty_mutation(list(arguments)).format(value_dict["birthDate"],
                                                               value_dict["firstName"],
                                                               value_dict["gender"],
                                                               value_dict["lastName"],
                                                               value_dict["phoneNumber"],
                                                               value_dict["shortBio"])

	response = """
		{{
			"data": {{
				"updateProfile": {{
					"updatedProfile": {{
						"birthDate": "{}",
						"firstName": "{}",
						"gender": "{}",
						"lastName": "{}",
						"phoneNumber": "{}",
						"shortBio": "{}"
					}}
				}}
			}}
		}}
 	""".format(value_dict["birthDate"], value_dict["firstName"], value_dict["gender"], value_dict["lastName"], value_dict["phoneNumber"], value_dict["shortBio"])

	return (request, response)


# tests if all valid values of all arguments get the expected response
def test_valids():
    print("testing positives")

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
        mutation, expected_response = (build_mutation(
            {
				"birthDate":	valid_birthdates		[min(i, len(valid_birthdates)-1)],
				"firstName":	valid_firstnames	[min(i, len(valid_firstnames)-1)],
				"gender": 		valid_genders		[min(i, len(valid_genders)-1)],
				"lastName":		valid_lastnames		[min(i, len(valid_lastnames)-1)],
				"phoneNumber":	valid_phonenumbers	[min(i, len(valid_phonenumbers)-1)],
				"shortBio":		valid_shortbios		[min(i, len(valid_shortbios)-1)]
			}
        ))

        token = helper.request_token(helper, payload = payload_token_auth)
        header = helper.build_header(helper, token = token)
        actual_response = helper.run_payload(helper, payload = mutation, header = header).json()
        expected_response = json.loads(expected_response)
        # assert expected_response == actual_response.json()

        if expected_response != actual_response:
            print(mutation)
            print(expected_response)
            print(actual_response)


# tests if all invalid arguments cause errors
def test_all_invalids():
    print("testing all invalids")
    for a in list(arguments):
        test_invalid_cases_of(a)

# tests all invalid values of one argument
def test_invalid_cases_of(argument):

    cases = arguments[argument]["invalid"]

    test_values = {}

    valid_arguments = arguments.copy()
    valid_arguments.pop(argument, None)
    valid_arguments = list(valid_arguments)

    for a in valid_arguments:
        test_values[a] = arguments[a]["valid"][0]

    for invalid_argument in cases:
        test_values[argument] = invalid_argument
        mutation, _ = build_mutation(test_values)

        token = helper.request_token(helper, payload = payload_token_auth)
        header = helper.build_header(helper, token = token)
        actual_response = helper.run_payload(helper, payload = mutation, header = header).json()

        if list(actual_response)[0] != 'errors':
            print("mutation:\n" + str(mutation))
            print("response:\n" + str(list(actual_response)[0]))




# create_test_user()
# test_valids()
# test_all_invalids()
# delete_test_user()
print(helper.build_empty_mutation(list(arguments)))