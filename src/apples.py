import arcade
import random

class Apples():

    def __init__(self, width=0, length=0):
        self.apple_list = []
        self.row_size = width
        self.column_size = length
        if self.row_size * self.column_size:
            self.new_apple()

    """Game Logic"""
    def new_apple(self, snake_list=[]):
        if len(snake_list) >= self.row_size * self.column_size:
            return()
        # x: random (left_bound, right_bound)
        # y: random (top_bound, bottom_bound)
        apple = (random.randint(0, self.row_size-1), random.randint(0, self.column_size-1))
        block_list = snake_list + self.apple_list
        for block in block_list:
            if block == apple:
                apple = (random.randint(0, self.row_size-1), random.randint(0, self.column_size-1))
        self.apple_list.append(apple)

    def eat_apple(self, apple_i):
        self.apple_list.pop(apple_i)

    def __len__(self):
        return(len(self.apple_list))

    def __str__(self):
        return(str([a for a in self.apple_list]))

    """Display Info"""
    def clear(self):
        self.apple_list = []

    def draw(self):
        for apple in self.apple_list:

            arcade.draw_circle_filled(apple[0]*16+8, apple[1]*16+8, 8, arcade.color.RADICAL_RED)
