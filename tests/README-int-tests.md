integration tests can be run throught the testhub.py script

following options are available:

- no parameters
	the script runs all int-tests and creates a log-file with a timestamp in the `logs` directory
- multiple filenames
	enter the filenames you want to run **without** endings (.py)
- custom logfile name
	with the option `-l` you can enter a name for the logfile
	the name must be the **last argument** and also **without** ending