#package this up
#Script to /usr/local/bin
#launchD to /Lib/LaunchDaemons
#postinstall script to load and RUN this launchD??

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

logged_in_username = (SCDynamicStoreCopyConsoleUser(None, None, None) or [None])[0]

#Move all the variables here and make them global?

unload_this_launchdaemon_command = ['/bin/launchctl', 'unload', '/Library/LaunchDaemons/com.zerowidth.launched.purple_fuze.plist']
remove_this_launchdaemon_command = ['/bin/rm', '/Library/LaunchDaemons/com.zerowidth.launched.purple_fuze.plist']

pause_persistent_fuze_command = ['/bin/launchctl', 'unload', '/Library/LaunchDaemons/com.thoughtworks.ws.persistentFuze.plist']
restart_persistent_fuze_command = ['/bin/launchctl', 'load', '/Library/LaunchDaemons/com.thoughtworks.ws.persistentFuze.plist']
quit_fuze_command = ['/usr/bin/killall', '-TERM',  'Fuze']
run_munki_command = ['/usr/local/munki/managedsoftwareupdate', '--installonly', '--munkipkgsonly']

#Test this script again at the login Window
if logged_in_username == None:
    print "We're at the login window - nothing for this script to do here"
    exit(1)
else:
    print logged_in_username
    fuze_version = find_major_version('/Applications/Fuze.app/')
    if fuze_version >= 17 and os.path.exists('/Users/Shared/Fuze/'):
        print "already upgraded to Purple Fuze including authentication data!"
        subprocess.check_output(unload_this_launchdaemon_command)
        subprocess.check_output(remove_this_launchdaemon_command)
    else:
        subprocess.check_output(pause_persistent_fuze_command)
        subprocess.check_output(quit_fuze_command)
        subprocess.check_output(run_munki_command)
        subprocess.check_output(restart_persistent_fuze_command)
        subprocess.check_output(unload_this_launchdaemon_command)
