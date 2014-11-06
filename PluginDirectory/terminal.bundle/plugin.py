import os

def is_valid_command(name):
	import subprocess
	whereis = subprocess.Popen(['whereis', name], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
	return len(whereis.communicate("")[0]) > 0

def results(parsed, original_query):
	command = parsed['command'] if parsed else original_query
	if command[0] not in '~/.' and not is_valid_command(command.split(' ')[0]):
		return None
	dict = {
		"title": "$ {0}".format(command),
		"run_args": [command]
	}
	if parsed==None:
		dict['dont_force_top_hit'] = True
	return dict

def run(command):
	from applescript import asrun, asquote
	# TODO: set the current working dir to the frontmost dir in Finder
	ascript = '''
	tell application "Finder" 
	 	if (count of Finder windows) is not 0 then
			set currentDir to (target of front Finder window) as text
		else
			set currentDir to "~/Desktop"
		end if
	end tell
	
	tell application "Terminal"
		activate
		do script "cd " & (quoted form of POSIX path of currentDir) & " && " & {0}
	end tell
	'''.format(asquote(command))

	asrun(ascript)