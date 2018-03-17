import bpy
from scipy.misc import imread
import numpy as np
import random
import math

name = "test"
#bpy.ops.object.select_all(action='DESELECT')
#bpy.data.objects[name].select = True
#bpy.ops.object.delete()

def displace(width, height, bs, im):
    verts = []
    edges = []
    faces = []
    array = np.array(im)
    widthindex=math.floor(width/bs)+1
    heightindex=math.floor(height/bs)+1
    for x in range(0, widthindex):
        for y in range(0, heightindex):
            rgb = array[x*10][y*10]
            z = rgb[0]*.3+rgb[1]*.59+rgb[2]*.11
            z = z/255.0*2
            if x==0 or y==0 or x==widthindex-1 or y==heightindex-1:
                z=0
            verts.append([x*bs, y*bs, z])
            if x > 0 and y > 0:
                tl = int((x-1)+(y-1)*widthindex)
                tr = int((x  )+(y-1)*widthindex)
                bl = int((x-1)+(y  )*widthindex)
                br = int((x  )+(y  )*widthindex)
                print("tl"+str(tl)+","+"tr"+str(tr)+","+"br"+str(br)+","+"bl"+str(bl)+",")
                faces.append((tl, tr, br, bl))

    print("length!:"+str(len(verts)))
    print(verts)
    print(faces)

    me = bpy.data.meshes.new(name+'Mesh')
    ob = bpy.data.objects.new(name, me)
    ob.show_name = True
    # Link object to scene
    bpy.context.scene.objects.link(ob)
    me.from_pydata(verts, edges, faces)
    me.validate(True)
    # Update mesh with new data
    me.update()




im = imread("/home/he-man/Desktop/texture.jpg")

displace(32, 32, 1, im)
# Create mesh and object
