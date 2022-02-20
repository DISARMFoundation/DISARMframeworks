from stix2 import Bundle


def make_stix_bundle(stix_objects):
    """Makes a STIX Bundle object.

    Args:
        stix_objects (list): A list of STIX objects.

    Returns:
        Bundle: A STIX Bundle object.

    """
    bundle = Bundle(stix_objects, allow_custom=True)
    return bundle
