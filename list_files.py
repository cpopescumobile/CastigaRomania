#import sys

#sys.path.append('c:\Program Files\Python38\Lib\site-packages\cv2')

import os
import cv2
import numpy as np
import shutil
from pathlib import Path
import sys

if len(sys.argv) <= 1:
    print ('Please specify the prefix of the folder name')
    exit()
    
# the name of the folder which contains the frames
framesDir = sys.argv[1] + '-opencv'

# the name of the folder where all qualified image files are being copied to
selectedDir = sys.argv[1] + '_selected'

# the Y coordinate below which we want to count the green pixels
tresholdY = 470

# the minimum number of green pixels in an image file, needed, in order for the file to be copied to the selected folder
tresholdPixelCount = 5000


def append_count(filename, fileSuffix):
  p = Path(filename)
  return "{0}_{2}{1}".format(p.stem, p.suffix, fileSuffix)
  
def countGreenPixels(img):
    im = cv2.imread(img)

    ## convert to hsv
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    ## mask of green (36,25,25) ~ (86, 255,255)
    # mask = cv2.inRange(hsv, (36, 25, 25), (86, 255,255))
    mask = cv2.inRange(hsv, (36, 25, 25), (70, 255,255))

    ## slice the green
    imask = mask>0
    green = np.zeros_like(im, np.uint8)
    green[imask] = im[imask]
    
    indices = np.where(green != (0, 0, 0))
    coordinates = zip(indices[0], indices[1]) 
    unique_coordinates = list(set(list(coordinates)))
    
    countPixels = 0
    for tuple1 in unique_coordinates:
        if tuple1[0] > tresholdY:
            countPixels = countPixels + 1

    return countPixels
    
def copy_file(fileName, fileFullPath, filePixelCount):
    curDir = os.path.dirname(__file__)
    destDir = os.path.join(curDir, selectedDir)
    fileName = append_count(fileName, str(filePixelCount))
    destFileFullPath = os.path.join(destDir, fileName)
    
    shutil.copy(fileFullPath, destFileFullPath)
    
    print ('Copied: ', str(filePixelCount), str(fileName))
    
    return
    
def process_file(fileName, fileFullPath):
    filePixelCount = countGreenPixels(fileFullPath)
    
    print (str(filePixelCount), str(fileName))
    
    if filePixelCount > tresholdPixelCount:
        #qualified file
        process_file.newFile = True
        
        bestCount = filePixelCount
        bestCountFileName = fileName
        bestCountFileFullPath = fileFullPath
        
        if bestCount > process_file.bestFile[0]:
            process_file.bestFile = (bestCount, bestCountFileName, bestCountFileFullPath)
    else:
        # not qualified file anymore
        if process_file.newFile:
            # start copying the file only after the last consecutive qualified file was processed (because we need to select the best of those)
            copy_file(process_file.bestFile[1], process_file.bestFile[2], process_file.bestFile[0])
            process_file.newFile = False
            process_file.bestFile = (0, '', '')
    return
# process_file.newFile is a static like variable that turns to True when processing the first qualified image file, and turn False after all subsequent consecutive qualified files were processed and one of those files was selected to be copied
process_file.newFile = False

# process_file.bestFile is a static like tuple variable that keeps the details of the best qualified image file
process_file.bestFile = (0, '', '')

# iterate over files in that directory
for filename in os.listdir(framesDir):
    f = os.path.join(framesDir, filename)
    
    # checking if it is a file
    if os.path.isfile(f):
        process_file(filename, f)
        
