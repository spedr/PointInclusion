import shapefile
import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
import argparse
import random
import time
import numpy as np
from UliEngineering.Math.Coordinates import BoundingBox
import os
import psutil


def add_args():
    parser = argparse.ArgumentParser(description='Test point inclusion in polygon with several algorithms.')
    parser.add_argument('-pc', '--polycount', metavar='',type=int, required=True, help='Defines how many polygons will be drawn.')
    parser.add_argument('-pt', '--polytype', metavar='', required=True, help='Either "concave" or "convex".')
    parser.add_argument('-a', '--algorithm', metavar='', required=True, help='Point inclusion algorithm. Can be "naive", "bbox" or "slab".')
    parser.add_argument('-m', '--mode', metavar='', required=True, help='Mouse click or point generation mode. Args: "pgen" or "mouse"')
    parser.add_argument('-poic', '--pointcount', metavar='',type=int, help='How many points will be randomly generated in point generation mode.')
    parser.add_argument('-sbb', '--showbbox', action='store_true', help='Render bounding boxes. True/False')
    parser.add_argument('-r', '--render', action='store_true', help='Render: True/False')
    parser.add_argument('-rp', '--report', action='store_true', help='Prints out execution time and memory report')
    return parser.parse_args()


def scale_points(points, WIDTH, HEIGHT):
    max_x = 0.0
    max_y = 0.0
    min_x = 0.0
    min_y = 0.0

    base_x = int(WIDTH/0.75)
    base_y = int(HEIGHT/0.75)

    offset_x = random.randint(10000,base_x*10000)/10000
    offset_y = random.randint(10000,base_y*10000)/10000



    for point in points:
        if point[0] > max_x:
            max_x = point[0]
        elif point[0] < min_x:
            min_x = point[0]

        if point[1] > max_y:
            max_y = point[1]
        elif point[1] < min_y:
            min_y = point[1]

    for point in points:
        point[0] =  (((point[0] - min_x) * (WIDTH - 0)) / (max_x - min_x)) + 0
        #point[1] =  (((point[1] - min_y) * (600 - 0)) / (max_y - min_y)) + 0
        #point[1] =  (((point[1] - min_y) * (HEIGHT - 0)) / (max_y - min_y)) + 0

        point[1] =  (((point[1] - min_y) * (HEIGHT - 0)) / (max_y - min_y)) + 0
        #NewPoint = (((OldMax - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin

def scale_points_list(points_list, WIDTH, HEIGHT):
    max_x = 0.0
    max_y = 0.0
    min_x = 0.0
    min_y = 0.0

    base_x = int(WIDTH/0.75)
    base_y = int(HEIGHT/0.75)

    offset_x = random.randint(10000,base_x*10000)/10000
    offset_y = random.randint(10000,base_y*10000)/10000


    for polygon in points_list:
        for point in polygon:
            if point[0] > max_x:
                max_x = point[0]
            elif point[0] < min_x:
                min_x = point[0]

            if point[1] > max_y:
                max_y = point[1]
            elif point[1] < min_y:
                min_y = point[1]

    for polygon in points_list:
        for point in polygon:
            point[0] =  (((point[0] - min_x) * (WIDTH - 0)) / (max_x - min_x)) + 0
            #point[1] =  (((point[1] - min_y) * (600 - 0)) / (max_y - min_y)) + 0
            #point[1] =  (((point[1] - min_y) * (HEIGHT - 0)) / (max_y - min_y)) + 0

            point[1] =  (((point[1] - min_y) * (HEIGHT - 0)) / (max_y - min_y)) + 0
            #NewPoint = (((OldMax - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin

def scale_size(scale, poly_list):
    for polygon in poly_list:
        for point in polygon:
            point[0] = point[0] * scale
            point[1] = point[1] * scale
            #point = point * scale

def random_offset(points, WIDTH, HEIGHT):
    base_x = int(WIDTH/1.25)
    base_y = int(HEIGHT/1.25)

    offset_x = random.randint(10000,base_x*10000)/10000
    offset_y = random.randint(10000,base_y*10000)/10000


    for point in points:
        point[0] = point[0] - offset_x
        point[1] = point[1] - offset_y

