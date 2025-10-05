global score  # inserted
import pygame
import random
import time
import os
import sys
import requests
try:
    import getpass
    username = getpass.getuser()
except Exception:
    username = 'player'

def wrap_text(text, max_chars=21):
    wrapped_lines = []
    for line in text.split('\n'):
        words = line.split()
        current_line = ''
        for word in words:
            if len(current_line) + len(word) + (1 if current_line else 0) > max_chars:
                wrapped_lines.append(current_line)
                current_line = word
            else:  # inserted
                current_line = word if not current_line else current_line + ' ' + word
        if current_line:
            wrapped_lines.append(current_line)
    return '\n'.join(wrapped_lines)
pygame.init()
icon = pygame.image.load('icon.ico')
pygame.display.set_icon(icon)
WIDTH, HEIGHT = (800, 600)
FRAME_DURATION = 600
SPRITE_SIZE = (200, 200)
FALL_SPEED = 7
MOVE_OFFSET = 100
FPS = 60
MAX_HEALTH = 5
FONT_SIZE = 48
TEXT_SPEED = 200
font = pygame.font.Font('assets/fonts/ByteBounce.ttf', FONT_SIZE)

def load_frames(paths, size):
    try:
        return [pygame.transform.scale(pygame.image.load(path), size) for path in paths]
    except pygame.error as e:
        print(f'Error loading frames: {e}')
        return []

