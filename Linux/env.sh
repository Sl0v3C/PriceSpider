#!/bin/bash

OS_VER=`cat /etc/issue | awk '{print $2}'`
echo "Your OS version is $OS_VER"
ARCH=`uname -m`

VAR=${OS_VER#12.04}
AA=${ARCH#x86_64}

if [ "$VAR" != "" ]; then
    echo "Your OS version is Ubuntu 12.04"
    # install python3.4
    sudo apt-get install python-software-properties 
    sudo add-apt-repository ppa:fkrull/deadsnakes #添加ppa源
    sudo apt-get update; sudo apt-get install python3.4

    # install pip
    curl -O https://bootstrap.pypa.io/get-pip.py
    sudo python3.4 get-pip.py
else
    VAR=${OS_VER#1[3|4|5|6].04}
    if [ "$VAR" != "" ]; then
        sudo apt-get install python3-pip
    fi  
fi

sudo pip install --upgrade pip
sudo pip install --upgrade virtualenv

#2. selenium
sudp pip3 install selenium

#3. requests & lxml
sudo pip3 install requests lxml

#4 webdriver needs
if [ "$AA" != "" ]; then # AA64
    # geckodriver v0.18 for Firefox 56 and greater
    sudo mv A64/geckodriver /usr/local/bin
    # chromdriver v2.30 Supports Chrome v58-60
    sudo mv A64/chromedriver /usr/local/bin
    # run the price spider
    python3.4 process.py
else # X86
    # geckodriver v0.18 for Firefox 56 and greater
    sudo mv X86/geckodriver /usr/local/bin
    # chromdriver v2.30 Supports Chrome v58-60
    sudo mv X86/chromedriver /usr/local/bin
    # run the price spider
    python3 process.py
fi
    
