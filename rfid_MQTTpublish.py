from machine import Pin
import binascii    #二進位制和ASCII轉換模組
from machine import UART
import time
#白線：pin23、紅線：5v、棕線：接地、Tx：Rx pin16、Rx：Tx pin17
import network
from umqtt.simple import MQTTClient

# 設定 Wi-Fi 連線
wlan = network.WLAN(network.STA_IF)
wlan.active(True) 
wlan.connect('Enxi', 'oc8x0ibt')
while not wlan.isconnected():
    pass

#連線到 MQTT 伺服器
mqClient0 = MQTTClient('mp3test','140.127.218.172')
mqClient0.connect()

# 初始化變數
i = 0
tagdict,tempstr = {},[]
en = Pin(23, Pin.OUT)
en.value(1)
uart = UART(2, baudrate=115200, parity=None, tx=17, rx=16)   #設置UART

#RFID偵測函式
def single_polling():  
    cmd = b'\xbb\x00\x22\x00\x00\x22\x7e'   
    uart.write(cmd)    #寫入cmd指令，RFID便會開始做一次偵測
    time.sleep_ms(50)

#從儲存表讀資料
with open("etag.csv","r") as f:
    for line in f.readlines():
        tempstr = line.replace("\n","").split(",")
        tagdict[tempstr[0]] = tempstr[1]   #將csv的資料做成dictionary方便搜索資料

while True:   #持續偵測
    flag = False
    token = []
    single_polling()
    t = time.time_ns()   #每次間隔時間
    while True:      
        data = 0
        s = uart.read(1)  
        #print(s)
        if s != None:    #一次讀取一截，資料是["bb","02","22"]開頭才會是正確標籤
            data = binascii.hexlify(s).decode()   #轉成16進位
            if data == 'bb':    
#                 flag = False
                if binascii.hexlify(uart.read(1)).decode() == '02':
#                     flag = False
                    if binascii.hexlify(uart.read(1)).decode() == '22':
                        token = ["bb","02","22"]    # token 用於儲存 RFID 數據
                        flag = True   
                        continue
                    
            if flag:   #若token是我們要的開頭，就將後面讀到的資料存到token
                token.append(str(data))    
                
            if len(token) == 24:    #當token長度達到24停止
                tag = ""
                i = i + 1
                for j in range(8,20):   #取出可判讀的token資料存到tag字串
                    tag = tag + token[j]
                print("(%d) : %s" %(i,tag))
                
                if tagdict.get(tag, "no") == "no":    #如果標籤不在儲存表中，請使用者輸入資訊並將標籤寫入表中
                    print("not exist : %s" %(tag))
                    music_code = input("input:")  
                    with open("etag.csv","a") as f:
                        f.write("\n%s,%s" %(tag, music_code))
                    tagdict[tag] = music_code
                else:
                    strout="%s" %(tagdict.get(tag))
                    print("exist : %s" %(tagdict.get(tag)))
                    mqClient0.publish("mp3test",strout)      #如果標籤在儲存表中，將相應的代碼發佈到 MQTT Server
                break
        
        if time.time_ns() - t >= 100000000:  #若程式間隔太久，跳出內層迴圈讓RFID重新讀取
            break
    