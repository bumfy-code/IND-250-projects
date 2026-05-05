import math
import random
import pygame

# Window settings
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 660
FPS = 60

# World/Map settings
WORLD_WIDTH = 2800
WORLD_HEIGHT = 2000

# Gameplay settings
PLAYER_SPEED = 260
PLAYER_RADIUS = 16
PLAYER_HEALTH = 100
BULLET_SPEED = 820
BULLET_RADIUS = 5
ENEMY_SPAWN_DISTANCE = 400
ENEMY_RADIUS = 18
PICKUP_RADIUS = 14
WAVE_START_DELAY = 1.5

# Weapon types
WEAPON_PISTOL = 'pistol'
WEAPON_SHOTGUN = 'shotgun'
WEAPON_SMG = 'smg'

# Colors
COLOR_BG = (18, 24, 45)
COLOR_GRID = (36, 46, 74)
COLOR_TEXT = (240, 240, 240)
COLOR_HEALTH = (180, 40, 40)
COLOR_PICKUP = (20, 200, 100)
COLOR_GRASS_LIGHT = (60, 120, 45)
COLOR_GRASS_DARK = (45, 100, 35)
COLOR_ROAD = (90, 85, 75)
COLOR_ROAD_MARK = (200, 200, 180)

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PIXEL SHOOTER")
clock = pygame.time.Clock()
font_big = pygame.font.Font(None, 56)
font_small = pygame.font.Font(None, 24)

# Fullscreen state
is_fullscreen = False


def create_player_sprite(size=40):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 0))
    body = pygame.Rect(size * 0.25, size * 0.25, size * 0.5, size * 0.5)
    pygame.draw.rect(surf, (100, 190, 240), body)
    pygame.draw.rect(surf, (20, 80, 110), body, 3)
    helmet = pygame.Rect(size * 0.18, size * 0.05, size * 0.64, size * 0.35)
    pygame.draw.rect(surf, (70, 120, 180), helmet)
    pygame.draw.rect(surf, (20, 50, 90), helmet, 3)
    visor = pygame.Rect(size * 0.28, size * 0.12, size * 0.44, size * 0.18)
    pygame.draw.rect(surf, (235, 255, 255), visor)
    pygame.draw.rect(surf, (30, 80, 120), visor, 2)
    pygame.draw.circle(surf, (80, 120, 190), (int(size * 0.5), int(size * 0.55)), int(size * 0.16))
    pygame.draw.rect(surf, (60, 80, 120), (size * 0.45, size * 0.6, size * 0.1, size * 0.2))
    return surf


def create_enemy_sprite(color, size=34):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 0))
    body = pygame.Rect(size * 0.18, size * 0.22, size * 0.64, size * 0.56)
    pygame.draw.rect(surf, color, body)
    pygame.draw.rect(surf, (30, 30, 30), body, 2)
    eye_left = pygame.Rect(size * 0.30, size * 0.30, size * 0.12, size * 0.12)
    eye_right = pygame.Rect(size * 0.58, size * 0.30, size * 0.12, size * 0.12)
    pygame.draw.rect(surf, (250, 250, 255), eye_left)
    pygame.draw.rect(surf, (250, 250, 255), eye_right)
    pygame.draw.rect(surf, (25, 25, 25), eye_left, 2)
    pygame.draw.rect(surf, (25, 25, 25), eye_right, 2)
    pygame.draw.rect(surf, (25, 25, 25), (size * 0.43, size * 0.62, size * 0.14, size * 0.10))
    return surf


