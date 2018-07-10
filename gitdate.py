import os
pid = os.getpid()
import sys
from make_colors import make_colors
import subprocess
import time
import vping
import tracert
import colorama
import configset
colorama.init(True)

GIT_BIN = r''
if GIT_BIN == r'':
	GIT_BIN = 'git.exe'
NOTIFY_HOST = "192.168.100.2"
NOTIFY_PORT = "23053"
MAX_WAIT = 50	
def checkFileVersion():
	if os.path.isfile(os.path.join(os.getcwd(), '__version__.py')):
		return os.path.join(os.getcwd(), '__version__.py')
	elif os.path.isfile(os.path.join(os.getcwd(), 'version.py')):
		return os.path.join(os.getcwd(), 'version.py')
	elif os.path.isfile(os.path.join(os.getcwd(), 'version')):
		return os.path.join(os.getcwd(), 'version')
	elif os.path.isfile(os.path.join(os.getcwd(), '__VERSION__.py')):
		return os.path.join(os.getcwd(), '__VERSION__.py')
	elif os.path.isfile(os.path.join(os.getcwd(), 'VERSION.py')):
		return os.path.join(os.getcwd(), 'VERSION.py')
	elif os.path.isfile(os.path.join(os.getcwd(), 'VERSION')):
		return os.path.join(os.getcwd(), 'VERSION')
	else:
		version_file = open('__version__.py', 'w')
		version_file.close()
		return version_file.name
	
def getVersion():
	file_version = checkFileVersion()
	#print "file_version =", checkFileVersion()
	if os.path.isfile(os.path.join(os.getcwd(), file_version)):
		version = open(os.path.join(os.getcwd(), file_version)).read().strip()
		#print "version =", version
		if isinstance(version, str) and len(version) > 1:
			#print "is STR"
			if "." in str(version):
				ver, build_num = str(version).split(".")
				#print "ver       =", ver
				#print "build_num =", build_num
				if len(build_num) > 1 and build_num[1] == '9':
					version = int(ver) + 1
					version = str(version) + "." + "0"
				else:
					#print "float(version) =", float(version)
					version = float(version) + 0.01
					#print "version x =", version
			else:
				version = float(version) + 0.01
		if version == '':
			version = "0.1"
		#print "version + =", version
		version_file = open(os.path.join(os.getcwd(), file_version), 'w')
		version_file.write(str(version))
		version_file.close()
	return str(version)
		
	
def notify(message, event='GitDate', app = 'Git Control', title = 'Git Control', icon = None, host = '127.0.0.1', port = 23053, timeout = 5):
	import traceback
	if os.getenv('GITDATE_GROWL_SERVER'):
		host = []
		for i in os.getenv('GITDATE_GROWL_SERVER').split(";"):
			host.append(str(i).strip())
	if not icon:
		icon = os.path.join(os.path.dirname(__file__), 'gitdate.png')
	try:
		import sendgrowl
		growl = sendgrowl.growl()
		print "host growl =",host
		if isinstance(host, list):
			for i in host:
				if ":" in i:
					growl_host, growl_port = str(i).strip().split(":")
					growl_port = int(growl_port)
					growl.publish(app, event, title, message, timeout= timeout, iconpath= icon, host = growl_host, port = int(growl_port))
				else:
					growl.publish(app, event, title, message, timeout= int(timeout), iconpath= str(icon))
		else:
			growl.publish(app, event, title, message, timeout= timeout, iconpath= icon)
	except:
		traceback.format_exc(print_msg= False)
	try:
		import PySnarl
		PySnarl.snShowMessage(title, message, timeout= timeout, iconPath= icon)
	except:
		traceback.format_exc(print_msg= False)

