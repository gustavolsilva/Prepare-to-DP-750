#!/usr/bin/env python3
"""
Databricks Formation — Prepare to DP-750
Gerador das 6 Folhas de Referência Rápida (Cheat Sheets de Alta Densidade Técnica)
Alinhadas 100% com as especificações oficiais do Exame Microsoft DP-750.
"""

import os

REFERENCES = [
    {
        "id": "01",
        "slug": "01-spark-and-databricks-architecture-visual-guide",
        "title": "Folha 01: Guia Visual de Arquitetura Apache Spark, Compute Plane & FinOps",
        "desc": "Control Plane vs Compute Plane, Driver & Executors, Catalyst Optimizer, Photon Engine C++, Pools e Governança de DBUs.",
        "content": """
        <h2>1. Control Plane vs Compute Plane no Azure Databricks</h2>
        <p>No Azure Databricks, a separação rígida de responsabilidades entre Control Plane e Compute Plane é a base de segurança, conformidade e governança de dados exigida no exame DP-750:</p>
        <table>
          <thead>
            <tr>
              <th>Camada Arquitetural</th>
              <th>Localização Física</th>
              <th>Componentes Hospedados</th>
              <th>Acesso a Dados de Clientes?</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Control Plane</strong></td>
              <td>Assinatura gerenciada pela Microsoft/Databricks na região do Azure</td>
              <td>Web Application UI, serviço de Notebooks, Job Scheduler, Cluster Manager e metadados de orquestração</td>
              <td><strong>NUNCA</strong> (dados de negócio NUNCA residem nem transitam pelo Control Plane)</td>
            </tr>
            <tr>
              <td><strong>Compute Plane (Classic)</strong></td>
              <td>Assinatura Azure do Cliente (Customer VNet gerenciada ou injetada)</td>
              <td>VMs dos Clusters (Driver e Workers), armazenamento DBFS raiz local e caches em memória/disco</td>
              <td><strong>SIM</strong> (lê e grava diretamente nos containers do ADLS Gen2 via credenciais seguras)</td>
            </tr>
            <tr>
              <td><strong>Compute Plane (Serverless)</strong></td>
              <td>Rede segura isolada gerenciada pela Databricks na mesma região do cliente</td>
              <td>MicroVMs efêmeras, Serverless SQL Warehouses, Serverless Jobs e pipelines de computação sob demanda</td>
              <td><strong>SIM</strong> (acessa o ADLS Gen2 do cliente via túneis privados e credenciais efêmeras do Entra ID)</td>
            </tr>
          </tbody>
        </table>

        <h2>2. Conectividade Segura: Secure Cluster Connectivity & Private Link</h2>
        <ul>
          <li><strong>Secure Cluster Connectivity (No Public IP - NPIP):</strong> Por padrão, os nós de computação no Compute Plane não possuem endereços IP públicos. Toda comunicação com o Control Plane ocorre via túneis TLS de saída (outbound) na porta 443 através de uma interface de rede segura (SCC relay). Não é necessário abrir nenhuma porta de entrada (inbound) no NSG.</li>
          <li><strong>VNet Injection:</strong> Permite implantar o Compute Plane em uma Rede Virtual (VNet) própria do cliente. <em>Requisito do DP-750:</em> Exige exatamente <strong>duas subnets dedicadas</strong> (uma pública/host e uma privada/container), cada uma com tamanho mínimo <strong>/26</strong> (recomendado <strong>/24</strong>), delegadas exclusivamente para o serviço <code>Microsoft.Databricks/workspaces</code>.</li>
          <li><strong>Azure Private Link:</strong>
            <ul>
              <li><strong>Front-end Private Link:</strong> Isola o acesso de analistas e conexões REST API do portal web, eliminando a exposição pública da UI do workspace.</li>
              <li><strong>Back-end Private Link:</strong> Isola a comunicação interna entre os nós do Compute Plane e a infraestrutura de gerenciamento do Control Plane.</li>
            </ul>
          </li>
        </ul>

        <h2>3. Anatomia do Apache Spark & Pipeline do Catalyst Optimizer</h2>
        <p>O Apache Spark opera sob o modelo mestre-trabalhador (Master-Worker), onde o <strong>Driver</strong> coordena a execução e os <strong>Executors</strong> processam partições de dados:</p>
        <pre><code>-- Fluxo de Compilação de Consultas no Apache Spark:
1. Unresolved Logical Plan: Sintaxe inicial de DataFrames PySpark ou consultas Spark SQL.
2. Analyzed Logical Plan: Validação de nomes de tabelas, colunas e tipos contra o Unity Catalog Metastore.
3. Optimized Logical Plan: Aplicação de regras heurísticas do Catalyst:
   - Predicate Pushdown (empurra filtros para o storage ADLS Gen2 antes de ler tudo).
   - Column Pruning (elimina colunas desnecessárias da memória).
   - Constant Folding e simplificação de expressões booleanas.
4. Physical Plans: Geração de múltiplos planos físicos candidatos avaliados pelo Cost-Based Optimizer (CBO).
5. Selected Physical Plan: Compilação do plano vencedor para:
   - WholeStageCodegen (Bytecode Java otimizado via Tungsten).
   - Photon Execution Engine (Instruções C++ vetorizadas SIMD caso habilitado).</code></pre>

        <h2>4. Photon Engine Vectorized Execution vs Spark Tradicional</h2>
        <table>
          <thead>
            <tr>
              <th>Dimensão</th>
              <th>Apache Spark Tradicional (Tungsten)</th>
              <th>Photon Engine (C++ Vetorizado)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Linguagem do Motor</strong></td>
              <td>Java / Scala compilado para bytecode na JVM</td>
              <td>C++ nativo com instruções de CPU vetorizadas (SIMD)</td>
            </tr>
            <tr>
              <td><strong>Processamento de Dados</strong></td>
              <td>Iterador linha a linha com sobrecarga de chamadas de métodos</td>
              <td>Processa blocos de milhares de linhas por ciclo de clock de CPU</td>
            </tr>
            <tr>
              <td><strong>Impacto de Garbage Collection</strong></td>
              <td>Sujeito a pausas de GC da JVM em grandes joins e agregações</td>
              <td>Gerenciamento nativo de memória fora da JVM (Zero pausas de GC)</td>
            </tr>
            <tr>
              <td><strong>Ganhos de Performance</strong></td>
              <td>Linha de base</td>
              <td>Aceleração de 3x a 8x em scans Delta, agregações, joins e merges</td>
            </tr>
          </tbody>
        </table>

        <h2>5. Matriz de Tipos de Computação & FinOps de DBUs</h2>
        <table>
          <thead>
            <tr>
              <th>Tipo de Cluster</th>
              <th>Caso de Uso Recomendado</th>
              <th>Custo de DBUs</th>
              <th>Política de Autotermination Recomendada</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>All-Purpose Cluster</strong></td>
              <td>Desenvolvimento interativo, exploração de dados e testes em notebooks</td>
              <td>Alta (~$0.55/DBU)</td>
              <td>15 a 20 minutos (imposto rigorosamente via Cluster Policy)</td>
            </tr>
            <tr>
              <td><strong>Job Cluster (Efêmero)</strong></td>
              <td>Workloads de produção agendados via Databricks Workflows</td>
              <td>Baixa (~$0.20-0.40/DBU; até 60% mais barato)</td>
              <td>Destruído automaticamente logo após a conclusão da tarefa</td>
            </tr>
            <tr>
              <td><strong>Serverless SQL Warehouse</strong></td>
              <td>Dashboards BI (Power BI), consultas analíticas ad-hoc e Lakeview</td>
              <td>Cobrança por segundo exato</td>
              <td>1 a 5 minutos de inatividade (inicialização instantânea sub-10s)</td>
            </tr>
            <tr>
              <td><strong>Databricks Instance Pool</strong></td>
              <td>Reduzir tempo de boot de clusters recorrentes de 5-7 min para &lt; 30s</td>
              <td>Zero DBU enquanto ocioso (apenas custo de VM Azure)</td>
              <td>Configurar Min Idle instances durante horário comercial</td>
            </tr>
            <tr>
              <td><strong>Single-Node Cluster</strong></td>
              <td>Cargas de trabalho que não precisam de paralelismo (MLflow, APIs, metadados)</td>
              <td>Baixíssima (1 única VM atuando como Driver e Executor)</td>
              <td>Desativa workers; previne alocação desnecessária de nós</td>
            </tr>
          </tbody>
        </table>

        <h2>6. ⚠️ Pegadinhas Críticas do Exame DP-750 (Arquitetura & FinOps)</h2>
        <blockquote>
          <ul>
            <li><strong>All-Purpose vs Job Cluster em Produção:</strong> Se a questão mencionar um pipeline que roda diariamente ou periodicamente e perguntar como reduzir custos de nuvem, a resposta correta SEMPRE envolve migrar o notebook para um <strong>Databricks Workflow orquestrado com Job Cluster efêmero</strong>.</li>
            <li><strong>Montagens Legadas no DBFS (/mnt):</strong> O exame considera o uso de <code>dbutils.fs.mount()</code> e chaves de acesso em texto plano uma prática legada obsoleta. A abordagem moderna oficial do DP-750 exige <strong>Unity Catalog com Storage Credentials e External Locations</strong> ou <strong>Volumes</strong>.</li>
            <li><strong>Subnets para VNet Injection:</strong> Lembre-se: duas subnets exclusivas, tamanho mínimo <code>/26</code>, delegadas para <code>Microsoft.Databricks/workspaces</code>. Elas NÃO podem ser compartilhadas com nenhum outro recurso da Azure.</li>
          </ul>
        </blockquote>
        """
    },
    {
        "id": "02",
        "slug": "02-unity-catalog-security-and-governance-guide",
        "title": "Folha 02: Guia de Governança e Segurança com Unity Catalog",
        "desc": "Metastore Regional, 3-Level Namespace, Managed vs External Tables & Volumes, Privilégios Hierárquicos (DCL), Row Filters, Column Masks e Delta Sharing.",
        "content": """
        <h2>1. Arquitetura do Unity Catalog: Metastore Regional & 3-Level Namespace</h2>
        <p>O Unity Catalog é o mecanismo unificado de governança do Databricks Lakehouse. Principais premissas arquiteturais testadas no exame:</p>
        <ul>
          <li><strong>Um Metastore por Região:</strong> Um único Metastore do Unity Catalog atende a múltiplos workspaces na mesma região da nuvem.</li>
          <li><strong>Namespace de 3 Níveis (catalog.schema.table_or_volume):</strong> Elimina a dependência do catálogo legado <code>hive_metastore</code> e possibilita consultas cruzadas totalmente qualificadas:</li>
        </ul>
        <pre><code>-- Consulta totalmente qualificada (FQDN) no Unity Catalog:
SELECT 
    c.id_cliente,
    c.nome_cliente,
    v.valor_total
FROM prod_lakehouse.financeiro.clientes AS c
JOIN prod_lakehouse.vendas.pedidos AS v
  ON c.id_cliente = v.id_cliente
WHERE v.data_pedido >= '2025-01-01';</code></pre>

        <h2>2. Managed Tables vs External Tables</h2>
        <table>
          <thead>
            <tr>
              <th>Característica</th>
              <th>Managed Table (Tabela Gerenciada)</th>
              <th>External Table (Tabela Externa)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Localização dos Dados</strong></td>
              <td>Armazenada no storage raiz padrão associado ao Schema ou Catalog</td>
              <td>Armazenada em um caminho explícito dentro de uma External Location no ADLS Gen2</td>
            </tr>
            <tr>
              <td><strong>Comportamento do DROP TABLE</strong></td>
              <td><strong>Exclui os Metadados E os arquivos físicos de dados Parquet</strong></td>
              <td><strong>Exclui APENAS os Metadados</strong> no Unity Catalog; os dados físicos no ADLS Gen2 permanecem intactos</td>
            </tr>
            <tr>
              <td><strong>Criação Típica SQL</strong></td>
              <td><code>CREATE TABLE cat.sch.tbl (id INT, nome STRING);</code></td>
              <td><code>CREATE TABLE cat.sch.tbl (...) LOCATION 'abfss://...';</code></td>
            </tr>
            <tr>
              <td><strong>Uso Recomendado</strong></td>
              <td>Tabelas internas padrão criadas e gerenciadas 100% pelo Databricks</td>
              <td>Dados compartilhados com outras ferramentas ou ingeridos externamente</td>
            </tr>
          </tbody>
        </table>

        <h2>3. Managed Volumes vs External Volumes</h2>
        <p>Volumes governam arquivos <strong>não tabulares</strong> (CSVs brutos, JSONs, logs, imagens, PDFs, arquivos de modelo MLflow) com controle de acesso RBAC:</p>
        <ul>
          <li><strong>Managed Volume:</strong> Os arquivos residem no storage padrão do Unity Catalog. Se o volume for excluído com <code>DROP VOLUME</code>, os arquivos são apagados.</li>
          <li><strong>External Volume:</strong> Aponta para um caminho em uma External Location. Se o volume for excluído, os arquivos no ADLS Gen2 continuam preservados.</li>
          <li><strong>Caminho POSIX Padronizado:</strong> Acessível em código PySpark/Python via caminho montado: <code>/Volumes/catalogo/schema/nome_volume/arquivo.csv</code>.</li>
        </ul>

        <h2>4. Storage Credentials & External Locations (Infraestrutura de Acesso)</h2>
        <pre><code>-- 1. Criação da Storage Credential usando a Identidade Gerenciada do Azure (Access Connector):
CREATE STORAGE CREDENTIAL cred_managed_identity
WITH (
    AZURE_MANAGED_IDENTITY = (
        RESOURCE_ID = '/subscriptions/.../resourceGroups/.../providers/Microsoft.Databricks/accessConnectors/meu-conector'
    )
)
COMMENT 'Credencial oficial usando Managed Identity com permissão Storage Blob Data Contributor';

-- 2. Criação da External Location associando o container ADLS Gen2 à credencial:
CREATE EXTERNAL LOCATION loc_adls_raw
URL 'abfss://raw@datalakeprod.dfs.core.windows.net/'
WITH (STORAGE CREDENTIAL cred_managed_identity)
COMMENT 'Localização externa para dados brutos de ingestão';</code></pre>

        <h2>5. Matriz de Concessão de Privilégios Hierárquicos (DCL)</h2>
        <p>No Unity Catalog, o acesso é hierárquico e explícito. Para que um usuário consiga ler uma tabela, ele necessita de privilégios cumulativos em toda a árvore:</p>
        <table>
          <thead>
            <tr>
              <th>Objeto</th>
              <th>Privilégio Essencial</th>
              <th>Comando SQL Oficial</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Catalog</strong></td>
              <td>USE CATALOG</td>
              <td><code>GRANT USE CATALOG ON CATALOG prod_lakehouse TO `analistas_bi`;</code></td>
            </tr>
            <tr>
              <td><strong>Schema</strong></td>
              <td>USE SCHEMA, CREATE TABLE</td>
              <td><code>GRANT USE SCHEMA, CREATE TABLE ON SCHEMA prod_lakehouse.vendas TO `analistas_bi`;</code></td>
            </tr>
            <tr>
              <td><strong>Table / View</strong></td>
              <td>SELECT, MODIFY</td>
              <td><code>GRANT SELECT ON TABLE prod_lakehouse.vendas.pedidos TO `analistas_bi`;</code></td>
            </tr>
            <tr>
              <td><strong>Volume</strong></td>
              <td>READ VOLUME, WRITE VOLUME</td>
              <td><code>GRANT READ VOLUME ON VOLUME prod_lakehouse.vendas.raw_files TO `engenharia_dados`;</code></td>
            </tr>
          </tbody>
        </table>

        <h2>6. Row Filters e Column Masks Dinâmicas (Proteção Fina de Dados)</h2>
        <pre><code>-- 1. Função de Filtro por Linha (Row Filter): Analistas do Brasil só veem clientes do Brasil
CREATE OR REPLACE FUNCTION prod_lakehouse.seguranca.filtro_pais_cliente(pais STRING)
RETURN IF(is_account_group_member('diretoria_global'), true, pais = 'Brasil');

ALTER TABLE prod_lakehouse.vendas.clientes
SET ROW FILTER prod_lakehouse.seguranca.filtro_pais_cliente ON (pais_residencia);

-- 2. Função de Mascaramento Dinâmico de Coluna (Column Mask): Ocultar CPF para não autorizados
CREATE OR REPLACE FUNCTION prod_lakehouse.seguranca.mascarar_cpf(cpf STRING)
RETURN IF(is_account_group_member('compliance_auditores'), cpf, CONCAT('***.***.', RIGHT(cpf, 2)));

ALTER TABLE prod_lakehouse.vendas.clientes
ALTER COLUMN cpf SET MASK prod_lakehouse.seguranca.mascarar_cpf;</code></pre>

        <h2>7. Delta Sharing & Auditoria com System Tables</h2>
        <ul>
          <li><strong>Delta Sharing:</strong> Primeiro protocolo aberto do mercado para compartilhamento seguro de tabelas ativas com destinatários dentro ou fora do Databricks (via REST API aberta, sem replicação física de dados).</li>
          <li><strong>System Tables:</strong>
            <ul>
              <li><code>system.access.audit</code>: Rastreia eventos de auditoria (quem consultou qual tabela, quando e de onde).</li>
              <li><code>system.billing.usage</code>: Rastreia o consumo exato de DBUs por workspace, cluster, SKU e tags de faturamento.</li>
              <li><code>system.lineage.table_lineage</code>: Rastreia a árvore completa de dependência entre tabelas e colunas.</li>
            </ul>
          </li>
        </ul>

        <h2>8. ⚠️ Pegadinhas Críticas do Exame DP-750 (Unity Catalog)</h2>
        <blockquote>
          <ul>
            <li><strong>Falta de USE CATALOG / USE SCHEMA:</strong> Conceder apenas <code>GRANT SELECT ON TABLE tbl TO grupo;</code> NÃO funcionará se o grupo não possuir <code>USE CATALOG</code> no catálogo pai e <code>USE SCHEMA</code> no schema pai.</li>
            <li><strong>Perda de Dados com DROP TABLE:</strong> Se uma tabela for <em>Managed</em>, o <code>DROP TABLE</code> exclui permanentemente os dados do storage. Se a intenção for apenas remover o registro do catálogo mantendo os dados no ADLS Gen2, ela deve ser criada como <em>External Table</em>.</li>
          </ul>
        </blockquote>
        """
    },
    {
        "id": "03",
        "slug": "03-ingestion-autoloader-and-dlt-decision-matrix",
        "title": "Folha 03: Matriz de Decisão: Auto Loader vs COPY INTO vs DLT vs Lakeflow",
        "desc": "Critérios de seleção para Ingestão Incremental, Auto Loader (cloudFiles), Schema Evolution, Rescued Data e Delta Live Tables.",
        "content": """
        <h2>1. Matriz Definitiva de Decisão de Ingestão do DP-750</h2>
        <table>
          <thead>
            <tr>
              <th>Critério / Requisito</th>
              <th>Auto Loader (cloudFiles)</th>
              <th>COPY INTO (SQL)</th>
              <th>Delta Live Tables (DLT)</th>
              <th>Lakeflow Connect</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Escala de Arquivos</strong></td>
              <td>Milhões de arquivos contínuos</td>
              <td>Milhares a centenas de milhares</td>
              <td>Qualquer escala declarativa</td>
              <td>Bancos OLTP relacionais e SaaS</td>
            </tr>
            <tr>
              <td><strong>Suporte a Streaming</strong></td>
              <td><strong>SIM</strong> (Spark Structured Streaming)</td>
              <td>NÃO (Apenas Batch idempotente)</td>
              <td><strong>SIM</strong> (Streaming Tables)</td>
              <td>Automático via pipelines DLT</td>
            </tr>
            <tr>
              <td><strong>Schema Drift &amp; Evolution</strong></td>
              <td>Automático com <code>_rescued_data</code></td>
              <td>Exige schema estável pré-definido</td>
              <td>Nativo em Streaming Tables</td>
              <td>Schema mapping gerenciado</td>
            </tr>
            <tr>
              <td><strong>Modo de Detecção</strong></td>
              <td>Directory Listing ou Event Grid</td>
              <td>Varredura de diretório (List API)</td>
              <td>Gerenciado pelo runtime DLT</td>
              <td>CDC direto na fonte</td>
            </tr>
            <tr>
              <td><strong>Custo e Complexidade</strong></td>
              <td>Baixíssimo; ideal para cloud files</td>
              <td>Mínimo; simples comando SQL</td>
              <td>Gerenciado; inclui Data Quality</td>
              <td>Conectores nativos Databricks</td>
            </tr>
          </tbody>
        </table>

        <h2>2. Auto Loader: Directory Listing vs File Notification</h2>
        <ul>
          <li><strong>Directory Listing Mode (Padrão):</strong> O Auto Loader lista recursivamente os arquivos no diretório do storage no ADLS Gen2. É rápido e não exige nenhuma infraestrutura adicional no Azure. É recomendado para diretórios com até <strong>alguns milhões de arquivos</strong>.</li>
          <li><strong>File Notification Mode:</strong> Para diretórios que acumulam <strong>dezenas de milhões de arquivos</strong>, o Auto Loader cria automaticamente um <strong>Azure Event Grid</strong> e uma fila <strong>Azure Queue Storage</strong> para escutar notificações de novos blobs. Isso elimina a latência de listar arquivos e evita gargalos no Driver.</li>
        </ul>

        <h2>3. Schema Evolution Modes & Coluna _rescued_data no Auto Loader</h2>
        <pre><code>-- Opções para cloudFiles.schemaEvolutionMode:
1. addNewColumns (Padrão): Novas colunas detectadas nos arquivos são adicionadas automaticamente ao schema Delta.
2. rescue: O schema permanece estrito, mas qualquer coluna nova ou dado corrompido é gravado na coluna _rescued_data.
3. failOnNewColumns: O pipeline falha imediatamente se detectar um campo novo, exigindo intervenção manual.
4. none: Ignora novos campos nos arquivos sem adicioná-los.</code></pre>

        <h2>4. Snippet Padrão Ouro de Auto Loader com Trigger AvailableNow</h2>
        <pre><code>from pyspark.sql.functions import current_timestamp

# Ingestão contínua com suporte a schema drift e processamento efêmero
df_stream = (spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", "abfss://checkpoints@adls.dfs.core.windows.net/schemas/pedidos")
    .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
    .option("cloudFiles.inferColumnTypes", "true")
    .load("abfss://raw@adls.dfs.core.windows.net/landing/pedidos/"))

# Adicionando metadados de ingestão
df_bronze = df_stream.withColumn("ingestion_time", current_timestamp())

# Gravando na camada Bronze com trigger AvailableNow (ideal para Job Clusters)
query = (df_bronze.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "abfss://checkpoints@adls.dfs.core.windows.net/checkpoints/pedidos_bronze")
    .trigger(availableNow=True)
    .toTable("prod_lakehouse.bronze.pedidos_raw"))

query.awaitTermination()</code></pre>

        <h2>5. Comando COPY INTO (Batch SQL Idempotente)</h2>
        <pre><code>-- Ingestão batch de arquivos Parquet com idempotência nativa:
COPY INTO prod_lakehouse.bronze.telemetria_copy
FROM 'abfss://raw@adls.dfs.core.windows.net/telemetria/'
FILEFORMAT = PARQUET
FILES = ('telemetria_20250101.parquet', 'telemetria_20250102.parquet')
FORMAT_OPTIONS ('mergeSchema' = 'true')
COPY_OPTIONS ('force' = 'false'); -- force=false garante que arquivos já carregados sejam ignorados</code></pre>

        <h2>6. ⚠️ Pegadinhas Críticas do Exame DP-750 (Ingestão)</h2>
        <blockquote>
          <ul>
            <li><strong>COPY INTO vs Auto Loader em Streaming:</strong> Se o enunciado mencionar carregamento <em>contínuo</em> ou <em>streaming</em> com <em>schema drift</em> inesperado, a resposta correta é <strong>Auto Loader (cloudFiles)</strong>. <code>COPY INTO</code> só roda em batch estático.</li>
            <li><strong>Trigger Once vs AvailableNow:</strong> O trigger <code>once=True</code> está depreciado no Spark moderno. O padrão oficial testado no DP-750 para processar lotes pendentes em Jobs efêmeros é <code>trigger(availableNow=True)</code>.</li>
            <li><strong>Onde os dados corrompidos vão no Auto Loader?</strong> Sempre para a coluna oculta especial <strong><code>_rescued_data</code></strong> em formato de string JSON.</li>
          </ul>
        </blockquote>
        """
    },
    {
        "id": "04",
        "slug": "04-pyspark-and-spark-sql-engineering-cheatsheet",
        "title": "Folha 04: Cheatsheet de Engenharia: PySpark, Spark SQL & MERGE SCD2",
        "desc": "Transformações essenciais, Window Functions para deduplicação, tratamento de JSON aninhado e MERGE INTO para SCD Tipo 1 e Tipo 2.",
        "content": """
        <h2>1. Funções de Janela (Window Functions) para Deduplicação de Dados</h2>
        <pre><code>from pyspark.sql.window import Window
from pyspark.sql.functions import col, row_number, dense_rank, lag, lead

# Cenário: Manter apenas o evento mais recente de cada cliente (Deduplicação Silver)
window_dedup = Window.partitionBy("id_cliente").orderBy(col("timestamp_evento").desc())

df_silver_dedup = (df_bronze
    .withColumn("row_num", row_number().over(window_dedup))
    .filter(col("row_num") == 1)
    .drop("row_num"))</code></pre>

        <h2>2. Manipulação de Colunas Complexas e JSON Aninhado</h2>
        <pre><code>from pyspark.sql.functions import from_json, to_json, explode, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, ArrayType

# Schema para array de itens dentro do pedido
schema_itens = ArrayType(StructType([
    StructField("produto_id", StringType(), False),
    StructField("quantidade", DoubleType(), False),
    StructField("valor_unitario", DoubleType(), False)
]))

# Desaninhando itens com explode
df_pedidos_detalhados = (df_raw
    .withColumn("itens_array", from_json(col("payload_json"), schema_itens))
    .withColumn("item", explode(col("itens_array")))
    .select(
        col("pedido_id"),
        col("cliente_id"),
        col("item.produto_id"),
        col("item.quantidade"),
        col("item.valor_unitario"),
        (col("item.quantidade") * col("item.valor_unitario")).alias("subtotal")
    ))</code></pre>

        <h2>3. MERGE INTO no Delta Lake: SCD Tipo 1 (Sobrescrita Simples)</h2>
        <pre><code>-- MERGE SCD Tipo 1: Atualiza registros existentes ou insere novos registros
MERGE INTO prod_lakehouse.silver.dim_cliente AS target
USING staging_clientes AS source
ON target.id_cliente = source.id_cliente
WHEN MATCHED THEN
  UPDATE SET 
    target.nome = source.nome,
    target.email = source.email,
    target.cidade = source.cidade,
    target.data_atualizacao = current_timestamp()
WHEN NOT MATCHED THEN
  INSERT (id_cliente, nome, email, cidade, data_atualizacao)
  VALUES (source.id_cliente, source.nome, source.email, source.cidade, current_timestamp());</code></pre>

        <h2>4. MERGE INTO no Delta Lake: SCD Tipo 2 (Histórico com Vigência)</h2>
        <pre><code>-- MERGE SCD Tipo 2: Mantém histórico com colunas is_current, start_date e end_date

-- Passo 1: Fechar a vigência do registro antigo que sofreu alteração cadastral
MERGE INTO prod_lakehouse.silver.dim_fornecedor AS target
USING staging_fornecedor AS source
ON target.id_fornecedor = source.id_fornecedor 
   AND target.is_current = true
WHEN MATCHED AND (target.endereco <> source.endereco OR target.telefone <> source.telefone) THEN
  UPDATE SET 
    target.is_current = false, 
    target.end_date = current_date();

-- Passo 2: Inserir a nova versão ativa
MERGE INTO prod_lakehouse.silver.dim_fornecedor AS target
USING staging_fornecedor AS source
ON target.id_fornecedor = source.id_fornecedor 
   AND target.endereco = source.endereco 
   AND target.is_current = true
WHEN NOT MATCHED THEN
  INSERT (id_fornecedor, nome, endereco, telefone, start_date, end_date, is_current)
  VALUES (source.id_fornecedor, source.nome, source.endereco, source.telefone, current_date(), NULL, true);</code></pre>

        <h2>5. Otimização de Joins: Broadcast Join vs Skew Join Hints</h2>
        <pre><code>from pyspark.sql.functions import broadcast

-- 1. Broadcast Hash Join: Ideal quando uma das tabelas é pequena (ex: dimensional &lt; 100 MB)
-- Elimina completamente o shuffle de rede pela troca de dados:
df_resultado = df_fatos_grande.join(broadcast(df_dimensao_pequena), "id_categoria")

-- 2. Skew Join Hint no Spark SQL: Quando uma chave tem distribuição desbalanceada (ex: NULLs ou 'SP')
-- O Spark divide a partição pesada em sub-partições balanceadas:
SELECT /*+ SKEW('f', 'id_cliente') */ 
    f.id_transacao, 
    c.nome_cliente, 
    f.valor
FROM prod_lakehouse.silver.fatos_transacoes AS f
JOIN prod_lakehouse.silver.dim_cliente AS c
  ON f.id_cliente = c.id_cliente;</code></pre>

        <h2>6. ⚠️ Pegadinhas Críticas do Exame DP-750 (PySpark & SQL)</h2>
        <blockquote>
          <ul>
            <li><strong>UDFs Python Tradicionais:</strong> UDFs definidas com <code>@udf</code> em Python forçam a serialização linha a linha entre a JVM e o processo Python, desabilitando o Catalyst Optimizer e o Photon Engine. Sempre prefira funções nativas de <code>pyspark.sql.functions</code> ou UDFs vetorizadas com Pandas (PyArrow).</li>
            <li><strong>Uso perigoso de df.collect():</strong> O comando <code>.collect()</code> envia TODOS os dados dos executors para a memória do Driver. Em produção com grandes volumes, causa erro fatal de <code>OutOfMemoryError (Driver OOM)</code>.</li>
          </ul>
        </blockquote>
        """
    },
    {
        "id": "05",
        "slug": "05-delta-lake-liquid-clustering-and-tuning-guide",
        "title": "Folha 05: Guia de Otimização Física: Liquid Clustering & Tuning de Performance",
        "desc": "Liquid Clustering (CLUSTER BY) vs Particionamento Hive, Deletion Vectors, OPTIMIZE, VACUUM e Diagnóstico na Spark UI.",
        "content": """
        <h2>1. Liquid Clustering (CLUSTER BY) vs Particionamento Tradicional Hive</h2>
        <p>O <strong>Liquid Clustering</strong> é a inovação mais importante de layout físico do Delta Lake no exame DP-750, substituindo o particionamento rígido Hive e o Z-Order tradicional:</p>
        <table>
          <thead>
            <tr>
              <th>Característica</th>
              <th>Particionamento Tradicional Hive (PARTITIONED BY)</th>
              <th>Liquid Clustering (CLUSTER BY) — Padrão DP-750</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Flexibilidade de Colunas</strong></td>
              <td>Rígido: alterar as colunas de partição exige recriar e reescrever a tabela</td>
              <td>Dinâmico: você pode alterar as chaves de clusterização com <code>ALTER TABLE</code> a qualquer momento</td>
            </tr>
            <tr>
              <td><strong>Problema de Small Files</strong></td>
              <td>Severo: colunas com alta cardinalidade geram milhões de pequenos arquivos</td>
              <td>Inexistente: o algoritmo agrupa dados mantendo arquivos de tamanho ideal (~1 GB)</td>
            </tr>
            <tr>
              <td><strong>Custo de Manutenção</strong></td>
              <td>O comando <code>ZORDER</code> exige reordenações globais caras e lentas</td>
              <td>O comando <code>OPTIMIZE</code> opera de forma incremental, clusterizando apenas novos dados</td>
            </tr>
            <tr>
              <td><strong>Concorrência de Escrita</strong></td>
              <td>Conflitos frequentes em commits simultâneos na mesma partição</td>
              <td>Excelente concorrência, especialmente combinado com <strong>Deletion Vectors</strong></td>
            </tr>
          </tbody>
        </table>

        <h2>2. Sintaxe Oficial de Liquid Clustering no SQL</h2>
        <pre><code>-- Criação de tabela com Liquid Clustering por múltiplas colunas:
CREATE TABLE prod_lakehouse.gold.vendas_analiticas (
    id_pedido BIGINT,
    data_pedido DATE,
    id_cliente INT,
    codigo_pais STRING,
    valor_total DECIMAL(10,2)
)
CLUSTER BY (codigo_pais, data_pedido, id_cliente);

-- Alterando as colunas de clusterização sem reescrever a tabela:
ALTER TABLE prod_lakehouse.gold.vendas_analiticas
CLUSTER BY (codigo_pais, data_pedido);

-- Executando a otimização incremental:
OPTIMIZE prod_lakehouse.gold.vendas_analiticas;</code></pre>

        <h2>3. Deletion Vectors (Mutações Ultrarrápidas no Delta Lake)</h2>
        <p>No Delta Lake tradicional, quando uma única linha era excluída ou atualizada em um arquivo Parquet de 100 MB, o Spark precisava reescrever o arquivo inteiro de 100 MB (Copy-on-Write). Com <strong>Deletion Vectors</strong>:</p>
        <ul>
          <li>O Delta grava um arquivo leve de bitmap (vetor de bits) indicando apenas os números das linhas deletadas/atualizadas.</li>
          <li>As consultas de leitura aplicam o bitmap em memória, ignorando as linhas removidas instantaneamente.</li>
          <li>Reduz o tempo de <code>MERGE INTO</code>, <code>DELETE</code> e <code>UPDATE</code> em até 10x!</li>
          <li>Habilitação: <code>ALTER TABLE tbl SET TBLPROPERTIES ('delta.enableDeletionVectors' = true);</code></li>
        </ul>

        <h2>4. Comandos de Manutenção Física: OPTIMIZE e VACUUM</h2>
        <pre><code>-- 1. OPTIMIZE: Bin-packing de pequenos arquivos para consolidar em arquivos de ~1 GB
OPTIMIZE prod_lakehouse.silver.fatos_transacoes;

-- 2. VACUUM: Limpeza de arquivos Parquet órfãos desassociados do log após transações
-- Remove apenas arquivos com mais de 7 dias (período de retenção padrão seguro)
VACUUM prod_lakehouse.silver.fatos_transacoes;

-- 3. VACUUM com retenção personalizada (ex: 3 dias / 72 horas para auditoria):
VACUUM prod_lakehouse.silver.fatos_transacoes RETAIN 72 HOURS;</code></pre>

        <h2>5. Diagnóstico de Gargalos na Spark UI</h2>
        <table>
          <thead>
            <tr>
              <th>Sintoma na Spark UI</th>
              <th>Causa Raiz Técnica</th>
              <th>Ação Corretiva Recomendada</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Spill (Memory / Disk)</strong></td>
              <td>Partições de Shuffle excedem a memória RAM alocada para os slots dos executors</td>
              <td>Aumentar <code>spark.sql.shuffle.partitions</code> ou migrar para nós de VM otimizados para memória</td>
            </tr>
            <tr>
              <td><strong>Data Skew (Stragglers)</strong></td>
              <td>Poucas tasks demoram minutos enquanto 199 tasks concluem em 2 segundos</td>
              <td>Usar Skew Join Hint <code>/*+ SKEW */</code> ou técnica de Salting na chave do Join</td>
            </tr>
            <tr>
              <td><strong>Garbage Collection Pauses</strong></td>
              <td>Alta taxa de alocação de objetos temporários na JVM do Java</td>
              <td>Habilitar o <strong>Photon Engine</strong> para execução nativa C++ fora da JVM</td>
            </tr>
          </tbody>
        </table>

        <h2>6. ⚠️ Pegadinhas Críticas do Exame DP-750 (Delta Lake & Otimização)</h2>
        <blockquote>
          <ul>
            <li><strong>O Perigo do VACUUM RETAIN 0 HOURS:</strong> Executar <code>VACUUM tbl RETAIN 0 HOURS;</code> falhará por padrão devido à trava de segurança <code>spark.databricks.delta.retentionDurationCheck.enabled</code>. Se forçada, essa ação <strong>DESTRÓI imediatamente a capacidade de Time Travel</strong> e corromperá leituras concorrentes em andamento!</li>
            <li><strong>Quando usar Liquid Clustering?</strong> Tabelas com padrões de consulta imprevisíveis, tabelas com cardinalidade variável ou tabelas atualizadas frequentemente com MERGE. O DP-750 prioriza Liquid Clustering em relação ao particionamento Hive.</li>
          </ul>
        </blockquote>
        """
    },
    {
        "id": "06",
        "slug": "06-workflows-dabs-cicd-and-system-tables-cheatsheet",
        "title": "Folha 06: Cheatsheet de Workflows, DABs (databricks.yml) & System Tables",
        "desc": "Databricks Workflows, Task Values, Repair Runs, Databricks Asset Bundles (DABs), CI/CD com Entra ID e System Tables.",
        "content": """
        <h2>1. Databricks Workflows: Multi-Task DAGs & Task Values</h2>
        <p>O Databricks Workflows é o orquestrador nativo totalmente gerenciado do Lakehouse para pipelines multitarefas:</p>
        <ul>
          <li><strong>Tipos de Tarefas Heterogêneas:</strong> Pode combinar em um único DAG tarefas de Notebook, scripts Python, consultas SQL/Alerts, pipelines Delta Live Tables (DLT) e dbt.</li>
          <li><strong>Task Values (Passagem de Parâmetros entre Tarefas):</strong></li>
        </ul>
        <pre><code># Tarefa 1 (Upstream): Define uma variável de saída compartilhada
total_registros_processados = 452000
dbutils.jobs.taskValues.set(key="total_rows", value=total_registros_processados)

# Tarefa 2 (Downstream): Lê a variável gerada pela Tarefa 1
linhas_anteriores = dbutils.jobs.taskValues.get(taskKey="tarefa_ingestao_bronze", key="total_rows")
print(f"Processando {linhas_anteriores} linhas na camada Silver...")</code></pre>

        <h2>2. Repair Run no Databricks Workflows (Eficiência Operacional)</h2>
        <p>Se um job multitarefa de 10 etapas falhar na etapa 7 devido a uma instabilidade passageira de rede:</p>
        <ul>
          <li><strong>O que NÃO fazer:</strong> Reiniciar o job inteiro do zero (recalculando as etapas 1 a 6 e gastando DBUs desnecessárias).</li>
          <li><strong>Padrão Ouro DP-750:</strong> Executar um <strong>Repair Run</strong>. O Databricks reexecuta <strong>exclusivamente a tarefa que falhou</strong> (etapa 7) e suas dependências downstream, preservando os resultados das etapas concluídas com sucesso.</li>
        </ul>

        <h2>3. Databricks Asset Bundles (DABs) & Estrutura do databricks.yml</h2>
        <p>DABs é a ferramenta oficial de Infraestrutura como Código (IaC) e automação de CI/CD para projetos Databricks:</p>
        <pre><code>bundle:
  name: dp750_lakehouse_prod

targets:
  dev:
    mode: development
    default: true
    workspace:
      host: https://adb-dev.azuredatabricks.net
  prod:
    mode: production
    workspace:
      host: https://adb-prod.azuredatabricks.net

resources:
  jobs:
    etl_pipeline_diario:
      name: "[PROD] Pipeline Medallion Diário"
      schedule:
        quartz_cron_expression: "0 0 3 * * ?"
        timezone_id: "America/Sao_Paulo"
      job_clusters:
        - job_cluster_key: job_cluster_finops
          new_cluster:
            spark_version: 15.4.x-photon-scala2.12
            node_type_id: Standard_D4ds_v5
            autoscale:
              min_workers: 1
              max_workers: 4
      tasks:
        - task_key: ingestao_bronze
          job_cluster_key: job_cluster_finops
          notebook_task:
            notebook_path: ../src/01_ingestao_bronze.py
        - task_key: transformacao_silver
          depends_on:
            - task_key: ingestao_bronze
          job_cluster_key: job_cluster_finops
          notebook_task:
            notebook_path: ../src/02_transformacao_silver.py</code></pre>

        <h2>4. Comandos CLI Essenciais de Databricks Asset Bundles</h2>
        <pre><code># 1. Validar a sintaxe dos arquivos YAML e caminhos do bundle:
databricks bundle validate

# 2. Fazer o deploy dos recursos no ambiente de desenvolvimento:
databricks bundle deploy -t dev

# 3. Fazer o deploy em produção e disparar a execução imediata:
databricks bundle deploy -t prod
databricks bundle run -t prod etl_pipeline_diario

# 4. Destruir os recursos criados pelo bundle no target:
databricks bundle destroy -t dev</code></pre>

        <h2>5. Consultas Analíticas em System Tables (FinOps & Auditoria)</h2>
        <pre><code>-- 1. Relatório FinOps: Consumo de DBUs agrupado por Job e SKU nos últimos 30 dias:
SELECT 
    usage_date,
    sku_name,
    usage_metadata.job_id,
    SUM(usage_quantity) AS total_dbus_consumidos
FROM system.billing.usage
WHERE usage_date >= current_date() - INTERVAL 30 DAYS
GROUP BY 1, 2, 3
ORDER BY total_dbus_consumidos DESC;

-- 2. Auditoria de Segurança: Rastreamento de acessos e modificações de privilégios:
SELECT 
    event_time,
    user_identity.email,
    action_name,
    request_params.catalog_name,
    request_params.schema_name,
    request_params.securable_type
FROM system.access.audit
WHERE service_name = 'unityCatalog'
  AND action_name IN ('grantPermissions', 'revokePermissions')
ORDER BY event_time DESC
LIMIT 50;</code></pre>

        <h2>6. ⚠️ Pegadinhas Críticas do Exame DP-750 (Workflows & CI/CD)</h2>
        <blockquote>
          <ul>
            <li><strong>Autenticação em CI/CD:</strong> NUNCA use tokens de acesso pessoal (PATs) de desenvolvedores individuais em pipelines de CI/CD (Azure DevOps / GitHub Actions). O exame exige <strong>Microsoft Entra ID Service Principals com autenticação federada OIDC</strong>.</li>
            <li><strong>Falha Parcial em Workflows:</strong> Ao identificar falhas em pipelines de produção, lembre-se da opção <strong>Repair Run</strong> para evitar reprocessamento dispendioso.</li>
          </ul>
        </blockquote>
        """
    }
]

