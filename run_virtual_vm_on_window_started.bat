# 将此文件`run_virtual_vm_on_window_started.bat`放到C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp
cd C:\Program Files\Oracle\VirtualBox

echo "starting ubuntu ......"
# ubuntu为虚拟机名称
VboxManage startvm ubuntu
