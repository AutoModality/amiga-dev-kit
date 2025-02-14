---
id: brain-apps
title: Developing Custom Applications
---

# Developing Custom Applications

#### Quick Tips
* The Amiga user is able to install APT packages. Edit the "entry.sh" script in the sample git repository.
* We leverage a venv per application. The contents of requirements.txt will be installed by the bootstrap.sh script.
* If you've updated the requirements.txt remove the hidden ".lock" before relaunching the app from the Brain UI.
* You may use VSCode remote development/containers to edit directly on the Amiga brain as well.


#### Initial Configuration
To make ssh easier, we'll add some configuration to our ssh on the workstation.

First add the following to your .ssh/config utilizing the IP addess displayed on the bottom right of the brain display:
```bash
Host amiga
    HostName <ip address>
    Port 22
    User amiga
    StrictHostKeyChecking no
```

Let’s copy our keys to the robot as well (you may need to do this any time you are working with a new robot)
```bash
    ssh-copy-id amiga
```

Now you can ssh to the robot with:
```bash
    ssh amiga
    exit
```

Open the "Hello World" workspace by ... You may use an alternate editor of your choice. If you do, the sample application for publishing an app is located at amiga-dev-kit/brain/examples/hello

Using a terminal window, change to the git repository file cloned above.

#### Live Code Syncing

Now we'll start a synchronization session that will mirror the code in this directory to an Apps directory (/data/apps) on the Amiga Brain. Note: This directory is persistent across reboots.

Our current sync process leverages Mutagen, the sync.sh script will set this up for you. Please provide your sudo password if required. This will copy the Mutagen binary and agents to your local filesystem.
Additional documentation regarding Mutagen may be viewed at: [Mutagen](https://mutagen.io/documentation/introduction).

To start the synchronization process in the background:
```bash
    ./sync.sh -s start
```

To stop the synchronization process:
```bash
    ./sync.sh -s stop
```

Finally to view the status:
```bash
    ./sync.sh -s status
```

While the sync process is running, any changes are mirrored to the Amiga Brain.

To test this process out, now that the current directory amiga-dev-kit/brain/examples/hello is being synchronized to your brain, lets trigger a refresh of the currently loaded apps by clicking on the "home" icon near the top right.

Click on the new app labeled "Hello" on the Amiga Brain. After a brief moment (bootstrapping the app) the app wil load and you'll be greeting a a simple UI app. Close the app by clicking "Exit".

On your workstation, open the "main.py" file in an editor and change the value for YOUR_NAME to be your name (i.e. joe dirt). Save the file and relaunch the app from the Amiga Brain. The text will now reflect your changes.
