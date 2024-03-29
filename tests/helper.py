import requests
from datetime import datetime
import os

class GraphQLHelper:
    # runs Query or Mutation and returns response object
    # payload: Query or Mutation in String format   eg. payoad = "{me{id}}""
    # header: request headers in JSON format        eg. haeder = {'Autorization':'JWT insert_token'}
    # host: string containing the Hostadress. Default is localhost
    # port: Port to call. Default is 8000
    def run_payload(self, payload, header='', host='http://localhost', port='8000'):
        addr = "{}:{}".format(host, port)
        response = requests.post(addr, {'query': payload}, headers=header)
        return response

    # builds valid header from jwt token
    # token: valid User Token, should've been requested from IronWind
    def build_header(self, token):
        return {'Authorization': 'JWT %s' %token}

    # requests and returns token
    # payload: tokenAuth mutation
    def request_token(self, payload):
        response = self.run_payload(self, payload = payload)
        try:
            return response.json()['data']['tokenAuth']['token']
        except:
            exc = "Recieved no token.\nPayload: {}\nResponse: {}".format(payload, response.json())
            raise Exception(exc)

    # requests ids for all job offers belonging to user token and returns first id
    # payload: jobOffers query
    # header: Autorization header
    def request_job_id(self, payload, header):
        response = self.run_payload(self, payload = payload, header = header)
        if response.status_code == 200:
            return response.json()['data']['jobOffers'][0]['id']

class Query:

    def __init__(self, name: str, arguments: dict):
        '''
        parameters:
			name:		the name of query
			arguments:	the names of all the arguments the query takes as keys
						a boolean as the values of the dict to tell if an argument's value needs quotation-marks "" or not
        '''
        self.name = name
        self.arguments = arguments

    def fill(self, values: dict = {}) -> str:
        '''
        fills the query with the given values

        parameters
			values (dict):	a dict of argument-value pairs
							e.g. "last_name": "Trump"

		returns
			query (str):	the query with all given values filled in
        '''
        query = "{" + self.name
        if self.arguments:
            query += "{"

            for arg in self.arguments:
                query += arg + ":\"" + values[arg] + "\","

            query += "}"
        query += "}"

        return query


class Mutation(Query):

    response_query = None

    def __init__(self, name: str, arguments: dict, response_query: str):
        '''
        parameters:
			name:			the name of query
			arguments:		the names of all the arguments the query takes
			response_query:	the query after the mutation to check the changed data
        '''
        super().__init__(name, arguments)
        self.response_query = response_query

    def fill(self, values: dict) -> str:
        '''
        fills the mutation with the given values

        parameters
			values (dict):	a dict of argument-value pairs
							e.g. "last_name": "Trump"

		returns
			mutation (str):	the mutation with all given values filled in
        '''
        mutation = "mutation"

        mutation += "{" + self.name

        if self.arguments:
            mutation += "("

            for arg in self.arguments:
                if self.arguments[arg]:
                    mutation += arg + ":\"" + str(values[arg]) + "\","
                else:
                    mutation += arg + ":" + str(values[arg]) + ","

            mutation += ")"

        mutation += self.response_query

        mutation += "}"

        return mutation


# class Logger:

#     def __init__(self, filename: str = None):
#         if filename == None:
#             self.filename = os.path.dirname(os.path.abspath(__file__)) + "\\logs\\testlog-" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") +".txt"
#         else:
#             self.filename = filename
#         f = open(self.filename, "w+")
#         f.close()



#     def start(self, name: str):
#         with open(self.filename, "a") as f:
# 	        f.write("############################################################ " + name + " ############################################################\n")
# 	        f.write("#"*len(name) + "##########################################################################################################################\n")


#     def test_failed(self, arg_name: str, expected, actual, query: str):
#         with open(self.filename, "a") as f:
# 	        f.write("expected\t" + arg_name + ":\t'" + str(expected) + "'\nbut was\t\t" + arg_name + ":\t'" + str(actual) + "'\n")
# 	        f.write("when sending:\t" + query + "\n\n")

#         # print("expected:\t" + expected + "\nbut was:\t" + str(actual) + "\n")


#     def expected_error(self, arg_name: str, arg_value,  query: str):
#         with open(self.filename, "a") as f:
# 	        f.write("expected an error when sending: " + query + "\n")
# 	        f.write("but got no error \n")
# 	        f.write("because of: \"" + arg_name + "\": '" + arg_value + "'\n\n")

#         # print("expected an error when sending: " + query)
#         # print("because of: \"" + arg_name + "\": " + arg_value)

#     def exception_raised(e):
#         with open(self.filename, "a") as f:
#             f.write("an unknown exception was raised during testing:")
#             f.write(str(e))
