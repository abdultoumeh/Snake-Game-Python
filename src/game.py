import arcade
import random
import snake
import apples
"""
blocks: [16px]

[------]
[------]
[------]
"""
class Game(arcade.Window):
    def __init__(self, window_width, window_height, title):
        # Call the Window class's init function
        super().__init__(window_width, window_height, title)
        # Display Variables
        self.window_width, self.window_height = window_width, window_height

        self.unit_row, self.unit_col = window_width//16, window_height//16

        # Logic Variable
        self.score = 0
        self.lives = 3
        self.snake = snake.Snake(self.unit_row//2, self.unit_col//2)
        self.apple_list = apples.Apples(self.unit_row, self.unit_col)
        # 0: Start, 1: Running, 2: Pause, 3: End
        self.state = 0

        self.set_update_rate(0.12)

        arcade.set_background_color(arcade.color.ASH_GREY)
        

    def check_eat(self):
        if self.state in (2,3) or len(self.apple_list) == 0:
            return()


        for apple_i, apple in enumerate(self.apple_list.apple_list):
            if self.snake.head() == apple:
                self.score += 1
                self.apple_list.eat_apple(apple_i)
                self.snake.grow()
                self.apple_list.new_apple(self.snake.get_body())

    # New Game
    def new_game(self):
        self.reset()
        self.score = 0
        self.lives =  3
        self.state = 0

    def reset(self):
        self.snake.clear()
        self.apple_list.clear()
        self.apple_list.new_apple(self.snake.get_body())
    
    def death(self):
        if self.lives > 1:
            self.lives -= 1
            self.reset()
        else:
            self.state = 3


    # COLLISIONS
    def isOutOfBoundaries(self, pos):
        if pos[0] in range(0, self.unit_row) and pos[1] in range(0, self.unit_col):
            return False
        return True

    def checkPositionAllowed(self):
        if self.state in (2,3):
            return()
        collides_with_body = False

        for i in range(1, len(self.snake)):
            if self.snake.head() == self.snake.get_part(i):
                collides_with_body = True
                break
        if (collides_with_body or self.isOutOfBoundaries(self.snake.head())):
            self.death()

    def on_update(self, delta_time):
        if self.state in (0,1):
            self.snake.move()
            self.check_eat()
            self.checkPositionAllowed()

    """Game I/O - Display Info"""
    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcade.start_render()
        self.snake.draw()
        self.apple_list.draw()
        if self.state not in (2,3):
            stats_overlay(self.width, self.height-20, self.score, self.lives)
        if self.state == 2:
            pause_overlay(self.width//2, 7*self.height//12)
        if self.state == 3:
            game_over_overlay(self.width//2, 7*self.height//12, self.score)

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if self.state == 0 and key in (arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT):
            self.state = 1
            
        if key == arcade.key.P:
            if self.state in (1,2):
                self.state = 3 - self.state
            elif self.state == 0:
                self.state = 2
        elif not self.state in (2,3):
            if key == arcade.key.DOWN:
                self.snake.set_direction(0)
            elif key == arcade.key.LEFT:
                self.snake.set_direction(1)
            elif key == arcade.key.UP:
                self.snake.set_direction(2)
            elif key == arcade.key.RIGHT:
                self.snake.set_direction(3)
        elif self.state == 3:
            if key == arcade.key.SPACE:
                self.new_game()

    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        pass

def stats_overlay(width, y, score, lives):
    arcade.draw_text("Score: %d" % (score), 20, y, arcade.color.ARSENIC, font_size=16)
    arcade.draw_text("Lives %d" % (lives), width-20, y, arcade.color.ARSENIC, font_size=16, anchor_x="right")

def pause_overlay(x, y):
    arcade.draw_text("PAUSED", x, y,arcade.color.ARSENIC,font_size=40, align="center", anchor_x="center")
    arcade.draw_text("Press P to continue.", x, y-100, arcade.color.ARSENIC, font_size=16, align="center", anchor_x="center")


def game_over_overlay(x, y, score):
    arcade.draw_text("Game Over!\nYou score %d points." % (score), x, y,arcade.color.ARSENIC,font_size=40, align="center", anchor_x="center")
    arcade.draw_text("Press SPACE to start a new game.", x, y-100, arcade.color.ARSENIC, font_size=16, align="center", anchor_x="center")