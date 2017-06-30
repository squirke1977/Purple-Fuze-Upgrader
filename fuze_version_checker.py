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
root_command = ['touch', '/Users/Shared/root_was_ere']

pause_persistent_fuze_command = ['/bin/launchctl', 'unload', '/Library/LaunchDaemons/com.thoughtworks.ws.persistentFuze.plist']
restart_persistent_fuze_command = ['/bin/launchctl', 'load', '/Library/LaunchDaemons/com.thoughtworks.ws.persistentFuze.plist']
quit_fuze_command = ['/usr/bin/killall', '-TERM',  'Fuze']
run_munki_command = ['/usr/local/munki/managedsoftwareupdate', '--auto', '--munkipkgsonly']

#Test this script again at the login Window
if logged_in_username == None:
    print "hello root"
    root_command = ['touch', '/Users/Shared/root_was_ere']
    subprocess.check_output(root_command)
    exit(1)
else:
    print logged_in_username
    fuze_version = find_major_version('/Applications/Fuze.app/')
    if fuze_version >= 17 and os.path.exists('/Users/Shared/Fuze/'):
        print "already upgraded hurrah!"
        subprocess.check_output(unload_this_launchdaemon_command)
        subprocess.check_output(remove_this_launchdaemon_command)
    else:
        subprocess.check_output(pause_persistent_fuze_command)
        subprocess.check_output(quit_fuze_command)
        subprocess.check_output(run_munki_command)
        subprocess.check_output(restart_persistent_fuze_command)
        subprocess.check_output(unload_this_launchdaemon_command)

    #UNLOAD/REMOVE LaunchD??? - or just unload - so this can re-run post reboot?

if fuze_version >= 17 and os.path.exists('/Users/Shared/Fuze/'):
#    subprocess.check_output(root_command)
    print "you have new Fuze I can delete myself"
elif fuze_version >= 17:
    print "you have new fuze but no auth data"
#    subprocess.check_output(root_command)
else:
    print "old Fuze = fake news"
