""" This is only a template build to be used for enemy sprites for space shooters. Highly recommend that
	you have a complete updated version of arcade for Python, and that you have files downloaded 
	from https://kenney.nl/assets?q=2d
    mostly the space shooter assets. I will try to include them in the package of the game,
	can't make any promises."""

import arcade
import math

from constants import *

class EnemySprite(arcade.Sprite):
    """ Sprite that represents the enemy """
    def __init__(self, filename, scale, delta_time, time_between_firing)
    """ set up the enemy sprite """
    super().__init__(image_file scale)
    
    self.time_since_last_firing = 0.0
    
    self.time_between_firing = time_between_firing
    
    self.bullet_list = bullet_list
    
    def on_update(self, delta_time: float = 1 / 60):
        self.track_since_last_firing += delta_time
        if self.time_since_last_firing >= self.time_between_firing:
            self.time_since_last_firing = 0
            
            bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png")
            bullet.center_x = self.center_x
            bullet.angle = -90
            bullet.top = self.bottom
            bullet.change_y = -2
            self.bullet_list.append(bullet)
            
                
    def setup(self):
        # Add top-left enemy ship
        enemy = EnemySprite(":resources:images/spaceshooter/PNG/Enemies/enemyBlack1.png",
                            scale=0.5,
                            bullet_list=self.bullet_list,
                            time_between_firing=2.0)
        enemy.center_x = 120
        enemy.center_y = SCREEN_HEIGHT - screen_height
        enemy.angle = 180
        self.enemy_list.append(enemy)
        
        # Add top-right enemy ship
        enemy = EnemySprite(":resources:images/spaceshooter/PNG/Enemies/enemyBlack1.png",
                            scale=0.5,
                            bullet_list=self.bullet_list,
                            time_between_firing=1.0)
        enemy.center_x = -120
        enemy.center_y = SCREEN_HEIGHT - screen_height
        enemy.angle = 180
        self.enemy_list.append(enemy)
		
	""" use either on_update 1 or 2 to determine what the enemy is going to do. DO NOT attempt
        to use both conditions at the same time, until completely tested."""
        
    def on_update(self, delta_time):
        self.enemy_list.on_update(delta_time)
        
        """  1 Only used for random shooting from enemies """
        for enemy in self.enemy_list:
            # Have a random 1 in 200 change of shooting each 1/60th of a second
            odds = 200
            
            # Adjust odds based on delta-time
            adj_odds = int(odds * (1 / 60) / delta_time)
            
            if random.randrange(adj_odds) == 0:
                bullet = arcade.Sprite(":resources:images/spaceshooter/laserBlue01.png")
                bullet.center_x = enemy.center_x
                bullet.angle = -90
                bullet.top = enemy.bottom
                bullet.change_y = -2
                self.bullet_list.append(bullet)
                
        """  2 Only used for enemies that follow your ship """
        self.frame_count += 1
        
        # Loop through each enemy that we have
        for enemy in self.enemy_list:
            
            # First calculate the angle to the player. We could do this
            # only when the bullet fires, but in this case we will rotate
            # the enemy to face the player each frame, so we will do this
            # each frame.
            
            # Position the start at the enemies current location
            start_x = enemy.center_x
            start_y = enemy.center_y
            
            # Get the destination location for the bullet
            dest_x = self.player.center_x
            dest_y = self.player.center_y
            
            # Do the math to calculate how to get the bullet to the destination.
            # Calculate the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)
            
            # Set the enemy to face the player
            enemy.angle = math.degrees(angle)-90
            
            # Shoot every 60 frames change of shooting each frame
            if self.frame_count % 60 == 0:
                bullet = arcade.Sprite(":resources:images/spaceshooter/laserBlue01.png")
                bullet.center_x = start_x
                bullet.center_y = start_y
                
                # Angle the bullet sprite
                bullet.angle = math.degrees(angle)
                
                # Taking into account the angle, calculate our change_x
                # and change_y. Velocity is how fast the bullet travels.
                bullet.change_x = math.cos(angle) * BULLET_SPEED
                bullet.change_y = math.sin(angle) * BULLET_SPEED
                
                self.bullet_list.append(bullet)
                
        """ Use bottom to finish the build for the enemy sprite """
                
        # Get rid of the bullet when it flies off-screen
        for bullet in self.bullet_list:
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()
                
        self.bullet_list.update()