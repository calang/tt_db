# Description

# variable definitions, available to all rules
REPO_ROOT := $(shell git rev-parse --show-toplevel)  # root directory of this git repo
BRANCH := $(shell git branch --show-current)
# BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
# Notes:
# all env variables are available
# = uses recursive substitution
# :=  uses immediate substitution

# ENV_NAME is second word, separated by one space, in file env.yml
ENV_NAME := $(shell head -1 env.yml | cut -d ' ' -f 2)


# target: help - Display callable targets.
help:
	@echo "Usage:  make <target>"
	@echo "  where <target> may be"
	@echo
	@egrep -h "^# target:" [Mm]akefile | sed -e 's/^# target: //'


# # target: .venv - create local venv
# .venv:	ALWAYS
# 	python3 -m venv .venv
# 	. .venv/bin/activate; pip install --upgrade pip

# target: requirements - install/update python required packages
requirements:	ALWAYS
	pip install --upgrade -r requirements.txt

# target: update-env - update conda environment based on latest content of environment.yml file
update-env:
	conda env update -f env.yml

# target: rm-env - update conda environment based on latest content of environment.yml file
rm-env:
	conda env remove -n ${ENV_NAME}

# target: jupl - start jupiter lab server
jupl:	ALWAYS
	jupyter lab &


# target push - sample docker image push, asking for passwords
# push: TEMPUSR := $(shell mktemp)
# push:
#	@$$SHELL -i -c 'read -p "username: " user;  echo -n $${user} >$(TEMPUSR)'
#	@$$SHELL -i -c 'read -s -p "password: " user;  echo -n $${user} >$(TEMPUSR)1'
#	@docker login -u $$(cat $(TEMPUSR)) -p $$(cat $(TEMPUSR)1) amr-registry.caas.intel.com
#	docker image push ${APP_IMAGE}
#	@rm $(TEMPUSR)*

# 	@rm $(TEMPUSR)*

# ignore files with any of these names
# so that the rules with those as target are always executed
.PHONY: ALWAYS

# always do/refresh ALWAYS target
ALWAYS:
