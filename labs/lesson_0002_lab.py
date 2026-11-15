#!/usr/bin/env python3
"""
Lab Lição 0002: Simulador do Catalyst Optimizer & Photon Vectorized Engine
Exame DP-750: Analisando Logical Plan, Physical Plan e eliminação de Shuffles.
"""

class CatalystPlanNode:
    def __init__(self, name: str, node_type: str, cost: int):
        self.name = name
        self.node_type = node_type # Scan, Filter, Project, Shuffle
        self.cost = cost

def optimize_plan(nodes):
    # Regra Catalyst: Predicate Pushdown (empurra Filter antes do Shuffle/Project)
    filters = [n for n in nodes if n.node_type == 'Filter']
    scans = [n for n in nodes if n.node_type == 'Scan']
    others = [n for n in nodes if n.node_type not in ('Filter', 'Scan')]
    
    optimized = scans + filters + others
    # Reducao de custo ao aplicar predicate pushdown
    total_cost = sum(n.cost for n in optimized) - (len(filters) * 10)
    return optimized, total_cost

def test_catalyst_optimizer():
    raw_nodes = [
        CatalystPlanNode('Scan ADLS', 'Scan', 50),
        CatalystPlanNode('HashAggregate', 'Shuffle', 80),
        CatalystPlanNode('Filter date > 2024', 'Filter', 30)
    ]
    opt_nodes, cost = optimize_plan(raw_nodes)
    assert opt_nodes[1].node_type == 'Filter', 'Filtro deve ter sofrido Predicate Pushdown!'
    assert cost < 160
    print(f'✅ Lab 0002 OK: Catalyst Otimizou Plano Físico com Custo={cost}')

if __name__ == '__main__':
    test_catalyst_optimizer()
