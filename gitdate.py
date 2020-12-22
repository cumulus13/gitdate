#!/usr/bin/env python3
#encoding:utf-8
from __future__ import print_function
import os
pid = os.getpid()
import sys
from make_colors import make_colors
import subprocess
import platform
import time
if not 'linux' in sys.platform:
    import vping
from configset import configset
import random
import re
if sys.version_info.major == 3:
    import urllib.parse
    raw_input = input
else:
    import urlparse
    class urllib:
        def parse(self):
            pass
    urllib.parse = urlparse
        
from pydebugger.debug import debug
import getpass
import traceback
try:
    from pause import pause
except:
    pass
import clipboard

GIT_BIN = r''
if not GIT_BIN:
    GIT_BIN = 'git'
NOTIFY_HOST = "127.0.0.1"
NOTIFY_PORT = "23053"
MAX_WAIT = 50
CONFIG_NAME = os.path.join(os.path.dirname(__file__), 'gitdate.ini')
debug(CONFIG_NAME = CONFIG_NAME)
CONFIG = configset(CONFIG_NAME)
IS_LINUX = False
SHELL = CONFIG.get_config('general', 'shell')
if not SHELL:
    SHELL = False
else:
    SHELL = bool(SHELL)
if 'linux' in sys.platform or 'msys' in sys.platform:
    IS_LINUX = True
    SHELL = False

    
