#file name main.py

import csv
import random
from glob import glob
from os import path
import os
import json
import math

from PyPDF2 import PdfFileMerger
from htmltemplater import HTMLTemplater
from description_generator import DescriptionGenerator
import pdfkit

pdfArray = []

keyToName = {
    'house': 'House',
    'dining_room': 'Dining room',
    'kitchen': 'Kitchen',
    'bathroom': 'Bathroom',
    'living_room': 'Living room',
    'bedroom': 'Bedroom'
}

class Room:
    def __init__(self, index, room_type, image_path, json_data, templater):
        self.index = index
        self.room_type = room_type
        self.image_path = image_path
        self.json_data = json_data
        self.templater = templater

        self.tags = [key for (key, value) in json_data]
        self.score = [value for (key, value) in json_data]
        self.avgscore = sum(self.score) / len(self.score)
        
        
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
        })

        self.templater.replaceImage(f'picture-src_{self.index}', self.image_path)


def presentTypesInHumanForm(types):
    d = {}
    for t in types:
        d[t] = d[t] + 1 if t in d else 1
    
    return d

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

            room_types = []
            index = 0
            avgscore = []
            for (image_filename, room_type) in data:
                room_types.append(room_type)

                json_filename = f'{image_filename}.json'
                json_path = path.join(test_path, json_filename)

                # load json
                room = loadRoomFromJSON(json_path, index, room_type, path.join(test_path, image_filename), templater)
                room.fillSheet()
                avgscore.append(room.avgscore)
                index = index + 1
        
        def presentTuple(entry):
            item = entry[0]
            amount = entry[1]
            return f'{amount} x {keyToName[item]}' if amount > 1 else keyToName[item]
        floor_area = len(room_types) * random.randint(8, 25)
        finalScore = sum(avgscore) / len(avgscore)
        price = math.ceil(floor_area * 970 * finalScore)
        room_types = presentTypesInHumanForm(room_types)
        templater.replace({
            'room-types': ", ".join([presentTuple(entry) for entry in room_types.items()]),
            'price': price,
            'floor-area': floor_area,
            'final-score': finalScore
        })
        
        if out_format == 'pdf':
            templater.save(path.join(out_dir, f'{path.basename(test_path)}.pdf'))

        else:
            with open(path.join(out_dir, f'{path.basename(test_path)}.html'), 'w') as output_file:
                output_file.write(templater.template)

import sys, getopt

if __name__ == '__main__':
    input_pattern = 'test*'
    output_dir = ''
    path_to_lib = 'C:\\Program Files (x86)\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
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
    #merger = PdfFileMerger()
    listpdf = glob(path.join(output_dir, 'test*.pdf') )
    print(listpdf)
    for pdf in listpdf:
        pdfArray.append(pdf)
    merger = PdfFileMerger()

    for pdf in pdfArray:
        merger.append(pdf)
    print(merger)
    merger.write("result.pdf")
    merger.close()

