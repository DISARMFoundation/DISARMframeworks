from stix2 import Identity


def make_disarm_identity():
    """Creates the default DISARM identity used for indicating authorship of various components in the bundle.

    Returns:
        identity: a STIX Identity object

    """
    identity = Identity(
        name="DISARM Foundation",
        identity_class="organization",
        description="DISARM is a framework designed for describing and understanding disinformation incidents.",
    )
    return [identity]
