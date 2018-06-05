import matplotlib.pyplot as plt
import matplotlib.image as mpimg
#import sys, termios, tty, os, time
import keyboard
import gc
import os
import re
import sys

blue = 'images/blue/'
red = 'images/red/'
common = 'images/common/'
move = 0
state = 0
maxrounds = 0

"Console.txt path array"
path = []
"Dynamic object array which will hold all the images"
ax = []

def pressedKey(e):
    global move
    
    if (keyboard.is_pressed('up')):
        os._exit(0)
    elif (keyboard.is_pressed('left')):
        move = -1
    elif (keyboard.is_pressed('right')):
        move = 1
    elif (keyboard.is_pressed('down')):
        move = 99
        
    return move

def readFiles():
    
    "Create directory listing of all player A's Console.txt files"
    evens = 0
    
    for dirpath, dirs, files in os.walk(".\Logs"):
        if (len(files) >= 3):        
            if (evens % 2 == 0):
                    #maps.append(files[2])
                    path.append(dirpath + '\Console\Console.txt')
                    #print(path[0])                
            evens += 1        
        #print(files)
       
    
    return None
    
def prepDisplay():
    
    "Start interactive figure viewer"
    plt.ion()
    fig = plt.figure('Viewer')
    
    plt.suptitle("Press the up arrow to end program\n\nPress left arrow to pause")
    plt.show()
    plt.pause(1e-6)

    "Generate sub-plot window objects for ax[] array."
    "The extra line is to prevent pictures from being displayed behind the player scores"
    for plotPos in range(9*16):        
        ax.append(fig.add_subplot(9, 16, plotPos + 1))
        
    "Hide the top row image subplots that are behind the player score text"    
    for top_row in range(16):
        ax[top_row].axis("off") 
    
    return None    
    
def display(f):
 
    global move 
    
    move = 0
 
    #while True:
        #if (keyboard.is_pressed('c')):
            #break
        #elif (keyboard.is_pressed('f')):

    
    file = open(path[f], 'r')
    lines = list(file)
       
    maps = []
        
    for i in range(8):
        left = -1    
        for j in range(16):
            left = lines[3 + i].find('[', left + 1)
            right = lines[3 + i].find(']', left + 1)
            tr = re.sub(r'\d+', '', lines[3 + i][left + 1:right])
            maps.append(tr)
    

              
    for plotPos in range(8*16): 
        
        if (int(plotPos / 8) % 2 == 0):
            colour = blue
        else:
            colour = red
            
        if (maps[plotPos].count('A') >= 1):
            ax[plotPos + 16].imshow(mpimg.imread(colour + 'A.jpg'))
        elif (maps[plotPos].count('a') >= 1):
            ax[plotPos + 16].imshow(mpimg.imread(colour + 'ab.jpg'))
        elif (maps[plotPos].count('E') >= 1):
            ax[plotPos + 16].imshow(mpimg.imread(colour + 'E.jpg'))
        elif (maps[plotPos].count('e') >= 1):
            ax[plotPos + 16].imshow(mpimg.imread(colour + 'eb.jpg')) 
        elif (maps[plotPos].count('D') >= 1):
            ax[plotPos + 16].imshow(mpimg.imread(colour + 'D.jpg'))
        elif (maps[plotPos].count('d') >= 1):
            ax[plotPos + 16].imshow(mpimg.imread(colour + 'db.jpg'))
        elif (maps[plotPos].count('>') == 1):
            ax[plotPos + 16].imshow(mpimg.imread(common + 'right.jpg'))
        elif (maps[plotPos].count('>') > 1):
            ax[plotPos + 16].imshow(mpimg.imread(common + 'rightRight.jpg'))
        elif (maps[plotPos].count('<') == 1):
            ax[plotPos + 16].imshow(mpimg.imread(common + 'left.jpg'))
        elif (maps[plotPos].count('<') > 1):
            ax[plotPos + 16].imshow(mpimg.imread(common + 'leftLeft.jpg'))
        elif ((maps[plotPos].count('>') >= 1) and (maps[plotPos].count('<') >= 1)):
            ax[plotPos + 16].imshow(mpimg.imread(common + 'leftAndRight.jpg'))    
        else:
            ax[plotPos + 16].imshow(mpimg.imread(common + 'N.jpg')) 
        
        #ax[plotPos + 16].axis("off")
        ax[plotPos + 16].xaxis.set_major_locator(plt.NullLocator())
        ax[plotPos + 16].yaxis.set_major_locator(plt.NullLocator())

        
        
    plt.suptitle("Round " + str(f) + " / " + str(maxrounds - 1) + '\n\n' + lines[1] + '\n' + lines[2])
    plt.plot()
    plt.pause(1e-6)
    
    
    
    file.close()
    
    gc.collect()
    


    return None


"================================ Main ========================================"
keyboard.hook(pressedKey)

readFiles()
prepDisplay()

maxrounds = len(path)
         
for f in range(maxrounds):
    if (move == -1):
        display(f)
        input("Press Enter to continue...")
    else:
        display(f)
    
plt.close()
