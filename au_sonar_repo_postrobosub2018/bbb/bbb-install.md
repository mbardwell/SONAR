# BBB Install guide

## Easy Way
* Download the prebuilt [sonar image](https://drive.google.com/a/ualberta.ca/file/d/1wReoiDjcon2ny3Dl7qBWqaYGj9TlAKMU/view?usp=sharing) from Team Drive. 
* Use [etcher](http://etcher.io/) to install image on SDCard
* Login into BBB using debian:temppwd
* Make sure to `git pull` au_sonar repo to get the latest updates. 

## Hard Way 👷
### Write Linux Image 
* Download and install from [beaglebone](https://beagleboard.org/latest-images) of Debian for Beaglebone black (tested kernel: Debian 9.2 2017-10-10 4GB SD IoT). Extract it
```
wget https://debian.beagleboard.org/images/bone-debian-9.2-iot-armhf-2017-10-10-4gb.img.xz
unxz bone-debian-9.2-iot-armhf-2017-10-10-4gb.img.xz
```
* Use [etcher](http://etcher.io/) to install image on SDCard
* Login into BBB using debian:temppwd

### Setting up static IP Address (10.42.43.125)
Edit `/etc/network/interfaces` and add the following 
```
auto eth0
iface eth0 inet static
  address 10.42.43.125
  netmask 255.255.255.0
  gateway 10.42.43.1
```

### Update date (make sure you are connected to the internet)
```
sudo apt update
sudo apt install ntpdate
ntpdate -b -s -u pool.ntp.org
```

### Update kernel and bootloader (only works with 4.4 kernel)
```
sudo /opt/scripts/tools/update_kernel.sh --bone-kernel --lts-4_4
sudo /opt/scripts/tools/developers/update_bootloader.sh
sudo reboot
```

### Modify boot settings (modify _/boot/uEnv.txt_) and enable UIO PRUSS
* Disabled HDMI and Audio comment
```
disable_uboot_overlay_video=1
disable_uboot_overlay_audio=1
```
* Enable UIO instead of remote proc by uncommenting `uboot_overlay_pru=/lib/firmware/AM335X-PRU-UIO-00A0.dtbo` and comment any other lines under PRUSS Options
* Ensure Universal Cape is enabled (a.k.a uncommented)	
* Set UIO memory size (2097152) by appending `cmdline=` with `cmdline=... uio_pruss.extram_pool_sz=2097152`
* Reboot
* Check bootloader settings `sudo /opt/scripts/tools/version.sh`. If 
* Check UIO memory size `cat /sys/class/uio/uio0/maps/map1/size`

### Install PRU libraries and PASM
```
git clone https://github.com/beagleboard/am335x_pru_package.git
cd am335x_pru_package/pru_sw/app_loader/interface/
make CROSS_COMPILE=""
cd ../
sudo cp lib/* /usr/lib/
sudo cp include/* /usr/include/
cd ~
```
Building PASM
```
cd am335x_pru_package/pru_sw/utils/pasm_source/
./linuxbuild
cd ../
sudo cp pasm /usr/bin
cd ~
```

### Downloading and building this repo
```
git clone https://github.com/arvpUofA/au_sonar.git
cd au_sonar/bbb
make clean
make
```
