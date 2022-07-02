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


def make_disarm_subtechnique_relationships(techniques, subtechniques):
    """Creates a map of technique and sub-technique.

    Args:
        techniques (list): List of STIX2 technique objects.
        subtechniques (list): List of STIX2 subtechnique objects.

    Returns:
        A Relationship object.

    """
    technique_ids = {}
    for technique in techniques:
        technique_ids[technique["external_references"][0]["external_id"]] = technique["id"]

    relationships = []
    for subtechnique in subtechniques:
        technique_id = technique_ids[subtechnique["external_references"][0]["external_id"].split(".")[0]]
        relationship = make_disarm_subtechnique_relationship(subtechnique["id"], technique_id)
        relationships.append(relationship)

    return relationships
