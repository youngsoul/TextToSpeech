#!/bin/sh


# ssh-keygen
# cat ~/.ssh/id_rsa.pub
# copy ssh key into bitbucket account.
# mkdir dev;cd dev
# git clone git@github.com:youngsoul/TextToSpeech.git
# chmod +x setup.sh

sudo raspi-config


#Install Packages:
sudo apt-get --yes update
sudp apt-get --yes upgrade

sudo apt-get install python-feedparser mpg123 festival
sudo apt-get install requests

# create a ram filesystem
# http://www.thegeekstuff.com/2008/11/overview-of-ramfs-and-tmpfs-on-linux/
sudo mkdir -p /mnt/ram
echo "ramfs /mnt/ram ramfs nodev,nosuid,noexec,nodiratime,size=64M 0 0" | sudo tee -a /etc/fstab

sudo apt-get --yes --force-yes install netatalk


