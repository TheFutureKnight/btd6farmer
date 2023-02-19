# width, height, top, left

import pytesseract

import numpy as np
import cv2
import sys
#import time

if sys.platform == "win32":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def formatImageOCR(originalScreenshot):
    screenshot = np.array(originalScreenshot, dtype=np.uint8)
    # Get local maximum:
    kernelSize = 5
    maxKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernelSize, kernelSize))
    localMax = cv2.morphologyEx(screenshot, cv2.MORPH_CLOSE, maxKernel, None, None, 1, cv2.BORDER_REFLECT101)
    # Perform gain division
    # print(screenshot, localMax)
    gainDivision = np.where(localMax == 0, 0, (screenshot / localMax))
    # Clip the values to [0,255]
    gainDivision = np.clip((255 * gainDivision), 0, 255)
    # Convert the mat type from float to uint8:
    gainDivision = gainDivision.astype("uint8")
    # Convert RGB to grayscale:
    grayscaleImage = cv2.cvtColor(gainDivision, cv2.COLOR_BGR2GRAY)
    # Resize image to improve the quality
    grayscaleImage = cv2.resize(grayscaleImage,(0,0), fx=3.0, fy=3.0)
    # Get binary image via Otsu:
    _, final_image = cv2.threshold(grayscaleImage, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # cv2.imwrite(f"./DEBUG/OCR_FORMAT_BINARY_IMAGE_{str(time.time())}.png", final_image, [cv2.IMWRITE_PNG_COMPRESSION, 0])

    # Set kernel (structuring element) size:
    kernelSize = 3
    # Set morph operation iterations:
    opIterations = 1
    # Get the structuring element:
    morphKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernelSize, kernelSize))
    # Perform closing:
    final_image = cv2.morphologyEx( final_image, cv2.MORPH_CLOSE, morphKernel, None, None, opIterations, cv2.BORDER_REFLECT101 )
    # cv2.imwrite(f"./DEBUG/OCR_FORMAT_BEFORE_FLOOD_{str(time.time())}.png", final_image, [cv2.IMWRITE_PNG_COMPRESSION, 0])

    # Flood fill (white + black):
    cv2.floodFill(final_image, mask=None, seedPoint=(int(0), int(0)), newVal=(255))
    # Invert image so target blobs are colored in white:
    final_image = 255 - final_image
    # Find the blobs on the binary image:
    contours, hierarchy = cv2.findContours(final_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Process the contours:
    for i, c in enumerate(contours):
        # Get contour hierarchy:
        currentHierarchy = hierarchy[0][i][3]
        # Look only for children contours (the holes):
        if currentHierarchy != -1:
            # Get the contour bounding rectangle:
            boundRect = cv2.boundingRect(c)
            # Get the dimensions of the bounding rect:
            rectX = boundRect[0]
            rectY = boundRect[1]
            rectWidth = boundRect[2]
            rectHeight = boundRect[3]
            # Get the center of the contour the will act as
            # seed point to the Flood-Filling:
            fx = rectX + 0.5 * rectWidth
            fy = rectY + 0.5 * rectHeight
            # Fill the hole:
            cv2.floodFill(final_image, mask=None, seedPoint=(int(fx), int(fy)), newVal=(0))
            # cv2.imwrite(f"./DEBUG/OCR_FLOOD_{i}_{str(time.time())}.png", final_image, [cv2.IMWRITE_PNG_COMPRESSION, 0])

    return final_image


# Change to https://stackoverflow.com/questions/66334737/pytesseract-is-very-slow-for-real-time-ocr-any-way-to-optimise-my-code 
# or https://www.reddit.com/r/learnpython/comments/kt5zzw/how_to_speed_up_pytesseract_ocr_processing/

def getTextFromImage(image):
    """ returns text from image """
    imageCandidate = formatImageOCR(image)
    # Write result to disk:
    
    # DEBUG log round to disk
    # import time
    # cv2.imwrite(f"./DEBUG/{str(time.time())}.png", imageCandidate, [cv2.IMWRITE_PNG_COMPRESSION, 0])

    # NOTE: This part seems to be buggy
    # Get current round from screenshot with tesseract
    return pytesseract.image_to_string(imageCandidate,  config='--psm 7').replace("\n", ""), imageCandidate

