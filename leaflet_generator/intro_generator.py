from array_utils import getRandomChoice

typeToNameMap = {
    'house': 'House',
    'dining_room': 'Dining room',
    'kitchen': 'Kitchen',
    'bathroom': 'Bathroom',
    'living_room': 'Living room',
    'bedroom': 'Bedroom'
}

formats = [
    'This is the {}.',
    'This beautiful {} is the cherry on top.',
    'Now for the {}.',
    'Take a look at the {}.',
    'The {}... what a room.',
    'Ah... the {}.',
]

class IntroGenerator:

    def __init__(self):
       pass

    def generate(self, room_type, description_index):
        random_format = getRandomChoice(formats)
        return random_format.format(typeToNameMap[room_type].lower())