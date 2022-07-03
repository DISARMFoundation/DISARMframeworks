from stix2 import AttackPattern, properties, ExternalReference
import objects.marking_definition
import pandas as pd
from objects import identity, marking_definition


def make_disarm_techniques(data, identity_id, marking_id):
    """Create all DISARM Techniques objects.

    Args:
        data: The xlsx technique sheet.

    Returns:
        A list of Techniques.

    """
    tacdict = pd.Series(data["tactics"].name.values, index=data["tactics"].disarm_id).to_dict()
    techniques = []
    for t in data["techniques"].values.tolist():
        external_references = [
            {
                'external_id': f'{t[0]}'.strip(),
                'source_name': 'mitre-attack',
                'url': f'https://github.com/DISARMFoundation/DISARM_framework/blob/master/techniques/{t[0]}.md'
            }
        ]

        kill_chain_phases = [
            {
                'phase_name': tacdict[t[3]].replace(' ', '-').lower(),
                'kill_chain_name': 'mitre-attack'
            }
        ]

        subtechnique = t[0].split(".")
        x_mitre_is_subtechnique = False
        if len(subtechnique) > 1:
            x_mitre_is_subtechnique = True

        # MITRE ATT&CK Navigator expect techniques to have at least one of these platforms.
        # Without one, the technique will not render in the Navigator.
        x_mitre_platforms = 'Windows', 'Linux', 'Mac'

        technique = AttackPattern(
            name=f"{t[1]}",
            description=f"{t[4]}",
            external_references=external_references,
            object_marking_refs=marking_id,
            created_by_ref=identity_id,
            kill_chain_phases=kill_chain_phases,
            custom_properties={
                'x_mitre_platforms': x_mitre_platforms,
                'x_mitre_version': "2.1",
                'x_mitre_is_subtechnique': x_mitre_is_subtechnique
            }
        )

        techniques.append(technique)
    return techniques
