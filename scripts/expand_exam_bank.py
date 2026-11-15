#!/usr/bin/env python3
"""
Databricks Formation — Prepare to DP-750
Compila e expande o banco massivo de mais de 180 questões inéditas do exame oficial
Microsoft Exam DP-750: Implementing Data Engineering Solutions Using Azure Databricks.
Gera o arquivo assets/exam-questions.js com 8 Estudos de Caso Corporativos em Split-Screen.
Todas as 184 questões possuem enunciados com cenários reais corporativos, 4 opções técnicas
distintas e plausíveis (sem distratores repetitivos/genéricos) e explicações aprofundadas.
"""

import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

CASE_STUDIES = [
    {
        "id": "case-01",
        "title": "Caso de Estudo 01: Banco Global FinTech — Migração para Unity Catalog e Serverless",
        "tabs": {
            "overview": "O FinTechBank é uma instituição financeira com 15 milhões de correntistas operando na América Latina e Europa. A instituição está migrando sua plataforma legada de analytics (baseada em Hive Metastore e DBFS) para o Azure Databricks com Unity Catalog para atender a regulamentações rigorosas de auditoria (SOX, LGPD e GDPR).",
            "architecture": "Atualmente, a empresa possui 3 workspaces legados conectados ao ADLS Gen2 via chaves de acesso (Access Keys) montadas em /mnt. A nova arquitetura prevê um único Metastore regional do Unity Catalog centralizado no Azure East US 2, com segregação de ambientes via catálogo de 3 níveis (prod_catalog, staging_catalog, dev_catalog).",
            "requirements": "1. Eliminar completamente o uso de credenciais em código e montagens no DBFS.\n2. Garantir que analistas de BI utilizem Serverless SQL Warehouses com tempo de resposta sub-segundo.\n3. Aplicar mascaramento automático de CPF e número de cartão para equipes de marketing.",
            "security": "Todos os acessos devem ser governados via Microsoft Entra ID com SCIM centralizado no Databricks Account Console. Usuários não devem ter privilégios de criar clusters all-purpose desgovernados.",
            "issues": "A fatura de nuvem aumentou 40% no último trimestre devido a clusters all-purpose deixados ligados durante noites e fins de semana sem autotermination configurado."
        }
    },
    {
        "id": "case-02",
        "title": "Caso de Estudo 02: Rede Multinacional de Varejo — Omnichannel & Ingestão com Auto Loader",
        "tabs": {
            "overview": "A RetailGiant opera mais de 2.000 lojas físicas e uma plataforma de e-commerce que gera 80 milhões de eventos de telemetria e vendas diárias em arquivos JSON e Parquet depositados no ADLS Gen2.",
            "architecture": "Eventos de pedidos chegam continuamente no container adls://raw/orders/. A equipe de engenharia utiliza Azure Databricks com pipelines Structured Streaming e Delta Lake.",
            "requirements": "1. Ingerir arquivos de forma contínua com latência menor que 1 minuto.\n2. Lidar com schema drift inesperado sem derrubar o pipeline de produção.\n3. Processar arquivos corrompidos em uma coluna de escape para auditoria posterior.",
            "security": "Os dados de pagamentos contêm informações de PII que devem ser acessíveis apenas por membros do grupo 'auditoria_financeira'.",
            "issues": "O comando legado de listar arquivos (dbutils.fs.ls) atinge timeout frequente no Driver do Spark devido à presença de mais de 10 milhões de arquivos acumulados no diretório."
        }
    },
    {
        "id": "case-03",
        "title": "Caso de Estudo 03: Indústria Farmacêutica — Delta Live Tables e Governança de Qualidade",
        "tabs": {
            "overview": "A PharmaHealth desenvolve medicamentos biológicos e conduz ensaios clínicos globais. A integridade dos dados dos ensaios clínicos é monitorada por órgãos reguladores internacionais (FDA e ANVISA).",
            "architecture": "Os cientistas de dados recebem dados de telemetria de sensores laboratoriais a cada 10 segundos. Os dados são processados através de pipelines Delta Live Tables (DLT) escritos em Python.",
            "requirements": "1. Descartar medições de temperatura fora do intervalo aceitável (entre 2°C e 8°C) gravando a métrica no log de qualidade.\n2. Se o identificador do lote (batch_id) for nulo, o pipeline deve abortar imediatamente a execução.\n3. Rastrear a linhagem de dados completa da camada Bronze até a Gold.",
            "security": "O metastore do Unity Catalog deve gerenciar o acesso com privilégios estritos de leitura apenas para pesquisadores autorizados.",
            "issues": "Pipelines anteriores em notebooks convencionais permitiam a inserção de dados inconsistentes na camada Silver por falta de validação declarativa de integridade."
        }
    },
    {
        "id": "case-04",
        "title": "Caso de Estudo 04: Empresa de Telecomunicações — Streaming em Tempo Real e Watermarking",
        "tabs": {
            "overview": "A TelcoNet processa bilhões de registros de chamadas telefônicas (Call Detail Records - CDRs) e consumo de dados 5G para detecção de fraudes em tempo real e tarifação dinâmica.",
            "architecture": "Os registros são ingeridos via Azure Event Hubs em formato Avro e processados por Spark Structured Streaming no Azure Databricks com clusters acelerados por Photon.",
            "requirements": "1. Agregar volume de dados consumido por usuário em janelas de 10 minutos.\n2. Descartar eventos com atraso superior a 15 minutos para evitar esgotamento de memória no State Store.\n3. Garantir tolerância a falhas exactly-once com checkpointing no ADLS Gen2.",
            "security": "A autenticação entre o Databricks e o Event Hubs deve utilizar Azure Key Vault-backed Secret Scopes.",
            "issues": "O cluster antigo sofria com erros frequentes de OutOfMemory (OOM) no State Store da JVM após 48 horas de execução ininterrupta."
        }
    },
    {
        "id": "case-05",
        "title": "Caso de Estudo 05: Logística Global — Otimização Física com Liquid Clustering e CDC",
        "tabs": {
            "overview": "A LogiTrans rastreia frotas de 50.000 navios e caminhões de carga pelo mundo, registrando coordenadas GPS e status de entregas a cada segundo.",
            "architecture": "A tabela principal de tracking possui 80 TB de dados no Delta Lake. As consultas dos clientes filtram simultaneamente por 'id_veiculo', 'codigo_pais' e 'data_posicao'.",
            "requirements": "1. Otimizar as consultas de rastreamento com resposta em menos de 2 segundos.\n2. Permitir deleções de dados sob demanda para atender à solicitação de esquecimento sem reescrever arquivos Parquet inteiros.\n3. Substituir o particionamento Hive que sofria com milhões de arquivos minúsculos (small files).",
            "security": "Permissões de acesso controladas por Row Filters garantindo que transportadoras parceiras visualizem apenas seus próprios veículos.",
            "issues": "O comando semanal de OPTIMIZE ZORDER demorava mais de 14 horas para concluir e consumia centenas de DBUs desnecessárias."
        }
    },
    {
        "id": "case-06",
        "title": "Caso de Estudo 06: Companhia de Energia — CI/CD e Databricks Asset Bundles (DABs)",
        "tabs": {
            "overview": "A PowerGrid gerencia a distribuição elétrica de 3 estados brasileiros, com telemetria inteligente de medidores residenciais e industriais.",
            "architecture": "A equipe de engenharia de dados é composta por 25 engenheiros que colaboram via Azure DevOps Git Repositories e utilizam Databricks Asset Bundles (DABs) para gerenciar infraestrutura como código (IaC).",
            "requirements": "1. Garantir que todo deploy em produção seja feito de forma declarativa e automatizada pelo pipeline de CI/CD sem edição manual no portal.\n2. Parametrizar dinamicamente os caminhos de storage entre os ambientes de dev, staging e prod via databricks.yml.\n3. Em caso de falha de uma tarefa em um job multitarefa de 6 etapas, o orquestrador deve permitir reexecutar apenas a etapa afetada (Repair Run).",
            "security": "Service Principals com autenticação federada OIDC no Microsoft Entra ID para execução dos pipelines de deploy sem senhas gravadas.",
            "issues": "Desenvolvedores aplicavam alterações manuais em notebooks de produção diretamente pelo workspace, causando divergências de versão e falhas silenciosas."
        }
    },
    {
        "id": "case-07",
        "title": "Caso de Estudo 07: Hospital de Alta Complexidade — Governança e Compartilhamento com Delta Sharing",
        "tabs": {
            "overview": "O Hospital Santa Mônica realiza pesquisas genéticas e atendimento de pacientes de alta complexidade. A instituição precisa compartilhar dados anonimizados de ensaios clínicos com universidades parceiras que não utilizam o Azure Databricks.",
            "architecture": "Os dados clínicos estão armazenados no catálogo 'pesquisa_medica' no Unity Catalog do Azure Databricks.",
            "requirements": "1. Compartilhar tabelas selecionadas em tempo real com cientistas que utilizam Python Pandas e Power BI em outras nuvens (AWS e GCP) sem fazer cópia física de dados.\n2. Rastrear exatamente quando e quais registros cada instituição parceira consultou via System Tables de auditoria.\n3. Revogar o acesso instantaneamente ao término do convênio de pesquisa.",
            "security": "Aplicação obrigatória de Column Masks para ocultar nomes de pacientes e números de prontuário antes do compartilhamento.",
            "issues": "O compartilhamento anterior era realizado enviando arquivos CSV por SFTP, o que gerava perda de governança, versões desatualizadas e riscos de vazamento."
        }
    },
    {
        "id": "case-08",
        "title": "Caso de Estudo 08: Marketplace B2B — Dimensionamento FinOps e Cluster Policies",
        "tabs": {
            "overview": "O MarketHub conecta 100.000 fornecedores a 500.000 compradores industriais. O tráfego de dados é altamente sazonal com picos expressivos no final de cada mês.",
            "architecture": "A empresa utiliza Azure Databricks conectado a um Azure Data Lake Storage Gen2 e Azure SQL Database.",
            "requirements": "1. Impor Cluster Policies obrigatórias para todas as equipes de engenharia, fixando autotermination em 20 minutos e limitando o tipo de VM para famílias D4ds_v5.\n2. Criar Databricks Instance Pools para permitir que clusters de desenvolvimento iniciem em menos de 30 segundos durante o expediente comercial.\n3. Ratear o consumo de DBUs por squad de produto usando tags de faturamento do Azure integradas à system.billing.usage.",
            "security": "Uso de Unity Catalog com isolamento de metadados e restrição de acesso via rede segura com VNet Injection.",
            "issues": "Equipes de ciência de dados criavam clusters de 16 nós com GPU para rodar análises simples em Pandas, estourando o orçamento mensal de nuvem em 10 dias."
        }
    }
]

