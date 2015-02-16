from math import *
from omega import *


class ToggleInteract:
        
        _lstObject = []
        _lstCallback = []
        _actionPressed = False
        _actionUsed = False
        _triggerDist = 2.5
        
        @staticmethod
        def Init(triggerDist):
                ToggleInteract._triggerDist = triggerDist
                
        @staticmethod       
        def Add(sceneObject, callback):
                ToggleInteract._lstObject.append(sceneObject)
                ToggleInteract._lstCallback.append(callback)
                print("Added")
                
        @staticmethod
        def ActionPressed():
                if (ToggleInteract._actionPressed):
                        ToggleInteract._actionUsed = True

                ToggleInteract._actionPressed = True

                        
                
        @staticmethod
        def ActionReleased():
                ToggleInteract._actionPressed = False
                ToggleInteract._actionUsed = False
                
        @staticmethod        
        def Update():
                for i in range(len(ToggleInteract._lstObject)):
                        cb = ToggleInteract._lstCallback[i]
                        cb.Update()
                
        @staticmethod        
        def Poll(position):
        
                if (not ToggleInteract._actionPressed or ToggleInteract._actionUsed):
                        return
                
                for i in range(len(ToggleInteract._lstObject)):
                # if close to object then
                        obj = ToggleInteract._lstObject[i]
                        
                        if (obj is None):
                                continue
                        
                        objPos = obj.getPosition()
                        #print(objPos)
                        #print(position)
                        diff = position - objPos
                        diff.y = 0.0;
                        length = diff.magnitude()
                        print(length)
                        if (length <= ToggleInteract._triggerDist):
                # if ray intersects the object then
                                #print("Action within range")
                                print(ToggleInteract._actionPressed)
                                print(ToggleInteract._actionUsed)
                                cb = ToggleInteract._lstCallback[i]
                                print("Action emit")
                                print(i)
                                cb.Action()  
                # check for action event
                
                # if action event, launch callback
                ToggleInteract._actionUsed = True