def build_ref_html(ref):
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{ref["title"]} | Databricks Formation DP-750</title>
  <meta name="description" content="{ref["desc"]}">
  <link rel="stylesheet" href="../assets/tufte.css">
  <link rel="stylesheet" href="../assets/vark.css">
  <script src="../assets/lens.js"></script>
</head>
<body data-active-lens="all">

  <!-- Top Navigation Bar -->
  <header class="top-navbar">
    <a href="../index.html" class="brand-logo">
      <span class="brand-badge">DP-750</span>
      <span>Databricks Formation</span>
    </a>
    <ul class="nav-links">
      <li><a href="../index.html">Portal</a></li>
      <li><a href="../index.html#referencias" class="active">Folhas de Referência</a></li>
      <li><a href="../simulados/index.html">Simulados Pearson VUE</a></li>
      <li><button type="button" class="theme-toggle-btn" onclick="window.toggleAppTheme()">🌙 Modo Dark</button></li>
    </ul>
  </header>

  <!-- Quick Index Superior (#quick-index) -->
  <nav id="quick-index">
    <div class="quick-index-container">
      <span class="quick-index-label">Folhas Rápidas:</span>
      <a href="01-spark-and-databricks-architecture-visual-guide.html" class="index-chip {'active' if ref['id'] == '01' else ''}">01 Arquitetura</a>
      <a href="02-unity-catalog-security-and-governance-guide.html" class="index-chip {'active' if ref['id'] == '02' else ''}">02 Unity Catalog</a>
      <a href="03-ingestion-autoloader-and-dlt-decision-matrix.html" class="index-chip {'active' if ref['id'] == '03' else ''}">03 Ingestão &amp; DLT</a>
      <a href="04-pyspark-and-spark-sql-engineering-cheatsheet.html" class="index-chip {'active' if ref['id'] == '04' else ''}">04 PySpark &amp; SQL</a>
      <a href="05-delta-lake-liquid-clustering-and-tuning-guide.html" class="index-chip {'active' if ref['id'] == '05' else ''}">05 Liquid &amp; Tuning</a>
      <a href="06-workflows-dabs-cicd-and-system-tables-cheatsheet.html" class="index-chip {'active' if ref['id'] == '06' else ''}">06 DABs &amp; System</a>
    </div>
  </nav>

  <article>
    <div style="margin-bottom: 2rem;">
      <span style="font-size: 0.85rem; font-weight: 700; color: #0078D4; text-transform: uppercase; letter-spacing: 0.05em;">Folha de Referência Rápida DP-750</span>
      <h1>{ref["title"]}</h1>
      <p class="subtitle">{ref["desc"]}</p>
    </div>

    <div class="fullwidth">
      {ref["content"]}
    </div>

    <footer style="margin-top: 4rem; padding-top: 1.5rem; border-top: 1px solid #E1E8ED; display: flex; justify-content: space-between; align-items: center; font-family: var(--font-sans);">
      <div><a href="../index.html#referencias">← Voltar ao Portal</a></div>
      <div><a href="../simulados/index.html" style="font-weight: 700; color: #FF3621;">Praticar no Simulado Oficial (+180Q) →</a></div>
    </footer>
  </article>

  <script src="../assets/lens.js"></script>
</body>
</html>
'''

def main():
    os.makedirs("reference", exist_ok=True)
    for ref in REFERENCES:
        path = os.path.join("reference", f"{ref['slug']}.html")
        content = build_ref_html(ref)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        print(f"Folha atualizada com sucesso: {path}")

if __name__ == "__main__":
    main()
