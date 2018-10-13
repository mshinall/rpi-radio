#!/usr/bin/bash

sudo apt-get install \
	rtl-sdr \
	sox \
	alsa \
	cmake \
	libusb

pip install \
	sys \
	pad4pi \
	time \
	subprocess \
	os \
	signal \
	shlex

#git clone https://github.com/osmocom/rtl-sdr.git
#cd rtl-sdr
#cmake ../ -DINSTALL_UDEV_RULES=ON
#make
#sudo make install

git clone https://github.com/sysrun/rtl-sdr.git
cd rtl-sdr
cmake ../ -DINSTALL_UDEV_RULES=ON -DDETACH_KERNEL_DRIVER=ON
make
sudo make install
