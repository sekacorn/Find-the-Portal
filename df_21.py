import pygame  # if you see No module Named pygame you need to install pygame framework
import random


# import numpy as np
#Sekacorn

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
        self.xPosition = 0 #xPosition
        self.yPosition = 0 # yPosition
        self.randPortalX = 0 #randPortalX
        self.randPortalY = 0 #randPortalY
        self.stack = []
        self.back_x = 0
        self.back_y = 0
        self.mazeWidth = 0 #mazeWidth
        self.mazeHeight = 0 #mazeHeight
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
        self.initX = 0 #xPosition
        self.initY = 0 #yPosition
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
        # Note: We have relativistic coordinates recorded here
        # since the map is relative to the player's first known and
        # recorded position:
        # self.state.ps=(0,0)

    # initialize variables
    def initialize(self, mazeWidth, mazeHeight):
        self.mazeWidth = mazeWidth
        self.mazeHeight = mazeHeight
        self.MakeMind()

        # create the maze array size
        for row in range(self.mazeHeight):
            self.maze.append([])
            # Add each column
            for column in range(mazeWidth):
                self.maze[row].append(0)

        #  Automatically fill in walls according to Map1 design
        for row in range(self.mazeHeight):
            for column in range(self.mazeWidth):
                if self.Map1[row][column] == "1":
                    self.maze[row][column] = 1
        #  Select the initial position of the intelligence
        self.xPosition = random.randint(1, self.mazeWidth - 2)
        self.yPosition= random.randint(1, self.mazeHeight - 2)
        # test if the selected space is a wall
        while self.maze[self.yPosition][self.xPosition] == 1:
            self.xPosition = random.randint(1, self.mazeWidth-2)
            self.yPosition = random.randint(1, self.mazeHeight-2)
        #  Select the position of the portal
        self.randPortalX = random.randint(1, self.mazeWidth-2)
        self.randPortalY = random.randint(1, self.mazeHeight-2)
        while self.maze[self.randPortalY][self.randPortalX] == 1:
            self.randPortalX = random.randint(1, self.mazeWidth-2)
            self.randPortalY = random.randint(1, self.mazeHeight-2)
        # Portal Location
        self.maze[self.randPortalY][self.randPortalX] = 3
        self.old_y = self.yPosition
        self.old_x = self.xPosition
        self.initX = self.xPosition
        self.initY = self.yPosition

        # Show the Portal Location and the initial position of the intelligent agent
        print("Portal:[", self.randPortalX, ", ", self.randPortalY, "]")
        print("Intiial Intelligence Position: [", self.xPosition, ", ", self.yPosition, "]")

        i = 0
        # insert poison
        while i < self.numP:
            addX = random.randint(1, self.mazeWidth - 2)
            addY= random.randint(1, self.mazeHeight - 2)
            while self.maze[addY][addX] != 0:
                addX = random.randint(1, self.mazeWidth - 2)
                addY= random.randint(1, self.mazeHeight - 2)
            self.maze[addY][addX] = 4
            i += 1

        i = 0
        # insert health ups
        while i < self.numUp:
            addX = random.randint(1, self.mazeWidth - 2)
            addY= random.randint(1, self.mazeHeight - 2)
            while self.maze[addY][addX] != 0:
                addX = random.randint(1, self.mazeWidth - 2)
                addY= random.randint(1, self.mazeHeight - 2)
            self.maze[addY][addX] = 5
            i += 1

       # for row in (self.mazeHeight):
        #    print self.maze

    # Calls for a random direction or calls for the second run
    def get_decision(self, verbose: object = True) -> object:
        if (self.last_result == 'portal'):
            return self.ReRun()
        else:
            return self.random_direction()

    def backtrack(self):
        print("Backtracking!")
        self.back_y = self.stack.pop()
        self.back_x = self.stack.pop()
        self.back = True
        self.choice = True

        if self.yPosition is self.back_y + 1:
            self.r = 2
        elif self.yPosition is self.back_y - 1:
            self.r = 1
        elif self.xPosition is self.back_x + 1:
            self.r = 3
        else:
            self.r = 4

    # Finds and returns the random direction
    def random_direction(self):
        self.r = random.randint(0, 4)
        self.old_x = self.xPosition
        self.old_y = self.yPosition
        self.choice = False
        self.back = False

        self.vision()
        while self.choice is False:
            # This section will test if the agent is trapped in a pocket and allow it to retrace its steps
            if self.mind[self.yPosition + 1][self.xPosition] != 0 and \
                    self.mind[self.yPosition - 1][self.xPosition] != 0 and \
                    self.mind[self.yPosition][self.xPosition + 1] != 0 and \
                    self.mind[self.yPosition][self.xPosition - 1] != 0:
                self.backtrack()
            else:  # checks for redundant movement
                if self.last_direction == self.directions[self.r] and self.last_result == 'wall':
                    self.r = random.randint(0, 4)
                elif self.last_direction == 'left' and self.directions[self.r] == 'right':
                    self.r = random.randint(0, 4)
                elif self.last_direction == 'right' and self.directions[self.r] == 'left':
                    self.r = random.randint(0, 4)
                elif self.last_direction == 'up' and self.directions[self.r] == 'down':
                    self.r = random.randint(0, 4)
                elif self.last_direction == 'down' and self.directions[self.r] == 'up':
                    self.r = random.randint(0, 4)
                elif self.directions[self.r] == 'left' and self.mind[self.yPosition][self.xPosition - 1] != 0:
                    self.r = random.randint(0, 4)
                elif self.directions[self.r] == 'right' and self.mind[self.yPosition][self.xPosition + 1] != 0:
                    self.r = random.randint(0, 4)
                elif self.directions[self.r] == 'up' and self.mind[self.yPosition - 1][self.xPosition] != 0:
                    self.r = random.randint(0, 4)
                elif self.directions[self.r] == 'down' and self.mind[self.yPosition + 1][self.xPosition] != 0:
                    self.r = random.randint(0, 4)
                else:
                    self.choice = True

        if self.directions[self.r] == 'up':
            if self.maze[self.yPosition - 1][self.xPosition] == 1:
                self.put_result('wall')
                self.last_result = 'wall'
                self.mind[self.yPosition - 1][self.xPosition] = 1
            elif self.maze[self.yPosition - 1][self.xPosition] == 5:
                self.yPosition -= 1
                self.put_result('health')
                self.last_result = 'health'
                self.mind[self.old_y][self.old_x] = 5
                self.maze[self.old_y][self.old_x] = 0
                self.health += 1
                if self.back is False:
                    self.stack.append(self.old_x)
                    self.stack.append(self.old_y)
            elif self.maze[self.yPosition - 1][self.xPosition] == 4:
                if self.maze[self.yPosition - 1][self.xPosition - 1] == 0:
                    if self.maze[self.yPosition][self.xPosition - 1] == 0:
                        if self.last_direction == 'right':
                            print("Backtracking!")
                            self.yPosition = self.stack.pop()
                            self.xPosition = self.stack.pop()
                            self.r = 3
                            self.put_result('success')
                            self.last_result = 'success'
                            print ("Avoiding Poison")
                            self.mind[self.old_y][self.old_x] = 9
                            self.maze[self.old_y][self.old_x] = 0
                        else:
                            self.r = 3
                            self.xPosition -= 1
                            self.put_result('success')
                            self.last_result = 'success'
                            print ("Avoiding Poison")
                            self.mind[self.old_y][self.old_x] = 9
                            self.maze[self.old_y][self.old_x] = 0
                            if self.back is False:
                                self.stack.append(self.old_x)
                                self.stack.append(self.old_y)
                    else:
                        self.yPosition -= 1
                        self.put_result('poison')
                        self.last_result = 'poison'
                        self.mind[self.old_y][self.old_x] = 4
                        self.maze[self.old_y][self.old_x] = 0
                        self.health -= 1
                        if self.back is False:
                            self.stack.append(self.old_x)
                            self.stack.append(self.old_y)
                elif self.maze[self.yPosition - 1][self.xPosition + 1] == 0:
                    if self.maze[self.yPosition][self.xPosition +1] == 0:
                        if self.last_direction == 'left':
                            print("Backtracking!")
                            self.yPosition = self.stack.pop()
                            self.xPosition = self.stack.pop()
                            self.r = 4
                            self.put_result('success')
                            self.last_result = 'success'
                            print ("Avoiding Poison")
                            self.mind[self.old_y][self.old_x] = 9
                            self.maze[self.old_y][self.old_x] = 0
                        else:
                            self.r = 4
                            self.xPosition += 1
                            self.put_result('success')
                            self.last_result = 'success'
                            print ("Avoiding Poison")
                            self.mind[self.old_y][self.old_x] = 9
                            self.maze[self.old_y][self.old_x] = 0
                            if self.back is False:
                                self.stack.append(self.old_x)
                                self.stack.append(self.old_y)
                    else:
                            self.yPosition -= 1
                            self.put_result('poison')
                            self.last_result = 'poison'
                            self.mind[self.old_y][self.old_x] = 4
                            self.maze[self.old_y][self.old_x] = 0
                            self.health -= 1
                            if self.back is False:
                                self.stack.append(self.old_x)
                                self.stack.append(self.old_y)
                else:
                    self.yPosition -= 1
                    self.put_result('poison')
                    self.last_result = 'poison'
                    self.mind[self.old_y][self.old_x] = 4
                    self.maze[self.old_y][self.old_x] = 0
                    self.health -= 1
                    if self.back is False:
                        self.stack.append(self.old_x)
                        self.stack.append(self.old_y)
            else:
                self.yPosition -= 1
                self.put_result('success')
                # Reset previous maze position to 1
                self.last_result = 'success'
                self.mind[self.old_y][self.old_x] = 9
                self.maze[self.old_y][self.old_x] = 0
                if self.back is False:
                    self.stack.append(self.old_x)
                    self.stack.append(self.old_y)

        elif self.directions[self.r] == 'down':
            if self.maze[self.yPosition + 1][self.xPosition] == 1:  # Checks for a wall
                self.put_result('wall')
                self.last_result = 'wall'
                self.mind[self.yPosition + 1][self.xPosition] = 1
            elif self.maze[self.yPosition + 1][self.xPosition] == 5:  # Checks for a health
                self.yPosition += 1
                self.put_result('health')
                self.last_result = 'health'
                self.mind[self.old_y][self.old_x] = 5
                self.maze[self.old_y][self.old_x] = 0
                self.health += 1
                if self.back is False:
                    self.stack.append(self.old_x)
                    self.stack.append(self.old_y)
            elif self.maze[self.yPosition + 1][self.xPosition] == 4:
                if self.maze[self.yPosition + 1][self.xPosition - 1] == 0:
                    if self.maze[self.yPosition][self.xPosition - 1] == 0:
                        if self.last_direction == 'right':
                            print("Backtracking!")
                            self.yPosition = self.stack.pop()
                            self.xPosition = self.stack.pop()
                            self.r = 3
                            self.put_result('success')
                            self.last_result = 'success'
                            print("Avoiding Poison")
                            self.mind[self.old_y][self.old_x] = 9
                            self.maze[self.old_y][self.old_x] = 0
                        else:
                            self.r = 3
                            self.xPosition -= 1
                            self.put_result('success')
                            self.last_result = 'success'
                            print("Avoiding Poison")
                            self.mind[self.old_y][self.old_x] = 9
                            self.maze[self.old_y][self.old_x] = 0
                            if self.back is False:
                                self.stack.append(self.old_x)
                                self.stack.append(self.old_y)
                    else:
                        self.yPosition += 1
                        self.put_result('poison')
                        self.last_result = 'poison'
                        self.mind[self.old_y][self.old_x] = 4
                        self.maze[self.old_y][self.old_x] = 0
                        self.health -= 1
                        if self.back is False:
                            self.stack.append(self.old_x)
                            self.stack.append(self.old_y)
                elif self.maze[self.yPosition + 1][self.xPosition + 1] == 0:
                    if self.maze[self.yPosition][self.xPosition + 1] == 0:
                        if self.last_direction == 'left':
                            print("Backtracking!")
                            self.yPosition = self.stack.pop()
                            self.xPosition = self.stack.pop()
                            self.r = 4
                            self.put_result('success')
                            self.last_result = 'success'
                            print ("Avoiding Poison")
                            self.mind[self.old_y][self.old_x] = 9
                            self.maze[self.old_y][self.old_x] = 0
                        else:
                            self.r = 4
                            self.xPosition += 1
                            self.put_result('success')
                            self.last_result = 'success'
                            print ("Avoiding Poison")
                            self.mind[self.old_y][self.old_x] = 9
                            self.maze[self.old_y][self.old_x] = 0
                            if self.back is False:
                                self.stack.append(self.old_x)
                                self.stack.append(self.old_y)
                    else:
                        self.yPosition += 1
                        self.put_result('poison')
                        self.last_result = 'poison'
                        self.mind[self.old_y][self.old_x] = 4
                        self.maze[self.old_y][self.old_x] = 0
                        self.health -= 1
                        if self.back is False:
                            self.stack.append(self.old_x)
                            self.stack.append(self.old_y)
                else:
                    self.yPosition += 1
                    self.put_result('poison')
                    self.last_result = 'poison'
                    self.mind[self.old_y][self.old_x] = 4
                    self.maze[self.old_y][self.old_x] = 0
                    self.health -= 1
                    if self.back is False:
                        self.stack.append(self.old_x)
                        self.stack.append(self.old_y)
            else:
                self.yPosition += 1
                self.put_result('success')
                self.last_result = 'success'
                self.mind[self.old_y][self.old_x] = 9
                self.maze[self.old_y][self.old_x] = 0
                if self.back is False:
                    self.stack.append(self.old_x)
                    self.stack.append(self.old_y)

        elif self.directions[self.r] == 'right':
            if self.maze[self.yPosition][self.xPosition + 1] == 1:  # Checks for a wall
                self.put_result('wall')
                self.last_result = 'wall'
                self.mind[self.yPosition][self.xPosition + 1] = 1
            elif self.maze[self.yPosition][self.xPosition + 1] == 5:  # Checks for health
                self.xPosition += 1
                self.put_result('health')
                self.last_result = 'health'
                self.mind[self.old_y][self.old_x] = 5
                self.maze[self.old_y][self.old_x] = 0
                self.health += 1
                if self.back is False:
                    self.stack.append(self.old_x)
                    self.stack.append(self.old_y)
            elif self.maze[self.yPosition][self.xPosition + 1] == 4:  # Checks for poison
                if self.maze[self.yPosition - 1][self.xPosition + 1] == 0:
                    if self.maze[self.yPosition - 1][self.xPosition] == 0:
                        if self.last_direction == 'down':
                            print("Backtracking!")
                            self.yPosition = self.stack.pop()
                            self.xPosition = self.stack.pop()
                            self.r = 2
                            self.put_result('success')
                            self.last_result = 'success'
                            print("Avoiding Poison")
                            self.mind[self.old_y][self.old_x] = 9
                            self.maze[self.old_y][self.old_x] = 0
                        else:
                            self.r = 2
                            self.yPosition -= 1
                            self.put_result('success')
                            self.last_result = 'success'
                            print("Avoiding Poison")
                            self.mind[self.old_y][self.old_x] = 9
                            self.maze[self.old_y][self.old_x] = 0
                            if self.back is False:
                                self.stack.append(self.old_x)
                                self.stack.append(self.old_y)
                    else:
                        self.xPosition += 1
                        self.put_result('poison')
                        self.last_result = 'poison'
                        self.mind[self.old_y][self.old_x] = 4
                        self.maze[self.old_y][self.old_x] = 0
                        self.health -= 1
                        if self.back is False:
                            self.stack.append(self.old_x)
                            self.stack.append(self.old_y)
                elif self.maze[self.yPosition + 1][self.xPosition + 1] == 0:
                    if self.maze[self.yPosition + 1][self.xPosition] == 0:
                        if self.last_direction == 'up':
                            print("Backtracking!")
                            self.yPosition = self.stack.pop()
                            self.xPosition = self.stack.pop()
                            self.r = 1
                            self.put_result('success')
                            self.last_result = 'success'
                            print ("Avoiding Poison")
                            self.mind[self.old_y][self.old_x] = 9
                            self.maze[self.old_y][self.old_x] = 0
                        else:
                            self.r = 1
                            self.yPosition += 1
                            self.put_result('success')
                            self.last_result = 'success'
                            print ("Avoiding Poison")
                            self.mind[self.old_y][self.old_x] = 9
                            self.maze[self.old_y][self.old_x] = 0
                            if self.back is False:
                                self.stack.append(self.old_x)
                                self.stack.append(self.old_y)
                    else:
                        self.xPosition += 1
                        self.put_result('poison')
                        self.last_result = 'poison'
                        self.mind[self.old_y][self.old_x] = 4
                        self.maze[self.old_y][self.old_x] = 0
                        self.health -= 1
                        if self.back is False:
                            self.stack.append(self.old_x)
                            self.stack.append(self.old_y)
                else:
                    self.xPosition += 1
                    self.put_result('poison')
                    self.last_result = 'poison'
                    self.mind[self.old_y][self.old_x] = 4
                    self.maze[self.old_y][self.old_x] = 0
                    self.health -= 1
                    if self.back is False:
                        self.stack.append(self.old_x)
                        self.stack.append(self.old_y)
            else:
                self.xPosition += 1
                self.put_result('success')
                self.last_result = 'success'
                self.mind[self.old_y][self.old_x] = 9
                self.maze[self.old_y][self.old_x] = 0
                if self.back is False:
                    self.stack.append(self.old_x)
                    self.stack.append(self.old_y)

        elif self.directions[self.r] == 'left':
            if self.maze[self.yPosition][self.xPosition - 1] == 1:  # Checks for a wall
                self.put_result('wall')
                self.last_result = 'wall'
                self.mind[self.yPosition][self.xPosition - 1] = 1
            elif self.maze[self.yPosition][self.xPosition - 1] == 5:  # Checks for a health
                self.xPosition -= 1
                self.put_result('health')
                self.last_result = 'health'
                self.mind[self.old_y][self.old_x] = 5
                self.maze[self.old_y][self.old_x] = 0
                self.health += 1
                if self.back is False:
                    self.stack.append(self.old_x)
                    self.stack.append(self.old_y)

            elif self.maze[self.yPosition][self.xPosition - 1] == 4:  # Checks for poison
                if self.maze[self.yPosition + 1][self.xPosition - 1] == 0:
                    if self.maze[self.yPosition + 1][self.xPosition] == 0:
                        if self.last_direction == 'up':
                            print("Backtracking!")
                            self.yPosition = self.stack.pop()
                            self.xPosition = self.stack.pop()
                            self.r = 1
                            self.put_result('success')
                            self.last_result = 'success'
                            print("Avoiding Poison")
                            self.mind[self.old_y][self.old_x] = 9
                            self.maze[self.old_y][self.old_x] = 0
                        else:
                            self.r = 1
                            self.yPosition += 1
                            self.put_result('success')
                            self.last_result = 'success'
                            print("Avoiding Poison")
                            self.mind[self.old_y][self.old_x] = 9
                            self.maze[self.old_y][self.old_x] = 0
                            if self.back is False:
                                self.stack.append(self.old_x)
                                self.stack.append(self.old_y)
                    else:
                        self.xPosition -= 1
                        self.put_result('poison')
                        self.last_result = 'poison'
                        self.mind[self.old_y][self.old_x] = 4
                        self.maze[self.old_y][self.old_x] = 0
                        self.health -= 1
                        if self.back is False:
                            self.stack.append(self.old_x)
                            self.stack.append(self.old_y)
                elif self.maze[self.yPosition - 1][self.xPosition - 1] == 0:
                    if self.maze[self.yPosition - 1][self.xPosition] == 0:
                        if self.last_direction == 'down:':
                            print("Backtracking!")
                            self.yPosition = self.stack.pop()
                            self.xPosition = self.stack.pop()
                            self.r = 2
                            self.put_result('success')
                            self.last_result = 'success'
                            print ("Avoiding Poison")
                            self.mind[self.old_y][self.old_x] = 9
                            self.maze[self.old_y][self.old_x] = 0
                        else:
                            self.r = 2
                            self.yPosition -= 1
                            self.put_result('success')
                            self.last_result = 'success'
                            print ("Avoiding Poison")
                            self.mind[self.old_y][self.old_x] = 9
                            self.maze[self.old_y][self.old_x] = 0
                            if self.back is False:
                                self.stack.append(self.old_x)
                                self.stack.append(self.old_y)
                    else:
                        self.xPosition -= 1
                        self.put_result('poison')
                        self.last_result = 'poison'
                        self.mind[self.old_y][self.old_x] = 4
                        self.maze[self.old_y][self.old_x] = 0
                        self.health -= 1
                        if self.back is False:
                            self.stack.append(self.old_x)
                            self.stack.append(self.old_y)
                else:
                    self.xPosition -= 1
                    self.put_result('poison')
                    self.last_result = 'poison'
                    self.mind[self.old_y][self.old_x] = 4
                    self.maze[self.old_y][self.old_x] = 0
                    self.health -= 1
                    if self.back is False:
                        self.stack.append(self.old_x)
                        self.stack.append(self.old_y)
            else:
                self.xPosition -= 1
                self.put_result('success')
                # Reset previous maze position to 1
                self.maze[self.old_y][self.old_x] = 0
                self.last_result = 'success'
                self.mind[self.old_y][self.old_x] = 9
                if self.back is False:
                    self.stack.append(self.old_x)
                    self.stack.append(self.old_y)

        elif self.directions[self.r] == 'wait':
            self.put_result('success')
            self.last_result = 'success'

        # update last direction to be the one just selected
        self.last_direction = self.directions[self.r]
        return self.directions[self.r]

    # Save the result
    def put_result(self, result):
        self.last_result = result

    # Create the "mind" array for the agent to remember where it has been
    def MakeMind(self):
        for row in range(self.mazeHeight):
            self.mind.append([])
            for column in range(self.mazeWidth):
                self.mind[row].append(0)

    # Allows the agent to run a second time utilizing the information learned in the first run.
    def ReRun(self):
        if self.count2 == 0:
            self.nextY = self.rev.pop()
            self.nextX = self.rev.pop()
        self.nextY = self.rev.pop()
        self.nextX = self.rev.pop()
        if self.yPosition is self.nextY + 1:
            r = 1
        elif self.yPosition is self.nextY - 1:
            r = 2
        elif self.xPosition is self.nextX + 1:
            r = 4
        elif self.xPosition is self.nextX - 1:
            r = 3
        else:
            r = 0
        if r != 0:
            self.checkPortal2()
            self.last_direction = self.directions[r]
        print("[", self.xPosition, ", ", self.yPosition, "]")
        print("Re-Run Decision: ", self.last_direction)
        print("Re-Run Result: ",  self.last_result)
        print("Health: ", self.health)
        print(self.count2, " Move(s) made\n")
        self.maze[self.yPosition][self.xPosition] = 0
        self.xPosition = self.nextX
        self.yPosition = self.nextY
        self.maze[self.yPosition][self.xPosition] = 2
        Voldemort.count2 += 1
        if self.runSecond == False:
            print("Success! Portal found in ", self.count2, " moves.")
            print("The first run found the portal in ", self.num, " moves. The second run found the portal in ", self.count2," moves")

    # Reverse the stack to start at the beginning
    def FillStack(self):
        while self.stack:
            self.counter += 1
            self.y = self.stack.pop()
            self.x = self.stack.pop()
            self.rev.append(self.x)
            self.rev.append(self.y)

    # Check if finished
    def checkPortal(self):
        if self.xPosition == self.randPortalX and self.yPosition == self.randPortalY:
            self.put_result('portal')
            self.runFirst = False
            self.stack.append(self.xPosition)
            self.stack.append(self.yPosition)

    def checkPortal2(self):
        if self.nextX == self.randPortalX and self.nextY == self.randPortalY:
            self.put_result('portal')
            self.runSecond = False
        else:
            self.put_result('success')

    def runIntelligence(self):
        # Random Starting Point
        self.maze[self.yPosition][self.xPosition] = 2
        self.get_decision()
        self.checkPortal()
        self.num += 1
        self.maze[self.yPosition][self.xPosition] = 2

        print("[", self.xPosition, ", ", self.yPosition, "]")
        print("Decision: ", self.last_direction)
        print("Result: ", self.last_result)
        print("Health: ", self.health)
        print(self.num, " Move(s) made\n")
        # Ends the first run
        if self.runFirst == False:
            print("Success! Portal found in ", Voldemort.num, " moves.")

    def initReRun(self):
        # Inverse the "mind" list to start at the beginning of the run
        self.FillStack()
        self.runSecond = True

        # Reposition the agent and the positions of x and y to the initial position
        self.maze[self.initY][self.initX] = 2
        self.yPosition = self.initY
        self.xPosition = self.initX

        # Reposition the Portal
        self.maze[self.randPortalY][self.randPortalX] = 3

    def runProg(self, mazeWidth, mazeHeight):
        if self.runFirst is True:
            if self.setFirst is False:
                self.initialize(mazeWidth, mazeHeight)
                self.setFirst = True
            self.runIntelligence()
        else:
            if self.setSecond is False:
                self.initReRun()
                self.setSecond = True
            self.ReRun()

    def vision(self):
        p = -1
        h = -1
        if self.maze[self.yPosition][self.xPosition + 1] != 0:
            if self.maze[self.yPosition][self.xPosition + 1] == 1:
                print("There is a wall to my right!")
                self.mind[self.yPosition][self.xPosition + 1] = 1
            elif self.maze[self.yPosition][self.xPosition + 1] == 3:
                print("The portal is to my right!")
                p = 4
            elif self.maze[self.yPosition][self.xPosition + 1] == 5:
                self.mind[self.yPosition][self.xPosition + 1] = 5
                print("Health is to my right!")
                h = 4

        if self.maze[self.yPosition][self.xPosition - 1] != 0:
            if self.maze[self.yPosition][self.xPosition - 1] == 1:
                print("There is a wall to my left!")
                self.mind[self.yPosition][self.xPosition - 1] = 1
            elif self.maze[self.yPosition][self.xPosition - 1] == 3:
                print("The portal is to my left!")
                p = 3
            elif self.maze[self.yPosition][self.xPosition - 1] == 5:
                self.mind[self.yPosition][self.xPosition - 1] = 5
                print("Health is to my left!")
                h = 3

        if self.maze[self.yPosition + 1][self.xPosition] != 0:
            if self.maze[self.yPosition + 1][self.xPosition] == 1:
                print("There is a wall one step down!")
                self.mind[self.yPosition + 1][self.xPosition] = 1
            elif self.maze[self.yPosition + 1][self.xPosition] == 3:
                print("The portal is one step down!")
                p = 1
            elif self.maze[self.yPosition + 1][self.xPosition] == 5:
                print("Health is one step down!")
                self.mind[self.yPosition + 1][self.xPosition] = 5
                h = 1

        if self.maze[self.yPosition - 1][self.xPosition] != 0:
            if self.maze[self.yPosition - 1][self.xPosition] == 1:
                print("There is a wall one step up!")
                self.mind[self.yPosition - 1][self.xPosition] = 1
            elif self.maze[self.yPosition - 1][self.xPosition ] == 3:
                print("The portal is one step up!")
                p = 2
            elif self.maze[self.yPosition - 1][self.xPosition] == 5:
                self.mind[self.yPosition - 1][self.xPosition] = 5
                print("Health is one step up!")
                h = 2

        if self.maze[self.yPosition + 1][self.xPosition + 1] != 0:
            if self.maze[self.yPosition + 1][self.xPosition + 1] == 1:
                print("There is a wall in my adjacent lower right block!")
                self.mind[self.yPosition + 1][self.xPosition + 1] = 1
            elif self.maze[self.yPosition + 1][self.xPosition + 1] == 3:
                print("The portal is in my adjacent lower right block!")
                if self.maze[self.yPosition][self.xPosition + 1] == 1:
                    p = 1
                else:
                    p = 4
            elif self.maze[self.yPosition + 1][self.xPosition + 1] == 5:
                print("Health is in my adjacent lower right block!")
                self.mind[self.yPosition + 1][self.xPosition + 1] = 5
                if self.maze[self.yPosition][self.xPosition + 1] == 1:
                    h = 1
                else:
                    h = 4

        if self.maze[self.yPosition + 1][self.xPosition - 1] != 0:
            if self.maze[self.yPosition + 1][self.xPosition - 1] == 1:
                print("There is a wall in my adjacent lower left block!")
                self.mind[self.yPosition + 1][self.xPosition - 1] = 1
            elif self.maze[self.yPosition + 1][self.xPosition - 1] == 3:
                print("The portal is to my adjacent lower left!")
                if self.maze[self.yPosition][self.xPosition - 1] == 1:
                    p = 1
                else:
                    p = 3
            elif self.maze[self.yPosition + 1][self.xPosition - 1] == 5:
                print("Health is to my adjacent lower left!")
                self.mind[self.yPosition + 1][self.xPosition - 1] = 5
                if self.maze[self.yPosition][self.xPosition - 1] == 1:
                    h = 1
                else:
                    h = 3

        if self.maze[self.yPosition - 1][self.xPosition + 1] != 0:
            if self.maze[self.yPosition - 1][self.xPosition + 1] == 1:
                print("There is a wall in my adjacent upper right block!")
                self.mind[self.yPosition - 1][self.xPosition + 1] = 1
            elif self.maze[self.yPosition - 1][self.xPosition + 1] == 3:
                print("The portal is in my adjacent upper right block!")
                if self.maze[self.yPosition][self.xPosition + 1] == 1:
                    p = 2
                else:
                    p = 4
            elif self.maze[self.yPosition - 1][self.xPosition + 1] == 5:
                print("Health is in my adjacent upper right block!")
                self.mind[self.yPosition - 1][self.xPosition + 1] = 5
                if self.maze[self.yPosition][self.xPosition + 1] == 1:
                    h = 2
                else:
                    h = 4

        if self.maze[self.yPosition - 1][self.xPosition - 1] != 0:
            if self.maze[self.yPosition - 1][self.xPosition - 1] == 1:
                print("There is a wall in my adjacent upper left block!")
                self.mind[self.yPosition - 1][self.xPosition - 1] = 1
            elif self.maze[self.yPosition - 1][self.xPosition - 1] == 3:
                print("The portal is in my adjacent upper left block")
                if self.maze[self.yPosition][self.xPosition - 1] == 1:
                    p = 2
                else:
                    p = 3
            elif self.maze[self.yPosition - 1][self.xPosition - 1] == 5:
                print("Health is in my adjacent upper left block")
                self.mind[self.yPosition - 1][self.xPosition - 1] = 5
                if self.maze[self.yPosition][self.xPosition - 1] == 1:
                    h = 2
                else:
                    h = 3

        if p >= 0:
            self.r = p
            self.choice = True
        elif h >= 0:
            self.r = h
            self.choice = True


