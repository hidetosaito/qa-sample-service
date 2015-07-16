# QA Sample Service
==

## Before you start
* Install docker. If you're using MacOS or Windows, you'll need [Boot2docker](http://boot2docker.io/) or [Vagrant](https://www.vagrantup.com/)

## Create your dev environment on local
* Normally you'll need [virtualenv](https://virtualenv.pypa.io/en/latest/) to isolate the development environment.
* You could use below command to install related packages
	```
	pip install -r requirements.txt
	```
	or 
	```
	python setup.py develop
	```
* export `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables
* Run the application by
	```
	python entry.py
	```
	
## Create your dev environment by Docker
### Before you start
* Install docker. If you're using MacOS or Windows, you'll need [Boot2docker](http://boot2docker.io/) or [Vagrant](https://www.vagrantup.com/)
### Setup 
* Beware! If you're using Boot2docker or Vagrant, please note that you'll need to sync the timezone between it and your host machine; otherwise, AWS authentication will be fail. One simple way to sync Boot2docker and MacOS is running `/usr/local/bin/boot2docker ssh sudo ntpclient -s -h pool.ntp.org` before you start the container.
* Go the the source code folder
* Build your docker image. Here we'll use sample-service as our image name tag
	```
	docker build -t sample-service .
	```
* Run your container

	```
docker run -d -p 49160:5000 -e APP_SETTING=config.DevelopmentContainerConfig  -e AWS_ACCESS_KEY_ID=$mykey -e AWS_SECRET_ACCESS_KEY=$mysecret --name sample sample-service
	```
	- You'll need to use either IAM role or set env variables for connecting to AWS services. If you are in your local machine. Using -e to setup the env variables in container
	- APP_SETTING is the variable you could set for changing the configuration setting in flask. For the different configuration setting, please refer to config.py. Flask listens to localhost by default, if you want it listen to network, change the default setting to `config.DevelopmentContainerConfig`
	- The default expose port is 5000, if you want to change it, using `-p ${host_port}:${container_port}` to change
	

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