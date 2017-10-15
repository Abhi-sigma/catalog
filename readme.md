
# Project Synopsis

This is the fourth project and is a requirement for  Udacity Full Stack Developers Nanodegree.The project uses python on
the backend with flask framework and sql lite as the database.Flask Sql Alchemy is used for manipulating databases.
The project requires a login system using third party apis, create,edit and delete functions when logged in,json endpoints
and implements local permission systems.for eg:only creator of a item can modify or delete a project.


## Running the Project:

Requirements:
+ **Virtual Box**
+ **Vagrant**
+ **Bash terminal(for windows machine)**


## Installation:
(Recommended Method)

1. If you are using a Mac or Linux system, your regular terminal program will do just fine.On Windows,
use the Git Bash terminal that comes with the Git software.
If you don't already have Git installed, download Git from [here](git-scm.com).

2. VirtualBox is the software that actually runs the virtual machine. You can download it from virtualbox.org, [here](https://www.virtualbox.org/wiki/Downloads).
Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need
to launch VirtualBox after installing it; Vagrant will do that.

	<strong>Note to Ubuntu users:
	If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center instead.
	Due to a reported bug, installing VirtualBox from the site may uninstall other software you need.</strong>

3. Vagrant is the software that configures the VM and lets you share files between your host computer
and the VM's filesystem. Download it from (vagrantup.com). Install the version for your operating system.

Windows users: The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.


4. You can download and unzip this file: [here](https://d17h27t6h515a5.cloudfront.net/topher/2017/June/5948287e_fsnd-virtual-machine/fsnd-virtual-machine.zip)
This will give you a directory called FSND-Virtual-Machine.
It may be located inside your Downloads folder.Alternately, you can use Github to fork and
clone the repository from this [repository](https://github.com/udacity/fullstack-nanodegree-vm). Either way,
you will end up with a new directory containing the VM files. Change to this directory in your terminal with cd.
Inside, you will find another directory called vagrant. Change directory to the vagrant directory:

5. Once you get your terminal(which may take quite a while) depending on your internet speed.Type `vagrant up`

6. SSH into virtual machine by typing `vagrant ssh`.

7. change directory to `cd /vagrant/`

8. cd into vagrant directory and type `git clone https://github.com/Abhi-sigma/catalog`.

This will clone the catalog git diretory into the vagrant directory.cd into this directory and type `python main.py`.If everything in followed
in correct order,you will be able to run the project by typing `http://localhost:5000`.At this instance,the database is empty.Now,
to test the project we have two options.


### 1.Run the tester.py
  When this python file is run,it connects to database seperately and inserts user "test1" and category
  "Bedroom" and items "Chairs","Tables" and "Bed" under the Bedroom category and makes user test1 as the owner of these database entries.
  You will be able to see that you cant modify items created by test1.Now,you can add your own items and category and observe
  that you can modify and delete the items that you have created.When you want to remove the items and user created by
  test1,run the tester.py again.It will simply delete everything related to user test1 including itself.Read through the tester.py
  documentation and comments to learn more how it works.

  <strong>Caution:When you run tester.py second time,it will delete Bedroom category,so if you have added anything in
  that category,it will be deleted too. </strong>

  <strong>Caution:Your local flask server may stop when you run tester.py so if you get error in connection,try running the main.py again.</strong>

 ### 2.Login to both facebook and google:
 Your email id is your identification when you create anything in catalog website.The facebook login api doesnt let access email
 when running from local host.So,in development,if you login by facebook your email id is saved as "user name"+@test.com.So even
 if you have same email id for both facebook and google,you are two different users.That code needs to be changed before deploying
 and then if you have same email address for facebook and google,you are the same person.

 ## JSON endpoints
 The catalog web api exposes three json endpoints namely:

 + host/catalog/json:
 This json enpoint returns all the items present in catalog_item table along with the catalog name from where it belongs.

 + host/get_all_categories
 This json endpoint exposes all the categories with their respective id.

 + host/catalog/<category>/json
 	This json enpoint returns all the items from a category.
 	For eg:localhost:5000/catalog/Bedroom/json will return all the items in Bedroom.
**replace host with localhost:5000 if you are following the instructions and no changes made in running the app.for e.g
localhost:5000/catalog/Bedroom/json**



