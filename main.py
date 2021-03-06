import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 640
screen_height = 600
player_size = 40
wall_size = 40
goal_size = 40
game_over = 0
main_menu = True

# Setting up the screen
screen = pygame.display.set_mode((screen_width,screen_height))

# Caption
pygame.display.set_caption("Maze Solver")

restart_img = pygame.image.load("restart.png")

s_img = pygame.image.load("start.png")
start_img = pygame.transform.scale(s_img,(100,100))

e_img = pygame.image.load("exit.png")
exit_img = pygame.transform.scale(e_img,(100,100))

# icon
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

def drawgrid():
    for line in range(0, 20):
        pygame.draw.line(screen,(255,255,255),(0, line * wall_size), (screen_width, line * wall_size))
        pygame.draw.line(screen,(255,255,255), (line * wall_size, 0), (line * wall_size, screen_height))

class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_clicked = False
    
    def draw(self):
        pos = pygame.mouse.get_pos()
        action = False
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
        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                dx -= 3
            if key[pygame.K_RIGHT]:
                dx += 3
            if key[pygame.K_DOWN]:
                dy += 3
            if key[pygame.K_UP]:
                dy -= 3

            #check of collision
            for wall in m.wall_list:
                if wall[1].colliderect(self.rect.x + dx, self.rect.y, self.width - 8, self.height - 5):
                    dx = 0
                if wall[1].colliderect(self.rect.x, self.rect.y + dy, self.width - 5, self.height - 5):
                    dy = 0

            #collision with enemy
            if pygame.sprite.spritecollide(self, enemy_group, False):
                game_over = -1
                
            self.rect.x += dx
            self.rect.y += dy
        
        elif game_over == -1:
            self.image = self.dead_img
            if self.rect.y > 30:
                self.rect.y -= 4

        #draw player on screen
        screen.blit(self.image, self.rect)
        return game_over

    def restart(self, x, y):
        player_img = pygame.image.load("minion.png")
        self.dead_img = pygame.image.load("dead.png")
        self.image = pygame.transform.scale(player_img,(40,40))
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
        self.rect.x += self.move_direction
        self.move_counter += 1
        if self.move_counter > 155:
            self.move_direction *= -1
            self.move_counter = 0



class Maze():
    def __init__(self, level, enemy_group):
        self.wall_list = []
        self.goal_list = []
        self.player_list = []
        self.level = level

        #load image of walls
        wall_img = pygame.image.load("brickwall.png")

        # load image of goal
        goal_img = pygame.image.load("goal.png")
        row_count = 0

        for row in level:
            col_count = 0
            for contents in row:
                if contents == 1:
                    w_img = pygame.transform.scale(wall_img, (wall_size, wall_size))
                    w_rect = w_img.get_rect()
                    w_rect.x = col_count * wall_size
                    w_rect.y = row_count * wall_size
                    wall = (w_img, w_rect)
                    self.wall_list.append(wall)                
                elif contents == 2:
                    g_img = pygame.transform.scale(goal_img,(goal_size, goal_size))
                    g_rect = g_img.get_rect()
                    g_rect.x = col_count * goal_size
                    g_rect.y = row_count * goal_size
                    goal = (g_img, g_rect)
                    self.goal_list.append(goal)
                
                elif contents == 3:
                    enemy = Enemies(col_count * wall_size, row_count * wall_size)
                    enemy_group.add(enemy)


                col_count += 1
            row_count += 1

    def draw(self):

        for wall in self.wall_list:
            screen.blit(wall[0], wall[1])

        for goal in self.goal_list:
            screen.blit(goal[0],goal[1])



# Maze list
maze_level = [
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1],
[1,0,1,0,1,0,1,1,1,0,1,1,1,0,1,1],
[1,0,1,0,1,0,1,1,1,1,1,1,1,0,1,1],
[1,0,1,3,0,0,0,0,1,0,1,1,1,0,1,1],
[1,0,1,1,0,1,3,0,0,0,0,0,0,0,1,1],
[1,0,1,0,0,1,0,1,1,1,1,1,1,1,1,1],
[1,0,0,1,0,1,0,0,0,0,1,1,0,1,1,1],
[1,1,0,1,0,1,1,1,1,0,1,0,0,0,0,1],
[1,1,3,0,0,0,0,1,1,0,1,0,1,1,0,1],
[1,0,0,1,1,1,0,1,1,0,0,0,1,1,0,1],
[1,1,0,1,1,1,1,0,1,1,1,1,1,1,0,1],
[1,1,0,0,0,1,1,0,0,0,0,1,1,1,2,1],
[1,0,1,1,0,0,0,1,0,1,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

enemy_group = pygame.sprite.Group()
m = Maze(maze_level, enemy_group)
p = Player(40, 40)
restart_button = Button(screen_width // 2 - 50, screen_height // 2 - 40 , restart_img)
start_button = Button(screen_width//2 - 40, screen_height//2 - 150, start_img)
exit_button = Button(screen_width // 2 - 40, screen_height //2  ,exit_img)

run = True

while run:
    clock.tick(fps)
    # Setting the background to yellow
    screen.fill((255,255,0))
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
        enemy_group.draw(screen)
        game_over = p.update(game_over)

    # Looping for catching events
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            run = False
            pygame.quit()
            
    pygame.display.update()





