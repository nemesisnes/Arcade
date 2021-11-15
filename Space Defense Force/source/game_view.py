import random
import math
import arcade

from game_over_view import GameOverView
from typing import cast
from arcade.experimental.shadertoy import Shadertoy
from constants import *
from asteroid_sprite import AsteroidSprite
from ship_sprite import ShipSprite
from bullet import Bullet
from glow_line import GlowLine
from glow_ball import GlowBall
from explosion import ExplosionMaker
from glow_image_sprite import GlowImageSprite
from enemy_ship_sprite import EnemyShipSprite
from window import Window as window


class GameView(arcade.View):
    # Main application class
    def __init__(self):
        super().__init__()
        
        # Sprite lists
        self.player_sprite_list = arcade.SpriteList()
        self.asteroid_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.ship_life_list = arcade.SpriteList()
        self.enemy_ship_sprite_list = arcade.SpriteList()
        
        # Sounds
        self.laser_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound1 = arcade.load_sound(":resources:sounds/explosion1.wav")
        self.hit_sound2 = arcade.load_sound(":resources:sounds/explosion2.wav")
        self.hit_sound3 = arcade.load_sound(":resources:sounds/hit1.wav")
        self.hit_sound4 = arcade.load_sound(":resources:sounds/hit2.wav")
        self.glowball_shadertoy = Shadertoy.create_from_file(self.window.get_size(), "glow_ball.glsl")
        self.glowline_shadertoy = Shadertoy.create_from_file(self.window.get_size(), "glow_line.glsl")
        self.explosion_list = []

    def start_new_game(self, player_count):
        #Set up the game and initialize the variables
        self.game_over = False
        arcade.set_background_color(arcade.csscolor.BLACK)
        # Sprite lists
        self.player_sprite_list = arcade.SpriteList()
        self.asteroid_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.ship_life_list = arcade.SpriteList()
        self.enemy_ship_sprite_list = arcade.SpriteList()

        joystick = None
        player_sprite = ShipSprite(":resources:images/space_shooter/playerShip1_orange.png",
                                   SCALE,
                                   joystick,
                                   player_no=1,
                                   player_count=player_count)
        self.player_sprite_list.append(player_sprite)
        if player_count > 1:
            joystick = None

            player_sprite = ShipSprite(":resources:images/space_shooter/playerShip1_green.png",
                                       SCALE,
                                       joystick,
                                       player_no=2,
                                       player_count=player_count
                                       )
            self.player_sprite_list.append(player_sprite)
            
        # Set up the player
        for player in self.player_sprite_list:
            player.score = 0
            player.lives = 3
            
        # Set up the little icons that represent the player lives.
        cur_pos = 10
        for i in range(self.player_sprite_list[0].lives):
            life = arcade.Sprite(":resources:images/space_shooter/playerLife1_orange.png", SCALE)
            life.center_x = cur_pos + life.width
            life.center_y = life.height
            cur_pos += life.width
            self.ship_life_list.append(life)
        if len(self.player_sprite_list) > 1:
            cur_pos = 100
            for i in range(self.player_sprite_list[1].lives):
                life = arcade.Sprite(":resources:images/space_shooter/playerLife1_green.png", SCALE)
                life.center_x = cur_pos + life.width
                life.center_y = life.height
                cur_pos += life.width
                self.ship_life_list.append(life)
                                
        # Make the asteroids
        image_list = (":resources:images/space_shooter/meteorGrey_big1.png",
                      ":resources:images/space_shooter/meteorGrey_big2.png",
                      ":resources:images/space_shooter/meteorGrey_big3.png",
                      ":resources:images/space_shooter/meteorGrey_big4.png")
        for i in range(STARTING_ASTEROID_COUNT):
            image_no = random.randrange(4)
            enemy_sprite = AsteroidSprite(image_list[image_no], SCALE)
            enemy_sprite.guid = "Asteroid"
            enemy_sprite.center_y = random.randrange(BOTTOM_LIMIT, TOP_LIMIT)
            enemy_sprite.center_x = random.randrange(LEFT_LIMIT, RIGHT_LIMIT)
            enemy_sprite.change_x = random.random() * 2 - 1
            enemy_sprite.change_y = random.random() * 2 - 1
            enemy_sprite.change_angle = (random.random() - 0.5) * 2
            enemy_sprite.size = 4
            self.asteroid_list.append(enemy_sprite)
            
        # Make the enemies   
    def spawn_enemy_ship_sprite(EnemyShipSprite):
            # Spawn a new enemy every 0.25 seconds
            arcade.schedule(self.add_enemy_ship_sprite, 0.25)
        
    def add_enemy_ship_sprite(self, delta_time: float):
            """ Adds a new enemy to the screen.
        
            Arguments:
                delta_time {float} -- How much time passed since the last call
            """
        
            # First, create the new enemy sprite
            enemy_ship_sprite = arcade.Sprite(":resources:images/space_shooter/enemyShipBlue1.png")
        
            # Set its position to a random height and off screen right
            enemy_ship_sprite.left = random.randint(self.width, self.width + 80)
            enemy_ship_sprite.top = random.randint(10, self.height, - 10)
        
            # Set its speed to a random speed heading left
            enemy_ship_sprite.velocity = (random.randint(-20, -5), 0)
        
            # Add it to the enemies list
            self.enemy_ship_sprite_list.append(enemy_ship_sprite)
            self.all_sprites.append(enemy_ship_sprite)
        
    def time_between_firing(self, bullet_list, time_between_firing):
            # tme between firing
            """ Enemy ship class that tracks how long it has been since firing """
            # How long has it been since we last fired?
            self.time_since_last_firing = 0.0
        
            # How often do we fire?
            self.time_between_firing = time_between_firing
        
            # When we fire, what list tracks the bullets?
            self.bullet_list = bullet_list
            
    def on_draw(self):
        # Render the screen.
        # This command has to happen before we start drawing
        arcade.start_render()
        
        # Draw all the sprites.
        self.asteroid_list.draw()
        self.ship_life_list.draw()
        for bullet in self.bullet_list:
            bullet.draw()
        self.bullet_list.draw()
        for explosion in self.explosion_list:
            explosion.render()
        self.player_sprite_list.draw()
        self.enemy_ship_sprite_list.draw()
        
        # Put the text on the screen.
        output = f"Player 1 Score: {self.player_sprite_list[0].score}"
        arcade.draw_text(output, 10, 40, arcade.color.AMBER,
                         font_size=15,
                         font_name="Arcade")
        if len(self.player_sprite_list) > 1:
            output = f"Player 2 Score: {self.player_sprite_list[1].score}"
            arcade.draw_text(output, 500, 40, arcade.color.AMBER,
                             font_size=15,
                             font_name="Arcade")
        output = f"Asteroid Count: {len(self.asteroid_list)}"
        arcade.draw_text(output, 10, 80, arcade.color.AMBER,
                         font_size=15,
                         font_name="Arcade")
        output = f"Enemy Ship Count: {len(self.enemy_ship_sprite_list)}"
        arcade.draw_text(output, 10, 60, arcade.color.AMBER,
                         font_size=15,
                         font_name="Arcade")
    
    def on_update(self, delta_time):
        # Call on update for each enemy in the list
        self.enemy_ship_sprite_list.on_update(delta_time)
        
        """ All the logic to move, and the game logic goes here """
        self.frame_count += 1
        
        # Loop through each enemy that we have
        for enemy_ship_sprite in self.enemy_ship_sprite_list:
            # Have a random 1 in 200 change in shooting each 1/60th of a second
            odds = 200
            
            # Adjust odds based on delta-time
            adj_odds = int(odds * (1 /60) / delta_time)
            
            if random.randrange(adj_odds) == 0:
                bullet = Bullet
                bullet.center_x = enemy_ship_sprite.center_x
                bullet.angle = -90
                bullet.top = enemy_ship_sprite.bottom
                bullet.change_y = -2
                self.bullet_list.append(bullet)
        
        # Get rid of the bullet when it flies off-screen
        for bullet in self.bullet_list:
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()
        
        self.bullet_list.update()
        
    def on_key_press(self, symbol, modifiers):
        # Shoot if the player hit the space bar and we aren't respawning.
        if symbol == arcade.key.LEFT:
            self.player_sprite_list[0].change_angle = 3
        elif symbol == arcade.key.RIGHT:
            self.player_sprite_list[0].change_angle = -3
        elif symbol == arcade.key.UP:
            self.player_sprite_list[0].thrust = 0.15
        elif symbol == arcade.key.DOWN:
            self.player_sprite_list[0].thrust = -.2
        elif symbol == arcade.key.KEY_1:
            color = (255, 128, 128)
            self.fire_circle(color, self.player_sprite_list[0], player_no=0)
        elif symbol == arcade.key.KEY_2:
            color = (128, 255, 128)
            self.fire_circle(color, self.player_sprite_list[0], player_no=0)
        elif symbol == arcade.key.KEY_3:
            color = (128, 128, 255)
            self.fire_circle(color, self.player_sprite_list[0], player_no=0)
        elif symbol == arcade.key.KEY_4:
            color = (255, 128, 255)
            self.fire_circle(color, self.player_sprite_list[0], player_no=0)
        elif symbol == arcade.key.KEY_5:
            color = (255, 255, 255)
            self.fire_line(color, self.player_sprite_list[0], player_no=0)
        elif symbol == arcade.key.KEY_6:
            color = (64, 255, 64)
            self.fire_line(color, self.player_sprite_list[0], player_no=0)
        elif symbol == arcade.key.KEY_7:
            bullet_sprite = GlowImageSprite(":resources:images/space_shooter/laserBlue01.png",
                                            SCALE,
                                            glowcolor=arcade.color.WHITE,
                                            shadertoy=self.glowball_shadertoy,
                                            player_no=0)
            self.set_bullet_vector(bullet_sprite, 13, self.player_sprite_list[0])
            arcade.play_sound(self.laser_sound)
            
    def fire_circle(self, bullet_color, player_sprite, player_no):
        bullet_sprite = GlowBall(glowcolor=bullet_color,
                                 radius=5,
                                 shadertoy=self.glowball_shadertoy,
                                 player_no=player_no)
        self.set_bullet_vector(bullet_sprite, 5, player_sprite)
        arcade.play_sound(self.laser_sound)
        
    def fire_line(self, bullet_color, player_sprite, player_no):
        bullet_sprite = GlowLine(glowcolor=bullet_color,
                                 shadertoy=self.glowline_shadertoy,
                                 player=player_sprite,
                                 player_no=player_no)
        self.set_bullet_vector(bullet_sprite, 13, player_sprite)
        arcade.play_sound(self.laser_sound)
        
    def set_bullet_vector(self, bullet_sprite, bullet_speed, player_sprite):
        bullet_sprite.change_y = \
            math.cos(math.radians(player_sprite.angle)) * bullet_speed
        bullet_sprite.change_x = \
            -math.sin(math.radians(player_sprite.angle)) \
            * bullet_speed
        bullet_sprite.center_x = player_sprite.center_x
        bullet_sprite.center_y = player_sprite.center_y
        self.bullet_list.append(bullet_sprite)
        
    def on_key_release(self, symbol, modifiers):
        # Called whenever a key is released
        if symbol == arcade.key.LEFT:
            self.player_sprite_list[0].change_angle = 0
        elif symbol == arcade.key.RIGHT:
            self.player_sprite_list[0].change_angle = 0
        elif symbol == arcade.key.UP:
            self.player_sprite_list[0].thrust = 0
        elif symbol == arcade.key.DOWN:
            self.player_sprite_list[0].thrust = 0
            
    def enemy_ship_sprite(self, enemy_ship_sprite, EnemyShipSprite):
        x = enemy_ship_sprite.center_x
        y = enemy_ship_sprite.center_y
        if enemy_ship_sprite.size == 4:
            for i in range(3):
                image_no = random.randrange(2)
                image_list = [":resources:images/space_shooter/enemyBlack1.png",
                              ":resources:images/space_shooter/enemyBlue1.png",
                              ":resources:images/space_shooter/enemyGreen1.png",
                              ":resources:images/space_shooter/enemyRed1.png"]
                enemy_ship_sprite = EnemyShipSprite(image_list[image_no],
                                              SCALE * 1.5)
                enemy_ship_sprite.center_y = y
                enemy_ship_sprite.center_x = x
                enemy_ship_sprite.change_x = random.random() * 2.5 - 1.25
                enemy_ship_sprite.change_y = random.random() * 2.5 - 1.25
                enemy_ship_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_ship_sprite.size = 4
                self.enemy_ship_sprite_list.append(enemy_ship_sprite)
                self.hit_sound4.play()
            
    def split_asteroid(self, asteroid: AsteroidSprite):
        # Split an asteroid into chunks
        x = asteroid.center_x
        y = asteroid.center_y
        if asteroid.size == 4:
            for i in range(3):
                image_no = random.randrange(2)
                image_list = [":resources:images/space_shooter/meteorGrey_med1.png",
                              ":resources:images/space_shooter/meteorGrey_med2.png"]
                enemy_sprite = AsteroidSprite(image_list[image_no],
                                              SCALE * 1.5)
                enemy_sprite.center_y = y
                enemy_sprite.center_x = x
                enemy_sprite.change_x = random.random() * 2.5 - 1.25
                enemy_sprite.change_y = random.random() * 2.5 - 1.25
                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = 3
                self.asteroid_list.append(enemy_sprite)
                self.hit_sound1.play()
        elif asteroid.size == 3:
            for i in range(3):
                image_no = random.randrange(2)
                image_list = [":resources:images/space_shooter/meteorGrey_small1.png",
                              ":resources:images/space_shooter/meteorGrey_small2.png"]
                enemy_sprite = AsteroidSprite(image_list[image_no],
                                              SCALE * 1.5)
                enemy_sprite.center_y = y
                enemy_sprite.center_x = x
                enemy_sprite.change_x = random.random() * 3 - 1.5
                enemy_sprite.change_y = random.random() * 3 - 1.5
                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = 2
                self.asteroid_list.append(enemy_sprite)
                self.hit_sound2.play()
        elif asteroid.size == 2:
            for i in range(3):
                image_no = random.randrange(2)
                image_list = [":resources:images/space_shooter/meteorGrey_tiny1.png",
                              ":resources:images/space_shooter/meteorGrey_tiny2.png"]
                enemy_sprite = AsteroidSprite(image_list[image_no],
                                              SCALE * 1.5)
                enemy_sprite.center_y = y
                enemy_sprite.center_x = x
                enemy_sprite.change_x = random.random() * 3.5 - 1.75
                enemy_sprite.change_y = random.random() * 3.5 - 1.75
                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = 1
                self.asteroid_list.append(enemy_sprite)
                self.hit_sound3.play()
        elif asteroid.size == 1:
            self.hit_sound4.play()
                       
    def on_update(self, x):
        # Move everything
        self.asteroid_list.update()
        self.bullet_list.update()
        self.player_sprite_list.update()
        self.enemy_ship_sprite_list.update()
        explosion_list_copy = self.explosion_list.copy()
        for explosion in explosion_list_copy:
            explosion.update(x)
            if explosion.time > .9:
                self.explosion_list.remove(explosion)
        for bullet in self.bullet_list:
            assert isinstance(bullet, Bullet)
            asteroids = arcade.check_for_collision_with_list(bullet, self.asteroid_list)
            if len(asteroids) > 0:
                explosion = ExplosionMaker(self.window.get_size(), bullet.position)
                self.explosion_list.append(explosion)
            for asteroid in asteroids:
                assert isinstance(asteroid, AsteroidSprite)
                self.player_sprite_list[bullet.player_no - 1].score += 1
                self.split_asteroid(cast(AsteroidSprite, asteroid))  # expected AsteroidSprite, got Sprite instead
                asteroid.remove_from_sprite_lists()
                bullet.remove_from_sprite_lists()
            enemy_ship_sprite = arcade.check_for_collision_with_list(bullet, self.enemy_ship_sprite_list)
            if len(enemy_ship_sprite) > 0:
                explosion = ExplosionMaker(self.window.get_size(), bullet.position)
                self.explosion_list.append(explosion)
            for enemy_ship_sprite in enemy_ship_sprite:
                assert isinstance(EnemyShipSprite, enemy_ship_sprite) # expected EnemyShipSprite, got sprite instead
                self.player_sprite_list[bullet.player_no, - 1].score += 1
                enemy_ship_sprite.remove_from_sprite_lists()
                bullet.remove_from_sprite_lists()
            
            # Remove bullet if it goes off-screen
            size = max(bullet.width, bullet.height)
            if bullet.center_x < 0 - size:
                bullet.remove_from_sprite_lists()
            if bullet.center_x > SCREEN_WIDTH + size:
                bullet.remove_from_sprite_lists()
            if bullet.center_y < 0 - size:
                bullet.remove_from_sprite_lists()
            if bullet.center_y > SCREEN_HEIGHT + size:
                bullet.remove_from_sprite_lists()
        for player in self.player_sprite_list:
            assert isinstance(player, ShipSprite)
            if not player.respawning:
                asteroids = arcade.check_for_collision_with_list(player, self.asteroid_list)
                if len(asteroids) > 0:
                    if player.lives > 0:
                        player.lives -= 1
                        player.respawn()
                        self.split_asteroid(cast(AsteroidSprite, asteroids[0]))
                        asteroids[0].remove_from_sprite_lists()
                        self.ship_life_list.pop().remove_from_sprite_lists()
                    else:
                        view = GameOverView()
                        self.window.show_view(view)

                enemy_ship_sprite = arcade.check_for_collision_with_list(player, self.enemy_ship_sprite_list)
                if len(enemy_ship_sprite) > 0:
                    if player.lives > 0:
                        player.lives -= 1
                        player.respawn()
                        self.enemy(cast(EnemyShipSprite, enemy_ship_sprite[0]))
                        enemy_ship_sprite[0].remove_from_sprite_lists()
                        self.ship_list.pop().remove_from_sprite_lists()
                    else:
                        view = GameOverView()
                        self.window.show_view(view)
