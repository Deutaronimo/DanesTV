import os
import random
import vlc
import time
from subprocess import call
from collections import deque

# Add this in for raspberry Pi GPIO
from gpiozero import RotaryEncoder, Button 

adsBetweenVideos = 3
adsCounter       = 0

playerIsRunning = True

# Lists
startingList = []
adsList      = []
movieList    = []

# Paths
moviePath    = '/home/dane/storage2/TARENTINO/MOVIE'
adsPath      = '/home/dane/storage2/TARENTINO/AD'

# Button and encoder settings
rotor         = RotaryEncoder(17, 18, wrap=True)
buttonEncoder = Button(22, pull_up = False, bounce_time = None)
buttonSide    = Button(27, pull_up = False, bounce_time = .1)
 

#main VLC player class
class Player():
    def __init__(self):
        self._instance = vlc.Instance()
        self._player = self._instance.media_player_new()
        self._player.set_fullscreen(False)
        self._player.video_set_aspect_ratio("2.21:1")
        self._player.video_set_scale(0)
        self.videoList   = []
        self.currentShow = ''
        self.videoIndex  = 0
        self.folderList  = []
        self.showList    = []
        self.isPlaying = True
        self._player.audio_set_volume(100)

    def stop(self):
        self._player.stop()
        self.isPlaying = False

        # Takes a list and selects a random show
    def playRandomShowFromList(self, _videoList):
        self.videoList   = _videoList
        print(_videoList)
        self.currentShow = random.choice(self.videoList)
        media = self._instance.media_new(self.currentShow)
        self._player.set_media(media)
        self._player.play()

        # switch to next or previous show from current list
    def playNextShow(self):
        self._player.stop()
        self.videoIndex = self.videoList.index(self.currentShow)
        self.videoIndex = self.videoIndex + 1

        if self.videoIndex > (len(self.videoList))-1:
            self.videoIndex = 1

        self.currentShow = self.videoList[self.videoIndex]
        media = self._instance.media_new(self.currentShow)
        self._player.set_media(media)
        self._player.play()

    def playPreviousShow(self):
        self._player.stop()
        self.videoIndex = self.videoList.index(self.currentShow)
        self.videoIndex = self.videoIndex - 1

        if self.videoIndex < 0 :
            self.videoIndex = 1

        self.currentShow = self.videoList[self.videoIndex]
        media = self._instance.media_new(self.currentShow)
        self._player.set_media(media)
        self._player.play()

    def getRunning(self):
        return self.isPlaying
		
    def playNextFolder(self):
        print('Play next folder')

    def playPrevousFolder(self):
        print('play previous folder')

        # Returns the current state of VLC
    def getStatus(self):
        return self._player.get_state()

    # This gets a location path and returns a list of all found videos in it.
    # Then adds the list to videolist
    def getShowsFromFolder(self,_path):
        self.showList.clear()
        for root, dirs, files in os.walk(_path):
            for file in files:
                if(file.endswith(".mp4")):
                    self.showList.append(os.path.join(root,file))   
        self.folderList.append(self.showList)         
        return self.showList
    
    def getFolderCount(self):
        return len(self.folderList)
			
# Hardware functions, these will be moved to player class if used.
def rotaryHeldDown():
	print('Previous folder')
	
def rotaryReleased():
    print('Rotary released')
    
def rotaryPressed():
    print('Rotary pressed')
	
	
# side Button functions
def buttonReleased():
    print('Button released')

def buttonHeld():
    print('Button held')

	
# Create the player and specify some media locations, 
# lists then get added to a folder list.
player     = Player()
adsList    = player.getShowsFromFolder(adsPath)
moviesList = player.getShowsFromFolder(moviePath)


# Rotary input function mapping.
rotor.when_rotated_counter_clockwise = player.playPreviousShow
rotor.when_rotated_clockwise         = player.playNextShow

buttonEncoder.when_pressed           = player.playNextFolder
buttonEncoder.when_released          = rotaryReleased
buttonEncoder.when_held              = rotaryHeldDown

# Side button function mapping.
buttonSide.when_pressed  = player.stop
buttonSide.when_released = buttonReleased
buttonSide.when_held     = buttonHeld

# Play a random show from the supplied list.
player.playRandomShowFromList(moviesList)

# Main Function.
while  playerIsRunning == True:
	playerIsRunning = player.getRunning()
	playerStatus = player.getStatus()
	time.sleep(1)
  
quit()






