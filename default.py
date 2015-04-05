import xbmc
import xbmcgui
import xbmcaddon
import time
import sys
import colorsys
import os
import datetime
import math

__addon__      = xbmcaddon.Addon()
__cwd__        = __addon__.getAddonInfo('path')
__resource__   = xbmc.translatePath( os.path.join( __cwd__, 'resources', 'lib' ) )

sys.path.append (__resource__)

from settings import *
from tools import *

try:
  import requests
except ImportError:
  xbmc.log("ERROR: Could not locate required library requests")
  notify("XBMC Super Legend Bulb", "ERROR: Could not import Python requests")

xbmc.log("XBMC Super Legend Bulb service started, version: %s" % get_version())


class MyPlayer(xbmc.Player):
  duration = 0
  playingvideo = None

  def __init__(self):
    xbmc.Player.__init__(self)
  
  def onPlayBackStarted(self):
    if self.isPlayingVideo():
      self.playingvideo = True
      self.duration = self.getTotalTime()
      state_changed("started", self.duration)

  def onPlayBackPaused(self):
    if self.isPlayingVideo():
      self.playingvideo = False
      state_changed("paused", self.duration)

  def onPlayBackResumed(self):
    if self.isPlayingVideo():
      self.playingvideo = True
      state_changed("resumed", self.duration)

  def onPlayBackStopped(self):
    if self.playingvideo:
      self.playingvideo = False
      state_changed("stopped", self.duration)

  def onPlayBackEnded(self):
    if self.playingvideo:
      self.playingvideo = False
      state_changed("stopped", self.duration)

def run():
  player = None
  last = datetime.datetime.now()

  while not xbmc.abortRequested:    
    if player == None:
      logger.debuglog("creating instance of player")
      player = MyPlayer()
    xbmc.sleep(500)


def state_changed(state, duration):
  logger.debuglog("state changed to: %s" % state)
  if duration < 300 and hue.settings.misc_disableshort:
    logger.debuglog("add-on disabled for short movies")
    return

  if state == "started" or state == "resumed":
    logger.debuglog("dimming lights")
    requests.get('https://192.168.1.65/bulb/api/v1.0/warm/50/', verify=False)
  elif state == "stopped" or state == "paused":
    logger.debuglog("brightening lights")
    requests.get('https://192.168.1.65/bulb/api/v1.0/warm/255/', verify=False)

if ( __name__ == "__main__" ):
  settings = settings()
  logger = Logger()
  if settings.debug == True:
    logger.debug()
  
  args = None
  if len(sys.argv) == 2:
    args = sys.argv[1]  
  run()
