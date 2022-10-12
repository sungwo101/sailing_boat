import pygame
from random import *
from time import sleep

BLACK = (0,0,0)
RED = (255,0,0)
pad_width = 512         #게임 가로
pad_height = 800      #게임 세로
bg_height = -960
boat_width = 30
boat_height = 60
enemy_width = 65
enemy_height = 65
ele_width = 35
ele_height = 80
wood_height = 50
wood_width = 65

#배경화면 이미지
bg1 = pygame.image.load('bg1.jpg')
bg2 = pygame.image.load('bg2.jpg')

#게이지 이미지
gauge = pygame.image.load('g.png')
gauge_L = pygame.image.load('g_L.png')
gauge_R = pygame.image.load('g_R.png')
g_ball = pygame.image.load('g_b.png')

#배경음악 
pygame.init()
mySound = pygame.mixer.Sound( "bgm.mp3" )
mySound.set_volume(0.015)
mySound.play(-1)

#장애물이 화면 아래로 통과한 개수
def Passed(c1,c2,c3):
    global gamepad
    font = pygame.font.SysFont(None,30)
    text = font.render('rock : '+ str(c1) + ' ali : ' + str(c2) + ' wood : ' + str(c3), True, RED)
    gamepad.blit(text, (280,0))
    
def Tilt(tilt):
    global gamepad
    font = pygame.font.SysFont(None,40)
    text = font.render('Degree : '+ str(tilt) + ' (0 or 50)', True, RED)
    gamepad.blit(text, (160,20))

#메세지 특성
def Message(text):
    global gamepad
    textfont = pygame.font.SysFont('font/nanum.ttf', 80)
    text = textfont.render(text, True, BLACK)
    textpos = text.get_rect()
    textpos.center = (pad_width/2, pad_height/2)
    gamepad.blit(text,textpos)
    
#게임오버 메세지
def gameover(c1, c2, c3):
    global gamepad
    count = c1 + c2 + c3
    Message('passed : ' + str(count))

#구름 소환
def apper_cloud(img1, img2 , x1, x2, state):
    global gamepad
    if state:
        Object(img1, x1, 95)
        Object(img2, x2, 95)
        
def img_boat(a,img, img1, img2, x, y):
    global gamepad
    if a == 1:
        Object(img, x, y)
        a == 0
    elif a == 2:
        Object(img1, x, y)
        a == 0
    elif a == 3:

        Object(img2, x, y)
        a == 0
    
