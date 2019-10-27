#file name main.py
#sheetset name Template.xlsx
#labels.csv
'''
    Image: A5
    Room name: F4
    surface area: G6
    tech spec: G7
    visual spec: G8
    Include(hashtags):
    F10
'''
#array to specify visual look
#visualspec = ['Gross',  'Bad', 'Nice', 'Awesome']
#techspec = ['Imposible to live', 'Liveable', 'OK', 'Like a new']
import csv
import random
from glob import glob
from os import path
import os
import json

from htmltemplater import HTMLTemplater
from description_generator import DescriptionGenerator
import pdfkit

class Room:
    def __init__(self, index, room_type, image_path, json_data, templater):
        self.index = index
        self.room_type = room_type
        self.image_path = image_path
        self.json_data = json_data
        self.templater = templater

        self.tags = [key for (key, value) in json_data]
        
    def fillSheet(self):

        # ''' , roomAverageScore '''
        description_generator = DescriptionGenerator()

        self.templater.replace({
            f'room_{self.index}': f'''
                <section class="room">
                    <div class="picture" alt="Real estate picture" style="background-image: url(<!-- model-replace: picture-src_{self.index} -->)"></div>
                    <p class="description"><!-- model-replace: description_{self.index} --></p>
                </section>
                <!-- model-replace: room_{self.index + 1} -->
            ''',
            f'description_{self.index}': description_generator.generate(self.json_data),
            'tags': ', '.join(self.tags),
            'floor-area': random.randint(7, 30),
        })

        self.templater.replaceImage(f'picture-src_{self.index}', self.image_path)


def loadRoomFromJSON(json_path, index, room_type, image_path, templater):
    with open(json_path) as json_file:
        json_data = json.load(json_file)
        json_data = [(entry['name'], entry['score']) for entry in json_data]
        
        return Room(index, room_type, image_path, json_data, templater)

def generatePDFs(glob_pattern, out_dir, path_to_lib, out_format = 'pdf'):
    test_paths = glob(glob_pattern)
    config = pdfkit.configuration(wkhtmltopdf=path_to_lib)

    for test_path in test_paths:
        summary_path = path.join(test_path, 'summary.txt')

        if not path.isfile(summary_path):
            continue

        templater = HTMLTemplater('template.html', config=config)

        with open(summary_path, 'r') as summary_file:
            summary = summary_file.read()
            data = [row.split(', ') for row in summary.splitlines()]

            index = 0
            for (image_filename, room_type) in data:
                json_filename = f'{image_filename}.json'
                json_path = path.join(test_path, json_filename)

                # load json
                room = loadRoomFromJSON(json_path, index, room_type, path.join(test_path, image_filename), templater)
                room.fillSheet()

                index = index + 1
        
        if out_format == 'pdf':
            templater.save(path.join(out_dir, f'{path.basename(test_path)}.pdf'))
        else:
            with open(path.join(out_dir, f'{path.basename(test_path)}.html'), 'w') as output_file:
                output_file.write(templater.template)

import sys, getopt

if __name__ == '__main__':
    input_pattern = 'test*'
    output_dir = ''
    path_to_lib = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
    out_format = 'pdf'

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:o:l:f:', ['in=', 'out=', 'lib=', 'format='])
    except getopt.GetoptError:
        print('main.py -i <inputpattern> -o <outputdir>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-i', '--in'):
            input_pattern = arg
        elif opt in ('-o', '--out'):
            output_dir = arg
        elif opt in ('-l', '--lib'):
            path_to_lib = arg
        elif opt in ('-f', '--format'):
            out_format = arg

    generatePDFs(input_pattern, output_dir, path_to_lib, out_format)
