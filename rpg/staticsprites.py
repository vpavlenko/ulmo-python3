#!/usr/bin/env python

from sprites import *

from spriteframes import StaticFrames
from events import CoinCollectedEvent, KeyCollectedEvent, DoorOpenedEvent, DoorOpeningEvent, CheckpointReachedEvent
from events import KeyMetadata, CoinMetadata, DoorMetadata, CheckpointMetadata

class Flames(OtherSprite):
    
    framesImage = None
    
    def __init__(self):
        if Flames.framesImage is None:    
            imagePath = os.path.join(SPRITES_FOLDER, "flame-frames.png")
            Flames.framesImage = view.loadScaledImage(imagePath, None)        
        animationFrames = view.processStaticFrames(Flames.framesImage)
        spriteFrames = StaticFrames(animationFrames, 6)
        OtherSprite.__init__(self, spriteFrames, (4, 2))

class Coin(OtherSprite):
    
    framesImage = None
    
    baseRectSize = (8 * SCALAR, BASE_RECT_HEIGHT)
        
    def __init__(self):
        if Coin.framesImage is None:    
            imagePath = os.path.join(SPRITES_FOLDER, "coin-frames.png")
            Coin.framesImage = view.loadScaledImage(imagePath, None)        
        animationFrames = view.processStaticFrames(Coin.framesImage)
        spriteFrames = StaticFrames(animationFrames, 6)
        OtherSprite.__init__(self, spriteFrames, (2, 2))
        
    def processCollision(self, player):
        event = CoinCollectedEvent(CoinMetadata(self.uid))
        self.eventBus.dispatchCoinCollectedEvent(event)
        player.incrementCoinCount()
        self.toRemove = True

class Key(OtherSprite):
    
    framesImage = None
    
    baseRectSize = (8 * SCALAR, BASE_RECT_HEIGHT)
        
    def __init__(self):
        if Key.framesImage is None:    
            imagePath = os.path.join(SPRITES_FOLDER, "key-frames.png")
            Key.framesImage = view.loadScaledImage(imagePath, None)        
        animationFrames = view.processStaticFrames(Key.framesImage, 6)
        spriteFrames = StaticFrames(animationFrames, 6)
        OtherSprite.__init__(self, spriteFrames, (2, 2))
        
    def processCollision(self, player):
        event = KeyCollectedEvent(KeyMetadata(self.uid))
        self.eventBus.dispatchKeyCollectedEvent(event)
        player.incrementKeyCount()
        self.toRemove = True

class Chest(OtherSprite):
    
    framesImage = None
    
    baseRectSize = (8 * SCALAR, BASE_RECT_HEIGHT)
        
    def __init__(self):
        if Chest.framesImage is None:    
            imagePath = os.path.join(SPRITES_FOLDER, "chest.png")
            Chest.framesImage = view.loadScaledImage(imagePath, None)        
        animationFrames = view.processStaticFrames(Chest.framesImage, 1)
        spriteFrames = StaticFrames(animationFrames)
        OtherSprite.__init__(self, spriteFrames)
        
    # override
    def advanceFrame(self, increment, metadata):
        pass
                
class Rock(OtherSprite):
    
    framesImage = None
    
    baseRectSize = (8 * SCALAR, BASE_RECT_HEIGHT)
        
    def __init__(self):
        if Rock.framesImage is None:    
            imagePath = os.path.join(SPRITES_FOLDER, "rock.png")
            Rock.framesImage = view.loadScaledImage(imagePath, None)        
        animationFrames = view.processStaticFrames(Rock.framesImage, 1)
        spriteFrames = StaticFrames(animationFrames)
        OtherSprite.__init__(self, spriteFrames, (0, -4))
        
    # override
    def advanceFrame(self, increment, metadata):
        pass
                
class Door(OtherSprite):
    
    framesImage = None
    
    baseRectSize = (4 * SCALAR, BASE_RECT_HEIGHT)    

    def __init__(self):
        if Door.framesImage is None:    
            imagePath = os.path.join(SPRITES_FOLDER, "door-frames.png")
            Door.framesImage = view.loadScaledImage(imagePath, None)
        animationFrames = view.processStaticFrames(Door.framesImage, 8)
        spriteFrames = StaticFrames(animationFrames, 6)
        OtherSprite.__init__(self, spriteFrames)
        self.opening = False
        self.frameCount = 0
        self.frameIndex = 0

    """
    Base rect extends beyond the bottom of the sprite image so player's base
    rect can intersect with it and allow it to be opened.
    """
    def getBaseRectTop(self, baseRectHeight):
        return self.mapRect.bottom + BASE_RECT_EXTEND - baseRectHeight
        
    # override
    def advanceFrame(self, increment, metadata):
        if increment and self.opening:
            self.frameCount = (self.frameCount + increment) % self.spriteFrames.frameSkip
            if self.frameCount == 0:
                self.frameIndex += 1       
                if self.frameIndex == self.spriteFrames.numFrames:
                    self.opened()
                else:
                    self.image = self.spriteFrames.animationFrames[self.frameIndex]
    
    def opened(self):
        metadata = DoorMetadata(self.uid, self.tilePosition, self.level)
        metadata.applyMapActions(self.rpgMap)
        event = DoorOpenedEvent(metadata)
        self.eventBus.dispatchDoorOpenedEvent(event)
        self.toRemove = True
        
    def processAction(self, player):
        if player.getKeyCount() > 0 and not self.opening:
            player.decrementKeyCount()
            self.opening = True
            self.eventBus.dispatchDoorOpeningEvent(DoorOpeningEvent())

class Checkpoint(OtherSprite):
    
    framesImage = None
    
    baseRectSize = (8 * SCALAR, BASE_RECT_HEIGHT)
        
    def __init__(self):
        if Checkpoint.framesImage is None:    
            imagePath = os.path.join(SPRITES_FOLDER, "check-frames.png")
            Checkpoint.framesImage = view.loadScaledImage(imagePath, None)        
        animationFrames = view.processStaticFrames(Checkpoint.framesImage, 4)
        spriteFrames = StaticFrames(animationFrames, 12)
        OtherSprite.__init__(self, spriteFrames, (3, -3))
        
    def processCollision(self, player):
        event = CheckpointReachedEvent(CheckpointMetadata(self.uid,
                                                          self.rpgMap.name,
                                                          self.tilePosition,
                                                          self.level,
                                                          player.getCoinCount(),
                                                          player.getKeyCount()))
        self.eventBus.dispatchCheckpointReachedEvent(event)
        player.checkpointReached()
        self.toRemove = True
        
class Shadow(OtherSprite):
    
    framesImage = None
    
    def __init__(self):
        if Shadow.framesImage is None:    
            imagePath = os.path.join(SPRITES_FOLDER, "shadow.png")
            Shadow.framesImage = view.loadScaledImage(imagePath, None)        
        animationFrames = view.processStaticFrames(Shadow.framesImage, 1)
        spriteFrames = StaticFrames(animationFrames)
        OtherSprite.__init__(self, spriteFrames, (4, 2))
        self.upright = False
        
    def setupFromPlayer(self, player, downLevel):
        self.setup("shadow", player.rpgMap, player.eventBus)
        px = player.mapRect.topleft[0]
        py = player.mapRect.topleft[1] + downLevel * TILE_SIZE + player.image.get_height() - self.image.get_height()
        self.setPixelPosition(px, py, player.level - downLevel)
