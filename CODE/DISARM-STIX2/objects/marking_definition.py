from stix2 import MarkingDefinition, StatementMarking
from objects import identity


def make_disarm_marking_definition():
    marking_definition = MarkingDefinition(
        definition_type="statement",
        created_by_ref=identity.make_disarm_identity(),
        definition=StatementMarking(statement="CC-BY-SA-4.0 DISARM Foundation")
    )
    return marking_definition
