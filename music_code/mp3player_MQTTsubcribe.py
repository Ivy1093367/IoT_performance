import pygame
import threading
#MQTT
import network
import paho.mqtt.client as mqtt
import time
#from umqtt.simple import MQTTClient   用在micropython的

global song_code
# 連接回調函數
def on_connect(client, userdata, flags, rc):
    print("已連線至 MQTT")
    # 訂閱主题
    client.subscribe("mp3test")

# 接收訊息回調函數
def on_message(client, userdata, msg):
    print("收到訊息：Topic ->", msg.topic, ", 訊息 ->", msg.payload.decode())
    song_code = str(msg.payload.decode()).rstrip()
    #print(len(song_code))
    #print(song_code)
    #print("hi"+ song_code + "嗨")
    time.sleep(0.1)
    # 停止當前歌曲的播放
    pygame.mixer.music.stop()

    # 創建新的播放執行緒並開始播放
    play_thread = threading.Thread(target=play_song, args=(song_code,))
    play_thread.start()

# 創建 MQTT 客戶端
client = mqtt.Client()

# 設置連接和接收訊息的回調函數
client.on_connect = on_connect
client.on_message = on_message

# 連接到 MQTT 代理服務器
client.connect("140.127.218.172", 1883, 60)

# 初始化pygame
pygame.mixer.init()

# 創建代碼和歌曲的對應字典
song_mapping = {
    'a': 'smoke.mp3',
    'b': 'aki.mp3',
    'c': 'yee.mp3',
    'd': 'exercise.mp3',
    'e': 'chu.mp3',
    'f': 'rolling_in_the_deep.mp3',
    'g': 'bir.mp3'
}

def play_song(song_code):
    # 檢查输入的代碼是否在字典中
    if song_code in song_mapping:
        # 加載並播放對應的歌曲
        song_file = song_mapping[song_code]
        #song_file = song_mapping.get(song_code, "not found")
        pygame.mixer.music.load(song_file)
        pygame.mixer.music.play()
    else:
        print("無效的歌曲代碼")

# 讀取初始的歌曲代碼
current_song_code = input("請输入初始歌曲代碼：")

# 創建播放執行緒並開始播放
play_thread = threading.Thread(target=play_song, args=(current_song_code,))
play_thread.start()

# 循環接受使用者输入並更換歌曲
while True:    
    # 循環監聽訊息
    client.loop_forever()
    client.on_message = on_message
    #print(song_code+"找到了")
    #song_code = input("请输入要播放的歌曲代码（或输入 q 退出）：")
    # 讀取使用者輸入的歌曲代碼
    #song_code = stringout
    # 檢查是否退出程序
    if song_code.lower() == "q":
        break

    # 停止當前歌曲的播放
    pygame.mixer.music.stop()

    # 創建新的播放執行緒並開始播放
    play_thread = threading.Thread(target=play_song, args=(song_code,))
    play_thread.start()

# 等待播放執行緒结束
play_thread.join()