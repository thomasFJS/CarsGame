import pygame, random, sys ,os,time
from pygame.locals import *

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 60
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 8
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 20
PLAYERMOVERATE = 5
count=10

def quit():
    pygame.quit()
    sys.exit()

def waitKeyPress():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: #escape quits
                    quit()
                return

def playerHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('car race')
pygame.mouse.set_visible(False)

# fonts
font = pygame.font.SysFont(None, 30)

# set images
playerImage = pygame.image.load('image/car1.png')
baddie1 = pygame.image.load('image/car2.png')
baddie2 = pygame.image.load('image/car3.png')
baddie3 = pygame.image.load('image/car4.png')

images = [baddie1,baddie2, baddie3]
wallLeft = pygame.image.load('image/left.png')
wallRight = pygame.image.load('image/right.png')

# player size
playerRect = playerImage.get_rect()

# home screen
drawText('Press any key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3))
drawText('And Enjoy', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3)+30)
pygame.display.update()
waitKeyPress()
while (count>0):
    # start of the game
    baddies = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    baddieAddCounter = 0


    while True: # the game loop
        score += 1 # increase score

        for event in pygame.event.get():
            
            if event.type == QUIT:
                quit()

            if event.type == KEYDOWN:
                #directions
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                #quit
                if event.key == ord('q'):
                        quit()
            
                #directions
                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

            

        # Add new baddies at the top of the scree
        baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize =30 
            newBaddie = {'rect': pygame.Rect(random.randint(140, 485), 0 - baddieSize, 23, 47),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface':pygame.transform.scale(random.choice(images), (23, 47)),
                        }
            baddies.append(newBaddie)
            sideLeft= {'rect': pygame.Rect(0,0,126,600),
                       'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                       'surface':pygame.transform.scale(wallLeft, (126, 599)),
                       }
            baddies.append(sideLeft)
            sideRight= {'rect': pygame.Rect(497,0,303,600),
                       'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                       'surface':pygame.transform.scale(wallRight, (303, 599)),
                       }
            baddies.append(sideRight)
        
            
        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)
        
         
        for b in baddies[:]:
            b['rect'].move_ip(0, b['speed'])
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        # Draw the game on the window.
        windowSurface.fill(BACKGROUNDCOLOR)

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 128, 0)
        drawText('Rest Life: %s' % (count), font, windowSurface,128, 40)
        
        windowSurface.blit(playerImage, playerRect)

        
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Check if any of the car have hit the player.
        if playerHitBaddie(playerRect, baddies):
            break

        mainClock.tick(FPS)

    # "Game Over" screen.
    count=count-1
    time.sleep(1)
    if (count==0):
     drawText('Game over', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
     drawText('Press any key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 30)
     pygame.display.update()
     time.sleep(2)
     waitForPlayerToPressKey()
     count=3
