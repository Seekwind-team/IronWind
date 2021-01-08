arguments = {
	"email": {
	# validation done by django
		"valid":	["a@a.aa"],
		"invalid":	["", "@a.aa", "a@.aa", "a@a.a", "a@a.", "aa.aa", "Z"*101 + "@a.aa", "a@" + "Z"*101 + ".aa", "a@a." + "Z"*21, "a a@.aa"]
	},

	"isCompany": {
		"valid":	["true", "false"],
		"invalid":	[""]
	},

	"password": {
	# [a-Z] + [0-9] + special characters, length 3-100
		"valid":	["aaa", "Z"*100, "000", "9"*100, "***", "*"*100],
		"invalid":	["", "aa", "Z"*101]
	},

	"companyName": {
	# [a-Z] + special characters, length: 1-50
		"valid":	["a", "Z"*50, "*"],
		"invalid":	["", "Z"*51]
	},

	"description": {
	# [a-Z] + special characters, length: 1-2000
		"valid":	["a", "Z"*2000, "*"],
		"invalid":	["", "Z"*2001]
	},

	"firstName": {
	# [a-Z] + special chars - and ' length: 1-50
		"valid":	["a", "Z"*50, "-", "'"],
		"invalid":	["", "*", "0", "a"*51]
	},

	"lastName": {
	# same as firstName + can be empty
		"valid":	["", "a", "Z"*50, "-", "'"],
		"invalid":	["*", "0", "a"*51]
	},

	"phoneNumber": {
	# telephone number according to e.165-format
	# [0-9], length: 3-15
		"valid":	["000", "9"*15],
		"invalid":	["", "00", "9"*16]
	},

	"birthDate": {
	# dates according to iso 8601
	# YYYY-MM-DD
	# Y: [0001-9999]
	# M: [01-12]
	# D: [01-31]
		"valid":	["0001-01-01", "9999-12-31"],
		"invalid":	["","0000-01-01", "0001-00-01", "0001-01-00", "10000-12-31", "9999-13-31", "9999-12-32"]
	},

	"gender": {
	# only male, female, diverse
		"valid":	["m", "f", "d"],
		"invalid":	["", "z"]
	},

	"shortBio": {
	# [a-Z] + [0-9] + special characters, length: 1-100
		"valid":	["a", "Z"*100, "*", "0"],
		"invalid":	["", "Z"*101]
	},

	"message": {
    # [a-Z] + [0-9] + special characters, length: 1-255
		"valid":	["a", "Z"*255, "0", "*"],
		"invalid":	["", "Z"*256]
	},

	"meta": {
    # [a-Z] + [0-9] + special characters, length: 0-255
		"valid":	["", "Z"*255, "0", "*"],
		"invalid":	["Z"*256]
	},

###############################################

	"city":{
	# [a-Z] + special characters, length: 0-100
		"valid":	[],
		"invalid":	[]
	},

	"location":{
    # [a-Z]
		"valid":	[],
		"invalid":	[]
	},

###############################################

	"hashtags":{
	# list of tags
	# tag: # [a-Z] + [0-9] + special characters, length: 1-100
		"valid": 	['["a", "'+"Z"*100+'", "0", "*"]', "[]"],
		"invalid":	[]
	},

	"jobType":{
	#
		"valid":	["", "Vollzeit", "Teilzeit", "Ausbildung", "Praktikum", "Volunteer"],
		"invalid":	["invalid"]
	},

	"jobTitle":{
	# [a-Z] + [0-9] + special characters, length: 1-255
		"valid":	["a", "Z"*255, "0", "*"],
		"invalid":	["", "Z"*256]
	},

	"jobOfferDescription":{
	# [a-Z] + [0-9] + special characters, length: 0-8000
		"valid":	["", "a", "Z"*8000, "0", "*"],
		"invalid":	["Z"*8001]
	},

	"highlights":{
    # [a-Z] + [0-9] + special characters, length: 0-1000
		"valid": 	["", "a", "Z"*1000, "0", "*"],
		"invalid":	["Z"*1001]
	},

	"mustHave":{
    # [a-Z] + [0-9] + special characters, length: 0-1000
		"valid": 	["", "a", "Z"*1000, "0", "*"],
		"invalid":	["Z"*1001]
	},

	"niceHave":{
    # [a-Z] + [0-9] + special characters, length: 0-1000
		"valid": 	["", "a", "Z"*1000, "0", "*"],
		"invalid":	["Z"*1001]
	},

	"publicEmail":{
    # same as email
    # declared after argument-dict initialization
	},

	"payPerYear":{
    # integer list separated by comma, values [1-max_int], list length 0-100
		"valid": 	["", "1", "9999999999, "*99 + "9999999999"],
		"invalid":	["9999999999, "*100 + "9999999999"]
	},

	"payPerHour":{
    # integer, can be blank
		"valid": 	["", "0"],
		"invalid":	["a", "*"]
	},

	"startDate":{
    # same as birthDate
    # declared after argument-dict initialization
	},

	"trade":{
    # [a-Z] + [0-9] + special characters, length: 0-255
		"valid": 	["", "a", "Z"*255, "0", "*"],
		"invalid":	["Z"*256]
	},



}

arguments["publicEmail"] = arguments["email"]
arguments["startDate"] = arguments["birthDate"]

def get(*arg_names: str):
    file_args = {}
    for arg_name in arg_names:
	    file_args[arg_name] = arguments[arg_name]
    return file_args