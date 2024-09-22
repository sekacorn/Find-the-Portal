import pygame  # if you see No module Named pygame you need to install pygame framework
import random

# Declare the necessary variables
class DecisionFactory(object):
    def __init__(self, name='Davros'):
        self.setFirst = False
        self.setSecond = False
        self.back = False
        self.name = name
        self.directions = ['wait', 'down', 'up', 'left', 'right']
        self.last_result = ['success', 'wall', 'portal', 'health', 'poison']
        self.last_direction = 'wait'
        self.xPosition = 0 # xPosition
        self.yPosition = 0 # yPosition
        self.randPortalX = 0 # randPortalX
        self.randPortalY = 0 # randPortalY
        self.stack = []
        self.back_x = 0
        self.back_y = 0
        self.mazeWidth = 0 # mazeWidth
        self.mazeHeight = 0 # mazeHeight
        self.nextX = 0
        self.nextY = 0
        self.rev = []
        self.count2 = 0
        self.x = 0
        self.y = 0
        self.counter = 0
        self.old_y = 0 # yPosition
        self.old_x = 0 # xPosition
        self.mind = []
        self.runFirst = True
        self.runSecond = True
        self.maze = []
        self.initX = 0 # xPosition
        self.initY = 0 # yPosition
        self.second = False
        self.num = 0
        self.r = 0
        self.choice = False
        self.health = 3
        self.numP = 5
        self.numUp = 5
        self.Map1 = ['11111111111111111111',
                     '1          1       1',
                     '1  1111    1  1111 1',
                     '1     1    1  1    1',
                     '1 11111    1111    1',
                     '1     1            1',
                     '1     1    1       1',
                     '11111 111111111    1',
                     '1     1       1    1',
                     '1     1    1111    1',
                     '1 11111            1',
                     '1     1111111 1111 1',
                     '1             1    1',
                     '11111111      1111 1',
                     '1                1 1',
                     '1   111111111    1 1',
                     '1   1         1111 1',
                     '1   1 111111111    1',
                     '1   1         1    1',
                     '11111111111111111111']

    # Initialize the maze
    def initialize(self, mazeWidth, mazeHeight):
        self.mazeWidth = mazeWidth
        self.mazeHeight = mazeHeight
        self.MakeMind()

        # Create the maze array size
        for row in range(self.mazeHeight):
            self.maze.append([])  # Add each column
            for column in range(mazeWidth):
                self.maze[row].append(0)

        # Automatically fill in walls according to Map1 design
        for row in range(self.mazeHeight):
            for column in range(self.mazeWidth):
                if self.Map1[row][column] == "1":
                    self.maze[row][column] = 1

        # Select the initial position of the intelligence
        self.xPosition = random.randint(1, self.mazeWidth - 2)
        self.yPosition = random.randint(1, self.mazeHeight - 2)
        while self.maze[self.yPosition][self.xPosition] == 1:
            self.xPosition = random.randint(1, self.mazeWidth - 2)
            self.yPosition = random.randint(1, self.mazeHeight - 2)

        # Select the position of the portal
        self.randPortalX = random.randint(1, self.mazeWidth - 2)
        self.randPortalY = random.randint(1, self.mazeHeight - 2)
        while self.maze[self.randPortalY][self.randPortalX] == 1:
            self.randPortalX = random.randint(1, self.mazeWidth - 2)
            self.randPortalY = random.randint(1, self.mazeHeight - 2)

        # Portal Location
        self.maze[self.randPortalY][self.randPortalX] = 3
        self.old_y = self.yPosition
        self.old_x = self.xPosition
        self.initX = self.xPosition
        self.initY = self.yPosition

        print("Portal:[", self.randPortalX, ",", self.randPortalY, "]")
        print("Initial Intelligence Position: [", self.xPosition, ",", self.yPosition, "]")

        # Insert poison and health ups
        self.add_random_items(self.numP, 4)  # Poison
        self.add_random_items(self.numUp, 5)  # Health

    # Helper to add random items
    def add_random_items(self, count, item_type):
        i = 0
        while i < count:
            addX = random.randint(1, self.mazeWidth - 2)
            addY = random.randint(1, self.mazeHeight - 2)
            while self.maze[addY][addX] != 0:
                addX = random.randint(1, self.mazeWidth - 2)
                addY = random.randint(1, self.mazeHeight - 2)
            self.maze[addY][addX] = item_type
            i += 1

    # Get a random decision (movement)
    def get_decision(self, verbose: bool = True):
        if self.last_result == 'portal':
            return self.ReRun()
        return self.random_direction()

    # More functions go here... (backtrack, random_direction, etc.)

# Set up the maze dimensions and display
mazeWidth = 20
mazeHeight = 20
margin = 5
width = 25
height = 25
value = 5

x = mazeWidth * 30 + 5
y = mazeHeight * 30 + 5 + 35
w_size = [x, y]

pygame.init()
win = pygame.display.set_mode(w_size)
pygame.display.set_caption('The Brainy Bunch')

# Set colors to be used
white = (255, 255, 255)
green = (0, 255, 0)
black = (0, 0, 0)
purple = (128, 0, 128)
red = (255, 0, 0)
yellow = (255, 255, 0)

# Create and initialize the intelligence object
Voldemort = DecisionFactory()

while Voldemort.runSecond and Voldemort.health > 0:
    Voldemort.runProg(mazeWidth, mazeHeight)
    win.fill(black)
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Draw maze
    for row in range(Voldemort.mazeHeight):
        for column in range(Voldemort.mazeWidth):
            color = white
            if Voldemort.maze[row][column] == 1:
                color = green
            elif Voldemort.maze[row][column] == 2:
                color = red
            elif Voldemort.maze[row][column] == 3:
                color = purple
            elif Voldemort.maze[row][column] == 4:
                color = black
            elif Voldemort.maze[row][column] == 5:
                color = yellow
            pygame.draw.rect(win, color, [(margin + width) * column + margin,
                                          (margin + height) * row + margin, width, height])

    pygame.display.update()

if Voldemort.health == 0:
    print("The intelligence died!")

pygame.quit()
