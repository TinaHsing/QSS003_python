2-4.	程式介紹:
	C12880.so：
	控制 C12880 與 LED 的副程式（無法編輯）

	QSS003.py：
	可攜式主程式，存檔為 black.txt 與 data_0.txt、data_1.txt ……
	需要讀取setting.txt，如果沒有setting.txt，LCD 將顯示：setting.txt not found
	setting.txt 欄位說明（不要寫括號）：
	25	(mA)		set LED driver1 current to setting mA
	25	(mA)		set LED driver2 current to setting mA
	25	(mA)		set LED driver3 current to setting mA
	3	(s)		set LED delay time
	100	(us)		set C12880 int time

	QSS003_desktop.py：
	桌上型主程式，存檔為 black.txt 與 desktop_0.txt、desktop_1.txt ……
	執行方式：
	python3 QSS003_desktop.py [led1_current] [led2_current] [led3_current] [led_stable_time] [int_time]
	範例：python3 QSS003_desktop.py 25 25 25 3 100	

	ShowIP.py
	開機自動執行 ShowIP.py，將樹梅派的 IP address 顯示於 LCD 上

2-5.	設定開機自動執行 QSS003.py
	修改 /etc/rc.local
	在exit 0 之前添加執行命令
	sudo -u pi python3 /home/pi/QSS003_python/QSS003.py

	切勿同時執行兩個 QSS003.py 或 QSS003_desktop.py
	檢查相關背景程式：
	ps aux | grep QSS003

	如果 QSS003.py 已經在背景執行，
	請先修改 rc.local 關閉自動執行，再重新開機。

2-6.	關閉自動執行 QSS003.py
	修改 /etc/rc.local
	將
	sudo -u pi python3 /home/pi/QSS003_python/QSS003.py
	改為
	#sudo -u pi python3 /home/pi/QSS003_python/QSS003.py

