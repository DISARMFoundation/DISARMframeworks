from stix2 import CustomObject, properties, ExternalReference

import objects.marking_definition
from objects import identity, marking_definition

valid_tactics = ["plan-strategy", "plan-objectives", "microtarget", "develop-content",
                 "select-channels-and-affordances", "conduct-pump-priming", "deliver-content",
                 "drive-offline-activity", "persist-in-the-information-environment", "assess-effectiveness",
                 "target-audience-analysis", "develop-narratives", "establish-social-assets", "establish-legitimacy",
                 "maximize-exposure", "drive-online-harms"]

@CustomObject('x-mitre-tactic', [
    ('name', properties.StringProperty(required=True)),
    ('description', properties.StringProperty(required=True)),
    ('x_mitre_shortname', properties.StringProperty(required=True)),
    ('external_references', properties.ListProperty(ExternalReference))
])
class Tactic(object):
    def __init__(self, x_mitre_shortname=None, **kwargs):
        if x_mitre_shortname and x_mitre_shortname not in valid_tactics:
            raise ValueError("'%s' is not a recognized DISARM Tactic." % x_mitre_shortname)


def make_disarm_tactics(data, identity_id, marking_id):
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
            object_marking_refs=marking_id,
            created_by_ref=identity_id
        )

        tactics.append(tactic)

    return tactics