def random_offset_list(polygon, hole1, hole2):
    base_x = int(WIDTH/1.25)
    base_y = int(HEIGHT/1.25)

    offset_x = random.randint(10000,base_x*10000)/10000
    offset_y = random.randint(10000,base_y*10000)/10000
    #offset_x = random.randint(1, 200)
    #offset_y = random.randint(1, 200)
    #print(offset_x)
    #print(offset_y)

    polygon_copy = polygon
    hole1_copy = hole1
    hole2_copy = hole2

    for point in polygon_copy:
        point[0] = point[0] + offset_x
        point[1] = point[1] + offset_y

    for point in hole1:
        point[0] = point[0] + offset_x
        point[1] = point[1] + offset_y

    for point in hole2:
        point[0] = point[0] + offset_x
        point[1] = point[1] + offset_y

    #print(polygon_copy)
    #print(points_list_copy)
    return [polygon_copy, hole1, hole2]



def naive_inclusion2(points, target_point_x, target_point_y, pprint, index):
    counter = 0
    global HEIGHT, RGB_LIST

    for i in range(len(points)-1):
        #rule 1 = ((points[i][1] <= target_point_y) and (points[i+1][1] > target_point_y))

        if ((points[i][1] <= target_point_y) and (points[i+1][1] > target_point_y)) or ((points[i][1] > target_point_y) and (points[i+1][1] <= target_point_y)):
            asdf = (target_point_y - points[i][1]) / (points[i+1][1] - points[i][1])
            asdf2 = (points[i][0] + asdf * (points[i+1][0] - points[i][0]))
                #print(asdf2)
            if target_point_x < asdf2:
                counter+=1
    if pprint:
        if counter&1 == 1:
            RGB_LIST[index][0] = 255
            RGB_LIST[index][1] = 0
            RGB_LIST[index][2] = 255
            #draw_polygon(points, 255, 0, 255, HEIGHT)
        #print(counter&1)


def bbox_inclusion(x, y, pprint):
    global POLYGON_LIST, RGB_LIST

    for i in range(len(POLYGON_LIST)):
        bbox = BBOX_META[i]
        result = False
        if (x > bbox.minx) and (x < bbox.maxx) and (y > bbox.miny) and (y < bbox.maxy):
            result = True

        if pprint:
            if result:
                RGB_LIST[i][0] = 255
                RGB_LIST[i][1] = 0
                RGB_LIST[i][2] = 255

def point_gen(point_count):
    global POLYGON_LIST, SLABS_META, POLYGON_LIST, args


    start = time.time()
    rand_list = []

    print('Generating random points...')
    for i in range(point_count):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        rand_list.append((x, y))


    print('Testing for ' + str(point_count) + ' random points on ' + str(len(POLYGON_LIST)) + ' polygons:')
    start = time.time()
    process = psutil.Process(os.getpid())
    mem_usage = float(process.memory_info().rss/1000000)
    print ('Current memory usage: ' + str(mem_usage) + ' MB')
    if args.algorithm == 'naive':
        for poic in rand_list:
            for points in POLYGON_LIST:
                naive_inclusion2(points, poic[0], poic[1], False, -1)
        end = time.time()
    elif args.algorithm == 'bbox':
        for poic in rand_list:
            for points in POLYGON_LIST:
                bbox_inclusion(poic[0], poic[1], False)
        end = time.time()
    elif args.algorithm == 'slab':
        for poic in rand_list:
            closest_slab = find_closest_slab(poic[1])
            #print(closest_slab)
            for polygon in SLABS_META[closest_slab]:
                naive_inclusion2(POLYGON_LIST[polygon], float(x), float(y), False, -1)
        end = time.time()
    completion = end-start
    print('All done. Completion time: ' + str(completion))
    mem_usage = float(process.memory_info().rss/1000000)
    print ('Current memory usage: ' + str(mem_usage) + ' MB')


