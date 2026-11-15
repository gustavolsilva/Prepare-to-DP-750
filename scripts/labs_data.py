"""
Definições dos 15 Laboratórios no formato oficial Microsoft Learn para o DP-750.
"""

LABS_STEPS = {
    "0001": {
        "title": "Lab 0001: Provisionamento e Governança de Computação no Azure Databricks",
        "duration": "30 minutos",
        "scenario": "Você é o Engenheiro de Dados líder de uma organização financeira e precisa provisionar um ambiente de desenvolvimento no Azure Databricks. Sua missão é configurar clusters All-Purpose com limites rígidos de auto-termination, calcular custos de DBUs e comparar o TCO com Job Clusters efêmeros e Serverless Compute.",
        "azure_prereq": "Assinatura ativa do Microsoft Azure com um Workspace Azure Databricks provisionado (Standard ou Premium). Permissão de 'Contributor' no Resource Group do Azure e 'Workspace Admin' ou permissão para criar clusters no Databricks.",
        "tasks": [
            {
                "num": 1,
                "title": "Acessar o Workspace no Azure Portal e Navegar até Compute",
                "instructions": "1. Acesse o portal do Azure (https://portal.azure.com).\n2. Localize seu recurso 'Azure Databricks Service' e clique em 'Launch Workspace'.\n3. Na barra de navegação esquerda do Databricks, clique no ícone 'Compute' (Computação).\n4. Observe as abas disponíveis: 'All-Purpose Compute', 'Job Clusters', 'Serverless' e 'Pools'."
            },
            {
                "num": 2,
                "title": "Criar um Cluster All-Purpose Otimizado para FinOps",
                "instructions": "1. Clique no botão 'Create compute' no canto superior direito.\n2. Configure os parâmetros exatos:\n   - Compute name: dp750-dev-cluster\n   - Policy: Personal Compute ou Unrestricted\n   - Multi node / Single node: Selecione 'Single node' (para economizar custos de VM em laboratório)\n   - Databricks Runtime Version: 15.4 LTS (Scala 2.12, Spark 3.5.0)\n   - Node type: Standard_D4ds_v5 (4 vCPUs, 16 GB memória)\n   - Auto-termination: Habilite a caixa e defina rigorosamente para 20 minutes (regras de FinOps do exame).\n3. Clique em 'Create compute' e aguarde o status mudar de 'Pending' para 'Running' (círculo verde)."
            },
            {
                "num": 3,
                "title": "Criar um Notebook Databricks e Testar Métricas de FinOps com PySpark",
                "instructions": "1. No menu lateral esquerdo, clique em 'Workspace' > 'Users' > Seu Usuário e clique em 'Create' > 'Notebook'.\n2. Nomeie o notebook como 'lab_0001_finops_compute'.\n3. Conecte o notebook ao cluster 'dp750-dev-cluster' no seletor superior direito.\n4. Na Célula 1, digite o código PySpark abaixo e pressione Shift + Enter para executar:",
                "code": """# COMMAND ----------
# Célula 1: Identificação da sessão Spark e cálculo de consumo de DBUs
spark_version = spark.conf.get("spark.databricks.clusterUsageTags.sparkVersion")
cluster_id = spark.conf.get("spark.databricks.clusterUsageTags.clusterId")
print(f"✓ Sessão Spark Ativa! Cluster ID: {cluster_id} | DBR Version: {spark_version}")

# Simulação FinOps de consumo de DBUs:
def calcular_custo_pipeline(horas_execucao, dbu_por_hora, preco_dbu=0.55):
    dbus_totais = horas_execucao * dbu_por_hora
    custo_total = dbus_totais * preco_dbu
    return dbus_totais, custo_total

# Cenário 1: All-Purpose Cluster (Interativo - taxa elevada)
dbu_ap, custo_ap = calcular_custo_pipeline(horas_execucao=5, dbu_por_hora=3.0, preco_dbu=0.55)

# Cenário 2: Job Cluster Efêmero (Produção - taxa reduzida em até 60%)
dbu_job, custo_job = calcular_custo_pipeline(horas_execucao=5, dbu_por_hora=1.5, preco_dbu=0.40)

print(f"📊 Relatório Comparativo FinOps (5 horas de workload):")
print(f"   [All-Purpose] DBUs: {dbu_ap:.1f} | Custo: ${custo_ap:.2f} USD")
print(f"   [Job Cluster] DBUs: {dbu_job:.1f} | Custo: ${custo_job:.2f} USD")
print(f"   💡 Economia obtida com Job Cluster: ${custo_ap - custo_job:.2f} USD ({(1 - custo_job/custo_ap)*100:.1f}%)")""",
                "expected_output": "✓ Sessão Spark Ativa!\n📊 Relatório Comparativo FinOps (5 horas de workload):\n   [All-Purpose] DBUs: 15.0 | Custo: $8.25 USD\n   [Job Cluster] DBUs: 7.5 | Custo: $3.00 USD\n   💡 Economia obtida com Job Cluster: $5.25 USD (63.6%)"
            },
            {
                "num": 4,
                "title": "Limpeza de Recursos FinOps (Desligamento Obrigatório)",
                "instructions": "1. Volte ao menu 'Compute'.\n2. Localize seu cluster 'dp750-dev-cluster' e clique no botão 'Terminate' (ícone de quadrado vermelho).\n3. Confirme o desligamento para garantir que nenhuma VM Azure nem DBUs continuem sendo cobrados enquanto você estuda as próximas lições."
            }
        ]
    },
    "0002": {
        "title": "Lab 0002: Análise de Planos de Execução do Catalyst e Photon Engine",
        "duration": "35 minutos",
        "scenario": "Investigar a fundo os 4 estágios de otimização de consultas do Apache Spark (Resolved Logical, Analyzed, Optimized e Physical Plan) e comparar o ganho de throughput de scans e agregações com o Photon Vectorized Engine em C++.",
        "azure_prereq": "Azure Databricks Workspace alocado no Azure com suporte a Photon (disponível em instâncias padrão de computação).",
        "tasks": [
            {
                "num": 1,
                "title": "Criar Cluster com Aceleração Photon Habilitada",
                "instructions": "1. No Databricks Workspace, navegue em 'Compute' > 'Create compute'.\n2. Habilite a caixa de seleção 'Use Photon Acceleration'.\n3. Selecione o runtime '15.4 LTS (Photon)' e configure autotermination para 20 minutos.\n4. Inicie o cluster 'dp750-photon-cluster'."
            },
            {
                "num": 2,
                "title": "Gerar Massa de Dados Sintética e Inspecionar o Plano Catalyst",
                "instructions": "1. Crie o notebook 'lab_0002_catalyst_photon' e anexe-o ao cluster Photon.\n2. Execute o código PySpark abaixo para inspecionar os planos lógico e físico:",
                "code": """# COMMAND ----------
from pyspark.sql.functions import col, expr, rand

# Gera um DataFrame distribuído de 5 milhões de linhas para teste de stress
df = spark.range(0, 5000000).withColumn("categoria", expr("CASE WHEN id % 4 = 0 THEN 'TECH' WHEN id % 4 = 1 THEN 'FIN' WHEN id % 4 = 2 THEN 'HEALTH' ELSE 'EDU' END")) \\
                           .withColumn("valor", rand() * 1000)

# Consulta com agregação e filtro (Wide Transformation)
df_analise = df.filter(col("valor") > 250) \\
               .groupBy("categoria") \\
               .agg(expr("sum(valor) as total_vendas"), expr("count(*) as transacoes"))

# Inspeciona os 4 estágios do Catalyst Optimizer:
print("=" * 70)
print("PLANO DETALHADO DO CATALYST OPTIMIZER:")
print("=" * 70)
df_analise.explain(extended=True)""",
                "expected_output": "== Parsed Logical Plan ==\n'Aggregate ['categoria], ['categoria, sum('valor) AS total_vendas#..., count(1) AS transacoes#...]\n+- 'Filter ('valor > 250)\n== Analyzed Logical Plan ==\n== Optimized Logical Plan ==\n+- Filter (isnotnull(valor#...) AND (valor#... > 250.0))\n== Physical Plan ==\nAdaptiveSparkPlan isFinalPlan=false\n+- PhotonHashAggregate..."
            },
            {
                "num": 3,
                "title": "Inspecionar Nós Photon na Spark UI",
                "instructions": "1. Execute a ação `.collect()` no notebook para disparar a execução física do Job:\n   `df_analise.show()`\n2. Clique no link 'View Spark UI' exibido logo abaixo da célula do notebook.\n3. Abra a aba 'SQL/Dataframe' e selecione a query executada.\n4. Observe o grafo físico gerado: identifique operadores prefixados com 'Photon' (ex: `PhotonScan`, `PhotonFilter`, `PhotonHashAggregate`). Isso comprova que a execução rodou em C++ vetorizado com instruções SIMD sem passar pela JVM!"
            },
            {
                "num": 4,
                "title": "Limpeza de Recursos",
                "instructions": "1. Retorne ao menu Compute e dê 'Terminate' no cluster 'dp750-photon-cluster'."
            }
        ]
    },
    "0003": {
        "title": "Lab 0003: Operações ACID, Time Travel e Manutenção Física no Delta Lake",
        "duration": "35 minutos",
        "scenario": "Uma auditoria contábil exige que você comprove as garantias ACID do Delta Lake, recupere uma versão histórica de dados apagados por engano via Time Travel e otimize os arquivos Parquet de armazenamento no ADLS Gen2 com OPTIMIZE e VACUUM.",
        "azure_prereq": "Azure Databricks Workspace com acesso de escrita a catálogo ou storage ADLS Gen2.",
        "tasks": [
            {
                "num": 1,
                "title": "Criar Tabela Delta e Executar Mutações Consecutivas",
                "instructions": "1. Abra um novo notebook 'lab_0003_delta_acid'.\n2. Execute a criação da tabela Delta e commits simulados:",
                "code": """# COMMAND ----------
# Célula 1: Criação e primeira inserção (Versão 0)
spark.sql("DROP TABLE IF EXISTS default.lab_delta_transacoes")

spark.sql(\"\"\"
CREATE TABLE default.lab_delta_transacoes (
    id_transacao INT,
    cliente STRING,
    valor DOUBLE,
    status STRING
) USING DELTA
\"\"\")

# Inserção de dados iniciais (Commit Versão 1)
spark.sql(\"\"\"
INSERT INTO default.lab_delta_transacoes VALUES
(101, 'Empresa Alfa', 15000.0, 'APROVADO'),
(102, 'Beta Logística', 4200.5, 'PENDENTE'),
(103, 'Gama Tech', 8900.0, 'APROVADO')
\"\"\")

# Mutações consecutivas gerando histórico (Commit Versão 2 e 3)
spark.sql("UPDATE default.lab_delta_transacoes SET status = 'CANCELADO' WHERE id_transacao = 102")
spark.sql("DELETE FROM default.lab_delta_transacoes WHERE id_transacao = 103")

print("✓ Mutações concluídas com sucesso!")""",
                "expected_output": "✓ Mutações concluídas com sucesso!"
            },
            {
                "num": 2,
                "title": "Inspecionar o Delta Log e Praticar Time Travel",
                "instructions": "1. Na Célula 2, consulte o histórico detalhado da tabela Delta:",
                "code": """# COMMAND ----------
# Exibe a trilha de auditoria e commits JSON do _delta_log
display(spark.sql("DESCRIBE HISTORY default.lab_delta_transacoes"))

# TIME TRAVEL: Consultar a tabela exatamente como ela estava na Versão 1 (antes do UPDATE e DELETE)
print("--- DADOS NA VERSÃO 1 (TIME TRAVEL HISTÓRICO) ---")
df_v1 = spark.sql("SELECT * FROM default.lab_delta_transacoes VERSION AS OF 1")
df_v1.show()

# Consultar o estado atual (Versão 3)
print("--- ESTADO ATUAL (VERSÃO 3) ---")
spark.sql("SELECT * FROM default.lab_delta_transacoes").show()""",
                "expected_output": "--- DADOS NA VERSÃO 1 (TIME TRAVEL HISTÓRICO) ---\n+------------+--------------+-------+---------+\n|id_transacao|       cliente|  valor|   status|\n+------------+--------------+-------+---------+\n|         101|  Empresa Alfa|15000.0| APROVADO|\n|         102|Beta Logística| 4200.5| PENDENTE|\n|         103|     Gama Tech| 8900.0| APROVADO|\n+------------+--------------+-------+---------+"
            },
            {
                "num": 3,
                "title": "Executar Manutenção Física com OPTIMIZE e VACUUM",
                "instructions": "1. Na Célula 3, execute a compactação de arquivos e limpeza de lixo órfão:",
                "code": """# COMMAND ----------
# Compacta arquivos pequenos em blocos otimizados de ~1 GB
spark.sql("OPTIMIZE default.lab_delta_transacoes")

# VACUUM: Limpa arquivos marcados como removidos que ultrapassaram o período de retenção (padrão 168 horas = 7 dias)
spark.sql("VACUUM default.lab_delta_transacoes RETAIN 168 HOURS")
print("✓ Manutenção de OPTIMIZE e VACUUM concluída conforme o exame DP-750!")""",
                "expected_output": "✓ Manutenção de OPTIMIZE e VACUUM concluída conforme o exame DP-750!"
            },
            {
                "num": 4,
                "title": "Limpeza da Tabela",
                "instructions": "1. Execute: `spark.sql('DROP TABLE IF EXISTS default.lab_delta_transacoes')`.\n2. Desligue seu cluster de teste."
            }
        ]
    },
    "0004": {
        "title": "Lab 0004: Segurança de Rede (VNet Injection) e Sincronização Microsoft Entra ID (SCIM)",
        "duration": "40 minutos",
        "scenario": "A equipe de segurança da informação exige que todo o ambiente Databricks opere dentro de uma VNet corporativa isolada com duas subnets dedicadas /26 e que os acessos sejam sincronizados automaticamente a partir do Microsoft Entra ID via conector SCIM.",
        "azure_prereq": "Assinatura Azure com permissão para criar Virtual Networks e Azure Databricks com VNet Injection.",
        "tasks": [
            {
                "num": 1,
                "title": "Validar Requisitos de VNet Injection no Azure Portal",
                "instructions": "1. No portal do Azure, acesse 'Virtual Networks' e localize a VNet do Databricks.\n2. Verifique as duas subnets obrigatórias:\n   - Subnet 1 (Public/Host): Mínimo /26 (ex: 10.0.1.0/24), delegada para 'Microsoft.Databricks/workspaces'.\n   - Subnet 2 (Private/Container): Mínimo /26 (ex: 10.0.2.0/24), delegada para 'Microsoft.Databricks/workspaces'.\n3. Verifique o Network Security Group (NSG) associado para garantir que não haja regras de bloqueio de saída na porta 443 nem entre subnets para tráfego de shuffle interno."
            },
            {
                "num": 2,
                "title": "Inspecionar o Databricks Account Console para Sincronização SCIM",
                "instructions": "1. Acesse o console corporativo do Databricks em `https://accounts.azuredatabricks.net`.\n2. No menu lateral, clique em 'User Management'.\n3. Observe a lista de usuários e grupos sincronizados a partir do Microsoft Entra ID.\n4. Verifique a existência de grupos corporativos (ex: `dp750_data_engineers`, `dp750_bi_analysts`). No exame DP-750, a governança moderna proíbe a criação de usuários manuais em cada workspace individual; tudo é gerido no Account Console!"
            },
            {
                "num": 3,
                "title": "Configurar Service Principal para Automação CI/CD",
                "instructions": "1. No Account Console, acesse a aba 'Service Principals'.\n2. Clique em 'Add Service Principal'.\n3. Vincule a identidade gerenciada do Microsoft Entra ID criada para o Azure DevOps.\n4. Conceda permissão de acesso ao workspace corporativo para permitir deploy automatizado via Databricks Asset Bundles (DABs)."
            }
        ]
    },
    "0005": {
        "title": "Lab 0005: Governança de FinOps: Cluster Policies e Serverless SQL Warehouses",
        "duration": "35 minutos",
        "scenario": "Implementar uma política de computação corporativa que force autotermination rígido de 20 minutos, proíba VMs de alto custo e configurar um Serverless SQL Warehouse com auto-stop de 1 minuto para o time de Analytics.",
        "azure_prereq": "Azure Databricks Workspace Premium com permissão de criação de Cluster Policies e SQL Warehouses.",
        "tasks": [
            {
                "num": 1,
                "title": "Criar uma Cluster Policy Restritiva em JSON",
                "instructions": "1. No workspace Databricks, vá em 'Compute' > aba 'Cluster policies' > 'Create policy'.\n2. Nome da política: `DP750-Strict-FinOps`.\n3. Cole o JSON de governança abaixo no editor:",
                "code": """{
  "autotermination_minutes": {
    "type": "range",
    "maxValue": 20,
    "defaultValue": 15,
    "isOptional": false
  },
  "node_type_id": {
    "type": "allowlist",
    "values": [
      "Standard_D4ds_v5",
      "Standard_D8ds_v5"
    ],
    "defaultValue": "Standard_D4ds_v5"
  },
  "custom_tags.CostCenter": {
    "type": "fixed",
    "value": "DataEngineering-DP750"
  }
}""",
                "expected_output": "✓ Política DP750-Strict-FinOps criada com sucesso com limites rígidos de FinOps."
            },
            {
                "num": 2,
                "title": "Conceder Permissão de Uso na Política",
                "instructions": "1. Na aba 'Permissions' da política recém-criada, adicione o grupo `users` com o privilégio `CAN_USE`.\n2. Tente criar um cluster como usuário comum usando esta política e verifique que o autotermination não pode ultrapassar 20 minutos e instâncias com GPU estão bloqueadas."
            },
            {
                "num": 3,
                "title": "Provisionar um Serverless SQL Warehouse",
                "instructions": "1. No menu lateral, alterne a persona para 'SQL' ou clique em 'SQL Warehouses'.\n2. Clique em 'Create SQL Warehouse'.\n3. Configure:\n   - Name: `dp750-serverless-bi`\n   - Cluster size: 2X-Small\n   - Type: Serverless\n   - Auto stop: 1 minute (desligamento ultrarrápido após inatividade)\n   - Scaling: Min 1, Max 2 clusters.\n4. Clique em 'Create' e execute uma query de teste no SQL Editor (`SELECT current_timestamp();`).\n5. Verifique que o startup levou menos de 10 segundos!"
            }
        ]
    },
    "0006": {
        "title": "Lab 0006: Integração Segura com Azure Key Vault e Storage Credentials ADLS Gen2",
        "duration": "35 minutos",
        "scenario": "A equipe de arquitetura proibiu credenciais em texto plano. Você deve conectar o Databricks ao Azure Key Vault via Secret Scope e configurar Storage Credentials no Unity Catalog via Managed Identity para acessar o ADLS Gen2.",
        "azure_prereq": "Assinatura Azure com Azure Key Vault e Azure Data Lake Storage Gen2 provisionados.",
        "tasks": [
            {
                "num": 1,
                "title": "Obter os Dados do Azure Key Vault",
                "instructions": "1. No Azure Portal, abra o recurso Azure Key Vault.\n2. Na aba 'Properties', copie:\n   - DNS Name (ex: `https://kv-dp750-prod.vault.azure.net/`)\n   - Resource ID (ex: `/subscriptions/.../resourceGroups/.../providers/Microsoft.KeyVault/vaults/...`)\n3. Na aba 'Secrets', crie um segredo chamado `adls-access-token` com um valor de teste."
            },
            {
                "num": 2,
                "title": "Criar o Secret Scope Backed pelo Azure Key Vault no Databricks",
                "instructions": "1. No navegador, acerte a URL do seu workspace Databricks adicionando `#secrets/createScope` ao final:\n   `https://<sua-instancia-databricks>#secrets/createScope`\n2. Preencha os campos:\n   - Scope Name: `kv-dp750-scope`\n   - Manage Principal: Creator\n   - DNS Name: cole o DNS Name do Key Vault\n   - Resource ID: cole o Resource ID do Key Vault\n3. Clique em 'Create'."
            },
            {
                "num": 3,
                "title": "Recuperar o Segredo Mascarado via PySpark",
                "instructions": "1. Abra um notebook e execute o código de leitura do segredo:",
                "code": """# COMMAND ----------
# Leitura segura do segredo armazenado no Azure Key Vault
token = dbutils.secrets.get(scope="kv-dp750-scope", key="adls-access-token")

# O Databricks mascara automaticamente o valor na saída com [REDACTED]
print(f"Segredo recuperado com segurança: {token}")

# Valida que o token não está vazio
assert len(token) > 0, "Falha ao recuperar o token do Azure Key Vault"
print("✓ Validação de conformidade DP-750 aprovada: Token protegido!")""",
                "expected_output": "Segredo recuperado com segurança: [REDACTED]\n✓ Validação de conformidade DP-750 aprovada: Token protegido!"
            }
        ]
    },
    "0007": {
        "title": "Lab 0007: Arquitetura Unity Catalog: Metastore, 3-Level Namespace e Volumes",
        "duration": "40 minutos",
        "scenario": "Implementar a governança centralizada no Unity Catalog: criar catálogos, schemas, Managed Tables, External Tables e gerenciar arquivos não estruturados em Volumes.",
        "azure_prereq": "Azure Databricks Workspace com Unity Catalog habilitado e permissão de CREATE CATALOG no Metastore.",
        "tasks": [
            {
                "num": 1,
                "title": "Criar a Estrutura de 3 Níveis via SQL",
                "instructions": "1. Crie o notebook 'lab_0007_unity_catalog' e execute a hierarquia oficial:",
                "code": """# COMMAND ----------
-- Criação do Catálogo e Schema governados
CREATE CATALOG IF NOT EXISTS dp750_corp_catalog;
USE CATALOG dp750_corp_catalog;

CREATE SCHEMA IF NOT EXISTS raw_bronze;
USE SCHEMA raw_bronze;

-- Criação de uma Managed Table (dados e metadados gerenciados pelo Unity Catalog)
CREATE OR REPLACE TABLE dp750_corp_catalog.raw_bronze.pedidos_managed (
    id_pedido BIGINT,
    data_pedido DATE,
    cliente_id INT,
    valor_total DOUBLE
);

INSERT INTO dp750_corp_catalog.raw_bronze.pedidos_managed VALUES
(1001, '2025-01-10', 501, 250.75),
(1002, '2025-01-11', 502, 1120.00);

SELECT * FROM dp750_corp_catalog.raw_bronze.pedidos_managed;""",
                "expected_output": "+---------+-----------+----------+-----------+\n|id_pedido|data_pedido|cliente_id|valor_total|\n+---------+-----------+----------+-----------+\n|     1001| 2025-01-10|       501|     250.75|\n|     1002| 2025-01-11|       502|    1120.00|\n+---------+-----------+----------+-----------+"
            },
            {
                "num": 2,
                "title": "Criar e Utilizar Volumes para Arquivos Não Estruturados",
                "instructions": "1. Na Célula 2, crie um Volume governado para arquivos brutos:",
                "code": """# COMMAND ----------
-- Criação de Volume gerenciado no Unity Catalog
CREATE VOLUME IF NOT EXISTS dp750_corp_catalog.raw_bronze.arquivos_landing;

-- Descreve o caminho POSIX-like do volume
DESCRIBE VOLUME dp750_corp_catalog.raw_bronze.arquivos_landing;""",
                "expected_output": "storage_location: /Volumes/dp750_corp_catalog/raw_bronze/arquivos_landing"
            },
            {
                "num": 3,
                "title": "Inspecionar no Catalog Explorer",
                "instructions": "1. No menu esquerdo do Databricks, clique em 'Catalog'.\n2. Navegue na árvore: `dp750_corp_catalog` > `raw_bronze` > `pedidos_managed`.\n3. Observe as abas 'Overview', 'Sample Data', 'Details', 'Permissions' e 'Lineage'."
            }
        ]
    },
    "0008": {
        "title": "Lab 0008: Controle de Acesso Fino: Row Filters e Column Masks no Unity Catalog",
        "duration": "35 minutos",
        "scenario": "Configurar segurança granular em uma tabela corporativa para que analistas vejam apenas registros de sua própria região e tenham dados de PII (CPF) mascarados dinamicamente.",
        "azure_prereq": "Azure Databricks Workspace com Unity Catalog.",
        "tasks": [
            {
                "num": 1,
                "title": "Criar Tabela com Dados Pessoais Sensíveis",
                "instructions": "1. Abra um notebook e execute o script de criação da tabela de clientes:",
                "code": """# COMMAND ----------
CREATE SCHEMA IF NOT EXISTS dp750_corp_catalog.seguranca;

CREATE OR REPLACE TABLE dp750_corp_catalog.seguranca.clientes_sensivel (
    id INT,
    nome STRING,
    regiao STRING,
    cpf STRING,
    salario DOUBLE
);

INSERT INTO dp750_corp_catalog.seguranca.clientes_sensivel VALUES
(1, 'Carlos Silva', 'SUL', '12345678901', 8500.0),
(2, 'Mariana Costa', 'SUDESTE', '98765432100', 12000.0),
(3, 'Renato Santos', 'SUL', '55544433322', 6200.0);""",
                "expected_output": "✓ Tabela criada e populada com 3 registros."
            },
            {
                "num": 2,
                "title": "Definir e Aplicar Funções SQL de Row Filter e Column Masking",
                "instructions": "1. Crie as SQL UDFs de mascaramento e restrição de linha:",
                "code": """# COMMAND ----------
-- 1. Criação do Row Filter por região geográfica
CREATE OR REPLACE FUNCTION dp750_corp_catalog.seguranca.filtro_regiao(regiao STRING)
RETURN IF(is_account_group_member('diretoria_global'), true, regiao = 'SUL');

-- 2. Aplica o Row Filter na tabela
ALTER TABLE dp750_corp_catalog.seguranca.clientes_sensivel 
SET ROW FILTER dp750_corp_catalog.seguranca.filtro_regiao ON (regiao);

-- 3. Criação da Column Mask para mascarar CPF
CREATE OR REPLACE FUNCTION dp750_corp_catalog.seguranca.mascara_cpf(cpf STRING)
RETURN IF(is_account_group_member('rh_auditoria'), cpf, CONCAT('***.***.', RIGHT(cpf, 3)));

-- 4. Aplica a Column Mask na coluna CPF
ALTER TABLE dp750_corp_catalog.seguranca.clientes_sensivel 
ALTER COLUMN cpf SET MASK dp750_corp_catalog.seguranca.mascara_cpf;

-- 5. Consulta de teste
SELECT * FROM dp750_corp_catalog.seguranca.clientes_sensivel;""",
                "expected_output": "+---+------------+------+-----------+-------+\n| id|        nome|regiao|        cpf|salario|\n+---+------------+------+-----------+-------+\n|  1|Carlos Silva|   SUL|***.***.901| 8500.0|\n|  3|Renato Santos|   SUL|***.***.322| 6200.0|\n+---+------------+------+-----------+-------+\n(Linha 2 de SUDESTE filtrada e CPF mascarado dinamicamente!)"
            }
        ]
    },
    "0009": {
        "title": "Lab 0009: Rastreamento de Linhagem e Auditoria Avançada com System Tables",
        "duration": "35 minutos",
        "scenario": "Consultar tabelas de auditoria do sistema (system.access.audit e system.billing.usage) e inspecionar a linhagem automática de dados no Catalog Explorer.",
        "azure_prereq": "Azure Databricks Workspace com System Tables habilitadas pela organização.",
        "tasks": [
            {
                "num": 1,
                "title": "Consultar Logs de Auditoria de Acessos",
                "instructions": "1. Abra o SQL Editor ou um notebook conectado ao SQL Warehouse.\n2. Execute a consulta em `system.access.audit`:",
                "code": """# COMMAND ----------
-- Consulta eventos de leitura e gravação no Unity Catalog
SELECT 
    event_time,
    user_identity.email,
    action_name,
    request_params.table_name,
    source_ip_address
FROM system.access.audit
WHERE service_name = 'unityCatalog'
  AND event_date >= current_date() - INTERVAL 7 DAYS
ORDER BY event_time DESC
LIMIT 15;""",
                "expected_output": "Exibe registros de auditoria com e-mail, ação (getTable, readTable), tabela acessada e IP de origem."
            },
            {
                "num": 2,
                "title": "Analisar Consumo de DBUs para FinOps",
                "instructions": "1. Execute a agregação de faturamento em `system.billing.usage`:",
                "code": """# COMMAND ----------
-- Relatório de consumo de DBUs por SKU e Data
SELECT 
    usage_date,
    sku_name,
    SUM(usage_quantity) AS total_dbus
FROM system.billing.usage
WHERE usage_date >= current_date() - INTERVAL 30 DAYS
GROUP BY 1, 2
ORDER BY usage_date DESC, total_dbus DESC;""",
                "expected_output": "Exibe tabela com consumo diário de DBUs segregado por SKU (STANDARD_ALL_PURPOSE, JOBS, SERVERLESS_SQL)."
            }
        ]
    },
    "0010": {
        "title": "Lab 0010: Ingestão Escalável com Auto Loader (Cloud Files) e Schema Rescue",
        "duration": "40 minutos",
        "scenario": "Configurar ingestão incremental com Auto Loader (cloudFiles) para processar milhões de arquivos no ADLS Gen2, tolerando schema drift e resgatando colunas inesperadas em _rescued_data.",
        "azure_prereq": "Azure Databricks Workspace conectado ao storage ADLS Gen2.",
        "tasks": [
            {
                "num": 1,
                "title": "Configurar o Pipeline de Streaming com Auto Loader",
                "instructions": "1. Crie o notebook 'lab_0010_autoloader'.\n2. Digite e execute o código:",
                "code": """# COMMAND ----------
# Criação do DataFrame em streaming com Auto Loader
landing_path = "/tmp/dp750_lab_autoloader_in"
checkpoint_path = "/tmp/dp750_lab_autoloader_checkpoints"

# Simula arquivos chegando na landing zone
dbutils.fs.mkdirs(landing_path)
dbutils.fs.put(f"{landing_path}/file1.json", '{"id": 1, "produto": "Teclado", "preco": 150.0}', overwrite=True)

df_stream = (spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", f"{checkpoint_path}/schema")
    .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
    .load(landing_path))

# Inicia a gravação em streaming
query = (df_stream.writeStream
    .format("delta")
    .option("checkpointLocation", f"{checkpoint_path}/data")
    .trigger(availableNow=True)
    .table("default.lab_bronze_produtos"))

query.awaitTermination()
print("✓ Primeiro lote ingerido pelo Auto Loader!")""",
                "expected_output": "✓ Primeiro lote ingerido pelo Auto Loader!"
            },
            {
                "num": 2,
                "title": "Simular Schema Drift e Validar a Coluna _rescued_data",
                "instructions": "1. Injete um arquivo com campo novo e valor com tipo incompatível:",
                "code": """# COMMAND ----------
# Simula arquivo com coluna extra e dados fora do padrão
dbutils.fs.put(f"{landing_path}/file2.json", '{"id": 2, "produto": "Mouse", "preco": "GRATIS_PROMOCAO", "novo_campo_origem": "APP_MOBILE"}', overwrite=True)

# Dispara novo micro-lote com availableNow
query2 = (spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", f"{checkpoint_path}/schema")
    .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
    .load(landing_path)
    .writeStream
    .format("delta")
    .option("checkpointLocation", f"{checkpoint_path}/data")
    .trigger(availableNow=True)
    .table("default.lab_bronze_produtos"))

query2.awaitTermination()

# Consulta o resultado: observe o valor resgatado!
spark.sql("SELECT id, produto, preco, _rescued_data FROM default.lab_bronze_produtos").show(truncate=False)""",
                "expected_output": "+---+-------+-----+---------------------------------+\n|id |produto|preco|_rescued_data                    |\n+---+-------+-----+---------------------------------+\n|1  |Teclado|150.0|NULL                             |\n|2  |Mouse  |NULL |{\"preco\":\"GRATIS_PROMOCAO\"}      |\n+---+-------+-----+---------------------------------+\n✓ O pipeline não quebrou! O dado malformado foi preservado com segurança em _rescued_data."
            }
        ]
    },
    "0011": {
        "title": "Lab 0011: Construção de Pipeline Medallion e Upserts MERGE (SCD1 e SCD2)",
        "duration": "45 minutos",
        "scenario": "Construir a esteira completa Medallion (Bronze -> Silver -> Gold) com deduplicação por Window Functions e operações de MERGE INTO para SCD Tipo 1 e Tipo 2.",
        "azure_prereq": "Azure Databricks Workspace com acesso de gravação a tabelas Delta.",
        "tasks": [
            {
                "num": 1,
                "title": "Construir Camada Bronze e Limpeza Silver com Deduplicação",
                "instructions": "1. No notebook 'lab_0011_medallion', execute a deduplicação com funções de janela:",
                "code": """# COMMAND ----------
from pyspark.sql.window import Window
from pyspark.sql.functions import col, row_number

# Dados simulados com duplicidade e timestamps distintos
raw_data = [
    (101, "Lucas Mendes", "Curitiba", "2025-01-01 10:00:00"),
    (101, "Lucas Mendes", "São Paulo", "2025-01-02 15:30:00"), # Mais recente
    (102, "Carla Dias", "Belo Horizonte", "2025-01-01 11:00:00")
]
df_raw = spark.createDataFrame(raw_data, ["cliente_id", "nome", "cidade", "data_modificacao"])

# Deduplica selecionando apenas a linha mais recente por cliente_id
window_spec = Window.partitionBy("cliente_id").orderBy(col("data_modificacao").desc())
df_silver = df_raw.withColumn("rn", row_number().over(window_spec)).filter(col("rn") == 1).drop("rn")

df_silver.write.format("delta").mode("overwrite").saveAsTable("default.silver_clientes")
print("✓ Camada Silver deduplicada com sucesso!")
spark.sql("SELECT * FROM default.silver_clientes").show()""",
                "expected_output": "+----------+------------+---------+-------------------+\n|cliente_id|        nome|   cidade|   data_modificacao|\n+----------+------------+---------+-------------------+\n|       101|Lucas Mendes|São Paulo|2025-01-02 15:30:00|\n|       102|  Carla Dias|Belo H...|2025-01-01 11:00:00|\n+----------+------------+---------+-------------------+"
            },
            {
                "num": 2,
                "title": "Executar MERGE INTO para SCD Tipo 2 (Histórico Vigencial)",
                "instructions": "1. Na Célula 2, execute o padrão ouro de SCD2 no Delta Lake:",
                "code": """# COMMAND ----------
-- Criação da tabela de dimensão Gold com colunas de controle temporal
CREATE OR REPLACE TABLE default.gold_dim_clientes (
    cliente_id INT,
    nome STRING,
    cidade STRING,
    start_date DATE,
    end_date DATE,
    is_current BOOLEAN
);

-- Carga inicial
INSERT INTO default.gold_dim_clientes VALUES
(101, 'Lucas Mendes', 'São Paulo', '2025-01-01', NULL, true);

-- Chegada de nova atualização (mudou para Salvador):
-- 1. Expira registro antigo
MERGE INTO default.gold_dim_clientes AS target
USING (SELECT 101 AS cliente_id, 'Salvador' AS nova_cidade) AS source
ON target.cliente_id = source.cliente_id AND target.is_current = true
WHEN MATCHED AND target.cidade <> source.nova_cidade THEN
  UPDATE SET target.is_current = false, target.end_date = current_date();

-- 2. Insere novo registro vigente
INSERT INTO default.gold_dim_clientes VALUES
(101, 'Lucas Mendes', 'Salvador', current_date(), NULL, true);

SELECT * FROM default.gold_dim_clientes;""",
                "expected_output": "+----------+------------+---------+----------+----------+----------+\n|cliente_id|        nome|   cidade|start_date|  end_date|is_current|\n+----------+------------+---------+----------+----------+----------+\n|       101|Lucas Mendes|São Paulo|2025-01-01|2025-11-13|     false|\n|       101|Lucas Mendes| Salvador|2025-11-13|      NULL|      true|\n+----------+------------+---------+----------+----------+----------+"
            }
        ]
    },
    "0012": {
        "title": "Lab 0012: Engenharia de Tempo Real com Structured Streaming e Watermarking",
        "duration": "35 minutos",
        "scenario": "Processar um fluxo contínuo de cliques e telemetria, aplicando janelas temporais de agregação e descartando eventos com mais de 10 minutos de atraso para evitar esgotamento de memória no State Store.",
        "azure_prereq": "Azure Databricks Workspace com cluster ativo.",
        "tasks": [
            {
                "num": 1,
                "title": "Configurar Streaming com withWatermark e Janela Tumbling",
                "instructions": "1. Abra o notebook 'lab_0012_streaming_watermark'.\n2. Execute a query de streaming em memória:",
                "code": """# COMMAND ----------
from pyspark.sql.functions import col, window, current_timestamp

# Gera stream sintético de eventos com timestamp
df_rate = spark.readStream.format("rate").option("rowsPerSecond", 5).load() \\
               .withColumn("sensor_id", (col("value") % 3).cast("string")) \\
               .withColumn("timestamp", current_timestamp())

# Define o Watermark de 10 minutos para descarte de dados atrasados
df_watermarked = df_rate.withWatermark("timestamp", "10 minutes") \\
                        .groupBy(window("timestamp", "5 seconds"), "sensor_id") \\
                        .count()

# Inicia o stream em memória para inspeção interativa
query = df_watermarked.writeStream \\
                      .format("memory") \\
                      .queryName("agregacao_sensores_stream") \\
                      .outputMode("complete") \\
                      .start()

query.awaitTermination(timeout=15)
query.stop()

# Consulta os resultados calculados pela janela
spark.sql("SELECT * FROM agregacao_sensores_stream ORDER BY window.start DESC LIMIT 10").show(truncate=False)""",
                "expected_output": "+------------------------------------------+---------+-----+\n|window                                    |sensor_id|count|\n+------------------------------------------+---------+-----+\n|{2025-11-13 17:00:05, 2025-11-13 17:00:10}|0        |8    |\n|{2025-11-13 17:00:05, 2025-11-13 17:00:10}|1        |9    |\n+------------------------------------------+---------+-----+"
            }
        ]
    },
    "0013": {
        "title": "Lab 0013: Otimização Física: Liquid Clustering e Deletion Vectors",
        "duration": "35 minutos",
        "scenario": "Comparar a flexibilidade do Liquid Clustering (CLUSTER BY) em relação ao particionamento tradicional e testar a velocidade instantânea de mutações com Deletion Vectors habilitados.",
        "azure_prereq": "Azure Databricks Workspace com Databricks Runtime 13.3 LTS ou superior.",
        "tasks": [
            {
                "num": 1,
                "title": "Criar Tabela com Liquid Clustering (CLUSTER BY)",
                "instructions": "1. Crie o notebook 'lab_0013_liquid_clustering'.\n2. Execute os comandos SQL de criação e alteração de chaves:",
                "code": """# COMMAND ----------
-- Criação de tabela utilizando Liquid Clustering moderno
CREATE OR REPLACE TABLE default.telemetria_liquid (
    id_dispositivo BIGINT,
    data_evento DATE,
    pais STRING,
    temperatura DOUBLE
) USING DELTA
CLUSTER BY (data_evento, pais);

-- Inserção de dados
INSERT INTO default.telemetria_liquid VALUES
(1001, '2025-01-01', 'BR', 28.5),
(1002, '2025-01-01', 'US', -2.1),
(1003, '2025-01-02', 'BR', 30.1);

-- Alteração dinâmica de chaves de clustering sem recriar a tabela!
ALTER TABLE default.telemetria_liquid CLUSTER BY (data_evento, pais, id_dispositivo);

-- Otimização incremental
OPTIMIZE default.telemetria_liquid;""",
                "expected_output": "✓ Tabela otimizada com Liquid Clustering incremental sem sobrecarga de Z-Order!"
            },
            {
                "num": 2,
                "title": "Validar Deletion Vectors em Operações de DELETE",
                "instructions": "1. Na Célula 2, valide a propriedade de Deletion Vectors:",
                "code": """# COMMAND ----------
-- Habilita Deletion Vectors explicitamente caso não esteja por padrão
ALTER TABLE default.telemetria_liquid SET TBLPROPERTIES ('delta.enableDeletionVectors' = true);

-- Executa DELETE que agora não reescreve arquivos inteiros, apenas grava o bitmap
DELETE FROM default.telemetria_liquid WHERE id_dispositivo = 1002;

-- Inspeciona o histórico comprovando o uso de Deletion Vectors
DESCRIBE HISTORY default.telemetria_liquid;""",
                "expected_output": "Exibe commit de DELETE indicando gravação leve de deletionVector."
            }
        ]
    },
    "0014": {
        "title": "Lab 0014: Pipelines Declarativos com Delta Live Tables (DLT) e Expectations",
        "duration": "45 minutos",
        "scenario": "Construir um pipeline corporativo DLT em Python declarativo com Streaming Tables, Materialized Views e regras de qualidade de dados (Expectations: EXPECT, DROP ROW, FAIL UPDATE).",
        "azure_prereq": "Azure Databricks Workspace com acesso à criação de Pipelines Delta Live Tables.",
        "tasks": [
            {
                "num": 1,
                "title": "Criar o Arquivo de Código Python do DLT",
                "instructions": "1. No Workspace, crie um notebook chamado `dlt_orders_pipeline` com linguagem Python.\n2. Insira o código declarativo oficial do DLT:",
                "code": """# COMMAND ----------
import dlt
from pyspark.sql.functions import col, expr

# 1. Camada Bronze: Streaming Table ingerindo dados contínuos
@dlt.table(
    name="bronze_pedidos_raw",
    comment="Tabela Bronze de pedidos brutos"
)
def bronze_pedidos_raw():
    return (spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "json")
        .load("/tmp/dlt_pedidos_in/"))

# 2. Camada Silver: Com Expectations de governança de qualidade
@dlt.table(
    name="silver_pedidos_validos",
    comment="Tabela Silver com regras de integridade"
)
@dlt.expect_or_drop("valor_positivo", "valor > 0")
@dlt.expect("cliente_obrigatorio", "cliente_id IS NOT NULL")
def silver_pedidos_validos():
    return dlt.read_stream("bronze_pedidos_raw").select("pedido_id", "cliente_id", "valor")

# 3. Camada Gold: Materialized View agregada para relatórios de BI
@dlt.table(
    name="gold_faturamento_cliente",
    comment="Visão materializada de faturamento"
)
def gold_faturamento_cliente():
    return (dlt.read("silver_pedidos_validos")
        .groupBy("cliente_id")
        .agg(expr("sum(valor) as total_gasto")))""",
                "expected_output": "✓ Código DLT salvo no notebook."
            },
            {
                "num": 2,
                "title": "Criar e Executar o Pipeline no Delta Live Tables UI",
                "instructions": "1. No menu lateral do Databricks, clique em 'Delta Live Tables' (ou 'Pipelines').\n2. Clique em 'Create pipeline'.\n3. Configure:\n   - Pipeline name: `DP750-Orders-DLT`\n   - Source code: selecione o notebook `dlt_orders_pipeline` recém-criado.\n   - Destination: Unity Catalog (selecione seu catálogo e schema).\n   - Pipeline mode: 'Triggered' (para execução sob demanda) e 'Development' (mantém o cluster pré-aquecido).\n4. Clique em 'Start'.\n5. Observe o grafo acíclico dirigido (DAG) verde se formando na interface e inspecione as métricas de linhas aprovadas e descartadas pela Expectation!"
            }
        ]
    },
    "0015": {
        "title": "Lab 0015: Orquestração em Produção: Databricks Workflows, DABs e Spark UI",
        "duration": "45 minutos",
        "scenario": "Orquestrar um pipeline multitarefa no Databricks Workflows, utilizar Task Values, simular falha e executar Repair Run, além de validar o manifesto de Databricks Asset Bundles (databricks.yml).",
        "azure_prereq": "Azure Databricks Workspace com acesso a Workflows e Databricks CLI configurada localmente.",
        "tasks": [
            {
                "num": 1,
                "title": "Criar um Job Multitarefa no Databricks Workflows",
                "instructions": "1. No menu esquerdo, clique em 'Workflows' > 'Jobs' > 'Create job'.\n2. Configure a Tarefa 1:\n   - Task name: `01_bronze_ingestion`\n   - Type: Notebook\n   - Compute: New Job Cluster (Standard_D4ds_v5)\n3. Clique no botão '+' abaixo da Tarefa 1 para adicionar a Tarefa 2:\n   - Task name: `02_silver_transform`\n   - Depends on: `01_bronze_ingestion`\n4. Salve o Job com o nome `DP750-Production-Orchestrator`."
            },
            {
                "num": 2,
                "title": "Utilizar Task Values para Passagem de Parâmetros",
                "instructions": "1. Na Tarefa 1, insira o código PySpark para exportar o ID do lote:\n   `dbutils.jobs.taskValues.set(key=\"batch_run_id\", value=\"LOTE_2025_001\")`\n2. Na Tarefa 2, insira o código para consumir o valor:\n   `lote = dbutils.jobs.taskValues.get(taskKey=\"01_bronze_ingestion\", key=\"batch_run_id\")`\n   `print(f'Processando lote: {lote}')`"
            },
            {
                "num": 3,
                "title": "Simular Falha e Executar o Recurso 'Repair Run'",
                "instructions": "1. Adicione um comando proposital de erro na Tarefa 2 (`raise ValueError('Erro temporário de conexão')`).\n2. Clique em 'Run now'. O job executará a Tarefa 1 com sucesso e falhará na Tarefa 2.\n3. Corrija o erro no notebook da Tarefa 2.\n4. Na tela de execução do Job, clique no botão 'Repair run'. Observe que a Tarefa 1 NÃO É REEXECUTADA, poupando tempo e DBUs, executando exclusivamente a Tarefa 2 que havia falhado!"
            },
            {
                "num": 4,
                "title": "Validar Manifesto de Databricks Asset Bundles (databricks.yml)",
                "instructions": "1. Em seu terminal local, crie o arquivo `databricks.yml` e valide a sintaxe oficial:\n   `databricks bundle validate`\n2. Observe a saída confirmando que os recursos de jobs e pipelines estão sintaticamente corretos para deploy via CI/CD no Azure DevOps ou GitHub Actions."
            }
        ]
    }
}

