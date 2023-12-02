#!/usr/bin/env python3
"""
Generate DISARM MISP galaxy
    see also https://github.com/MISP/misp-galaxy

Author: Christophe Vandeplas
License: AGPL-3
"""

from generate_DISARM_pages import Disarm
import json
import uuid
import os


class DisarmGalaxy:
    def __init__(self, out_path=os.path.join('..', '..', 'misp-galaxy')):
        self.disarm = Disarm()
        self.out_path = out_path

    def generate_disarm_galaxy(self):
        galaxy = {'name': 'DISARM Techniques',
                  'type': 'disarm',
                  'description': 'DISARM is a framework designed for describing and understanding disinformation incidents.',
                  'uuid': str(uuid.uuid5(uuid.UUID("9319371e-2504-4128-8410-3741cebbcfd3"), 'disarm-galaxy-techniques')),
                  'version': 1,
                  'icon': 'map',
                  'namespace': 'disarm',
                  'kill_chain_order': {
                      'disarm-tactics': []
                  }}

        for k, v in self.disarm.tactics.items():
            galaxy['kill_chain_order']['disarm-tactics'].append(f'{v}')

        self.write_json_file(os.path.join(self.out_path, 'galaxies', 'disarm-techniques.json'), galaxy)

    def write_json_file(self, fname, file_data):
        with open(fname, 'w') as f:
            json.dump(file_data, f, indent=2, sort_keys=True, ensure_ascii=False)
            f.write('\n')

    def generate_disarm_clusters(self):
        cluster = {'authors': ['DISARM Project'],
                   'category': 'disarm',
                   'description': 'DISARM is a framework designed for describing and understanding disinformation incidents.',
                   'name': 'DISARM Techniques',
                   'source': 'https://github.com/misinfosecproject/amitt_framework',
                   'type': 'disarm',
                   'uuid': str(uuid.uuid5(uuid.UUID("9319371e-2504-4128-8410-3741cebbcfd3"), 'disarm-cluster-techniques')),
                   'values': [],
                   'version': 1}

        df = self.disarm.df_techniques
        for i in range(len(df)):
            t = {
                'uuid': str(uuid.uuid5(uuid.UUID("9319371e-2504-4128-8410-3741cebbcfd3"), df.values[i][0])),
                'value': f"{df.values[i][0]} - {df.values[i][1]}",
                'description': df.values[i][4],
                'meta': {
                    'external_id': df.values[i][0],
                    'kill_chain': [
                        f'disarm-tactics:{self.disarm.tactics[df.values[i][3]]}'
                    ],
                    'refs': [
                        f'https://github.com/DISARMFoundation/DISARMframeworks/blob/main/generated_pages/techniques/{df.values[i][0]}.md'
                    ]
                }
            }

            cluster['values'].append(t)

        self.write_json_file(os.path.join(self.out_path, 'clusters', 'disarm-techniques.json'), cluster)

        pass


def main():
    disarm_galaxy = DisarmGalaxy()
    disarm_galaxy.generate_disarm_galaxy()
    disarm_galaxy.generate_disarm_clusters()


if __name__ == "__main__":
    main()
    print("All done, please look at the delta, and update the version number if needed.")
    print("After that do ./jq_all_the_things.sh, commit, and then ./validate_all.sh.")
