import arcade

"""
Class: Snake
Description: stores information and methods for a SpriteList representing a
    snake and information such as the snake's size and speed. The snake's 
    movement is based on it's speed in the x- and y-directions.
Class Variables:
    snake_list: arcade SpriteList for pieces of the snake.
    num_segments: the number of body segments in the snake.
    speed: the speed the snake can travel in either x- or y-directions.
    x_speed: speed of the snake's head in x-direction.
    y_speed: speed of the snake's head in y-direction.
    head_directions: list of arcade textures for snake's head pointing in 
        different directions.
    snake_head: the Sprite in the snake_list that is the snake's head.
"""
class Snake():
    """
    Function: init
    Description: Initializes class variables and creates the Sprites that
        compose the Snake.
    Parameters:
        x_start: x-coordinate for placement of the first Sprite in the snake
        y_start: y-coordinate for placement of the first Sprite in the snake
        segments: number of body segments to create in the snake
    """
    def __init__(self, x_start, y_start, segments):
        
        # SpriteList for Sprites comprising the snake
        self.snake_list = arcade.SpriteList()

        # set class variables
        self.num_segments = segments
        self.speed = 10
        # snake starts movement in x-direction
        self.x_speed = self.speed
        self.y_speed = 0
        
        # load textures for snake head directions
        self.head_directions = [arcade.load_texture('images\snake_images\snake_head_horz.png', width=self.speed, height=self.speed),
                                arcade.load_texture('images\snake_images\snake_head_horz.png', flipped_horizontally=True, width=self.speed, height=self.speed),
                                arcade.load_texture('images\snake_images\snake_head_vert.png', width=self.speed, height=self.speed),
                                arcade.load_texture('images\snake_images\snake_head_vert.png', flipped_vertically=True, width=self.speed, height=self.speed)]

        # create sprite for snake head and add to snake_list
        self.snake_head = arcade.Sprite(image_height=self.speed,
                                   image_width=self.speed,
                                   center_x=x_start,
                                   center_y=y_start,
                                   hit_box_algorithm='Simple'
        )
        # add snake head textures to snake_head Sprite
        for texture in self.head_directions:
            self.snake_head.append_texture(texture)
        
        # set starting texture and add snake_head to SpriteList
        self.snake_head.set_texture(0)
        self.snake_list.append(self.snake_head)
        
        # update starting x-coordinate for next Sprite
        x_start -= self.speed

        # create sprites for snake body segments and add to snake_list
        # head is first element in list, then each segment is appended to it
        for i in range(0, self.num_segments - 1):
            segment = arcade.Sprite(filename='images\snake_images\snake_segment.png', 
                                        image_height=self.speed,
                                        image_width=self.speed,
                                        center_x=x_start,
                                        center_y=y_start,
                                        hit_box_algorithm='Simple'
            )
            self.snake_list.append(segment)
            x_start -= self.speed

        # set x,y direction for each segment
        for seg in self.snake_list:
            seg.change_x = self.x_speed
            seg.change_y = self.y_speed
    
    """
    Function: update
    Description: Updates the position and direction of movement for each
        Sprite comprising the snake.
    """
    def update(self):
        # loop through snake_list Sprites backwards. 
        for i in range(len(self.snake_list) - 1, 0, -1):
            # Make the Sprite's speed in each direction (change_x and change_y) 
            # equal to the speed of the segment one index closer to the head.
            self.snake_list[i].change_x = self.snake_list[i - 1].change_x
            self.snake_list[i].change_y = self.snake_list[i - 1].change_y
            # Update the position of the Sprite based on its speed in each direction
            self.snake_list[i].center_x += self.snake_list[i].change_x
            self.snake_list[i].center_y += self.snake_list[i].change_y
            
        # update snake_head sprite's speed in each direction
        self.snake_list[0].change_x = self.x_speed
        self.snake_list[0].change_y = self.y_speed
        # Update position of snake_head based on its speed in each direction
        self.snake_list[0].center_x += self.snake_list[0].change_x
        self.snake_list[0].center_y += self.snake_list[0].change_y

        # update texture for snake_head sprite based on direction of travel
        if self.x_speed > 0:
            self.snake_list[0].set_texture(0)
        elif self.x_speed < 0:
            self.snake_list[0].set_texture(1)
        elif self.y_speed > 0:
            self.snake_list[0].set_texture(2)
        elif self.y_speed < 0:
            self.snake_list[0].set_texture(3)

    """
    Function: grow
    Description: Adds a body segment Sprite to the end of the  SpriteList
    """
    def grow(self):
        # create new segment sprite
        new_segment = arcade.Sprite(filename='images\snake_images\snake_segment.png',
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

    """
    Function: draw
    Description: Draws all sprites in the snake_list SpriteList
    """
    def draw(self):
        self.snake_list.draw()
