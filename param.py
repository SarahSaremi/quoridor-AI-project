import pygame

windowWidth = 705
windowHeight = 705
backGroundColor = (102, 42, 42)
squareLighterColor = (176, 70, 44)
squareDarkerColorColor = (176, 70, 44)
rangeColor = (30, 255, 109)
player1moves = (122, 122, 122)
player2moves = (100, 100, 122)
player3moves = (50, 60, 70)
player4moves = (83, 2, 122)
playerOneColor = (226, 91, 88)
playerTwoColor = (250, 181, 28)
playerThreeColor = (0, 255, 0)
playerFourColor = (76, 0, 150)
wallColor = (255, 228, 159)
squareSize = 45
margin = 10
beamRadius = int(squareSize / 3)
rectangle_draging = False

# assets
playerImg1 = pygame.image.load('player1.png')
playerImg2 = pygame.image.load('player2.png')
playerImg3 = pygame.image.load('player3.png')
playerImg4 = pygame.image.load('player4.png')

miniMaxDepth = 3
initialAlpha = -1000
initialBeta = +1000
initialMaxEval = -1000
initialMinEval = 1000
wallRangeCheck = 1
numberOfRows = 17
numberOfHeuristicComponents = 4

finalc1 = 0.2534474322446254
finalc2 = 0.5669233076022984
finalc3 = 0.6951495873044347
finalc4 = 0.18851450511603118

exploredSetPlayer1 = set()
exploredSetPlayer2 = set()

initialNumberOfPopulation = 12
initialNumberOfGenerations = 15
initialNumberOfleagues = 3