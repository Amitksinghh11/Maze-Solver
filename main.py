import pygame
import pickle

pygame.init()

# frame per seconds
clock = pygame.time.Clock()
fps = 60

# constants 
screen_width = 980
screen_height = 635
player_size = 30
wall_size = 35
goal_size = 35
game_over = 0
main_menu = True

# Setting up the screen
screen = pygame.display.set_mode((screen_width,screen_height))

# Caption
pygame.display.set_caption("Maze Solver")

# loading restart image
restart_img = pygame.image.load("restart.png")

# reached goal image
r_img = pygame.image.load("fireworks.png")
reached_img = pygame.transform.scale(r_img,(100,100))

# loading start image
s_img = pygame.image.load("start.png")
start_img = pygame.transform.scale(s_img,(100,100))

# loading exit image
e_img = pygame.image.load("exit.png")
exit_img = pygame.transform.scale(e_img,(100,100))

# icon
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# drawing grids for refrence
def drawgrid():
    for line in range(0, 53):
        pygame.draw.line(screen,(255,255,255),(0, line * wall_size), (screen_width, line * wall_size))
        pygame.draw.line(screen,(255,255,255), (line * wall_size, 0), (line * wall_size, screen_height))

class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # trigger to check if mouse is clicked
        self.is_clicked = False
    
    def draw(self):
        # getting the position of mouse
        pos = pygame.mouse.get_pos()
        # trigger to perform an action
        action = False
        # checking if the mouse is clicked on the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1 and self.is_clicked == False:
                action = True
                self.is_clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.is_clicked = False

        screen.blit(self.image, self.rect)
        return action


class Player():
    def __init__(self,x ,y):
        self.restart(x, y)
    
    def update(self, game_over):
        dx = 0
        dy = 0
        # checking if game is still running or not
        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                dx -= 2
            if key[pygame.K_RIGHT]:
                dx += 2
            if key[pygame.K_DOWN]:
                dy += 2
            if key[pygame.K_UP]:
                dy -= 2

            #check of collision
            for wall in m.wall_list:
                if wall[1].colliderect(self.rect.x + dx, self.rect.y, self.width - 2, self.height):
                    dx = 0
                if wall[1].colliderect(self.rect.x, self.rect.y + dy, self.width - 2, self.height):
                    dy = 0

            #collision with enemy
            if pygame.sprite.spritecollide(self, enemy_group, False):
                game_over = -1

            if pygame.sprite.spritecollide(self, goal_group, False):
                game_over = 1
                
            self.rect.x += dx
            self.rect.y += dy
        # checking for game is over
        elif game_over == -1:
            self.image = self.dead_img
            if self.rect.y > 30:
                self.rect.y -= 4

        #draw player on screen
        screen.blit(self.image, self.rect)
        return game_over

    def restart(self, x, y):
        # initializing all the needed variables
        player_img = pygame.image.load("minion.png")
        self.dead_img = pygame.image.load("dead.png")
        self.image = pygame.transform.scale(player_img,(player_size, player_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()



class Enemies(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("enemy.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
    def update(self):
        # for moving enemies
        self.rect.x += self.move_direction
        self.move_counter += 1
        if self.move_counter > 155:
            self.move_direction *= -1
            self.move_counter = 0

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load("goal.png")
        self.image = pygame.transform.scale(self.img,(goal_size, goal_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Maze():
    def __init__(self, level, enemy_group):
        self.wall_list = []
        self.goal_list = []
        self.player_list = []
        self.level = level

        #load image of walls
        wall_img = pygame.image.load("brickwall.png")

        row_count = 0

        for row in level:
            col_count = 0
            for contents in row:
                # checking for walls
                if contents == 1:
                    w_img = pygame.transform.scale(wall_img, (wall_size, wall_size))
                    w_rect = w_img.get_rect()
                    w_rect.x = col_count * wall_size
                    w_rect.y = row_count * wall_size
                    wall = (w_img, w_rect)
                    self.wall_list.append(wall)   
                # checking for goal             
                elif contents == 2:
                    goal = Goal(col_count * wall_size, row_count * wall_size)
                    goal_group.add(goal)
                
                # checking for enemies
                elif contents == 3:
                    enemy = Enemies(col_count * wall_size, row_count * wall_size)
                    enemy_group.add(enemy)


                col_count += 1
            row_count += 1

    def draw(self):
        # drawing wall and goal
        for wall in self.wall_list:
            screen.blit(wall[0], wall[1])

        for goal in self.goal_list:
            screen.blit(goal[0],goal[1])



# Maze list
maze_level = [
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,1,1],
[1,0,1,0,1,0,1,1,1,0,1,1,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,1],
[1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,1,0,1,1,1,0,0,0,0,1,0,1,1],
[1,0,1,3,0,0,0,0,0,1,1,0,0,0,1,1,1,0,0,0,1,0,0,1,1,1,1,1],
[1,0,1,1,0,1,3,0,0,0,0,0,1,0,1,1,0,1,1,0,1,0,1,1,1,1,0,1],
[1,0,1,0,0,1,0,1,0,1,0,1,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,1],
[1,0,0,1,0,1,0,0,0,0,1,1,0,1,1,1,1,0,1,0,1,1,1,0,1,1,0,1],
[1,1,0,1,0,1,1,1,1,0,1,0,0,0,0,0,0,0,1,0,1,1,1,0,1,1,0,1],
[1,1,3,0,0,0,0,0,1,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,0,0,0,1],
[1,0,0,0,1,0,1,1,0,0,0,0,1,0,0,0,0,1,1,0,1,0,1,0,1,0,1,1],
[1,1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,1,0,1,0,1,0,0,1,1],
[1,1,0,0,0,1,1,0,0,0,0,1,1,1,0,1,1,0,1,1,1,1,0,1,1,0,1,1],
[1,0,1,1,0,0,0,1,0,1,0,0,0,0,0,1,1,0,0,0,1,1,0,1,1,0,2,1],
[1,0,0,1,0,1,0,0,0,1,1,1,0,1,1,0,1,0,1,0,0,0,0,0,0,0,1,1],
[1,1,0,1,1,0,1,0,0,0,0,0,0,1,1,0,1,0,1,0,1,1,1,1,1,0,0,1],
[1,1,0,0,0,0,0,0,1,1,0,1,0,1,1,0,0,0,1,0,0,1,1,0,0,1,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

# calling instances of the classes
enemy_group = pygame.sprite.Group()
goal_group = pygame.sprite.Group()
m = Maze(maze_level, enemy_group)
p = Player(36, 35)
restart_button = Button(screen_width // 2 - 50, screen_height // 2 - 40 , restart_img)
start_button = Button(screen_width//2 - 40, screen_height//2 - 150, start_img)
exit_button = Button(screen_width // 2 - 40, screen_height //2  ,exit_img)

# trigger to check if game is running
run = True

while run:
    # fixing the fps
    clock.tick(fps)

    # Setting the background to yellow
    screen.fill((255,255,0))

    # checking for main menu
    if main_menu:
        if start_button.draw():
            main_menu = False
        if exit_button.draw():
            run = False
    else:
        m.draw()
        if game_over == 0:
            enemy_group.update()
        elif game_over == -1:
            if restart_button.draw():
                p.restart(40,40)
                game_over = 0
        elif game_over == 1:
            screen.blit(reached_img, (screen_width // 2 , screen_height // 2 - 200))
            if restart_button.draw():
                p.restart(40,40)
                game_over = 0
        enemy_group.draw(screen)
        goal_group.draw(screen)
        game_over = p.update(game_over)

    # Looping for exit event
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            run = False
            pygame.quit()
            
    pygame.display.update()





