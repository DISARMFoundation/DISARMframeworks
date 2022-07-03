from stix2 import Relationship, properties, ExternalReference


def make_disarm_subtechnique_relationship(source, target, marking_id):
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
        description="",
        relationship_type="subtechnique-of",
        object_marking_refs=marking_id
    )

    return relationship


def make_disarm_subtechnique_relationships(techniques, marking_id):
    """Creates a map of technique and sub-technique.

    Args:
        techniques (list): List of STIX2 technique objects.

    Returns:
        A Relationship object.

    """
    technique_ids = {}
    for technique in techniques:
        technique_ids[technique["external_references"][0]["external_id"]] = technique["id"]

    relationships = []
    for technique in techniques:
        if technique["x_mitre_is_subtechnique"]:
            technique_id = technique_ids[technique["external_references"][0]["external_id"].split(".")[0]]
            relationship = make_disarm_subtechnique_relationship(technique["id"], technique_id, marking_id)
            relationships.append(relationship)

    return relationships