def draw_polygon(points, r, g, b, HEIGHT):
    global POLYGON_LIST

    glColor3f(r, g, b)
    glBegin(GL_LINES)

    for i in range(len(points)):
        if i+1 == len(points):
            break
        p1 = points[i]
        p2 = points[i+1]
        glVertex2f(p1[0], abs(p1[1] - HEIGHT))
        glVertex2f(p2[0], abs(p2[1] - HEIGHT))
    glEnd()


def mouse(button, state, x, y):
    global POLYGON_LIST, SLABS_META, args
    if button == GLUT_LEFT_BUTTON:
        print('X:' + str(x) + '      Y: ' + str(y))
        if args.algorithm=='bbox':
            bbox_inclusion(float(x), float(y), True)
        elif args.algorithm=='naive':
            for i in range(len(POLYGON_LIST)):
                naive_inclusion2(POLYGON_LIST[i], float(x), float(y), True, i)

            #for points in POLYGON_LIST:
            #    naive_inclusion2(points, float(x), float(y), True, points.index)
        elif args.algorithm=='slab':
            closest_slab = find_closest_slab(y)
            #print(closest_slab)
            for i in range(len(SLABS_META[closest_slab])):
                #print(SLABS_META[closest_slab][i])
                naive_inclusion2(POLYGON_LIST[SLABS_META[closest_slab][i]], float(x), float(y), True, SLABS_META[closest_slab][i])

def tesselate(points, holes):
    vertices = []
    def edgeFlagCallback(param1, param2): pass
    def beginCallback(param=None):
        vertices = []
    def vertexCallback(vertex, otherData=None):
        vertices.append(vertex[:2])
    def combineCallback(vertex, neighbors, neighborWeights, out=None):
        out = vertex
        return out
    def endCallback(data=None): pass

    tess = gluNewTess()
    gluTessProperty(tess, GLU_TESS_WINDING_RULE, GLU_TESS_WINDING_ODD)
    gluTessCallback(tess, GLU_TESS_EDGE_FLAG_DATA, edgeFlagCallback)#forces triangulation of polygons (i.e. GL_TRIANGLES) rather than returning triangle fans or strips
    gluTessCallback(tess, GLU_TESS_BEGIN, beginCallback)
    gluTessCallback(tess, GLU_TESS_VERTEX, vertexCallback)
    gluTessCallback(tess, GLU_TESS_COMBINE, combineCallback)
    gluTessCallback(tess, GLU_TESS_END, endCallback)
    gluTessBeginPolygon(tess, 0)

    gluTessBeginContour(tess)
    for point in points:
        point3d = (point[0], point[1], 0)
        gluTessVertex(tess, point3d, point3d)
    gluTessEndContour(tess)

    if holes != []:
        for hole in holes:
            gluTessBeginContour(tess)
            for point in hole:
                point3d = (point[0], point[1], 0)
                gluTessVertex(tess, point3d, point3d)
            gluTessEndContour(tess)

    gluTessEndPolygon(tess)
    gluDeleteTess(tess)
    return vertices

#if args.polytype=='convex':
#    for i in range(len(POLYGON_LIST)):
#        POLYGON_LIST[i] = tesselate(POLYGON_LIST[i])
#    for points in POLYGON_LIST:
#        print(tesselate(points))

def drawConvex(points):
    global HEIGHT
    glColor(1, 1, 1)
    glBegin(GL_TRIANGLES)
    for vertex in points:
        glVertex(vertex[0], abs(vertex[1] - HEIGHT))
    glEnd()

def drawConvex2(points):
    global HEIGHT
    glColor(1, 1, 1)
    glBegin(GL_TRIANGLES)
    for vertex in points:
        glVertex(vertex[0], abs(vertex[1] - HEIGHT))
    glEnd()

def drawSlabs():
    global SLABS, WIDTH
    glColor(0,1,0)
    glBegin(GL_LINES)
    for slab in SLABS:
        glVertex(0, slab)
        glVertex(WIDTH, slab)
    glEnd()

