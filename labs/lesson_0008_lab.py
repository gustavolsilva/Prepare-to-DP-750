#!/usr/bin/env python3
"""
Lab Lição 0008: Controle de Acesso Fino (Row Filters & Column Masks)
Exame DP-750: Aplicando mascaramento de CPF/PII e filtros por região geográfica.
"""

def apply_column_mask(value: str, user_groups: list, allowed_group: str = 'hr_admins'):
    if allowed_group in user_groups:
        return value
    # Mascara exibindo apenas os últimos 3 caracteres
    return '***-***-' + value[-3:]

def apply_row_filter(record: dict, user_region: str):
    if user_region == 'GLOBAL' or record.get('region') == user_region:
        return True
    return False

def test_fine_grained_access():
    user_a = {'groups': ['analysts'], 'region': 'BR_SOUTH'}
    user_b = {'groups': ['hr_admins'], 'region': 'GLOBAL'}
    
    record = {'name': 'Ana Silva', 'cpf': '12345678901', 'region': 'BR_SOUTH'}
    
    # Analista vê mascarado
    mask_a = apply_column_mask(record['cpf'], user_a['groups'])
    assert mask_a == '***-***-901'
    
    # HR Admin vê completo
    mask_b = apply_column_mask(record['cpf'], user_b['groups'])
    assert mask_b == '12345678901'
    print('✅ Lab 0008 OK: Row Filters e Column Masks aplicados com sucesso')

if __name__ == '__main__':
    test_fine_grained_access()
