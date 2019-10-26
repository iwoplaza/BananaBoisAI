from Augmentor.Operations import Operation
from PIL import Image

class FitImage(Operation):
    # Here you can accept as many custom parameters as required:
    def __init__(self, probability, desired_size):
        # Call the superclass's constructor (meaning you must
        # supply a probability value):
        Operation.__init__(self, probability)

        self.desired_size = desired_size

    # Your class must implement the perform_operation method:
    def perform_operation(self, image):

        [im] = image

        old_size = im.size

        ratio = float(self.desired_size)/max(old_size)
        new_size = tuple([int(x*ratio) for x in old_size])

        im.thumbnail(new_size, Image.ANTIALIAS)

        new_im = Image.new("RGB", (self.desired_size, self.desired_size))
        new_im.paste(im, ((self.desired_size-new_size[0])//2,
                          (self.desired_size-new_size[1])//2))

        return [new_im]