def display_func():
    global POLYGON_LIST, args, HEIGHT, RGB_LIST
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT);
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    #draw_glpoly(points, 255, 255, 255)
    if args.polytype=='concave':
        if args.showbbox:
            if args.report:
                print('Rendering bounding boxes...')
                start = time.time()
                process = psutil.Process(os.getpid())
                mem_usage = float(process.memory_info().rss/1000000)
                print ('Current memory usage: ' + str(mem_usage) + ' MB')
            for points in BOUNDING_BOXES:
                #draw_polygon(points, r, g, b, HEIGHT, POLYGON_LIST)
                draw_polygon(points, 255, 0, 0, HEIGHT)
            if args.report:
                end = time.time()
                completion = end - start
                print('Completed! Execution time: ' + str(completion))
                mem_usage = float(process.memory_info().rss/1000000)
                print ('Current memory usage: ' + str(mem_usage) + ' MB')
        if args.algorithm=='slab':
            drawSlabs()
        if args.report:
            print('Rendering concave polygons...')
            start = time.time()
            process = psutil.Process(os.getpid())
            mem_usage = float(process.memory_info().rss/1000000)
            print ('Current memory usage: ' + str(mem_usage) + ' MB')
        for i in range(len(POLYGON_LIST)):
            #RGB_LIST[i][0] = 255
            #RGB_LIST[i][1] = 0
            #RGB_LIST[i][2] = 255
            draw_polygon(POLYGON_LIST[i], RGB_LIST[i][0], RGB_LIST[i][1], RGB_LIST[i][2], HEIGHT)
            #draw_polygon(POLYGON_LIST[i], 255, 255, 255, HEIGHT)
        #for points in POLYGON_LIST:
        #    draw_polygon(points, 255, 255, 255, HEIGHT)
        if args.report:
            end = time.time()
            completion = end - start
            print('Completed! Execution time: ' + str(completion))
            mem_usage = float(process.memory_info().rss/1000000)
            print ('Current memory usage: ' + str(mem_usage) + ' MB')
    elif args.polytype=='convex':
        for points in POLYGON_LIST:
            drawConvex(points)
        #drawConvex2(POLYGON_LIST[-1])
    #glPopMatrix();
    glutSwapBuffers()

def reshape_func(w, h):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, w, 0, h, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    width = w
    height = h

def ogl_setup(w, h):
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH | GLUT_STENCIL)
    glutInitWindowPosition (0,0)
    glutInitWindowSize(w, h)
    glutCreateWindow('Testando poligonos...')
    glClearColor(0.15, 0.15, 0.15, 1.0)

    glutDisplayFunc(display_func)
    glutReshapeFunc(reshape_func)

    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    #glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glDisable(GL_DEPTH_TEST);
    glDisable(GL_CULL_FACE);
    if args.mode=='mouse':
        glutMouseFunc(mouse)
    glutIdleFunc(glutPostRedisplay)
    glutMainLoop()

def create_convex_polygons():
    for i in range(args.polycount):
        polygon = [[0, 0], [550, 0], [550, 400], [275, 200], [0, 400]]
        hole1 = [[10, 10], [10, 100], [100, 100], [100, 10]]
        hole2 = [[300, 50], [350, 100], [400, 50], [350, 200]]
        #scale_size(0.6, [polygon, hole1, hole2])


        #poly_offsets, hole1_offsets, hole2_offsets = random_offset_list(polygon, hole1, hole2)
        #holes = [hole1_offsets, hole2_offsets]
        holes_test = [hole1, hole2]
        v = tesselate(polygon, holes_test)
        #v = tesselate(poly_offsets, holes=holes)
        #print(v)
        POLYGON_LIST.append(v)

def create_concave_polygons(WIDTH, HEIGHT, args):
    if args.report:
        print('Loading, scaling and offsetting meshes...')
        start = time.time()
        process = psutil.Process(os.getpid())
        mem_usage = float(process.memory_info().rss/1000000)
        print ('Current memory usage: ' + str(mem_usage) + ' MB')


    global POLYGON_LIST
    shape = shapefile.Reader('mesh/mongolia.shp')
    POLYGON_LIST = []

    for i in range(args.polycount):
        points = []
        for feature in shape.iterShapeRecords():
            for pf in feature.shape.points:
                points.append(list(pf))
        POLYGON_LIST.append(points)
    for points in POLYGON_LIST:
        scale_points(points, WIDTH, HEIGHT)
    for points in POLYGON_LIST:
        random_offset(points, WIDTH, HEIGHT)

    if args.report:
        end = time.time()
        completion = end - start
        print('Completed! Execution time: ' + str(completion))
        mem_usage = float(process.memory_info().rss/1000000)
        print ('Current memory usage: ' + str(mem_usage) + ' MB')


