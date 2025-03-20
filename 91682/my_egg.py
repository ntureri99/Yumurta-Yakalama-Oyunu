import play
import time # 3sn bir yumurta
import pygame #ses dosyası için
from random import randint # rastgele yerden çıkacak yumurta

pygame.mixer_music.load('hello.mp3')#arka plan müziği= fon müziği
pygame.mixer_music.play()
play.set_backdrop('light green') #arkaplan rengi

hello_txt=play.new_text(words='Catch 10 EGGS!', x=0, y=play.screen.height/2-30)

egg=play.new_circle(color='white', x=0, y=0, radius=30, border_color='grey', border_width=2)

eggs=[egg]
eggs_amount=play.new_text(words='0', x=300, y=play.screen.height/2-30, color='yellow')

backet=play.new_image(image='sepet.png', x=0, y=-play.screen.height/2+50, size=20)

frames = 48 # kare sıklığı
old_time = 0 # süre için 

@play.when_program_starts #fiziksel özellikler burada tanımlanır 
def start():
    global old_time
    old_time = time.time()

    backet.start_physics(
        can_move=True,stable=True, obeys_gravity=False, bounciness=1, mass=10
    )
    eggs[0].x = randint(-play.screen.width/2+20, play.screen.width/2-20)
    eggs[0].y = play.screen.height/2-20

@play.repeat_forever
async def game():
    global old_time # her yerden erişim sağlamak için 

    #yumurta yakalama
    for egg in eggs: #yumurtlar listesindeki her yumurta içn 
        if egg.is_touching(backet): #yumurta sepete değiyor mu
            eggs.remove(egg) # yumurtalar listesinden değen yumurtayı sil
            egg.hide() # yumurtayı gizle  
            eggs_amount.words=str(int(eggs_amount.words)+1) #metini sayıya cevirdik 
        egg.y=egg.y-5  #yumurta yukarıdan aşagıya düşerken y kordinatı değişr 

        #kazanma
        if int(eggs_amount.words) == 10: # 10 yumurt topladıysam 
            win = play.new_text(words='YOU WIN', x=0, y=0, color='yellow', font_size=100)
            backet.hide() #sepet gizlenecek 
            await play.timer(seconds=1)
            quit()

        #kaybetme
        if egg.y < backet.y:
            lose = play.new_text(words='YOU LOSE', x=0, y=0, color='red', font_size=100)
            backet.hide()
            await play.timer(seconds=1)
            quit()
 
    #sepet yönlendirme  sağa sola hareket edrken x kordinatı kullanılır 
    if play.key_is_pressed('a','A',"left"):
        backet.physics.x_speed = -15
    elif play.key_is_pressed('d','D',"right"):
        backet.physics.x_speed = 15
    else:
        backet.physics.x_speed = 0
 
    #3 saniyede bir yeni yumurta düşer 
    if time.time()-old_time > 3:
        new_egg = play.new_circle(color='white', x=0, y=0,
                                 radius=30, border_color='grey', border_width=2)
       
        new_egg.x = randint(-play.screen.width/2+20, play.screen.width/2-20)
        new_egg.y = play.screen.height/2-20
        eggs.append(new_egg)

        old_time = time.time()

    await play.timer(seconds=1/frames)

play.start_program()

