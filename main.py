import pygame, os, random, time, threading
#게임 초기화
pygame.init()
pygame.mixer.init()
# 초기설정
SCREEN_HEIGHT = 370
SCREEN_WIDTH = 910
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('쿠키런')
# 캐릭터 모션
RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "OvenRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "OvenRun2.png"))]

RUNNING2 = [pygame.image.load(os.path.join("Assets/Dino", "KingRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "KingRun2.png"))]

ITEM_RUNNING =[pygame.image.load(os.path.join("Assets/Dino", "OvenRun1Item.png")),
           pygame.image.load(os.path.join("Assets/Dino", "OvenRun2Item.png"))]
ITEM_RUNNING2 =[pygame.image.load(os.path.join("Assets/Dino", "KingRun1Item.png")),
           pygame.image.load(os.path.join("Assets/Dino", "KingRun2Item.png"))]

JUMPING = pygame.image.load(os.path.join("Assets/Dino", "OvenJump.png"))

JUMPING2 = pygame.image.load(os.path.join("Assets/Dino", "KingJump.png"))

ITEM_JUMPING = pygame.image.load(os.path.join("Assets/Dino", "OvenJumpItem.png"))
ITEM_JUMPING2 = pygame.image.load(os.path.join("Assets/Dino", "KingJumpItem.png"))

DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "OvenDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "OvenDuck1.png"))]

DUCKING2 = [pygame.image.load(os.path.join("Assets/Dino", "KingDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "KingDuck2.png"))]

ITEM_DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "OvenDuck1Item.png")),
           pygame.image.load(os.path.join("Assets/Dino", "OvenDuck1Item.png"))]

ITEM_DUCKING2 = [pygame.image.load(os.path.join("Assets/Dino", "KingDuck1Item.png")),
           pygame.image.load(os.path.join("Assets/Dino", "KingDuck2Item.png"))]

GAME_OVER = [pygame.image.load(os.path.join("Assets/Dino", "OvenOver.png"))]
#장애물
SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png"))]

LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

TOP_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "TopCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "TopCactus2.png"))]

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))
ITEM_BG = pygame.image.load(os.path.join("Assets/Other", "Track2.png"))

MENU_BG = pygame.image.load(os.path.join("Assets/Other", "menu.png"))
MENU_CHARA = [pygame.image.load(os.path.join("Assets/Dino", "menuChara1.png")),
            pygame.image.load(os.path.join("Assets/Dino", "menuChara2.png"))]

ITEM = [pygame.image.load(os.path.join("Assets/Item", "star.png")),
        pygame.image.load(os.path.join("Assets/Item", "drug.png"))]

START_BTN = pygame.image.load(os.path.join("Assets/Other", "start.png"))
END_BTN = pygame.image.load(os.path.join("Assets/Other", "end.png"))

CHANGE_BTN = [pygame.image.load(os.path.join("Assets/Other", "btn_l.png")),
            pygame.image.load(os.path.join("Assets/Other", "btn_r.png"))]

CHARA_CHANGE = 0

FULL_HEART = pygame.image.load(os.path.join("Assets/Other", "full_heart.png"))
EMPTY_HEART = pygame.image.load(os.path.join("Assets/Other", "empty_heart.png"))

COIN = [pygame.image.load(os.path.join("Assets/Other", "coin.png"))]
SCORE_BOARD = pygame.image.load(os.path.join("Assets/Other", "score.png"))
item_hit = False
item2 = False
#사운드
JUMP_SOUND = pygame.mixer.Sound('Assets/Sounds/jump.ogg')
ITEM_SOUND = pygame.mixer.Sound('Assets/Sounds/item.ogg')
COIN_SOUND = pygame.mixer.Sound('Assets/Sounds/coin.ogg')
COIN_SOUND.set_volume(0.4)
DAMAGE_SOUND = pygame.mixer.Sound('Assets/Sounds/damage.ogg')
DAMAGE_SOUND.set_volume(0.4)
END_SOUND = pygame.mixer.Sound('Assets/Sounds/end.ogg')

# 공룡동작
class Dinosaur:
    X_POS = 70
    Y_POS = 195
    Y_POS_DUCK = 245
    JUMP_VEL = 8.0
    
    def __init__(self):
        #이미지 대입
        if CHARA_CHANGE:
            CHANGE = [DUCKING2, RUNNING2, JUMPING2]
        else:
            CHANGE = [DUCKING, RUNNING, JUMPING]

        self.duck_img = CHANGE[0]
        self.run_img = CHANGE[1]
        self.jump_img = CHANGE[2]
        
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        # 런 이미지 초기값
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    # 공룡 상태 확인
    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
            
        # 스텝이 10이 넘어가면 //5로 인해 0 or 1를 넘어가므로 0으로 다시 초기화
        if self.step_index >= 10:
            self.step_index = 0
        #점프
        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
            JUMP_SOUND.play()
            
        #덕킹
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
            
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1
        
    def run(self):
            #달리는 이미지 가변
        self.image = self.run_img[self.step_index // 5]
            #다이노의 직사각형 위치
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            #초기화
            self.jump_vel = self.JUMP_VEL
        
    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


#장애물, 아이템  부모 클래스 이미지 설정, 이동
class Object:
    def __init__(self, image, type):
        self.imgae = image
        self.type = type
        self.rect = self.imgae[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def draw(self, SCREEN):
        SCREEN.blit(self.imgae[self.type], self.rect)


#장애물
class Obstacle(Object):
    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()
        
# 선인장 장애물, 부모인 Ob를 상속받음
class SmallCactus(Obstacle):
    def __init__(self, image):
        #선인장 타입 2개 랜덤
        self.type = random.randint(0, 1)
        super().__init__(image, self.type)
        self.rect.y = 210

class LargeCactus(Obstacle):
    def __init__(self, image):
        #선인장 타입 3개 랜덤
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 210

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.randint(100, 150)
        self.index = 0
    
    #날갯짓 0~4는 윗날개 5~9는 아랫날게 10이되면 초기화
    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.imgae[self.index // 5], self.rect)
        self.index += 1

class TopCactus(Obstacle):
    def __init__(self, image):
        #선인장 타입 2개 랜덤
        self.type = random.randint(0, 1)
        super().__init__(image, self.type)
        self.rect.y = 0

#아이템
class Item(Object):
    
    def draw(self, SCREEN):
        #아이템 먹으면 이미지 제거
        if not item_hit:
            SCREEN.blit(self.imgae[self.type], self.rect)
            
    def update(self):
        global item_hit
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            #화면에서 사라지면 삭제 및 아이템 생성
            if len(items) > 0:
                items.pop()
            item_hit = False

#무적아이템 이미지 그리기
class GameItem(Item):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 120

#마약 아이템
class GameItem2(Item):
    def __init__(self, image):
        self.type = 1
        super().__init__(image, self.type)
        self.rect.y = 30

#코인
class Coin(Object):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 230

    def update(self):
        self.rect.x -= game_speed

#버튼 클릭 이벤트 클래스
class Button:
    def __init__(self, img_in, x, y, width, height, action = None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        SCREEN.blit(img_in,(x,y))
        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            if click[0] and action != None:
                time.sleep(0.5)
                action()

def CharaChangeBtn():
    global CHARA_CHANGE
    if CHARA_CHANGE == 0:
        CHARA_CHANGE = 1
    else:
        CHARA_CHANGE = 0

def StartBtn():
    main()
    
def EndBtn():
    quit()

def main():
    pygame.mixer.music.stop()
    pygame.mixer.music.load('Assets/Sounds/main.ogg')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play()
    #게임배경음 넣을 곳
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, items, count, immortal, item_hit, hearts, hit, coins, c
    immortal = 1
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    game_speed = 14
    x_pos_bg = 0
    y_pos_bg = 0
    points = 0
    hearts = 3
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    items = []
    items2 = []
    coins = []
    death_count = 0
    count = 0
    hit = 1
    c = 0
    #무적 지속 시간
    def ImmotalCount():
        global count, immortal
        changeItem = []
        change = []
        if CHARA_CHANGE:
            changeItem = [ITEM_RUNNING2, ITEM_JUMPING2, ITEM_DUCKING2]
            change = [RUNNING2, JUMPING2, DUCKING2]
        else:
            changeItem = [ITEM_RUNNING, ITEM_JUMPING, ITEM_DUCKING]
            change = [RUNNING, JUMPING, DUCKING]

        if immortal == 0:
            player.run_img = changeItem[0]
            player.jump_img = changeItem[1]
            player.duck_img = changeItem[2]
            count += 1
            if count % 200 == 0:
                player.run_img = change[0]
                player.jump_img = change[1]
                player.duck_img = change[2]
                immortal = 1
    
    def damage():
        global count, hit
        if hit == 0:
            count += 1
            if count % 50 == 0:
                hit = 1
    
    def score():
        global points
        text = font.render(str(points), True, (255, 255, 255))
        #textRect = text.get_rect()
        #extRect.center = (480, 40)
        SCREEN.blit(text, (60, 22))
        SCREEN.blit(COIN[0], (10, 10))
    def heart():
        for heart in range(3):
            x = 790 + (heart * 35)
            if heart < hearts:
                SCREEN.blit(FULL_HEART, (x, 15))
            else:
                SCREEN.blit(EMPTY_HEART,(x, 15))
            
    def background(image):
        global x_pos_bg, y_pos_bg
        image_width = image.get_width()
        #백그라운드 그림
        SCREEN.blit(image, (x_pos_bg, y_pos_bg))
        #실시간으로 변화되는 배경 적용
        SCREEN.blit(image, (image_width + x_pos_bg, y_pos_bg))
       
       #bg가 x축으로 다 돌면 원상복귀
        if x_pos_bg <= -image_width:
            SCREEN.blit(image, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        # -14로 x측을 계속 뺀다.
        x_pos_bg -= game_speed

    def coinzen():
        global c
        c += 1
        if c % 10 == 0:
            coins.append(Coin(COIN))
            c = 0
        

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        SCREEN.fill((255, 255, 255))
        #사용자입력
        userInput = pygame.key.get_pressed()
        background(BG)
        
        player.draw(SCREEN)
        player.update(userInput)

        #1로 바꾸면 안뜸
        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))
            elif random.randint(0, 1) == 0:
                obstacles.append(TopCactus(TOP_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                # 무적아이템과 데미지 입었을때 무적이 되어야하기에 and
                if immortal and hit:
                    pygame.time.delay(300)
                    DAMAGE_SOUND.play()
                    hit = 0
                    hearts -= 1
                    if hearts == 0:
                        END_SOUND.play()
                        death_count += 1
                        menu(death_count)

        # 아이템
        if len(items) == 0 or len(items2) == 0:
            #아이템 드랍률
            if random.randint(0, 300) == 0:
                items.append(GameItem(ITEM))
            if random.randint(0, 1000) == 0:
                items2.append(GameItem2(ITEM))

        for item in items:
            item.draw(SCREEN)
            item.update()
            if player.dino_rect.colliderect(item.rect):
                immortal = 0
                item_hit = True
                ITEM_SOUND.play()
        
        
        #코인
        coinzen()

        #코인 충돌 이벤트
        for coin in coins:
            coin.draw(SCREEN)
            coin.update()
            if player.dino_rect.colliderect(coin.rect):
                COIN_SOUND.play()
                coins.pop(0)
                points += 10

        #마약 아이템
        for item in items2:
            item.draw(SCREEN)
            item.update()
            if player.dino_rect.colliderect(item.rect):
                item_hit = True
                background(ITEM_BG)
                ITEM_SOUND.play()
                player.draw(SCREEN)
                pygame.time.delay(300)

        
        score()
        heart()
        damage()
        ImmotalCount()
        #프레임 설정
        clock.tick(30)
        pygame.display.update()

def menu(death_count):
    global points
    menu = True
    chara = 0
    pygame.mixer.music.stop()
    pygame.mixer.music.load('Assets/Sounds/lobby.ogg')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play()
    
    while menu:
        
        global CHARA_CHANGE
        chara = RUNNING[0]
        font = pygame.font.Font('freesansbold.ttf', 30)

        SCREEN.blit(MENU_BG, (0, 0))
        
        if CHARA_CHANGE:
            chara = MENU_CHARA[1]
        else:
            chara = MENU_CHARA[0]
        
        if death_count > 0:
            score = font.render("SCORE : " + str(points), True, (255, 255, 255))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 145)
            SCREEN.blit(SCORE_BOARD, (SCREEN_WIDTH // 2 - 170, 10))
            SCREEN.blit(score, scoreRect)
        
        SCREEN.blit(chara, (SCREEN_WIDTH // 2-60, SCREEN_HEIGHT // 2-40))

        Button(CHANGE_BTN[0], SCREEN_WIDTH // 2-170, SCREEN_HEIGHT // 2-100, 177,88, CharaChangeBtn)

        Button(CHANGE_BTN[1],SCREEN_WIDTH // 2+50,SCREEN_HEIGHT // 2-100, 177,88,CharaChangeBtn)
        Button(END_BTN,SCREEN_WIDTH // 2-370,SCREEN_HEIGHT // 2+50, 137,78,EndBtn)
        Button(START_BTN,SCREEN_WIDTH // 2+250,SCREEN_HEIGHT // 2+50, 137,78,StartBtn)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                EndBtn()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    CHARA_CHANGE = 1
                elif event.key == pygame.K_RIGHT:
                    CHARA_CHANGE = 0
                elif event.key == pygame.K_UP:
                    main()

menu(death_count=0)
