#!/usr/bin/env python

from getDinoBoneData import getData

with open("dinosaurs.txt") as f:
    dinoList = f.read().splitlines()

df = getData(dinoList,10)

