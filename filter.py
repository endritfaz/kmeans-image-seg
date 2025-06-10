import argparse
from PIL import Image 
import random 

parser = argparse.ArgumentParser(description="Applies a K-Means filter to an image")

parser.add_argument("-i",
                    "--imageDir", 
                    help="Path to the image which the filter will be applied to",
                    required=True)

parser.add_argument("-n",
                    "--numCentres", 
                    help="The number of centres for K-Means",
                    required=True)

# Applies K-Means segmentation to image and displays it 
def filter(imageDir, numCentres):
    img = Image.open(imageDir)

    pixels = list(img.getdata())
    newPixels = [0]*len(pixels)
    centres = genRandomCentres(numCentres)
    
    i = 0
    while(True):
        i += 1
        closestPoints = expectation(pixels, centres)
        centresChanged = maximisation(closestPoints, centres)

        if not centresChanged:
            break
        print(str(i) + ":" + str(centres[0]) + ", " + str(centres[1]))
    
    for i in range(len(centres)): 
        centres[i] = tuple(int(x) for x in centres[i])

    for i in range(len(pixels)):
        pixel = pixels[i]
        distances = [squaredDistance(pixel, centre) for centre in centres]
        closestCentreIndex = distances.index(min(distances))
        newPixels[i] = centres[closestCentreIndex]
    
    filterImg = Image.new("RGB", img.size)
    filterImg.putdata(newPixels)

    img.show()
    filterImg.show()

# Calculates new centres as the mean of all the points closest to that centre 
def maximisation(centrePoints, centres): 
    centresChanged = False 
    for i in range(len(centres)): 
        oldCentre = centres[i]
        if (len(centrePoints[i]) > 0):
            newCentre = averagePoints(centrePoints[i])
        else: 
            newCentre = oldCentre

        if (newCentre != oldCentre):
            centresChanged = True 
            centres[i] = newCentre

    return centresChanged 

# Calculates the centres to which each point is assigned 
def expectation(points, centres): 
    closestPoints = [[] for centre in centres]

    for point in points: 
        distances = [squaredDistance(point, centre) for centre in centres]
        closestCentreIndex = distances.index(min(distances))
        closestPoints[closestCentreIndex].append(point)
    
    return closestPoints 

def averagePoints(points): 
    return tuple(map(lambda x: sum(x)/len(points), zip(*points)))

def squaredDistance(x1, x2): 
    if (len(x1) != len(x2)):
        return 

    squaredDistance = 0
    for i in range(len(x1)): 
        squaredDistance += (x1[i] - x2[i])**2

    return squaredDistance

def genRandomCentres(n):
    return [(random.random()*255, random.random()*255, random.random()*255) for i in range(n)]; 
    
args = parser.parse_args()

filter(args.imageDir, int(args.numCentres))