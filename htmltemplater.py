import pdfkit
import base64

class HTMLTemplater:

    def __init__(self, filepath, config):
        self.template = None
        with open(filepath, 'r') as file:
            self.template = file.read()

        self.config = config


    def replace(self, fillMap):
        for (key, value) in fillMap.items():
            self.template = self.template.replace(f'<!-- model-replace: {key} -->', str(value))


    def replaceImage(self, key, filepath):
        with open(filepath, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read())
            print(encoded_string[:40])
            encoded_string = 'data:image/jpeg;base64,' + encoded_string.decode('utf-8')

            self.template = self.template.replace(f'<!-- model-replace: {key} -->', encoded_string)


    def save(self, outpath):
        pdfkit.from_string(self.template, outpath, configuration=self.config, css='./style.css')
    