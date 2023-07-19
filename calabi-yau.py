import math
import cmath
import bpy
import bmesh

pi = 3.141592653589793

# parametric functions
def cCos(theta, xi):
    val = (0.5 * (cmath.exp(xi + (1j * theta)))) + cmath.exp(-xi - (1j * theta))
    return val

def cSin(theta, xi):
    val = ((-0.5j) * (cmath.exp(xi + (1j * theta)))) - cmath.exp(-xi - (1j * theta))
    return val

def z1(theta, xi, n, k):
    val = cmath.exp(k * 2 * pi * 1j / n) * (cmath.cos(theta + (xi * 1j)) ** (2/n))
    return val

def z2(theta, xi, n, k):
    val = cmath.exp(k * 2 * pi * 1j / n) * (cmath.sin(theta + (xi * 1j)) ** (2/n))
    return val

def findPoint(theta, xi, n, k1, k2):
    angle = pi/4
    cosA = math.cos(angle)
    sinA = math.sin(angle)
    z1complex = z1(theta, xi, n, k1)
    z2complex = z2(theta, xi, n, k2)
    pt = (z1complex.real, z2complex.real, (z1complex.imag * cosA + z2complex.imag * sinA))
    indicator = (cmath.cos(theta + (xi * 1j)) ** n) + (cmath.sin(theta + (xi * 1j)) ** n)
    #print('theta: ' + str(theta) + ' xi: ' + str(xi) + ' k1: ' + str(k1) + ' k2: ' + str(k2) + ' 1.0: ' + str(indicator))
    return pt

def createMesh():
    n1 = 5
    n2 = 5
    xiSteps = 17
    xiMin = -1.0
    xiMax = 1.0
    xiStep = (xiMax - xiMin) / (xiSteps - 1)
    thetaSteps = 17
    thetaMin = 0
    thetaMax = pi/2
    thetaStep = (thetaMax - thetaMin) / (thetaSteps - 1)
    
    mesh = bpy.data.meshes.new("Calabi-YauMesh")  # add a new mesh
    obj = bpy.data.objects.new("Calabi-YauObj", mesh)  # add a new object using the mesh

    scene = bpy.context.scene
    scene.objects.link(obj)  # put the object into the scene (link)
    scene.objects.active = obj  # set as the active object in the scene
    obj.select = True  # select object

    mesh = bpy.context.object.data
    bm = bmesh.new()

    k1 = 0
    while(k1 < n1):
        k2 = 0
        while(k2 < n2):
            theta = thetaMin
            fudgeFactor = thetaStep * 0.1 # float comparison is unreliable
            while(theta <= (thetaMax + fudgeFactor)):
                xi = xiMin
                while(xi <= xiMax):
                    ptTuple = findPoint(theta, xi, n1, k1, k2)
                    bm.verts.new(ptTuple)
                    if((theta > thetaMin) and (xi > xiMin)):
                        bm.verts.ensure_lookup_table()
                        set_of_verts = (bm.verts[-xiSteps-1], bm.verts[-xiSteps-2], bm.verts[-2], bm.verts[-1])
                        bm.faces.new(set_of_verts)
                    xi += xiStep
                theta += thetaStep
            k2 += 1
        k1 += 1

    bm.to_mesh(mesh)  
    bm.free()
    return

createMesh()
