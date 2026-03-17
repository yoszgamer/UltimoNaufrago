#!/usr/bin/python
# -*- coding: utf-8 -*-

class FishingGame:
    def __init__(self):
        self.markerPos = None
        self.succesZone = None
        self.speed = None
        self.stateTimer = 600
        self.active = False

    def start(self):
        self.stateTimer = 600
        self.active = True

    def update(self):
        if not self.active:
            return
        self.stateTimer -= 1

    def is_finished(self):
        return self.stateTimer <= 0

    def checkInput(self, ):
        pass

    def giveReward(self, p):
        pass
