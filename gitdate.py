#!/usr/bin/python2
#encoding:utf-8

import os
pid = os.getpid()
import sys
from make_colors import make_colors
import subprocess
import platform
import time
if not 'arm' in platform.machine():
    import vping
# import tracert
import colorama
import configset
import random
import re
import urlparse
from debug import debug
import getpass
import traceback
colorama.init(True)

GIT_BIN = r''
if GIT_BIN == r'':
    GIT_BIN = 'git.exe'
NOTIFY_HOST = "127.0.0.1"
NOTIFY_PORT = "23053"
MAX_WAIT = 50
CONFIG = configset.configset()
CONFIG_NAME = os.path.join(os.path.dirname(__file__), 'gitdate.ini')
CONFIG.path = os.path.dirname(__file__)
CONFIG.configname = CONFIG_NAME
debug(CONFIG_NAME = CONFIG_NAME)
IS_LINUX = False
if 'linux' in sys.platform or 'msys' in sys.platform:
    IS_LINUX = True

def checkFileVersion():
    if os.path.isfile(os.path.join(os.getcwd(), '__version__.py')):
        debug("PROCESS CHECK 001 ....")
        return os.path.join(os.getcwd(), '__version__.py')
    elif os.path.isfile(os.path.join(os.getcwd(), 'version.py')):
        debug("PROCESS CHECK 002 ....")
        return os.path.join(os.getcwd(), 'version.py')
    elif os.path.isfile(os.path.join(os.getcwd(), 'version')):
        debug("PROCESS CHECK 003 ....")
        return os.path.join(os.getcwd(), 'version')
    elif os.path.isfile(os.path.join(os.getcwd(), '__VERSION__.py')):
        debug("PROCESS CHECK 004 ....")
        return os.path.join(os.getcwd(), '__VERSION__.py')
    elif os.path.isfile(os.path.join(os.getcwd(), 'VERSION.py')):
        debug("PROCESS CHECK 005 ....")
        return os.path.join(os.getcwd(), 'VERSION.py')
    elif os.path.isfile(os.path.join(os.getcwd(), 'VERSION')):
        debug("PROCESS CHECK 006 ....")
        return os.path.join(os.getcwd(), 'VERSION')
    else:
        debug("PROCESS CHECK 007 ....")
        version_file = open('__version__.py', 'w')
        version_file.close()
        return version_file.name

