#!/usr/bin/env python

"""
Copyright (c) 2020 Sublunar Space

---- MIT License ----
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys
import math
import re
import drawsvg as svg

def prepareMessage(message):
    message = re.sub("[^a-zA-Z]+", "", message) # get rid of all non-alphabetic characters
    message = message.lower()
    message = "".join(dict.fromkeys(message)) # remove duplicate letters
    return message

def kameaSigil(planet, message):
    kamea = [
        [
            [37, 78, 29, 70, 21, 62, 13, 54,  5], 
            [ 6, 38, 79, 30, 71, 22, 63, 14, 46], 
            [47,  7, 39, 80, 31, 72, 23, 55, 15], 
            [16, 48,  8, 40, 81, 32, 64, 24, 56], 
            [57, 17, 49,  9, 41, 73, 33, 65, 25], 
            [26, 58, 18, 50,  1, 42, 74, 34, 66], 
            [67, 27, 59, 10, 51,  2, 43, 75, 35], 
            [36, 68, 19, 60, 11, 52,  3, 44, 76], 
            [77, 28, 69, 20, 61, 12, 53,  4, 45]
        ], # moon
        [
            [ 8, 58, 59,  5,  4, 62, 63,  1], 
            [49, 15, 14, 52, 53, 11, 10, 56], 
            [41, 23, 22, 44, 45, 19, 18, 48], 
            [32, 34, 35, 29, 28, 38, 39, 25], 
            [40, 26, 27, 37, 36, 30, 31, 33], 
            [17, 47, 46, 20, 21, 43, 42, 24], 
            [ 9, 55, 54, 12, 13, 51, 50, 16], 
            [64,  2,  3, 61, 60,  6,  7, 57]
        ], # mercury
        [
            [22, 47, 16, 41, 10, 35,  4], 
            [ 5, 23, 48, 17, 42, 11, 29], 
            [30,  6, 24, 49, 18, 36, 12], 
            [13, 31,  7, 25, 43, 19, 37], 
            [38, 14, 32,  1, 26, 44, 20], 
            [21, 39,  8, 33,  2, 27, 45], 
            [46, 15, 40,  9, 34,  3, 28]
        ], # venus
        [
            [ 6, 32,  3, 34, 35,  1], 
            [ 7, 11, 27, 28,  8, 30], 
            [19, 14, 16, 15, 23, 24], 
            [18, 20, 22, 21, 17, 13], 
            [25, 29, 10,  9, 26, 12], 
            [36,  5, 33,  4,  2, 31]
        ], # sun
        [
            [11, 24,  7, 20,  3],
            [ 4, 12, 25,  8, 16],
            [17,  5, 13, 21,  9],
            [10, 18,  1, 14, 22],
            [23,  6, 19,  2, 15]
        ], # mars
        [
            [ 4, 14, 15,  1],
            [ 9,  7,  6, 12],
            [ 5, 11, 10,  8],
            [16,  2,  3, 13]
        ], # jupiter
        [
            [4, 9, 2],
            [3, 5, 7],
            [8, 1, 6]
        ] # saturn    
    ]
    size = 400
    square = kamea[planet]
    divisions = 9 - planet
    distance = size / divisions
    halfSize = size / 2
    coordList = []
    for char in message.lower(): # message to lowercase
        digit = ord(char) - 96 # find ordinal number and substract 96 for ASCII position of 'a'
        for squareRow in square: # for the desired planetary square
            if digit in squareRow: # check if digit is present
                row = square.index(squareRow) # remember row
                col = squareRow.index(digit)  # and column
                # calculate center of the square element per position (row or column) in the kamea
                coordX = (round((col + 1) * distance) - distance / 2) - halfSize
                coordY = size - (round((row + 1) * distance) - distance / 2) - halfSize
                coordList.append([coordX, coordY]) # write center coordinates to sigil coordinate list
    
    return coordList

def drawSigil(points, canvas, color='white'): # draw sigil from coordinate list

    # setup sigil
    dash = svg.Marker(-0.5, -0.5, 0.5, 0.5, scale=5, orient='auto') # define line to terminate the sigil
    dash.append(svg.Line(-0., -0.5, 0., 0.5, stroke_width=0.2, stroke=color))
    dot = svg.Marker(-0.8, -0.5, 0.5, 0.5, scale=5, orient='auto') # define circle to start the sigil
    dot.append(svg.Circle(-0.3, 0.0, 0.3, stroke_width=0.2, stroke=color, fill='none'))
    p = svg.Path(stroke_width=7, stroke=color, fill='none', marker_start=dot, marker_end=dash)

    # draw sigil
    for point in points:
        if points.index(point) == 0:
            originX = point[0]
            originY = point[1]
            p.M(originX, originY)
        else:
            x = point[0] - originX # abs. to rel. coords
            y = point[1] - originY # abs. to rel. coords
            p.l(x,y) # draw
            originX = point[0]
            originY = point[1]

    # add to canvas
    canvas.append(p)

def createSigil(message, planet, fileName):

    planets = ["moon", "mercury", "venus", "sun", "mars", "jupiter", "saturn"]
    planet = planets.index(planet.lower())
    # set up SVG canvas
    d = svg.Drawing(400, 400, origin='center', context=svg.Context(invert_y=True)) # define canvas

    # draw sigils
    message = prepareMessage(message)
    print("sigilizing:", message)
    coordList = kameaSigil(planet, message)
    drawSigil( coordList, d, "black")

    # save sigil to SVG file
    d.save_svg(fileName)

def main():
    argNo = len(sys.argv) - 1

    if argNo == 3: # if three arguments are provided
        createSigil(sys.argv[1], sys.argv[2], sys.argv[3])

    else:
        print("--------------------------------------------")
        print("Please provide arguments: <string> <planet> <filename>")
        print("--------------------------------------------")

if __name__ == "__main__":
    main()
