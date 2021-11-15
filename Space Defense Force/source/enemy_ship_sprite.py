from constants import *
import arcade
import math
import bullet

from pyglet.input import Joystick


class EnemyShipSprite(arcade.Sprite):
    """ Sprite that represents the enemy """
    def __init__(self, image_file_name, scale, delta_time, time_between_firing, bullet_list):
        super.__init__(image_file_name, scale=scale)
        self.size = 0
    
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
        
                  
    def update(self, delta_time, time_between_firing, bullet_list):
        
        self.frame_count += 1
        
        # Track time since last fired
        self.time_since_last_firing += delta_time
        
        # If we are past the firing time, then fire
        if self.time_since_last_firing >= self.time_between_firing:
            
            # Reset timer
            self.time_since_last_firing = 0
            
            # Fire the bullet
            bullet_sprite = GlowImageSprite(":resources:images/space_shooter/laserBlue01.png",
                                            SCALE,
                                            glowcolor=arcade.color.WHITE,
                                            shadertoy=self.glowball_shadertoy,
                                            player_no=0)
            self.set_bullet_vector(bullet_sprite, 13, self.player_sprite_list[0])
            arcade.play_sound(self.laser_sound)
            bullet.center_x = self.center_x
            bullet.angle = -90
            bullet.top = self.bottom
            bullet.change_y = -2
            self.bullet_list.append(bullet)
            
        # Loop through each enemy we have
        for enemy_ship_sprite in self.enemy_ship_sprite_list:
            # Have a random 1 in 200 chance of shooting each 1/60th of a second
            odds = 200
            
            # Adjust odds based on delta-time
            adj_odds = int(odds * (1 / 60) / delta_time)
            
            if random.randrange(adj_odds) == 0:
                bullet = Bullet
                bullet.center_x = enemy.center_x
                bullet.angle = -90
                bullet.top = enemy.bottom
                bullet.change_y = - 2
                self.bullet_list.append(bullet)
                
        # Get rid of the bullet when it flies off-screen
        for bullet in self.bullet_list:
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()
                
        self.bullet_list.update()
        # Add it to the enemies list
        self.enemy_ship_sprite_list.append(enemy_ship_sprite)
        self.all_sprites.append(enemy_ship_sprite)