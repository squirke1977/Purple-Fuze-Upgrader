Upgrading to Purple Fuze
---

We're in the middle of upgrading to the new **Purple** (version 17) [Fuze for rooms client.](https://www.fuze.com/products/fuze-rooms)

In our meeting rooms we've been spawning the Fuze for Rooms product with a LaunchDaemon - so that if anyone quits the application, it'll relaunch. Great for meeting room availability, not so good for being able to upgrade the app.

This script is designed to check for two things...

* Has Fuze version 17 (Purple) been installed?
* has a package containing login/configuration been installed?

If the answer to one (or both) of these questions is no, the script will:

* Unload the LaunchDaemon keeping Fuze running
* Quit the Fuze application
* Run Munki to update Fuze/Fuze configuration pacakges
* reload the Fuze LaunchDaemon
* Unload the script's own LaunchDaemon

At least, that's the general idea.
