# simple environment as starting point for VR 528 Spring 2015
# copyright 2014-2015 evl
# written by Andrew Johnson

# this example shows:
# loading in google sketup models converted into fbx format
# adding directional and point lights
# adding shadows to the point lights
# adding sounds
# walking on the floor / walking into walls

from math import *
from euclid import *
from omega import *
from cyclops import *
from omegaToolkit import *
import time
import random

# local modules
from walkabout import walkabout
from toggleInteract import ToggleInteract


# constants
SOUND_FACTOR = 1.0
BGMUSIC_VOL = 0.8
HUMAN_SCALE = 1.0
INSECT_SCALE = 20.0
NAVI_SPEED_MOD = 2.0
INTERACT_DIST = 3.0

BACKDOOR_POS = Vector3(4.3, 0.0, -3.0)
FRONTDOOR_POS = Vector3(7.5, 0.0, -8.0)
GARAGE_POS = Vector3(14.0, 0.0, -15.3)
FUTON_POS = Vector3(1.3, 0.1, -14.00)

GLOBAL_SCALE = HUMAN_SCALE




scene = getSceneManager()
cam = getDefaultCamera()
cam.setPosition(4, 0, -3)

# black background
scene.setBackgroundColor(Color(0, 0, 0, 1))

#set the far clipping plane to 1000 meters away
setNearFarZ(0.1, 100)

# create a skybox
skybox = Skybox()
skybox.loadCubeMap("models/box", "png")
scene.setSkyBox(skybox)


# create a node to hold everything else
everything = SceneNode.create('everything')

# Load house model
houseModel = ModelInfo()
houseModel.name = "house"
houseModel.path = "models/house.fbx"
scene.loadModel(houseModel)
houseModel.generateNormals = True
houseModel.optimize = True

# Create a scene object using the loaded model
house = StaticObject.create("house")
house.setSelectable(True)
house.setEffect("colored")
house.setEffect("textured -C")

# omegalib uses meters as its default scale
# house model seems to use inches - inches to meters 0.025400
house.setScale(Vector3(0.0254, 0.0254, 0.0254))


# put everything under a single node for easier control
everything.addChild(house)


# ******************************************************************************
# ********************************* MODELS *************************************
# ******************************************************************************

# turntable
turntableModel = ModelInfo()
turntableModel.name = "turntable"
turntableModel.path = "models/turntable.fbx"
scene.loadModel(turntableModel)
turntable = StaticObject.create("turntable")
turntable.setSelectable(True)
turntable.setEffect("colored")
everything.addChild(turntable)
turntable.setPosition(9.8, 0.9, -0.4)
turntable.yaw(radians(90))

# speaker
speakerModel = ModelInfo()
speakerModel.name = "speaker"
speakerModel.path = "models/speaker.fbx"
scene.loadModel(speakerModel)

speaker1 = StaticObject.create("speaker")
speaker1.setSelectable(True)
speaker1.setEffect("colored")
speaker1.setEffect("textured -C")
everything.addChild(speaker1)
speaker1.setPosition(4.8, 0, -10.5)
speaker1.yaw(radians(45))

speaker2 = StaticObject.create("speaker")
speaker2.setSelectable(True)
speaker2.setEffect("colored")
speaker2.setEffect("textured -C")
everything.addChild(speaker2)
speaker2.setPosition(9.0, 0, -17)
speaker2.yaw(radians(45))


# floor lamp
floorLampModel = ModelInfo()
floorLampModel.name = "floorLamp"
floorLampModel.path = "models/floor_lamp.fbx"
scene.loadModel(floorLampModel)

floorLamp = StaticObject.create("floorLamp")
floorLamp.setSelectable(True)
floorLamp.setEffect("colored")
floorLamp.setEffect("textured -C")
everything.addChild(floorLamp)
floorLamp.setPosition(6.5, 0, -0.4)

floorLamp2 = StaticObject.create("floorLamp")
floorLamp2.setSelectable(True)
floorLamp2.setEffect("colored")
floorLamp2.setEffect("textured -C")
everything.addChild(floorLamp2)
floorLamp2.setPosition(3, 0, -0.4)

# dragon balls
dbModel = ModelInfo()
dbModel.name = "dragonBalls"
dbModel.path = "models/db.fbx"
scene.loadModel(dbModel)

dragonBalls = StaticObject.create("dragonBalls")
dragonBalls.setSelectable(True)
dragonBalls.setEffect("colored")
dragonBalls.setEffect("textured -C")
everything.addChild(dragonBalls)
dragonBalls.setPosition(30, 0, -5.0)





# add some lights

# two directional lights to get some light on all surface
light1 = Light.create()
light1.setColor(Color(0.4, 0.4, 0.4, 1))
light1.setAmbient(Color(0.1, 0.1, 0.1, 1))
light1.setPosition(Vector3(-30, 40, -10))
light1.setEnabled(True)
sm1 = ShadowMap()
sm1.setTextureSize(2048, 2048)
light1.setShadow(sm1)
light1.setShadowRefreshMode(ShadowRefreshMode.OnLightMove)


