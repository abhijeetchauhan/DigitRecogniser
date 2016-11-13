import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
import cv2
import math
from scipy import ndimage
from sklearn.externals import joblib


def getBestShift(img):
    cy,cx = ndimage.measurements.center_of_mass(img)

    rows,cols = img.shape
    shiftx = np.round(cols/2.0-cx).astype(int)
    shifty = np.round(rows/2.0-cy).astype(int)

    return shiftx,shifty

def shift(img,sx,sy):
    rows,cols = img.shape
    M = np.float32([[1,0,sx],[0,1,sy]])
    shifted = cv2.warpAffine(img,M,(cols,rows))
    return shifted  

def predictDigit(img):
  clf = joblib.load('static/mlModel/digitrecogniser.pkl') 
  pca = joblib.load('static/pca/digitPca.pkl') 
  image = cv2.imread(img,0)

  # resize the images and invert it (black background)
  image = cv2.resize(255-image, (28, 28))
  (thresh, im_bw) = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
  while np.sum(im_bw[0]) == 0:
        im_bw = im_bw[1:]

  while np.sum(im_bw[:,0]) == 0:
        im_bw = np.delete(im_bw,0,1)

  while np.sum(im_bw[-1]) == 0:
        im_bw = im_bw[:-1]

  while np.sum(im_bw[:,-1]) == 0:
        im_bw = np.delete(im_bw,-1,1)

  rows,cols = im_bw.shape
  if rows > cols:
      factor = 20.0/rows
      rows = 20
      cols = int(round(cols*factor))
      im_bw = cv2.resize(im_bw, (cols,rows))
  else:
      factor = 20.0/cols
      cols = 20
      rows = int(round(rows*factor))
      im_bw = cv2.resize(im_bw, (cols, rows))
  colsPadding = (int(math.ceil((28-cols)/2.0)),int(math.floor((28-cols)/2.0)))
  rowsPadding = (int(math.ceil((28-rows)/2.0)),int(math.floor((28-rows)/2.0)))
  im_bw = np.lib.pad(im_bw,(rowsPadding,colsPadding),'constant')
  shiftx,shifty = getBestShift(im_bw)
  shifted = shift(im_bw,shiftx,shifty)
  im_bw = shifted
  im_bw = [val for sublist in im_bw for val in sublist]
  im_bw = np.array(im_bw)
  X = pca.transform(im_bw)
  predict=clf.predict(X)
  return predict