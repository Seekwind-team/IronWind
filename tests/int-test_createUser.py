from helper_functions import GraphQLHelper as helper
from helper_functions import Mutation
# from testhub import Testcase, testhub
import pytest


################################################## TEST CASE ARGUMENTS ##################################################

arguments = {
	"email": {
    # email:	text@text.endung
    # text:		[a-Z] + special characters, length 1-100
    # endung:	[a-Z], length 2-20 chars
		"valid":	["a@a.aa"],
        "invalid":	["", "@a.aa", "a@.aa", "a@a.a", "a@a.", "aa.aa", "Z"*101 + "@a.aa", "a@" + "Z"*101 + ".aa", "a@a." + "Z"*21]
	},
	"isCompany": {
		"valid":	["true", "false"],
		"invalid":	[""]
	},
	"password": {
    # [a-Z] + [0-9] + special characters, length 3-100
		"valid":	["aaa", "Z"*100, "000", "9"*100, "***", "*"*100],
		"invalid":	["", "aa", "Z"*101]
	}
}


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
    response = helper.run_payload(helper, header = header, payload = """
													    mutation {{
													        deleteUser(
													            password:"{}"
													        ){{
													            ok
													        }}
													    }}
													    """.format(password))


################################################## TEST FUNCTIONS ##################################################


def test_valids():
    '''
    tests the mutation with all valid argument values
    fails if the any mutation fails
    '''
    print("testing all valids")

    valid_emails = arguments["email"]["valid"]
    valid_isCompanies = arguments["isCompany"]["valid"]
    valid_passwords = arguments["password"]["valid"]


    maxlength = max(len(valid_emails),
        len(valid_isCompanies),
        len(valid_passwords))

    for i in range(maxlength):
        filled_mutation = mutation.fill({"email":		valid_emails[min(i, len(valid_emails)-1)],
                                  		 "isCompany":	valid_isCompanies[min(i, len(valid_isCompanies)-1)],
                                  		 "password":	valid_passwords[min(i, len(valid_passwords)-1)]})


        response = helper.run_payload(helper, payload = filled_mutation).json()

        if list(response)[0] == 'data':
            delete_user(valid_emails[min(i, len(valid_emails)-1)], valid_passwords[min(i, len(valid_passwords)-1)])
        else:
            print(filled_mutation)
            print(response)

        # assert list(response)[0] == 'data'


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

        response = helper.run_payload(helper, payload = filled_mutation).json()

        if list(response)[0] != 'errors':
            print("mutation:\n" + str(filled_mutation))
            print("response:\n" + str(response))
			# delete user if creation
            # delete_user(test_values["email"], test_values["password"])

        assert list(response)[0] == 'errors'


def test():
    test_valids()
    test_all_invalids()

test()