# Usage: ./flash.sh /dev/XXXXXX

if command -v esptool >/dev/null 2>&1; then
    ESPTOOL=esptool
else
    ESPTOOL=esptool.py
fi


# FLASH NEW FIRMWARE
$ESPTOOL --chip esp32 --port $1 erase_flash
$ESPTOOL --chip esp32 --port $1 --baud 2000000 write_flash -z 0x1000 esp32spiram-20190125-v1.10.bin

sleep 2

# PUT C01N OPERATING FILES
put_path()
{
	echo "Putting $2"
	ampy -p $1 put $2
	sleep 1
}

echo "-~=  Moving files into place  =~-"
put_path $1 lib
put_path $1 systemapps
put_path $1 apps
put_path $1 config.json
put_path $1 badge.pbm
put_path $1 launcher.py
put_path $1 main.py
put_path $1 boot.py

echo "Reset ESP32 Now"