# 将此文件`run_virtual_vm_on_windows_started.bat`放到C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp
cd C:\Program Files\Oracle\VirtualBox

echo "starting ubuntu ......"
# ubuntu为虚拟机名称
VboxManage startvm ubuntu
# 重启系统后即可自动启动虚拟机系统

