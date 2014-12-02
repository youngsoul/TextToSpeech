#!/bin/sh


# ssh-keygen
# cat ~/.ssh/id_rsa.pub
# copy ssh key into github account.
# mkdir dev;cd dev
# git clone git@github.com:youngsoul/TextToSpeech.git
# chmod +x setup.sh

sudo raspi-config


#Install Packages:
sudo apt-get --yes update
sudo apt-get --yes upgrade
sudo apt-get --yes --force-yes install python-pip
sudo apt-get install mpg123
sudo pip install requests
sudo apt-get install python-feedparser

# no longer used
#sudo apt-get install festival

# create a ram filesystem
# http://www.thegeekstuff.com/2008/11/overview-of-ramfs-and-tmpfs-on-linux/
#<device> <mountpoint> <filesystemtype><options> <dump> <fsckorder>
sudo mkdir -p /mnt/ram
echo "ramfs /mnt/ram ramfs nodev,nosuid,noexec,nodiratime,size=64M 0 0" | sudo tee -a /etc/fstab
# so we do not have to run the scripts with sudo just open up the /mnt/ram mount
sudo chmod 0777 /mnt/ram

#sudo apt-get --yes --force-yes install netatalk


