#!/usr/bin/env bash

# exit on any command failure 
# or usage of undefined variable 
# or failure of any command within a pipaline
set -euo pipefail


# install postgres


# uncomment these lines if you need to ensure this runs under root/sudo
if [ "$EUID" -ne 0 ]
	then echo "Please run as root"
	exit 1
fi


apt-get update
apt-get install -y postgresql postgresql-contrib
