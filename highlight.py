#!/usr/bin/env python

from PIL import Image, ImageChops, ImageSequence
import sys
import argparse

def in_range(x,y,w,h):
    return x >= 0 and x < w and y >= 0 and y < h

def neighbors(x, y, w, h, distance):
    for dx in range(0, distance+1):
        dy = distance - dx
        points = set(filter(lambda z: in_range(z[0], z[1], w, h), [
            (x-dx, y-dy),
            (x-dx, y+dy),
            (x+dx, y-dy),
            (x+dx, y+dy)
        ]))
        for p in points:
            yield p

def find_nearest_pixel(img, x, y, f):
    distance = 0
    while True:
        for (i,j) in neighbors(x, y, img.width, img.height, distance):
            try:
                pixel = img.getpixel((i,j))
                if f(pixel):
                    return distance
            except IndexError as e:
                # Ignore when outside the image
                print("This shouldn't happen anymore")
        distance += 1
    return -1

from functools import cache

def find_min_distances(img, f):
    ret = {}
    stack = []
    for i in range(0, img.width):
        for j in range(0, img.height):
            if f(img.getpixel((i,j))):
                stack.append((i,j))
    while len(stack) != 0:
        (x,y) = stack[0]
        stack = stack[1:]
        if (x,y) in ret:
            continue
        nbors = list(neighbors(x,y,img.width,img.height,1))
        if f(img.getpixel((x,y))):
            ret[(x,y)] = 0
        else:
            visited_nbors = [x for x in nbors if x in ret]
            rets = [ret[(i,j)] for (i,j) in visited_nbors]
            min_dist = min(rets)
            ret[(x,y)] = min_dist + 1
        stack.extend(nbors)
    return ret

def is_transparent(pixel):
    (r,g,b,a) = pixel
    return a < 120

def is_opaque(pixel):
    (r,g,b,a) = pixel
    return a > 100

RGBA_MODE = "RGBA"

WHITE_PIXEL = (255, 255, 255, 255)
BLACK_PIXEL = (30, 30, 30, 255)
TRANSPARENT_PIXEL = (0,0,0,0)

img = Image.open("mood.png").convert(RGBA_MODE)
img = img.resize((img.width * 2, img.height * 2))

THRESHOLD = 4

def highlight(img):
    new_img = img.copy()
    for i in range(0, img.width):
        for j in range(0, img.height):
            dist = find_nearest_pixel(img, i, j, is_transparent)
            if dist >= THRESHOLD:
                new_img.putpixel((i,j), WHITE_PIXEL)

    new_img.save("output-highlight.png")

def highlight2(img):
    THRESHOLD=6
    new_img = img.copy()
    min_distances = find_min_distances(img, is_opaque)
    for i in range(0, img.width):
        for j in range(0, img.height):
            dist = min_distances[(i,j)]
            if dist == 0:
                new_img.putpixel((i,j), WHITE_PIXEL)
            elif dist <= THRESHOLD:
                new_img.putpixel((i,j), BLACK_PIXEL)
            else:
                new_img.putpixel((i,j), TRANSPARENT_PIXEL)

    new_img.save("output-highlight2.png")

highlight(img)
highlight2(img)
