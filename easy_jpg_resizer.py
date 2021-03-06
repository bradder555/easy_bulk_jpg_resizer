#!/usr/bin/python

from PIL import Image
from PIL import ExifTags

import sys
import os
import glob

from easy_arg_parse import easy_arg_parse

CURRENT_WORKING_DIR = os.getcwd()

if __name__ == '__main__':
    eap = easy_arg_parse.EasyArgParse\
            (
                defined_args=
                {
                    'input_dir':
                        {
                            'optional': False,
                            'help_text': "Directory containing jpgs"
                        },
                    'output_dir':
                        {
                            'optional': False,
                            'help_text': "The output directory"
                        },
                    'resize_ratio':
                        {
                            'optional': False,
                            'help_text': "How much you want to shrink the jpg as a fraction of 1 i.e. 0.75"
                        },
                    'resize_quality':
                        {
                            'optional': True,
                            "help_text": "The quality level of the saved jpg as a fraction of 1 i.e. 0.9"
                        }
                },
                aliases={
                    "i": "input_dir",
                    "in": "input_dir",
                    "o": "output_dir",
                    "out": "output_dir",
                    "ratio": "resize_ration",
                    "r": "resize_ratio",
                    "q": "resize_quality"
                }
            )
    args_dict = eap.parse()
    print("args:")
    print(args_dict)

    real_input_path = os.path.realpath(os.path.join(os.getcwd(), args_dict['input_dir']))
    print("Input path: " + real_input_path)

    real_output_path = os.path.realpath(os.path.join(os.getcwd(), args_dict['output_dir']))
    print("Output path: " + real_output_path)

    if not os.path.exists(real_output_path):
        os.makedirs(real_output_path)

    if not 'resize_quality' in args_dict:
        args_dict['resize_quality'] = 1

    print("resize_quality: " + str(args_dict['resize_quality']))
    
    list_of_files = []
    
    for e in ["jpg", "jpeg", "png", "bmp"]:
        list_of_files.extend(glob.glob(real_input_path + "/*" + e))
    
    print("list of files:")
    for file in list_of_files:
        file_name = os.path.split(file)[1]
        print("processing:\t" + file_name)
        with open(file, 'r+b') as f:
            with Image.open(f) as image:
                try:
                    for orientation in ExifTags.TAGS.keys():
                        if ExifTags.TAGS[orientation] == 'Orientation': break
                    exif = dict(image._getexif().items())

                    if exif[orientation] == 3:
                        image = image.rotate(180, expand=True)
                    elif exif[orientation] == 6:
                        image = image.rotate(270, expand=True)
                    elif exif[orientation] == 8:
                        image = image.rotate(90, expand=True)
                except:
                    pass

                # get original dimensions:
                prev_width = image.width
                prev_height = image.height
                ratio = args_dict['resize_ratio']
                new_width = int(prev_width * ratio)
                new_height = int(prev_height * ratio)
                print(
                    "prev dimensions: %ix%i\t new dimensions: %ix%i" %
                    (prev_width, prev_height, new_width, new_height))
                new_image = image.resize((new_width, new_height), Image.ANTIALIAS)
                #new_image = resizeimage.resize_cover(image, [new_width, new_height])
                new_image.save(
                    os.path.join(
                        real_output_path, file_name
                    ), image.format, quality=int(100*args_dict['resize_quality']))
