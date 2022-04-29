import pygame
import random
import time, datetime 
import psycopg2 

pygame.init()
screen = pygame.display.set_mode((800, 600))

conn = psycopg2.connect(
    host = 'localhost',
    database = 'phonebook',
    user = 'postgres',
    password = '4477'
)

conn.autocommit = True

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

xx = 20
yy = 770
zz = 570

def wall_dr():
    for i in range(80):
        pygame.draw.rect(screen, (0, 0, 255), (i*10, 0*10, 10, 10))
        pygame.draw.rect(screen, (0, 0, 255), (i*10, 59*10, 10, 10))
    for i in range(60):
        pygame.draw.rect(screen, (0, 0, 255), (0*10, i*10, 10, 10))
        pygame.draw.rect(screen, (0, 0, 255), (79*10, i*10, 10, 10))
    

class Food:
    def __init__(self, color, time, size):
        self.x = random.randint(10, yy)
        self.y = random.randint(10, zz)
        self.type = color
        self.time = time
        self.st_time = datetime.datetime.now()
        self.size = size

    def get(self, snake):
        self.x = random.randint(10, yy)
        self.y = random.randint(10, zz)
        while([self.x, self.y] in snake.elements):
            self.x = random.randint(10, yy)
            self.y = random.randint(10, zz)
        self.st_time = datetime.datetime.now()
        #print(self.st_time.second)

    def draw(self, snake):
        if self.time < (datetime.datetime.now() - self.st_time).seconds:
            self.get(snake)
        pygame.draw.rect(screen, self.type, (self.x, self.y, 20, 20))

class Snakee:
    def __init__(self):
        self.size = 1
        self.elements = [[400, 300]]
        self.dx = 0
        self.dy = 1
        self.is_add = 0
        self.speed = 20
        self.color = GREEN
        self.radius = 20

    def draw(self):
        for element in self.elements:
            pygame.draw.rect(screen, self.color, (element[0], element[1], self.radius, self.radius))

    def eat(self, foodx, foody):
        x = self.elements[0][0]
        y = self.elements[0][1]

        if foodx-10 <= x <= foodx + 10 and foody -10 <= y <= foody + 10:
            #if(foodx == x and foody == y):
            return True
        return False

    def add_to_snake(self):
        while(self.is_add != 0):    
            self.size += 1
            #self.elements.append([0, 0])
            self.elements.insert(0, [self.elements[0][0] + self.dx*10, self.elements[0][1] + self.dy*10])
            self.is_add -= 1
        if not self.size % 7:
            self.speed += 5

    def lose(self):
        for i in range(1, self.size - 1):
            if self.elements[0][0] == self.elements[i][0] and self.elements[0][1] == self.elements[i][1]:
                return True
        if 10 >= self.elements[0][0] or 10 >= self.elements[0][1] or yy <= self.elements[0][0] or zz <= self.elements[0][1]:
            return True

        return False

    def move(self):
        if self.is_add:
            self.add_to_snake()
        self.elements.insert(0, [self.elements[0][0] + self.dx*10, self.elements[0][1] + self.dy*10])
        self.elements.pop(-1)

def move(ls):
    return ls[random.randint(0, 1)]

def game():
    font_small = pygame.font.SysFont("Verdana", 20)
    snake = Snakee()
    foodx = [Food(RED, 5, 1), Food(BLUE, 3, 3)]
    food = move(foodx)
    FPS = pygame.time.Clock()
    running = True

    while running:
        if snake.lose():
            time.sleep(1)
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_UP and snake.dy != 1:
                    snake.dx = 0
                    snake.dy = -1
                elif event.key == pygame.K_DOWN and snake.dy != -1:
                    snake.dx = 0
                    snake.dy = 1
                elif event.key == pygame.K_RIGHT and snake.dx != -1:
                    snake.dx = 1
                    snake.dy = 0
                elif event.key == pygame.K_LEFT and snake.dx != 1:
                    snake.dx = -1
                    snake.dy = 0

        snake.move()
        if snake.eat(food.x, food.y):
            snake.is_add = food.size
            food = move(foodx)
            food.get(snake)

        screen.fill(BLACK)
        snake.draw()
        food.draw(snake)
        wall_dr()

        if snake.lose():
            time.sleep(1)
            running = False

        sc = font_small.render('Score: ' + str(snake.size), True, WHITE)
        screen.blit(sc, (680, 15))
        lv = snake.size // 4 + 1
        lvls = font_small.render(f'Lvl: {lv}', True, WHITE)
        screen.blit(lvls, (680, 35))

        pygame.display.flip()

        FPS.tick(snake.speed)
    return (False, snake.size)


def create_table():
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE snakebd(
        name VARCHAR(50),
        score INT
    );
    ''')
    cursor.close();
def delete_table():
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE snakebd''')
    cursor.close()

def main():
    #create_table();
    #delete_table();
    running = True
    start = False
    font = pygame.font.SysFont("Verdana", 60)
    font2 = pygame.font.SysFont("Verdana", 40)
    #snake = Snakee()
    cnt = 0
    name = input("Loggin:")
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT * FROM snakebd WHERE name = \'{name}\'")
        bdscore = cursor.fetchone()
        #print(bdscore[1])
        if(bdscore == None):
            maxx = 0
            cursor.execute(f"insert into snakebd (name, score) values ('{name}','{maxx}')")
        else:
            maxx = bdscore[1]
    while running:
        screen.fill((23, 45, 155))
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 300 <= pos[0] <= 500 and 400 <= pos[1] <= 500:
                    start = True

        pygame.draw.rect(screen, WHITE, (300, 400, 200, 100))
        st_but = font.render("START", True, BLACK)
        screen.blit(st_but, (305, 410))

        maxi = font2.render(f'Maximum score: {maxx}', True, WHITE)
        screen.blit(maxi, (310, 540))
        if start:
            start, score = game()
            maxx = max(maxx, score)
            #cnt += 1
            '''
            snake.cleaning()
            snake.elements = [[400, 300]]
            snake.speed = 20
            snake.size = 1
            #del snake
            '''
        pygame.display.flip()

    with conn.cursor() as cursor:
        cursor.execute(f"update snakebd set score = \'{maxx}\' where name = \'{name}\'")
    pygame.quit()

main()