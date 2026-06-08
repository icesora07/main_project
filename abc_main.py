import pygame, math, time, random

pygame.init()
WIDTH = 500
HEIGHT = 800
FPS = 60
ACCELERATION = 1

MAIN = 0
GAME = 1
GAME_READY = 2
GAME_CLEAR = 3
state = MAIN

ing = False

s_items = []
attacks = []
monsters = []
boss_attacks = []
boss_follow_attacks = []
removed_attacks = set()
removed_monsters = set()
removed_s_items = set()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("lapis lazuli hoopoe")
clock = pygame.time.Clock()

ATTACK_TIME = pygame.USEREVENT + 1 
pygame.time.set_timer(ATTACK_TIME, 50)

MONSTER_TIME = pygame.USEREVENT + 2
pygame.time.set_timer(MONSTER_TIME, 2000)

BOSS_F_MONSTER_TIME = pygame.USEREVENT + 3
pygame.time.set_timer(BOSS_F_MONSTER_TIME, 120)

BOSS_F_1_ATTACK_TIME = pygame.USEREVENT + 4
pygame.time.set_timer(BOSS_F_1_ATTACK_TIME, 700)

BOSS_F_3_TIME = pygame.USEREVENT + 5
pygame.time.set_timer(BOSS_F_3_TIME, 2000)

BOSS_F_3_ATTACK_TIME = pygame.USEREVENT + 6
pygame.time.set_timer(BOSS_F_3_ATTACK_TIME, 200)

BOSS_F_4_ATTACK_TIME = pygame.USEREVENT + 7
pygame.time.set_timer(BOSS_F_4_ATTACK_TIME, 1000)

invincible = False
boss_invincible = False
boss_fight = False
magnet = False

score = 0
max_score = 0

main_RGB_CK = [False, False, False]
main_RGB = [255, 255, 255]

boss_hp_bar_RGB = [0, 0, 0]

score_item_hitbox = 16

player_hitbox = 10
player_x = WIDTH // 2
player_y = HEIGHT // 2 + 250
player_hp = 1
player_damage = 10

attack_hitbox = 32

boss_hitbox = 54
boss_x = WIDTH // 2
boss_y = -100
boss_speed_x = 0
boss_speed_y = 3
boss_hp = 13000
BOSS_HP = boss_hp
boss_level = 0
boss_move_y = False
boss_attack_hitbox = 16

monster_speed = 10
monster_x = 50
monster_y = -100
monster_hitbox = 25
monster_hp = 10

level = 0
level_check = 0

world_y = -800
world_y_ = -2400

img_boss = pygame.image.load('lala_boss.png')
img_boss_mb = pygame.image.load('boss_mb.png')
img_boss_attack_mb = pygame.image.load('boss_attack_mb.png')
img_score_item = "score_item.png"
img_e_score_item = "e_score_item.png"
img_attack = 'attack.png'
img_monster_1 = 'monday_bird.png'
img_boss_attack = "boss_attack.png"

img_player = [
    pygame.image.load('hoopt1.png'),
    pygame.image.load('hoopt2.png'),
    pygame.image.load('hoopt3.png'),
    pygame.image.load('hoopt4.png'),
    pygame.image.load('hoopt5.png'),
    pygame.image.load('hoopt3.png'),
    pygame.image.load('hoopt2.png')
]

img_item = [
    pygame.image.load('ax.png'),
    pygame.image.load('earthenware.png'),
    pygame.image.load('sangpyeongtongbo.png')
]

img_world = pygame.image.load('world.png')

player_anim = 0
anim_time = 0

font_title = pygame.font.SysFont('Comic Sans MS', 50, bold=True)
font_title_outline = pygame.font.SysFont('Comic Sans MS', 55, bold=True)
font_main = pygame.font.SysFont('Comic Sans MS', 70, bold=True)
font_score = pygame.font.SysFont('Comic Sans MS', 40, bold=True)
font_level = pygame.font.SysFont('Comic Sans MS', 40, bold=True)
font_desc = pygame.font.SysFont("malgungothic", 20, bold=True)