#버튼
class Button:
    def __init__(self, img, x, y, act = None):
        self.act = act
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.topleft = (x,y)
        
    def draw(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        if self.rect.collidepoint(mouse):
            if click[0] and self.act != None:
                sleep(1)
                return self.act()
                
        Object(self.img, self.rect.x, self.rect.y)       
  
        
#경고 
def B_state(angle):
    point = 216
    
    if angle == 25:
        Object(gauge, 0, 0)
    elif angle < 25:
        Object(gauge_L, 0, 0)
    elif angle > 25:
        Object(gauge_R, 0, 0)
    
    point += ((angle - 25) * 9)
    if point <= 0:
        point = 0
    if point >= 432:
        point = 432
    
    Object(g_ball, point, 0)
    
    

#돌
def Rock(a):
    global gamepad, enemy
    if a == 0:
        enemy = pygame.image.load('rock1.png')
    elif a == 1:
        enemy = pygame.image.load('rock2.png')
    elif a == 2:
        enemy = pygame.image.load('rock3.png')
    elif a == 3:
        enemy = pygame.image.load('rock4.png')
    else:
        enemy = pygame.image.load('rock5.png')
  
#게임 리셋
def reset():
    pygame.display.update()
    runGame()
    
#게임 객체 드로잉
def Object(obj,x,y):
    global gamepad
    gamepad.blit(obj, (x,y))

#게임 첫화면
def game_intro():
    global gamepad, game_s
    i = True
    
    while i:
        Object(game_s, 0, 200)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                runGame()
                
        pygame.display.update()
        clock.tick(15)


#게임 실행 메인
def runGame():
    global gamepad, clock, boat, boat_L, boat_R, enemy, ele1, ele2, i_button, game_over ,\
        cloud1,cloud2, cloud_w, wood, game_s
    
    enemypassed = 0     #장애물 지나간 수
    e_passed = 0
    w_passed = 0
    
    #보트 초기 위치
    x = pad_width * 0.45
    y = pad_height * 0.9
    x_change = 0
    B_a = 25     #배 각도의 상태
    B_angle = 0
    
    #배경
    bg1_y = 0
    bg2_y = bg_height
    bg_speed = 3
    
    #바위
    enemy_x = randrange(0, pad_width - enemy_width)
    enemy_y = 0
    enemy_speed = 3
    
    #악어
    ele_x = randrange(0, pad_width - ele_width)
    ele_y = 0
    ele_speed = 5
    
    #통나무
    wood_x = randrange(0, pad_width - wood_width)
    wood_y = 0
    wood_speed = 3
    G_wood = 0
    wood_t = 1
    
    cloud_s = False
    cloud_w = True
    state = False
    
    cloud_speed = 5
    cloud_x1 = -512
    cloud_x2 = 512
    
    ali = 0    
    s = True
    rock_a = randint(0,5)    
    
    boat_a = 0
    
    run = True
    while run:
        
        #보트 화면에 그리기
        Rock(rock_a)
        
        Object(bg1, 0, bg1_y)
        Object(bg2, 0, bg2_y)
        
        chance = randint(0,9)      #1/10 확률로 배가 자연스래 기움 
        path = randint(0,1)     #0,1로 좌우 선택 (0 = 좌, 1 = 우)
        
        Object(boat, x, y)      #보트 화면에 그리기
        Object(enemy, enemy_x, enemy_y)     #장애물 화면에 그리기

        ali += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:       # X버튼으로 창 종료
                run = False
                
            if event.type == pygame.KEYDOWN:    # a누르면 왼쪽으로 이동
                if event.key == pygame.K_a:
                    x_change -= 5
                    
                elif event.key == pygame.K_d:   # d누르면 오른쪽으로 이동
                    x_change += 5
                
                #왼,오 화살표로 각도 조정
                elif event.key == pygame.K_LEFT:    
                    B_angle -= 1
                
                elif event.key == pygame.K_RIGHT:
                    B_angle += 1
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    x_change = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    B_angle = 0
       
        ###장애물
        #보트 위치 재조정
        x += x_change
        
        if x <= 0:
            x = 0
        elif x >= pad_width - boat_width:
            x = pad_width - boat_width
        
        #보트의 각도 재조정
        B_a += B_angle
        
        #배경 위치 조정
        if bg1_y >= pad_height:
            bg1_y = bg_height
        if bg2_y >= pad_height:
            bg2_y = bg_height
        
        
        #배경 속도
        bg1_y += bg_speed
        bg2_y += bg_speed
        
        if state == False:
            
            #보트가 바위이랑 부딫쳤는지
            if y <= enemy_y + enemy_height and y >= enemy_y:
                if (enemy_x <= x <= enemy_x + enemy_width) or\
                        (enemy_x <= x + boat_width <= enemy_x + enemy_width):
                        state = True

            
            #장애물들 아래로 이동
            enemy_y += enemy_speed
            ele_y += ele_speed
            
            
            if enemy_y > pad_height:
                enemy_y = 0
                enemy_x = randrange(0, pad_width - enemy_width)
                rock_a = randint(0,5)
                enemypassed += 1
                
                if enemypassed >= 12:
                    enemy_speed += 0.5
                else:
                    enemy_speed += 1
                bg_speed += 1
                if enemypassed >= 10:
                    enemy_x1 = randrange(0, pad_width - enemy_width)
                
                
            #장애물 8번 피하면 악어생성
            if enemypassed >= 0:
                if ali % 8 == 0 or ali % 8 == 1 or ali % 8 == 2 or ali % 8 == 3:
                    Object(ele1, ele_x, ele_y)
                elif ali % 8 == 4 or ali % 8 == 5 or ali % 8 == 6 or ali % 8 == 7:
                    Object(ele2, ele_x, ele_y)
                
                #보트와 악어가 부딫쳤는지
                if y <= ele_y + ele_height and y >= ele_y:
                    if (ele_x <= x <= ele_x + ele_width) or\
                        (ele_x <= x + boat_width <= ele_x + ele_width):
                            state = True
                        
            #악어 위치 초기화
            if ele_y > pad_height:
                ele_y = 0
                ele_x = randrange(0, pad_width - enemy_width)
                e_passed += 1
             
            #통나무
            G_wood += 2.5
            if G_wood >= pad_height:
                Object(wood, wood_x, wood_y)
                wood_y += wood_speed
    
                if y <= wood_y + wood_height and y >= wood_y:
                    if (wood_x <= x <= wood_x + wood_width) or\
                        (wood_x <= x + boat_width <= wood_x + wood_width):
                            state = True
                
            if wood_y > pad_height:
                wood_y = 0
                wood_x = randint(0, pad_width - enemy_width)
                G_wood = 0
                w_passed += 1
                
            ###
            ##보트 흔들림
            if chance == 0:
                if B_a <= 20:
                    if path == 0:
                        if enemypassed == 7:
                            B_plus = -4
                        elif enemypassed == 15:
                            B_plus = -5
                        else:
                            B_plus = -3
                        if B_a < 10:
                            B_plus *= 1.5
                        B_a += B_plus
                        
                    else:
                        B_plus = 2                
                        B_a += B_plus
                
                elif B_a >= 30:
                    if path == 0:
                        B_plus = -2   
                        B_a += B_plus

                    else:
                        if enemypassed == 7:
                            B_plus = 4
                        elif enemypassed == 15:
                            B_plus = 5  
                        else:
                            B_plus = 3
                        if B_a > 40:
                            B_plus *= 1.5
                        B_a += B_plus
                        
                else:
                    if path == 0:
                        B_plus = -2
                        B_a += B_plus
                    else:
                        B_plus = 2
                        B_a += B_plus
            
            if B_a <= 0 or B_a >= 50:       #보트의 침몰
                state = True
            else:                           #각도에 따른 보트의 그림
                if B_a < 20:
                    boat_a = 2
                elif B_a > 30:
                    boat_a = 3
                else:
                    boat_a = 1
                img_boat(boat_a, boat, boat_L, boat_R, x, y)
            ##
        
            #안개가 나오도록    
            if (enemypassed >= 4 and enemypassed <= 9) or (enemypassed >= 16 and enemypassed <= 23):
                cloud_x1 += 7
                cloud_x2 -= 7
                
                if cloud_x1 >= 0:
                    cloud_x1 = 0
                if cloud_x2 <= 0:
                    cloud_x2 = 0
                
                cloud_s = True
                apper_cloud(cloud1,cloud2,cloud_x1,cloud_x2, cloud_s)
        
            elif enemypassed > 5 :
                
                cloud_x1 -= 8
                cloud_x2 += 8
                
                apper_cloud(cloud1,cloud2,cloud_x1,cloud_x2, cloud_s)
                if cloud_x1 < -512:
                    cloud_s = False
        if state:
            Object(ele1, ele_x, ele_y)
            Object(wood, wood_x, wood_y)
            apper_cloud(cloud1,cloud2,cloud_x1,cloud_x2, cloud_s)
                
        B_state(B_a)
        
        #리셋버튼
        if state:
            button = Button(i_button, 200, 530, reset)
            gameover(enemypassed, e_passed, w_passed)
            button.draw()
            
        Passed(enemypassed, e_passed, w_passed)
        pygame.display.update()
        clock.tick(60)
        
    pygame.quit()
    
def initGame():
    global gamepad, clock, boat, boat_L, boat_R, enemy, ele1, ele2, i_button, cloud1, cloud2, wood,\
        game_s
    
    pygame.init()
    gamepad = pygame.display.set_mode((pad_width, pad_height))
    pygame.display.set_caption('Lowing')
    i_button = pygame.image.load('button.png')
    boat = pygame.image.load('boat.png')
    boat_L = pygame.image.load('boat_l.png')
    boat_R = pygame.image.load('boat_r.png')
    enemy = pygame.image.load('rock2.png')
    ele1 = pygame.image.load('ele1.png')
    ele2 = pygame.image.load('ele2.png')
    cloud1 = pygame.image.load('cloud1.png')
    cloud2 = pygame.image.load('cloud2.png')
    wood = pygame.image.load('wood.png')
    game_s = pygame.image.load('start_b.png')
    clock = pygame.time.Clock()
    
initGame()
game_intro()

