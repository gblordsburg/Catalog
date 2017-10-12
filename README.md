This is the README.md file for the Item Catalog project

For this project a virtual machine(VM) and data are needed and a Unix-style terminal will be used to run the DB app.

The VM is run by software named Virtualbox and a software named Vagrant configures the VM and allows for files to be shared between your system and the VM filesystem.

Install VirtualBox and Vagrant.

Download VM configuration by either:

        **Note: either option will give you a new directory named FSND-Virtual-Machine that contains the VM files.

        Downloading and unzipping this file: https://d17h27t6h515a5.cloudfront.net/topher/2017/May/59125904_fsnd-virtual-machine/fsnd-virtual-machine.zip.

        Using GitHub fork from the repository: https://github.com/udacity/fullstack-nanodegree-vm.


To obtain the application via zip file:
    - download the zip file copy and unzip into /FSND-Virtual-Machine/vagrant directory.

To obtain the application via git clone:

    -visit github.com/gblordsburg and copy clone address to your clipboard.

    -cd into the /FSND-Virtual-Machine/vagrant directory and run git clone https://github.com/gblordsburg/Item-Catalog

The data used for the project was in a file named db_populator.py and is a modified version of a database populator file from Udacity Fullstack Nanodegree Backend: Databases & Applications lessons and placed inside the application folder.

Open terminal (e.g. Git Bash) to run the app.

cd to the directory containing the VM files, then cd to the vagrant directory.

Start the VM by running the command "vagrant up" from the vagrant directory, then run "vagrant ssh" to log in to the VM.

Once logged in, cd to the shared files location: cd /vagrant/.

cd to the Item-Catalog directory that contains the DB python file (named catalog2.py) to run.

To CREATE the database, populate it with data, and THEN run the application:

    -run db_setup2.py to set up database and create tables

    -run db_populator.py to add the necessary data to the tables

    -run catalog2.py, open browser and go to localhost:5000/


To just run the application:

    -run catalog2.py, open browser and go to localhost:5000/

To close the application just close the browser window, reopen terminal window and stop the application with cntrl-c, log out of VM with cntrl-d, close terminal.
