#!/usr/bin/env python3
"""
Lab Lição 0001: Simulador de FinOps de DBUs & Control vs Compute Plane
Exame DP-750: Entendendo custos de computação clássica vs serverless e rede Azure.
"""

def calculate_dbu_cost(compute_type: str, dbu_rate_per_hour: float, hours: float, dbu_price_usd: float = 0.55):
    valid_types = ['classic_all_purpose', 'classic_jobs', 'serverless_sql', 'serverless_jobs']
    if compute_type not in valid_types:
        raise ValueError(f'Tipo de computação inválido: {compute_type}')
    
    total_dbus = dbu_rate_per_hour * hours
    total_cost = total_dbus * dbu_price_usd
    return round(total_cost, 2)

def test_dbu_calculation():
    # Job cluster usa taxa reduzida de DBU em comparacao a all-purpose
    job_cost = calculate_dbu_cost('classic_jobs', dbu_rate_per_hour=1.5, hours=10, dbu_price_usd=0.40)
    all_purpose_cost = calculate_dbu_cost('classic_all_purpose', dbu_rate_per_hour=3.0, hours=10, dbu_price_usd=0.55)
    
    assert job_cost < all_purpose_cost, 'Job Clusters devem ter custo inferior ao All-Purpose!'
    print(f'✅ Lab 0001 OK: Job Cost = , All-Purpose = ')

if __name__ == '__main__':
    test_dbu_calculation()