class Monster():
    def __init__(self, speed, hp, level, hitbox, x, y, img):
        self.speed = speed * (1 + 0.05 * level)
        self.hp = hp * (1 + 0.2 * level)
        self.hitbox = hitbox
        self.x = x
        self.y = y
        self.img = pygame.image.load(img)

    def move(self):
        self.y += self.speed

    def draw(self):
        screen.blit(self.img, (self.x - 32, self.y - 32))

    def hp_down(self, player_damage):
        self.hp -= player_damage
        return self.hp

class S_item():
    def __init__(self, hitbox, x, y, img, img_e):
        self.hitbox = hitbox
        self.speed_x = random.randint(-3, 3)
        self.x = x
        self.y = y
        self.speed_y = -15
        self.rand = random.randint(1, 5)
        self.img = pygame.image.load(img)
        self.img_e = pygame.image.load(img_e)

    def move(self):
        self.x += self.speed_x
        self.speed_y += ACCELERATION - 0.5
        self.y += self.speed_y

        if self.x < self.hitbox:
            self.x = self.hitbox
        if self.x > WIDTH - self.hitbox:
            self.x = WIDTH - self.hitbox

    def draw(self):
        if self.rand == 1:
            screen.blit(self.img_e, (self.x - self.hitbox, self.y - self.hitbox))
        else:
            screen.blit(self.img, (self.x - self.hitbox, self.y - self.hitbox))

class Attack:
    def __init__(self, speed, hitbox, x, y, img):
        self.speed = speed
        self.hitbox = hitbox
        self.x = x
        self.y = y
        self.img = pygame.image.load(img)
        
    def move(self):
        self.y -= self.speed
    
    def draw(self, screen):
        screen.blit(self.img, (self.x - self.hitbox, self.y - self.hitbox))
    
class Boss_Attack:
    def __init__(self, speed_x, speed_y, hitbox, x, y, img):
        self.hitbox = hitbox
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.img = pygame.image.load(img)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
    
    def draw(self, screen):
        screen.blit(self.img, (self.x - self.hitbox, self.y - self.hitbox))

class Boss_Follow_Attack:
    def __init__(self, speed, hitbox, x, y, target_x, target_y, img):
        self.hitbox = hitbox
        self.x = x
        self.y = y
        self.speed = speed
        self.dx = target_x - x
        self.dy = target_y - y
        self.img = pygame.image.load(img)
        
    def move(self):
        distance = math.sqrt(self.dx**2 + self.dy**2)
        if distance != 0:
            self.vx = (self.dx / distance) * self.speed
            self.vy = (self.dy / distance) * self.speed
        else:
            self.vx = 0
            self.vy = self.speed
        self.x += self.vx
        self.y += self.vy
    
    def draw(self, screen):
        screen.blit(self.img, (self.x - self.hitbox, self.y - self.hitbox))

def crash(x, y, size, x_, y_, size_):
    n_x = 0
    n_y = 0
    ck_num = 0
    n_x = x - x_
    n_y = y_ - y
    
    ck_num = math.sqrt(n_x**2 + n_y**2)
    if ck_num < size + size_:
        return True
    else:
        return False
    
def euclidean_distance(x, y, x_, y_):
    n_x = 0
    n_y = 0
    ck_num = 0
    n_x = x - x_
    n_y = y_ - y
    
    ck_num = math.sqrt(n_x**2 + n_y**2)
    return ck_num

def player_move(x, y, size, mouse_x):
    global anim_time
    global player_anim

    if size < mouse_x < WIDTH - size:
        x = mouse_x
    elif WIDTH - size > mouse_x:
        x = size 
    elif size < mouse_x:
        x = WIDTH - size

    screen.blit(img_player[player_anim], (x - 64, y - 60))
    if anim_time == 2:
        anim_time = 0
        player_anim += 1
        player_anim %= 7
    else:
        anim_time += 1

    return x, y