# Set the size of the grid
mazeWidth = 20
mazeHeight = 20

#  Set the size of the cells and the cushion between
margin = 5
width = 25
height = 25
value = 5

#  Find the window size
x = mazeWidth * 30 + 5
y = mazeHeight * 30 + 5 + 35
w_size = [x, y]

pygame.init()  # everything below .init() and .quit() runs with pygame
win = pygame.display.set_mode(w_size)  # creates size of window x and y
pygame.display.set_caption('The Brainy Bunch')

#  Set colors to be used
white = (255, 255, 255)
green = (0, 255, 0)
black = (0, 0, 0)
purple = (128, 0, 128)
red = (255, 0, 0)
blue = (0, 0, 255)
orange =(255, 165, 0)
yellow = (255, 255, 0)
# create and initialize an object called Voldemort
Voldemort = DecisionFactory()


while Voldemort.runSecond and Voldemort.health > 0:
    Voldemort.runProg(mazeWidth, mazeHeight)
    win.fill(black)
    pygame.time.delay(100)
    # pygame.font.init()

    # font = pygame.font.SysFont('Comic Sans MS', 32)
    # health = "health: " + str(Voldemort.health)
    # text1 = font.render(health, True, green, blue)
    # textRect = text1.get_rect()
    # textRect.center = (730, 780)
    # win.blit(text1, textRect)

    for event in pygame.event.get():
        # This checks if the X close button is pressed to end the while loop
        if event.type == pygame.QUIT:
            run = False
            # deactivates the pygame library
            pygame.quit()
            # quit the program.
            quit()

    # pygame.display.update()

    if Voldemort.runFirst is True:
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
                pygame.draw.rect(win, color, [(margin + width) * column + margin, (margin + height) * row + margin,
                                          width, height])
    else:
        for row in range(Voldemort.mazeHeight):
            for column in range(Voldemort.mazeWidth):
                color = white
                if Voldemort.maze[row][column] == 1:
                    color = blue
                elif Voldemort.maze[row][column] == 2:
                    color = red
                elif Voldemort.maze[row][column] == 3:
                    color = purple
                elif Voldemort.maze[row][column] == 4:
                    color = black
                elif Voldemort.maze[row][column] == 5:
                    color = yellow
                pygame.draw.rect(win, color, [(margin + width) * column + margin, (margin + height) * row + margin,
                                      width, height])

    pygame.display.update()
    
if Voldemort.health == 0:
    print("The intelligence died!")

pygame.quit()
