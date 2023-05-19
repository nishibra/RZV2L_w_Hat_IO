# RZV2L_w_Hat_IO

RZ-BoardにRasPi4用HATを組み合わせてロボットを開発します。

![RZV2L_w_Hat_IO](/pics/rz_hat.jpg)



Raspberry Piへの電源供給は外付けのプッシュスイッチによってON/OFFする事ができ、更にサーボモータなどをコントロールするRS-485とTTL I/F、およびI2C　I/Fを装備しています。

>DXHAT(BTE100): [（株）ベストテクノロジー](https://www.besttechnology.co.jp/modules/knowledge/?BTE100%20DXHAT)

RasPi4用HATなので一部改造が必要です。

## 電源のON-OFF方法

RZボードに電源システムが搭載されており、ボード上のSWを押すことで電源が入るようになっています。HATにも同じ機能があります。
いずれかを使用することでON-OFFをさせるという対応が必要で、これにはRZボード上のSWを短絡することにより対応しました。

## Serial servoを接続

Serial servoを接続するにはBTE094 TTL2DXIFを使うと便利です。DXHATにはこれが搭載されており、ttySC2に接続されています。
HATの代わりにこれを接続することもできます。

[BTE094 TTL2DXIF](https://www.besttechnology.co.jp/modules/knowledge/?BTE094%20TTL2DXIF)

### uEnv.txtの編集
UARTやI2Cを起動するにはDiskのbootにあるuEnv.txtを編集します。

```
enable_overlay_uart2=yes
```
を追加するとUARTが活性します。 

### FTDI install driver

USBのシリアルドライバーを使用するにはFTDIのドライバーをbitbakeする必要があります。

https://ftdichip.com/drivers/d2xx-drivers/


## I2Cを使う場合

HATでI2Cを使用する場合2KΩ程度のプルアップ抵抗が必要です。
![プルアップ抵抗](/pics/pullup.jpg)

Python3ではsmbus2をインストールして使ってください。
```
$ pip3 install smbus2
```
以下のようにインポートします。
```
>>import smbus2 as sambus
```

### TFLuna-I2C_python

https://github.com/budryerson/TFLuna-I2C_python

https://files.seeedstudio.com/wiki/Grove-TF_Mini_LiDAR/res/SJ-PM-TF-Luna-A03-Product-Manual.pdf

### I2C接続の確認

uEnv.txtでi2cを活性化しておきます。
以下でポートとアドレスが確認できます。
```
# ls /dev/*i2c*
# /dev/i2c-1 ・・・
# i2cdetect -y 4
```