def create_bbox():
    if args.report:
        print('Creating bounding boxes...')
        start = time.time()

    global POLYGON_LIST, BOUNDING_BOXES, BBOX_META

    for points in POLYGON_LIST:
        bbox = BoundingBox(np.asarray(points))
        c1 = (bbox.minx, bbox.miny)
        c2 = (bbox.maxx, bbox.miny)
        c3 = (bbox.maxx, bbox.maxy)
        c4 = (bbox.minx, bbox.maxy)
        c5 = (bbox.minx, bbox.miny)
        c_list = [c1, c2, c3, c4, c5]
        BOUNDING_BOXES.append(c_list)
        BBOX_META.append(bbox)

    if args.report:
        end = time.time()
        completion = end - start
        print('Completed! Execution time: ' + str(completion))
        process = psutil.Process(os.getpid())
        mem_usage = float(process.memory_info().rss/1000000)
        print ('Current memory usage: ' + str(mem_usage) + ' MB')

def create_slabs(slab_count, h):
    global SLABS

    slab_offset = h/slab_count
    curr = 0

    for i in range(slab_count):
        SLABS.append(curr)
        curr+=slab_offset

def fill_slab_meta():
    global SLABS, SLABS_META, BBOX_META
    create_bbox()

    for asdf in range(len(SLABS)):
        polygon_list = []
        for i in range(len(BBOX_META)):
            if SLABS[asdf] > BBOX_META[i].miny and SLABS[asdf] < BBOX_META[i].maxy:
                polygon_list.append(i)
        SLABS_META.append(polygon_list)



def find_closest_slab(y):
    global SLABS
    aux = []
    for valor in SLABS:
        aux.append(abs(y-valor))

    return aux.index(min(aux))


def fill_RGB_list():
    global RGB_LIST, POLYGON_LIST

    for i in range(len(POLYGON_LIST)):
        r = 255#random.randint(0, 255)
        g = 255#random.randint(0,255)
        b = 255#random.randint(0, 255)
        rgb = [r, g, b]

        RGB_LIST.append(rgb)



################################################################################################################################
#   Execution portion                                                                                                          #
################################################################################################################################

#globals
WIDTH = 1280
HEIGHT = 720
POLYGON_LIST = []
BOUNDING_BOXES =[]
BBOX_META = []
SLABS = []
SLABS_META = []
RGB_LIST = []
args = add_args()

def main():
    global WIDTH, HEIGHT, POLYGON_LIST, BOUNDING_BOXES, BBOX_META, POLYGON_LIST_NP, SLABS, SLABS_META, RGB_LIST, args

    if args.report:
        print('Starting program...\nArguments given:')
        print('\tMode:\t\t\t\t' + args.mode)
        if args.mode=='pgen':
            print('\tRandom point count:\t' + str(args.pointcount))
        print('\tPolygon count:\t\t\t' + str(args.polycount))
        print('\tPolygon type:\t\t\t' + args.polytype)
        print('\tPoint inclusion algorithm:\t' + args.algorithm)
        if args.algorithm=='bbox':
            print('\tRender bounding boxes:\t\t' + str(args.showbbox))
        print('\tRender polygons in OpenGL:\t' + str(args.render))
        print('\n\n')


    if args.polytype=='concave':
        create_concave_polygons(WIDTH, HEIGHT, args)
        fill_RGB_list()
        #print(RGB_LIST[0][0])
        if args.algorithm=='bbox':
            create_bbox()
        elif args.algorithm=='slab':
            create_slabs(8, HEIGHT)
            fill_slab_meta()

    elif args.polytype=='convex':
        create_convex_polygons()

    if args.mode == 'pgen':
        point_gen(args.pointcount)

    if args.render:
        print('Rendering meshes in OpenGL...')
        ogl_setup(WIDTH, HEIGHT)


if __name__ == "__main__":
    main()
