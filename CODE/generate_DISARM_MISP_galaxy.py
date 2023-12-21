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

        self.galaxy_types = ['techniques', 'countermeasures', 'detections', 'actortypes']

    def generate_all_galaxies(self):
        for galaxy_type in self.galaxy_types:
            getattr(self, f'generate_{galaxy_type}_galaxy')()  # also saves the files

    def generate_all_clusters(self):
        for galaxy_type in self.galaxy_types:
            getattr(self, f'generate_{galaxy_type}_clusters')()

    def write_json_file(self, fname, file_data):
        with open(fname, 'w') as f:
            json.dump(file_data, f, indent=2, sort_keys=True, ensure_ascii=False)
            f.write('\n')

    def generate_techniques_galaxy(self):
        galaxy_type = 'techniques'
        galaxy = {'name': 'Techniques',
                  'type': f'disarm-{galaxy_type}',
                  'description': DISARM_DESCRIPTION,
                  'uuid': str(uuid.uuid5(uuid.UUID(CORE_UUID), f'disarm-galaxy-{galaxy_type}')),
                  'version': 1,
                  'icon': 'map',
                  'namespace': 'disarm',
                  'kill_chain_order': {
                      'tactics': []
                  }}

        for k, v in self.disarm.tactics.items():
            galaxy['kill_chain_order']['tactics'].append(f'{v}')

        self.write_json_file(os.path.join(self.out_path, 'galaxies', f'disarm-{galaxy_type}.json'), galaxy)

    def generate_techniques_clusters(self):
        galaxy_type = 'techniques'
        cluster = {'authors': DISARM_AUTHORS,
                   'category': DISARM_CATEGORY,
                   'description': DISARM_DESCRIPTION,
                   'name': 'Techniques',
                   'source': DISARM_SOURCE,
                   'type': f'disarm-{galaxy_type}',
                   'uuid': str(uuid.uuid5(uuid.UUID(CORE_UUID), f'disarm-cluster-{galaxy_type}')),
                   'values': [],
                   'version': 1}
        values = []
        seen_values = []
        df = self.disarm.df_techniques
        for i in range(len(df)):
            if df.values[i][1] in seen_values:  # remove duplicates
                continue
            seen_values.append(df.values[i][1])

            entry_id = df.values[i][0]
            kill_chain = [f'tactics:{self.disarm.tactics[df.values[i][3]]}']
            related = []
            # Countermeasures relations
            mapping = self.disarm.cross_counterid_techniqueid[
                self.disarm.cross_counterid_techniqueid['technique_id'] == entry_id]
            for index, row in mapping.sort_values('disarm_id').iterrows():
                related_id = row['disarm_id']
                related.append({
                  "dest-uuid": str(uuid.uuid5(uuid.UUID(CORE_UUID), related_id)),
                  "type": "blocked-by"  # mitigated-by would be cleaner, but does not exist as relationship type
                })
            # Detections relations
            mapping = self.disarm.cross_detectionid_techniqueid[
                self.disarm.cross_detectionid_techniqueid['technique_id'] == entry_id]
            for index, row in mapping.sort_values('disarm_id').iterrows():
                related_id = row['disarm_id']
                related.append({
                    "dest-uuid": str(uuid.uuid5(uuid.UUID(CORE_UUID), related_id)),
                    "type": "detected-by"
                })

            value = {
                'uuid': str(uuid.uuid5(uuid.UUID(CORE_UUID), entry_id)),
                'value': df.values[i][1],
                'description': df.values[i][4],
                'meta': {
                    'external_id': entry_id,
                    'kill_chain': kill_chain,
                    'refs': [
                        f'https://github.com/DISARMFoundation/DISARMframeworks/blob/main/generated_pages/{galaxy_type}/{entry_id}.md'
                    ]
                },
                'related': related
            }
            values.append(value)

        cluster['values'] = sorted(values, key=lambda x: x['meta']['external_id'])
        self.write_json_file(os.path.join(self.out_path, 'clusters', f'disarm-{galaxy_type}.json'), cluster)

    def generate_countermeasures_galaxy(self):
        galaxy_type = 'countermeasures'
        galaxy = {'name': 'Countermeasures',
                  'type': f'disarm-{galaxy_type}',
                  'description': DISARM_DESCRIPTION,
                  'uuid': str(uuid.uuid5(uuid.UUID(CORE_UUID), f'disarm-galaxy-{galaxy_type}')),
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

        self.write_json_file(os.path.join(self.out_path, 'galaxies', f'disarm-{galaxy_type}.json'), galaxy)

    def generate_countermeasures_clusters(self):
        galaxy_type = 'countermeasures'
        cluster = {'authors': DISARM_AUTHORS,
                   'category': DISARM_CATEGORY,
                   'description': DISARM_DESCRIPTION,
                   'name': 'Countermeasures',
                   'source': DISARM_SOURCE,
                   'type': f'disarm-{galaxy_type}',
                   'uuid': str(uuid.uuid5(uuid.UUID(CORE_UUID), f'disarm-cluster-{galaxy_type}')),
                   'values': [],
                   'version': 1}
        values = []
        seen_values = []
        df = self.disarm.df_counters
        for i in range(len(df)):
            if df.values[i][1] in seen_values:  # remove duplicates
                continue
            seen_values.append(df.values[i][1])

            entry_id = df.values[i][0]
            kill_chain = []
            if self.disarm.tactics[df.values[i][15]]:
                kill_chain.append(f'tactics:{self.disarm.tactics[df.values[i][15]]}')
            if self.disarm.responsetypes[df.values[i][10]]:
                kill_chain.append(f'responsetypes:{self.disarm.responsetypes[df.values[i][10]]}')
            if self.disarm.metatechniques[df.values[i][17]]:
                kill_chain.append(f'metatechniques:{self.disarm.metatechniques[df.values[i][17]]}')

            related = []
            # Techniques relations
            mapping = self.disarm.cross_counterid_techniqueid[
                self.disarm.cross_counterid_techniqueid['disarm_id'] == entry_id]
            for index, row in mapping.sort_values('technique_id').iterrows():
                related_id = row['technique_id']
                related.append({
                    "dest-uuid": str(uuid.uuid5(uuid.UUID(CORE_UUID), related_id)),
                    "type": "blocks"  # mitigated would be cleaner, but mitigated-by does not exist as relationship type
                })
            # Actortype relations
            mapping = self.disarm.cross_counterid_actortypeid[
                self.disarm.cross_counterid_actortypeid['disarm_id'] == entry_id]
            for index, row in mapping.sort_values('actortype_id').iterrows():
                related_id = row['actortype_id']
                related.append({
                    "dest-uuid": str(uuid.uuid5(uuid.UUID(CORE_UUID), related_id)),
                    "type": "affected-by"
                    # mitigated-by would be cleaner, but mitigated-by does not exist as relationship type
                })

            value = {
                'uuid': str(uuid.uuid5(uuid.UUID(CORE_UUID), entry_id)),
                'value': df.values[i][1],
                'description': df.values[i][3],
                'meta': {
                    'external_id': entry_id,
                    'kill_chain': kill_chain,
                    'refs': [
                        f'https://github.com/DISARMFoundation/DISARMframeworks/blob/main/generated_pages/counters/{entry_id}.md'
                    ]
                },
                'related': related
            }
            values.append(value)

        cluster['values'] = sorted(values, key=lambda x: x['meta']['external_id'])
        self.write_json_file(os.path.join(self.out_path, 'clusters', f'disarm-{galaxy_type}.json'), cluster)

    def generate_detections_galaxy(self):
        galaxy_type = 'detections'
        galaxy = {'name': 'Detections',
                  'type': f'disarm-{galaxy_type}',
                  'description': DISARM_DESCRIPTION,
                  'uuid': str(uuid.uuid5(uuid.UUID(CORE_UUID), f'disarm-galaxy-{galaxy_type}')),
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

        self.write_json_file(os.path.join(self.out_path, 'galaxies', f'disarm-{galaxy_type}.json'), galaxy)

    def generate_detections_clusters(self):
        galaxy_type = 'detections'
        cluster = {'authors': DISARM_AUTHORS,
                   'category': DISARM_CATEGORY,
                   'description': DISARM_DESCRIPTION,
                   'name': 'Detections',
                   'source': DISARM_SOURCE,
                   'type': f'disarm-{galaxy_type}',
                   'uuid': str(uuid.uuid5(uuid.UUID(CORE_UUID), f'disarm-cluster-{galaxy_type}')),
                   'values': [],
                   'version': 1}
        values = []
        seen_values = []
        df = self.disarm.df_detections
        for i in range(len(df)):
            if df.values[i][1] in seen_values:  # remove duplicates
                continue
            seen_values.append(df.values[i][1])

            entry_id = df.values[i][0]
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

            related = []
            # Techniques relations
            mapping = self.disarm.cross_detectionid_techniqueid[
                self.disarm.cross_detectionid_techniqueid['disarm_id'] == entry_id]
            for index, row in mapping.sort_values('technique_id').iterrows():
                related_id = row['technique_id']
                related.append({
                    "dest-uuid": str(uuid.uuid5(uuid.UUID(CORE_UUID), related_id)),
                    "type": "detects"
                })
            # Actortypes relations
            mapping = self.disarm.cross_detectionid_actortypeid[
                self.disarm.cross_detectionid_actortypeid['disarm_id'] == entry_id]
            for index, row in mapping.sort_values('actortype_id').iterrows():
                related_id = row['actortype_id']
                related.append({
                    "dest-uuid": str(uuid.uuid5(uuid.UUID(CORE_UUID), related_id)),
                    "type": "detected-by"
                    # mitigated-by would be cleaner, but mitigated-by does not exist as relationship type
                })

            value = {
                'uuid': str(uuid.uuid5(uuid.UUID(CORE_UUID), entry_id)),
                'value': df.values[i][1],
                'description': df.values[i][3],
                'meta': {
                    'external_id': entry_id,
                    'kill_chain': kill_chain,
                    'refs': [
                        f'https://github.com/DISARMFoundation/DISARMframeworks/blob/main/generated_pages/{galaxy_type}/{entry_id}.md'
                    ]
                },
                'related': related
            }
            values.append(value)

        cluster['values'] = sorted(values, key=lambda x: x['meta']['external_id'])
        self.write_json_file(os.path.join(self.out_path, 'clusters', f'disarm-{galaxy_type}.json'), cluster)

    def generate_actortypes_galaxy(self):
        galaxy_type = 'actortypes'
        galaxy = {'name': 'Actor Types',
                  'type': f'disarm-{galaxy_type}',
                  'description': DISARM_DESCRIPTION,
                  'uuid': str(uuid.uuid5(uuid.UUID(CORE_UUID), f'disarm-galaxy-{galaxy_type}')),
                  'version': 1,
                  'icon': 'user-secret',
                  'namespace': 'disarm',
                  'kill_chain_order': {
                      'sectors': []
                  }}

        for k, v in self.disarm.sectors.items():
            galaxy['kill_chain_order']['sectors'].append(f'{v}')

        self.write_json_file(os.path.join(self.out_path, 'galaxies', f'disarm-{galaxy_type}.json'), galaxy)

    def generate_actortypes_clusters(self):
        galaxy_type = 'actortypes'
        cluster = {'authors': DISARM_AUTHORS,
                   'category': DISARM_CATEGORY,
                   'description': DISARM_DESCRIPTION,
                   'name': 'Actor Types',
                   'source': DISARM_SOURCE,
                   'type': f'disarm-{galaxy_type}',
                   'uuid': str(uuid.uuid5(uuid.UUID(CORE_UUID), f'disarm-cluster-{galaxy_type}')),
                   'values': [],
                   'version': 1}
        values = []
        seen_values = []
        df = self.disarm.df_actortypes
        for i in range(len(df)):
            if df.values[i][1] in seen_values:  # remove duplicates
                continue
            seen_values.append(df.values[i][1])

            entry_id = df.values[i][0]
            kill_chain = []
            try:
                sectors = df.values[i][3].split(',')
                for sector in sectors:
                    sector = sector.strip()
                    if self.disarm.sectors[sector]:
                        kill_chain.append(f'sectors:{self.disarm.sectors[sector]}')
            except KeyError:
                pass

            related = []
            # Countermeasures relations
            mapping = self.disarm.cross_counterid_actortypeid[
                self.disarm.cross_counterid_actortypeid['actortype_id'] == entry_id]
            for index, row in mapping.sort_values('disarm_id').iterrows():
                related_id = row['disarm_id']
                related.append({
                    "dest-uuid": str(uuid.uuid5(uuid.UUID(CORE_UUID), related_id)),
                    "type": "affects"
                })
            # Detections relations
            mapping = self.disarm.cross_detectionid_actortypeid[
                self.disarm.cross_detectionid_actortypeid['actortype_id'] == entry_id]
            for index, row in mapping.sort_values('disarm_id').iterrows():
                related_id = row['disarm_id']
                related.append({
                    "dest-uuid": str(uuid.uuid5(uuid.UUID(CORE_UUID), related_id)),
                    "type": "detects"
                })

            value = {
                'uuid': str(uuid.uuid5(uuid.UUID(CORE_UUID), entry_id)),
                'value': df.values[i][1],
                'description': df.values[i][2],
                'meta': {
                    'external_id': entry_id,
                    'kill_chain': kill_chain,
                    'refs': [
                        f'https://github.com/DISARMFoundation/DISARMframeworks/blob/main/generated_pages/{galaxy_type}/{entry_id}.md'
                    ]
                },
                'related': related
            }

            values.append(value)
        cluster['values'] = sorted(values, key=lambda x: x['meta']['external_id'])
        self.write_json_file(os.path.join(self.out_path, 'clusters', f'disarm-{galaxy_type}.json'), cluster)


def main():
    disarm_galaxy = DisarmGalaxy()
    disarm_galaxy.generate_all_galaxies()
    disarm_galaxy.generate_all_clusters()


if __name__ == "__main__":
    main()
    print("All done, please look at the delta, and update the version number if needed.")
    print("After that do ./jq_all_the_things.sh, commit, and then ./validate_all.sh.")
