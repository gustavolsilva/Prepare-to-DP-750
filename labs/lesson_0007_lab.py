#!/usr/bin/env python3
"""
Lab Lição 0007: Unity Catalog 3-Level Namespace e Volumes
Exame DP-750: Estrutura catalog.schema.table e Managed vs External Volumes.
"""

class UnityCatalogMetastore:
    def __init__(self):
        self.tree = {} # catalog -> schema -> objects
    
    def create_table(self, fqdn: str, table_type: str = 'MANAGED'):
        parts = fqdn.split('.')
        if len(parts) != 3:
            raise ValueError('Unity Catalog exige FQDN de 3 níveis: catalog.schema.table')
        cat, sch, tbl = parts
        self.tree.setdefault(cat, {}).setdefault(sch, {})[tbl] = {'type': table_type}
        return True

def test_unity_catalog():
    uc = UnityCatalogMetastore()
    uc.create_table('prod_lakehouse.finance.gold_revenues', 'MANAGED')
    assert 'gold_revenues' in uc.tree['prod_lakehouse']['finance']
    print('✅ Lab 0007 OK: Namespace de 3 níveis validado com sucesso')

if __name__ == '__main__':
    test_unity_catalog()
