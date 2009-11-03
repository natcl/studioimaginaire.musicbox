#!/usr/bin/env python
"""\
SVG.py - Construct/display SVG scenes.

The following code is a lightweight wrapper around SVG files. The metaphor
is to construct a scene, add objects to it, and then write it to a file
to display it.

This program uses ImageMagick to display the SVG files. ImageMagick also 
does a remarkable job of converting SVG files into other units.
"""

import os
import random
display_prog = 'display' # Command to execute to display images.

columns = []
      
class Scene:
    def __init__(self,name="svg",height=400,width=400, stroke_width = '1mm'):
        self.name = name
        self.items = []
        self.height = height
        self.width = width
        self.stroke_width = stroke_width
        return

    def add(self,item): self.items.append(item)

    def strarray(self):
        var = ["<?xml version=\"1.0\"?>\n",
               "<svg height=\"%s\" width=\"%s\" >\n" % (self.height,self.width),
               " <g style=\"fill-opacity:1.0; stroke:black;\n",
               "  stroke-width:%s;\">\n" % (self.stroke_width)]
        for item in self.items: var += item.strarray()            
        var += [" </g>\n</svg>\n"]
        return var

    def write_svg(self,filename=None):
        if filename:
            self.svgname = filename
        else:
            self.svgname = self.name + ".svg"
        file = open('./'+ self.svgname,'w')
        file.writelines(self.strarray())
        file.close()
        return

    def display(self,prog=display_prog):
        os.system("%s %s" % (prog,self.svgname))
        return        
        

class Line:
    def __init__(self,start,end):
        self.start = start #xy tuple
        self.end = end     #xy tuple
        return

    def strarray(self):
        return ["  <line x1=\"%s\" y1=\"%s\" x2=\"%s\" y2=\"%s\" />\n" %\
                (self.start[0],self.start[1],self.end[0],self.end[1])]


class Circle:
    def __init__(self,center,radius,color):
        self.center = center #xy tuple
        self.radius = radius #xy tuple
        self.color = color   #rgb tuple in range(0,256)
        return

    def strarray(self):
        return ["  <circle cx=\"%s\" cy=\"%s\" r=\"%s\"\n" %\
                (self.center[0],self.center[1],self.radius),
                "    style=\"fill:%s;\"  />\n" % colorstr(self.color)]

class Rectangle:
    def __init__(self,origin,height,width,color):
        self.origin = origin
        self.height = height
        self.width = width
        self.color = color
        return

    def strarray(self):
        return ["  <rect x=\"%s\" y=\"%s\" height=\"%s\"\n" %\
                (self.origin[0],self.origin[1],self.height),
                "    width=\"%s\" style=\"fill:%s;\" />\n" %\
                (self.width,colorstr(self.color))]

class Text:
    def __init__(self,origin,text,size=24):
        self.origin = origin
        self.text = text
        self.size = size
        return

    def strarray(self):
        return ["  <text x=\"%s\" y=\"%s\" font-size=\"%s\">\n" %\
                (self.origin[0],self.origin[1],self.size),
                "   %s\n" % self.text,
                "  </text>\n"]
        
    
def colorstr(rgb): return "#%x%x%x" % (rgb[0]/16,rgb[1]/16,rgb[2]/16)

def get_columns(*c):
    global columns
    columns.append(c)

def reset():
    global columns
    columns = []
    
def generate_svg():
    scene = Scene('svg_output', height = '69mm', width = '240mm', stroke_width = '0mm')
    for i1, c in enumerate(columns):
        for i2, state in enumerate(c):
            if state:
                print i1, i2, state
                x = str(i1*3 + 19)+ 'mm'
                y = str(i2 * 3 + 6) + 'mm'
                scene.add(Circle((x, y), '1.5mm',(0,0,0)))
    scene.write_svg()
    return
