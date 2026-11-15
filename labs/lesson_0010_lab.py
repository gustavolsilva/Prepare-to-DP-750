#!/usr/bin/env python3
"""
Lab Lição 0010: Auto Loader (Cloud Files) & Rescued Data Column
Exame DP-750: Ingestão de JSON com Schema Evolution e captura de dados corrompidos.
"""
import json

def process_autoloader_batch(raw_records: list, expected_schema: dict):
    valid_rows = []
    rescued_rows = []
    
    for row in raw_records:
        rescued = {}
        processed = {}
        for k, v in row.items():
            if k in expected_schema:
                processed[k] = v
            else:
                rescued[k] = v
        
        processed['_rescued_data'] = json.dumps(rescued) if rescued else None
        valid_rows.append(processed)
    return valid_rows

def test_autoloader_rescued_data():
    schema = {'id': int, 'name': str}
    raw = [
        {'id': 1, 'name': 'Item A'},
        {'id': 2, 'name': 'Item B', 'extra_field_unseen': 99.9}
    ]
    result = process_autoloader_batch(raw, schema)
    assert result[0]['_rescued_data'] is None
    assert 'extra_field_unseen' in result[1]['_rescued_data']
    print('✅ Lab 0010 OK: Auto Loader Schema Rescue simulado com sucesso')

if __name__ == '__main__':
    test_autoloader_rescued_data()
