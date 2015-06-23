# 6.00.2x Problem Set 2: Simulating robots

import math
import random
import pylab
import ps2_visualize
from ps2_verify_movement27 import testRobotMovement



class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        Given an Int, angle - representing angle in degrees, 0 <= angle < 360
        Given a Float, speed - positive float representing speed
        Returns a Position - represents the new position
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)



class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.totalTiles = width * height
        self.cleanTiles = []
    
    def cleanTileAtPosition(self, pos):
        """
        Given a Position - sets the tile at pos as cleaned
        also assumes that pos represents a valid position inside this room
        """
        x = int(math.floor(pos.getX()))
        y = int(math.floor(pos.getY()))
        if self.isTileCleaned(x, y) != True:
            strPos = "(" + str(x) + ", " + str(y) + ")"
            self.cleanTiles.append(strPos)

    def isTileCleaned(self, m, n):
        """
        Given two Ints, Returns a Boolean - true if the tile has been cleaned, false if not
        also assumes that (m, n) represents a valid tile inside the room
        """
        if len(self.cleanTiles) == 0:
            return False
        else:
            strPos = "(" + str(m) + ", " + str(n) + ")"
            for c in range(len(self.cleanTiles)):
                if self.cleanTiles[c] == strPos:
                    return True
            return False
    
    def getNumTiles(self):
        """
        Returns an Int - the total number of tiles in the room
        """
        return self.totalTiles


    def getNumCleanedTiles(self):
        """
        Returns an Int - the total number of clean tiles in the room
        """
        return len(self.cleanTiles)

    def getRandomPosition(self):
        """
        Return a Position - a random position inside the room.
        """
        x = random.random() * self.width
        y = random.random() * self.height
        pos = Position(x, y)
        if self.isPositionInRoom(pos):
            return pos
        else:
            raise ValueError('a new random position was not inside the room')

    def isPositionInRoom(self, pos):
        """
        Given a Position, Returns a Boolean - true if inside the room, false if not
        """
        x = pos.getX()
        y = pos.getY()
        if x < 0 or x >= self.width:
            return False
        else:
            if y < 0 or y >= self.height:
                return False
            else:
                return True



class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        Given a RectangularRoom, room 
        Given a Float, speed - where speed > 0        
        """
        self.room = room
        self.speed = speed
        intPos = room.getRandomPosition()
        room.cleanTileAtPosition(intPos)
        self.direction = random.randint(0,359)
        self.currentPos = intPos

    def getRobotPosition(self):
        """
        Returns a Position - the robot's position
        """
        return self.currentPos
        
    def getRobotDirection(self):
        """
        Returns an Int - the direction of the robot as an angle in degrees
        """
        return self.direction 

    def setRobotPosition(self, position):
        """
        Given a Position - sets the position of the robot to POSITION
        """
        self.currentPos = position

    def setRobotDirection(self, direction):
        """
        Given an Int - sets the direction of the robot to DIRECTION, an angle in degrees
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.
        Move the robot to a new position and mark the tile it is on as having been cleaned.
        """
        raise NotImplementedError # don't change this!



class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        tempPos = self.currentPos
        newPos = tempPos.getNewPosition(self.direction, self.speed)
        while self.room.isPositionInRoom(newPos) != True:
            self.setRobotDirection(random.randint(0,359))
            newPos = tempPos.getNewPosition(self.direction, self.speed)            
        self.currentPos = newPos
        self.room.cleanTileAtPosition(newPos)



class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new random direction at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        tempPos = self.currentPos
        self.setRobotDirection(random.randint(0,359))
        newPos = tempPos.getNewPosition(self.direction, self.speed)
        while self.room.isPositionInRoom(newPos) != True:
            self.setRobotDirection(random.randint(0,359))
            newPos = tempPos.getNewPosition(self.direction, self.speed)            
        self.currentPos = newPos
        self.room.cleanTileAtPosition(newPos)










def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots, width, height, num_trials all Ints > 0
    speed is a Float > 0 and min_coverage is a float between 0 and 1 inclusive
    robot_type: robot class to be instantiated (e.g. StandardRobot or RandomWalkRobot)
    """
    timeSteps = []
    averageClean = 0.0
    for t in range(num_trials):
        thisRoom = RectangularRoom(width, height)
        robots = []
        timesteps = 0

        for i in range(num_robots):
            robots.append(robot_type(thisRoom, speed))

        #anim = ps2_visualize.RobotVisualization(num_robots, width, height)
        #anim.update(thisRoom, robots)
                                    
        current = float(thisRoom.getNumCleanedTiles()) / float(thisRoom.getNumTiles())
        while current < min_coverage: 
            for x in range(len(robots)):
                robots[x].updatePositionAndClean()
            #anim.update(thisRoom, robots)
            timesteps += 1
            current = float(thisRoom.getNumCleanedTiles()) / float(thisRoom.getNumTiles())     

        timeSteps.append(timesteps)
    
    #anim.done()    
    averageClean = float(sum(timeSteps)) / float(num_trials)    
    return averageClean

#runSimulation(1, 1.0, 10, 12, 0.75, 1, StandardRobot)
#runSimulation(2, 1.0, 6, 6, 0.95, 1, RandomWalkRobot)

#testRobotMovement(StandardRobot, RectangularRoom)

def showPlot1(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print "Plotting", num_robots, "robots..."
        times1.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
        times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

showPlot1("Time It Takes 1 - 10 Robots To Clean 80% Of A Room", "Number of Robots", "Time-steps")

def showPlot2(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300/width
        print "Plotting cleaning time for a room of width:", width, "by height:", height
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 200, StandardRobot))
        times2.append(runSimulation(2, 1.0, width, height, 0.8, 200, RandomWalkRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    
#showPlot2("Time It Takes Two Robots To Clean 80% Of Variously Shaped Rooms", "Aspect Ratio", "Time-steps")