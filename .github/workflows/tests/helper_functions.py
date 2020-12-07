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

    def __init__(self, name, arguments= {}):
        self.name = name
        self.arguments = arguments



    def fill(self, values: dict = {}) -> str:
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

    def __init__(self, name, arguments, response_query):
        super().__init__(name, arguments=arguments)
        self.response_query = response_query

    def fill(self, values: dict) -> str:
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