def gitStatus(print_separated=False):
    if sys.platform == 'win32':
        color_random = [colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.LIGHTWHITE_EX, colorama.Fore.LIGHTCYAN_EX, colorama.Fore.LIGHTMAGENTA_EX, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.LIGHTWHITE_EX, colorama.Fore.LIGHTCYAN_EX, colorama.Fore.LIGHTMAGENTA_EX, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.LIGHTWHITE_EX, colorama.Fore.LIGHTCYAN_EX, colorama.Fore.LIGHTMAGENTA_EX, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.LIGHTWHITE_EX, colorama.Fore.LIGHTCYAN_EX, colorama.Fore.LIGHTMAGENTA_EX, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.LIGHTWHITE_EX, colorama.Fore.LIGHTCYAN_EX, colorama.Fore.LIGHTMAGENTA_EX, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.LIGHTWHITE_EX, colorama.Fore.LIGHTCYAN_EX, colorama.Fore.LIGHTMAGENTA_EX]
    else:
        color_random = [colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.WHITE, colorama.Fore.CYAN, colorama.Fore.MAGENTA, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.WHITE, colorama.Fore.CYAN, colorama.Fore.MAGENTA, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.WHITE, colorama.Fore.CYAN, colorama.Fore.MAGENTA, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.WHITE, colorama.Fore.CYAN, colorama.Fore.MAGENTA, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.WHITE, colorama.Fore.CYAN, colorama.Fore.MAGENTA, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.WHITE, colorama.Fore.CYAN, colorama.Fore.MAGENTA]

    a = os.popen(GIT_BIN + " status").readlines()
    try:
        a[-1]
    except:
        print "\n"
        print make_colors("NOT a GIT REPO !", 'lightwhite', 'lightred', attrs=['blink'])
        sys.exit(1)
    if "nothing to commit, working tree clean\n" in a:
        return True
    else:
        for i in a:
            print random.choice(color_random) + str(i).split('\n')[0]
        notify(a[-1], host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
        if print_separated:
            print "-" * len(a[-1])
        return False

def writeVersion(file_version, version_number):
    f = open(file_version, 'wb')
    f.write("version = " + str(version_number))
    f.close()


def getVersion(check=True, write=True, step=0.01, test=False):
    test_number = "1"
    file_version = checkFileVersion()
    debug(file_version=file_version)
    if file_version.endswith('.py'):
        import imp
        # print "__version__ file:", __version__.__file__
        # print "dir(__version__) =", dir(__version__)
        version = ''
        try:
            # version = getattr(__version__, 'version')
            __version__ = imp.load_source('__version__', '__version__.py')
            version = __version__.version
            debug(version=version)
        except:
            traceback.format_exc()
        debug(version=version)
        if version:
            version = str(version).split(".")
            debug(version=version)
            
            if len(version) == 1:
                version = str(float(version[0]) + step)
                writeVersion(file_version, version)
            elif len(version) < 3:
                version, build_number = version[0], version[1]
                if test:
                    version = str(version) + "." + str(build_number) + "." + str(int(test_number) + 1)
                    writeVersion(file_version, version)
                else:
                    version = float(str(version) + "." + str(build_number)) + step
                    debug(version=version)
                    writeVersion(file_version, version)
            elif len(version) > 2:
                version, build_number, test_number = version[0], version[1], version[2]
                if test:
                    version = str(version) + "." + str(build_number) + "." + str(int(test_number) + 1)
                    writeVersion(file_version, version)
                else:
                    version = float(str(version) + "." + str(build_number)) + step
                    writeVersion(file_version, version)
            else:
                version = "1.00"
                writeVersion(file_version, version)
        else:
            f = open(file_version, 'rb').read()
            # with open(file_version, 'rb') as f:
            if len(f) > 1:
                version = f.split("\n")[0].strip()
                debug(version=version)
                version = float(version) + step
                debug(version=version)
                writeVersion(file_version, version)        
        
        if not version:
            print make_colors("NO VERSION FOUND !", 'lw', 'lr')
            sys.exit()
            # version = "1.00"
            # writeVersion(file_version, version)
        return version
    else:
        print make_colors("Please re-name version file to '__version__.py'", 'lw', 'lr')
        raise SystemError("Please re-name version file to '__version__.py'")
    # sys.exit(0)

def notify(message, event='Control', app = 'GitDate', title = '', icon = None, host = '127.0.0.1', port = 23053, timeout = 5):
    if not event:
        event = os.path.basename(os.getcwd())
    if not title:
        title = "Repository: " + os.path.basename(os.getcwd())
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
        if isinstance(host, list):
            for i in host:
                if ":" in i:
                    growl_host, growl_port = str(i).strip().split(":")
                    growl_port = int(growl_port)
                    try:
                        growl.publish(app, event, title, message, timeout= timeout, iconpath= icon, host = growl_host, port = int(growl_port))
                    except:
                        print "Growl Server not Found (%s:%s)" %(host,port)
                else:
                    if host and isinstance(port,int):
                        growl.publish(app, event, title, message, timeout= int(timeout), iconpath= str(icon), host=host, port=port)
                    elif host:
                        growl.publish(app, event, title, message, timeout= int(timeout), iconpath= str(icon), host=host)
                    else:
                        growl.publish(app, event, title, message, timeout= int(timeout), iconpath= str(icon))
        else:
            if host and isinstance(port,int):
                growl.publish(app, event, title, message, timeout= int(timeout), iconpath= str(icon), host=host, port=port)
            else:
                growl.publish(app, event, title, message, timeout= timeout, iconpath= icon)
    except:
        traceback.format_exc(print_msg= False)
    try:
        import PySnarl
        PySnarl.snShowMessage(title, message, timeout= timeout, iconPath= icon)
    except:
        traceback.format_exc(print_msg= False)

def checkRemoteName(remote_push_name='origin'):
    a = os.popen(GIT_BIN + " remote -v").readlines()
    a_push = []
    remote_pushs = {}
    for i in a:
        if 'push' in i:
            a_push.append(i)
    if a_push:
        for i in a_push:
            a_push = re.split("\n|\t|\(push\)", i)
            remote_pushs.update({a_push[0].strip():a_push[1].strip()})
    for i in remote_pushs:
        if remote_push_name == i:
            return True
    return False

def pushs(remote_name = None):
    global NOTIFY_HOST
    global NOTIFY_PORT
    global GIT_BIN
    a = os.popen(GIT_BIN + " remote -v").readlines()
    a_push = []
    remote_pushs = {}
    for i in a:
        if 'push' in i:
            a_push.append(i)
    if a_push:
        for i in a_push:
            a_push = re.split("\n|\t|\(push\)", i)
            remote_pushs.update({a_push[0].strip():a_push[1].strip()})
            
    #print "remote_pushs =", remote_pushs
    if remote_name and remote_name in remote_pushs.keys():
        host = format_git_remote(remote_pushs.get(remote_name))
        if host:
            print make_colors("PUSH to: ", 'white', 'red') +  make_colors("%s" % str(remote_pushs.get(remote_name)), 'yellow', '', ['blink'])
            push = subprocess.Popen([GIT_BIN, "push", host, "master"], stdout = subprocess.PIPE, shell= True)
            (push_out, push_err) = push.communicate()
            print make_colors(push_out, 'lightcyan')
            notify('Push to remote origin: %s' % str(remote_pushs.get(remote_name)), 'PUSH', host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
            
            print make_colors("PUSH Tags to: ", 'white', 'red') +  make_colors("%s" % str(remote_pushs.get(remote_name)), 'yellow', '', ['blink'])
            push_tags = subprocess.Popen([GIT_BIN, "push", host, "--tags"], stdout = subprocess.PIPE, shell= True)
            (push_out, push_err) = push_tags.communicate()
            print make_colors(push_out, 'lightcyan')
            notify('Push Tags to remote: %s' % str(remote_pushs.get(remote_name)), 'PUSH', host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
    else:
        for i in remote_pushs:
            debug(remote_pushs = remote_pushs)
            debug(remote_pushs_get_i = remote_pushs.get(i))
            host = format_git_remote(remote_pushs.get(i))
            debug(host = host)
            if host:
                print make_colors("PUSH to: ", 'white', 'red') +  make_colors("%s" % str(remote_pushs.get(i)), 'yellow', '', ['blink'])
                push = subprocess.Popen([GIT_BIN, "push", host, "master"], stdout = subprocess.PIPE, shell= True)
                (push_out, push_err) = push.communicate()
                print make_colors(push_out, 'lightcyan')
                notify('Push to remote origin: %s' % str(remote_pushs.get(i)), 'PUSH', host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
                
                print make_colors("PUSH Tags to: ", 'white', 'red') +  make_colors("%s" % str(remote_pushs.get(i)), 'yellow', '', ['blink'])
                push_tags = subprocess.Popen([GIT_BIN, "push", host, "--tags"], stdout = subprocess.PIPE, shell= True)
                (push_out, push_err) = push_tags.communicate()
                print make_colors(push_out, 'lightcyan')
                notify('Push Tags to remote: %s' % str(remote_pushs.get(i)), 'PUSH', host = [NOTIFY_HOST + ":" + NOTIFY_PORT])    
        
    
def get_hostping(host_ping):
    # host_ping = urlparse.urlparse(host_ping).netloc.split('www.')[:-1]
    host_ping = urlparse.urlparse(host_ping).netloc.split('www.')[-1]
    if "@" in host_ping:
        host_ping = host_ping.split('@')[1]
    debug(host_ping=host_ping)
    if ":" in host_ping:
        host_ping, port = str(host_ping).split(":")
        return host_ping
    debug(host_ping=host_ping)
    return host_ping

def remote_pack(remote, username = None, password = None):
    username_x = ''
    password_x = ''
    host = ''
    remote_parse = urlparse.urlparse(remote)
    scheme = remote_parse.scheme
    netloc = remote_parse.netloc
    path = remote_parse.path
    query = remote_parse.query
    if '@' in netloc:
        username_x, host = netloc.split('@')
        if ":" in username:
            username_x, password_x = username.split(":")
    if not host:
        host = netloc
    if not username:
        if username_x:
            username = username_x
    if not password:
        if password_x:
            password = password_x
    debug(username = username)
    debug(password = password)
    if username:
        if password:
            host = '%s:%s@%s' % (username, password, host)
        else:
            host = '%s@%s' % (username, host)
        if query:
            return scheme + '://' + host + path + '?' + query
        else:
            return scheme + '://' + host + path

def format_git_remote(remote):
    global CONFIG
    username = ''
    password = ''
    host = ''
    port = ''
    _remote = ''
    if not urlparse.urlparse(remote).scheme in ['http', 'https', 'ssh']:
        return False
    
    if '@' in remote:
        debug(remote = remote)
        if ":" in remote:
            check_sep = re.findall(":", remote)
            debug(check_sep = check_sep)
            debug(len_check_sep = len(check_sep))
            if len(check_sep) == 2:
                if ":" in re.split('http://|https://|ssh://|@', remote)[1]:
                    username, password = re.split('http://|https://|ssh://|@', remote)[1].split(":")
                else:
                    username = re.split('http://|https://|ssh://|@', remote)[1]
                    #password = getpass.getpass('PASSWORD: ')
                host = re.split('http://|https://|ssh://|@', remote)[-1].split('/')[0]
                if ":" in host:
                    port = host.split(":")[1]
                debug(username = username)
                debug(password = password)
                debug(host = host)
            elif len(check_sep) == 3:
                username, password = re.split('http://|https://|ssh://|@', remote)[1].split(":")
                host = re.split('http://|https://|ssh://|@', remote)[-1].split('/')[0]
                if ":" in host:
                    port = host.split(":")[1]                
                debug(username = username)
                debug(password = password)
                debug(host = host)
            else:
                username = re.split('http://|https://|ssh://|@', remote)[1]
                host = re.split('http://|https://|ssh://|@', remote)[-1].split('/')[0]
                if ":" in host:
                    port = host.split(":")[1]
                debug(username = username)
                debug(password = password)
                debug(host = host)                
            #return False
    else:
        host = urlparse.urlparse(remote).netloc
        debug(host = host)
        if ":" in host:
            port = host.split(":")[1]        
        debug(host = host)
        #return False
    if not host:
        print make_colors('INVALID REMOTE HOST NAME !', 'lightwhite', 'lightred')
        sys.exit(0)
    #if 'bitbucket' in remote or 'github' in remote or 'gogs' in remote:
    flag = host.split(".")[0]
    debug(flag = flag)
    debug(port = port)
    if ":" in flag:
        flag, port = str(flag).split(":")
    if port == '68' or port == 68:
        flag == 'gogs'
    elif port == '69' or port == 69:
        flag == 'gogs'
    elif port == '5000':
        flag = 'kallithea'
    debug(flag = flag)
    if CONFIG.read_config(flag, 'username'):
        username = CONFIG.read_config(flag, 'username')
    else:
        if not username:
            username = raw_input('[%s] USERNAME: ' % (flag))
            CONFIG.write_config(flag, 'username', value= username)
    if CONFIG.read_config(flag, 'password'):
        password = CONFIG.read_config(flag, 'password')
    else:
        if not password:
            password = getpass.getpass('[%s] PASSWORD: ' % (flag))
            CONFIG.write_config(flag, 'password', value= password)
    if not username and not password:
        return False
    remote = remote_pack(remote, username, password)
    debug(remote)
    return remote
    #else:
        #debug(remote)
        #return remote
        
def checkRemote(remote_push_name=None, branch='master'):
    host_ping = ''
    if remote_push_name:
        if checkRemoteName(remote_push_name):
            print make_colors("PUSH to: ", 'white', 'red') +  make_colors("%s" % str(remote_push_name), 'yellow', '', ['blink'])
            b = os.popen(GIT_BIN + " push %s %s"%(remote_push_name, branch)).readlines()
            print make_colors("PUSH Tags to: ", 'white', 'red') +  make_colors("%s" % str(remote_push_name), 'yellow', '', ['blink'])
            b1 = os.popen(GIT_BIN + " push %s --tags"%(remote_push_name)).readlines()
        notify('Push to remote origin: %s' % str(remote_push_name), 'PUSH', host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
        return True

    a = os.popen(GIT_BIN + " remote -v").readline()
    if len(a) < 1:
        q = raw_input(make_colors('git remote origin (URL): ', 'white', 'red'))

        if len(q) == 0:
            print make_colors("Please Add remote git url (origin) first !", 'white', 'red')
            print make_colors("EXIT!", 'white', 'red')
            sys.exit(0)
        else:
            host_ping = get_hostping(q)
            print make_colors('add remote origin: ', 'lightgreen') + make_colors('%s' % str(q), 'lightmagenta') + make_colors(' .....', 'lightcyan')
            remote_add = subprocess.Popen([GIT_BIN, 'remote', 'add', 'origin', '%s' %(str(q))], stdout = subprocess.PIPE, shell= True)
            (remote_add_out, remote_add_err) = remote_add.communicate()
            print make_colors(remote_add_out, 'lightyellow')
            notify('Add remote origin: %s' % str(q), 'Add Remote', host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
            if not IS_LINUX:
                while 1:
                    if remote_add.poll() == 0:
                        break
                    else:
                        sys.stdout.write(".")
            if not os.path.isdir(q):
                if not checkRemoteName('origin'):
                    print make_colors("Can't PUSH to %s, NO ORIGIN REMOTE NAME" % (make_colors(str(q), 'yellow')), 'white', 'red')
                    sys.exit()
                # if not host_ping and not vping.vping('8.8.8.8'):
                # 	print make_colors("Can't PUSH to %s, NO INTERNET CONNECTION" % (make_colors(str(q), 'yellow')), 'white', 'red')
                # 	sys.exit(0)
                if host_ping == 'bitbucket.org':
                    pass
                else:
                    if not 'arm' in platform.machine():
                        if not vping.vping(host_ping):
                            print make_colors("Can't PUSH to %s, NO HOST CONNECTION" % (make_colors(str(q), 'yellow')), 'white', 'red')
                            sys.exit(0)
            print make_colors("PUSH to: ", 'white', 'red') +  make_colors("%s" % str(q), 'yellow', '', ['blink'])
            push = subprocess.Popen([GIT_BIN, "push", "origin", "master"], stdout = subprocess.PIPE, shell= True)
            (push_out, push_err) = push.communicate()
            print make_colors(push_out, 'lightcyan', '')
            #os.system(GIT_BIN + " push origin master")
            notify('Push to remote origin: %s' % str(q), 'PUSH', host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
            if not IS_LINUX:
                while 1:
                    if push.poll() == 0 or push.poll() == 1 or push.poll() == 128:
                        break
                    else:
                        sys.stdout.write(".")			
            print make_colors("PUSH Tags to: ", 'white', 'red') +  make_colors("%s" % str(q), 'yellow', '', ['blink'])
            push_tags = subprocess.Popen([GIT_BIN, "push", "origin", "--tags"], stdout = subprocess.PIPE, shell= True)
            (push_out, push_err) = push_tags.communicate()
            print make_colors(push_out, 'lightcyan', '')
            #os.system(GIT_BIN + " push origin master")
            notify('Push Tags to remote origin: %s' % str(q), 'PUSH', host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
            if not IS_LINUX:
                while 1:
                    if push.poll() == 0 or push.poll() == 1 or push.poll() == 128:
                        break
                    else:
                        sys.stdout.write(".")	
    else:
        b = os.popen(GIT_BIN + " remote get-url origin").read()[:-1]
        if b:
            debug(b = b)
            host_ping = get_hostping(b)
        if not b:
            q = raw_input(make_colors('git remote origin (URL): ', 'white', 'red'))
            debug(q=q)
            host_ping = get_hostping(q)
            if len(q) == 0:
                print make_colors("Please Add remote git url (origin) first !", 'white', 'red')
                print make_colors("EXIT!", 'white', 'red')
                sys.exit(0)
        #print make_colors("PUSH to: ", 'white', 'red', ['blink'], 'termcolor') + make_colors("%s" % str(b), 'red', 'yellow', ['bold'], 'termcolor')
        #os.system(GIT_BIN + " push origin master")
        #notify('Push to remote origin: %s' % str(b), 'PUSH', host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
        if not os.path.isdir(b):
            if not checkRemoteName('origin'):
                print make_colors("Can't PUSH to %s, NO ORIGIN REMOTE NAME" % (make_colors(str(host_ping), 'yellow')), 'white', 'red')
                sys.exit(0)
            else:
                # if not host_ping and not vping.vping('8.8.8.8'):
                # 	print make_colors("Can't PUSH to %s, NO INTERNET CONNECTION" % (make_colors(str(b), 'yellow')), 'white', 'red')
                # 	sys.exit(0)
                # debug(host_ping = host_ping)
                if host_ping == 'bitbucket.org':
                    pass
                else:
                    if not 'arm' in platform.machine():
                        if not vping.vping(host_ping):
                            print make_colors("Can't PUSH to %s, NO HOST CONNECTION" % (make_colors(str(host_ping), 'yellow')), 'white', 'red')
                            sys.exit(0)		
        print make_colors("PUSH to: ", 'white', 'red') +  make_colors("%s" % str(b), 'yellow', '', ['blink'])
        push = subprocess.Popen([GIT_BIN, "push", "origin", "master"], stdout = subprocess.PIPE, shell= True)
        (push_out, push_err) = push.communicate()
        print make_colors(push_out, 'lightcyan')
        #os.system(GIT_BIN + " push origin master")
        notify('Push to remote origin: %s' % str(b), 'PUSH', host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
        if not IS_LINUX:
            while 1:
                if push.poll() == 0 or push.poll() == 1 or push.poll() == 128:
                    break
                else:
                    sys.stdout.write(".")			
        print make_colors("PUSH Tags to: ", 'white', 'red') +  make_colors("%s" % str(b), 'yellow', '', ['blink'])
        push_tags = subprocess.Popen([GIT_BIN, "push", "origin", "--tags"], stdout = subprocess.PIPE, shell= True)
        (push_out, push_err) = push_tags.communicate()
        print make_colors(push_out, 'lightcyan')
        #os.system(GIT_BIN + " push origin master")
        notify('Push Tags to remote origin: %s' % str(b), 'PUSH', host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
        if not IS_LINUX:
            while 1:
                if push.poll() == 0 or push.poll() == 1 or push.poll() == 128:
                    break
                else:
                    sys.stdout.write(".")

def controlRemote(show=True, add=False, change=False, interactive=False, show_dir=''):
    add_remote = [('',''),]
    add_remote_add = ''
    add_remote_url_add = ''
    change_remote = [('',''),]
    change_remote_add = ''
    change_remote_url_add = ''
    if show_dir:
        show_dir = "[" + make_colors("REPOSITORY: ", 'lightmagenta') + make_colors(os.path.dirname(show_dir) + "\\", "lightyellow") + make_colors(os.path.basename(show_dir), 'white', 'blue', attrs=['bold','italic']) + make_colors("", 'black') + "]"
    if sys.platform == 'win32':
        color_random = [colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.LIGHTWHITE_EX, colorama.Fore.LIGHTCYAN_EX, colorama.Fore.LIGHTMAGENTA_EX, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.LIGHTWHITE_EX, colorama.Fore.LIGHTCYAN_EX, colorama.Fore.LIGHTMAGENTA_EX, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.LIGHTWHITE_EX, colorama.Fore.LIGHTCYAN_EX, colorama.Fore.LIGHTMAGENTA_EX, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.LIGHTWHITE_EX, colorama.Fore.LIGHTCYAN_EX, colorama.Fore.LIGHTMAGENTA_EX, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.LIGHTWHITE_EX, colorama.Fore.LIGHTCYAN_EX, colorama.Fore.LIGHTMAGENTA_EX, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.LIGHTWHITE_EX, colorama.Fore.LIGHTCYAN_EX, colorama.Fore.LIGHTMAGENTA_EX]
    else:
        color_random = [colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.WHITE, colorama.Fore.CYAN, colorama.Fore.MAGENTA, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.WHITE, colorama.Fore.CYAN, colorama.Fore.MAGENTA, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.WHITE, colorama.Fore.CYAN, colorama.Fore.MAGENTA, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.WHITE, colorama.Fore.CYAN, colorama.Fore.MAGENTA, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.WHITE, colorama.Fore.CYAN, colorama.Fore.MAGENTA, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.WHITE, colorama.Fore.CYAN, colorama.Fore.MAGENTA]

    a = os.popen(GIT_BIN + " remote -v").readlines()

    if show:
        for i in a:
            print random.choice(color_random) + str(i).split("\n")[0]
        return True
    if add:
        if isinstance(add, list):
            for i in add:
                if ";" in i:
                    add_remote_add, add_remote_url_add = str(i).split(";")
                    add_remote.insert(0, (add_remote_add,add_remote_url_add))

        if interactive or add == True:
            qa_n = raw_input('Add Remote Name [%s] %s:'%(add_remote[0][0],show_dir))
            qa_u = raw_input('Add Remote URL  [%s] %s:'%(add_remote[0][1],show_dir))
            add_remote.insert(0,(qa_n,qa_u))
            if add_remote[0][0] and add_remote[0][1]:
                os.system(GIT_BIN + " remote add %s %s"%(add_remote[0][0],add_remote[0][1]))
        else:
            for i in add_remote:
                if i[0] and i[1]:
                    os.system(GIT_BIN + " remote add %s %s"%(i[0],i[1]))
        return True
    elif change:
        if isinstance(change, list):
            for i in change:
                if ";" in i:
                    change_remote_add, change_remote_url_add = str(i).split(";")
                    change_remote.insert(0, (change_remote_add,change_remote_url_add))
        if interactive or add == True:
            qa_n = raw_input('Change Remote Name [%s] %s:'%(change_remote[0][0],show_dir))
            qa_u = raw_input('Change Remote URL  [%s] %s:'%(change_remote[0][1],show_dir))
            change_remote.insert(0,(qa_n,qa_u))
            if change_remote[0][0] and change_remote[0][1]:
                os.system(GIT_BIN + " remote remove %s"%(change_remote[0][0]))
                os.system(GIT_BIN + " remote add %s %s"%(change_remote[0][0],change_remote[0][1]))
            elif change_remote[0][0] and not change_remote[0][1]:
                os.system(GIT_BIN + " remote remove %s"%(change_remote[0][0]))
        else:
            for i in change_remote:
                if i[0] and i[1]:
                    os.system(GIT_BIN + " remote remove %s"%(i[0]))
                    os.system(GIT_BIN + " remote add %s %s"%(i[0],i[1]))
                elif i[0] and not i[1]:
                    os.system(GIT_BIN + " remote remove %s"%(i[0]))
        return True
    else:
        return False

def controlRemoteDirs(show=True, add=False, change=False, interactive=False, show_dir='', dirs=None):
    if dirs:
        if isinstance(dirs ,list):
            for i in dirs:
                if os.path.isdir(i):
                    os.chdir(i)
                    controlRemote(show, add, change, interactive, show_dir=i)

def commit(no_push = False, check=False, commit=True, push_version=True, with_time=True, comment=None, print_separated=False):
    import datetime
    comment_datetime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S:%f')
    tag_datetime = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d_%H%M%S_%f')

    if not with_time:
        comment_datetime = ''
        tag_datetime = ''

    if check:
        _check = gitStatus(print_separated)
        if _check:
            print make_colors('No Commit need !', 'white', 'red', attrs=['blink'])
            notify("No Commit need !", host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
        return True

    else:
        if gitStatus(print_separated):
            print make_colors('No Commit need !', 'white', 'red', attrs=['blink'])
            notify("No Commit need !", host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
            return False

    if not push_version:
        version = getVersion(write=False)
        if not comment:
            comment = raw_input('Comment:')
        comment = comment + " ~ " + comment_datetime
    else:
        version = getVersion(False,True)
        comment = "version: " + str(version) + " ~ " + comment_datetime
    TAG = "v" + str(version) + "." + tag_datetime
    if not os.path.isfile(os.path.join(os.getcwd(), '.gitignore')):
        print make_colors('add .gitignore', 'lightyellow') + make_colors(' .....', 'lightcyan')
        f = open(os.path.join(os.getcwd(), '.gitignore'), 'w')
        f.write("*.pyc\n*.zip\n*.rar\n*.7z\n*.mp3\n*.wav\n.hg/\n*.hgignore\n*.hgtags")
        f.close()

    print make_colors('add file to index', 'lightyellow') + make_colors(' .....', 'lightcyan')
    add = subprocess.Popen([GIT_BIN, "add", "-A", '.'], stdout = subprocess.PIPE, shell= True)
    (add_out, add_err) = add.communicate()
    print make_colors(add_out, 'red', 'yellow', ['bold'])
    notify("Add file to index", 'Add File', host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
    if not IS_LINUX:
        while 1:
            if add.poll() == 0:
                break
            else:
                sys.stdout.write(".")
                time.sleep(1)

    if commit:
        print make_colors('Commit', 'lightmagenta') + make_colors(' .....', 'lightcyan')
        commit = subprocess.Popen([GIT_BIN, "commit", "-a", "-m", '%s' % comment], stdout = subprocess.PIPE, shell= True)
        (commit_out, commit_err) = commit.communicate()
        # if commit_out:
            # print "OUTPUT :", commit_out
        if commit_err:
            print "ERROR  :", commit_err
        print make_colors(str(commit_out), 'lightcyan')
        notify("Commit", 'Commit', host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
        if not IS_LINUX:
            while 1:
                if commit.poll() == 0 or commit.poll() == 1:
                    break
                else:
                    sys.stdout.write(".")
                    time.sleep(1)
        if commit_out:
            if "merge" in commit_out:
                return False
            if commit_err:
                if "merge" in commit_err:
                    return False
            else:
                if push_version:
                    print make_colors("Add Tag: ", "lightyellow") + make_colors("%s" % TAG, "lightgreen") + make_colors(' .....', 'lightcyan')
                    tag = subprocess.Popen([GIT_BIN, "tag", '%s'%str(TAG)], stdout= subprocess.PIPE, shell= True)
                    (tag_out, tag_err) = tag.communicate()
                    if tag_out:
                        print "OUTPUT :", tag_out
                    if tag_err:
                        print "ERROR  :", tag_err		
                    print make_colors(tag_out, 'white', 'cyan')
                    notify("Add tag", 'Add Tag', host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
                    if not IS_LINUX:
                        while 1:
                            if tag.poll() == 0:
                                break
                            else:
                                sys.stdout.write(".")
                                time.sleep(1)
    if no_push:
        return
    else:
        try:
            remotes = os.popen(GIT_BIN + ' remote -v' ).readlines()
            remotes_list = []
            for i in remotes:
                if '(push)' in i:
                    debug(i = i)
                    debug(i_split = re.split('\(push\)| |\t', i))
                    remotes_list.append({'name': re.split('\(push\)| |\t', i)[0], 'url': re.split('\(push\)| |\t', i)[1]})
            debug(remotes_list = remotes_list)
            if len(remotes_list) > 1:
                for i in remotes_list:
                    host = format_git_remote(i.get('url'))
                    debug(host = host)
                    if 'http:' in host or 'https:' in host or 'ssh:' in host or 'git:' in host:
                        print make_colors("PUSH to: ", 'white', 'red') +  make_colors("%s" % str(i.get('name')), 'yellow', '', ['blink'])
                        push = subprocess.Popen([GIT_BIN, "push", host, "master"], stdout = subprocess.PIPE, shell= True)
                        (push_out, push_err) = push.communicate()
                        print make_colors(push_out, 'lightcyan')
                        notify('Push to remote origin: %s' % str(i.get('name')), 'PUSH', host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
                        
                        print make_colors("PUSH Tags to: ", 'white', 'red') +  make_colors("%s" % str(i.get('name')), 'yellow', '', ['blink'])
                        push_tags = subprocess.Popen([GIT_BIN, "push", host, "--tags"], stdout = subprocess.PIPE, shell= True)
                        (push_out, push_err) = push_tags.communicate()
                        print make_colors(push_out, 'lightcyan')
                        notify('Push Tags to remote: %s' % str(i.get('name')), 'PUSH', host = [NOTIFY_HOST + ":" + NOTIFY_PORT])                                        
                    
            else:
                if len(remotes_list) == 1 and not remotes_list[0].get('name') == 'origin':
                    host = format_git_remote(remotes_list[0].get('url'))
                    if 'http:' in host or 'https:' in host or 'ssh:' in host or 'git:' in host:
                        print make_colors("PUSH to: ", 'white', 'red') +  make_colors("%s" % str(remotes_list[0].get('name')), 'yellow', '', ['blink'])
                        push = subprocess.Popen([GIT_BIN, "push", host, "master"], stdout = subprocess.PIPE, shell= True)
                        (push_out, push_err) = push.communicate()
                        print make_colors(push_out, 'lightcyan')
                        notify('Push to remote origin: %s' % str(remotes_list[0].get('name')), 'PUSH', host = [NOTIFY_HOST + ":" + NOTIFY_PORT])                    
                        print make_colors("PUSH Tags to: ", 'white', 'red') +  make_colors("%s" % str(remotes_list[0].get('name')), 'yellow', '', ['blink'])
                        push_tags = subprocess.Popen([GIT_BIN, "push", host, "--tags"], stdout = subprocess.PIPE, shell= True)
                        (push_out, push_err) = push_tags.communicate()
                        print make_colors(push_out, 'lightcyan')
                        notify('Push Tags to remote: %s' % str(remotes_list[0].get('name')), 'PUSH', host = [NOTIFY_HOST + ":" + NOTIFY_PORT])                    
                else:
                    checkRemote()
        except:
            if os.getenv('DEBUG'):
                traceback.format_exc()
            else:
                traceback.format_exc(print_msg = False)
        return

def usage():
    __help__ = make_colors("By Default if will commit with version ~ datetime if no options given", 'white','red', attrs=['italic'])
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-np', '--no-push', action='store_true', help='Doing all but don\'t push it')
    parser.add_argument('-s', '--check', action='store_true', help='Check Status')
    parser.add_argument('-ss', '--check-dir', action='store', help='Check Status by given spesific directory path', nargs='*')
    parser.add_argument('-c', '--commit', action='store_true', help='Commit this Repository')
    parser.add_argument('-cc', '--commit-dir', action='store', help='Commit this Repository by given spesific directory path')
    parser.add_argument('-r', '--add-remote', action='store_true', help='Add remote Current Repository')
    parser.add_argument('-rr', '--add-remotes', action='store', help='Add remote by given input REMOTE_NAME;REMOTE_URL it can be done with many times, for using with spesific dir use with: --add-remote-dir', nargs='*')
    parser.add_argument('-rrr', '--add-remote-dir', action='store', help='Add remote Repository by given spesific directory path', nargs='*')
    parser.add_argument('-p', '--push', action='store_true', help='Push to Current Repository')
    parser.add_argument('-pp', '--pushs', action='store', help='Push to Remote Repository by given spesific directory path it can be done with many times, for using with spesific dir use with: --push-dir', nargs='*')
    parser.add_argument('-ppp', '--push-dir', action='store', help='Push to Remote Repository with spesific directory path', nargs='*')
    parser.add_argument('-v', '--show-remote', action='store_true', help='Show all of remote Repository')
    parser.add_argument('-vv', '--show-remote-dir', action='store', help='Show all of remote Repository by given spesific directory path')
    parser.add_argument('-i', '--change-remote', action='store_true', help='Change remote Current Repository')
    parser.add_argument('-ii', '--change-remotes', action='store', help='Change remote given input REMOTE_NAME;REMOTE_URL it can be done with many times, for using with spesific dir use with: --change-remote-dir', nargs='*')
    parser.add_argument('-iii', '--change-remote-dir', action='store', help='Change remote by given spesific directory path', nargs='*')
    parser.add_argument('-nv', '--no-version', action='store_false', help='Don\'t Generate version of this program/project')
    parser.add_argument('-nt', '--no-time', action='store_false', help='Don\'t Generate Comment time of this program/project')
    parser.add_argument('-m', '--message', action='store', help='comment if --no-version')
    parser.add_argument('-V', '--version', action='store_true', help='Show version of this program/project')
    print __help__
    if len(sys.argv) == 1:
        commit()
        # parser.print_help()
    elif len(sys.argv) == 2 and sys.argv[1] == '--no-push' or sys.argv[1] == '-np':
        commit(no_push=True)
    else:
        args = parser.parse_args()
        if args.push:
            pushs()
        if args.pushs:
            for i in args.pushs:
                pushs(i)
        if args.version:
            print "VERSION     :", getVersion()
            print "NEXT VERSION:", getVersion(False, False)
        if args.check:
            #commit(no_push = False, check=False, commit=True, push_version=False, with_time=True, comment=None):
            commit(check=args.check)
        elif args.check_dir:
            for i in args.check_dir:
                if os.path.isdir(i):
                    print make_colors("REPOSITORY: ", 'lightmagenta') + make_colors(os.path.dirname(i) + "\\", "lightyellow") + make_colors(os.path.basename(i), 'white', 'blue', attrs=['bold','italic'])
                    os.chdir(i)
                    commit(check=True,print_separated=True)
        if args.add_remote:
            controlRemote(show=False, add=[os.getcwd()], interactive=True)
        elif args.add_remotes:
            controlRemote(show=False, add=args.add_remotes)
        elif args.add_remote_dir:
            if args.add_remotes:
                controlRemoteDirs(show=False, add=args.add_remotes, change=False, interactive=False, show_dir=args.add_remote_dir, dirs=args.add_remote_dir)
            else:
                controlRemoteDirs(show=False, add=True, change=False, interactive=True, show_dir=args.add_remote_dir, dirs=args.add_remote_dir)

        if args.change_remote:
            controlRemote(show=False, change=[os.getcwd()], interactive=True)
        elif args.change_remotes:
            controlRemote(show=False, change=args.change_remotes)
        elif args.change_remote_dir:
            for i in args.change_remote_dir:
                if os.path.isdir(i):
                    os.chdir(i)
                    if args.change_remotes:
                        controlRemote(show=False, add=False, change=args.change_remotes, interactive=False)
                    else:
                        controlRemote(show=False, add=False, change=True, interactive=True)

        if args.commit:
            commit(no_push = args.no_push, check=False, commit=True, push_version=args.no_version, with_time=args.no_time, comment=args.message)
        elif args.commit_dir:
            for i in args.check_dir:
                if os.path.isdir(i):
                    os.chdir(i)
                    commit(no_push = args.no_push, check=False, commit=True, push_version=args.no_version, with_time=args.no_time, comment=args.message)

if __name__ == '__main__':
    print "PID =", pid
    # print "checkFileVersion() =", checkFileVersion()
    # print "VERSION:", getVersion()
    # controlRemote()
    usage()
    #pushs()
    # checkRemote()
    # sys.exit(0)
    # if len(sys.argv) > 1:
    # 	if sys.argv[1] == '--no-push':
    # 		commit(no_push = True)
    # 	else:
    # 		commit()		
    # else:
    # 	commit()
