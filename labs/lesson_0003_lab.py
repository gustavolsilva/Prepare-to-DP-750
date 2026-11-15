#!/usr/bin/env python3
"""
Lab Lição 0003: Simulador do Delta Log Protocol, ACID e Time Travel
Exame DP-750: Criando commits JSON em _delta_log e executando Time Travel por versão.
"""
import json

class InMemoryDeltaTable:
    def __init__(self):
        self.commits = [] # lista de commits JSON
    
    def commit(self, version: int, action: str, data_file: str, num_records: int):
        commit_entry = {
            'version': version,
            'commit_file': f'{version:020d}.json',
            'action': action,
            'add': {'path': data_file, 'records': num_records}
        }
        self.commits.append(commit_entry)
        return commit_entry

    def read_at_version(self, target_version: int):
        files = []
        for c in self.commits:
            if c['version'] <= target_version:
                if c['action'] == 'add':
                    files.append(c['add']['path'])
                elif c['action'] == 'remove':
                    if c['add']['path'] in files:
                        files.remove(c['add']['path'])
        return files

def test_delta_protocol():
    table = InMemoryDeltaTable()
    table.commit(0, 'add', 'part-000.parquet', 100)
    table.commit(1, 'add', 'part-001.parquet', 200)
    
    v0_files = table.read_at_version(0)
    v1_files = table.read_at_version(1)
    
    assert len(v0_files) == 1 and v0_files[0] == 'part-000.parquet'
    assert len(v1_files) == 2
    print(f'✅ Lab 0003 OK: Delta Log Time Travel v0={v0_files}, v1={v1_files}')

if __name__ == '__main__':
    test_delta_protocol()
