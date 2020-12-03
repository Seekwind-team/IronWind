from helper_functions import GraphQLHelper as helper
backend_tests = __import__('int-test_backend-api')
import pytest
import json

EMAIL = "email@test.de"
PASSWORD = "123"

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


birthDateCases = {
    "valid":	["0001-01-01", "9999-12-31"],
    "invalid":	["","0000-01-01", "0001-00-01", "0001-01-00", "10000-12-31", "9999-13-31", "9999-12-32"]
            }

firstNameCases = {
	"valid":	["a", "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ", "-", "'"],
	"invalid":	["", "*", "0", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"]
}

genderCases = {
	"valid":	["m", "f", "d"],
	"invalid":	["", "z"]
}

lastNameCases = {
	"valid":	["", "a", "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ", "-", "'"],
	"invalid":	["*", "0", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"]
}

phoneNumberCases = {
	"valid":	["000", "999999999999999"],
	"invalid":	["", "00", "9999999999999999"]
}

shortBioCases = {
	"valid":	["a", "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ", "*"],
	"invalid":	["", "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ"]
}


def build_mutation_and_response(birthDate, firstName, gender, lastName, phoneNumber, shortBio):
	request = """
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
	""".format(birthDate, firstName, gender, lastName, phoneNumber, shortBio)

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
 	""".format(birthDate, firstName, gender, lastName, phoneNumber, shortBio)

	return (request, response)


def test_positives():
    print("testing positives")
    maxlength = max(len(birthDateCases["valid"]),
        len(firstNameCases["valid"]),
        len(genderCases["valid"]),
        len(lastNameCases["valid"]),
        len(phoneNumberCases["valid"]),
        len(shortBioCases["valid"]))

    for i in range(maxlength):
        mutation, expected_response = (build_mutation_and_response(
			birthDate=birthDateCases["valid"][min(i, len(birthDateCases["valid"])-1)],
			firstName=firstNameCases["valid"][min(i, len(firstNameCases["valid"])-1)],
			gender=genderCases["valid"][min(i, len(genderCases["valid"])-1)],
			lastName=lastNameCases["valid"][min(i, len(lastNameCases["valid"])-1)],
			phoneNumber=phoneNumberCases["valid"][min(i, len(phoneNumberCases["valid"])-1)],
			shortBio=shortBioCases["valid"][min(i, len(shortBioCases["valid"])-1)]
		))

        token = helper.request_token(helper, payload = payload_token_auth)
        header = helper.build_header(helper, token = token)
        actual_response = helper.run_payload(helper, payload = mutation, header = header).json()
        # assert expected_response == actual_response.json()
        expected_response = json.loads(expected_response)

        if expected_response != actual_response:
            print(mutation)
            print(expected_response)
            print(actual_response)


create_test_user()
test_positives()
delete_test_user()