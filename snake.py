import pygame
import sys
from pygame.math import Vector2
import random
import time


pygame.init()

cell_size = 40
cell_number = 20

window = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))

clock = pygame.time.Clock()

game = True


class FRUIT:
    def __init__(self) :
        self.spawn()
        
    
    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int (self.pos.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(window, "red", fruit_rect)

    def spawn(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class SNAKE:
    def __init__(self):
        self.body = [Vector2(7,10), Vector2(6,10), Vector2(5,10)]
        self.dir = Vector2(1,0)
        self.add_block = False

    def draw_snake(self):
        for block in self.body:
            snakeX = int(block.x * cell_size)
            snakeY = int(block.y * cell_size)
            snake_rect = pygame.Rect(snakeX, snakeY , cell_size, cell_size)
            pygame.draw.rect(window,(183,111,122), snake_rect)

    def move_snake(self):
        if self.add_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.dir)
            self.body = body_copy[:]
            self.add_block = False

        body_copy = self.body[:-1]
        body_copy.insert(0,body_copy[0] + self.dir)
        self.body = body_copy[:]

    def grow(self):
        self.add_block = True


class MAIN:
    
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.eat()
        self.death()

    def draw(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def eat(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.spawn()
            self.fruit.draw_fruit()
            self.snake.grow()
            
    def death(self):
        if not 0 <= self.snake.body[0].x < cell_number: # if snake hits walls
            self.game_end()
        if not 0 <= self.snake.body[0].y < cell_number:
            self.game_end()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_end()


    def game_end(self):
        pygame.quit()
        sys.exit()

main = MAIN()

WINDOW_UPDATE = pygame.USEREVENT
pygame.time.set_timer(WINDOW_UPDATE,150)

while game:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == WINDOW_UPDATE:
            main.update()
        if event.type == pygame.KEYDOWN:## movement of snake
            if event.key == pygame.K_UP:
                if main.snake.dir.y != 1:
                    main.snake.dir = Vector2(0,-1)
            if event.key == pygame.K_DOWN:
                if main.snake.dir.y != -1:
                    main.snake.dir = Vector2(0,1)
            if event.key == pygame.K_LEFT:
                if main.snake.dir.x != 1:
                    main.snake.dir = Vector2(-1,0)
            if event.key == pygame.K_RIGHT:
                if main.snake.dir.x != -1:
                    main.snake.dir = Vector2(1,0)

    
        

    window.fill((175,215,70))
    main.draw()
    pygame.display.update()
    clock.tick(60)