def get_user_country():
    try:
        response = requests.get('http://ip-api.com/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            country = data.get('country')
            if country:
                return country
        return 'your place'
        return 'your place'
    except Exception as e:
        return 'your place'
country = get_user_country()
walk_frames = load_frames(['assets/melodie/walk_1.gif', 'assets/melodie/walk_2.gif'], SPRITE_SIZE)
idle_frames = load_frames(['assets/melodie/idle_1.gif', 'assets/melodie/idle_2.gif'], SPRITE_SIZE)
pick_up_frames = load_frames(['assets/melodie/pick_up_1.gif', 'assets/melodie/pick_up_2.gif'], SPRITE_SIZE)
fall_frames = load_frames(['assets/melodie/fall_1.gif', 'assets/melodie/fall_2.gif'], SPRITE_SIZE)
ouch_frames = load_frames([f'assets/melodie/ouch_{i}.gif' for i in range(1, 8)], SPRITE_SIZE)
wounded_frames = load_frames(['assets/melodie/wounded_1.gif', 'assets/melodie/wounded_2.gif'], SPRITE_SIZE)
sing_frames = load_frames(['assets/melodie/sing_1.gif', 'assets/melodie/sing_2.gif'], SPRITE_SIZE)
headpat_frames = load_frames(['assets/melodie/headpat_1.gif', 'assets/melodie/headpat_2.gif'], SPRITE_SIZE)
eat_frames = load_frames(['assets/melodie/eat_1.gif', 'assets/melodie/eat_2.gif'], SPRITE_SIZE)
fat_frames = load_frames(['assets/melodie/fat_1.gif', 'assets/melodie/fat_2.gif'], SPRITE_SIZE)
fat_headpat_frames = load_frames(['assets/melodie/fat_headpat_1.gif', 'assets/melodie/fat_headpat_2.gif'], SPRITE_SIZE)
fat_pick_up_frames = load_frames(['assets/melodie/fat_pick_up_1.gif', 'assets/melodie/fat_pick_up_2.gif'], SPRITE_SIZE)
vomit_frames = load_frames([f'assets/melodie/vomit_{i}.gif' for i in range(1, 12)], SPRITE_SIZE)
dead_frames = load_frames(['assets/melodie/kill_1.gif', 'assets/melodie/kill_2.gif'], SPRITE_SIZE)
hurt_walk_frames = load_frames(['assets/melodie/hurt_walk_1.gif', 'assets/melodie/hurt_walk_2.gif'], SPRITE_SIZE)
jealous_idle_frames = load_frames(['assets/melodie/jealous_idle_1.gif', 'assets/melodie/jealous_idle_2.gif'], SPRITE_SIZE)
jealous_walk_frames = load_frames(['assets/melodie/jealous_walk_1.gif', 'assets/melodie/jealous_walk_2.gif'], SPRITE_SIZE)
facing_frames = load_frames(['assets/melodie/facing_1.gif', 'assets/melodie/facing_2.gif'], SPRITE_SIZE)
lust_idle_frames = load_frames(['assets/melodie/lust_1.gif', 'assets/melodie/lust_2.gif'], SPRITE_SIZE)
lust_walk_frames = load_frames(['assets/melodie/lust_walk_1.gif', 'assets/melodie/lust_walk_2.gif'], SPRITE_SIZE)
bed_frames = load_frames(['assets/melodie/bed_1.gif', 'assets/melodie/bed_2.gif'], SPRITE_SIZE)
sounds = {'sing': pygame.mixer.Sound('assets/sound/sing.mp3'), 'dont_own': pygame.mixer.Sound('assets/sound/dont_own.mp3'), 'eating': pygame.mixer.Sound('assets/sound/eating.mp3')}
for _ in range(2, 5):
    key = f'sing{_}'
    sounds[key] = pygame.mixer.Sound(f'assets/sound/{key}.mp3')
health_bar = load_frames([f'assets/melodie/health_bar/health_{i}.png' for i in range(6)], (100, 100))
kys = {}
for level in range(0, 12):
    file_paths = [f'assets/happy_bar/{level}_bar_{frame}.gif' for frame in [1, 2]]
    kys[level] = load_frames(file_paths, (190, 301))

def wrap_text(text, max_chars=21):
    words = text.split()
    lines = []
    current_line = ''
    for word in words:
        if len(current_line) + len(word) + 1 > max_chars:
            if current_line:
                lines.append(current_line)
            current_line = word
        else:  # inserted
            if current_line:
                current_line += ' ' + word
            else:  # inserted
                current_line = word
    if current_line:
        lines.append(current_line)
    return '\n'.join(lines)

class Poop:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load('assets/other/poop.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.speed = 5
        self.active = True

    def update(self):
        if self.y < HEIGHT:
            self.y += self.speed
        else:  # inserted
            self.active = False

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class FlyingPet:
    def __init__(self, x, y, frames):
        self.x = x
        self.y = y
        self.frames = frames
        self.current_frame = 0
        self.frame_timer = 0
        self.speed = 20
        self.direction = (random.uniform((-1), 1), random.uniform((-1), 1))
        self.lifetime = 15000
        self.start_time = pygame.time.get_ticks()

    def update(self):
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
        if self.x < 0 or self.x > WIDTH:
            self.direction = (-self.direction[0], self.direction[1])
        if self.y < 0 or self.y > HEIGHT:
            self.direction = (self.direction[0], -self.direction[1])
        if random.random() < 0.02:
            self.direction = (random.uniform((-1), 1), random.uniform((-1), 1))
        self.frame_timer += 1
        if self.frame_timer >= FRAME_DURATION:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.frame_timer = 0

    def draw(self, screen):
        screen.blit(self.frames[self.current_frame], (self.x, self.y))

    def is_expired(self):
        return pygame.time.get_ticks() - self.start_time >= self.lifetime

class Melodie:
    def __init__(self, x, y, speed=0.05):
        self.x = x
        self.y = y
        self.speed = speed
        self.current_frame = 0
        self.frame_timer = 0
        self.frames = idle_frames
        self.state = 'idle'
        self.target_x = x
        self.target_y = y
        self.width, self.height = SPRITE_SIZE
        self.stop_timer = random.randint(3000, 5000)
        self.last_move_time = pygame.time.get_ticks()
        self.health = MAX_HEALTH
        self.is_ouching = False
        self.is_eating = False
        self.eat_timer = 0
        self.is_fat = False
        self.is_vomiting = False
        self.vomit_timer = 0
        self.space_press_count = 0
        self.hit_counter = 0
        self.happiness = 5
        self.fat_feed_counter = 0

    def set_state(self, new_state):
        if self.state == new_state:
            return
        self.state = new_state
        state_frames = {}
        lust_headpat_frames = load_frames(['assets/melodie/lust_headpat_1.gif', 'assets/melodie/lust_headpat_2.gif'], SPRITE_SIZE)
        if self.is_fat:
            state_frames = {'idle': fat_frames, 'walk': fat_frames, 'dragging': fat_pick_up_frames, 'falling': fat_pick_up_frames, 'headpat': fat_headpat_frames}
        else:  # inserted
            if self.happiness == 11:
                state_frames = {'idle': lust_idle_frames, 'walk': lust_walk_frames, 'headpat': lust_headpat_frames, 'dragging': pick_up_frames, 'falling': fall_frames}
            else:  # inserted
                if chonet and (not self.is_fat):
                    state_frames = {'idle': jealous_idle_frames, 'walk': jealous_walk_frames, 'headpat': headpat_frames, 'dragging': pick_up_frames, 'falling': fall_frames}
                else:  # inserted
                    state_frames = {'idle': idle_frames, 'walk': walk_frames, 'headpat': headpat_frames, 'dragging': pick_up_frames, 'falling': fall_frames}
        state_frames.update({'wounded': wounded_frames, 'singing': sing_frames, 'ouch': ouch_frames, 'eating': eat_frames, 'vomiting': vomit_frames, 'dead': dead_frames, 'hurt_walk': hurt_walk_frames, 'facing': facing_frames, 'fat': fat_frames, 'bed': bed_frames})
        self.frames = state_frames[new_state]
        self.current_frame = 0
        self.frame_timer = 0

    def move_randomly(self, delta_time):
        if self.state in ['falling', 'wounded', 'eating', 'fat', 'dead']:
            return
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time > self.stop_timer:
            direction = random.choice([(-1), 1])
            self.target_x += direction * MOVE_OFFSET
            self.target_x = max(0, min(WIDTH - self.width, self.target_x))
            self.last_move_time = current_time
            self.stop_timer = random.randint(3000, 5000)
        self.x += (self.target_x - self.x) * self.speed
        self.y += (self.target_y - self.y) * self.speed
        if abs(self.x - self.target_x) > 1:
            if self.state!= 'walk':
                self.set_state('walk')
        else:  # inserted
            if self.state!= 'idle':
                self.set_state('idle')

    def _happiness(self, increase: bool=True):
        if increase and (not self.is_fat):
            self.happiness += 1 if self.happiness < 11 else 0
        else:  # inserted
            self.happiness -= 1 if self.happiness > 0 else 0

    def take_damage(self, bibi):
        if self.state not in ['wounded', 'ouch', 'falling', 'dragging', 'eating', 'fat', 'headpat'] and bibi == None:
            self.health -= 1
            self._happiness(False)
            self.hit_counter += 1
            self.set_state('ouch')
            self.is_ouching = True

    def die(self, cheese=True):
        self.happiness = 0
        if cheese:
            self.set_state('dead')
        else:  # inserted
            self.set_state('hurt_walk')
        pygame.mixer.music.fadeout(1000)

    def respawn(self):
        self.health = MAX_HEALTH
        self.set_state('falling')
        self.happiness = 5
        self.y = 200
        self.x = 400
        pygame.mixer.music.play(loops=(-1), fade_ms=2000)

    def update(self, delta_time, chat=None, score=None, current_food=None):
        if self.state == 'dead':
            self.happiness = 0
            self.y -= 1
            if self.y <= (-230):
                self.respawn()
        if self.is_fat and self.happiness >= 11:
            self.happiness = 10
        else:  # inserted
            if self.state == 'ouch' and (not self.is_ouching):
                if self.health <= 0:
                    self.set_state('wounded')
                    chat.start_chat(['You\'re hurting me..', 'Is this fun to you?', 'Please..\nGive me some food..\nAnything but cheese..'])
                else:  # inserted
                    self.set_state('idle')
            else:  # inserted
                if self.state in ('idle', 'walk') and self.state!= 'singing' and (not self.is_fat):
                    self.move_randomly(delta_time)
                else:  # inserted
                    if self.state == 'falling':
                        self.y += FALL_SPEED * (2 if self.is_fat else 1)
                        if self.y >= HEIGHT - self.height:
                            self.y = HEIGHT - self.height
                            self.set_state('idle')
                    else:  # inserted
                        if self.state == 'headpat':
                            self.headpat_timer += delta_time
                            if self.headpat_timer >= 2000:
                                self.set_state('idle')
                                self.headpat_timer = 0
                        else:  # inserted
                            if self.state == 'eating':
                                self.eat_timer += delta_time
                                if self.eat_timer >= 2000:
                                    self.set_state('idle')
                                    self.eat_timer = 0
                            else:  # inserted
                                if self.state == 'vomiting':
                                    self.vomit_timer += delta_time
                                    if self.vomit_timer >= 2000:
                                        self.is_vomiting = False
                                        self.set_state('idle')
                                else:  # inserted
                                    if self.state == 'wounded' and score < 5 and (not chat.is_texting) and (current_food is None):
                                        chat.start_chat(['Oh wait..\nEw, you\'re too\npoor to buy\na thing..'])
                                        self.set_state('hurt_walk')
                                    else:  # inserted
                                        if self.state == 'hurt_walk':
                                            self.x += 5
                                            if self.x >= 800:
                                                self.respawn()
        self.animate(delta_time)

    def animate(self, delta_time):
        frame_duration = FRAME_DURATION
        if self.state == 'ouch':
            frame_duration = 150
        else:  # inserted
            if self.state == 'vomiting':
                frame_duration = 200
        self.frame_timer += delta_time
        if self.frame_timer >= frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.frame_timer -= frame_duration
        if self.state == 'ouch' and self.current_frame == len(self.frames) - 1:
            self.is_ouching = False
        if self.state == 'vomiting' and self.current_frame == len(self.frames) - 1:
            self.is_vomiting = False

    def draw_health_bar(self, screen):
        if 0 <= self.health < len(health_bar):
            health_image = health_bar[self.health]
            bar_x = self.x + (self.width - health_image.get_width()) // 2 - 5
            bar_y = self.y - 40
            screen.blit(health_image, (bar_x, bar_y))

    def draw(self, screen):
        self.draw_health_bar(screen)
        screen.blit(self.frames[self.current_frame], (self.x, self.y))

    def start_singing(self, score):
        if self.health > 0 and self.state not in ['falling', 'wounded', 'singing'] and (not self.is_fat):
            sound_names = list(sounds.keys())
            if 'eating' in sound_names:
                sound_names.remove('eating')
            sound_name = random.choice(sound_names)
            sound = sounds[sound_name]
            self.set_state('singing')
            sound.play()
            pygame.time.set_timer(pygame.USEREVENT + 1, int(sound.get_length() * 1000))
            return score + 5
        return score

    def eat(self, food, chat=None):
        self.set_state('eating')
        sounds['eating'].play()
        self.eat_timer = 0
        if 'cheese' in food.image_path.lower():
            self.is_vomiting = True
            self.vomit_timer = 0
            self.set_state('vomiting')
            if self.health > 1:
                self.health -= 1
                if chat is not None:
                    chat.start_chat(random.choice(['Ew! Smells like\nDraco\'s feet..', 'Don\'t you dare\nfeed me this..', 'Don\'t make me call\nLarry & Lawrie on\nyou..', 'Ew..!\nGive that to Dynamike!']))
            else:  # inserted
                if self.health <= 0:
                    self.die()
            self.is_fat = False
        else:  # inserted
            if self.health < MAX_HEALTH:
                self.health += food.heal_amount
                if chat is not None:
                    if 'sushi' in food.image_path.lower():
                        chat.start_chat(wrap_text(random.choice(['Hosomaki healing best dish!', 'Fresh and healing!', 'I feel as strong as a samurai! Except that I\'m an idol'])))
                    else:  # inserted
                        if 'janet' in food.image_path.lower():
                            chat.start_chat(wrap_text(random.choice(['Why does her head heal this much..?', 'I\'m even more alive, she\'s dead.', 'The blood\'s taste is left in my mouth..'])))
                        else:  # inserted
                            if 'apple' in food.image_path.lower():
                                chat.start_chat(wrap_text(random.choice(['Cheap.. but healing', 'On a certain game apples heal more', 'Could you get me something else?'])))
                            else:  # inserted
                                if 'popcorn' in food.image_path.lower():
                                    chat.start_chat(wrap_text(random.choice(['Yummy.. wouldn\'t mind eating more', 'I wonder if they\'re produced in Korea', 'More, more! I want to eat more!'])))
                                else:  # inserted
                                    if 'egg' in food.image_path.lower():
                                        chat.start_chat(wrap_text(random.choice(['I\'m not sure if I should eat this..', 'Try keeping it on the ground rather than feeding it to me', 'Well.. maybe it doesn\'t taste too bad'])))
                if self.health > MAX_HEALTH:
                    self.health = MAX_HEALTH
            else:  # inserted
                if self.health >= MAX_HEALTH and (not self.is_fat):
                    self.fat_feed_counter += 1
                    if self.fat_feed_counter < 4 and chat is not None:
                        if 'sushi' in food.image_path.lower():
                            chat.start_chat(random.choice(['Ah.. Kenji\'s specialty', 'That\'s good for my\nidol diet ^-^', 'My palate is at the\ntop, watch the sushi\nin my tummy drop!']))
                        else:  # inserted
                            if 'janet' in food.image_path.lower():
                                chat.start_chat(random.choice(['She\'ll never be as\ngood as me..', 'Stu will never\nfind out.', 'I wonder how Bonnie\nalso tastes like']))
                            else:  # inserted
                                if 'apple' in food.image_path.lower():
                                    chat.start_chat(random.choice(['Is the cheapest food\nthe only you\ncould get me?', 'An apple a day,\nkeeps bad randoms\naway', 'This apple seems\nfamiliar']))
                                else:  # inserted
                                    if 'popcorn' in food.image_path.lower():
                                        chat.start_chat(random.choice(['Quite some bouncy\npopcorn.. weird', 'Don\'t tell Fang what\nI just ate, okay?', 'What movie are we\nwatching? Maybe\none about me?']))
                                    else:  # inserted
                                        if 'egg' in food.image_path.lower():
                                            chat.start_chat(random.choice(['An egg? What if it\nhatches in my stomach?', 'Doesn\'t taste very\ngood, is this from\nchicken Rico?', 'Maybe it\'s dinosaur egg,\nmust belong to Buzz']))
                    else:  # inserted
                        self.is_fat = True
                        self.set_state('fat')
                        self.fat_feed_counter = 0
                        if chat is not None:
                            if 'sushi' in food.image_path.lower():
                                chat.start_chat(random.choice(['Too much fish!\nI\'m not a whale!', 'Ugh.. too much fish..', 'I won\'t be able to\nswim like this..']))
                            else:  # inserted
                                if 'janet' in food.image_path.lower():
                                    chat.start_chat(random.choice(['Great.. now I\'m as\nbig as Janet..', 'This isn\'t pitch\nperfect..', 'She\'s stuck in my\nstomach!']))
                                else:  # inserted
                                    if 'apple' in food.image_path.lower():
                                        chat.start_chat('Since when did\napples have so\nmany calories\n..?')
                                    else:  # inserted
                                        if 'popcorn' in food.image_path.lower():
                                            chat.start_chat(random.choice(['What did you put\nin this popcorn..?', 'You could have given\nthe rest to Fang..']))
                                        else:  # inserted
                                            if 'egg' in food.image_path.lower():
                                                chat.start_chat(random.choice(['Can\'t you feed me\nsomething normal for\nonce? Maybe apples?', 'I don\'t think this\nis supposed to\nbe eaten..']))

    def stop_dragging(self):
        if self.state not in ['wounded', 'dead']:
            self.set_state('falling')
            self.target_x = self.x

    def start_dragging(self):
        if self.state not in ['wounded', 'dead']:
            self.set_state('dragging')

    def stop_singing(self):
        if self.state == 'singing':
            self.set_state('idle')

    def start_headpat(self, mouse_pos):
        if self.state in ['falling', 'wounded', 'singing', 'headpat', 'dead', 'ouch', 'lust']:
            return False
        if pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(mouse_pos):
            self.set_state('headpat')
            self.headpat_timer = 0
            self.is_headpatting = True
            self._happiness()
            return True

    def drop_poop(self):
        if not self.is_fat or self.state == 'dragging':
            self.space_press_count += 1
            if self.space_press_count >= 3:
                self.is_fat = False
                self.space_press_count = 0
                self.set_state('falling')

def draw_happiness_bar(screen, happiness):
    if 0 <= happiness < 12:
        frames = kys[happiness]
        current_frame = pygame.time.get_ticks() // 500 % 2
        screen.blit(frames[current_frame], (600, 10))

class Food:
    def __init__(self, x, y, image_path, heal_amount, animated=False, frames=None):
        self.image_path = image_path
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.heal_amount = heal_amount
        self.animated = animated
        self.frames = frames if frames else []
        self.current_frame = 0
        self.frame_timer = 0
        self.is_dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.spawn_time = pygame.time.get_ticks()
        self.hatched = False
        self.hatch_count = 1

    def draw(self, screen):
        if self.animated:
            screen.blit(self.frames[self.current_frame], (self.x, self.y))
        else:  # inserted
            screen.blit(self.image, (self.x, self.y))

    def update(self, delta_time):
        if self.animated:
            self.frame_timer += delta_time
            if self.frame_timer >= FRAME_DURATION:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.frame_timer -= FRAME_DURATION

    def start_dragging(self, mouse_pos):
        self.is_dragging = True
        self.drag_offset_x = mouse_pos[0] - self.x
        self.drag_offset_y = mouse_pos[1] - self.y

    def stop_dragging(self):
        self.is_dragging = False

    def move(self, mouse_pos):
        if self.is_dragging:
            self.x = mouse_pos[0] - self.drag_offset_x
            self.y = mouse_pos[1] - self.drag_offset_y

    def should_hatch(self):
        return not self.hatched and pygame.time.get_ticks() - self.spawn_time >= 20000 and (self.hatch_count <= 2)

    def hatch(self):
        if self.hatch_count <= 2:
            self.hatched = True
            return True
        return False

def draw_button(screen, x, y, width, height, image_path):
    button_image = pygame.image.load(image_path)
    button_image = pygame.transform.scale(button_image, (width, height))
    screen.blit(button_image, (x, y))

def draw_score(screen, score, font, x, y):
    score_image = pygame.image.load('assets/buttons/score.png')
    score_image = pygame.transform.scale(score_image, (180, 140))
    screen.blit(score_image, (x, y))
    score_text = font.render(f'{score}', True, (144, 64, 117))
    score_text_rect = score_text.get_rect(center=(x + 20 + score_image.get_width() // 2, y + score_image.get_height() // 2))
    screen.blit(score_text, score_text_rect)

def draw_text_animated(screen, text, font, color, x, y, progress):
    visible_text = text[:progress]
    text_surface = font.render(visible_text, True, color)
    screen.blit(text_surface, (x, y))
pygame.mixer.init()

class MelodieChat:
    def __init__(self, screen):
        self.screen = screen
        self.chat_box_img = pygame.image.load('assets/buttons/chat_box.png').convert_alpha()
        self.chat_box_img = pygame.transform.scale(self.chat_box_img, (400, 300))
        self.font = pygame.font.Font('assets/fonts/ByteBounce.ttf', 34)
        self.text_color = (144, 64, 117)
        self.is_texting = False
        self.waiting_for_click = False
        self.text = ''
        self.full_text = ''
        self.text_index = 0
        self.sentence_index = 0
        self.sentence_list = []
        self.chat_box_rect = self.chat_box_img.get_rect(center=(220, 240))
        self.typing_sfx = [f'assets/talk_sfx/talk_{i}.mp3' for i in range(1, 11)]
        self.typing_sound_channel = pygame.mixer.Channel(1)

    def start_chat(self, sentences):
        if self.is_texting:
            return
        self.sentence_list = sentences if isinstance(sentences, list) else [sentences]
        self.sentence_index = 0
        self.is_texting = True
        self.waiting_for_click = False
        self.text = ''
        self.full_text = self.sentence_list[self.sentence_index]
        self.text_index = 0
        self.typing_sound_channel.stop()

    def update(self):
        if self.is_texting and (not self.waiting_for_click):
            if self.text_index < len(self.full_text):
                self.text_index += 1
                self.text = self.full_text[:self.text_index]
                if not self.typing_sound_channel.get_busy():
                    sound_file = random.choice(self.typing_sfx)
                    sound = pygame.mixer.Sound(sound_file)
                    self.typing_sound_channel.play(sound)
            else:  # inserted
                self.typing_sound_channel.fadeout(500)
                self.waiting_for_click = True
        self.draw()

    def draw(self):
        if self.is_texting:
            self.screen.blit(self.chat_box_img, self.chat_box_rect)
            lines = self.text.split('\n')
            line_height = self.font.get_height()
            for i, line in enumerate(lines):
                text_surface = self.font.render(line, True, self.text_color)
                self.screen.blit(text_surface, (self.chat_box_rect.x + 55, self.chat_box_rect.y + 100 + i * line_height))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_texting and self.waiting_for_click:
            if self.sentence_index < len(self.sentence_list) - 1:
                self.sentence_index += 1
                self.text = ''
                self.full_text = self.sentence_list[self.sentence_index]
                self.text_index = 0
                self.waiting_for_click = False
            else:  # inserted
                self.is_texting = False

def is_melodie_on_chonet(melodie, chonet):
    if chonet is None:
        return False
    return melodie.x < chonet.x + chonet.width and melodie.x + melodie.width > chonet.x and (melodie.y < chonet.y + chonet.height) and (melodie.y + melodie.height > chonet.y)

class Chonet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 2
        self.current_frame = 0
        self.frame_timer = 0
        self.frames = {'idle': load_frames(['assets/chonet/chonet_idle_1.gif', 'assets/chonet/chonet_idle_2.gif'], (100, 100)), 'walk': load_frames(['assets/chonet/chonet_walk_1.gif', 'assets/chonet/chonet_walk_2.gif'], (100, 100)), 'headpat': load_frames(['assets/chonet/chonet_pat_1.gif', 'assets/chonet/chonet_pat_2.gif'], (100, 100)), 'scared': load_frames(['assets/chonet/scared_1.gif', 'assets/chonet/scared_2.gif'], (100, 100)), 'dead': load_frames(['assets/chonet/dead.png'], (100, 100)), 'janet': load_frames(['assets/chonet/janet_1.gif', 'assets/chonet/janet_2.gif'], (200, 200))}
        self.state = 'walk'
        self.target_x = WIDTH // 2
        self.width, self.height = (100, 100)
        self.stop_timer = 0
        self.headpat_timer = 0
        self.is_headpatting = False
        self.fade_alpha = 255
        self.fade_speed = 5

    def set_state(self, new_state):
        if new_state in self.frames:
            self.state = new_state
            self.current_frame = 0
            self.frame_timer = 0
            if new_state!= 'headpat':
                self.headpat_timer = 0
                self.is_headpatting = False

    def start_headpat(self, mouse_pos):
        if self.state == 'janet':
            return False
        if self.state in ['falling', 'wounded', 'singing', 'headpat', 'dead']:
            return False
        if pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(mouse_pos):
            self.set_state('headpat')
            self.headpat_timer = 0
            return True

    def animate(self, delta_time):
        self.frame_timer += delta_time
        if self.frame_timer >= FRAME_DURATION:
            self.current_frame = (self.current_frame + 1) % len(self.frames[self.state])
            self.frame_timer -= FRAME_DURATION

    def update(self, delta_time):
        global chonet  # inserted
        if self.state == 'dead':
            self.fade_alpha -= self.fade_speed
            if self.fade_alpha <= 0:
                self.fade_alpha = 0
                chonet = None
            return None
        if self.state == 'headpat':
            self.headpat_timer += delta_time
            if self.headpat_timer >= 2000:
                self.set_state('walk')
            self.animate(delta_time)
        else:  # inserted
            if self.state == 'walk' and (not self.is_headpatting):
                if self.x < self.target_x:
                    self.x += self.speed
                else:  # inserted
                    if self.x > self.target_x:
                        self.x -= self.speed
                if abs(self.x - self.target_x) < self.speed:
                    self.set_state('idle')
                    self.stop_timer = 0
            else:  # inserted
                if self.state == 'idle' and (not self.is_headpatting):
                    self.stop_timer += delta_time
                    if self.stop_timer >= 3000:
                        self.stop_timer = 0
                        self.set_state('walk')
                        self.target_x = random.randint(0, WIDTH - self.width)
            self.animate(delta_time)

    def draw(self, screen):
        if self.state == 'dead' and 'dead' in self.frames:
            dead_frame = self.frames['dead'][0]
            if dead_frame:
                dead_frame.set_alpha(self.fade_alpha)
                screen.blit(dead_frame, (self.x, self.y))
        else:  # inserted
            screen.blit(self.frames[self.state][self.current_frame], (self.x, self.y))

def handle_kill_button(melodie, chonet, screen, background):
    if chonet and chonet.state == 'janet':
        return
    if is_melodie_on_chonet(melodie, chonet):
        pygame.mixer.music.fadeout(1000)
        clock = pygame.time.Clock()
        melodie.set_state('facing')
        chonet.set_state('scared')
        melodie.current_frame = 0
        chonet.current_frame = 0
        start_anim = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_anim < 2000:
            delta_time = clock.tick(FPS)
            melodie.animate(delta_time)
            chonet.animate(delta_time)
            screen.blit(background, (0, 0))
            chonet.draw(screen)
            melodie.draw(screen)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        start_black = pygame.time.get_ticks()
        kill_effect = pygame.mixer.Sound('assets/kill_effect.mp3')
        kill_effect.play()
        while pygame.time.get_ticks() - start_black < 2000:
            screen.fill((0, 0, 0))
            pygame.display.update()
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        melodie.set_state('idle')
        chonet.set_state('dead')
        chonet.fade_alpha = 255
        fade_duration = 2000
        start_fade = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_fade < fade_duration:
            delta_time = clock.tick(FPS)
            fade_decrement = 255 * (delta_time / fade_duration)
            chonet.fade_alpha -= fade_decrement
            if chonet.fade_alpha < 0:
                chonet.fade_alpha = 0
            chonet.animate(delta_time)
            screen.blit(background, (0, 0))
            chonet.draw(screen)
            melodie.draw(screen)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        chonet = None
        pygame.mixer.music.play((-1))

def entrance_animation(screen):
    clock = pygame.time.Clock()
    animation_duration_in = 2000
    hold_duration = 1000
    animation_duration_out = 2000
    total_duration = animation_duration_in + hold_duration + animation_duration_out
    start_time = pygame.time.get_ticks()
    normal_font = pygame.font.Font('assets/fonts/ByteBounce.ttf', FONT_SIZE)
    small_font = pygame.font.Font('assets/fonts/ByteBounce.ttf', FONT_SIZE // 2)
    text = 'Melodie Pet Game\n\nMade by Takaso and Hashimoto\n\nGithub: https://github.com/Takaso/'
    lines = text.splitlines()
    rendered_lines = []
    for line in lines:
        if 'Github:' in line:
            rendered_lines.append(small_font.render(line, True, (255, 255, 255)).convert_alpha())
        else:  # inserted
            rendered_lines.append(normal_font.render(line, True, (255, 255, 255)).convert_alpha())
    total_height = sum((line.get_height() for line in rendered_lines))
    while True:
        current_time = pygame.time.get_ticks()
        elapsed = current_time - start_time
        if elapsed > total_duration:
            return
        if elapsed < animation_duration_in:
            alpha = int(elapsed / animation_duration_in * 255)
        else:  # inserted
            if elapsed < animation_duration_in + hold_duration:
                alpha = 255
            else:  # inserted
                fade_out_time = elapsed - (animation_duration_in + hold_duration)
                alpha = int(255 * (1 - fade_out_time / animation_duration_out))
        screen.fill((0, 0, 0))
        y_offset = (HEIGHT - total_height) // 2
        for rendered in rendered_lines:
            rendered_copy = rendered.copy()
            rendered_copy.set_alpha(alpha)
            x = (WIDTH - rendered_copy.get_width()) // 2
            screen.blit(rendered_copy, (x, y_offset))
            y_offset += rendered_copy.get_height()
        pygame.display.flip()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def handle_sex_option(melodie, screen, background, clock, chat):
    original_y = melodie.y
    melodie.set_state('walk')
    target_x = (WIDTH - melodie.width) // 2
    step_size = 3
    last_frame_switch = pygame.time.get_ticks()
    while abs(melodie.x - target_x) > 0:
        delta_time = clock.tick(FPS)
        now = pygame.time.get_ticks()
        if now - last_frame_switch >= 400:
            melodie.current_frame = (melodie.current_frame + 1) % len(melodie.frames)
            last_frame_switch = now
        if melodie.x < target_x:
            melodie.x = min(melodie.x + step_size, target_x)
        else:  # inserted
            melodie.x = max(melodie.x - step_size, target_x)
        screen.blit(background, (0, 0))
        if bibi is not None:
            bibi.draw(screen)
        melodie.y = original_y
        melodie.draw(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    if bibi is not None:
        kiss_paths = ['assets/bibi/melobibi_1.gif', 'assets/bibi/melobibi_2.gif']
        kiss_frames = load_frames(kiss_paths, (melodie.width, melodie.height))
        start_time = pygame.time.get_ticks()
        frame_interval = 200
        while pygame.time.get_ticks() - start_time < 2000:
            dt = clock.tick(FPS)
            elapsed = pygame.time.get_ticks() - start_time
            idx = elapsed // frame_interval % len(kiss_frames)
            screen.blit(background, (0, 0))
            frame = kiss_frames[idx]
            pos = ((WIDTH - melodie.width) // 2, original_y)
            screen.blit(frame, pos)
            pygame.display.update()
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        chat.start_chat(wrap_text('Mhhh, your mouth tastes so good, just like bubblegum~'))
        return
    else:  # inserted
        melodie.y = original_y + 20
        melodie.set_state('bed')
        sex_sound = pygame.mixer.Sound(f'assets/sex{random.randint(1, 2)}.ogg')
        sex_sound.play(loops=(-1))
        sex_duration = 3000
        start_time = pygame.time.get_ticks()
        frame_interval = 100
        last_switch = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < sex_duration:
            dt = clock.tick(FPS)
            now = pygame.time.get_ticks()
            if now - last_switch >= frame_interval:
                melodie.current_frame = (melodie.current_frame + 1) % len(melodie.frames)
                last_switch = now
            shake_x = random.randint((-2), 2)
            shake_y = random.randint((-2), 2)
            screen.blit(background, (shake_x, shake_y))
            bed_img = melodie.frames[melodie.current_frame]
            screen.blit(bed_img, (melodie.x + shake_x, melodie.y + shake_y))
            pygame.display.update()
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        sex_sound.stop()
        melodie.set_state('idle')
        melodie.y = original_y
        melodie.happiness = 11

def get_decision_options(category):
    """\n    Returns the decision options that the player can choose from.\n    \n    category: 0 for Love, 1 for Neutral, 2 for Hate.\n    Only the following options are returned:\n      - Love: \"You\'re amazing!\", \"I adore you\", \"I love your music!\"\n      - Neutral: \"Not much to say\", \"Ok\", \"I don\'t know\"\n      - Hate: \"I hate you\", \"You\'re the worst\", \"Just shut up\"\n    """  # inserted
    if category == 0:
        return ['You\'re amazing!', 'I adore you', 'I love your music!']
    if category == 1:
        return ['Not much to say', 'Ok', 'I don\'t know']
    if category == 2:
        return ['I hate you', 'You\'re the worst', 'Just shut up']
    return []

def get_melodie_reply(category, option, health, happiness):
    """\n    category: 0 = Love, 1 = Neutral, 2 = Hate.\n    option: for each category:\n         For Love: 0 = \"You\'re amazing!\", 1 = \"I adore you\", 2 = \"I love your music!\"\n         For Neutral: 0 = \"Not much to say\", 1 = \"Ok\", 2 = \"I don\'t know\"\n         For Hate: 0 = \"I hate you\", 1 = \"You\'re the worst\", 2 = \"Just shut up\"\n    health and happiness determine the mode:\n         health <= 2 --> \"sad\" mode\n         happiness == 11 --> \"yandere\" mode\n         otherwise --> \"default\" mode\n    """  # inserted
    if health <= 2:
        mode = 'sad'
    else:  # inserted
        if happiness == 11:
            mode = 'yandere'
        else:  # inserted
            mode = 'default'
    I bask in the glow of your adoration = {'I bask in the glow of your adoration': [*, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *, *
    try:
        replies = replies_dict[mode][category][option]
    except KeyError:
        replies = ['...']
    chosen_reply = random.choice(replies)
    return wrap_text(chosen_reply, max_chars=21)
BIBI_WALK_SIZE = (89, 132)
BIBI_IDLE_SIZE = (89, 132)
BIBI_CHAT_SIZE = (288, 378)
INFO_BUTTON_SIZE = (50, 50)
ARROW_BUTTON_SIZE = (20, 20)
BIBI_SPEED = 3

class Bibi:
    def __init__(self):
        self.walk_frames = load_frames(['assets/bibi/bibi_walk_1.gif', 'assets/bibi/bibi_walk_2.gif'], BIBI_WALK_SIZE)
        self.idle_frames = load_frames(['assets/bibi/bibi_1.gif', 'assets/bibi/bibi_2.gif'], BIBI_IDLE_SIZE)
        self.current_frame = 0
        self.frame_timer = 0
        self.state = 'walking_in'
        self.x = -BIBI_WALK_SIZE[0]
        self.y = HEIGHT // 2 - BIBI_WALK_SIZE[1] // 2 + 205
        self.dest_x = WIDTH // 2 - BIBI_WALK_SIZE[0] // 2
        self.speed = BIBI_SPEED

    def update(self, delta_time):
        self.frame_timer += delta_time
        if self.frame_timer >= FRAME_DURATION:
            if self.state in ['walking_in', 'walking_out']:
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
            else:  # inserted
                if self.state == 'idle':
                    self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
            self.frame_timer -= FRAME_DURATION
        if self.state == 'walking_in':
            if self.x < self.dest_x:
                self.x += self.speed
            else:  # inserted
                self.x = self.dest_x
                self.state = 'idle'
                self.current_frame = 0
                self.frame_timer = 0
        else:  # inserted
            if self.state == 'walking_out':
                if self.x < WIDTH:
                    self.x += self.speed
                else:  # inserted
                    self.state = 'hidden'

    def draw(self, screen):
        if self.state in ['walking_in', 'walking_out']:
            frame = self.walk_frames[self.current_frame]
        else:  # inserted
            if self.state == 'idle':
                frame = self.idle_frames[self.current_frame]
            else:  # inserted
                return None
        screen.blit(frame, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, BIBI_WALK_SIZE[0], BIBI_WALK_SIZE[1])
DARK_PURPLE = (75, 0, 130)

class BibiChatBubble:
    def __init__(self, x, y):
        self.image = pygame.image.load('assets/bibi/bibi_chat.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, BIBI_CHAT_SIZE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.arrow_left = pygame.image.load('assets/bibi/arrow_left.png').convert_alpha()
        self.arrow_left = pygame.transform.scale(self.arrow_left, ARROW_BUTTON_SIZE)
        self.arrow_right = pygame.image.load('assets/bibi/arrow_right.png').convert_alpha()
        self.arrow_right = pygame.transform.scale(self.arrow_right, ARROW_BUTTON_SIZE)
        self.arrow_left_rect = self.arrow_left.get_rect(center=(self.rect.centerx - 60, self.rect.bottom - 50))
        self.arrow_right_rect = self.arrow_right.get_rect(center=(self.rect.centerx + 60, self.rect.bottom - 50))
        self.index_font = pygame.font.Font('assets/fonts/ByteBounce.ttf', 20)
        self.index_color = (128, 0, 128)
        self.text_font = pygame.font.Font('assets/fonts/ByteBounce.ttf', 20)
        self.bold_font = pygame.font.Font('assets/fonts/ByteBounce.ttf', 26)
        self.pages = ['**How to Handle Your Melodie** **Pet**\n1. **Give Some Respect!**\n- Right-click to headpat Melodie, she\'ll vibe with it, just don\'t get rough!', '2. **Move & Drag!**\n- Hold SPACE + left-click to move her. No tossing around, got it?', '3. **Feeding her!**\n- Click the food button and choose wisely.\n- **Good Food:** Sushi, apples, she loves \'em!\n- **Bad Food:** Cheese? Big mistake.', '4. **Sing It Out!**\n- Press the sing button to make her drop some beats and earn points.', '5. **Special Actions!**\n- **Love Mode:** Unlocks an extra interaction, up to you to find out!\n- **The \"Kill\" Button:** You can\'t see it? Not my problem, push it at your own risk!\n- **Fat Mode:** What? She gained weight? Drag her and Hold SPACE three times to help her let it out, or give her a smack attack! Just kidding, I ain\'t like you.', '6. **Watch the Chat!**\n- Melodie\'s got attitude. She\'ll react, talk back, and let you know exactly how she feels, be careful not to make her angry when she\'s in love mode..']
        self.current_page = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.arrow_left_rect.collidepoint(mouse_pos):
                self.current_page = (self.current_page - 1) % len(self.pages)
            else:  # inserted
                if self.arrow_right_rect.collidepoint(mouse_pos):
                    self.current_page = (self.current_page + 1) % len(self.pages)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.draw_formatted_text(screen, self.pages[self.current_page], self.rect)
        screen.blit(self.arrow_left, self.arrow_left_rect)
        screen.blit(self.arrow_right, self.arrow_right_rect)
        index_text = self.index_font.render(f'{self.current_page + 1}/{len(self.pages)}', True, self.index_color)
        index_rect = index_text.get_rect(center=(self.rect.centerx, self.rect.bottom - 50))
        screen.blit(index_text, index_rect)

    def draw_formatted_text(self, screen, text, rect):
        y_offset = rect.y + 50
        for original_line in text.split('\n'):
            wrapped_line = wrap_text(original_line, max_chars=28)
            for line in wrapped_line.split('\n'):
                x_offset = rect.x + 45
                segments = line.split('**')
                for i, seg in enumerate(segments):
                    if i % 2 == 1:
                        if len(seg) > 20:
                            bold_wrapped = wrap_text(seg, max_chars=20)
                            for bold_line in bold_wrapped.split('\n'):
                                rendered = self.bold_font.render(bold_line, True, (0, 0, 0))
                                screen.blit(rendered, (x_offset, y_offset))
                                y_offset += self.bold_font.get_height() + 5
                                x_offset = rect.x + 45
                        else:  # inserted
                            rendered = self.bold_font.render(seg, True, (0, 0, 0))
                            screen.blit(rendered, (x_offset, y_offset))
                            x_offset += rendered.get_width()
                    else:  # inserted
                        rendered = self.text_font.render(seg, True, DARK_PURPLE)
                        screen.blit(rendered, (x_offset, y_offset))
                        x_offset += rendered.get_width()
                y_offset += self.text_font.get_height() + 5
screen = pygame.display.set_mode((WIDTH, HEIGHT))
score = 0

def generate_pet_world():
    global score  # inserted
    global janet_head_eaten_count  # inserted
    global bibi  # inserted
    global chonet  # inserted
    background = pygame.image.load('assets/background.png')
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    melodie = Melodie(WIDTH // 2, HEIGHT - SPRITE_SIZE[1])
    is_dragging = False
    drag_offset_x, drag_offset_y = (0, 0)
    space_held = False
    running = True
    menu_open = False
    warning_hit = False
    hatch_count = 1
    items = [('Sushi', 10, 'assets/food/sushi.png', 2), ('Cheese', 5, 'assets/food/dynamike_cheese_1.gif', 0), ('Janet', 20, 'assets/food/janet_head.png', 4), ('Apple', 5, 'assets/food/minecraft_apple.png', 1), ('Popcorn', 15, 'assets/food/ricos_popcorn.png', 3), ('Egg', 30, 'assets/food/egg.png', 1), ('Love', 100, 'assets/buttons/sex.png', 0)]
    chonet = None
    menu_image = pygame.image.load('assets/buttons/menu_bar.png')
    menu_image = pygame.transform.scale(menu_image, (500, 500))
    close_button_image = pygame.image.load('assets/buttons/close.png')
    close_button_image = pygame.transform.scale(close_button_image, (50, 50))
    menu_rect = menu_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    close_button_rect = close_button_image.get_rect(topleft=(menu_rect.right - 390, menu_rect.top + 110))
    pygame.mixer.music.load('assets/background.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play((-1))
    untouchable = ('wounded', 'singing', 'dead', 'hurt_walk')
    current_food = None
    poops = []
    flying_pets = []
    janet_head_eaten_count = 0
    score_font = pygame.font.Font('assets/fonts/ByteBounce.ttf', 45)
    menu_font = pygame.font.Font('assets/fonts/ByteBounce.ttf', 30)
    show_stop_hitting_screen = False
    text_progress = 0
    text = f'Stop hitting me, {username}..'
    text_timer = 0
    chat = MelodieChat(screen)
    chat_bubble = None
    decision_menu = None
    chat_choice = None
    conversation_messages = []
    last_chat_click = 0
    bibi_button_img = pygame.image.load('assets/bibi/info_button.png').convert_alpha()
    bibi_button_img = pygame.transform.scale(bibi_button_img, INFO_BUTTON_SIZE)
    bibi_button_rect = bibi_button_img.get_rect(topleft=(665, 290))
    bibi = None
    bibi_chat = None
    while running:
        delta_time = clock.tick(FPS)
        keys = pygame.key.get_pressed()
        space_held = keys[pygame.K_SPACE]
        if bibi is not None and bibi.get_rect().collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:  # inserted
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        for event in pygame.event.get():
            chat.handle_event(event)
            if chat_bubble:
                chat_bubble.handle_event(event)
            if bibi_chat:
                bibi_chat.handle_event(event)
            if decision_menu:
                decision_index = decision_menu.handle_event(event)
                if decision_index is not None:
                    reply = get_melodie_reply(chat_choice, decision_index, melodie.health, melodie.happiness)
                    conversation_messages.append(reply)
                    chat.start_chat([reply])
                    decision_menu = None
                    chat_choice = None
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if bibi_button_rect.collidepoint(event.pos):
                    if melodie.state in ['idle', 'walk', 'singing']:
                        if bibi is None and (not melodie.is_fat):
                            bibi = Bibi()
                            melodie.target_x = 0 if melodie.x > WIDTH // 2 else WIDTH - melodie.width
                else:  # inserted
                    if bibi is not None and bibi.get_rect().collidepoint(event.pos):
                        if bibi.state == 'idle':
                            if bibi_chat is None:
                                chat_x = bibi.x + BIBI_WALK_SIZE[0] + 10
                                chat_y = bibi.y - BIBI_CHAT_SIZE[1] // 2 - 120
                                bibi_chat = BibiChatBubble(chat_x, chat_y)
                            else:  # inserted
                                bibi_chat = None
                                bibi.state = 'walking_out'
                    else:  # inserted
                        button_x, button_y, button_width, button_height = (220, 60, 113, 61)
                        food_button_x, food_button_y, food_button_width, food_button_height = (358, 60, 113, 61)
                        chat_button_x, chat_button_y, chat_button_width, chat_button_height = (496, 60, 115, 61)
                        kill_button_x, kill_button_y, kill_button_width, kill_button_height = (25, 340, 144, 144)
                        current_time = pygame.time.get_ticks()
                        if pygame.Rect(chat_button_x, chat_button_y, chat_button_width, chat_button_height).collidepoint(mouse_pos) and current_time - last_chat_click > 500:
                            last_chat_click = current_time
                            if chat_bubble:
                                if chat_bubble.state in ['static', 'animating']:
                                    chat_bubble.state = 'closing'
                            else:  # inserted
                                bubble_x = chat_button_x - 37
                                bubble_y = chat_button_y + chat_button_height - 20
                                chat_bubble = ChatBubble(bubble_x, bubble_y)
                        if event.button == 3:
                            if melodie.state not in untouchable and melodie.state!= 'headpat' and melodie.start_headpat(mouse_pos):
                                score += 1
                            if chonet:
                                chonet.start_headpat(mouse_pos)
                                if melodie.state!= 'headpat':
                                    chat.start_chat(random.choice(['..', 'What about me?', 'Did you replace me?', 'No! Not her!', 'The pats are for me!', 'I\'m a better pet\ndon\'t pat her!']))
                        else:  # inserted
                            if event.button == 1:
                                if pygame.Rect(kill_button_x, kill_button_y, kill_button_width, kill_button_height).collidepoint(mouse_pos):
                                    handle_kill_button(melodie, chonet, screen, background)
                                else:  # inserted
                                    if pygame.Rect(button_x, button_y, button_width, button_height).collidepoint(mouse_pos):
                                        if melodie.state not in ['wounded', 'singing', 'falling', 'dead']:
                                            score = melodie.start_singing(score)
                                    else:  # inserted
                                        if pygame.Rect(food_button_x, food_button_y, food_button_width, food_button_height).collidepoint(mouse_pos):
                                            if not menu_open:
                                                menu_open = True
                                        else:  # inserted
                                            if menu_open:
                                                if close_button_rect.collidepoint(mouse_pos):
                                                    menu_open = False
                                                else:  # inserted
                                                    for i, (item, price, image_path, heal_amount) in enumerate(items):
                                                        item_x = menu_rect.left + 150
                                                        item_y = menu_rect.top + 170 + i * 40
                                                        item_rect = pygame.Rect(item_x, item_y, 200, 40)
                                                        if item_rect.collidepoint(mouse_pos):
                                                            if item == 'Love':
                                                                effective_price = 0 if melodie.happiness == 11 else 100
                                                                if melodie.state in ('idle', 'walk') and (not melodie.is_fat):
                                                                    if score >= effective_price:
                                                                        score -= effective_price
                                                                        handle_sex_option(melodie, screen, background, clock, chat)
                                                                    else:  # inserted
                                                                        chat.start_chat(['Not enough..'])
                                                                else:  # inserted
                                                                    chat.start_chat(['Not now!\nIt\'s not time for it!'])
                                                                menu_open = False
                                                            else:  # inserted
                                                                if score >= price:
                                                                    score -= price
                                                                    current_food = None
                                                                    if 'cheese' in image_path.lower():
                                                                        frames = load_frames(['assets/food/dynamike_cheese_1.gif', 'assets/food/dynamike_cheese_2.gif'], (100, 100))
                                                                        current_food = Food(mouse_pos[0], mouse_pos[1], image_path, heal_amount, True, frames)
                                                                    else:  # inserted
                                                                        current_food = Food(mouse_pos[0], mouse_pos[1], image_path, heal_amount)
                                                                    menu_open = False
                                                            break
                                            else:  # inserted
                                                if pygame.Rect(melodie.x, melodie.y, melodie.width, melodie.height).collidepoint(mouse_pos):
                                                    if space_held and melodie.state not in untouchable:
                                                        melodie.start_dragging()
                                                        is_dragging = True
                                                        drag_offset_x, drag_offset_y = (mouse_pos[0] - melodie.x, mouse_pos[1] - melodie.y)
                                                    else:  # inserted
                                                        if melodie.state not in untouchable and (not melodie.is_fat):
                                                            melodie.take_damage(bibi)
                                                            if melodie.hit_counter == 3 and (not warning_hit) and (melodie.health > 1):
                                                                chat.start_chat(['Don\'t hit me!'])
                                                                warning_hit = True
                                                            if melodie.hit_counter >= 40:
                                                                show_stop_hitting_screen = True
                                                                pygame.mixer.music.fadeout(1000)
                                                                pygame.mixer.music.load('assets/dead.mp3')
                                                                pygame.mixer.music.set_volume(1)
                                                                pygame.mixer.music.play((-1))
                                                else:  # inserted
                                                    if current_food and pygame.Rect(current_food.x, current_food.y, 100, 100).collidepoint(mouse_pos):
                                                        current_food.start_dragging(mouse_pos)
            if event.type == pygame.MOUSEMOTION:
                if current_food and current_food.is_dragging:
                    current_food.move(event.pos)
                else:  # inserted
                    if is_dragging:
                        melodie.x = event.pos[0] - drag_offset_x
                        melodie.y = event.pos[1] - drag_offset_y
            if event.type == pygame.MOUSEBUTTONUP:
                if is_dragging:
                    is_dragging = False
                    melodie.stop_dragging()
                if current_food and current_food.is_dragging:
                    current_food.stop_dragging()
                    melodie_rect = pygame.Rect(melodie.x, melodie.y, melodie.width, melodie.height)
                    food_rect = pygame.Rect(current_food.x, current_food.y, 100, 100)
                    if melodie_rect.colliderect(food_rect):
                        melodie.eat(current_food, chat)
                        if 'janet' in current_food.image_path.lower():
                            janet_head_eaten_count += 1
                            if janet_head_eaten_count % 3 == 0 and chonet is None:
                                chonet = Chonet(-SPRITE_SIZE[0], 475)
                                melodie._happiness(False)
                        current_food = None
                    else:  # inserted
                        if chonet and pygame.Rect(chonet.x, chonet.y, chonet.width, chonet.height).colliderect(pygame.Rect(current_food.x, current_food.y, 100, 100)):
                            if 'janet' in current_food.image_path.lower():
                                chonet.set_state('janet')
                                current_food = None
                                pygame.mixer.Sound('assets/sound/eating.mp3').play()
                                chonet.y = melodie.y
                                chat.start_chat(wrap_text('I told you I\'d see you when you grew up, but I didn\'t expect it to be this early..'))
            if event.type == pygame.USEREVENT + 1:
                melodie.stop_singing()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if melodie.is_fat and melodie.state == 'dragging':
                    poops.append(Poop(melodie.x + 70, melodie.y + 100))
                    melodie.drop_poop()
                    melodie.health = 5
        if not show_stop_hitting_screen:
            screen.blit(background, (0, 0))
            draw_score(screen, score, score_font, 20, 17)
            draw_button(screen, 220, 60, 113, 61, 'assets/buttons/sing.png')
            draw_button(screen, 358, 60, 113, 61, 'assets/buttons/food.png')
            draw_button(screen, 496, 60, 115, 61, 'assets/buttons/sup_chat.png')
            if chat_bubble:
                chat_bubble.update(delta_time)
                if chat_bubble.state == 'closed':
                    if chat_bubble.selected_option is not None and (not decision_menu):
                        chat_choice = chat_bubble.selected_option
                        options = get_decision_options(chat_choice)
                        decision_menu = DecisionMenu(chat_bubble.x - 200, chat_bubble.y + chat_bubble.size[1] - 200, options)
                        chat_bubble = None
                else:  # inserted
                    chat_bubble.draw(screen)
            if decision_menu:
                decision_menu.draw(screen)
            chat.update()
            melodie.update(delta_time, chat, score, current_food)
            melodie.draw(screen)
            draw_happiness_bar(screen, melodie.happiness)
            if chonet:
                chonet.draw(screen)
                chonet.update(delta_time)
            if current_food:
                current_food.draw(screen)
            if chonet and is_melodie_on_chonet(melodie, chonet) and (chonet.state not in ('dead', 'janet')) and (melodie.state not in untouchable) and (melodie.state not in ('dragging', 'falling')):
                draw_button(screen, 25, 340, 144, 144, 'assets/buttons/kill.png')
            for poop in poops:
                poop.update()
                poop.draw(screen)
            poops = [poop for poop in poops if poop.active]
            screen.blit(bibi_button_img, bibi_button_rect)
            if bibi is not None and bibi.state in ('walking_in', 'walking_out') and (abs(melodie.x - (bibi.x + BIBI_WALK_SIZE[0] // 2)) < 150):
                if melodie.x < bibi.x:
                    melodie.target_x = max(0, melodie.x - 100)
                else:  # inserted
                    melodie.target_x = min(WIDTH - melodie.width, melodie.x + 100)
            if bibi is not None:
                bibi.update(delta_time)
                if bibi.state == 'hidden':
                    bibi = None
                    bibi_chat = None
            if bibi is not None:
                bibi.draw(screen)
            if bibi_chat is not None:
                bibi_chat.draw(screen)
            if menu_open:
                screen.blit(menu_image, menu_rect)
                screen.blit(close_button_image, close_button_rect)
                for i, (item, price, _, _) in enumerate(items):
                    if item == 'Love' and melodie.happiness == 11:
                        display_text = f'{item} - Free'
                    else:  # inserted
                        display_text = f'{item} - {price} pts'
                    item_text = menu_font.render(display_text, True, (144, 64, 117))
                    item_x = menu_rect.left + 150
                    item_y = menu_rect.top + 170 + i * 40
                    item_rect = pygame.Rect(item_x, item_y, 200, 40)
                    screen.blit(item_text, item_rect)
            if current_food and current_food.image_path == 'assets/food/egg.png' and current_food.should_hatch():
                current_food.hatch_count = hatch_count
                if not hatch_count > 2 and current_food.hatch():
                    if hatch_count == 1:
                        pet_frames = load_frames(['assets/pets/note_2_1.gif', 'assets/pets/note_2_2.gif'], (80, 64))
                        chat.start_chat(['W-what!\nThe egg hatched!?'])
                        hatch_count += 1
                    else:  # inserted
                        pet_frames = load_frames(['assets/pets/note_1.png'], (80, 80))
                        chat.start_chat(['It happened again..', 'This time it\'s another\nbaby note..'])
                    flying_pets.append(FlyingPet(current_food.x, current_food.y, pet_frames))
                    current_food = None
            for pet in flying_pets:
                pet.update()
                pet.draw(screen)
            flying_pets = [pet for pet in flying_pets if not pet.is_expired()]
        else:  # inserted
            screen.fill((0, 0, 0))
            text_timer += delta_time
            if text_timer >= TEXT_SPEED:
                text_progress += 1
                text_timer = 0
            draw_text_animated(screen, text, font, (255, 255, 255), WIDTH // 4, HEIGHT // 2, text_progress)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and text_progress >= len(text):
                    running = False
        pygame.display.update()
    pygame.mixer.music.stop()
    pygame.quit()

class ChatBubble:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = (200, 250)
        self.anim_frames = load_frames(['assets/buttons/bubble_anim_1.gif', 'assets/buttons/bubble_anim_2.gif', 'assets/buttons/bubble_anim_3.gif'], self.size)
        self.bubble_img = pygame.image.load('assets/buttons/bubble.png').convert_alpha()
        self.bubble_img = pygame.transform.scale(self.bubble_img, self.size)
        self.state = 'animating'
        self.current_frame_index = 0
        self.anim_timer = 0
        self.anim_duration = 50
        self.texts = ['Love', 'Neutral', 'Hate']
        self.selected_option = None
        self.font = pygame.font.Font('assets/fonts/ByteBounce.ttf', 30)
        self.text_surfaces = [self.font.render(text, True, (144, 64, 117)) for text in self.texts]
        total_text_height = sum((surface.get_height() for surface in self.text_surfaces))
        spacing = (self.size[1] - total_text_height) // (len(self.text_surfaces) + 1)
        self.text_rects = []
        current_y = self.y + spacing
        for surface in self.text_surfaces:
            text_width = surface.get_width()
            text_height = surface.get_height()
            x_offset = self.x + (self.size[0] - text_width) // 2
            rect = pygame.Rect(x_offset, current_y, text_width, text_height)
            self.text_rects.append(rect)
            current_y += text_height + spacing

    def update(self, delta_time):
        if self.state == 'animating':
            self.anim_timer += delta_time
            if self.anim_timer >= self.anim_duration:
                self.anim_timer = 0
                self.current_frame_index += 1
                if self.current_frame_index >= len(self.anim_frames):
                    self.state = 'static'
        else:  # inserted
            if self.state == 'closing':
                self.anim_timer += delta_time
                if self.anim_timer >= self.anim_duration:
                    self.anim_timer = 0
                    self.current_frame_index -= 1
                    if self.current_frame_index < 0:
                        self.state = 'closed'

    def draw(self, screen):
        if self.state in ['animating', 'closing']:
            frame = self.anim_frames[self.current_frame_index % len(self.anim_frames)]
            screen.blit(frame, (self.x, self.y))
        else:  # inserted
            if self.state == 'static':
                screen.blit(self.bubble_img, (self.x, self.y))
                for i, surface in enumerate(self.text_surfaces):
                    screen.blit(surface, self.text_rects[i])

    def handle_event(self, event):
        if self.state == 'static' and event.type == pygame.MOUSEBUTTONDOWN and (event.button == 1):
            mouse_pos = event.pos
            for i, rect in enumerate(self.text_rects):
                if rect.collidepoint(mouse_pos):
                    self.selected_option = i
                    self.state = 'closing'
                    break

class DecisionMenu:
    def __init__(self, x, y, options) -> None:
        self.x = x
        self.y = y
        self.image = pygame.image.load('assets/buttons/decision_menu.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (300, 200))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.options = options
        self.font = pygame.font.Font('assets/fonts/ByteBounce.ttf', 24)
        self.options_surfaces = [self.font.render(opt, True, (144, 64, 117)) for opt in options]
        total_text_height = sum((surface.get_height() for surface in self.options_surfaces))
        spacing = (self.rect.height - total_text_height) // (len(self.options_surfaces) + 1)
        self.option_rects = []
        current_y = self.y + spacing
        for surface in self.options_surfaces:
            text_width = surface.get_width()
            text_height = surface.get_height()
            x_offset = self.x + (self.rect.width - text_width) // 2
            rect = pygame.Rect(x_offset, current_y, text_width, text_height)
            self.option_rects.append(rect)
            current_y += text_height + spacing
        self.active = True

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        for i, surface in enumerate(self.options_surfaces):
            screen.blit(surface, self.option_rects[i])

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            for i, rect in enumerate(self.option_rects):
                if rect.collidepoint(mouse_pos):
                    return i
        return None

class NewWorldMelodie:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.velocity_y = 0
        self.on_ground = True
        self.speed = 4
        self.jump_strength = (-15)

    def update(self, keys):
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_w] and self.on_ground:
            self.velocity_y = self.jump_strength
            self.on_ground = False
        self.velocity_y += 1
        self.y += self.velocity_y
        if self.y >= HEIGHT - self.height:
            self.y = HEIGHT - self.height
            self.velocity_y = 0
            self.on_ground = True

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.width, self.height))

def generate_new_world():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    new_melodie = NewWorldMelodie(400, HEIGHT - 50)
    door_rect = pygame.Rect(10, HEIGHT - 120, 50, 120)
    running = True
    while running:
        delta_time = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        new_melodie.update(keys)
        mel_rect = pygame.Rect(new_melodie.x, new_melodie.y, new_melodie.width, new_melodie.height)
        if mel_rect.colliderect(door_rect):
            running = False
            generate_pet_world()
            return
        screen.fill((100, 149, 237))
        pygame.draw.rect(screen, (255, 182, 193), door_rect)
        new_melodie.draw(screen)
        pygame.display.flip()
pygame.display.set_caption('Melodie Pet Game')
entrance_animation(screen)
generate_pet_world()