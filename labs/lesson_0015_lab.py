#!/usr/bin/env python3
"""
Lab Lição 0015: Orquestração com Databricks Asset Bundles (DABs) & Workflows
Exame DP-750: Validação de databricks.yml, DAG de tarefas e Repair Run.
"""

def validate_dab_manifest(manifest: dict):
    required_keys = ['bundle', 'resources']
    for k in required_keys:
        if k not in manifest:
            return False, f'Chave obrigatória ausente em databricks.yml: {k}'
    
    jobs = manifest.get('resources', {}).get('jobs', {})
    if not jobs:
        return False, 'DABs exige definição de ao menos um job/pipeline em resources'
    return True, 'Bundle válido'

def test_dab_validation():
    sample_bundle = {
        'bundle': {'name': 'dp750_medallion_etl'},
        'resources': {
            'jobs': {
                'daily_finance_etl': {
                    'tasks': [{'task_key': 'bronze_ingest'}, {'task_key': 'silver_transform'}]
                }
            }
        }
    }
    valid, msg = validate_dab_manifest(sample_bundle)
    assert valid is True
    print(f'✅ Lab 0015 OK: {msg}')

if __name__ == '__main__':
    test_dab_validation()
