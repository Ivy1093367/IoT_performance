#import playsound
#playsound.playsound('aki.mp3')

#import pygame
#pygame.mixer.init()
#pygame.mixer.music.load('yee.mp3')
#pygame.mixer.music.play()

#import vlc
#p = vlc.MediaPlayer("yee.mp3")
#p.play()

import pygame
import threading

# 初始化pygame
pygame.mixer.init()

# 創建代碼和歌曲的對應字典
song_mapping = {
    "1": "ahh_1.mp3",
    "2": "aki.mp3",
    "3": "yee.mp3"
}

def play_song(song_code):
    # 检查输入的代码是否在字典中
    if song_code in song_mapping:
        # 加载并播放对应的歌曲
        song_file = song_mapping[song_code]
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
    # 讀取使用者输入的歌曲代碼
    song_code = input("请输入要播放的歌曲代码（或输入 q 退出）：")

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