# point light in the family room ceiling
light4 = Light.create()
light4.setColor(Color(0.7, 0.7, 0.7, 1))
light4.setPosition(Vector3(8.85, 2.00, -5.79))
light4.setEnabled(True)
sm4 = ShadowMap()
sm4.setTextureSize(2048, 2048)
light4.setShadow(sm4)
light4.setShadowRefreshMode(ShadowRefreshMode.OnLightMove)

# add the lights to the scene
everything.addChild(light1)
everything.addChild(light4)





# ******************************************************************************
# ********************************* SOUNDS *************************************
# ******************************************************************************
se = getSoundEnvironment()
se.setVolumeScale(SOUND_FACTOR)
ambientMusic = se.loadSoundFromFile('ambientMusic', 'SOUNDS/japanese_ambient.wav')
recordMusic = se.loadSoundFromFile('recordMusic', 'SOUNDS/azuma_kabuki_nagauta.wav')
twinkleSound = se.loadSoundFromFile('twinkleSound', 'SOUNDS/twinkle.wav')
gongSound = se.loadSoundFromFile('gongSound', 'SOUNDS/gong.wav')


def addMusic(instance, vol):
        time.sleep(1)
        simusic = SoundInstance(instance)
        houseCenter = house.getBoundCenter()
        houseCenter.y = 1
        simusic.setPosition(houseCenter)
       
        simusic.setLoop(True)
        simusic.setVolume(vol)
        simusic.play()
        simusic.setEnvironmentSound(True)
        return(simusic)
        
def addSound(instance, vol):
        time.sleep(1)
        sisound = SoundInstance(instance)
        sisound.setPosition(house.getBoundCenter())
        sisound.setLoop(True)
        sisound.setVolume(vol)
        sisound.play()
        sisound.setEnvironmentSound(True)
        return(sisound)
        


bgMusic = addMusic(ambientMusic, BGMUSIC_VOL)





# ******************************************************************************
# ********************************* SCALING ************************************
# ******************************************************************************

previousScale = 1.0
def scaleEverything(scale):
        global GLOBAL_SCALE
        GLOBAL_SCALE = scale
        everything.setScale(scale, scale, scale)
        ToggleInteract.Init(scale * INTERACT_DIST)
        
        ctl = cam.getController()
        ctl.setSpeed(scale * NAVI_SPEED_MOD)
        
        
        
def setHumanMode():
        global previousScale
        scale = HUMAN_SCALE
        scaleEverything(scale)
        walkabout.setFloorCheck(True)
        cam.setPosition(cam.getPosition() / previousScale)
        
        previousScale = scale
        
def setInsectMode():
        global previousScale
        scale = INSECT_SCALE
        scaleEverything(scale)
        
        if (previousScale != scale):
                cam.setPosition(cam.getPosition() * scale)
        walkabout.setFloorCheck(False)

        previousScale = scale
        

# ******************************************************************************
# ********************************* TELEPORT ***********************************
# ******************************************************************************

def teleportBackDoor():
        cam.setPosition(BACKDOOR_POS * GLOBAL_SCALE)
        cam.setPitchYawRoll(Vector3(0, radians(90), 0))
        
def teleportFrontDoor():
        cam.setPosition(FRONTDOOR_POS * GLOBAL_SCALE)
        cam.setPitchYawRoll(Vector3(0, radians(-90), 0))
        
def teleportGarage():
        cam.setPosition(GARAGE_POS * GLOBAL_SCALE)
        cam.setPitchYawRoll(Vector3(0, radians(90), 0))
        
def teleportFuton():
        cam.setPosition(FUTON_POS * GLOBAL_SCALE)
        cam.setPitchYawRoll(Vector3(0, 0, 0))





# ******************************************************************************
# *********************************** MENU *************************************
# ******************************************************************************


mm = MenuManager.createAndInitialize()

# Get the default menu (System menu)
menu = mm.getMainMenu()
mm.setMainMenu(menu)

#positionMenu = mm.createMenu("positionMenu")
positionMenu = menu.addSubMenu("Teleport")

btnTeleportBacktDoor = positionMenu.addButton("Back Door", "teleportBackDoor()")
btnTeleportFrontDoor = positionMenu.addButton("Front Door", "teleportFrontDoor()")
btnTeleportGarage    = positionMenu.addButton("Garage", "teleportGarage()")
btnTeleportFuton     = positionMenu.addButton("Futon", "teleportFuton()")


#navMenu = mm.createMenu("navMenu")
navMenu = menu.addSubMenu("Navigation Mode")

btnHuman = navMenu.addButton("Human", "setHumanMode()")
btnInsect = navMenu.addButton("Insect", "setInsectMode()")