def create_bullet_sprite(radius=BULLET_RADIUS * 2):
    surf = pygame.Surface((radius, radius), pygame.SRCALPHA)
    pygame.draw.circle(surf, (255, 235, 120), (radius // 2, radius // 2), radius // 2)
    return surf


def create_pickup_sprite(size=22):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.rect(surf, (20, 170, 80), (0, 0, size, size), border_radius=6)
    pygame.draw.line(surf, (240, 240, 240), (size * 0.5, size * 0.18), (size * 0.5, size * 0.82), 4)
    pygame.draw.line(surf, (240, 240, 240), (size * 0.18, size * 0.5), (size * 0.82, size * 0.5), 4)
    return surf


def create_building_office(width=80, height=120):
    """Modern office building"""
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    # Main structure
    pygame.draw.rect(surf, (140, 140, 150), (0, 0, width, height))
    pygame.draw.rect(surf, (60, 60, 70), (0, 0, width, height), 4)
    # Windows
    window_color = (180, 220, 255)
    for row in range(0, height - 10, 16):
        for col in range(5, width - 5, 16):
            pygame.draw.rect(surf, window_color, (col, row + 5, 10, 10))
            pygame.draw.rect(surf, (40, 40, 50), (col, row + 5, 10, 10), 1)
    # Door
    pygame.draw.rect(surf, (80, 50, 20), (width // 2 - 8, height - 20, 16, 20))
    return surf


def create_building_warehouse(width=140, height=90):
    """Industrial warehouse"""
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    # Main structure - rust/industrial color
    pygame.draw.rect(surf, (120, 95, 75), (0, 0, width, height))
    pygame.draw.rect(surf, (70, 50, 30), (0, 0, width, height), 3)
    # Corrugated panels effect
    for y in range(0, height, 12):
        pygame.draw.line(surf, (100, 75, 55), (0, y), (width, y), 2)
    # Large door
    door_width = int(width * 0.6)
    door_x = (width - door_width) // 2
    pygame.draw.rect(surf, (60, 50, 40), (door_x, height - 35, door_width, 35))
    pygame.draw.line(surf, (80, 70, 60), (door_x + door_width // 2, height - 35), (door_x + door_width // 2, height), 2)
    return surf


def create_building_residential(width=70, height=100):
    """Residential apartment building"""
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    # Main structure - lighter brick color
    pygame.draw.rect(surf, (180, 120, 100), (0, 0, width, height))
    pygame.draw.rect(surf, (120, 70, 50), (0, 0, width, height), 3)
    # Windows in grid pattern
    window_color = (220, 240, 255)
    for row in range(0, height - 15, 18):
        for col in range(6, width - 6, 20):
            pygame.draw.rect(surf, window_color, (col, row + 5, 12, 12))
            pygame.draw.rect(surf, (100, 100, 100), (col, row + 5, 12, 12), 1)
            # Window cross
            pygame.draw.line(surf, (100, 100, 100), (col + 6, row + 5), (col + 6, row + 17), 1)
            pygame.draw.line(surf, (100, 100, 100), (col, row + 11), (col + 12, row + 11), 1)
    return surf


def create_building_tower(width=60, height=140):
    """Tall communication/antenna tower"""
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    # Main tower structure - metallic gray
    pygame.draw.polygon(surf, (120, 130, 140), [(0, height), (width, height), (width * 0.8, 0), (width * 0.2, 0)])
    pygame.draw.polygon(surf, (80, 85, 95), [(0, height), (width, height), (width * 0.8, 0), (width * 0.2, 0)], 3)
    # Antenna
    mid_x = width // 2
    pygame.draw.line(surf, (255, 100, 100), (mid_x, 10), (mid_x, -10), 3)
    pygame.draw.line(surf, (255, 100, 100), (mid_x - 8, 5), (mid_x + 8, 5), 2)
    # Structural beams
    pygame.draw.line(surf, (100, 110, 120), (width * 0.2, 0), (width * 0.3, height * 0.5), 1)
    pygame.draw.line(surf, (100, 110, 120), (width * 0.8, 0), (width * 0.7, height * 0.5), 1)
    return surf


def create_building_factory(width=120, height=100):
    """Factory with smokestacks"""
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    # Main building
    pygame.draw.rect(surf, (95, 95, 105), (10, 30, width - 20, 70))
    pygame.draw.rect(surf, (60, 60, 70), (10, 30, width - 20, 70), 2)
    # Smokestacks
    stack_positions = [20, 50, 80, 110]
    for x in stack_positions:
        if x < width - 10:
            pygame.draw.rect(surf, (70, 70, 75), (x, 0, 12, 35))
            pygame.draw.rect(surf, (50, 50, 55), (x, 0, 12, 35), 1)
            # Smoke effect
            pygame.draw.circle(surf, (120, 120, 130), (x + 6, -5), 4)
    # Windows
    for row in range(40, 90, 18):
        for col in range(20, width - 20, 22):
            pygame.draw.rect(surf, (160, 180, 200), (col, row, 10, 10))
    # Door
    pygame.draw.rect(surf, (80, 60, 40), (width // 2 - 12, 90, 24, 30))
    return surf

player_sprite = create_player_sprite()
enemy_sprite_normal = create_enemy_sprite((220, 65, 65))
enemy_sprite_fast = create_enemy_sprite((255, 180, 60))
enemy_sprite_tank = create_enemy_sprite((95, 190, 95))
bullet_sprite = create_bullet_sprite()
pickup_sprite = create_pickup_sprite()


class Bullet:
    def __init__(self, pos, direction, damage=16):
        self.pos = pygame.Vector2(pos)
        self.velocity = pygame.Vector2(direction).normalize() * BULLET_SPEED
        self.radius = BULLET_RADIUS
        self.damage = damage
        self.alive = True

    def update(self, dt):
        self.pos += self.velocity * dt
        if not (0 <= self.pos.x <= WORLD_WIDTH and 0 <= self.pos.y <= WORLD_HEIGHT):
            self.alive = False

    def draw(self, surface):
        offset = pygame.Vector2(self.radius, self.radius)
        surface.blit(bullet_sprite, self.pos - offset)


class Enemy:
    def __init__(self, pos, kind='normal'):
        self.pos = pygame.Vector2(pos)
        self.kind = kind
        self.radius = ENEMY_RADIUS
        self.alive = True
        if kind == 'fast':
            self.speed = 200
            self.health = 18
            self.sprite = enemy_sprite_fast
        elif kind == 'tank':
            self.speed = 120
            self.health = 45
            self.sprite = enemy_sprite_tank
        else:
            self.speed = 160
            self.health = 28
            self.sprite = enemy_sprite_normal

    def update(self, dt, target_pos):
        direction = pygame.Vector2(target_pos) - self.pos
        if direction.length_squared() > 0.1:
            self.pos += direction.normalize() * self.speed * dt

    def draw(self, surface):
        offset = pygame.Vector2(self.sprite.get_width() / 2, self.sprite.get_height() / 2)
        surface.blit(self.sprite, self.pos - offset)

    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            return True
        return False


class Pickup:
    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
        self.radius = PICKUP_RADIUS
        self.alive = True
        self.sprite = pickup_sprite

    def draw(self, surface):
        offset = pygame.Vector2(self.sprite.get_width() / 2, self.sprite.get_height() / 2)
        surface.blit(self.sprite, self.pos - offset)


class Building:
    def __init__(self, pos, sprite, width, height):
        self.pos = pygame.Vector2(pos)
        self.sprite = sprite
        self.width = width
        self.height = height
        self.collision_radius = (width + height) / 4

    def draw(self, surface, screen_pos):
        offset = pygame.Vector2(self.width / 2, self.height / 2)
        surface.blit(self.sprite, screen_pos - offset)

    def collides_with(self, pos, radius):
        """Check if a point with given radius collides with building"""
        return (pos - self.pos).length() < (self.collision_radius + radius)


class Player:
    def __init__(self):
        self.pos = pygame.Vector2(WORLD_WIDTH / 2, WORLD_HEIGHT / 2)
        self.radius = PLAYER_RADIUS
        self.health = PLAYER_HEALTH
        self.score = 0
        self.wave = 1
        self.last_shot = 0
        self.alive = True
        self.sprite = player_sprite
        
        # Weapon system
        self.current_weapon = WEAPON_PISTOL
        self.weapons = {
            WEAPON_PISTOL: {'shoot_delay': 0.18, 'damage': 16, 'bullets_per_shot': 1, 'spread': 0},
            WEAPON_SHOTGUN: {'shoot_delay': 0.6, 'damage': 20, 'bullets_per_shot': 8, 'spread': 0.35},
            WEAPON_SMG: {'shoot_delay': 0.08, 'damage': 10, 'bullets_per_shot': 1, 'spread': 0.15}
        }

    def can_shoot(self, current_time):
        weapon = self.weapons[self.current_weapon]
        return current_time - self.last_shot >= weapon['shoot_delay']

    def shoot(self, target_pos, current_time):
        self.last_shot = current_time
        bullets = []
        weapon = self.weapons[self.current_weapon]
        direction = pygame.Vector2(target_pos) - self.pos
        
        if direction.length_squared() == 0:
            direction = pygame.Vector2(1, 0)
        else:
            direction = direction.normalize()
        
        # Create bullets based on weapon type
        for i in range(weapon['bullets_per_shot']):
            if weapon['spread'] > 0:
                angle_offset = random.uniform(-weapon['spread'], weapon['spread'])
                rotated = direction.rotate(math.degrees(angle_offset))
                bullets.append(Bullet(self.pos, rotated, weapon['damage']))
            else:
                bullets.append(Bullet(self.pos, direction, weapon['damage']))
        
        return bullets

    def switch_weapon(self, weapon_type):
        if weapon_type in self.weapons:
            self.current_weapon = weapon_type

    def move(self, dt, keys):
        velocity = pygame.Vector2(0, 0)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            velocity.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            velocity.y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            velocity.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            velocity.x += 1
        if velocity.length_squared() > 0:
            velocity = velocity.normalize() * PLAYER_SPEED
            self.pos += velocity * dt
            # Clamp to world boundaries
            self.pos.x = max(self.radius, min(WORLD_WIDTH - self.radius, self.pos.x))
            self.pos.y = max(self.radius, min(WORLD_HEIGHT - self.radius, self.pos.y))

    def draw(self, surface, aim_pos):
        rotated = pygame.transform.rotate(self.sprite, -math.degrees(math.atan2(aim_pos.y - self.pos.y, aim_pos.x - self.pos.x)))
        offset = pygame.Vector2(rotated.get_width() / 2, rotated.get_height() / 2)
        surface.blit(rotated, self.pos - offset)


def draw_background(surface, camera_pos):
    # Fill with grass base color
    surface.fill(COLOR_GRASS_LIGHT)
    
    # Draw grass patches for variation
    patch_size = 120
    start_x = int(camera_pos.x // patch_size) * patch_size
    start_y = int(camera_pos.y // patch_size) * patch_size
    
    for world_x in range(start_x - patch_size, start_x + SCREEN_WIDTH + patch_size, patch_size):
        for world_y in range(start_y - patch_size, start_y + SCREEN_HEIGHT + patch_size, patch_size):
            # Use world coordinates for seeding consistent patch colors
            seed = (world_x // patch_size + world_y // patch_size * 997) % 4
            if seed == 0 or seed == 3:  # Add darker grass patches
                screen_x = world_x - camera_pos.x
                screen_y = world_y - camera_pos.y
                pygame.draw.rect(surface, COLOR_GRASS_DARK, (screen_x, screen_y, patch_size, patch_size))
    
    # Draw roads - horizontal and vertical grid pattern
    road_width = 40
    road_spacing = 400
    
    # Draw horizontal roads
    start_y = int(camera_pos.y // road_spacing) * road_spacing
    for world_y in range(start_y - road_spacing, start_y + SCREEN_HEIGHT + road_spacing, road_spacing):
        if 0 <= world_y <= WORLD_HEIGHT:
            screen_y = world_y - camera_pos.y
            pygame.draw.rect(surface, COLOR_ROAD, (0 - camera_pos.x, screen_y - road_width // 2, WORLD_WIDTH, road_width))
            # Draw road markings
            mark_spacing = 80
            start_x = int(camera_pos.x // mark_spacing) * mark_spacing
            for world_x in range(start_x, start_x + SCREEN_WIDTH + mark_spacing, mark_spacing):
                screen_x = world_x - camera_pos.x
                pygame.draw.rect(surface, COLOR_ROAD_MARK, (screen_x - 20, screen_y - 2, 40, 4))
    
    # Draw vertical roads
    start_x = int(camera_pos.x // road_spacing) * road_spacing
    for world_x in range(start_x - road_spacing, start_x + SCREEN_WIDTH + road_spacing, road_spacing):
        if 0 <= world_x <= WORLD_WIDTH:
            screen_x = world_x - camera_pos.x
            pygame.draw.rect(surface, COLOR_ROAD, (screen_x - road_width // 2, 0 - camera_pos.y, road_width, WORLD_HEIGHT))
            # Draw road markings
            mark_spacing = 80
            start_y = int(camera_pos.y // mark_spacing) * mark_spacing
            for world_y in range(start_y, start_y + SCREEN_HEIGHT + mark_spacing, mark_spacing):
                screen_y = world_y - camera_pos.y
                pygame.draw.rect(surface, COLOR_ROAD_MARK, (screen_x - 2, screen_y - 20, 4, 40))
    
    # Draw subtle grid lines
    grid_spacing = 44
    start_x = int(camera_pos.x // grid_spacing) * grid_spacing
    start_y = int(camera_pos.y // grid_spacing) * grid_spacing
    grid_color = (80, 95, 70)  # Subtle green-tinted grid
    
    for x in range(start_x, start_x + SCREEN_WIDTH + grid_spacing, grid_spacing):
        screen_x = x - camera_pos.x
        pygame.draw.line(surface, grid_color, (screen_x, 0), (screen_x, SCREEN_HEIGHT), 1)
    
    for y in range(start_y, start_y + SCREEN_HEIGHT + grid_spacing, grid_spacing):
        screen_y = y - camera_pos.y
        pygame.draw.line(surface, grid_color, (0, screen_y), (SCREEN_WIDTH, screen_y), 1)
    
    # Draw world boundaries
    boundary_color = (100, 100, 120)
    boundary_thickness = 3
    
    if camera_pos.x < 100:
        pygame.draw.line(surface, boundary_color, (-camera_pos.x, 0), (-camera_pos.x, SCREEN_HEIGHT), boundary_thickness)
    if camera_pos.y < 100:
        pygame.draw.line(surface, boundary_color, (0, -camera_pos.y), (SCREEN_WIDTH, -camera_pos.y), boundary_thickness)
    if camera_pos.x + SCREEN_WIDTH > WORLD_WIDTH - 100:
        screen_x = WORLD_WIDTH - camera_pos.x
        pygame.draw.line(surface, boundary_color, (screen_x, 0), (screen_x, SCREEN_HEIGHT), boundary_thickness)
    if camera_pos.y + SCREEN_HEIGHT > WORLD_HEIGHT - 100:
        screen_y = WORLD_HEIGHT - camera_pos.y
        pygame.draw.line(surface, boundary_color, (0, screen_y), (SCREEN_WIDTH, screen_y), boundary_thickness)


def draw_ui(surface, player, wave, lives, enemies_remaining, camera_pos):
    health_text = font_small.render(f"Health: {player.health}", True, COLOR_TEXT)
    score_text = font_small.render(f"Score: {player.score}", True, COLOR_TEXT)
    wave_text = font_small.render(f"Wave: {wave}", True, COLOR_TEXT)
    enemy_text = font_small.render(f"Enemies: {enemies_remaining}", True, COLOR_TEXT)
    
    # Weapon names
    weapon_names = {WEAPON_PISTOL: "Pistol", WEAPON_SHOTGUN: "Shotgun", WEAPON_SMG: "Auto SMG"}
    weapon_text = font_small.render(f"Weapon: {weapon_names[player.current_weapon]} (1/2/3)", True, (100, 200, 255))
    
    # Position text
    pos_text = font_small.render(f"Pos: {int(player.pos.x)}, {int(player.pos.y)}", True, (150, 150, 150))
    
    surface.blit(health_text, (18, 16))
    surface.blit(score_text, (18, 42))
    surface.blit(weapon_text, (18, 68))
    surface.blit(wave_text, (SCREEN_WIDTH - wave_text.get_width() - 18, 16))
    surface.blit(enemy_text, (SCREEN_WIDTH - enemy_text.get_width() - 18, 42))
    surface.blit(pos_text, (SCREEN_WIDTH - pos_text.get_width() - 18, 68))

    if player.health < 40:
        danger = font_small.render("LOW HEALTH! Find a medkit.", True, COLOR_HEALTH)
        surface.blit(danger, (18, SCREEN_HEIGHT - 32))



def toggle_fullscreen():
    """Toggle between fullscreen and windowed mode"""
    global screen, is_fullscreen
    is_fullscreen = not is_fullscreen
    if is_fullscreen:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("PIXEL SHOOTER")


def get_camera_pos(player_pos):
    """Calculate camera position to keep player centered on screen"""
    camera_x = player_pos.x - SCREEN_WIDTH / 2
    camera_y = player_pos.y - SCREEN_HEIGHT / 2
    # Clamp camera to world boundaries
    camera_x = max(0, min(WORLD_WIDTH - SCREEN_WIDTH, camera_x))
    camera_y = max(0, min(WORLD_HEIGHT - SCREEN_HEIGHT, camera_y))
    return pygame.Vector2(camera_x, camera_y)


def world_to_screen(world_pos, camera_pos):
    """Convert world coordinates to screen coordinates"""
    return world_pos - camera_pos


def draw_center_overlay(surface, text, subtext=None):
    label = font_big.render(text, True, COLOR_TEXT)
    surface.blit(label, ((SCREEN_WIDTH - label.get_width()) / 2, SCREEN_HEIGHT * 0.28))
    if subtext:
        hint = font_small.render(subtext, True, COLOR_TEXT)
        surface.blit(hint, ((SCREEN_WIDTH - hint.get_width()) / 2, SCREEN_HEIGHT * 0.5))


def spawn_enemy(player, wave):
    # Spawn enemies in a circle around the player, respecting world boundaries
    angle = random.uniform(0, 2 * math.pi)
    distance = ENEMY_SPAWN_DISTANCE + random.uniform(-50, 50)
    
    pos_x = player.pos.x + math.cos(angle) * distance
    pos_y = player.pos.y + math.sin(angle) * distance
    
    # Clamp to world boundaries
    pos_x = max(ENEMY_RADIUS, min(WORLD_WIDTH - ENEMY_RADIUS, pos_x))
    pos_y = max(ENEMY_RADIUS, min(WORLD_HEIGHT - ENEMY_RADIUS, pos_y))
    
    pos = pygame.Vector2(pos_x, pos_y)

    choice = random.random()
    if wave >= 5 and choice < 0.18:
        return Enemy(pos, 'tank')
    if choice < 0.42:
        return Enemy(pos, 'fast')
    return Enemy(pos, 'normal')


def reset_game():
    player = Player()
    bullets = []
    enemies = []
    pickups = []
    buildings = generate_buildings()
    wave = 1
    spawn_timer = 0.0
    wave_active = False
    wave_delay = WAVE_START_DELAY
    return player, bullets, enemies, pickups, buildings, wave, spawn_timer, wave_active, wave_delay


def generate_buildings():
    """Generate a variety of buildings scattered across the map"""
    buildings = []
    building_types = [
        ('office', create_building_office, 80, 120),
        ('warehouse', create_building_warehouse, 140, 90),
        ('residential', create_building_residential, 70, 100),
        ('tower', create_building_tower, 60, 140),
        ('factory', create_building_factory, 120, 100),
    ]
    
    min_distance = 200
    attempts = 0
    max_attempts = 150
    
    while len(buildings) < 18 and attempts < max_attempts:
        attempts += 1
        building_type, sprite_func, width, height = random.choice(building_types)
        
        # Try to place building in random location
        x = random.randint(int(width / 2 + 100), int(WORLD_WIDTH - width / 2 - 100))
        y = random.randint(int(height / 2 + 100), int(WORLD_HEIGHT - height / 2 - 100))
        new_pos = pygame.Vector2(x, y)
        
        # Check distance from other buildings
        too_close = False
        for building in buildings:
            if (new_pos - building.pos).length() < min_distance:
                too_close = True
                break
        
        if not too_close:
            sprite = sprite_func()
            building = Building(new_pos, sprite, width, height)
            buildings.append(building)
    
    return buildings


player, bullets, enemies, pickups, buildings, wave, spawn_timer, wave_active, wave_delay = reset_game()
game_state = 'MENU'
spawn_pickup_timer = 0.0
pickup_interval = 6.0
camera_pos = pygame.Vector2(0, 0)

running = True
while running:
    dt = clock.tick(FPS) / 1000.0
    now = pygame.time.get_ticks() / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_state == 'MENU' and event.key == pygame.K_SPACE:
                game_state = 'PLAYING'
                player, bullets, enemies, pickups, buildings, wave, spawn_timer, wave_active, wave_delay = reset_game()
            elif game_state == 'GAME_OVER' and event.key == pygame.K_r:
                game_state = 'PLAYING'
                player, bullets, enemies, pickups, buildings, wave, spawn_timer, wave_active, wave_delay = reset_game()
            elif event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_f:
                toggle_fullscreen()
            # Weapon switching
            elif game_state == 'PLAYING' and event.key == pygame.K_1:
                player.switch_weapon(WEAPON_PISTOL)
            elif game_state == 'PLAYING' and event.key == pygame.K_2:
                player.switch_weapon(WEAPON_SHOTGUN)
            elif game_state == 'PLAYING' and event.key == pygame.K_3:
                player.switch_weapon(WEAPON_SMG)
        if game_state == 'PLAYING' and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and player.can_shoot(now):
                new_bullets = player.shoot(pygame.Vector2(pygame.mouse.get_pos()) + camera_pos, now)
                bullets.extend(new_bullets)

    keys = pygame.key.get_pressed()
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

    if game_state == 'PLAYING':
        player.move(dt, keys)
        camera_pos = get_camera_pos(player.pos)
        
        if keys[pygame.K_SPACE] and player.can_shoot(now):
            new_bullets = player.shoot(mouse_pos + camera_pos, now)
            bullets.extend(new_bullets)

        for bullet in bullets:
            bullet.update(dt)
        bullets = [bullet for bullet in bullets if bullet.alive]

        for enemy in enemies:
            enemy.update(dt, player.pos)

        for pickup in pickups:
            if (pickup.pos - player.pos).length_squared() < (pickup.radius + player.radius) ** 2:
                player.health = min(PLAYER_HEALTH, player.health + 26)
                pickup.alive = False

        for bullet in bullets:
            for enemy in enemies:
                if enemy.alive and (bullet.pos - enemy.pos).length_squared() < (bullet.radius + enemy.radius) ** 2:
                    enemy.hit(bullet.damage)
                    bullet.alive = False
                    if not enemy.alive:
                        player.score += 15 + wave * 4
                        if enemy.kind == 'fast':
                            player.score += 6
                        elif enemy.kind == 'tank':
                            player.score += 14
        bullets = [bullet for bullet in bullets if bullet.alive]

        enemies = [enemy for enemy in enemies if enemy.alive]
        pickups = [pickup for pickup in pickups if pickup.alive]

        if any((enemy.pos - player.pos).length_squared() < (enemy.radius + player.radius) ** 2 for enemy in enemies):
            player.health -= 1
            if player.health <= 0:
                player.alive = False
                game_state = 'GAME_OVER'

        if not wave_active:
            spawn_timer += dt
            if spawn_timer >= wave_delay:
                enemies = [spawn_enemy(player, wave) for _ in range(4 + wave * 2)]
                wave_active = True
                spawn_timer = 0.0
        else:
            if not enemies:
                wave += 1
                wave_active = False
                wave_delay = max(0.8, WAVE_START_DELAY - wave * 0.08)
                player.score += 30

        spawn_pickup_timer += dt
        if spawn_pickup_timer >= pickup_interval:
            padding = 70
            pos = pygame.Vector2(random.randint(padding, WORLD_WIDTH - padding), random.randint(padding, WORLD_HEIGHT - padding))
            pickups.append(Pickup(pos))
            spawn_pickup_timer = 0.0
            pickup_interval = max(4.4, pickup_interval - 0.2)

    draw_background(screen, camera_pos)

    if game_state == 'MENU':
        draw_center_overlay(screen, "PIXEL SHOOTER", "Press SPACE to start — F for fullscreen — WASD/arrows + mouse to play")
    elif game_state == 'PLAYING':
        # Draw buildings (in background)
        for building in buildings:
            screen_pos = world_to_screen(building.pos, camera_pos)
            if -150 < screen_pos.x < SCREEN_WIDTH + 150 and -150 < screen_pos.y < SCREEN_HEIGHT + 150:
                building.draw(screen, screen_pos)
        
        # Draw pickups
        for pickup in pickups:
            screen_pos = world_to_screen(pickup.pos, camera_pos)
            if -50 < screen_pos.x < SCREEN_WIDTH + 50 and -50 < screen_pos.y < SCREEN_HEIGHT + 50:
                offset = pygame.Vector2(pickup.sprite.get_width() / 2, pickup.sprite.get_height() / 2)
                screen.blit(pickup.sprite, screen_pos - offset)
        
        # Draw enemies
        for enemy in enemies:
            screen_pos = world_to_screen(enemy.pos, camera_pos)
            if -50 < screen_pos.x < SCREEN_WIDTH + 50 and -50 < screen_pos.y < SCREEN_HEIGHT + 50:
                offset = pygame.Vector2(enemy.sprite.get_width() / 2, enemy.sprite.get_height() / 2)
                screen.blit(enemy.sprite, screen_pos - offset)
        
        # Draw player
        player_screen_pos = world_to_screen(player.pos, camera_pos)
        rotated = pygame.transform.rotate(player.sprite, -math.degrees(math.atan2(mouse_pos.y - player_screen_pos.y, mouse_pos.x - player_screen_pos.x)))
        offset = pygame.Vector2(rotated.get_width() / 2, rotated.get_height() / 2)
        screen.blit(rotated, player_screen_pos - offset)
        
        # Draw bullets
        for bullet in bullets:
            screen_pos = world_to_screen(bullet.pos, camera_pos)
            if -50 < screen_pos.x < SCREEN_WIDTH + 50 and -50 < screen_pos.y < SCREEN_HEIGHT + 50:
                offset = pygame.Vector2(bullet.radius, bullet.radius)
                screen.blit(bullet_sprite, screen_pos - offset)
        
        draw_ui(screen, player, wave, player.health, len(enemies), camera_pos)
    elif game_state == 'GAME_OVER':
        draw_center_overlay(screen, "GAME OVER", "Press R to restart or ESC to quit")
        score_label = font_small.render(f"Final Score: {player.score}", True, COLOR_TEXT)
        screen.blit(score_label, ((SCREEN_WIDTH - score_label.get_width()) / 2, SCREEN_HEIGHT * 0.42))

    pygame.display.flip()

pygame.quit()