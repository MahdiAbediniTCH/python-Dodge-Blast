print('Loading...')
import pygame,sys
from time import clock
from os.path import exists
from random import randint
pygame.init()
#display
width,height=500,700
window=pygame.display.set_mode((width,height))
pygame.display.set_caption('Dodge Blast')
pygame.display.set_icon(pygame.image.load('icon.png'))
#loads and variables
#functions
def encrypt(n):
    n=str(n)
    t=''
    for i in n:
        t+=chr(155-ord(i))+chr(ord(i)-15)+str(ord(i))[0]
    return t
def decrypt(n):
    t=''
    for i in range(0,len(n),3):
        t+=chr(155-ord(n[i]))
    return t
def show_coin(n,t):
    text=font3.render(str(n),True,(255,255,255))
    lil_coin=pygame.transform.scale(coinpics[0],(text.get_height()-2,text.get_height()-2))
    window.blit(lil_coin,(t[0],t[1]-4))
    window.blit(text,(t[0]+lil_coin.get_width()+2,t[1]))
#fonts and design
font0=pygame.font.SysFont('FFF Forward',25)
font1=pygame.font.SysFont('FFF Forward',30)
font2=pygame.font.SysFont('FFF Forward',40)
font3=pygame.font.SysFont('FFF Forward',20)
db=pygame.image.load('Graphics\\dodgeblast.png')
db=pygame.transform.scale(db,(350,150))
button1=pygame.image.load('Graphics\\button1.png')
button1=pygame.transform.scale(button1,(200,50))
button2=pygame.image.load('Graphics\\button2.png')
button2=pygame.transform.scale(button2,(240,60))
button3=pygame.image.load('Graphics\\button3.png')
button3=pygame.transform.scale(button3,(240,60))
button4=pygame.image.load('Graphics\\button4.png')
button4=pygame.transform.scale(button4,(240,60))
button5=pygame.image.load('Graphics\\button5.png')
button5=pygame.transform.scale(button5,(240,60))
pauseb=pygame.image.load('Graphics\\pause.png')
pauseb=pygame.transform.scale(pauseb,(35,50))
#ship
ship=pygame.image.load('Graphics\\ship.png')
ship=pygame.transform.scale(ship,(90,90))
ship_w,ship_h=ship.get_size()
#blast
blast=pygame.image.load('Graphics\\blast.png')
blast=pygame.transform.scale(blast,(40,76))
blast_w,blast_h=blast.get_size()
eblast=pygame.image.load('graphics\\eblast.png')
eblast=pygame.transform.scale(eblast,(40,40))
#enemy
enemy1=pygame.image.load('Graphics\\enemy1.png')
enemy2=pygame.image.load('Graphics\\enemy2.png')
enemy1=pygame.transform.scale(enemy1,(100,50))
enemy2=pygame.transform.scale(enemy2,(100,50))
enemy_w,enemy_h=enemy1.get_size()
#coins_count
coinpics=[pygame.transform.scale(pygame.image.load('Graphics\\coin1.png'),(40,40)),
          pygame.transform.scale(pygame.image.load('Graphics\\coin2.png'),(40,40)),
          pygame.transform.scale(pygame.image.load('Graphics\\coin3.png'),(40,40)),
          pygame.transform.scale(pygame.image.load('Graphics\\coin4.png'),(40,40)),
          pygame.transform.scale(pygame.image.load('Graphics\\coin5.png'),(40,40)),
          pygame.transform.scale(pygame.image.load('Graphics\\coin6.png'),(40,40))]
#stars(background)
stars=[]
for i in range(150):
    stars.append([randint(0,500),randint(0,700)])
#file
if exists('Player Data\\high.score'):
    highf=open('Player Data\\high.score','r+')
    highscore=int(decrypt(highf.read()))
    highf.seek(0)
else:
    highf=open('Player Data\\high.score','w')
    highf.write(encrypt(0))
    highf.close()
    highf=open('Player Data\\high.score','r+')
    highscore=int(decrypt(highf.read()))
    highf.seek(0)
