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
# nano //boot/uEnv.txt
--以下を追加します。--
enable_overlay_uart2=yes
enable_overlay_i2c=yes
enable_overlay_gpio=yes
```
を追加するとUART/I2C/GPIOが活性化します。詳細は同じフォルダーにあるreadme.txtをご参照ください。 

### KRSをコントロールしてみよう

class_krs_dr.pyをダウンロードしてRZボードに転送します。
```
$ scp class_krs_dr.py root@192.168.8.99:~root/sv
$ ssh root@192.168.8.99

# cd sv
# python3 class_krs_dr.py
```
でサーボモータが動作します。



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

TFLuna-I2Cを使ってみます。サンプルを以下gitHubよりダウンロードします。

[gitHub](https://github.com/budryerson/TFLuna-I2C_python)

[資料](https://files.seeedstudio.com/wiki/Grove-TF_Mini_LiDAR/res/SJ-PM-TF-Luna-A03-Product-Manual.pdf)

### I2C接続の確認

uEnv.txtでi2cを活性化しておきます。ポート4が活性化され、他のポートはシステムで使われています。

以下でポートとアドレスが確認できます。TFLunaはポート4 アドレス10になります。RTCのアドレスは68です。

サンプルプログラム中のsmbusをsambus2に変更して使ってください。

```
# ls /dev/*i2c*
# /dev/i2c-1 ・・・
# i2cdetect -y 4
```