from xnotify.notify import notify
EVENT = []
ICON = os.path.join(os.path.dirname(__file__), 'gitdate.png')
# notify.register("GitDate", EVENT, ICON)


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
    global EVENT
    global ICON
    status = []
    status_filter = ["modified:", "deleted:"]

    if sys.version_info.major == 2:
        a = os.popen3(GIT_BIN + " status")[1].readlines()
    else:
        a = os.popen(GIT_BIN + " status").readlines()
    debug(a = a)
    for i in a:
        for s in status_filter:
            if re.findall(s, i):
                status.append(re.sub("\t|\n", "", i))
    debug(status = status)
    try:
        a[-1]
    except:
        print("\n")
        print(make_colors("NOT a GIT REPO !", 'lw', 'lr', attrs=['blink']))
        sys.exit(1)
    if "nothing to commit, working tree clean\n" in a:
        return True
    else:
        print("\n")
        for i in status:
            print("\t" + make_colors(i, 'lw', 'lr'))
        #print(make_colors("".join(status), 'lw', 'lr'))        
        EVENT.append("gitstatus")
        notify.register("GitDate", EVENT, ICON)
        notify.send("gitStatus", "\n".join(status), "GitDate", "gitstatus", host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
        if print_separated:
            print("-" * len(a[-1]))
        return False

def writeVersion(file_version, version_number):
    f = open(file_version, 'w')
    f.write("version = " + str(version_number))
    f.close()

def getVersion(check=True, write=True, step=0.01, test=False, version = None):
    test_number = "1"
    file_version = checkFileVersion()
    debug(file_version=file_version)
    
    if file_version.endswith('.py'):
        if version:
            if write:
                writeVersion(file_version, version)
            return version
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
            if os.getenv('DEBUG') == '1':
                traceback.format_exc()
        debug(version=version)
        #print("version =", version)
        if version:
            version = str(version).split(".")
            #print("version 0 =", version)
            debug(version=version)

            if len(version) == 1:
                version = str(float(version[0]) + step)
                version = "%0.2f" % (version)
                if write:
                    writeVersion(file_version, version)
            elif len(version) < 3:
                version, build_number = version[0], version[1]
                if test:
                    version = str(version[0]) + "." + str(build_number) + str(int(test_number) + 1)
                    if write:
                        writeVersion(file_version, version)
                else:
                    #print("version 1 =", version[0])
                    #print("build_number 1 =", build_number)
                    #print("step 1 =", step)
                    version0 = str(version[0]) + "." + str(build_number)
                    #print("version0 =", version0)
                    version = float(version0) + float(step)
                    version = "%0.2f" % (version)
                    #print("version 1 =", version)
                    
                    debug(version=version)
                    if write:
                        writeVersion(file_version, version)
            elif len(version) > 2:
                version, build_number, test_number = version[0], version[1], version[2]
                if test:
                    version = str(version) + "." + str(build_number) + "." + str(int(test_number) + 1)
                    if write:
                        writeVersion(file_version, version)
                else:
                    #print("version 2 =", version[0])
                    #print("build_number 2 =", build_number)
                    #print("step 2 =", step)                    
                    version = float(str(version[0]) + "." + str(build_number)) + float(step)
                    version = "%0.2f" % (version)
                    if write:
                        writeVersion(file_version, version)
            else:
                version = "1.00"
                if write:
                    writeVersion(file_version, version)
        else:
            f = open(file_version, 'rb').read()
            if sys.version_info.major == 3:
                f = f.decode('utf-8')
            debug(f_version = f, debug = True)
            # with open(file_version, 'rb') as f:
            if len(f) > 1:
                version = f.split("\n")[0].strip()
                debug(version = version, debug = True)
                if "version" in version:
                    version = re.split("version|=", version)[-1]
                debug(version=version)
                version = float(version) + step
                version = "%0.2f" % (version)
                debug(version=version)
                writeVersion(file_version, version)        
            else:
                version = "0.1"
                writeVersion(file_version, version)        


        if not version:
            print(make_colors("NO VERSION FOUND !", 'lw', 'lr'))
            print(make_colors("MAKE NEW VERSION !", 'lw', 'lm'))
            # sys.exit()
            # version = "1.00"
            # writeVersion(file_version, version)
        return version
    else:
        print(make_colors("Please re-name version file to '__version__.py'", 'lw', 'lr'))
        raise SystemError("Please re-name version file to '__version__.py'")

def notifyx(message, event='Control', app = 'GitDate', title = '', icon = None, host = '127.0.0.1', port = 23053, timeout = 5):
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
                    #print("Growl Host:", growl_host)
                    #print("Growl Port:", growl_port)
                    try:
                        growl.publish(app, event, title, message, timeout= timeout, iconpath= icon, host = growl_host, port = int(growl_port))
                    except:
                        if os.getenv('DEBUG'):
                            traceback.format_exc()
                        else:
                            print("Growl Server not Found (%s:%s)" %(host,port))
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
        traceback.format_exc()
    try:
        import PySnarl
        PySnarl.snShowMessage(title, message, timeout= timeout, iconPath= icon)
    except:
        #traceback.format_exc()
        pass

def checkRemoteName(remote_push_name='origin'):
    a = os.popen(GIT_BIN + " remote -v").readlines()
    a_push = []
    remote_pushs = {}
    for i in a:
        if 'push' in i:
            a_push.append(i)
    debug(a_push = a_push)
    if a_push:
        for i in a_push:
            a_push = re.split("\n|\t|\(push\)", i)
            remote_pushs.update({a_push[0].strip():a_push[1].strip()})
    debug(remote_pushs = remote_pushs)
    for i in remote_pushs:
        if remote_push_name == i:
            return True
    return False

def getOrigin(remote_push_name='origin'):
    a = os.popen(GIT_BIN + " remote -v").readlines()
    a_push = []
    remote_pushs = {}
    for i in a:
        if 'push' in i:
            a_push.append(i)
    debug(a_push = a_push)
    if a_push:
        for i in a_push:
            a_push = re.split("\n|\t|\(push\)", i)
            remote_pushs.update({a_push[0].strip():a_push[1].strip()})
    debug(remote_pushs = remote_pushs)
    
    if remote_push_name:
        for i in remote_pushs:
            if remote_push_name == i:
                return remote_pushs.get(i)
    return remote_pushs

def pushs(remote_name = None):
    global NOTIFY_HOST
    global NOTIFY_PORT
    global GIT_BIN
    global EVENT
    global ICON
    EVENT.append("push")
    EVENT.append("push_tag")
    notify.register("GitDate", EVENT, ICON)
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

    # print "remote_pushs =", remote_pushs
    if remote_name and remote_name in list(remote_pushs.keys()):
        host = format_git_remote(remote_pushs.get(remote_name))
        if host:
            print(make_colors("PUSH to: ", 'w', 'r') +  make_colors("%s" % str(remote_pushs.get(remote_name)), 'y', '', ['blink']))
            push = subprocess.Popen([GIT_BIN, "push", host, "master"], stdout = subprocess.PIPE, shell= SHELL)
            (push_out, push_err) = push.communicate()
            if not push_out:
                push_out = b''
            if not push_err:
                push_err = b''
            print(make_colors(push_out.decode('utf-8'), 'lc'))
            print(make_colors(push_err.decode('utf-8'), 'lc'))
            
            notify.send("GitDate - Push", 'Push to remote origin: %s' % str(remote_pushs.get(remote_name)) + ":\n" + push_out.decode('utf-8') + "\n" + push_err.decode('utf-8'), 'GitDate', "push", host = [NOTIFY_HOST + ":" + NOTIFY_PORT])

            print(make_colors("PUSH Tags to: ", 'lw', 'lr') +  make_colors("%s" % str(remote_pushs.get(remote_name)), 'y', '', ['blink']))
            push_tags = subprocess.Popen([GIT_BIN, "push", host, "--tags"], stdout = subprocess.PIPE, shell= SHELL)
            (push_out, push_err) = push_tags.communicate()
            if not push_out:
                push_out = b''
            if not push_err:
                push_err = b''
            print(make_colors(push_out.decode('utf-8'), 'lc'))
            print(make_colors(push_err.decode('utf-8'), 'lc'))

            notify.send("GitDate - Push Tag", 'Push Tags to remote: %s' % str(remote_pushs.get(remote_name)) + ":\n" + push_out.decode('utf-8') + "\n" + push_err.decode('utf-8'), 'GitDate', "push_tag", host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
    else:
        for i in remote_pushs:
            debug(remote_pushs = remote_pushs)
            debug(remote_pushs_get_i = remote_pushs.get(i))
            host = format_git_remote(remote_pushs.get(i))
            debug(host = host)
            if host:
                print(make_colors("PUSH to: ", 'lw', 'lr') +  make_colors("%s" % str(remote_pushs.get(i)), 'ly', ['blink']))
                push = subprocess.Popen([GIT_BIN, "push", host, "master"], stdout = subprocess.PIPE, shell= SHELL)
                (push_out, push_err) = push.communicate()
                if not push_out:
                    push_out = b'-'
                if not push_err:
                    push_err = b'--'
                print(make_colors(push_out.decode('utf-8'), 'ly'))
                print(make_colors(push_err.decode('utf-8'), 'ly'))

                notify.send("GitDate - Push", 'Push to remote origin: %s' % str(remote_pushs.get(i)) + ":\n" + push_out.decode('utf-8') + "\n" + push_err.decode('utf-8'), 'GitDate', "push", host = [NOTIFY_HOST + ":" + NOTIFY_PORT])

                print(make_colors("PUSH Tags to: ", 'b', 'ly') + make_colors("%s" % str(remote_pushs.get(i)), 'ly', ['blink']))
                push_tags = subprocess.Popen([GIT_BIN, "push", host, "--tags"], stdout = subprocess.PIPE, shell= SHELL)
                (push_out, push_err) = push_tags.communicate()
                if not push_out:
                    push_out = b''
                if not push_err:
                    push_err = b''
                print(make_colors(push_out.decode('utf-8'), 'lc'))
                print(make_colors(push_err.decode('utf-8'), 'lc'))

                notify.send("GitDate - Push Tag", 'Push Tags to remote: %s' % str(remote_pushs.get(i)) + ":\n" + push_out.decode('utf-8') + "\n" + push_err.decode('utf-8'), 'GitDate', "push_tag", host = [NOTIFY_HOST + ":" + NOTIFY_PORT])

def get_hostping(host_ping):
    # host_ping = urlparse.urlparse(host_ping).netloc.split('www.')[:-1]
    host_ping = urllib.parse.urlparse(host_ping).netloc.split('www.')[-1]
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
    remote_parse = urllib.parse.urlparse(remote)
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
    debug(remote = remote)
    global CONFIG
    username = ''
    password = ''
    host = ''
    port = ''
    if not remote:
        remote = ''
    debug(remote = remote)
    #print ("SCHEME:", urlparse.urlparse(remote))
    if not urllib.parse.urlparse(remote).scheme == 'https' and not urllib.parse.urlparse(remote).scheme == 'http' and not urllib.parse.urlparse(remote).scheme == 'ssh':
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
        host = urllib.parse.urlparse(remote).netloc
        debug(host = host)
        if ":" in host:
            port = host.split(":")[1]        
        debug(host = host)
        #return False
    if not host:
        print(make_colors('INVALID REMOTE HOST NAME !', 'lw', 'lr'))
        sys.exit(0)
    #if 'bitbucket' in remote or 'github' in remote or 'gogs' in remote:
    flag = host.split(".")[0]
    debug(flag = flag)
    debug(port = port)
    if ":" in flag:
        flag, port = str(flag).split(":")
    if port == '68' or port == 68:
        flag == 'gogs'
    if port == '69' or port == 69:
        flag == 'gogs'
    elif port == '5000':
        flag = 'kallithea'
    # print("FLAG: %s"%(str(flag)))
    debug(flag = flag)
    if CONFIG.read_config(flag, 'username'):
        username = CONFIG.read_config(flag, 'username')
        if "@" in username:
            username = re.split("@", username)[0].strip()
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
    global EVENT
    global ICON
    EVENT.append("add_remote")
    notify.register("GitDate", EVENT, ICON)

    host_ping = ''
    if remote_push_name:
        if checkRemoteName(remote_push_name):
            print(make_colors("PUSH to: ", 'w', 'r') +  make_colors("%s" % str(remote_push_name), 'y', '', ['blink']))
            b = os.popen(GIT_BIN + " push %s %s"%(remote_push_name, branch)).readlines()
            print(make_colors("PUSH Tags to: ", 'lw', 'lr') +  make_colors("%s" % str(remote_push_name), 'y', '', ['blink']))
            b1 = os.popen(GIT_BIN + " push %s --tags"%(remote_push_name)).readlines()
        notify.send("GitDate - Push", 'Push to remote origin: %s' % str(remote_push_name), 'GitDate', "push", host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
        return True

    a = os.popen(GIT_BIN + " remote -v").readline()
    if len(a) < 1:
        q = raw_input(make_colors('git remote origin (URL), type "github" for Github: ', 'w', 'r'))
        if q == 'github':
            CONFIG.write_config('default', 'repo', 'github')
            check_repo()
        else:
            if len(q) == 0:
                print(make_colors("Please Add remote git url (origin) first !", 'w', 'r'))
                print(make_colors("EXIT!", 'w', 'r'))
                sys.exit(0)
            else:
                host_ping = get_hostping(q)
                print(make_colors('add remote origin: ', 'lg') + make_colors('%s' % str(q), 'lm') + make_colors(' .....', 'lc'))
                remote_add = subprocess.Popen([GIT_BIN, 'remote', 'add', 'origin', '%s' %(str(q))], stdout = subprocess.PIPE, shell= SHELL)
                (remote_add_out, remote_add_err) = remote_add.communicate()
                if not remote_add_out:
                    remote_add_out = b''
                if not remote_add_err:
                    remote_add_err = b''
                print(make_colors(remote_add_out, 'ly'))
                
                notify.send("GitDate - Add remote", 'Add remote origin: %s' % str(q), 'GitDate', "add_remote", host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
                
                if not IS_LINUX:
                    while 1:
                        if remote_add.poll() == 0:
                            break
                        else:
                            sys.stdout.write(".")
                if not os.path.isdir(q):
                    if not checkRemoteName('origin'):
                        print(make_colors("Can't PUSH to %s, NO ORIGIN REMOTE NAME" % (make_colors(str(q), 'y')), 'w', 'r'))
                        sys.exit()
                    # if not host_ping and not vping.vping('8.8.8.8'):
                    # 	print make_colors("Can't PUSH to %s, NO INTERNET CONNECTION" % (make_colors(str(q), 'y')), 'w', 'r')
                    # 	sys.exit(0)
                    #if host_ping == 'bitbucket.org':
                        #pass
                    #else:
                        #if not 'arm' in platform.machine():
                            #if not vping.vping(host_ping):
                                #print(make_colors("Can't PUSH to %s, NO HOST CONNECTION" % (make_colors(str(q), 'y')), 'w', 'r'))
                                #sys.exit(0)
                print(make_colors("PUSH to: ", 'w', 'r') +  make_colors("%s" % str(q), 'y', '', ['blink']))
                push = subprocess.Popen([GIT_BIN, "push", "origin", "master"], stdout = subprocess.PIPE, shell= SHELL)
                (push_out, push_err) = push.communicate()
                if not push_out:
                    push_out = b''
                if not push_err:
                    push_err = b''
                print(make_colors(push_out, 'lc', ''))
                #os.system(GIT_BIN + " push origin master")
                
                notify.send("GitDate - Push", 'Push to remote origin: %s' % str(q) + ":\n" + push_out.decode('utf-8'), 'GitDate', "push", host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
                
                if not IS_LINUX:
                    while 1:
                        if push.poll() == 0 or push.poll() == 1 or push.poll() == 128:
                            break
                        else:
                            sys.stdout.write(".")			
                print(make_colors("PUSH Tags to: ", 'lw', 'lr') +  make_colors("%s" % str(q), 'y', '', ['blink']))
                push_tags = subprocess.Popen([GIT_BIN, "push", "origin", "--tags"], stdout = subprocess.PIPE, shell= SHELL)
                (push_out, push_err) = push_tags.communicate()
                if not push_out:
                    push_out = b''
                if not push_err:
                    push_err = b''
                print(make_colors(push_out, 'lc', ''))
                #os.system(GIT_BIN + " push origin master")
                
                notify.send("GitDate - Push Tag", 'Push Tags to remote origin: %s' % str(q) + ":\n" + push_out.decode('utf-8'), 'GitDate', "push_tag", host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
                
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
            q = raw_input(make_colors('git remote origin (URL): ', 'w', 'r'))
            debug(q=q)
            host_ping = get_hostping(q)
            if len(q) == 0:
                print(make_colors("Please Add remote git url (origin) first !", 'w', 'r'))
                print(make_colors("EXIT!", 'w', 'r'))
                sys.exit(0)
        #print make_colors("PUSH to: ", 'w', 'r', ['blink'], 'termcolor') + make_colors("%s" % str(b), 'r', 'y', ['bold'], 'termcolor')
        #os.system(GIT_BIN + " push origin master")
        #notify('Push to remote origin: %s' % str(b), 'PUSH', host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
        if not os.path.isdir(b):
            if not checkRemoteName('origin'):
                print(make_colors("Can't PUSH to %s, NO ORIGIN REMOTE NAME" % (make_colors(str(host_ping), 'y')), 'w', 'r'))
                sys.exit(0)
            #else:
                # if not host_ping and not vping.vping('8.8.8.8'):
                # 	print make_colors("Can't PUSH to %s, NO INTERNET CONNECTION" % (make_colors(str(b), 'y')), 'w', 'r')
                # 	sys.exit(0)
                # debug(host_ping = host_ping)
                #if host_ping == 'bitbucket.org':
                    #pass
                #else:
                    #if not 'arm' in platform.machine():
                        #if not vping.vping(host_ping):
                            #print(make_colors("Can't PUSH to %s, NO HOST CONNECTION" % (make_colors(str(host_ping), 'y')), 'w', 'r'))
                            #sys.exit(0)		
        print(make_colors("PUSH to: ", 'w', 'r') +  make_colors("%s" % str(b), 'y', '', ['blink']))
        push = subprocess.Popen([GIT_BIN, "push", "origin", "master"], stdout = subprocess.PIPE, shell= SHELL)
        (push_out, push_err) = push.communicate()
        if not push_out:
            push_out = b''
        if not push_err:
            push_err = b''
        print(make_colors(push_out, 'lc'))
        #os.system(GIT_BIN + " push origin master")
        
        notify.send("GitDate - Push", 'Push to remote origin: %s' % str(b) + ":\n" + push_out.decode('utf-8'), 'GitDate', "push", host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
        
        if not IS_LINUX:
            while 1:
                if push.poll() == 0 or push.poll() == 1 or push.poll() == 128:
                    break
                else:
                    sys.stdout.write(".")			
        print(make_colors("PUSH Tags to: ", 'lw', 'lr') +  make_colors("%s" % str(b), 'y', '', ['blink']))
        push_tags = subprocess.Popen([GIT_BIN, "push", "origin", "--tags"], stdout = subprocess.PIPE, shell= SHELL)
        (push_out, push_err) = push_tags.communicate()
        if not push_out:
            push_out = b''
        if not push_err:
            push_err = b''
        print(make_colors(push_out, 'lc'))
        #os.system(GIT_BIN + " push origin master")
        
        notify.send("GitDate - Push Tag", 'Push Tags to remote origin: %s' % str(b) + ":\n" + push_out.decode('utf-8'), 'GitDate', "push_tag", host = [NOTIFY_HOST + ":" + NOTIFY_PORT])

        if not IS_LINUX:
            while 1:
                if push.poll() == 0 or push.poll() == 1 or push.poll() == 128:
                    break
                else:
                    sys.stdout.write(".")

def controlRemote(show=True, add=False, change=False, interactive=False, show_dir=''):
    debug(add = add)
    add_remote = [('',''),]
    add_remote_add = ''
    add_remote_url_add = ''
    change_remote = [('',''),]
    change_remote_add = ''
    change_remote_url_add = ''
    if show_dir:
        show_dir = "[" + make_colors("REPOSITORY: ", 'lm') + make_colors(os.path.dirname(show_dir) + "\\", 'ly') + make_colors(os.path.basename(show_dir), 'w', 'bl', attrs=['bold','italic']) + make_colors("", 'black') + "]"
    color_random = ['g', 'y', 'lw', 'lc', 'lm']

    a = os.popen(GIT_BIN + " remote -v").readlines()

    if show:
        for i in a:
            print(make_colors(str(i).split("\n")[0]), random.choice(color_random))
        if not add:
            return True
    if add:
        if isinstance(add, list):
            for i in add:
                if ";" in i:
                    add_remote_add, add_remote_url_add = str(i).split(";")
                    add_remote.insert(0, (add_remote_add,add_remote_url_add))

        if interactive and not add:
            qa_n = raw_input('Add Remote Name [%s] %s:'%(add_remote[0][0],show_dir))
            qa_u = raw_input('Add Remote URL  [%s] %s:'%(add_remote[0][1],show_dir))
            add_remote.insert(0,(qa_n,qa_u))
            if add_remote[0][0] and add_remote[0][1]:
                os.system(GIT_BIN + " remote add %s %s"%(add_remote[0][0],add_remote[0][1]))
        else:
            debug(add = add)
            if ";" in add:
                remote, url = add.split(";")
                CMD = GIT_BIN + " remote add {0} {1}".format(remote.strip(), url.strip())
                debug(CMD = CMD)
                os.system(CMD)
            else:
                if not 'http:' in add or not 'https:' in add or not 'ssh' in add or not 'git:' in add:
                    return controlRemote(show, False, change, True, show_dir)
                else:
                    while 1:
                        url = raw_input(make_colors('Add Remote URL: ', 'lw', 'lr'))
                        if remote:
                            break
                    CMD = GIT_BIN + " remote add {0} {1}".format(add , url.strip())
                    debug(CMD = CMD)
                    os.system(CMD)
                    
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
                    
def check_version(version, repo_path = os.getcwd()):
    if not version:
        return True
    import git
    repo = git.Repo(repo_path)
    
    for i in repo.iter_commits('--all'):
        _version = re.findall('version: (.*?) ~', i.message)
        debug(version = _version)
        if len(_version) > 0:
            if _version[0].strip() == version:
                return False
    return True
    
def commit(no_push = False, check=False, commit=True, push_version=True, with_time=True, comment=None, print_separated=False, version = None):
    global EVENT
    global ICON
    EVENT.append("error")
    EVENT.append("add_file")
    EVENT.append("commit")
    notify.register("GitDate", EVENT, ICON)

    import datetime
    comment_datetime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S:%f')
    tag_datetime = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d_%H%M%S_%f')
    debug(comment_datetime = comment_datetime)
    debug(tag_datetime = tag_datetime)
    debug(check = check)
    debug(with_time = with_time)
    debug(getcwd = os.getcwd())
    
    if not with_time:
        comment_datetime = ''
        tag_datetime = ''
    
    if check:
        _check = gitStatus(print_separated)
        if _check:
            print(make_colors('No Commit need !', 'w', 'r', attrs=['blink']))
            
            notify.send("GitDate - Commit", 'No Commit need !', 'GitDate', "error", host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
            return False
        return True

    else:
        if gitStatus(print_separated):
            print(make_colors('No Commit need !', 'w', 'r', attrs=['blink']))
            notify.send("GitDate - Commit", 'No Commit need !', 'GitDate', "error", host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
            return False
    #pause()
    debug(push_version = push_version)
    #pause()
    if not push_version:
        if version and not check_version(version):
            print(make_colors("Version {0} is Exists !".format(version), 'lw', 'lr', ['blink']))
            version = None
            sys.exit()

        version = getVersion(write=False, version = version)
        debug(version = version)
        debug(comment = comment)
        if not comment:
            comment = raw_input('Comment:')
        comment = comment + " ~ " + comment_datetime
        debug(comment = comment)
            
    else:
        if version and not check_version(version):
            print(make_colors("Version {0} is Exists !".format(version), 'lw', 'lr', ['blink']))
            version = None
            sys.exit()
            
        version = getVersion(False, True)
        comment = "version: " + str(version) + " ~ " + comment_datetime
        debug(version = version)
        debug(comment = comment)        
    TAG = "v" + str(version) + "." + tag_datetime
    debug(TAG = TAG)
    debug(check_gitignore = os.path.isfile(os.path.join(os.getcwd(), '.gitignore')))
    #pause()
    if not os.path.isfile(os.path.join(os.getcwd(), '.gitignore')):
        print(make_colors('add .gitignore', 'ly') + make_colors(' .....', 'lc'))
        f = open(os.path.join(os.getcwd(), '.gitignore'), 'w')
        f.write("*.pyc\n*.bak\n*.zip\n*.rar\n*.7z\n*.mp3\n*.wav\n*.sublime-workspace\n.hg/\nbuild/\n*.hgignore\n*.hgtags\n*dist/\n*.egg-info/\ntraceback.log\n__pycache__/")
        f.close()

    print(make_colors('add file to index', 'ly') + make_colors(' .....', 'lc'))
    add = subprocess.Popen([GIT_BIN, "add", "-A", '.'], stdout = subprocess.PIPE, shell= SHELL)
    (add_out, add_err) = add.communicate()
    if not add_out:
        add_out = b''
    if not add_err:
        add_err = b''
    print(make_colors(add_out, 'r', 'y', ['bold']))
    
    notify.send("GitDate - Add File", 'Add File:' + "\n" + add_out.decode('utf-8') + "\n" + add_err.decode('utf-8'), 'GitDate', "add_file", host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
    
    if not IS_LINUX:
        while 1:
            if add.poll() == 0:
                break
            else:
                sys.stdout.write(".")
                time.sleep(1)

    if commit:
        print(make_colors('Commit', 'lm') + make_colors(' .....', 'lc'))
        commit = subprocess.Popen([GIT_BIN, "commit", "-a", "-m", '%s' % comment], stdout = subprocess.PIPE, shell= SHELL)
        (commit_out, commit_err) = commit.communicate()
        if not commit_out:
            commit_out = b''
        if not commit_err:
            commit_err = b''
        # if commit_out:
            # print "OUTPUT :", commit_out
        if commit_err:
            print("ERROR  :", commit_err)
            notify.send("GitDate - Commit", 'Commit ERROR:' + "\n" + commit_err.decode('utf-8') + "\n" + commit_out.decode('utf-8'), 'GitDate', "error", host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
        print(make_colors(commit_out.decode('utf-8'), 'lc'))
        
        notify.send("GitDate - Commit", 'Commit:' + "\n" + commit_out.decode('utf-8') + "\n" + commit_err.decode('utf-8'), 'GitDate', "commit", host = [NOTIFY_HOST + ":" + NOTIFY_PORT])

        if not IS_LINUX:
            while 1:
                if commit.poll() == 0 or commit.poll() == 1:
                    break
                else:
                    sys.stdout.write(".")
                    time.sleep(1)
        if commit_out:
            if "merge" in str(commit_out):
                return False
            if commit_err:
                if "merge" in commit_err:
                    return False
            else:
                if push_version:
                    print(make_colors("Add Tag: ", 'ly') + make_colors("%s" % TAG, 'lg') + make_colors(' .....', 'lc'))
                    tag = subprocess.Popen([GIT_BIN, "tag", '%s'%str(TAG)], stdout= subprocess.PIPE, shell= SHELL)
                    (tag_out, tag_err) = tag.communicate()
                    if not tag_out:
                        tag_out = b''
                    if not tag_err:
                        tag_err = b''
                    if tag_out:
                        print("OUTPUT :", tag_out)
                    if tag_err:
                        print("ERROR  :", tag_err)		
                    print(make_colors(tag_out, 'w', 'cyan'))
                    
                    notify.send("GitDate - Add Tag", 'Add Tag:' + "\n" + str(TAG), 'GitDate', "add_tag", host = [NOTIFY_HOST + ":" + NOTIFY_PORT])

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
            debug(remotes = remotes)
            remotes_list = []
            for i in remotes:
                if '(push)' in i:
                    debug(i = i)
                    debug(i_split = re.split('\(push\)| |\t', i))
                    remotes_list.append({'name': re.split('\(push\)| |\t', i)[0], 'url': re.split('\(push\)| |\t', i)[1]})
            debug(remotes_list = remotes_list)
            if len(remotes_list) > 0:
                for i in remotes_list:
                    debug(i = i)
                    host = format_git_remote(i.get('url'))
                    debug(host = host)
                    if 'git@' in i.get('url') or 'https:' in i.get('url') or 'ssh:' in i.get('url') or 'http:' in i.get('url'):
                        print(make_colors("PUSH to: ", 'w', 'r') +  make_colors("%s" % str(i.get('name')), 'y', '', ['blink']))
                        push = subprocess.Popen([GIT_BIN, "push", host, "master"], stdout = subprocess.PIPE, shell= SHELL)
                        (push_out, push_err) = push.communicate()
                        if not push_out:
                            push_out = b''
                        if not push_err:
                            push_err = b''
                        print(make_colors(push_out, 'lc'))
                    
                        notify.send("GitDate - Push", 'Push to remote %s [%s]' % (str(i.get('name')) + ":\n" + push_out.decode('utf-8') + "\n" + push_err.decode('utf-8'), i.get('url')), 'GitDate', "push", host = [NOTIFY_HOST + ":" + NOTIFY_PORT])

                        print(make_colors("PUSH Tags to: ", 'lw', 'lr') +  make_colors("%s" % str(i.get('name')), 'y', '', ['blink']))
                        push_tags = subprocess.Popen([GIT_BIN, "push", host, "--tags"], stdout = subprocess.PIPE, shell= SHELL)
                        (push_out, push_err) = push_tags.communicate()
                        if not push_out:
                            push_out = b''
                        if not push_err:
                            push_err = b''
                        print(make_colors(push_out, 'lc'))
                    
                        notify.send("GitDate - Push Tag", 'Push Tags to remote %s [%s]' % (str(i.get('name')) + ":\n" + push_out.decode('utf-8') + "\n" + push_err.decode('utf-8'), i.get('url')), 'GitDate', "push_tag", host = [NOTIFY_HOST + ":" + NOTIFY_PORT])

            else:
                if len(remotes_list) == 1 and not remotes_list[0].get('name') == 'origin':
                    host = format_git_remote(remotes_list[0].get('url'))
                    debug(host = host)
                    # if 'https:' in host or 'http:' in host or 'ssh:' in host or 'git:' in host:
                    if  urllib.parse.urlparse(host).scheme == 'https' or urllib.parse.urlparse(host).scheme == 'http' or urllib.parse.urlparse(host).scheme == 'ssh' or urllib.parse.urlparse(host).scheme == 'git':
                        print(make_colors("PUSH to: ", 'w', 'r') +  make_colors("%s" % str(remotes_list[0].get('name')), 'y', '', ['blink']))
                        push = subprocess.Popen([GIT_BIN, "push", host, "master"], stdout = subprocess.PIPE, shell= SHELL)
                        (push_out, push_err) = push.communicate()
                        if not push_out:
                            push_out = b''
                        if not push_err:
                            push_err = b''
                        print(make_colors(push_out, 'lc'))
                        
                        notify.send("GitDate - Push", 'Push to remote origin: %s' % str(remotes_list[0].get('name')) + ":\n" + push_out.decode('utf-8') + "\n" + push_err.decode('utf-8'), 'GitDate', "push", host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
                        
                        print(make_colors("PUSH Tags to: ", 'lw', 'lr') +  make_colors("%s" % str(remotes_list[0].get('name')), 'y', '', ['blink']))
                        push_tags = subprocess.Popen([GIT_BIN, "push", host, "--tags"], stdout = subprocess.PIPE, shell= SHELL)
                        (push_out, push_err) = push_tags.communicate()
                        if not push_out:
                            push_out = b''
                        if not push_err:
                            push_err = b''
                        print(make_colors(push_out, 'lc'))
                        
                        notify.send("GitDate - Push Tag", 'Push Tags to remote origin: %s' % str(remotes_list[0].get('name')) + ":\n" + push_out.decode('utf-8') + "\n" + push_err.decode('utf-8'), 'GitDate', "push_tag", host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
                else:
                    checkRemote()
        except:
            if os.getenv('DEBUG'):
                traceback.format_exc()
            else:
                traceback.format_exc()
        return

def create_repo(data):
    data_split = None
    if ":" in data:
        data_split = re.split(":", data)
    else:
        data_split = [data]
    if len(data_split) == 1 and data_split[0] == 'github':
        create_repo_github()
    elif len(data_split) == 2:
        if data_split[0] == 'github':
            if data_split[1] == 'private' or data_split[1] == 'public':
                if data_split[1] == 'private':
                    repo_name, repo_url = create_repo_github(private=True)
                else:
                    repo_name, repo_url = create_repo_github(private=False)
            else:
                repo_name, repo_url = create_repo_github(repo_name = data_split[1])
            add = "origin;" + repo_url
            controlRemote(add = add, interactive = True)

        else:
            add = data_split[0] + ";" + data_split[1]
            controlRemote(add = add, interactive = True)
    elif len(data_split) == 3:
        if data_split[0] == 'github':
            if data_split[1] == 'private' or data_split[1] == 'public':
                if data_split[1] == 'private':
                    repo_name, repo_url = create_repo_github(private=True)
                else:
                    repo_name, repo_url = create_repo_github(private=False)
            elif data_split[2] == 'public' or data_split[2] == 'private':
                repo_name, repo_url = create_repo_github(None, False, data_split[1])
            else:
                repo_name, repo_url = create_repo_github(None, True, data_split[1])
            add = "origin;" + repo_url
            controlRemote(add = add, interactive = True)
        else:
            add = data_split[0] + ";" + data_split[1]
            controlRemote(add = add, interactive = True)

    elif len(data_split) == 4:
        if data_split[0] == 'github':
            if data_split[1] == 'private' or data_split[1] == 'public':
                if data_split[1] == 'private':
                    repo_name, repo_url = create_repo_github(private=True)
                else:
                    repo_name, repo_url = create_repo_github(private=False)

            elif data_split[2] == 'public' or data_split[2] == 'private':
                repo_name, repo_url = create_repo_github(data_split[3], False, data_split[1])
            else:
                repo_name, repo_url = create_repo_github(data_split[3], True, data_split[1])
            add = "origin;" + repo_url
            controlRemote(add = add, interactive = True)
        else:
            add = data_split[0] + ";" + data_split[1]
            controlRemote(add = add, interactive = True)
    
def create_repo_github(username = None, private = True, repo_name = None, token = None, client_id = None, client_secret = None):
    global EVENT
    global ICON
    EVENT.append("github")
    notify.register("GitDate", EVENT, ICON)
    try:
        from github import Github
    except:
        print(make_colors("No pygithub installer !", 'lw', 'lr'))
        notify.send("GitDate - Error", 'No pygithub installer !', 'GitDate', "error", host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
        return False
    if not repo_name:
        REPO_NAME = os.path.basename(os.getcwd())
    else:
        REPO_NAME = repo_name
    if check_repo_github(REPO_NAME, as_is = True):
            # add = "origin;" + 'https://github.com/' + REPO_NAME
            # controlRemote(add = add, interactive = True)
            # os.system(GIT_BIN + " remote -v")
        return True
    debug(REPO_NAME = REPO_NAME)
    if not username:
        username = CONFIG.get_config('github', 'username')
    
    debug(username = username)
    if not username:
        username = raw_input(make_colors("Github Username :", 'b', 'ly'))
        if username:
            CONFIG.write_config('github', 'username', username)
    
    if not token:
        token = CONFIG.get_config('github', 'token', '2c5a2b2dbab79f8042c0b2ebdfb6c4a9fc0828b6')
    client_id = CONFIG.get_config('github', 'client_id', 'bcc0c5253f5a43845355')
    client_secret = CONFIG.get_config('github', 'client_secret', '264e42f7ecff43665d0c948edee04d1d54eea9ea')

    debug(username = username)
    
    if token:
        g = Github(token)
    auth = g.get_user()
    debug(auth = auth)
    README = None
    DECRIPTION = None
    for i in os.listdir(os.getcwd()):
        if 'readme' in i.lower():
            README = os.path.join(os.getcwd(), i)
            break
    print("README:", make_colors(README, 'lw', 'bl'))
    if README and os.path.isfile(README):
        DECRIPTION = open(README, 'rb').read()
    if DECRIPTION:
        try:
            auth.create_repo(REPO_NAME, private = private, has_issues = True, description = DECRIPTION)
            notify.send("GitDate - Create Repo On Github", 'Create Repo On Github with description: ' + REPO_NAME, 'GitDate', "github", host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
        except:
            auth.create_repo(REPO_NAME, private = private, has_issues = True, description = '')
            notify.send("GitDate - Create Repo On Github", 'Create Repo On Github: ' + REPO_NAME, 'GitDate', "github", host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
    else:
        auth.create_repo(REPO_NAME, private = private, has_issues = True)
        notify.send("GitDate - Create Repo On Github", 'Create Repo On Github has_issues: ' + REPO_NAME, 'GitDate', "github", host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
    return REPO_NAME, 'https://github.com/' + username + "/" + REPO_NAME

def edit_repo_github(private = True, repo_name = None, token = None):
    try:
        from github import Github
    except:
        print(make_colors("No pygithub installer !", 'lw', 'lr'))
        notify.send("GitDate - Error", 'No pygithub installer !', 'GitDate', "error", host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
        return False
    if not repo_name:
        REPO_NAME = os.path.basename(os.getcwd())
    else:
        REPO_NAME = repo_name
    if not check_repo_github(REPO_NAME, as_is = True):
            # add = "origin;" + 'https://github.com/' + REPO_NAME
            # controlRemote(add = add, interactive = True)
            # os.system(GIT_BIN + " remote -v")
        return create_repo_github(private = private, token = token, repo_name = repo_name)
    debug(REPO_NAME = REPO_NAME)
    
    if not token:
        token = CONFIG.get_config('github', 'token', '2c5a2b2dbab79f8042c0b2ebdfb6c4a9fc0828b6')
    if not token:
        token = raw_input(make_colors("TOKEN:", 'lw', 'lr') + " ")

    if token:
        g = Github(token)
    else:
        while 1:
            token = raw_input(make_colors("TOKEN:", 'lw', 'lr') + " ")
            if token:
                break
        g = Github(token)
    debug(REPO_NAME = REPO_NAME)
    auth = g.get_user()
    repo_edit = auth.get_repo(REPO_NAME)
    debug(auth = auth)
    README = None
    DECRIPTION = None
    for i in os.listdir(os.getcwd()):
        if 'readme' in i.lower():
            README = os.path.join(os.getcwd(), i)
            break
    if not README:
        README = ''
    print("README:", make_colors(README, 'lw', 'bl'))
    if README and os.path.isfile(README):
        DECRIPTION = open(README, 'rb').read()
    debug(DECRIPTION = DECRIPTION)
    if DECRIPTION:
        try:
            repo_edit.edit(REPO_NAME, private = private, has_issues = True, description = DECRIPTION)
        except:
            repo_edit.edit(REPO_NAME, private = private, has_issues = True, description = '')
    else:
        repo_edit.edit(REPO_NAME, private = private, has_issues = True)
    username = CONFIG.write_config('github', 'username', 'cumulus13')
    return REPO_NAME, 'https://github.com/' + username + "/" + REPO_NAME

def check_repo_github(name = None, private = False, sort = 'time', as_is = True, token = None, client_id = None, client_secret = None):
    try:
        from github import Github
    except:
        print(make_colors("No pygithub installer !", 'lw', 'lr'))
        notify.send("GitDate - Error", 'No pygithub installer !', 'GitDate', "error", host = [NOTIFY_HOST + ":" + NOTIFY_PORT])
        return False
    
    username = CONFIG.get_config('github', 'username')
    
    debug(username = username)
    if not username:
        username = raw_input(make_colors("Github Username :", 'b', 'ly'))
        if username:
            CONFIG.write_config('github', 'username', username)
    
    debug(username = username)
    
    #if not username and password:
    #    return create_repo_github()
    
    if not token:
        token = CONFIG.get_config('github', 'token', '2c5a2b2dbab79f8042c0b2ebdfb6c4a9fc0828b6')
    
    client_id = CONFIG.get_config('github', 'client_id', 'bcc0c5253f5a43845355')
    client_secret = CONFIG.get_config('github', 'client_secret', '264e42f7ecff43665d0c948edee04d1d54eea9ea')

    debug(username = username)
    debug(token = token)
    if token:
        g = Github(token)
    
    auth = g.get_user()
    dtype = ''
    if private:
        dtype = 'private'
    FOUND = False
    for i in auth.get_repos(type = dtype, sort = sort):
        if name:
            if isinstance(name, list):
                for n in name:
                    if as_is:
                        if n.lower() == i.name.lower():
                            print(make_colors("FOUND:", 'lw', 'lr') + " " + make_colors(i.name, 'lw', 'bl'))
                            FOUND = True
                    else:
                        if n.lower() in i.name.lower() or n.lower() == i.name.lower():
                            print(make_colors("FOUND:", 'lw', 'lr') + " " + make_colors(i.name, 'lw', 'bl'))
                            FOUND = True
            else:
                if as_is:
                    if name.lower() == i.name.lower():
                        print(make_colors("FOUND:", 'lw', 'lr') + " " + make_colors(i.name, 'lw', 'bl'))
                        FOUND = True
                else:
                    if name.lower() in i.name.lower() or name.lower() == i.name.lower():
                        print(make_colors("FOUND:", 'lw', 'lr') + " " + make_colors(i.name, 'lw', 'bl'))
                        FOUND = True
        else:
            print(i.name)
    return FOUND
            
def check_repo():
    repo_name = ''
    if not checkRemoteName() and CONFIG.get_config('default', 'repo') == 'github': # if nor origin is exists and set origin to github
        repo_name = create_repo_github()
        if isinstance(repo_name, bool) and repo_name == True:
            repo_name = os.path.basename(os.getcwd())
        if repo_name:
            user = re.split("@", CONFIG.get_config('github', 'username'))[0]
            debug(user = user)
            if user:
                add = "origin;" + 'https://github.com/{0}/{1}'.format(user, repo_name)
                controlRemote(add = add, interactive = True)
        os.system(GIT_BIN + " remote -v")
        return True
    else:
        while not checkRemoteName():
            add = None
            origin = raw_input(make_colors("Remote Origin URL [type 'github' or 'github:private/public' for Github or e[x]it|[q]uit]: ", 'lw', 'lr'))
            if origin == 'github':
                create_repo_github()
            elif ":" in origin and 'github' in origin:
                rn, rt = origin.split(":")
                rn = rn.strip()
                if rt:
                    rt = rt.strip()
                if rt == 'private':
                    create_repo_github(private = True)
                elif rt == 'private':
                    create_repo_github(private = False)
                else:
                    create_repo_github(private = True)
            if origin:
                if not repo_name:
                    repo_name = os.path.basename(os.getcwd())
                if origin == 'github':
                    user = re.split("@", CONFIG.get_config('github', 'username'))[0]
                    add = "origin;" + 'https://github.com/{0}/{1}'.format(user, repo_name)
                else:
                    add = "origin;" + origin
                controlRemote(add = add, interactive = True)
                os.system(GIT_BIN + " remote -v")
                return True
            elif origin == 'exit' or origin == 'quit' or origin == 'x' or origin == 'q':
                os.system(GIT_BIN + " remote -v")
                sys.exit()
    return False

def usage():
    __help__ = make_colors("By Default if will commit with version ~ datetime if no options given", 'w','r', attrs=['italic'])
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-f', '--github-find', action = 'store', help = 'Find remote repository name on github, type "all" to show all repository')
    parser.add_argument('-C', '--create', action = 'store', help = 'Create remote repository type: github for automactly create repo to github with username store on config file or type: REMOTE_NAME:URL_REMOTE for create another remote repo or for github may type: github:REPO_NAME:PUBLIC/PRIVATE or github:REPO_NAME:PUBLIC/PRIVATE:USERNAME for public or private repository with default github repo is private mode')
    parser.add_argument('-fp', '--github-find-private', action = 'store_true', help = 'Set find private for Find remote repository name on github')
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
    parser.add_argument('-sr', '--show-remote', action='store_true', help='Show all of remote Repository')
    parser.add_argument('-vv', '--show-remote-dir', action='store', help='Show all of remote Repository by given spesific directory path')
    parser.add_argument('-i', '--change-remote', action='store_true', help='Change remote Current Repository')
    parser.add_argument('-ii', '--change-remotes', action='store', help='Change remote given input REMOTE_NAME;REMOTE_URL it can be done with many times, for using with spesific dir use with: --change-remote-dir', nargs='*')
    parser.add_argument('-iii', '--change-remote-dir', action='store', help='Change remote by given spesific directory path', nargs='*')
    parser.add_argument('-nv', '--no-version', action='store_false', help='Don\'t Generate version of this program/project')
    parser.add_argument('-nt', '--no-time', action='store_false', help='Don\'t Generate Comment time of this program/project')
    parser.add_argument('-m', '--message', action='store', help='comment if --no-version')
    parser.add_argument('-g', '--get', action='store_true', help='get origin remote repo name and copy to clipboard')
    parser.add_argument('-d', '--dir', action='store', help='Change dir to')
    parser.add_argument('--set-private', action = 'store_true', help='Set github repository as Private')
    parser.add_argument('--set-public', action = 'store_true', help='Set github repository as Public')
    parser.add_argument('-V', '--version', action='store_true', help='Show version of this program/project')
    parser.add_argument('-v', '--set-version', action = 'store', help = 'Set Version for commit')
    print(__help__)
    if len(sys.argv) == 1:
        check_repo()
        commit()
        pushs()
        # parser.print_help()
    elif len(sys.argv) == 2 and os.path.isdir(sys.argv[1]):
        os.chdir(sys.argv[1])
        check_repo()
        commit()
        pushs()
        sys.exit()        
    elif len(sys.argv) == 2 and sys.argv[1] == '--no-push' or sys.argv[1] == '-np':
        commit(no_push=True)
    else:
        args = parser.parse_args()
        if args.set_private:
            edit_repo_github(private=True)
        elif args.set_public:
            edit_repo_github(private=False)
        if args.dir and len(sys.argv[1:]) == 2:
            os.chdir(args.dir)
            check_repo()
            commit()
            pushs()
            sys.exit()
        if args.get:
            origin = getOrigin()
            if isinstance(origin, str):                
                clipboard.copy(origin)
            if isinstance(origin, list):
                print(make_colors("No repo origin found !", 'lw', 'lr', ['blink']))
                if len(origin) > 0:
                    n = 1
                    for i in origin:
                        print(str(n) + ". " + make_colors(i, 'lw', 'bl') + ":" + make_colors(origin.get(i), 'lw', 'm'))
                    qr = raw_input("select you want copy to")
                    if qr and qr.isdigit() and not len(int(str(qr).strip())) > len(origin):
                        clipboard.copy(origin.get(origin.key()[int(qr) - 1]))

        if args.github_find:
            check_repo_github(args.github_find, args.github_find_private, as_is = False)
            sys.exit()
        if args.push:
            pushs()
        if args.create:
            create_repo(args.create)
        if args.pushs:
            for i in args.pushs:
                pushs(i)
        if args.version:
            print("VERSION     :", getVersion())
            print("NEXT VERSION:", getVersion(False, False))
        if args.check:
            #commit(no_push = False, check=False, commit=True, push_version=False, with_time=True, comment=None):
            commit(check=args.check)
        elif args.check_dir:
            for i in args.check_dir:
                if os.path.isdir(i):
                    print(make_colors("REPOSITORY: ", 'lm') + make_colors(os.path.dirname(i) + "\\", 'ly') + make_colors(os.path.basename(i), 'w', 'bl', attrs=['bold','italic']))
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

        if args.commit or args.set_version:
            commit(no_push = args.no_push, check=False, commit=True, push_version=args.no_version, with_time=args.no_time, comment=args.message, version = args.set_version)
        elif args.commit_dir:
            for i in args.check_dir:
                if os.path.isdir(i):
                    os.chdir(i)
                    commit(no_push = args.no_push, check=False, commit=True, push_version=args.no_version, with_time=args.no_time, comment=args.message)

if __name__ == '__main__':
    print("PID =", pid)
    # print "checkFileVersion() =", checkFileVersion()
    # print "VERSION:", getVersion()
    # controlRemote()
    usage()
    #check_repo_github('nime')
    #print(checkRemoteName())
    # print "VERSION =", getVersion(check=True, write=False, step=0.01, test=False)
    
