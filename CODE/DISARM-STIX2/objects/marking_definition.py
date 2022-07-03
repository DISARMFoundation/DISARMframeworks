from stix2 import MarkingDefinition, StatementMarking
from objects import identity


def make_disarm_marking_definition(identity_id):
    marking_definition = MarkingDefinition(
        definition_type="statement",
        created_by_ref=identity_id,
        name="DISARM Foundation",
        definition=StatementMarking(statement="CC-BY-SA-4.0 DISARM Foundation")
    )
    return [marking_definition]
