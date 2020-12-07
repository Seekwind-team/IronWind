from helper_functions import GraphQLHelper as helper
from helper_functions import Mutation


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

# adds the test user to the database and adds userdata
def create_test_user():
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

# deletes the test user from the database
def delete_test_user():
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


################################################## TEST CASE ARGUMENTS ##################################################
# all arguments for the mutation updateProfile
# includes equivalence classes valid and invalid that are filled with edge values
arguments = {
        "birthDate": {
            "valid":    ["0001-01-01", "9999-12-31"],
            "invalid":    ["","0000-01-01", "0001-00-01", "0001-01-00", "10000-12-31", "9999-13-31", "9999-12-32"]
        },

        "firstName": {
            "valid":    ["a", "Z"*50, "-", "'"],
            "invalid":    ["", "*", "0", "a"*51]
        },

        "gender": {
            "valid":    ["m", "f", "d"],
            "invalid":    ["", "z"]
        },

        "lastName": {
            "valid":    ["", "a", "Z"*50, "-", "'"],
            "invalid":    ["*", "0", "a"*51]
        },

        "phoneNumber": {
            "valid":    ["000", "9"*15],
            "invalid":    ["", "00", "9"*16]
        },

        "shortBio": {
            "valid":    ["a", "Z"*100, "*"],
            "invalid":    ["", "Z"*101]
        }
    }

################################################## MUTATION ##################################################

mutation = Mutation("updateProfile",
                    {"birthDate": True,
                     "firstName": True,
                     "gender": True,
                     "lastName": True,
                     "phoneNumber": True,
                     "shortBio": True},
                    "{updatedProfile{birthDate firstName gender lastName phoneNumber shortBio}}")



################################################## TEST FUNCTIONS ##################################################

# tests if all valid values of all arguments get the expected response
def test_valids():
    print("testing all valids")

    valid_birthdates    = arguments["birthDate"]["valid"]
    valid_firstnames    = arguments["firstName"]["valid"]
    valid_genders        = arguments["gender"]["valid"]
    valid_lastnames        = arguments["lastName"]["valid"]
    valid_phonenumbers    = arguments["phoneNumber"]["valid"]
    valid_shortbios        = arguments["shortBio"]["valid"]

    maxlength = max(len(valid_birthdates),
        len(valid_firstnames),
        len(valid_genders),
        len(valid_lastnames),
        len(valid_phonenumbers),
        len(valid_shortbios))

    for i in range(maxlength):
        filled_mutation = mutation.fill({"birthDate":	valid_birthdates[min(i, len(valid_birthdates)-1)],
                                  		 "firstName":	valid_firstnames[min(i, len(valid_firstnames)-1)],
                                  		 "gender":		valid_genders[min(i, len(valid_genders)-1)],
                                  		 "lastName":    valid_lastnames[min(i, len(valid_lastnames)-1)],
                                  		 "phoneNumber":	valid_phonenumbers[min(i, len(valid_phonenumbers)-1)],
                                  		 "shortBio":	valid_shortbios[min(i, len(valid_shortbios)-1)]})

        token = helper.request_token(helper, payload = payload_token_auth)
        header = helper.build_header(helper, token = token)
        response = helper.run_payload(helper, payload = filled_mutation, header = header).json()

        if list(response)[0] != 'data':
            print(filled_mutation)
            print(response)

        assert list(response)[0] == 'data'


# tests if all invalid arguments cause errors
def test_all_invalids():
    print("testing all invalids")
    for a in list(arguments):
        test_invalid_cases_of(a)

# tests all invalid values of one argument
def test_invalid_cases_of(invalid_argument):

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
        response = helper.run_payload(helper, payload = filled_mutation, header = header).json()

        if list(response)[0] != 'errors':
            print("mutation:\n" + str(filled_mutation))
            print("response:\n" + str(response))

        assert list(response)[0] == 'errors'


def test():
    create_test_user()
    test_valids()
    test_all_invalids()
    delete_test_user()

test()

# testhub.add_testcase(Testcase("updateProfile", test))
