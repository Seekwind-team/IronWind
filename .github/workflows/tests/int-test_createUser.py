from helper_functions import GraphQLHelper as helper
from helper_functions import Mutation
# from testhub import Testcase, testhub
import pytest


################################################## TEST CASE ARGUMENTS ##################################################

arguments = {
	"email": {
		"valid":	["a@a.aa"],
        "invalid":	["", "@a.aa", "a@.aa", "a@a.a", "a@a.", "aa.aa", "Z"*101 + "@a.aa", "a@" + "Z"*101 + ".aa", "a@a." + "Z"*21]
	},
	"isCompany": {
		"valid":	["true", "false"],
		"invalid":	[""]
	},
	"password": {
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


# def test_





test_valids()