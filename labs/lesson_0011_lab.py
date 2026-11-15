#!/usr/bin/env python3
"""
Lab Lição 0011: Arquitetura Medallion & MERGE INTO SCD Tipo 1 e Tipo 2
Exame DP-750: Upserts de dados e versionamento histórico em Silver/Gold.
"""

def merge_scd_type1(target_table: dict, incoming_batch: list):
    for row in incoming_batch:
        target_table[row['customer_id']] = row # Sobrescreve valores (SCD1)
    return target_table

def test_medallion_merge():
    target = {101: {'customer_id': 101, 'city': 'Curitiba', 'status': 'ACTIVE'}}
    incoming = [{'customer_id': 101, 'city': 'São Paulo', 'status': 'ACTIVE'},
                {'customer_id': 102, 'city': 'Rio de Janeiro', 'status': 'NEW'}]
    
    updated = merge_scd_type1(target, incoming)
    assert updated[101]['city'] == 'São Paulo'
    assert len(updated) == 2
    print('✅ Lab 0011 OK: Merge SCD Tipo 1 efetuado com fidelidade Medallion')

if __name__ == '__main__':
    test_medallion_merge()
