import os
import cv2
from iptcinfo3 import IPTCInfo
from PIL import Image
import re

DATADIR_RAW = 'C:/Users/xpn381/Documents/data/wetransfer-d44dd0/Simon_Tests_12092019/raw'
DATADIR_RAW_NEW = 'C:/Users/xpn381/Documents/data/wetransfer-d44dd0/Simon_Tests_12092019/raw_w_dates'

def get_date(DATADIR_RAW,DATADIR_RAW_NEW):
    
    '''Function wich takes as input path of dirs. in those dirs the function will irreterate throug all jpg, extract a date from their meta date and it a IPTC protocol'''
    
    # get the image name from the dir DATADIR_RAW
    for img in os.listdir(DATADIR_RAW):
        image_path = os.path.join(DATADIR_RAW, img)
        info = IPTCInfo(image_path, force=True)
        print(img)
        
        # Open the image and access the metadate. Use regex to extract date:
        image = Image.open(image_path) 
        txt = str(image.info['exif']) # exif are mostly JPEG
        r  = '[\d]{4}:[\d]{2}:[\d]{2}' # format yyyy:mm:dd
        date = re.search(r, txt).group().replace(':','')
        print(f'date of picture: {date}')
        
        # Force open the IPTC protocol to insert date
        info = IPTCInfo(image_path, force=True)
        print(f"info before: {info['date created']}") #Before. Shows wheter or not the entry was empty before
        info['date created'] = date 
        print(f"info after: {info['date created']}") # after. Shows the date extracted from the meta data
        print('\n')
        
        # Create the new dir DATADIR_RAW_NEW if it does not already exist
        if not os.path.exists(DATADIR_RAW_NEW):
            os.makedirs(DATADIR_RAW_NEW)
        
        # Create the new path for the image
        new_path = os.path.join(DATADIR_RAW_NEW, 'new' + img)
        
        # If that image is already in the path, delete it.
        if os.path.exists(DATADIR_RAW_NEW):
            try:
                os.remove(new_path)
            except:
                pass
        
        # Save new image.
        info.save_as(new_path)

# Run function
get_date(DATADIR_RAW,DATADIR_RAW_NEW)