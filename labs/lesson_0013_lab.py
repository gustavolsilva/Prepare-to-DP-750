#!/usr/bin/env python3
"""
Lab Lição 0013: Otimização Física: Liquid Clustering vs Partitioning & Deletion Vectors
Exame DP-750: Aplicando CLUSTER BY e operando soft-deletes via Deletion Vectors.
"""

class TableOptimizationSimulator:
    def __init__(self, cluster_keys: list):
        self.cluster_keys = cluster_keys
        self.deletion_vectors_enabled = True
        self.deleted_rows = set()
    
    def soft_delete(self, row_id: int):
        # Em vez de reescrever o arquivo parquet, adiciona id ao Deletion Vector
        self.deleted_rows.add(row_id)
        return True
    
    def read_live_records(self, all_records: list):
        return [r for r in all_records if r['id'] not in self.deleted_rows]

def test_liquid_clustering_and_dv():
    sim = TableOptimizationSimulator(cluster_keys=['country', 'event_date'])
    records = [{'id': 1, 'country': 'BR'}, {'id': 2, 'country': 'US'}]
    
    sim.soft_delete(1)
    live = sim.read_live_records(records)
    assert len(live) == 1 and live[0]['id'] == 2
    print('✅ Lab 0013 OK: Deletion Vector evitou reescrita completa do arquivo')

if __name__ == '__main__':
    test_liquid_clustering_and_dv()
