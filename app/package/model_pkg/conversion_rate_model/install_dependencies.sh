#! /bin/sh

# script to install Linux dependencies required by python package
# Dmitry Kisler © 2019
# www.dkisler.com

pkgs=$1

if [ ! -f /etc/os-release ]; then
  echo "Unrecognized OS"; exit 1
fi

OS_ID=$(cat /etc/os-release | grep -i "^id=" | awk -F "=" '{print $2}' | sed 's/"//g')

if [ ! $? -eq 0 ]; then
  echo "Unrecognized OS"; exit 1
fi

debian () {
  apt-get update -y \
  && apt-get install $1 -y
}

centos () {
  yum update -y \
  && yum install $1 -y
}

alpine () {
  apk update \
  && apk add $1
}

case "${OS_ID}" in
    alpine*)  alpine ${pkgs} ;;
    debian*)  debian ${pkgs} ;;
    ubuntu*)  debian ${pkgs} ;;
    centos*)  centos ${pkgs} ;;
    *)        echo "Unrecognized OS"; exit 1 ;;
esac