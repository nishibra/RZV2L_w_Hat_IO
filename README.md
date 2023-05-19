# RZV2L_w_Hat_IO

RZ-BoardにRasPi4用HATを組み合わせてロボットを開発します。

![RZV2L_w_Hat_IO](/pics/rz_hat.jpg)



Raspberry Piへの電源供給は外付けのプッシュスイッチによってON/OFFする事ができ、更にサーボモータなどをコントロールするRS-485とTTL I/F、およびI2C　I/Fを装備しています。

>DXHAT(BTE100): [（株）ベストテクノロジー](https://www.besttechnology.co.jp/modules/knowledge/?BTE100%20DXHAT)

RasPi4用HATなので一部改造が必要です。


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

```
$ pip3 install smbus2

>>import smbus2 as sambus


```
#### TFLuna-I2C_python

https://github.com/budryerson/TFLuna-I2C_python

https://files.seeedstudio.com/wiki/Grove-TF_Mini_LiDAR/res/SJ-PM-TF-Luna-A03-Product-Manual.pdf
### I2C接続の確認

uEnv.txtでi2cを活性
```
# ls /dev/*i2c*
# /dev/i2c-1 ・・・
# i2cdetect -y 1
```


### new servo
```
ID=2の1つを対象とする場合は
　指令:<#2...>
　応答:(#2...)
複数IDの場合は
　指令:<#3...#1...#2...>
　応答:(#3...)(#1...)(#2...)
以下のようなコマンドでID=1に対して360度へ移動する角度指令がなされます。
　指令:<#1EX=1TA=36000TP=500>
　応答:(#1EX=OKTA=OKTP=OK)

指令は以下の通りです。
EX=0:停止, 1:角度, 2:角速度, 3:角度+角速度, 4:電流, 5:角度+電流, 6:角速度+電流, 7:角度+角速度+電流,
8:PWM
TA=角度指令値 (x100 deg)
TV=角速度指令値 (?)
TC=電流指令値 (mA)
TP=PWM指令値 (‰)
各指令に対してOKないしNGの応答を返します。
なおいずれの制御においてもPWMが最終段にあるので、PWM値を指定しておかないと動きません。

またLabVIEWのツールでは全ての設定を一括で送っている(設定忘れがない)のでどう動くかが見えます。
https://www.besttechnology.co.jp/download/USER/UEMITSU/lv_debug3_20230501.7z

なお角度はセンサのワンタイムROMという仕様により使用不能になるリスクを回避するため、現時点でキャリブレーションをしていません。
まずは角度センサのフルスケールの中央をセンターにして使って下さい。
デミリタとしてカンマを入れて指令すれば応答もカンマ入りになりますので、長さが不定のパケットも容易に切り出せます。
CA:角度
CV:角速度
CC:電流
CP:PWM
なお以下のようなパケットの場合、サーボからはまとめて応答が返ります。
<#1CA#2CA#3CA#1CV#3CV#4CV>
(#1CA=??CV=??)(#2CA=??)(#3CA=??CV=??)(#4CV=??)
これはサーボ側のパケット処理をOSのqueueを用いて行っていた時の名残ですが、ホスト側も頭から順にqueueに投げる想定で処理すればお気楽かと。

