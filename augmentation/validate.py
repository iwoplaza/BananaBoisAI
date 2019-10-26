from Augmentor.Operations import Operation
from PIL import Image

class ValidateImage(Operation):
    # Here you can accept as many custom parameters as required:
    def __init__(self, probability):
        # Call the superclass's constructor (meaning you must
        # supply a probability value):
        Operation.__init__(self, probability)

    # Your class must implement the perform_operation method:
    def perform_operation(self, image):

        [im] = image

        try:
            im.load()
        except:
            print("ERROR")
            return []

        return image