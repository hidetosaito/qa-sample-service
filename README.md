# QA Sample Service
==

## Before you start
* Install docker. If you're using MacOS or Windows, you'll need [Boot2docker](http://boot2docker.io/) or [Vagrant](https://www.vagrantup.com/). 


## Create your dev environment
* Beware! If you're using Boot2docker or Vagrant, please note that you'll need to sync the timezone between it and your host machine; otherwise, AWS authentication will be fail. One simple way to sync Boot2docker and MacOS is running */usr/local/bin/boot2docker ssh sudo ntpclient -s -h pool.ntp.org* before you start the container.

* Checkout the code from github and *cd* to qa-poc folder
* Build your docker image. Here we'll use my-qa as our image name tag
	```
	docker build -t my-qa .
	```
* Run your docker. 
* TBD

## API Call Test
TBD

## Run Test
* Run unit tests  
	- By default
	
	```
	python setup.py test
	```
	- By nose
	
	```
	nosetests [--nocapture]
	```
* Run a single unit test 

	```
	nosetests -v $test_file [--nocapture]
	```