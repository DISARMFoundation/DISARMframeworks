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

DISARM_DESCRIPTION = 'DISARM is a framework designed for describing and understanding disinformation incidents.'
DISARM_CATEGORY = 'disarm'
DISARM_AUTHORS = ['DISARM Project']
DISARM_SOURCE = 'https://github.com/DISARMFoundation/DISARMframeworks'
CORE_UUID = "9d6bd9d2-2cd3-4900-b61a-06cd64df3996"

class DisarmGalaxy:
    def __init__(self, out_path=os.path.join('..', '..', 'misp-galaxy')):
        self.disarm = Disarm()
        self.out_path = out_path

    def write_json_file(self, fname, file_data):
        with open(fname, 'w') as f:
            json.dump(file_data, f, indent=2, sort_keys=True, ensure_ascii=False)
            f.write('\n')

    def generate_disarm_techniques_galaxy(self):
        galaxy = {'name': 'Techniques',
                  'type': 'disarm-techniques',
                  'description': DISARM_DESCRIPTION,
                  'uuid': str(uuid.uuid5(uuid.UUID(CORE_UUID), 'disarm-galaxy-techniques')),
                  'version': 1,
                  'icon': 'map',
                  'namespace': 'disarm',
                  'kill_chain_order': {
                      'tactics': []
                  }}

        for k, v in self.disarm.tactics.items():
            galaxy['kill_chain_order']['tactics'].append(f'{v}')

        self.write_json_file(os.path.join(self.out_path, 'galaxies', 'disarm-techniques.json'), galaxy)

    def generate_disarm_techniques_clusters(self):
        cluster = {'authors': DISARM_AUTHORS,
                   'category': DISARM_CATEGORY,
                   'description': DISARM_DESCRIPTION,
                   'name': 'Techniques',
                   'source': DISARM_SOURCE,
                   'type': 'disarm-techniques',
                   'uuid': str(uuid.uuid5(uuid.UUID(CORE_UUID), 'disarm-cluster-techniques')),
                   'values': [],
                   'version': 1}
        values = []
        df = self.disarm.df_techniques
        for i in range(len(df)):
            t = {
                'uuid': str(uuid.uuid5(uuid.UUID(CORE_UUID), df.values[i][0])),
                'value': df.values[i][1],
                'description': df.values[i][4],
                'meta': {
                    'external_id': df.values[i][0],
                    'kill_chain': [
                        f'tactics:{self.disarm.tactics[df.values[i][3]]}'
                    ],
                    'refs': [
                        f'https://github.com/DISARMFoundation/DISARMframeworks/blob/main/generated_pages/techniques/{df.values[i][0]}.md'
                    ]
                }
            }

            values.append(t)
        cluster['values'] = sorted(values, key=lambda x: x['meta']['external_id'])
        self.write_json_file(os.path.join(self.out_path, 'clusters', 'disarm-techniques.json'), cluster)

    def generate_disarm_countermeasures_galaxy(self):
        galaxy = {'name': 'Countermeasures',
                  'type': 'disarm-countermeasures',
                  'description': DISARM_DESCRIPTION,
                  'uuid': str(uuid.uuid5(uuid.UUID(CORE_UUID), 'disarm-galaxy-counters')),
                  'version': 1,
                  'icon': 'shield-alt',
                  'namespace': 'disarm',
                  'kill_chain_order': {
                      'tactics': [],
                      'responsetypes': [],
                      'metatechniques': []
                  }}

        for k, v in self.disarm.tactics.items():
            galaxy['kill_chain_order']['tactics'].append(f'{v}')
        for k, v in self.disarm.responsetypes.items():
            galaxy['kill_chain_order']['responsetypes'].append(f'{v}')
        for k, v in self.disarm.metatechniques.items():
            galaxy['kill_chain_order']['metatechniques'].append(f'{v}')

        self.write_json_file(os.path.join(self.out_path, 'galaxies', 'disarm-countermeasures.json'), galaxy)

    def generate_disarm_countermeasures_clusters(self):
        cluster = {'authors': DISARM_AUTHORS,
                   'category': DISARM_CATEGORY,
                   'description': DISARM_DESCRIPTION,
                   'name': 'Countermeasures',
                   'source': DISARM_SOURCE,
                   'type': 'disarm-countermeasures',
                   'uuid': str(uuid.uuid5(uuid.UUID(CORE_UUID), 'disarm-cluster-counters')),
                   'values': [],
                   'version': 1}
        values = []
        df = self.disarm.df_counters
        for i in range(len(df)):
            kill_chain = []
            if self.disarm.tactics[df.values[i][15]]:
                kill_chain.append(f'tactics:{self.disarm.tactics[df.values[i][15]]}')
            if self.disarm.responsetypes[df.values[i][10]]:
                kill_chain.append(f'responsetypes:{self.disarm.responsetypes[df.values[i][10]]}')
            if self.disarm.metatechniques[df.values[i][17]]:
                kill_chain.append(f'metatechniques:{self.disarm.metatechniques[df.values[i][17]]}')

            t = {
                'uuid': str(uuid.uuid5(uuid.UUID(CORE_UUID), df.values[i][0])),
                'value': df.values[i][1],
                'description': df.values[i][3],
                'meta': {
                    'external_id': df.values[i][0],
                    'kill_chain': kill_chain,
                    'refs': [
                        f'https://github.com/DISARMFoundation/DISARMframeworks/blob/main/generated_pages/counters/{df.values[i][0]}.md'
                    ]
                }
            }

            values.append(t)
        cluster['values'] = sorted(values, key=lambda x: x['meta']['external_id'])
        self.write_json_file(os.path.join(self.out_path, 'clusters', 'disarm-countermeasures.json'), cluster)

    def generate_disarm_detections_galaxy(self):
        galaxy = {'name': 'Detections',
                  'type': 'disarm-detections',
                  'description': DISARM_DESCRIPTION,
                  'uuid': str(uuid.uuid5(uuid.UUID(CORE_UUID), 'disarm-galaxy-detections')),
                  'version': 1,
                  'icon': 'bell',
                  'namespace': 'disarm',
                  'kill_chain_order': {
                      'tactics': [],
                      'responsetypes': [],
                      # 'metatechniques': []
                  }}

        for k, v in self.disarm.tactics.items():
            galaxy['kill_chain_order']['tactics'].append(f'{v}')
        for k, v in self.disarm.responsetypes.items():
            galaxy['kill_chain_order']['responsetypes'].append(f'{v}')
        # for k, v in self.disarm.metatechniques.items():
        #     galaxy['kill_chain_order']['metatechniques'].append(f'{v}')

        self.write_json_file(os.path.join(self.out_path, 'galaxies', 'disarm-detections.json'), galaxy)

    def generate_disarm_detections_clusters(self):
        cluster = {'authors': DISARM_AUTHORS,
                   'category': DISARM_CATEGORY,
                   'description': DISARM_DESCRIPTION,
                   'name': 'Detections',
                   'source': DISARM_SOURCE,
                   'type': 'disarm-detections',
                   'uuid': str(uuid.uuid5(uuid.UUID(CORE_UUID), 'disarm-cluster-detections')),
                   'values': [],
                   'version': 1}
        values = []
        df = self.disarm.df_detections
        for i in range(len(df)):

            kill_chain = []
            try:
                if self.disarm.tactics[df.values[i][14]]:
                    kill_chain.append(f'tactics:{self.disarm.tactics[df.values[i][14]]}')
            except KeyError:
                pass
            try:
                if self.disarm.responsetypes[df.values[i][10]]:
                    kill_chain.append(f'responsetypes:{self.disarm.responsetypes[df.values[i][10]]}')
            except KeyError:
                pass
            # Metatechnique ID is not in the array
            # if self.disarm.metatechniques[df.values[i][???]]:
            #     kill_chain.append(f'metatechniques:{self.disarm.metatechniques[df.values[i][???]]}')

            t = {
                'uuid': str(uuid.uuid5(uuid.UUID(CORE_UUID), df.values[i][0])),
                'value': df.values[i][1],
                'description': df.values[i][3],
                'meta': {
                    'external_id': df.values[i][0],
                    'kill_chain': kill_chain,
                    'refs': [
                        f'https://github.com/DISARMFoundation/DISARMframeworks/blob/main/generated_pages/detections/{df.values[i][0]}.md'
                    ]
                }
            }

            values.append(t)
        cluster['values'] = sorted(values, key=lambda x: x['meta']['external_id'])
        self.write_json_file(os.path.join(self.out_path, 'clusters', 'disarm-detections.json'), cluster)


    def generate_disarm_actortypes_galaxy(self):
        galaxy = {'name': 'Actor Types',
                  'type': 'disarm-actortypes',
                  'description': DISARM_DESCRIPTION,
                  'uuid': str(uuid.uuid5(uuid.UUID(CORE_UUID), 'disarm-galaxy-actortypes')),
                  'version': 1,
                  'icon': 'user-secret',
                  'namespace': 'disarm',
                  'kill_chain_order': {
                      'sectors': []
                  }}

        for k, v in self.disarm.sectors.items():
            galaxy['kill_chain_order']['sectors'].append(f'{v}')

        self.write_json_file(os.path.join(self.out_path, 'galaxies', 'disarm-actortypes.json'), galaxy)

    def generate_disarm_actortypes_clusters(self):
        cluster = {'authors': DISARM_AUTHORS,
                   'category': DISARM_CATEGORY,
                   'description': DISARM_DESCRIPTION,
                   'name': 'Actor Types',
                   'source': DISARM_SOURCE,
                   'type': 'disarm-actortypes',
                   'uuid': str(uuid.uuid5(uuid.UUID(CORE_UUID), 'disarm-cluster-actortypes')),
                   'values': [],
                   'version': 1}
        values = []
        df = self.disarm.df_actortypes
        for i in range(len(df)):

            kill_chain = []
            try:
                sectors = df.values[i][3].split(',')
                for sector in sectors:
                    sector = sector.strip()
                    if self.disarm.sectors[sector]:
                        kill_chain.append(f'sectors:{self.disarm.sectors[sector]}')
            except KeyError:
                pass

            t = {
                'uuid': str(uuid.uuid5(uuid.UUID(CORE_UUID), df.values[i][0])),
                'value': df.values[i][1],
                'description': df.values[i][2],
                'meta': {
                    'external_id': df.values[i][0],
                    'kill_chain': kill_chain,
                    'refs': [
                        f'https://github.com/DISARMFoundation/DISARMframeworks/blob/main/generated_pages/actortypes/{df.values[i][0]}.md'
                    ]
                }
            }

            values.append(t)
        cluster['values'] = sorted(values, key=lambda x: x['meta']['external_id'])
        self.write_json_file(os.path.join(self.out_path, 'clusters', 'disarm-actortypes.json'), cluster)


def main():
    disarm_galaxy = DisarmGalaxy()
    disarm_galaxy.generate_disarm_techniques_galaxy()
    disarm_galaxy.generate_disarm_techniques_clusters()
    disarm_galaxy.generate_disarm_countermeasures_galaxy()
    disarm_galaxy.generate_disarm_countermeasures_clusters()
    disarm_galaxy.generate_disarm_detections_galaxy()
    disarm_galaxy.generate_disarm_detections_clusters()
    disarm_galaxy.generate_disarm_actortypes_galaxy()
    disarm_galaxy.generate_disarm_actortypes_clusters()

if __name__ == "__main__":
    main()
    print("All done, please look at the delta, and update the version number if needed.")
    print("After that do ./jq_all_the_things.sh, commit, and then ./validate_all.sh.")
