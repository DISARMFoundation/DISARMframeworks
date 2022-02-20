from stix2 import CustomObject, properties, ExternalReference

import objects.marking_definition
from objects import identity, marking_definition


@CustomObject('x-mitre-matrix', [
    ('name', properties.StringProperty(required=True)),
    ('description', properties.StringProperty(required=True)),
    ('tactic_refs', properties.ListProperty(properties.ReferenceProperty(valid_types="SDO"), required=True))
])
class Matrix(object):
    def __init__(self, **kwargs):
        if True:
            pass


def make_disarm_matrix(tactics):
    """Creates a Matrix object.

    Args:
        tactics: A list of Tactic objects.

    Returns:

    """
    description = 'DISARM is a framework designed for describing and understanding disinformation incidents.'
    external_references = [
        {
            "external_id": "DISARM",
            "source_name": "DISARM",
            "url": "https://github.com/DISARMFoundation"
        }
    ]
    name = 'DISARM Framework'

    # print(tactics)
    # p =[i.id for i in tactics]
    # r = properties.ReferenceProperty()
    # f = properties.ListProperty(r)

    tactic_refs = [i.id for i in tactics]

    matrix = Matrix(
        name=name,
        description=description,
        external_references=external_references,
        tactic_refs=tactic_refs,
        allow_custom=True
    )
    return [matrix]
