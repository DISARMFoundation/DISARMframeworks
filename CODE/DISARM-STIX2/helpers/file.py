import json
import os
from stix2 import Bundle
import shutil

outdir = '../generated_files/DISARM_STIX/'

def write_disarm_dir(dir, outdir=outdir):
    """

     Args:
        dir (str): a directory name

    Returns:

    """
    try:
        os.mkdir(outdir)
    except FileExistsError:
        pass

    try:
        os.mkdir(outdir + dir)
    except FileExistsError:
        pass


def clean_output_dir(outdir=outdir):
    """Recursively delete the output folder.

    Returns:

    """
    try:
        os.mkdir(outdir)
    except FileExistsError:
        pass

    shutil.rmtree(outdir)


def write_file(file_name, file_data):
    """Write a JSON file to outdir

    Args:
        file_name (str): a file name
        file_data (str): the file json data

    Returns:

    """
    with open(file_name, 'w') as f:
        # f.write(json.dumps(file_data, sort_keys=True, indent=4))
        f.write(file_data.serialize(pretty=True))
        f.write('\n')


def write_files(stix_objects, outdir=outdir):
    """

    Args:
        stix_objects:

    Returns:

    """
    for i in stix_objects:
        write_disarm_dir(i.type)
        write_file(outdir+f"{i.type}/{i.id}.json", Bundle(i, allow_custom=True))


def write_bundle(bundle, bundle_name, outdir=outdir):
    """

    Args:
        bundle:
        bundle_name:

    Returns:

    """
    write_file(outdir+f"{bundle_name}.json", bundle)
