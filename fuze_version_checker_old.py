import os
import subprocess
import shutil
from SystemConfiguration import SCDynamicStoreCopyConsoleUser

def find_major_version(path_to_application):
    sw_version_command = ['mdls', '-name', 'kMDItemVersion', path_to_application]
    version_data = subprocess.check_output(sw_version_command)
    version_data = version_data.split('"')
    versions = version_data[1]
    versions = versions.split(".")
    major_version = int(versions[0])
    return major_version

fuze_version = find_major_version('/Applications/Fuze.app/')
#major_version = 19

print fuze_version

logged_in_username = (SCDynamicStoreCopyConsoleUser(None, None, None) or [None])[0]

if logged_in_username == None:
    print "hello root"
    exit(1)
else:
    print logged_in_username
    fuze_version = find_major_version('/Applications/Fuze.app/')
    #fuze_version = 16
    if fuze_version >= 17 and os.path.exists('/Users/Shared/Fuze/'):
        #unload and delete launchD and this file?
        print "already upgraded hurrah!"
    else:
        pause_persistent_fuze_command = ['/bin/launchctl', 'unload', '/Library/LaunchDaemons/com.thoughtworks.ws.persistentFuze.plist']
        restart_persistent_fuze_command = ['/bin/launchctl', 'load', '/Library/LaunchDaemons/com.thoughtworks.ws.persistentFuze.plist']
        quit_fuze_command = ['/usr/bin/killall', '-TERM',  'Fuze']
        run_munki_command = ['/usr/local/munki/managedsoftwareupdate', '--auto', '--munkipkgsonly']
        subprocess.check_output(pause_persistent_fuze_command)
        subprocess.check_output(quit_fuze_command)
        subprocess.check_output(run_munki_command)
	subprocess.check_output(restart_persistent_fuze_command)

print logged_in_username

if fuze_version >= 17 and os.path.exists('/Users/Shared/Fuze/'):
#    subprocess.check_output(root_command)
    print "you have new Fuze I can delete myself"
elif fuze_version >= 17:
    print "you have new fuze but no auth data"
#    subprocess.check_output(root_command)
else:
    print "old Fuze = fake news"