def checkRemote():
	a = os.popen(GIT_BIN + " remote -v").readline()
	# print "len(a) =", len(a)
	if len(a) < 1:
		q = raw_input(make_colors('git remote origin (URL): ', 'white', 'red'))
		if len(q) == 0:
			print make_colors("Please Add remote git url (origin) first !", 'white', 'red')
			print make_colors("EXIT!", 'white', 'red')
			sys.exit(0)
		else:
			print make_colors('add remote origin: ', 'lightgreen', color_type= 'colorama') + make_colors('%s' % str(q), 'lightmagenta', color_type= 'colorama') + make_colors(' .....', 'lightcyan', 'colorama')
			remote_add = subprocess.Popen([GIT_BIN, 'remote', 'add', 'origin', '%s' %(str(q))], stdout = subprocess.PIPE, shell= True)
			(remote_add_out, remote_add_err) = remote_add.communicate()
			print make_colors(remote_add_out, 'lightyellow', 'colorama')
			notify('Add remote origin: %s' % str(q), 'Add Remote', host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
			while 1:
				if remote_add.poll() == 0:
					break
				else:
					sys.stdout.write(".")
			if not os.path.isdir(q):
				if not vping.vping('8.8.8.8'):
					print make_colors("Can't PUSH to %s, NO INTERNET CONNECTION" % (make_colors(str(q), 'yellow')), 'white', 'red')
					sys.exit(0)
			print make_colors("PUSH to: ", 'white', 'red') +  make_colors("%s" % str(q), 'yellow', '', ['blink'], 'termcolor')
			push = subprocess.Popen([GIT_BIN, "push", "origin", "master"], stdout = subprocess.PIPE, shell= True)
			(push_out, push_err) = push.communicate()
			print make_colors(push_out, 'lightcyan', '', color_type= 'colorama')
			#os.system(GIT_BIN + " push origin master")
			notify('Push to remote origin: %s' % str(q), 'PUSH', host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
			while 1:
				if push.poll() == 0 or push.poll() == 1 or push.poll() == 128:
					break
				else:
					sys.stdout.write(".")				
	else:
		b = os.popen(GIT_BIN + " remote get-url origin").read()[:-1]
		#print make_colors("PUSH to: ", 'white', 'red', ['blink'], 'termcolor') + make_colors("%s" % str(b), 'red', 'yellow', ['bold'], 'termcolor')
		#os.system(GIT_BIN + " push origin master")
		#notify('Push to remote origin: %s' % str(b), 'PUSH', host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
		if not os.path.isdir(b):
			if not vping.vping('8.8.8.8'):
				print make_colors("Can't PUSH to %s, NO INTERNET CONNECTION" % (make_colors(str(b), 'yellow')), 'white', 'red')
				sys.exit(0)		
		print make_colors("PUSH to: ", 'white', 'red') +  make_colors("%s" % str(b), 'yellow', '', ['blink'], 'termcolor')
		push = subprocess.Popen([GIT_BIN, "push", "origin", "master"], stdout = subprocess.PIPE, shell= True)
		(push_out, push_err) = push.communicate()
		print make_colors(push_out, 'lightcyan', color_type= 'colorama')
		#os.system(GIT_BIN + " push origin master")
		notify('Push to remote origin: %s' % str(b), 'PUSH', host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
		while 1:
			if push.poll() == 0 or push.poll() == 1 or push.poll() == 128:
				break
			else:
				sys.stdout.write(".")			
			
def commit(no_push = False):
	version = getVersion()
	import datetime
	comment = "version: " + str(version) + " ~ " + datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S:%f')
	TAG = "v" + str(version) + "." + datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d_%H%M%S_%f')
	if not os.path.isfile(os.path.join(os.getcwd(), '.gitignore')):
		print make_colors('add .gitignore', 'lightyellow', color_type= 'colorama') + make_colors(' .....', 'lightcyan', 'colorama')
		f = open(os.path.join(os.getcwd(), '.gitignore'), 'w')
		f.write("*.pyc\n*.zip\n*.rar\n*.7z\n*.mp3\n*.wav\n")
		f.close()
	
	print make_colors('add file to index', 'lightyellow', color_type= 'colorama') + make_colors(' .....', 'lightcyan', 'colorama')
	add = subprocess.Popen([GIT_BIN, "add", "-A", '.'], stdout = subprocess.PIPE, shell= True)
	(add_out, add_err) = add.communicate()
	print make_colors(add_out, 'red', 'yellow', ['bold'])
	notify("Add file to index", 'Add File', host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
	while 1:
		if add.poll() == 0:
			break
		else:
			#print tag.poll()
			sys.stdout.write(".")
			time.sleep(1)
	print make_colors('Commit', 'lightmagenta', color_type= 'colorama') + make_colors(' .....', 'lightcyan', 'colorama')
	commit = subprocess.Popen([GIT_BIN, "commit", "-a", "-m", '%s' % comment], stdout = subprocess.PIPE, shell= True)
	(commit_out, commit_err) = commit.communicate()
	if commit_out:
		print "OUTPUT :", commit_out
	if commit_err:
		print "ERROR  :", commit_err
	print make_colors(str(commit_out), 'lightcyan', 'colorama')
	notify("Commit", 'Commit', host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
	while 1:
		if commit.poll() == 0 or commit.poll() == 1:
			break
		else:
			sys.stdout.write(".")
			time.sleep(1)

	if commit_out or commit_err:
		# if "merge" in commit_out or "error" in commit_out or "merge" in commit_err or "error" in commit_err:
		# 	pass
		# else:
		print make_colors("Add Tag: ", "lightyellow", color_type= 'colorama') + make_colors("%s" % TAG, "lightgreen", color_type= 'colorama') + make_colors(' .....', 'lightcyan', 'colorama')
		tag = subprocess.Popen([GIT_BIN, "tag", '%s'%str(TAG)], stdout= subprocess.PIPE, shell= True)
		(tag_out, tag_err) = tag.communicate()
		if tag_out:
			print "OUTPUT :", tag_out
		if tag_err:
			print "ERROR  :", tag_err		
		print make_colors(tag_out, 'white', 'cyan')
		notify("Add tag", 'Add Tag', host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
		m = 1
		while 1:
			if m == MAX_WAIT:
				break
			if tag.poll() == 0:
				break
			else:
				sys.stdout.write(".")
				m+=1
				time.sleep(1)
	if no_push:
		return
	else:
		checkRemote()
		return

if __name__ == '__main__':
	print "PID =", pid
	#getVersion()
	if len(sys.argv) > 1:
		if sys.argv[1] == '--no-push':
			commit(no_push = True)
		else:
			commit()		
	else:
		commit()