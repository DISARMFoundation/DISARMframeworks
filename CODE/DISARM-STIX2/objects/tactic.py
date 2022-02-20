from stix2 import CustomObject, properties, ExternalReference

import objects.marking_definition
from objects import identity, marking_definition


@CustomObject('x-mitre-tactic', [
    ('name', properties.StringProperty(required=True)),
    ('description', properties.StringProperty(required=True)),
    ('x_mitre_shortname', properties.StringProperty(required=True)),
    ('external_references', properties.ListProperty(ExternalReference))
])
class Tactic(object):
    def __init__(self, x_mitre_shortname=None, **kwargs):
        if x_mitre_shortname and x_mitre_shortname not in ["strategic-planning", "objective-planning",
                                                           "develop-people", "develop-persona",
                                                           "develop-networks", "microtargeting", "develop-content",
                                                           "channel-selection", "pump-priming", "exposure",
                                                           "go-physical",
                                                           "persistence", "measure-effectiveness"]:
            # raise ValueError("'%s' is not a recognized DISARM Tactic." % x_mitre_shortname)
            print("'%s' is not a recognized DISARM Tactic." % x_mitre_shortname)


def make_disarm_tactics(data):
    """Create all DISARM tactic objects.

    Args:
        data: The xlsx tactic sheet.

    Returns:
        A list of Tactics.

    """
    tactics = []
    for t in data["tactics"].values.tolist():
        external_references = [
            {
                'external_id': f'{t[0]}',
                'source_name': 'DISARM',
                'url': f'https://github.com/DISARMFoundation/DISARM_framework/blob/master/tactics/{t[0]}.md'
            }
        ]

        tactic = Tactic(
            name=f"{t[1]}",
            description=f"{t[5]}",
            x_mitre_shortname=f'{t[1].lower().replace(" ", "-")}',
            external_references=external_references,
            object_marking_refs=objects.marking_definition.make_disarm_marking_definition(),
            created_by_ref=objects.identity.make_disarm_identity()
        )

        tactics.append(tactic)

    return tactics

