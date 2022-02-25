import arcade

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800

"""
This class describes a snake sprite. The snake is a SpriteList of sprites
that move along the screen in response to user input.
"""
class Snake():
    def __init__(self, x_start, y_start, segments):
        """
        Class Initializer
        """
        # list of all sprites composing the snake
        self.snake_list = arcade.SpriteList()

        self.num_segments = segments
        self.speed = 10
        self.x_speed = self.speed
        self.y_speed = 0
        
        # load textures for different snake head directions
        self.head_directions = [arcade.load_texture('snake_images\snake_head_horz.png', width=self.speed, height=self.speed),
                                arcade.load_texture('snake_images\snake_head_horz.png', flipped_horizontally=True, width=self.speed, height=self.speed),
                                arcade.load_texture('snake_images\snake_head_vert.png', width=self.speed, height=self.speed),
                                arcade.load_texture('snake_images\snake_head_vert.png', flipped_vertically=True, width=self.speed, height=self.speed)
        ]

        # Ryan - instantiated snake_head
        # create sprite for snake head and add to snake_list
        self.snake_head = arcade.Sprite(image_height=self.speed,
                                   image_width=self.speed,
                                   center_x=x_start,
                                   center_y=y_start,
                                   hit_box_algorithm='Simple'
        )
        # add textures to snake_head
        for texture in self.head_directions:
            # Ryan - instantiated snake_head
            self.snake_head.append_texture(texture)
        # Ryan - instantiated snake_head
        self.snake_head.set_texture(0)
        # Ryan - instantiated snake_head
        self.snake_list.append(self.snake_head)
        x_start -= self.speed

        # create sprites for snake body segments and add to snake_list
        # head is first element in list, then each segment is appended to ti
        for i in range(0, self.num_segments - 1):
            segment = arcade.Sprite(filename='snake_images\snake_segment.png', 
                                        image_height=self.speed,
                                        image_width=self.speed,
                                        center_x=x_start,
                                        center_y=y_start,
                                        hit_box_algorithm='Simple'
            )
            self.snake_list.append(segment)
            x_start -= self.speed

        # set direction for each segment
        for seg in self.snake_list:
            seg.change_x = self.x_speed
            seg.change_y = self.y_speed
    
    def update(self):
        """
        Update the position of the snake sprite and handle interacting with the game border
        """

        # loop through snake sprites backwards. Make the speed in each direction 
        # (change_x and change_y) equal to the speed of the segment one index 
        # closer to the head. Then add speed in each direction to the position
        for i in range(len(self.snake_list) - 1, 0, -1):
            self.snake_list[i].change_x = self.snake_list[i - 1].change_x
            self.snake_list[i].change_y = self.snake_list[i - 1].change_y
            self.snake_list[i].center_x += self.snake_list[i].change_x
            self.snake_list[i].center_y += self.snake_list[i].change_y
            
        # update the snake head sprite's speed in each direction then update
        # its position
        self.snake_list[0].change_x = self.x_speed
        self.snake_list[0].change_y = self.y_speed
        self.snake_list[0].center_x += self.snake_list[0].change_x
        self.snake_list[0].center_y += self.snake_list[0].change_y

        # orient snake head sprite based on direction of travel
        if self.x_speed > 0:
            self.snake_list[0].set_texture(0)
        elif self.x_speed < 0:
            self.snake_list[0].set_texture(1)
        elif self.y_speed > 0:
            self.snake_list[0].set_texture(2)
        elif self.y_speed < 0:
            self.snake_list[0].set_texture(3)

        # check if reached edge of screen and force to turn around
        if self.snake_list[0].center_x >= SCREEN_WIDTH or self.snake_list[0].center_x <= 0:
            self.x_speed *= -1
        if self.snake_list[0].center_y >= SCREEN_HEIGHT or self.snake_list[0].center_y <= 0:
            self.y_speed *= -1

    def grow(self):
        """"
        Add a body segment to the end of the snake
        """
        
        # create new segment sprite
        new_segment = arcade.Sprite(filename='snake_images\snake_segment.png',
                                image_height=self.speed,
                                image_width=self.speed,
                                center_x=0,
                                center_y=0,
                                hit_box_algorithm='Simple'
        )
        # set new last segment's speed to same as old last segment's speed
        new_segment.change_x = self.snake_list[-1].change_x
        new_segment.change_y = self.snake_list[-1].change_y
        
        # set new segment position based on speed and position of old last segment
        if self.snake_list[-1].change_x > 0:
            new_segment.center_x = self.snake_list[-1].center_x - self.speed
            new_segment.center_y = self.snake_list[-1].center_y
        elif self.snake_list[-1].change_x < 0:
            new_segment.center_x = self.snake_list[-1].center_x + self.speed
            new_segment.center_y = self.snake_list[-1].center_y
        elif self.snake_list[-1].change_y > 0:
            new_segment.center_x = self.snake_list[-1].center_x
            new_segment.center_y = self.snake_list[-1].center_y - self.speed
        elif self.snake_list[-1].change_y < 0:
            new_segment.center_x = self.snake_list[-1].center_x
            new_segment.center_y = self.snake_list[-1].center_y + self.speed
        
        # add new segment to the sprite list
        self.snake_list.append(new_segment)
        self.num_segments += 1

    def draw(self):
        """
        Draw the sprites in the snake SpriteList
        """
        self.snake_list.draw()
