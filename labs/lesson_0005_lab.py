#!/usr/bin/env python3
"""
Lab Lição 0005: Validador de Cluster Policies e Auto-Termination FinOps
Exame DP-750: Limitando tipos de instâncias VM e timeout de desligamento.
"""

def evaluate_cluster_policy(policy_rules: dict, cluster_spec: dict):
    # Valida autotermination_minutes
    max_auto_term = policy_rules.get('autotermination_minutes', {}).get('max_value', 120)
    spec_auto_term = cluster_spec.get('autotermination_minutes', 0)
    
    if spec_auto_term == 0 or spec_auto_term > max_auto_term:
        return False, f'Autotermination excede limite permitido de {max_auto_term} min'
    
    allowed_nodes = policy_rules.get('node_type_id', {}).get('values', [])
    if allowed_nodes and cluster_spec.get('node_type_id') not in allowed_nodes:
        return False, 'Node type não autorizado pela política de governança'
    
    return True, 'Cluster em conformidade'

def test_cluster_policy():
    policy = {
        'autotermination_minutes': {'max_value': 30},
        'node_type_id': {'values': ['Standard_D4ds_v5', 'Standard_D8ds_v5']}
    }
    valid_spec = {'autotermination_minutes': 20, 'node_type_id': 'Standard_D4ds_v5'}
    invalid_spec = {'autotermination_minutes': 60, 'node_type_id': 'Standard_D4ds_v5'}
    
    assert evaluate_cluster_policy(policy, valid_spec)[0] is True
    assert evaluate_cluster_policy(policy, invalid_spec)[0] is False
    print('✅ Lab 0005 OK: Cluster Policy Engine validou limites FinOps com sucesso')

if __name__ == '__main__':
    test_cluster_policy()
