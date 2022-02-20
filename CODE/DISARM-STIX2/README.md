# DISARM STIX2 Generator

## Usage

1. Clone this repository.
2. Download the latest version of the DISARM Framework xlsx [here](https://github.com/DISARMFoundation/DISARMframeworks).
3. Copy the xlsx to the root directory of this repository.
4. Run `python3 main.py` to generate STIX objects in the `output/` folder.
5. `output/DISARM.json` contains the complete STIX bundle.  The folders in `output/` contain individual objects for reference.

## DISARM STIX2

The DISARM STIX2 Generator encodes the DISARM object into the corresponding STIX2 object shown in the following table.

| DISARM    | STIX2                 |
|-----------|-----------------------|
| Matrix    | Matrix (MITRE custom) |
| Tactic    | Tactic (MITRE custom) |
| Technique | AttackPattern         |

## MITRE ATT&CK Navigator

DISARM STIX is compatible with the MITRE ATT&CK Navigator.

DISARM object types, such as `Matrix`, `Tatic` are prefixed with `x-mitre--` for compatibility reasons.

DISARM `AttackPattern` objects also contain `x_mitre_is_subtechnique` and `x_mitre_platforms` properties for compatability.  These properties cannot be removed without upstream changes to the ATT&CK Navigator.

## OpenCTI

DISARM STIX can be imported into OpenCTI via the OpenCTI STIX Importer plugin which is installed in OpenCTI by default.
Alternatively, use the OpenCTI DISARM plugin to continuously pull the latest DISARM STIX.

