---
title: ClamAV
---

#### Install clamav
```
sudo apt-add-repository ppa:ubuntu-clamav/ppa
sudo apt-get install clamav
```


#### Disable update service
```
sudo update-rc.d clamav-freshclam disable
```


#### Stop update service
```
sudo /etc/init.d/clamav-freshclam stop
```


#### Update clamav
```
sudo freshclam
```


#### Scan system
```
mkdir $HOME/Desktop/infected; sudo clamscan -r --bell -i --move=$HOME/Desktop/infected --exclude-dir=$HOME/Desktop/infected / &> $HOME/Desktop/infected/scan.txt
```
