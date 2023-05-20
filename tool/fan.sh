# FAN on program

echo 193 > /sys/class/gpio/export
echo out > /sys/class/gpio/P9_1/direction
echo 1 > /sys/class/gpio/P9_1/value

#chmod +x fan.sh
#./fan.sh