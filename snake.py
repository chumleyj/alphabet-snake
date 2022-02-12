import arcade

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800

"""
This class describes a snake sprite. The snake is a collection of sprites
that move along the screen in response to user input.
"""
class Snake():
    """Initializer"""
    def __init__(self, x_start, y_start, segments):
        """list of all sprites composing the snake"""
        self.snake_list = arcade.SpriteList()

        self.num_segments = segments
        self.speed = 10
        self.x_speed = self.speed
        self.y_speed = 0
        
        """load textures for different snake head directions"""
        self.head_directions = [arcade.load_texture('snake_head_horz.png', width=self.speed, height=self.speed),
                                arcade.load_texture('snake_head_horz.png', flipped_horizontally=True, width=self.speed, height=self.speed),
                                arcade.load_texture('snake_head_vert.png', width=self.speed, height=self.speed),
                                arcade.load_texture('snake_head_vert.png', flipped_vertically=True, width=self.speed, height=self.speed)
        ]

        """create sprite for snake head and add to snake_list"""
        snake_head = arcade.Sprite(image_height=self.speed,
                                   image_width=self.speed,
                                   center_x=x_start,
                                   center_y=y_start,
                                   hit_box_algorithm='Simple'
        )
        """add textures to snake_head"""
        for texture in self.head_directions:
            snake_head.append_texture(texture)
        snake_head.set_texture(0)
        self.snake_list.append(snake_head)
        x_start -= self.speed

        """create sprites for snake body segments and add to snake_list"""
        for i in range(0, self.num_segments - 1):
            segment = arcade.Sprite(filename='snake_segment.png', 
                                        image_height=self.speed,
                                        image_width=self.speed,
                                        center_x=x_start,
                                        center_y=y_start,
                                        hit_box_algorithm='Simple'
            )
            self.snake_list.append(segment)
            x_start -= self.speed

        """set direction for each segment"""
        for seg in self.snake_list:
            seg.change_x = self.x_speed
            seg.change_y = self.y_speed
    
    """update the position of the snake sprite"""
    def update(self):

        """update segment's direction then position"""
        for i in range(len(self.snake_list) - 1, 0, -1):
            self.snake_list[i].change_x = self.snake_list[i - 1].change_x
            self.snake_list[i].change_y = self.snake_list[i - 1].change_y
            self.snake_list[i].center_x += self.snake_list[i].change_x
            self.snake_list[i].center_y += self.snake_list[i].change_y
            
        """update head's direction then position"""
        self.snake_list[0].change_x = self.x_speed
        self.snake_list[0].change_y = self.y_speed
        self.snake_list[0].center_x += self.snake_list[0].change_x
        self.snake_list[0].center_y += self.snake_list[0].change_y

        """orient head segment based on direction"""
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

    """"grow body by one segment"""
    def grow(self):
        """create new segment sprite"""
        new_segment = arcade.Sprite(filename='snake_segment.png',
                                image_height=self.speed,
                                image_width=self.speed,
                                center_x=0,
                                center_y=0,
                                hit_box_algorithm='Simple'
        )
        """set new last segment direction to same as old last segment direction"""
        new_segment.change_x = self.snake_list[-1].change_x
        new_segment.change_y = self.snake_list[-1].change_y
        
        """set new segment position based on direction of old last segment"""
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
        
        self.snake_list.append(new_segment)
        self.num_segments += 1

    # draw the list of points that make up the TestSnake
    def draw(self):
        """Jeff - updated drawing for sprites"""
        self.snake_list.draw()