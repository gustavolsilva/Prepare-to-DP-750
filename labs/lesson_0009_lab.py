#!/usr/bin/env python3
"""
Lab Lição 0009: Linhagem e Consultas de Auditoria nas System Tables
Exame DP-750: Consultando system.access.audit e system.billing.usage.
"""

def parse_audit_log(events: list, target_table: str):
    access_events = [e for e in events if e.get('table_name') == target_table]
    unique_principals = set(e.get('user_identity') for e in access_events)
    return unique_principals

def test_system_tables():
    mock_audit = [
        {'event_time': '2025-01-01T10:00:00Z', 'table_name': 'gold.orders', 'user_identity': 'user1@azure.com'},
        {'event_time': '2025-01-01T10:05:00Z', 'table_name': 'gold.orders', 'user_identity': 'user2@azure.com'},
        {'event_time': '2025-01-01T10:10:00Z', 'table_name': 'silver.raw', 'user_identity': 'sp_adf@azure.com'}
    ]
    users = parse_audit_log(mock_audit, 'gold.orders')
    assert len(users) == 2
    print(f'✅ Lab 0009 OK: System Tables Audit Parser retornou {len(users)} identidades')

if __name__ == '__main__':
    test_system_tables()
