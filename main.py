import pygame, os, random, time


#게임 초기화
pygame.init()

# 초기설정
SCREEN_HEIGHT = 370
SCREEN_WIDTH = 910
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 기본 캐릭터
RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "OvenRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "OvenRun2.png"))]

ITEM_RUNNING =[pygame.image.load(os.path.join("Assets/Dino", "OvenRun1Item.png")),
           pygame.image.load(os.path.join("Assets/Dino", "OvenRun2Item.png"))]

JUMPING = pygame.image.load(os.path.join("Assets/Dino", "OvenJump.png"))
ITEM_JUMPING = pygame.image.load(os.path.join("Assets/Dino", "OvenJumpItem.png"))

DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "OvenDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "OvenDuck1.png"))]
ITEM_DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "OvenDuck1Item.png")),
           pygame.image.load(os.path.join("Assets/Dino", "OvenDuck1Item2.png"))]
GAME_OVER = [pygame.image.load(os.path.join("Assets/Dino", "OvenOver.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png"))]

LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))
MENU_BG = pygame.image.load(os.path.join("Assets/Other", "menu.png"))

ITEM = [pygame.image.load(os.path.join("Assets/Item", "star.png")),
        pygame.image.load(os.path.join("Assets/Item", "star2.png"))]

# 공룡동작
class Dinosaur:
    X_POS = 70
    Y_POS = 195
    Y_POS_DUCK = 245
    JUMP_VEL = 8.0
    def __init__(self):
        #이미지 대입
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

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
        #덕킹
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        #다른키 입력해도 달림
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
#구름
class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))
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
#아이템
class Item(Object):

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            items.pop()


# 선인장 장애물, 부모인 Ob를 상속받음
class SmallCactus(Obstacle):
    def __init__(self, image):
        #선인장 타입 3개 랜덤
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
        self.rect.y = 150
        self.index = 0
    
    #날갯짓 0~4는 윗날개 5~9는 아랫날게 10이되면 초기화
    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.imgae[self.index // 5], self.rect)
        self.index += 1

class GameItem(Item):
    def __init__(self, image):
        self.type = random.randint(0, 1)
        super().__init__(image, self.type)
        self.rect.y = 120
    


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, items, count, immortal
    immortal = 1
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    game_speed = 14
    cloud = Cloud()
    x_pos_bg = 0
    y_pos_bg = 0
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    items = []
    death_count = 0
    count = 0

    #무적 지속 시간
    def ImmotalCount():
        global count, immortal
        if immortal == 0:
            player.run_img = ITEM_RUNNING
            player.jump_img = ITEM_JUMPING
            player.duck_img = ITEM_DUCKING
            count += 1
            if count % 250 == 0:
                player.run_img = RUNNING
                player.jump_img = JUMPING
                player.duck_img = DUCKING
                immortal = 1
        
    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        # antialias True로 하면 폰트가 선명해진다. 
        text = font.render("Points: " + str(points), True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (850, 25)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        #백그라운드 그림
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        #실시간으로 변화되는 배경 적용
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
       
       #bg가 x축으로 다 돌면 원상복귀
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        # -14로 x측을 계속 뺀다.
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        SCREEN.fill((255, 255, 255))
        #사용자입력
        userInput = pygame.key.get_pressed()
        background()
        
        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                if immortal:
                    pygame.time.delay(300)
                    death_count += 1
                    menu(death_count)

        # 아이템
        if len(items) == 0:
            #아이템 드랍률
            if random.randint(0, 200) == 0:
                items.append(GameItem(ITEM))

        for item in items:
            item.draw(SCREEN)
            item.update()
            if player.dino_rect.colliderect(item.rect):
                immortal = 0
                

        
        
        #구름
        cloud.draw(SCREEN)
        cloud.update()
        score()
        ImmotalCount()
        #프레임 설정
        clock.tick(30)
        pygame.display.update()



def menu(death_count):
    global points
    run = True
    chara = 0
    while run:
        chara = RUNNING[0]
        font = pygame.font.Font('freesansbold.ttf', 30)
        SCREEN.blit(MENU_BG, (0, 0))
        if death_count == 0:
            text = font.render("->change", True, (255, 255, 255))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (255, 255, 255))
            score = font.render("Your Score : " + str(points), True, (255, 255, 255))
            chara = GAME_OVER[0]
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 130)
            SCREEN.blit(score, scoreRect)
        
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)
        SCREEN.blit(text, textRect)
        SCREEN.blit(chara, (SCREEN_WIDTH // 2-50, SCREEN_HEIGHT // 2-40))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
            #캐릭터 변경 추가 예정
menu(death_count=0)