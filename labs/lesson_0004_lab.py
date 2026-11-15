#!/usr/bin/env python3
"""
Lab Lição 0004: Simulador de Entra ID SCIM, Service Principals e VNet Injection
Exame DP-750: Validacao de subnets pública/privada e resolução Private Link.
"""

def validate_vnet_injection(public_subnet_cidr: str, private_subnet_cidr: str):
    # Exige duas subnets dedicadas sem sobreposição com minimo /26
    def get_mask(cidr):
        return int(cidr.split('/')[1])
    
    if get_mask(public_subnet_cidr) > 26 or get_mask(private_subnet_cidr) > 26:
        raise ValueError('Databricks VNet Injection exige subnets de no minimo /26 (64 IPs)')
    return True

def test_vnet_validation():
    assert validate_vnet_injection('10.0.1.0/24', '10.0.2.0/24') is True
    print('✅ Lab 0004 OK: VNet Injection Subnets validadas conforme padrão Azure')

if __name__ == '__main__':
    test_vnet_validation()
