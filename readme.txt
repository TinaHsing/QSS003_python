開機自動執行 QSS003.py
1.修改rc.local文件
sudo nano /etc/rc.local
2.在exit 0 之前添加執行命令
sudo -u pi python3 /home/pi/QSS003_python/QSS003.py

*

關閉自動執行 QSS003.py
1.修改rc.local文件
sudo nano /etc/rc.local
2.修改
sudo -u pi python3 /home/pi/QSS003_python/QSS003.py
為
#sudo -u pi python3 /home/pi/QSS003_python/QSS003.py

*

查詢相關背景程式
ps aux | grep QSS003
ps aux | grep QSS003 | awk '{print $2}'

