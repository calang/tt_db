#!/usr/bin/env bash

# exit on any command failure 
# or usage of undefined variable 
# or failure of any command within a pipaline
set -euo pipefail


# setup the postgresql DB


# uncomment these lines if you need to ensure this runs under root/sudo
if [ "$EUID" -ne 0 ]
	then echo "Please run as root"
	exit 1
fi


echo "Creating user calang"
sudo -u postgres createuser --superuser calang

echo "Creating database tt"
# -u postgres (used with sudo):
# Runs the command as the postgres system user,
# which has permission to manage PostgreSQL roles and databases.
# -O calang (used with createdb):
# Specifies that the new database should be owned by the PostgreSQL role/user calang.
sudo -u postgres createdb -O calang tt
