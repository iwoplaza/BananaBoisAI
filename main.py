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
from description_generator import generateDescription
from PyPDF2 import PdfFileMerger
import pdfkit

class Room:
    image_dir = ""
    
    # konstruktor - określa jakie labele kategoryzują dane zdjęcie (HTML)
    def __init__(self, index, image_path, json_data, templater):
        self.index = index
        self.image_path = image_path
        self.json_data = json_data
        self.templater = templater

        self.tags = [key for (key, value) in json_data]
        
    def fillSheet(self):
        # self.worksheet['F4'] = self.room_type
        # ''' , roomAverageScore '''

        self.templater.replace({
            f'room_{self.index}': f'''
                <section class="room">
                    <div class="picture" alt="Real estate picture" style="background-image: url(<!-- model-replace: picture-src_{self.index} -->)"></div>
                    <p class="description"><!-- model-replace: description_{self.index} --></p>
                </section>
                <!-- model-replace: room_{self.index + 1} -->
            ''',
            f'description_{self.index}': generateDescription(self.tags),
            'tags': ', '.join(self.tags),
            'floor-area': random.randint(7, 30),
        })

        self.templater.replaceImage(f'picture-src_{self.index}', self.image_path)
        

    def mergePDF(self, fin_report_path, fin_report_name, *pdf_files):
        merger = PdfFileMerger()
        for pdf_file in pdf_files:
            merger.append(fin_report_path + pdf_file)
        if not os.path.exists(fin_report_path + fin_report_name):
            merger.write(fin_report_path + fin_report_name)
        merger.close()


testPath = glob('test*')
 
config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

templater = HTMLTemplater('template.html', config=config)

for test in testPath:
    summary_path = path.join(test, 'summary.txt')

    with open(summary_path, 'r') as summary_file:
        summary = summary_file.read()
        data = [x.split(', ') for x in summary.splitlines()]

        # start merge
        index = 0
        for (image_filename, room_class) in data:
            json_filename = image_filename + '.json'
            json_path = path.join(test, json_filename)

            # load json
            with open(json_path) as json_file:
                json_data = json.load(json_file)
                json_data = [(entry['name'], entry['score']) for entry in json_data]
                
                room = Room(index, path.join(test, image_filename), json_data, templater)
                room.fillSheet()

            index = index + 1

with open("myfile.html", "w") as file1: 
  
    file1.write(templater.template) 

templater.save('out.pdf')


# with open(csvPath) as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter = ',')

#     workbook = HTMLTemplater('template.html')

#     header = None
#     for row in csv_reader:
#         if not header:
#             header = row
#             continue
        
#         line = Line(header, row, workbook)
#         line.fillSheet()
#         line.putImage()
#         line.convertFile()
#         break

    