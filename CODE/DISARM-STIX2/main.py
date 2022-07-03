# A STIX bundle generator for the DISARM Framework.
#
# Author: Roger Johnston, Twitter: @VV_X_7
# License: GPL-3

import pandas as pd
import openpyxl
from stix2 import (Bundle, AttackPattern, ThreatActor, IntrusionSet, Relationship, CustomObject, properties,
                   Malware, Tool, Campaign, Identity, MarkingDefinition, ExternalReference, StatementMarking,
                   GranularMarking, Location, MemoryStore, Filter)
from stix2.properties import (ReferenceProperty, ListProperty, StringProperty, TimestampProperty, BooleanProperty, IntegerProperty)

import helpers
from objects import tactic, technique, matrix, bundle, relationship, identity, marking_definition
from helpers import xlsx, file


def generate_disarm_stix():
    """Generates a DISARM STIX bundle.

    Returns:

    """
    data = helpers.xlsx.load_excel_data("../DISARM_MASTER_DATA/DISARM_FRAMEWORKS_MASTER.xlsx")

    disarm_identity = identity.make_disarm_identity()
    identity_id = disarm_identity[0]["id"]
    disarm_marking_definition = marking_definition.make_disarm_marking_definition(identity_id)
    marking_id = disarm_marking_definition[0]["id"]

    tactics = tactic.make_disarm_tactics(data, identity_id, marking_id)
    techniques = technique.make_disarm_techniques(data, identity_id, marking_id)
    subtechnique_relationships = relationship.make_disarm_subtechnique_relationships(techniques, marking_id)
    navigator_matrix = matrix.make_disarm_matrix(tactics)

    stix_objects = []
    stix_objects.append(tactics)
    stix_objects.append(techniques)
    stix_objects.append(subtechnique_relationships)
    stix_objects.append(disarm_identity)
    stix_objects.append(disarm_marking_definition)
    stix_objects.append(navigator_matrix)
    stix_objects = [item for sublist in stix_objects for item in sublist]
    disarm_bundle = bundle.make_stix_bundle(stix_objects)
    helpers.file.clean_output_dir()
    helpers.file.write_files(stix_objects)
    helpers.file.write_bundle(disarm_bundle, "DISARM")


if __name__ == "__main__":
    generate_disarm_stix()