class LampStateMgr:
        
        def Action(self):
                print("Light Action")
                
                # toggle state    
                self.light.setEnabled(not self.light.isEnabled())
                print("Light is on")
                
        def Update(self):
                pass      
                
        def __init__(self, lampObject):
                self.lamp = lampObject
                self.light = Light.create()
                self.light.setLightType(LightType.Point)
                self.light.setAttenuation(0.5, 0.5, 0.5);
                self.light.setColor(Color(0.9, 0.4, 0.4, 1))
                self.light.setEnabled(False)
                self.lamp.addChild(self.light)
                self.light.setPosition(Vector3(0, self.lamp.getBoundRadius(), 0))
                        
        

class SoundSrc:
        
        def __init__(self, sceneObj, sound, vol, boolLoop, boolStopAmbient, boolHasAction):
                self.obj = sceneObj
                
                self.ha = boolHasAction
                self.sa = boolStopAmbient
                self.sound = SoundInstance(sound)
                self.sound.setLoop(boolLoop)
                self.sound.setVolume(vol)
                self.sound.setEnvironmentSound(True)
                
                if (not self.ha):
                        self.sound.play()
                
                self.Update()
                
        def Update(self):
                self.sound.setPosition(self.obj.getPosition() * GLOBAL_SCALE)
                #print(self.sound.getPosition())
                
                if (self.sa):
                        if (self.sound.isDone()):
                                bgMusic.fade(BGMUSIC_VOL, 3)
                
        def Action(self):
                if (self.ha):
                        if (self.sound.isPlaying()):
                                self.sound.stop()
                        else:
                                if (self.sa):
                                        bgMusic.fade(0.0, 3)
                                self.sound.play()
                                
                        self.Update()

                
                
















random.seed()


# update function 
def onUpdate(frame, t, dt):
    global oldTyping
    
    # polling
    cameraRef = getDefaultCamera()
    headPos = cameraRef.getPosition() + cameraRef.getHeadOffset()
    ToggleInteract.Poll(headPos)

    # updates
    ToggleInteract.Update()
    walkabout.update(dt)
    









ToggleInteract.Init(INTERACT_DIST)

# add items for interaction
ToggleInteract.Add(floorLamp, LampStateMgr(floorLamp))
ToggleInteract.Add(floorLamp2, LampStateMgr(floorLamp2))
ToggleInteract.Add(floorLamp, SoundSrc(floorLamp, gongSound, 0.5,  False, False, True))
ToggleInteract.Add(floorLamp2, SoundSrc(floorLamp2, gongSound, 0.5, False, False, True))

ToggleInteract.Add(turntable, SoundSrc(speaker1, recordMusic, 0.2, False, True, True))
ToggleInteract.Add(turntable, SoundSrc(speaker2, recordMusic, 0.2, False, True, True))
ToggleInteract.Add(None, SoundSrc(dragonBalls, twinkleSound, 0.2, True, False, False))


# set walkabout settings
walkabout.init(getDefaultCamera())

# Use options below to turn on and off floor and wall checking
walkabout.setFloorCheck(True)
walkabout.setWallCheck(True)

# Sets how high you can climb as a ratio of your body height.
# 0.4 is default and means you can climb things that are 40% of your height
#walkabout.setClimbRatio(0.5)

# Sets how smoothly you climb or fall (max is 1)
# 0.01 means it will take 100 steps to interpolate
#walkabout.setClimbInterpolationSpeed(0.01)  

# set the omegalib update function
setUpdateFunction(onUpdate)



#input handling                                                                 
def handleEvent():
        e = getEvent()
        #print(e.getPosition())                                                 
        #print(e.getType())                                                     
        if(e.isButtonDown(EventFlags.ButtonLeft) or e.isButtonDown(EventFlags.Button3)):                             
            print("Left button pressed")
            ToggleInteract.ActionPressed()
        if(e.isButtonUp(EventFlags.ButtonLeft) or e.isButtonUp(EventFlags.Button3)):                               
            print("Left button released")
            ToggleInteract.ActionReleased()


setEventFunction(handleEvent)

# start with human mode
setHumanMode()


# prove that I made it to the end of the code without an error
print(">>>>>>>>>>>>>>>>>>>>>>>>>> MADE IT !!! <<<<<<<<<<<<<<<<<<<<<<<<<<")
print(">>>>>>>>>>>>>>>>>>>>>>>>>> MADE IT !!! <<<<<<<<<<<<<<<<<<<<<<<<<<")
print(">>>>>>>>>>>>>>>>>>>>>>>>>> MADE IT !!! <<<<<<<<<<<<<<<<<<<<<<<<<<")
print(">>>>>>>>>>>>>>>>>>>>>>>>>> MADE IT !!! <<<<<<<<<<<<<<<<<<<<<<<<<<")
print(">>>>>>>>>>>>>>>>>>>>>>>>>> MADE IT !!! <<<<<<<<<<<<<<<<<<<<<<<<<<")
print(">>>>>>>>>>>>>>>>>>>>>>>>>> MADE IT !!! <<<<<<<<<<<<<<<<<<<<<<<<<<")
print(">>>>>>>>>>>>>>>>>>>>>>>>>> MADE IT !!! <<<<<<<<<<<<<<<<<<<<<<<<<<")
