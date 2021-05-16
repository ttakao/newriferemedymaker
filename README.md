# newriferemedymaker
For driving "New Rife Frequency Therapy Remedy Maker V.1" on Windows PC.

Prerequisite

- Python V3
- PIP3
- PyUSB (pip install pyusb)
- EasyGUI (pip install easy_gui)
- LIBUSB (In case of AG-051F, install "WaveForm Generator")

When installing LIBUSB, please check this document.(http://files.owon.com.cn/software/Application/AG_Series_USB_Driver_Install_Guide.pdf)

Setup
1.Download all files into adequate folder.
2.'freq_list.zip' also unzip in the adequate folder.
3.Install LIBUSB
4.Install PyUSB and EasyGUI
5.Connect function generator such as AG-051F
6.Run 'FindDev.py' for finding vender ID an product ID
7.Review 'config.ini'
8.Run 'rifemaker16e.py'
9.You can choose Rife frequency list from 'freq_list' folder.