def world_draw(x, y, y_, size, speed_y, mouse_x):
    if size < mouse_x < WIDTH - size:
        x = -mouse_x / 25 - 50

    elif WIDTH - size > mouse_x:
        x = -50
    elif size < mouse_x:
        x = -70

    y += speed_y
    y_ += speed_y

    if y >= HEIGHT:
        y -= 3200
    if y_ >= HEIGHT:
        y_ -= 3200

    screen.blit(img_world, (x, y))
    screen.blit(img_world, (x, y_))

    return y, y_

def hp_bar():
    x = boss_hp // WIDTH - 30
    boss_hp_bar = boss_hp // x
    return boss_hp_bar

def boss_start(y, speed_y):
    speed_y -= 0.02
    y += speed_y
    return y, speed_y

def boss_idle(boss_y, boss_speed_y, boss_move_y):
    if boss_speed_y >= 0.6:
        boss_move_y = False
    elif boss_speed_y <= -0.6:
        boss_move_y = True

    if boss_move_y == False:
        boss_speed_y -= 0.02

    elif boss_move_y == True:
        boss_speed_y += 0.02

    boss_y -= boss_speed_y
    return boss_y, boss_speed_y, boss_move_y


def boss_fight_2(monster_x, sp_rule):
    if monster_x <= 50:
        sp_rule = 0
    elif monster_x >= 450:
        sp_rule = 1
    if sp_rule == 0:
        monster_x += 100
    elif sp_rule == 1:
        monster_x -= 100
    return monster_x, sp_rule