def build_raw_question_bank():
    """
    Gera o banco estruturado com 184 questões cobrindo cirurgicamente os 4 domínios:
    - Domínio 1 (15-20%): 38 questões
    - Domínio 2 (15-20%): 38 questões
    - Domínio 3 (30-35%): 54 questões
    - Domínio 4 (30-35%): 54 questões
    """
    from scripts.build_full_questions import build_questions
    return build_questions()

def main():
    questions = build_raw_question_bank()
    
    js_content = f"""/**
 * Databricks Formation — Prepare to DP-750
 * Banco Massivo Oficial de Questões (+180Q) e Estudos de Caso Split-Screen
 * Exame Microsoft DP-750: Implementing Data Engineering Solutions Using Azure Databricks
 */

const CASE_STUDIES = {json.dumps(CASE_STUDIES, indent=2, ensure_ascii=False)};

const EXAM_QUESTIONS = {json.dumps(questions, indent=2, ensure_ascii=False)};

if (typeof module !== 'undefined' && module.exports) {{
  module.exports = {{ CASE_STUDIES, EXAM_QUESTIONS }};
}}
"""
    
    target_path = os.path.join("assets", "exam-questions.js")
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(js_content)
    
    print(f"Banco de questões gerado com sucesso em {target_path}!")
    print(f"Total de Questões: {len(questions)}")
    print(f"Total de Estudos de Caso: {len(CASE_STUDIES)}")

if __name__ == "__main__":
    main()
