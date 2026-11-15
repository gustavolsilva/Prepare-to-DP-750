#!/usr/bin/env python3
"""
Lab Lição 0006: Azure Key Vault Secret Scopes e Storage Credentials
Exame DP-750: Acesso a credenciais via dbutils.secrets e Managed Identity no ADLS Gen2.
"""

class MockSecretVault:
    def __init__(self):
        self.scopes = {'adls-keyvault-scope': {'storage-key': 'sig_azure_token_xyz'}}
    
    def get_secret(self, scope: str, key: str):
        if scope not in self.scopes:
            raise KeyError(f'Scope {scope} não encontrado.')
        if key not in self.scopes[scope]:
            raise KeyError(f'Key {key} não encontrada no scope {scope}.')
        return self.scopes[scope][key]

def test_secret_access():
    vault = MockSecretVault()
    token = vault.get_secret('adls-keyvault-scope', 'storage-key')
    assert token.startswith('sig_')
    print('✅ Lab 0006 OK: Recuperação segura de secrets KeyVault simulada com sucesso')

if __name__ == '__main__':
    test_secret_access()