running = True
while running:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()

    if state == MAIN:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if ing == False:
            screen.fill((10, 0, 5))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 155 < mouse_x < 345 and 400 < mouse_y < 460:
                    if ing == False:
                        item_choice = 0
                        state = GAME_READY
                    else:
                        state = GAME

        if max_score < score:
            max_score = score

        for i in range(3):
            if main_RGB_CK[i] == True:
                main_RGB[i] += 1 + i
            else:
                main_RGB[i] -= 3 - i
            if main_RGB[i] >= 255:
                main_RGB[i] = 255
                main_RGB_CK[i] = False
            elif main_RGB[i] <= 50:
                main_RGB[i] = 50
                main_RGB_CK[i] = True

        title = font_title.render("START", True, (60, 40, 100))
        main_text_1 = font_main.render("hoopoe fly", True, (main_RGB))
        score_text_1 = font_score.render("HIGH SCORE", True, (255, 200, 30))
        score_text_2 = font_score.render(f"<{int(max_score)}>", True, (255, 230, 100))

        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 10))
        screen.blit(main_text_1, (WIDTH//2 - main_text_1.get_width()//2, HEIGHT//2 - 150))
        if score > 0:
            screen.blit(score_text_1, (WIDTH//2 - score_text_1.get_width()//2, HEIGHT//2 + 100))
            screen.blit(score_text_2, (WIDTH//2 - score_text_2.get_width()//2, HEIGHT//2 + 150))
        if 155 < mouse_x < 345 and 400 < mouse_y < 460:
            title_outline = font_title_outline.render("START", True, (10, 60, 170))
            screen.blit(title_outline, (WIDTH//2 - title_outline.get_width()//2, HEIGHT//2 - 12))
        else:
            title_outline = font_title_outline.render("START", True, (50, 150, 250))
            screen.blit(title_outline, (WIDTH//2 - title_outline.get_width()//2, HEIGHT//2 - 10))

    elif state == GAME_READY:
        screen.fill((20, 0, 20))
        player_hp = 1
        player_damage = 10
        score = 0
        magnet = False
        invincible = False
        boss_fight = False
        boss_move_y = False
        boss_level = 0
        boss_speed_y = 3
        boss_y = -100
        boss_speed_x = 0
        boss_hp = BOSS_HP
        boss_3_attack = False
        level = 1

        for i in range(3):
            if main_RGB_CK[i] == True:
                main_RGB[i] += 1 + i
            else:
                main_RGB[i] -= 3 - i
            if main_RGB[i] >= 255:
                main_RGB[i] = 255
                main_RGB_CK[i] = False
            elif main_RGB[i] <= 50:
                main_RGB[i] = 50
                main_RGB_CK[i] = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    item_choice -= 1
                    if item_choice == -1:
                        item_choice = 2
                if event.key == pygame.K_RIGHT:
                    item_choice += 1
                    if item_choice == 3:
                        item_choice = 0

        pygame.draw.rect(screen, (30, 30, 70), [20, 20, 460, 470])
        pygame.draw.rect(screen, (0, 150, 250), [20, 20, 460, 470], 3)
        for i in range(3):
            pygame.draw.rect(screen, (50, 50, 50), [50 + i * 150, 650, 100, 100])
            pygame.draw.rect(screen, (100, 100, 100), [50 + i * 150, 650, 100, 100], 2)
            screen.blit(img_item[i], (50 + i * 150, 650))

        if (item_choice == 0):
            name = "주먹도끼"
            effect = "효과: 공격력 1.5배 증가"
            desc = "구석기 시대를 대표하는 만능\n도구이자 인류 최초의 맥가이버\n칼입니다. 짐승을 사냥하는\n공격적인 용도뿐만 아니라,\n가죽을 벗기고 뼈를 깎는 등\n다양한 생존 활동에 활용된\n강력한 타격력을 상징합니다."
            pygame.draw.rect(screen, (255, 255, 255), [50, 650, 100, 100], 4)
        elif (item_choice == 1):
            name = "빗살무늬 토기"
            effect = "효과: 최대 체력 3으로 증가"
            desc = "신석기 시대의 혁명적 발명품\n입니다. 밑바닥이 뾰족한 포탄\n모양으로 만들어져 강가나 바닷가\n모래에 꽂아 썼습니다. 탄화된\n도토리와 곡물을 안전하게 저장\n하고 조리할 수 있게 되면서\n정착 생활과 인류의 생존력을\n획기적으로 높여주었습니다."
            pygame.draw.rect(screen, (255, 255, 255), [200, 650, 100, 100], 4)
        elif (item_choice == 2):
            name = "상평통보"
            effect = "효과: 자석 효과 (아이템 흡수)"
            desc = "조선 숙종 4년(1678년)에\n발행되어 말기까지 약 2세기\n동안 전국에서 쓰인 유일한\n법화입니다. 17세기 상공업\n발달과 함께 조선 팔도의 모든\n재화와 돈을 강력하게 끌어\n모았던 실제 경제 역사적 특징을\n살려, 주변의 아이템을 자석처럼\n당겨오는 효과를 부여합니다."
            pygame.draw.rect(screen, (255, 255, 255), [350, 650, 100, 100], 4)

        screen.blit(font_desc.render(name, True, (255, 215, 0)), (40, 50))
        screen.blit(font_desc.render(effect, True, (100, 200, 255)), (40, 95))

        k_text = font_score.render("<<  >>", True, (250, 250, 250))
        screen.blit(k_text, (WIDTH//2 - k_text.get_width()//2, HEIGHT//2 + 170))

        et_text = font_score.render("[ENTER]", True, (main_RGB))
        screen.blit(et_text, (WIDTH//2 - et_text.get_width()//2, HEIGHT//2 + 100))
        
        text_y = 150
        for line in desc.split("\n"):
            screen.blit(font_desc.render(line, True, (230, 230, 230)), (40, text_y))
            text_y += 25

        if keys[pygame.K_RETURN]:
            state = GAME
            if (item_choice == 0):
                player_damage = 15
            elif (item_choice == 1):
                player_hp = 3
            elif (item_choice == 2):
                magnet = True
        elif keys[pygame.K_ESCAPE]:
            state = MAIN

    elif state == GAME:
        ing = True
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == ATTACK_TIME:
                attacks.append(Attack(25, attack_hitbox, player_x, player_y, img_attack))
            if event.type == MONSTER_TIME and boss_fight == False:
                monster_x = 50
                level_check += 1
                if level_check % 5 == 0:
                    level_check = 0
                    level += 1
                if level >= 10:
                    boss_fight = True
                for i in range(5):
                    monsters.append(Monster(monster_speed, monster_hp, level, monster_hitbox, monster_x, monster_y, img_monster_1))
                    monster_x += 100
            if event.type == BOSS_F_1_ATTACK_TIME and boss_level == 1:
                if boss_1_attack_num == 0:
                    boss_1_attack_num = 1
                    boss_attacks.append(Boss_Attack(0, 5, boss_attack_hitbox, boss_x - 75, BOSS_Y - 50, img_boss_attack))
                    boss_attacks.append(Boss_Attack(0, 5, boss_attack_hitbox, boss_x + 75, BOSS_Y - 50, img_boss_attack))
                    boss_attacks.append(Boss_Attack(0, 5, boss_attack_hitbox, boss_x - 225, BOSS_Y - 50, img_boss_attack))
                    boss_attacks.append(Boss_Attack(0, 5, boss_attack_hitbox, boss_x + 225, BOSS_Y - 50, img_boss_attack))
                elif boss_1_attack_num == 1:
                    boss_1_attack_num = 0
                    boss_attacks.append(Boss_Attack(0, 5, boss_attack_hitbox, boss_x, BOSS_Y, img_boss_attack))
                    boss_attacks.append(Boss_Attack(0, 5, boss_attack_hitbox, boss_x - 150, BOSS_Y, img_boss_attack))
                    boss_attacks.append(Boss_Attack(0, 5, boss_attack_hitbox, boss_x + 150, BOSS_Y, img_boss_attack))
                    boss_follow_attacks.append(Boss_Follow_Attack(2, boss_attack_hitbox, boss_x, boss_y, player_x, player_y, img_boss_attack))
            
            if event.type == BOSS_F_3_TIME and boss_level == 2:
                for i in range(4):
                    for k in range(4):
                        boss_attacks.append(Boss_Attack(1.5 - i, 4 - k, boss_attack_hitbox, boss_x, boss_y, img_boss_attack))

            if event.type == BOSS_F_MONSTER_TIME and boss_level == 2:
                monsters.append(Monster(monster_speed, monster_hp, level, monster_hitbox, monster_x, monster_y, img_monster_1))
                monster_x, sp_rule = boss_fight_2(monster_x, sp_rule)

                
            if event.type == BOSS_F_3_TIME and boss_level == 3:
                boss_3_attack = True
                boss_3_attack_num = 0
            if boss_3_attack == True:
                if boss_3_attack_num != 5:
                    if event.type == BOSS_F_3_ATTACK_TIME:
                        boss_3_attack_num += 1
                        boss_follow_attacks.append(Boss_Follow_Attack(4, boss_attack_hitbox, boss_x - 150, BOSS_Y, player_x, player_y, img_boss_attack))
                        boss_follow_attacks.append(Boss_Follow_Attack(4, boss_attack_hitbox, boss_x + 150, BOSS_Y, player_x, player_y, img_boss_attack))
                        boss_follow_attacks.append(Boss_Follow_Attack(5, boss_attack_hitbox, boss_x - 50, BOSS_Y - 100, player_x, player_y, img_boss_attack))
                        boss_follow_attacks.append(Boss_Follow_Attack(5, boss_attack_hitbox, boss_x + 50, BOSS_Y - 100, player_x, player_y, img_boss_attack))
                else:
                    boss_3_attack = False
            if event.type == BOSS_F_4_ATTACK_TIME and boss_level == 4:
                bullet_count = 24
                bullet_speed = 3
                for i in range(bullet_count):
                    angle_deg = i * (360 / bullet_count) 
                    angle_rad = math.radians(angle_deg)
                    c_speed_x = math.cos(angle_rad) * bullet_speed
                    s_speed_y = math.sin(angle_rad) * bullet_speed

                    boss_attacks.append(Boss_Attack(c_speed_x / 2, s_speed_y / 2, boss_attack_hitbox, boss_x, BOSS_Y, img_boss_attack))
                    if boss_1_attack_num == 0:
                        boss_attacks.append(Boss_Attack(c_speed_x, s_speed_y, boss_attack_hitbox, boss_x - 150, BOSS_Y, img_boss_attack))
                    elif boss_1_attack_num == 1:
                        boss_attacks.append(Boss_Attack(c_speed_x, s_speed_y, boss_attack_hitbox, boss_x + 150, BOSS_Y, img_boss_attack))
                if boss_1_attack_num == 0:
                    boss_1_attack_num = 1
                elif boss_1_attack_num == 1:
                    boss_1_attack_num = 0
                    boss_follow_attacks.append(Boss_Follow_Attack(3, boss_attack_hitbox, boss_x, boss_y, player_x, player_y, img_boss_attack))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        world_y, world_y_ = world_draw(player_x, world_y, world_y_, player_hitbox, 2 + monster_speed * (0.01 * level), mouse_x)

        if boss_fight == True and boss_hp > 0:
            boss_hp_bar = boss_hp / (BOSS_HP / (WIDTH - 30))
            boss_hp_bar_s = BOSS_HP / (BOSS_HP / (WIDTH - 30))
            
            if boss_level == 0:
                screen.blit(img_boss_mb, (boss_x - 64, boss_y - 64))
                screen.blit(img_boss, (boss_x - 64, boss_y - 70))
                boss_y, boss_speed_y = boss_start(boss_y, boss_speed_y)
                if boss_speed_y <= 0:
                    boss_speed_y = 0
                    BOSS_Y = boss_y
                    boss_1_attack_num = 0
                    boss_level = 1

            elif boss_level == 1:
                boss_hp_bar_RGB = [30, 155, 225]
                screen.blit(img_boss_attack_mb, (boss_x - 48 - 75, BOSS_Y - 48 - 50))
                screen.blit(img_boss_attack_mb, (boss_x - 48 + 75, BOSS_Y - 48 - 50))
                screen.blit(img_boss_attack_mb, (boss_x - 48 - 225, BOSS_Y - 48 - 50))
                screen.blit(img_boss_attack_mb, (boss_x - 48 + 225, BOSS_Y - 48 - 50))

                screen.blit(img_boss_attack_mb, (boss_x - 48, BOSS_Y - 48))
                screen.blit(img_boss_attack_mb, (boss_x - 48 - 150, BOSS_Y - 48))
                screen.blit(img_boss_attack_mb, (boss_x - 48 + 150, BOSS_Y - 48))
                if BOSS_HP * 3 // 4 >= boss_hp:
                    boss_level = 2
                    monster_x = 50
                    sp_rule = 0

            elif boss_level == 2:
                for i in range(3):
                    if boss_hp_bar_RGB[i] < 20 and i == 0 or boss_hp_bar_RGB[i] < 255 and i == 1 or boss_hp_bar_RGB[i] < 55 and i == 2:
                        boss_hp_bar_RGB[i] += 1
                    elif boss_hp_bar_RGB[i] > 100 and i == 0 or boss_hp_bar_RGB[i] > 255 and i == 1 or boss_hp_bar_RGB[i] > 55 and i == 2:
                        boss_hp_bar_RGB[i] -= 1
                if BOSS_HP * 2 // 4 >= boss_hp:
                    boss_3_attack = True
                    boss_3_attack_num = 0
                    boss_level = 3

            elif boss_level == 3:
                for i in range(3):
                    if boss_hp_bar_RGB[i] < 255 and i == 0 or boss_hp_bar_RGB[i] < 255 and i == 1 or boss_hp_bar_RGB[i] < 5 and i == 2:
                        boss_hp_bar_RGB[i] += 1
                    elif boss_hp_bar_RGB[i] > 255 and i == 0 or boss_hp_bar_RGB[i] > 255 and i == 1 or boss_hp_bar_RGB[i] > 5 and i == 2:
                        boss_hp_bar_RGB[i] -= 1
                screen.blit(img_boss_attack_mb, (boss_x - 48 + 150, BOSS_Y - 48))
                screen.blit(img_boss_attack_mb, (boss_x - 48 - 150, BOSS_Y - 48))
                screen.blit(img_boss_attack_mb, (boss_x - 48 + 50, BOSS_Y - 48 - 100))
                screen.blit(img_boss_attack_mb, (boss_x - 48 - 50, BOSS_Y - 48 - 100))
                if BOSS_HP * 1 // 4 >= boss_hp:
                    boss_level = 4
            
            elif boss_level == 4:
                for i in range(3):
                    if boss_hp_bar_RGB[i] < 200 and i == 0 or boss_hp_bar_RGB[i] < 55 and i == 1 or boss_hp_bar_RGB[i] < 25 and i == 2:
                        boss_hp_bar_RGB[i] += 1
                    elif boss_hp_bar_RGB[i] > 200 and i == 0 or boss_hp_bar_RGB[i] > 55 and i == 1 or boss_hp_bar_RGB[i] > 25 and i == 2:
                        boss_hp_bar_RGB[i] -= 1
                screen.blit(img_boss_attack_mb, (boss_x - 48 - 150, BOSS_Y - 48))
                screen.blit(img_boss_attack_mb, (boss_x - 48 + 150, BOSS_Y - 48))

            if boss_level > 0:
                pygame.draw.rect(screen, (25, 25, 25), [15, 15, boss_hp_bar_s, 20])
                pygame.draw.rect(screen, boss_hp_bar_RGB, [15, 15, boss_hp_bar, 20])
                pygame.draw.rect(screen, (45, 15, 5), [15, 15, WIDTH - 30, 20], 3)
                for boss_attack in boss_attacks:
                    if crash(player_x, player_y, player_hitbox, boss_attack.x, boss_attack.y, boss_attack.hitbox) == True and invincible == False:
                        player_hp -= 1
                        boss_attacks = []
                        boss_follow_attacks = []
                        for i in range(200):
                            pygame.draw.circle(screen, (255, 255, 255), (player_x, player_y), 10 * i, 3)
                for boss_follow_attack in boss_follow_attacks:
                    if crash(player_x, player_y, player_hitbox, boss_follow_attack.x, boss_follow_attack.y, boss_follow_attack.hitbox) == True and invincible == False:
                        player_hp -= 1
                        boss_attacks = []
                        boss_follow_attacks = []
                        for i in range(200):
                            pygame.draw.circle(screen, (255, 255, 255), (player_x, player_y), 10 * i, 3)
                for boss_attack in boss_attacks:
                    boss_attack.move()
                    boss_attack.draw(screen)
                for boss_follow_attack in boss_follow_attacks:
                    boss_follow_attack.move()
                    boss_follow_attack.draw(screen)
                screen.blit(img_boss_mb, (boss_x - 64, boss_y - 64))
                screen.blit(img_boss, (boss_x - 64, boss_y - 70))
                boss_y, boss_speed_y, boss_move_y = boss_idle(boss_y, boss_speed_y, boss_move_y)
                for attack in attacks:
                    if crash(attack.x, attack.y, attack.hitbox, boss_x, boss_y, boss_hitbox) == True:
                        removed_attacks.add(attack)
                        boss_hp -= player_damage

        for attack in attacks:
            attack.move()
            attack.draw(screen)

        color = (255, 255, 255)
        for monster in monsters:
            if crash(player_x, player_y, player_hitbox, monster.x, monster.y, monster.hitbox) == True and invincible == False:
                player_hp -= 1
                monsters = []
                for i in range(200):
                    pygame.draw.circle(screen, (255, 255, 255), (player_x, player_y), 10 * i, 3)
            monster.move()
            monster.draw()

        if player_hp < 1:
            attacks = []
            s_items = []
            monsters = []
            boss_attacks = []
            boss_follow_attacks = []
            ing = False
            level = 1
            time.sleep(1)
            state = MAIN

        for s_item in s_items:
            if magnet == True:
                if euclidean_distance(player_x, player_y, s_item.x, s_item.y) < 200:
                    if s_item.y < player_y and s_item.speed_y > 30:
                        s_item.speed_y -= 7
                    elif s_item.y > player_y and s_item.speed_y > 0:
                        s_item.speed_y = -2
                    elif s_item.y > player_y:
                        s_item.speed_y -= 3

                    if s_item.speed_y > 0:
                        if s_item.x < player_x - 10:
                            s_item.speed_x += s_item.speed_y
                        elif s_item.x > player_x + 10:
                            s_item.speed_x -= s_item.speed_y
                    else:
                        if s_item.x < player_x - 10:
                            s_item.speed_x -= s_item.speed_y
                        elif s_item.x > player_x + 10:
                            s_item.speed_x += s_item.speed_y

                    if player_x + 20 > s_item.x > player_x - 20:
                        s_item.speed_x = 0
                        s_item.x = player_x

                    if player_y > s_item.y > player_y - 10:
                        s_item.speed_y = 0
                        s_item.y = player_y

                    if s_item.y < player_y and s_item.speed_y < 0:
                        s_item.speed_y *= -1

                    if s_item.speed_x > 25:
                        s_item.speed_x = 25
                    if s_item.speed_x < -25:
                        s_item.speed_x = -25

                    if s_item.speed_y > 30:
                        s_item.speed_y = 30
                    if s_item.speed_y < -30:
                        s_item.speed_y = -30
                                
            if crash(player_x, player_y, player_hitbox, s_item.x, s_item.y, 40) == True:
                if s_item.rand == 1:
                    score += 30000 * (1 + level * 0.3)
                else:
                    score += 10000 * (1 + level * 0.3)
                removed_s_items.add(s_item)
            s_item.move()
            s_item.draw()

        for attack in attacks:
            for monster in monsters:
                if crash(attack.x, attack.y, attack.hitbox, monster.x, monster.y, monster.hitbox) == True:
                    if monster.hp_down(player_damage) <= 0:
                        if boss_fight == False:
                            s_items.append(S_item(score_item_hitbox, monster.x, monster.y, img_score_item, img_e_score_item))
                            score += 9000 * (1 + level * 0.1)
                        removed_monsters.add(monster)
                    removed_attacks.add(attack)

        score += (level + 1) * 30
        score_font = font_score.render(f"score {int(score)}", True, (130, 20, 40))
        screen.blit(score_font, (20, HEIGHT - 15 - score_font.get_height()))

        level_font = font_level.render(f"level {level}", True, (170, 20, 10))
        screen.blit(level_font, (20, HEIGHT - 60 - score_font.get_height()))

        attacks = [a for a in attacks if a not in removed_attacks]
        monsters = [m for m in monsters if m not in removed_monsters]
        s_items = [s for s in s_items if s not in removed_s_items]

        attacks = [a for a in attacks if a.y >= -a.hitbox]
        monsters = [m for m in monsters if m.y <= HEIGHT + 100]
        s_items = [s for s in s_items if s.y <= HEIGHT + 100]
        boss_attacks = [ba for ba in boss_attacks if ba.y <= HEIGHT + 100 and ba.y >= -100 and ba.x <= WIDTH + 100 and ba.x >= -100]
        boss_follow_attacks = [bfa for bfa in boss_follow_attacks if bfa.y <= HEIGHT + 100 and bfa.y >= -100 and bfa.x <= WIDTH + 100 and bfa.x >= -100]
        
        player_x, player_y = player_move(player_x, player_y, player_hitbox, mouse_x)

        if boss_hp <= 0:
                ing = False
                boss_level = 0
                boss_fight = False
                time.sleep(1)
                state = GAME_CLEAR

        # 임시 (보스 테스트 용도)
        if keys[pygame.K_n]:
            level += 1
            if level > 10:
                level = 10

        if keys[pygame.K_ESCAPE]:
            state = MAIN

    elif state == GAME_CLEAR:
        screen.fill((0, 0, 0))
        title = font_title.render("CLEAR!!", True, (240, 100, 25))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2))
        pygame.display.update()
        time.sleep(2)
        state = MAIN

    pygame.display.update()
pygame.quit()