if exists('Player Data\\coin.s'):
    coinf=open('Player Data\\coin.s','r+')
    coins_count=int(decrypt(coinf.read()))
    coinf.seek(0)
else:
    coinf=open('Player Data\\coin.s','w')
    coinf.write(encrypt(0))
    coinf.close()
    coinf=open('Player Data\\coin.s','r+')
    coins_count=int(decrypt(coinf.read()))
    coinf.seek(0)
#start loop
started=False
while not started:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            coinf.write(encrypt(coins_count))
            highf.close() ; coinf.close()
            pygame.display.quit() ; sys.exit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            x,y=event.pos
            if 150<x<150+button1.get_size()[0] and 400<y<400+button1.get_size()[1]:
                started=True
        if event.type==pygame.KEYDOWN:
            started=True
    for i in range(150):
        stars[i][1]+=10
        pygame.draw.circle(window,(240,240,240),stars[i],3)
        if stars[i][1]-3>=700:
            stars[i][1]=0
    text=font3.render('Highscore : '+str(highscore),True,(255,255,255))
    window.blit(db,(80,100))
    window.blit(button1,(150,400))
    window.blit(text,(250-text.get_width()/2,310))
    show_coin(coins_count,(10,10))
    pygame.display.update()
    pygame.time.Clock().tick(60)
    window.fill((0,0,0))
