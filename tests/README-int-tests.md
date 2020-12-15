integration tests can be run throught the testhub.py script

following options are available:

- no parameters
	the script runs all int-tests and creates a log-file with a timestamp in the `logs` directory
- multiple queries
	enter the names of the queries/mutations you want to run tests on
- custom logfile name
	with the option `-l` you can enter a name for the logfile
	the name must be the **last argument** and also **without** ending

example: `python testhub.py -l updateProfile updateCompany logfile`
	to run the tests for updateProfile and updateCompany and log results into logs/logfile.txt