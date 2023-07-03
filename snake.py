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
apple = pygame.image.load('graphic/apple.png').convert_alpha()


game = True


class FRUIT:
    def __init__(self) :
        self.spawn()
        
    
    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int (self.pos.y * cell_size), cell_size, cell_size)
        window.blit(apple,fruit_rect)

    def spawn(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class SNAKE:
    def __init__(self):
        self.body = [Vector2(7,10), Vector2(6,10), Vector2(5,10)]
        self.dir = Vector2(1,0)
        self.add_block = False
        #graphics
        self.head_up = pygame.image.load('graphic/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('graphic/head_down.png').convert_alpha()
        self.head_left = pygame.image.load('graphic/head_left.png').convert_alpha()
        self.head_right = pygame.image.load('graphic/head_right.png').convert_alpha()
        self.tail_up = pygame.image.load('graphic/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('graphic/tail_down.png').convert_alpha()
        self.tail_left = pygame.image.load('graphic/tail_left.png').convert_alpha()
        self.tail_right = pygame.image.load('graphic/tail_right.png').convert_alpha()
        self.body_horizontal = pygame.image.load('graphic/body_horizontal.png').convert_alpha()
        self.body_vertical = pygame.image.load('graphic/body_vertical.png').convert_alpha()
        #corners
        self.body_tr = pygame.image.load('graphic/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('graphic/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('graphic/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('graphic/body_bl.png').convert_alpha()
        
        
    def draw_snake(self):
        self.update_head_dir()
        self.update_tail_dir()

        for index,block in enumerate(self.body):
            #a rect for the snake
            posX = int(block.x * cell_size)
            posY = int(block.y * cell_size)
            block_rect = pygame.Rect(posX, posY ,cell_size ,cell_size)

            #direction of head
            if index == 0:
                window.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                window.blit(self.tail,block_rect)
            else:
                #dir of body
                prev_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if prev_block.x == next_block.x:
                    window.blit(self.body_vertical, block_rect)
                elif prev_block.y == next_block.y:
                    window.blit(self.body_horizontal, block_rect)
                else:
                    if prev_block.x == -1 and next_block.y == -1 or prev_block.y == -1 and next_block.x == -1:
                        window.blit(self.body_tl, block_rect)
                    elif prev_block.x == -1 and next_block.y == 1 or prev_block.y == 1 and next_block.x == -1:
                        window.blit(self.body_bl, block_rect)
                    elif prev_block.x == 1 and next_block.y == -1 or prev_block.y == -1 and next_block.x == 1:
                        window.blit(self.body_tr, block_rect)
                    elif prev_block.x == 1 and next_block.y == 1 or prev_block.y == 1 and next_block.x == 1:
                        window.blit(self.body_br, block_rect)


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

    def update_head_dir(self):
        head_dir = self.body[1] - self.body[0]
        if head_dir == Vector2(1,0):self.head = self.head_left
        elif head_dir == Vector2(-1,0): self.head = self.head_right
        elif head_dir == Vector2(0,1): self.head = self.head_up    
        elif head_dir == Vector2(0,-1): self.head = self.head_down

    def update_tail_dir(self):
        tail_dir = self.body[-2] - self.body[-1]
        if tail_dir == Vector2(1,0):self.tail = self.tail_left
        elif tail_dir == Vector2(-1,0): self.tail = self.tail_right
        elif tail_dir == Vector2(0,1): self.tail = self.tail_up
        elif tail_dir == Vector2(0,-1): self.tail = self.tail_down


    
    



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
