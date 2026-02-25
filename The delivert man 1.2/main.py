import pygame
from sprites import *
from config import *
from data import *
import sys

class Map:
    def __init__(self, name, data):
        self.name = name
        self.map_pic = pygame.image.load(data["map"]).convert()
        self.collision_map = data["collision"]
        self.exits = data.get("exits", {})
        self.dialogs = data.get("dialog", [])
        self.cutscenes = data.get("cutscenes", {})

class Camera:
    def __init__(self, map_width, map_height, zoom=1.75):
        self.offset = pygame.Vector2(0, 0)
        self.zoom = zoom
        self.map_width = map_width
        self.map_height = map_height


    def update(self, target):
        self.offset.x = max(0, min(target.rect.centerx - WIN_WIDTH / (2 * self.zoom), 
                                   self.map_width - WIN_WIDTH / self.zoom))
        self.offset.y = max(0, min(target.rect.centery - WIN_HEIGHT / (2 * self.zoom), 
                                   self.map_height - WIN_HEIGHT / self.zoom))
        
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("The Delivery Man")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(font, 24)
        self.running = True

        #maps
        self.maps = {}
        self.current_map = None
        self.spawn_x = None
        self.spawn_y = None
        self.player = None

        #character
        self.character_spritesheet = Spritesheet(
            "game graphics/sprites/mc_sprite.png")
        
        #intro screen
        self.intro_background = pygame.image.load(
            "game graphics/maps/START.png")
        
        # Systems
        self.fade_surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
        self.fade_surface.fill(BLACK)
        self.fade_alpha = 0
        self.fading = False
        self.scene_changing = False
        self.change_requested = False
        self.target_exit = None
        self.map_cooldown = 0
        self.show_dialog = False
        self.cutscene_active = False
        self.current_cutscene = None
        self.cutscene_starting = False
        self.cutscene_fade_speed = 8
        self.day_changing = False
        self.next_day_index = None
        self.camera = None
        self.cutscene_end_id = None
        self.interact_locked = False
        self.current_cutscene_key = None
        self.show_dialog = False
        self.dialogs_id = None

    def createtilemap(self):
        if not self.current_map: return
        
        for i, row in enumerate(self.current_map.collision_map):
            for j, column in enumerate(row):
                if column == '1': Blocked_Block(self, j, i)
                if column == 'A': interact_blocks(self, j, i, cutscene_key="HouseA")
                if column == 'C': interact_blocks(self, j, i, cutscene_key="HouseC")
                if column == '7': Dialog_Block(self, j, i, dialog_id=0)
                if column == 'B': Dialog_Block(self, j, i, dialog_id=1)
                if column == 'g': interact_blocks(self, j, i, cutscene_key="End")
                if column == 'a': ChangeMap_Block(self, j, i, 'a')
                if column == 'b': ChangeMap_Block(self, j, i, 'b')
                if column == 'c': ChangeMap_Block(self, j, i, 'c')
                if column == 'd': ChangeMap_Block(self, j, i, 'd')
                if column == 'e': ChangeMap_Block(self, j, i, 'e')
                if column == 'f': ChangeMap_Block(self, j, i, 'f')
                if column == 'D': interact_blocks(self, j, i, cutscene_key="HouseD")
                if column == 'E': Dialog_Block(self, j, i, dialog_id=0)
                if column == 'F': Dialog_Block(self, j, i, dialog_id=1)
                if column == 'G': interact_blocks(self, j, i, cutscene_key="HouseG")
                if column == 'H': interact_blocks(self, j, i, cutscene_key="HouseH")
                if column == 'I': interact_blocks(self, j, i, cutscene_key="HouseI")
                if column == 'J': interact_blocks(self, j, i, cutscene_key="HouseJ")
                if column == '8': Dialog_Block(self, j, i, dialog_id=0)

    def next_scene(self):
        if not self.target_exit: return
        
        exit_data = self.current_map.exits.get(self.target_exit)
        if exit_data:
            self.current_map = self.maps[exit_data["target_map"]]
            new_pos = exit_data["spawn_at"]

            self.dialogs = self.current_map.dialogs

            self.load_cutscenes()             
            self.all_sprites.empty()
            self.blocks.empty()
            self.interact_block.empty()
            self.dialog_block.empty()
            self.changemap_block.empty()            
            self.createtilemap()

            self.player.rect.topleft = (new_pos[0] * TILESIZE, new_pos[1] * TILESIZE)
            self.all_sprites.add(self.player)
            self.camera.map_width = self.current_map.map_pic.get_width()
            self.camera.map_height = self.current_map.map_pic.get_height()

        else: return

    def update(self):
        if self.map_cooldown > 0: self.map_cooldown -= 1
        if not self.cutscene_active:
            self.all_sprites.update()

            if self.camera and self.player:
                self.camera.update(self.player)

                # prevent player from getting out of the map
                self.player.rect.left = max(0, self.player.rect.left)
                self.player.rect.top = max(0, self.player.rect.top)

                self.player.rect.right = min(
                    self.current_map.map_pic.get_width(),
                    self.player.rect.right
                )
                self.player.rect.bottom = min(
                    self.current_map.map_pic.get_height(),
                    self.player.rect.bottom
                )

        if self.change_requested and not self.scene_changing:
            self.change_requested = False
            self.scene_changing = True
            self.start_fade("out", 15)

        if self.fading:
            self.update_fade()

        if self.cutscene_active and self.current_cutscene is None:
            self.cutscene_active = False

    def update_fade(self):
        if self.fade_direction == "out":
            self.fade_alpha += self.fade_speed

            if self.fade_alpha >= 255:
                self.fade_alpha = 255
                self.fading = False

            # if day changing
            if self.day_changing:
                self.day_changing = False

                self.load_day(self.next_day_index)
                self.new()

                # start each day intro cutscene
                if (
                    self.current_map and
                    self.current_map.cutscenes and
                    "intro_cutscene" in self.current_map.cutscenes
                ):
                    print("Starting intro cutscene")
                    self.start_cutscene("intro_cutscene")
                    return
                
                if self.day == 5:
                    self.start_fade("in", 2)
                else:
                    self.start_fade("in", 15)

                # if starting cutscene
            elif self.cutscene_starting:
                self.cutscene_starting = False
                self.cutscene_active = True
                self.start_fade("in", self.cutscene_fade_speed)

            elif self.scene_changing:
                self.next_scene()
                self.scene_changing = False
                self.start_fade("in", self.cutscene_fade_speed)
        else:
            self.fade_alpha -= self.fade_speed
            if self.fade_alpha <= 0:
                self.fade_alpha = 0
                self.fading = False

    def dialog_popup(self, dialog_id):
        dialog_surface = pygame.Surface((640, 150))
        dialog_surface.fill((255, 255, 255))
        dialog_rect = dialog_surface.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT - 120))

        if self.dialogs and 0 <= dialog_id < len(self.dialogs):
            dialog_string = self.dialogs[dialog_id]
        else:
            dialog_string = "..."

        # make \n available
        lines = dialog_string.split("\n")

        line_height = self.font.get_height()
        total_text_height = line_height * len(lines)
        start_y = (dialog_surface.get_height() - total_text_height) // 2

        for i, line in enumerate(lines):
            text_surface = self.font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(centerx=dialog_surface.get_width() // 2)
            text_rect.y = start_y + i * line_height
            dialog_surface.blit(text_surface, text_rect)

        self.screen.blit(dialog_surface, dialog_rect)

    def draw(self):
        self.screen.fill(BLACK)

        if self.cutscene_active and self.current_cutscene in self.cutscene_images:
            self.screen.blit(self.cutscene_images[self.current_cutscene], (0, 0))
        else:
            if not self.current_map or not self.camera:
                pygame.display.update()
                return

            cam_surf = pygame.Surface(
                (WIN_WIDTH / self.camera.zoom,
                WIN_HEIGHT / self.camera.zoom)
            )

            cam_surf.blit(self.current_map.map_pic, -self.camera.offset)

            for sprite in self.all_sprites:
                cam_surf.blit(sprite.image,
                          sprite.rect.topleft - self.camera.offset)

            self.screen.blit(
                pygame.transform.scale(cam_surf, (WIN_WIDTH, WIN_HEIGHT)),
                (0, 0)
            )

        # draw fade
        if self.fading:
            self.fade_surface.set_alpha(self.fade_alpha)
            self.screen.blit(self.fade_surface, (0,0))

        if self.show_dialog and self.dialogs_id is not None:
            self.dialog_popup(self.dialogs_id)

        pygame.display.update()

    def start_fade(self, dir, speed=10):
        self.fade_direction = dir
        self.fade_speed = speed
        self.fading = True
        self.fade_alpha = 255 if dir == "in" else 0

    # start cutscene
    def start_cutscene(self, cutscene_key):

        group = self.current_map.cutscenes.get(cutscene_key)
        if not group: return

        self.current_cutscene_key = cutscene_key
        self.cutscene_images = {}

        for cid, path in sorted(group.items()):
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (WIN_WIDTH, WIN_HEIGHT))
            self.cutscene_images[cid] = img

        self.current_cutscene = min(self.cutscene_images.keys())
        self.cutscene_end_id = max(self.cutscene_images.keys())

        self.cutscene_active = False
        self.cutscene_starting = True
        self.start_fade("out", 10)

    def load_cutscenes(self):
        self.cutscene_images = {}

        if not self.current_map: return

        if not self.current_map.cutscenes: return

        for key, value in self.current_map.cutscenes.items():
            if isinstance(value, dict):
                for cid, path in value.items():
                    image = pygame.image.load(path).convert_alpha()
                    image = pygame.transform.scale(image, (WIN_WIDTH, WIN_HEIGHT))
                    self.cutscene_images[cid] = image
            else:
                image = pygame.image.load(value).convert_alpha()
                image = pygame.transform.scale(image, (WIN_WIDTH, WIN_HEIGHT))
                self.cutscene_images[key] = image

    def new(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.Group()
        self.interact_block = pygame.sprite.Group()
        self.dialog_block = pygame.sprite.Group()
        self.changemap_block = pygame.sprite.Group()

        # if no map, no tile map
        if not self.current_map:
            self.player = None
            return

        if self.spawn_x is not None and self.spawn_y is not None:
            self.player = Player(self, self.spawn_x, self.spawn_y)
            self.all_sprites.add(self.player)   
        else:
            self.player = None

        self.createtilemap()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def events(self):
        colliding_dialog = None
        colliding_interact = None

        # ถ้าไม่ชน interact แล้ว → ปลดล็อค
        if not colliding_interact:
            self.interact_locked = False

        # เช็คชน dialog ก่อน
        for dialog in self.dialog_block:
            if dialog.rect.colliderect(self.player.rect):
                colliding_dialog = dialog
                break

        # เช็คชน interact block
        for block in self.interact_block:
            if block.rect.colliderect(self.player.rect):
                colliding_interact = block
                break

        # Day 5 auto trigger End cutscene
        if (
            self.day == 5 and
            colliding_interact and
            colliding_interact.cutscene_key == "End" and
            not self.cutscene_active
        ):
            self.start_cutscene("End")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:

                    # cutscene mode
                    if self.cutscene_active and self.current_cutscene is not None:
                        print("current:", self.current_cutscene, "end:", self.cutscene_end_id)

                        if (self.cutscene_end_id is not None and 
                            self.current_cutscene < self.cutscene_end_id):
                            self.current_cutscene += 1
                        else:
                            self.cutscene_active = False
                            self.current_cutscene = None

                            # if intro cutscenes
                            if self.current_cutscene_key == "intro_cutscene":
                                self.start_fade("out", 10)
                                self.scene_changing = True
                                return

                            # day 5 End cutscene
                            if self.current_cutscene_key == "End":
                                print("Game Finished! Returning to Intro Screen...")
                                self.playing = False
                                return

                            # House J
                            if self.day == 4 and self.current_cutscene_key == "HouseJ":
                                next_day = game_data.get(self.day, {}).get("next_day")
                                if next_day:
                                    print("HouseJ finished → moving to Day", next_day)
                                    self.change_day(next_day)

                            # if cutscene-only day
                            day_config = game_data.get(self.day, {})

                            if "maps" not in day_config:
                                next_day_num = day_config.get("next_day")
                                if next_day_num:
                                    print("Changing to day:", day_config["next_day"])
                                    self.change_day(day_config["next_day"])
                                    
                    # dialog mode
                    elif colliding_dialog:

                        if not self.show_dialog:
                            self.dialogs_id = colliding_dialog.dialog_id
                            self.show_dialog = True

                        else:
                            if self.dialogs_id == 1:
                                found_exit = False

                                # using exit
                                for block in self.changemap_block:
                                    if block.rect.colliderect(self.player.rect):
                                        self.target_exit = block.exit_type
                                        self.change_requested = True
                                        found_exit = True
                                        print("TARGET EXIT:", self.target_exit)
                                        break
                                if not found_exit:
                                    next_day_num = game_data.get(self.day, {}).get("next_day")
                                    if next_day_num:
                                        print(f"Ending Day {self.day}, moving to Day {next_day_num}")
                                        self.change_day(next_day_num)

                            self.show_dialog = False

                    # start cutscene
                    elif colliding_interact:
                        self.start_cutscene(colliding_interact.cutscene_key)
                    else:
                        self.show_dialog = False
                
    # intro screen            
    def intro_screen(self):
        intro = True
        play_button = Button(WIN_WIDTH//2 - 50, WIN_HEIGHT//2 + 40, 
                             100, 40, None, None, "", 32)
        help_button = Button(WIN_WIDTH - 110, 20,
                         100, 30, BLACK, WHITE, "How to play", 18)
        
        self.playing = False
        show_instructions = False
        instructions = [
            "How to play",
            "WASD / Arrows - Walking",
            "E  -  Interact",
            "Click Play to start"
        ]

        self.fade_alpha = 255
        self.fade_direction = "in"
        self.fade_speed = 5
        self.fading = True

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            # press help
            if help_button.is_pressed(mouse_pos, mouse_pressed):
                show_instructions = True
            # press play
            if not show_instructions:    
                if play_button.is_pressed(mouse_pos, mouse_pressed):
                    self.start_fade("out")
                    self.fade_speed = 3
                    intro = False
                    self.start_fade("in")
                    self.fade_speed = 3

            # draw buttons on screen
            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(help_button.image, help_button.rect)

            # show instructions box
            if show_instructions:
                overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
                overlay.set_alpha(180)
                overlay.fill((0, 0, 0))
                self.screen.blit(overlay, (0, 0))
                box_width = 400
                box_height = 250
                box_surface = pygame.Surface((box_width, box_height))
                box_surface.fill((255, 255, 255))
                box_rect = box_surface.get_rect(center=(WIN_WIDTH//2, WIN_HEIGHT//2))
                self.screen.blit(box_surface, box_rect)
                line_height = self.font.get_height()
                start_y = box_rect.y + 40

                for i, line in enumerate(instructions):
                    text_surface = self.font.render(line, True, (0, 0, 0))
                    text_rect = text_surface.get_rect(centerx=WIN_WIDTH//2)
                    text_rect.y = start_y + i * (line_height + 10)
                    self.screen.blit(text_surface, text_rect)

                # close button
                close_button = Button(
                    box_rect.right - 100,
                    box_rect.top + 20,
                    30, 30,
                    BLACK, WHITE,
                    "X", 20
                )

                self.screen.blit(close_button.image, close_button.rect)

                if close_button.is_pressed(mouse_pos, mouse_pressed):
                    show_instructions = False

            # fading on intro
            if self.fading:
                self.update_fade()
                self.fade_surface.set_alpha(self.fade_alpha)
                self.screen.blit(self.fade_surface, (0, 0))

            self.clock.tick(FPS)
            pygame.display.update()

    def change_day(self, next_day):
        self.day_changing = True
        self.next_day_index = next_day

        if next_day == 5:
            self.start_fade("out", 2)
        else:
            self.start_fade("out", 10)

    def load_day(self, day_number):

        print("Loading day:", day_number)

        # reset basic state
        self.day = day_number
        day_config = game_data.get(day_number, {})

        self.maps = {}
        self.cutscene_images = {}
        self.cutscene_active = False
        self.cutscene_starting = False
        self.show_dialog = False
        self.current_cutscene = None
        self.current_map = None
        self.day_changing = False
        self.cutscene_end_id = None
        self.dialogs = []
        self.current_cutscene_key = None

        # cutscene-only day
        if "maps" not in day_config:
            self.cutscene_images = {}
            cutscenes_data = day_config.get("cutscenes", {})
            
            # loading
            for cid, path in cutscenes_data.items():
                if isinstance(path, str):
                    img = pygame.image.load(path).convert_alpha()
                    img = pygame.transform.scale(img, (WIN_WIDTH, WIN_HEIGHT))
                    self.cutscene_images[cid] = img
                elif isinstance(path, dict):
                    for sub_id, sub_path in path.items():
                        img = pygame.image.load(sub_path).convert_alpha()
                        img = pygame.transform.scale(img, (WIN_WIDTH, WIN_HEIGHT))
                        self.cutscene_images[sub_id] = img

            if self.cutscene_images:
                self.current_cutscene = min(self.cutscene_images.keys())
                self.cutscene_end_id = max(self.cutscene_images.keys())
                self.cutscene_active = True
                print(f"Day {day_number} Cutscene Loaded: {len(self.cutscene_images)} frames")
            
            return

        # gameplay day
        for map_name, map_data in day_config["maps"].items():
            self.maps[map_name] = Map(map_name, map_data)

        first_map_key = day_config.get("first_map")
        if not first_map_key or first_map_key not in self.maps:
            return
        self.current_map = self.maps[first_map_key]

        # spawn player
        spawn = day_config["maps"][first_map_key].get("first_spawn")
        if spawn:
            self.spawn_x, self.spawn_y = spawn

        # load dialog
        self.dialogs = self.current_map.dialogs

        # auto intro
        if "intro_cutscene" in self.current_map.cutscenes:
            self.start_cutscene("intro_cutscene")

        # create camera only if map exists
        self.camera = Camera(
            self.current_map.map_pic.get_width(),
            self.current_map.map_pic.get_height()
        )

        # load dialogs
        self.dialogs = self.current_map.dialogs


g = Game()
while g.running:
    g.intro_screen()
    
    if g.running:
        g.load_day(1)
        g.new()
        g.main()

pygame.quit()
sys.exit()
