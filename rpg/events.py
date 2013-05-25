#! /usr/bin/env python

class Event():    
    def getMetadata(self):
        pass

class DoorOpeningEvent(Event):
    pass

class PlayerFootstepEvent(Event):
    pass

class MapTransitionEvent(Event):
    pass

class LifeLostEvent(Event):
    pass

class EndGameEvent(Event):
    pass

class WaspZoomingEvent(Event):
    pass

class BeetleCrawlingEvent(Event):
    pass

class PlayerFallingEvent(Event):
    pass
        
# ==============================================================================

class MetadataEvent(Event):
    
    def __init__(self, metadata):
        self.metadata = metadata
        
    def getMetadata(self):
        return self.metadata
        
class CoinCollectedEvent(MetadataEvent):
    def __init__(self, metadata):
        MetadataEvent.__init__(self, metadata)

class KeyCollectedEvent(MetadataEvent):
    def __init__(self, metadata):
        MetadataEvent.__init__(self, metadata)
        
class DoorOpenedEvent(MetadataEvent):
    def __init__(self, metadata):
        MetadataEvent.__init__(self, metadata)

class CheckpointReachedEvent(MetadataEvent):
    def __init__(self, metadata):
        MetadataEvent.__init__(self, metadata)
        
# ==============================================================================

class SpriteMetadata:
    
    def __init__(self, uid):
        self.uid = uid
    
    # placeholder method    
    def isRemovedFromMap(self):
        return True
    
    # placeholder method
    def applyMapActions(self, rpgMap):
        pass
    
class CoinMetadata(SpriteMetadata):    
    def __init__(self, uid):
        SpriteMetadata.__init__(self, uid)
        
class KeyMetadata(SpriteMetadata):
    def __init__(self, uid):
        SpriteMetadata.__init__(self, uid)

class DoorMetadata(SpriteMetadata):
    
    def __init__(self, uid, tilePosition, level):
        SpriteMetadata.__init__(self, uid)
        self.x, self.y = tilePosition[0], tilePosition[1]
        self.level = level

    # makes the corresponding tile available for this level
    def applyMapActions(self, rpgMap):
        rpgMap.addLevel(self.x, self.y + 1, self.level)

class CheckpointMetadata(SpriteMetadata):    
    def __init__(self, uid, mapName, tilePosition, level, coinCount, keyCount):
        SpriteMetadata.__init__(self, uid)
        self.mapName = mapName
        self.tilePosition = tilePosition
        self.level = level
        self.coinCount = coinCount
        self.keyCount = keyCount
        