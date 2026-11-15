#!/usr/bin/env python3
"""
Lab Lição 0014: Delta Live Tables (DLT) Data Quality Expectations
Exame DP-750: EXPECT, EXPECT ON VIOLATION DROP ROW e ON VIOLATION FAIL UPDATE.
"""

def apply_dlt_expectation(record: dict, rule: str, action: str):
    # Regra: valid_amount = amount > 0
    is_valid = record.get('amount', 0) > 0
    if is_valid:
        return 'PASS', record
    
    if action == 'WARN':
        return 'LOG_WARN', record
    elif action == 'DROP':
        return 'DROP', None
    elif action == 'FAIL':
        raise ValueError(f'DLT Pipeline Failed: {record} violou regra crítica {rule}')
    return 'UNKNOWN', record

def test_dlt_expectations():
    rec_valid = {'id': 1, 'amount': 150}
    rec_invalid = {'id': 2, 'amount': -20}
    
    status, _ = apply_dlt_expectation(rec_valid, 'amount_gt_zero', 'DROP')
    assert status == 'PASS'
    
    status_drop, dropped_rec = apply_dlt_expectation(rec_invalid, 'amount_gt_zero', 'DROP')
    assert status_drop == 'DROP' and dropped_rec is None
    print('✅ Lab 0014 OK: DLT Expectations processadas conforme especificação Lakeflow')

if __name__ == '__main__':
    test_dlt_expectations()
