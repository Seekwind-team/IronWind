import requests

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
        if response.status_code == 200:
            return response.json().get('data').get('tokenAuth').get('token')
        else:
            exc = "Recieved no token. Payload: {}Response: {}".format(payload, response.json())
            raise Exception(exc)

    # requests ids for all job offers belonging to user token and returns first id
    # payload: jobOffers query
    # header: Autorization header
    def request_job_id(self, payload, header):
        response = self.run_payload(self, payload = payload, header = header)
        if response.status_code == 200:
            return response.json().get('data').get('jobOffers')[0].get('id')



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
                    mutation += arg + ":\"" + values[arg] + "\","
                else:
                    mutation += arg + ":" + values[arg] + ","

            mutation += ")"

        mutation += self.response_query

        mutation += "}"



        return mutation