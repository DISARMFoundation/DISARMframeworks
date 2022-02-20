from stix2 import Relationship, properties, ExternalReference


def make_disarm_subtechnique_relationship(source, target):
    """Creates a relationship between the parent technique and sub-technique.

    Args:
        source (str): Subtechnique ID
        target (str): Parent technique ID

    Returns:
        A Relationship object.

    """
    relationship = Relationship(
        source_ref=source,
        target_ref=target,
        relationship_type="subtechnique-of"
    )

    return relationship
