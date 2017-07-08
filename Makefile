USE_PKGBUILD=1
include /usr/local/share/luggage/luggage.make
TITLE=Purple_Fuze_upgrader
PACKAGE_VERSION=1.3
REVERSE_DOMAIN=com.thoughtworks
PAYLOAD=\
	pack-script-preinstall\
	pack-script-postinstall\
	pack-Library-LaunchDaemons-com.zerowidth.launched.purple_fuze.plist\
	pack-fuze_upgrade_script

pack-fuze_upgrade_script: l_usr_local_bin
	@sudo ${CP} fuze_version_checker.py ${WORK_D}/usr/local/bin/
