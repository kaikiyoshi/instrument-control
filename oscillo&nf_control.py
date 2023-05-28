#pyvisaをインポート(計測機器とのやり取りに必要)
import pyvisa as visa

#リソースマネージャーを有効化
rm = visa.ResourceManager()

#リソースマネージャーを止める
rm.close()

#接続されている機器のアドレスを表示
print(rm.list_resources())

#機器との通信を確立する
inst = rm.open_resource("アドレス名")

#機器との通信を止める
inst.close()

###############オシロスコープの制御###############

#設定などの初期化
inst.write('*RST')

#測定の開始・停止(ON=RUN=1,OFF=STOP=0)
inst.write("ACQUIRE:STATE 0")

#画面クリア
inst.write("CLEAR")

#CH2～4の有効化
inst.write("CH2:STATE ON")
inst.write("CH3:STATE ON")
inst.write("CH4:STATE ON")

#縦軸の目盛設定
inst.write("CH1:SCAle 0.1")
inst.write("CH2:SCAle 0.01")
inst.write("CH3:SCAle 0.01")
inst.write("CH4:SCAle 0.01")

#横軸0sの位置(％で指定)
inst.write("HORIZONTAL:POSITION 0")

#横軸の目盛設定
inst.write("HORIZONTAL:SCALE 1")

#トリガ設定
#トリガの種類を設定(RISE：立ち上がり、FALL：立ち下がり)
inst.write("TRIGGER:A:EDGE:SLOPE RISE")

#トリガを掛けるCHを選択し、トリガレベルを設定
inst.write("TRIGGER:A:EDGE:SOURCE CH1")
inst.write("TRIGGER:A:LEVEL:CH1 0.5")

#外部入力に対してトリガを掛ける場合
inst.write("TRIGGER:A:EDGE:SOURCE AUXiliary")
inst.write("TRIGGER:AUXLEVEL 0.5")

#トリガモードの設定
inst.write("TRIGGER:A:MODE NORMAL")
#画面に収まる波形を測定した時点で測定を止める設定(singleボタンを押すのと等価)
inst.write("ACQUIRE:STOPAFTER SEQUENCE")
inst.write("ACQUIRE:STATE 1")

#オシロスコープの状態確認
inst.query("ACQUIRE:STATE?")

###############データ保存###############
import time
#リソースマネージャーを有効化
rm = visa.ResourceManager()
#機器との通信を確立する
inst = rm.open_resource("アドレス名")
#タイムアウトエラーにならないようにタイムアウトまでの時間を長めに設定(30秒)
inst.timeout=30000
#波形データをオシロスコープ側に保存
inst.write('SAVE:WAVEFORM ALL, "C:/Temp.csv"')
while inst.query('*OPC?')[0] != "1":
    time.sleep(1)
#波形データを読み込み、Dataに格納
inst.write('FILESYSTEM:READFILE "C:/Temp_ALL.csv"')
Data = inst.read_raw()
while inst.query('*OPC?')[0] != "1":
    time.sleep(1)
#自分のPCにDataを書き出す
fileName = "保存先のパス"
file = open(fileName, mode = "wb")
file.write(Data)
file.close()
#オシロスコープ側のファイルを削除
inst.write('FILESYSTEM:DELETE "C:/Temp_ALL.csv"')
while inst.query('*OPC?')[0] != "1":
    time.sleep(1)
#通信を止める
inst.close()
rm.close()

###############ファンクションジェネレータ制御###############
#各種設定(初期化、チャネルモード、発振モード、振幅単位)
inst.write("PST;CMO 1;OMO 0;AMU 0")

#波形設定(チャネル、オフセット、位相、周波数、振幅、波形)
inst.write("CHA ;OFS ;PHS ;FRQ ;AMV ;FNC ")

#出力のON/OFF(1=ON、0=OFF)
inst.write("CHA 1;SIG 1")