while True:
    g=True
    while g:
        window.fill((0,0,0))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                coinf.write(encrypt(coins_count))
                highf.close() ; coinf.close()
                pygame.display.quit() ; sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN or event.type==pygame.KEYDOWN:
                g=False
        for i in range(150):
            stars[i][1]+=10
            pygame.draw.circle(window,(240,240,240),stars[i],3)
            if stars[i][1]-3>=700:
                stars[i][1]=0
        text1=font1.render('Press G to dodge',True,(255,255,255))
        text2=font1.render('Press H to blast',True,(255,255,255))
        window.blit(text1,(100,200))
        window.blit(text2,(100,400))
        pygame.display.update()
        pygame.time.Clock().tick(60)
    #setups
    nh_countdown=120
    play_again=False
    ship_x,ship_y=width//2-ship_w//2,height-ship_h-40#middle of screen
    ship_xm=0
    blasts=[]
    enemies=[]
    eas=1
    eas_timer=0
    done=False
    stop=True
    move=29#move switch(left or right)
    shoot_timer=clock()#clock object
    enemy_spawn_timer=clock()
    reload=True#blast reload
    shoots=0
    score=0
    e_spawn=2
    e_speed=5
    combo=0
    levelup_timer=0
    enemy_set_timer=0
    expl=0
    coinind=0
    cointimer=0
    cc_expl=0
    coins=[]
    revived=False
    level=1
    eblasts=[]
    lost=False
    while not done:
        #events
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                done=True
                coinf.write(encrypt(coins_count))
                highf.close() ; coinf.close()
                pygame.display.quit() ; sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_g:#dodge
                    ship_xm=move
                    stop=False
                    move=-move
                    reload=True
                    shoots=0
                if event.key==pygame.K_h:#blast
                    dt=float(clock()-shoot_timer)
                    if dt>=0.05:
                        if reload:
                            blasts.append([ship_x+25,ship_y-20])
                            shoot_timer=clock()
                            shoots+=1
                            if shoots>=3:
                                reload=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                x,y=event.pos
                if 455<x<455+35 and 10<y<10+50:#make an inner loop for pause
                    gray=pygame.surface.Surface((500,700))
                    gray.fill((157,157,157))
                    gray.set_alpha(200)
                    text=font0.render('Press any key to continue',True,(255,255,255))
                    window.blit(gray,(0,0))
                    window.blit(text,(250-text.get_width()/2,250))
                    pressed=False
                    while not pressed:
                        for event in pygame.event.get():
                            if event.type==pygame.QUIT:
                                pygame.display.quit() ; sys.exit()
                            if event.type==pygame.KEYDOWN:
                                pressed=True
                        pygame.display.update()
                        pygame.time.Clock().tick(60)
        #updates
        window.fill((0,0,0))
        #new highscore
        if score>highscore and nh_countdown>0:
            text=font3.render('New highscore!',True,(255,255,255))
            window.blit(text,(250-text.get_width()/2,25+text.get_height()))
            nh_countdown-=1
        #level up
        if levelup_timer>=60*25 and (ship_x<=405 or ship_x<=5):
            level+=1
            starsc=stars[:]
            stars=[]
            for i in range(150):
                stars.append([randint(0,500),randint(0,700)])
            levelup_timer=0
            enemies=[]
            blasts=[]
            sm=10
            if e_spawn>0.8:
                e_spawn-=0.3
            if e_speed<10:
                e_speed+=0.6
            for i in range(150):
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        done=True
                        coinf.write(encrypt(coins_count))
                        highf.close() ; coinf.close()
                        pygame.display.quit() ; sys.exit()
                    if event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_g:#dodge
                            ship_xm=move
                            stop=False
                            move=-move
                            reload=True
                            shoots=0
                if (ship_x+ship_w+10>=width or ship_x-10<=0) and stop==True:#stopping at edges
                    ship_xm=0
                ship_x+=ship_xm
                lu_text=font2.render('Level Up!',True,(255,255,255))
                for j in range(150):
                    starsc[j][1]+=int(sm)
                    pygame.draw.circle(window,(240,240,240),starsc[j],3)
                    if starsc[j][1]-3>=700:
                        starsc[j][1]=0
                window.blit(lu_text,(250-lu_text.get_width()/2,0))
                window.blit(ship,(ship_x,ship_y))
                pygame.display.update()
                pygame.time.Clock().tick(60)
                window.fill((0,0,0))
                stop=True
                if i>75:
                    sm-=0.3
                else:
                    sm+=0.3
        #text
        sctext=font2.render(str(score),True,(255,255,255))
        combotext=font3.render('Combo x'+str(combo),True,(255,255,255))
        #enemies' blasts
        if level>=3:
            for i in range(len(enemies)):
                if 45<enemies[i][1]<55:
                    if randint(1,4)==1:
                        eblasts.append([enemies[i][0]+enemy_w//2-20,enemies[i][1]+5])
        for i in range(len(eblasts)):
            window.blit(eblast,eblasts[i])
            eblasts[i][1]+=e_speed+5
        for i in range(len(eblasts)):
            if eblasts[i][1]>=700:
                del eblasts[i]
                break
        #enemies
        if float(clock()-enemy_spawn_timer)>=e_spawn:
            if enemy_set_timer==4:
                enemy_set_timer=0
                rand=randint(1,2)
                if rand==1:
                    enemies.append([5,-enemy_h])
                    coins.append([enemies[len(enemies)-1][0]+25,enemies[len(enemies)-1][1]])
                    enemies.append([int(250-enemy_w/2),-(2*enemy_h+5)])
                    coins.append([enemies[len(enemies)-1][0]+25,enemies[len(enemies)-1][1]])
                    enemies.append([500-5-enemy_w,-(3*enemy_h)+5])
                    coins.append([enemies[len(enemies)-1][0]+25,enemies[len(enemies)-1][1]])
                else:
                    enemies.append([500-5-enemy_w,-enemy_h])
                    coins.append([enemies[len(enemies)-1][0]+25,enemies[len(enemies)-1][1]])
                    enemies.append([int(250-enemy_w/2),-(2*enemy_h+5)])
                    coins.append([enemies[len(enemies)-1][0]+25,enemies[len(enemies)-1][1]])
                    enemies.append([5,-(3*enemy_h+5)])
                    coins.append([enemies[len(enemies)-1][0]+25,enemies[len(enemies)-1][1]])
            else:
                enemies.append([randint(5,500-enemy_w),-enemy_h])
                coins.append([enemies[len(enemies)-1][0]+25,enemies[len(enemies)-1][1]])
                enemy_set_timer+=1
            enemy_spawn_timer=clock()
        if eas_timer>=10:
            eas_timer=0
            eas=not eas
        #coins
        for i in range(len(coins)):#blit and movement
            window.blit(coinpics[coinind],coins[i])
            coins[i][1]+=int(e_speed)
        for i in range(len(coins)):#ship touch
            if coins[i][0]-ship_w<ship_x<coins[i][0]+50:
                if coins[i][1]-ship_h<ship_y<coins[i][1]+30:
                    coins_count+=1
                    cc_expl=2
                    del coins[i]
                    break
        if cc_expl:
            pygame.draw.circle(window,(241,230,12),(ship_x+int(ship_w/2),ship_y+int(ship_h/2)-20),60)
            cc_expl-=1
        for i in range(len(coins)):#deleting coins that are out of screen for runtime
            if coins[i][1]>=701:
                del coins[i]
                break
        #coin animaion
        if cointimer>=5:
            coinind+=1
            cointimer=0
        if coinind==6:
            coinind=0
        #ship
        if (ship_x+ship_w+10>=width or ship_x-10<=0) and stop==True:#stopping at edges
            ship_xm=0
        ship_x+=ship_xm
        #stars(background)
        for i in range(150):
            stars[i][1]+=10
            pygame.draw.circle(window,(240,240,240),stars[i],3)
            if stars[i][1]-3>=700:
                stars[i][1]=0
        #blit
        window.blit(ship,(ship_x,ship_y))
        ed=[]
        ed2=[]
        for i in range(len(enemies)):
            if eas==1:
                window.blit(enemy1,(enemies[i][0],enemies[i][1]))
            else:
                window.blit(enemy2,(enemies[i][0],enemies[i][1]))
            enemies[i][1]+=int(e_speed)
            if enemies[i][1]>700:
                ed2.append(i)
                combo=0
            #loose condition
            if enemies[i][0]-ship_w<ship_x<enemies[i][0]+enemy_w and enemies[i][1]-ship_h<ship_y<enemies[i][1]+enemy_h-20:
                lost=True
        for i in range(len(eblasts)):
            if eblasts[i][0]-ship_w<ship_x<eblasts[i][0]+40:
                if eblasts[i][1]-ship_h<ship_y<eblasts[i][1]+20:
                    del eblasts[i]
                    lost=True
                    break
        if lost:
            enemies=[]
            hf=False
            if score > highscore:
                highf.seek(0)
                highscore=score
                highf.truncate()
                highf.write(encrypt(highscore))
                hf=True
            pr=True
            coinf.write(encrypt(coins_count))
            coinf.close()
            coinf=open('player data\\coin.s','r+')
            spent=False
            if not revived and coins_count>=150 and score>10:
                revived=True
                while pr:
                    window.fill((0,0,0))
                    show_coin(coins_count,(10,10))
                    text=font3.render('Score : '+str(score),True,(255,255,255))
                    text2=font2.render('Continue?',True,(255,255,255))
                    window.blit(text,(250-text.get_width()/2,230))
                    window.blit(text2,(250-text2.get_width()/2,275))
                    for event in pygame.event.get():
                        if event.type==pygame.QUIT:
                            coinf.write(encrypt(coins_count))
                            highf.close() ; coinf.close()
                            pygame.display.quit() ; sys.exit()
                        if event.type==pygame.MOUSEBUTTONDOWN:
                            x,y=event.pos
                            if 250-button2.get_width()/2<x<250-button2.get_width()/2+button2.get_width() and 350<y<350+button2.get_height():
                                coins_count-=150
                                coinf.write(encrypt(coins_count))
                                coinf.close()
                                coinf=open('player data\\coin.s','r+')
                                pr=False
                                lost=False
                                spent=True
                            if 250-button2.get_width()/2<x<250-button2.get_width()/2+button2.get_width() and 425<y<425+button3.get_height():
                                pr=False
                    for i in range(150):
                        stars[i][1]+=10
                        pygame.draw.circle(window,(230,230,230),stars[i],3)
                        if stars[i][1]-3>=700:
                            stars[i][1]=0
                    window.blit(button4,(250-button4.get_width()/2,350))
                    window.blit(button5,(250-button5.get_width()/2,425))
                    pygame.display.update()
                    pygame.time.Clock().tick(60)
            if not spent:
                pr=True
                while pr:
                    window.fill((142,0,60))
                    show_coin(coins_count,(10,10))
                    if hf:
                        text=font1.render('New highscore! : '+str(score),True,(255,255,255))
                        window.blit(text,(250-text.get_width()/2,300))
                    else:
                        text=font1.render('Score : '+str(score),True,(255,255,255))
                        text2=font1.render('HighScore : '+str(highscore),True,(255,255,255))
                        window.blit(text,(250-text.get_width()/2,225))
                        window.blit(text2,(250-text2.get_width()/2,275))
                    for event in pygame.event.get():
                        if event.type==pygame.QUIT:
                            coinf.write(encrypt(coins_count))
                            highf.close() ; coinf.close()
                            pygame.display.quit() ; sys.exit()
                        if event.type==pygame.MOUSEBUTTONDOWN:
                            x,y=event.pos
                            if 250-button2.get_width()/2<x<250-button2.get_width()/2+button2.get_width() and 350<y<350+button2.get_height():
                                play_again=True
                            if 250-button2.get_width()/2<x<250-button2.get_width()/2+button2.get_width() and 425<y<425+button3.get_height():
                                highf.close() ; coinf.close()
                                pygame.display.quit() ; sys.exit()
                        if event.type==pygame.KEYDOWN:
                            play_again=True
                    for i in range(150):
                        stars[i][1]+=10
                        pygame.draw.circle(window,(230,230,230),stars[i],3)
                        if stars[i][1]-3>=700:
                            stars[i][1]=0
                    window.blit(button2,(250-button2.get_width()/2,350))
                    window.blit(button3,(250-button3.get_width()/2,425))
                    pygame.display.update()
                    pygame.time.Clock().tick(60)
                    if play_again:
                        pr=False
        if play_again:
            break
        bd=[]
        for i in range(len(blasts)):
            window.blit(blast,blasts[i])
            blasts[i][1]-=25
            if blasts[i][1]+blast_h<0:
                bd.append(i)
                combo=0
            else: 
                for j in range(len(enemies)):
                    if enemies[j][0]-blast_w<blasts[i][0]<enemies[j][0]+enemy_w and enemies[j][1]-blast_h<blasts[i][1]<enemies[j][1]+enemy_h-20:
                        ed.append(j)
                        if not(i in bd):
                            bd.append(i)
                        score+=1+combo//5
                        combo+=1
        #texts
        show_coin(coins_count,(10,10))
        window.blit(sctext,(10,40))
        if combo>=2:
            window.blit(combotext,(250-combotext.get_width()/2,15))
        #pause button
        window.blit(pauseb,(455,10))
        #dels
        edied=False
        for i in ed:
            center=(int((enemies[i][0]+(enemies[i][0]+enemy_w))/2),int((enemies[i][1]+(enemies[i][1]+enemy_h))/2))
            expl=2
            del enemies[i]
            edied=True
        for i in ed2:
            if edied:
                del enemies[i-1]
            else:
                del enemies[i]
        for i in bd:
            try:
                del blasts[i]
            except:
                pass
        if expl:
            expl-=1
            pygame.draw.circle(window,(235,235,235),center,70)
        pygame.display.update()
        pygame.time.Clock().tick(60)
        stop=True
        eas_timer+=1
        levelup_timer+=1
        cointimer+=1
pygame.quit()
