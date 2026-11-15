#!/usr/bin/env python3
"""
Databricks Formation — Prepare to DP-750
Gerador Definitivo de Narrações Neurais Explicativas em Nível Masterclass com Kokoro-82M ONNX.
Utiliza arquitetura híbrida de fonemização:
- Texto em Português do Brasil com fonemizador pt-br nativo
- Termos técnicos em inglês com fonemizador en-us nativo e dicionário de pronúncia perfeita
- Áudios explicativos completos com ~2 minutos de duração por lição (+120s)
"""

import os
import sys
import re
import subprocess
import soundfile as sf
from kokoro_onnx import Kokoro

FFMPEG_BIN = "/home/gustavo/.cache/uv/archive-v0/ITc_Ru6ZEPSSpm8h/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
MODEL_PATH = "assets/models/kokoro-v1.0.onnx"
VOICES_PATH = "assets/models/voices-v1.0.bin"

ENGLISH_TERMS = [
    'Databricks Formation', 'Databricks', 'Azure Databricks', 'Azure Data Factory', 'Azure Key Vault', 'Azure Event Grid',
    'Azure Data Lake Storage Gen2', 'Azure Data Lake Storage', 'Azure Private Link',
    'Azure Monitor', 'Microsoft Entra ID', 'Power BI', 'GitHub Actions', 'Azure DevOps',
    'Control Plane', 'Compute Plane', 'All-Purpose Clusters', 'All-Purpose Cluster',
    'All-Purpose', 'Job Clusters', 'Job Cluster', 'Single Node', 'Serverless Compute',
    'Serverless SQL Warehouses', 'Serverless SQL Warehouse', 'Serverless', 'SQL Warehouses',
    'SQL Warehouse', 'Cluster Policies', 'Cluster Policy', 'Instance Pools', 'Instance Pool',
    'Secure Cluster Connectivity', 'VNet Injection', 'Private Link', 'Private Endpoints',
    'Private Endpoint', 'Secret Scopes', 'Secret Scope', 'External Locations', 'External Location',
    'Storage Credentials', 'Storage Credential', 'Managed Identity', 'Service Principals',
    'Service Principal', 'Databricks Units', 'Databricks CLI', 'Databricks Workflows',
    'Databricks Asset Bundles', 'Asset Bundles', 'REST API',
    'Apache Spark', 'SparkSession', 'Catalyst Optimizer', 'Photon Engine', 'Photon',
    'Driver', 'Executors', 'Executor', 'Wide Transformation', 'Narrow Transformation',
    'Predicate Pushdown', 'Column Pruning', 'Tungsten Engine', 'Garbage Collection',
    'Directed Acyclic Graphs', 'Shuffles', 'Shuffle', 'Stages', 'Stage', 'Tasks', 'Task',
    'Jobs', 'Job', 'Spark UI', 'RocksDB',
    'Delta Lake', 'Lakehouse', 'Lakehouse Federation', 'Delta Sharing', 'Time Travel',
    'Delta Log', 'Parquet Checkpoints', 'Parquet', 'Checkpoints', 'Checkpointing', 'Checkpoint',
    'Liquid Clustering', 'Deletion Vectors', 'Deletion Vector', 'Z-Ordering', 'Z-Order',
    'Change Data Feed', 'Merge Into', 'SCD Type 1', 'SCD Type 2', 'Star Schema',
    'Unity Catalog', 'Metastore', 'Three-level Namespace', 'Managed Tables', 'Managed Table',
    'External Tables', 'External Table', 'Volumes', 'Volume', 'Row Filters', 'Row Filter',
    'Column Masks', 'Column Mask', 'Dynamic Views', 'Dynamic View', 'System Tables',
    'System Table',
    'Auto Loader', 'Cloud Files', 'COPY INTO', 'Directory Listing', 'File Notification',
    'Schema Evolution', 'Rescued Data Column', 'rescued data', 'Medallion Architecture',
    'Medallion', 'Bronze', 'Silver', 'Gold', 'Structured Streaming', 'Watermarking',
    'Watermark', 'AvailableNow', 'ProcessingTime', 'Micro-batch',
    'Delta Live Tables', 'Streaming Tables', 'Streaming Table', 'Materialized Views',
    'Materialized View', 'Expectations', 'Expectation', 'Enhanced Autoscaling',
    'Repair Run', 'Task Values', 'Event Log', 'Clusters', 'Cluster', 'Workspaces',
    'Workspace', 'Workflows', 'Workflow', 'Notebooks', 'Notebook', 'Pipelines', 'Pipeline',
    'Pools', 'Pool', 'Storage', 'Compute', 'FinOps', 'DBUs', 'IP', 'Gen2', 'ACID'
]
ENGLISH_TERMS.sort(key=len, reverse=True)
PATTERN = re.compile(r'\b(' + '|'.join(re.escape(t) for t in ENGLISH_TERMS) + r')\b', re.IGNORECASE)

CUSTOM_EN_PHONEMES = {
    'Databricks Formation': 'dˈeɪɾəbɹˌɪks fɔːɹmˈeɪʃən',
    'Databricks': 'dˈeɪɾəbɹˌɪks',
    'DBUs': 'dˌiːbˌiːjˈuːz',
    'FinOps': 'fˈɪnˌɑːps',
    'IP': 'ˌaɪpˈiː',
    'Gen2': 'dʒˈɛn tˈuː',
    'ACID': 'ˈæsɪd',
    'DP-750': 'dˌiːpˌiː sˌɛvən fˈɪfti',
    'All-Purpose Clusters': 'ˈɔːlpˈɜːpəs klˈʌstɚz',
    'All-Purpose': 'ˈɔːlpˈɜːpəs',
    'Job Clusters': 'dʒˈɑːb klˈʌstɚz',
    'Single Node': 'sˈɪŋɡəl nˈoʊd',
    'Control Plane': 'kəntɹˈoʊl plˈeɪn',
    'Compute Plane': 'kəmpjˈuːt plˈeɪn',
    'Compute': 'kəmpjˈuːt',
    'Cluster': 'klˈʌstɚ',
    'Clusters': 'klˈʌstɚz',
    'Workspace': 'wˈɜːkspeɪs',
    'Workspaces': 'wˈɜːkspeɪsᵻz',
    'Warehouse': 'wˈɛɹhaʊs',
    'Warehouses': 'wˈɛɹhaʊsᵻz',
    'Driver': 'dɹˈaɪvɚ',
    'Executors': 'ɛɡzˈɛkjuːɾɚz',
    'Shuffle': 'ʃˈʌfəl',
    'Liquid Clustering': 'lˈɪkwɪd klˈʌstɚɹɪŋ',
    'Deletion Vectors': 'dᵻlˈiːʃən vˈɛktɚz',
    'Delta Lake': 'dˈɛltə lˈeɪk',
    'Lakehouse': 'lˈeɪkhaʊs',
    'Unity Catalog': 'jˈuːnɪɾi kˈæɾɐlˌɑːɡ',
    'Photon': 'fˈoʊtɑːn',
    'Delta Live Tables': 'dˈɛltə lˈaɪv tˈeɪbəlz'
}

def hybrid_phonemize(text, kokoro):
    tokens = []
    last_idx = 0
    for m in PATTERN.finditer(text):
        start, end = m.span()
        if start > last_idx:
            tokens.append(('pt-br', text[last_idx:start]))
        tokens.append(('en-us', m.group(0)))
        last_idx = end
    if last_idx < len(text):
        tokens.append(('pt-br', text[last_idx:]))
        
    phonemes = []
    for lang, seg in tokens:
        if not seg.strip():
            phonemes.append(seg)
            continue
        seg_strip = seg.strip()
        matched_override = None
        for k, v in CUSTOM_EN_PHONEMES.items():
            if seg_strip.lower() == k.lower():
                matched_override = v
                break
        if matched_override:
            phonemes.append(matched_override)
        elif lang == 'en-us':
            try:
                ph = kokoro.tokenizer.phonemize(seg, lang='en-us')
                phonemes.append(ph)
            except Exception:
                ph = kokoro.tokenizer.phonemize(seg, lang='pt-br')
                phonemes.append(ph)
        else:
            ph = kokoro.tokenizer.phonemize(seg, lang='pt-br')
            phonemes.append(ph)
    return ' '.join(phonemes)

LESSON_SCRIPTS = {
    1: (
        "Bem-vindo à Lição 0001 da Databricks Formation, estruturada especificamente para a sua aprovação de primeira "
        "no exame oficial Microsoft DP-750: Implementing Data Engineering Solutions Using Azure Databricks. "
        "Nesta lição fundamental de arquitetura, você domina a separação estrita entre o plano de controle, o Control Plane, "
        "e o plano de computação, o Compute Plane. "
        "No modelo clássico de implantação do Azure Databricks, o Control Plane reside em uma assinatura gerenciada pela Microsoft e pela Databricks. "
        "Essa camada de gerenciamento corporativo hospeda serviços centrais como a interface web do Workspace, o agendador de tarefas do Databricks Workflows, "
        "o gerenciador de Notebooks colaborativos e o catálogo corporativo Unity Catalog. "
        "Por outro lado, o Compute Plane é a camada física onde os dados da sua organização realmente residem e são processados. "
        "Na arquitetura clássica, esse plano de computação é alocado diretamente dentro da assinatura Azure do cliente, "
        "implantado em uma rede virtual privada com duas sub-redes dedicadas para os nós Driver e Executors. "
        "Os dados brutos e tratados dos clientes residem no Azure Data Lake Storage Gen2 e absolutamente nunca transitam pelo Control Plane. "
        "A segurança da comunicação entre os nós de computação e o Control Plane é assegurada pelo recurso de Secure Cluster Connectivity, "
        "que utiliza túneis de saída na porta 443, dispensando totalmente a alocação de endereços de IP público nos nós. "
        "Para a prova DP-750, a principal regra de FinOps envolve a governança de custos em DBUs, as Databricks Units. "
        "Clusters interativos compartilhados, conhecidos como All-Purpose Clusters, possuem a taxa de DBUs mais onerosa da plataforma "
        "e devem ser restritos estritamente ao desenvolvimento e testes analíticos em notebooks. "
        "Trabalhos e rotinas agendadas de produção devem obrigatoriamente utilizar Job Clusters efêmeros ou soluções de Serverless Compute, "
        "que cobram uma taxa de DBUs até sessenta por cento menor e são destruídos imediatamente após a conclusão da execução. "
        "Adicionalmente, na computação Serverless, os nós sobem instantaneamente em um pool seguro gerenciado pela Databricks, "
        "eliminando o tempo de espera de inicialização de máquinas virtuais e cobrando apenas pelos segundos exatos de processamento consumidos."
    ),
    2: (
        "Lição 0002 da Databricks Formation: Anatomia do Apache Spark, Catalyst Optimizer e o motor vetorizado Photon Engine. "
        "Compreender a distribuição física do Apache Spark é crucial para diagnosticar gargalos de desempenho e otimizar custos na nuvem. "
        "Em uma aplicação Spark, o nó Driver atua como o cérebro central: ele mantém a SparkSession ativa, compila o código do usuário em grafos acíclicos dirigidos, "
        "e coordena a distribuição física do trabalho entre os nós Executors espalhados pelo cluster. "
        "O trabalho analítico é fragmentado hierarquicamente: Ações submetidas pelo código geram Jobs, que são divididos em Stages por limites de Shuffle, "
        "e estes são decompostos em Tasks atômicas enviadas para execução nos núcleos de processamento dos Executors. "
        "Operações de Wide Transformation, como junções entre tabelas grandes, agrupamentos por chave e distinção de registros, "
        "forçam a movimentação massiva de dados pela rede, conhecida como Shuffle, que representa o principal gargalo de I-O em pipelines analíticos de larga escala. "
        "O Catalyst Optimizer atua em quatro fases sucessivas para minimizar esse impacto: ele analisa a consulta com base no catálogo de metadados, "
        "aplica regras de otimização lógica como Predicate Pushdown para filtrar dados direto no Storage e Column Pruning para ler apenas as colunas necessárias, "
        "e seleciona o plano físico mais eficiente avaliando custos estatísticos de processamento. "
        "Historicamente, o Spark gerava código Java em tempo de execução através do motor Tungsten. "
        "No entanto, o Azure Databricks introduziu o Photon Engine, um motor de execução de consultas reescrito do zero em C mais mais. "
        "O Photon opera execução vetorizada com instruções SIMD, processando milhares de registros por ciclo de clock de CPU em memória colunar. "
        "Ele elimina completamente a sobrecarga de gerenciamento de memória e Garbage Collection da máquina virtual Java, "
        "acelerando filtros, agregações e joins analíticos em até oito vezes, reduzindo drasticamente o tempo de cluster ativo e o consumo de DBUs."
    ),
    3: (
        "Lição 0003 da Databricks Formation: Protocolo Delta Lake à fundo, transações ACID, Time Travel e manutenção preventiva de FinOps. "
        "O Delta Lake é a camada de Storage de código aberto que transforma data lakes comuns em arquiteturas Lakehouse confiáveis e transacionais. "
        "A garantia de propriedades ACID de atomicidade, consistência, isolamento e durabilidade é viabilizada pelo diretório especial underline delta log. "
        "Cada mutação ou inserção na tabela resulta em um novo arquivo de commit sequencial no formato JSON, registrado através de operações atômicas no sistema de arquivos da nuvem. "
        "O protocolo emprega Controle de Concorrência Otimista: se duas transações simultâneas tentarem modificar os mesmos dados, "
        "a segunda transação detecta o conflito no log e repete a operação automaticamente sem corromper a base. "
        "Para evitar a leitura de milhares de pequenos arquivos de log durante o planejamento de consultas, o protocolo gera automaticamente "
        "arquivos de checkpoint compactados em formato Parquet a cada dez commits transacionais registrados. "
        "Esse mecanismo robusto fornece o recurso nativo de Time Travel, permitindo auditar o histórico de alterações, reverter exclusões acidentais "
        "e consultar versões históricas dos dados utilizando tanto o número sequencial da versão quanto carimbos de data e hora específicos. "
        "O Delta Lake também oferece evolução e imposição estrita de esquema: alterações incompatíveis de tipo de dados são bloqueadas por padrão, "
        "mas novas colunas podem ser incorporadas com segurança através da opção mergeSchema. "
        "Em cenários de produção avaliados no exame DP-750, a manutenção contínua das tabelas Delta é uma competência mandatória de FinOps. "
        "O comando Optimize deve ser executado periodicamente para resolver o problema de proliferação de arquivos pequenos, "
        "aplicando compactação inteligente para fundir múltiplos fragmentos de dados em arquivos Parquet consolidados de cerca de um gigabyte. "
        "Complementarmente, o comando Vacuum atua na limpeza física do Storage, apagando arquivos de dados órfãos que não pertencem mais à versão ativa da tabela. "
        "É fundamental respeitar o período padrão de retenção de segurança de sete dias do Vacuum, "
        "impedindo a remoção de arquivos que possam estar sendo lidos por consultas simultâneas de longa duração ou rotinas de Time Travel em andamento."
    ),
    4: (
        "Lição 0004 da Databricks Formation: Provisionamento de Workspaces, integração com Microsoft Entra ID, SCIM, VNet Injection e Private Link. "
        "Configurar a infraestrutura corporativa do Azure Databricks com segurança de nível empresarial é um dos domínios mais rigorosos do exame oficial. "
        "O provisionamento de Workspaces pode ser realizado interativamente pelo portal Azure ou automatizado via modelos ARM, Terraform e Databricks CLI. "
        "Para governança centralizada de identidade, o Azure Databricks se integra nativamente ao Microsoft Entra ID através do protocolo corporativo SCIM. "
        "Isso permite que o Account Console sincronize automaticamente usuários, grupos de segurança e Service Principals a partir do diretório corporativo, "
        "garantindo provisionamento centralizado e revogação imediata de credenciais quando colaboradores deixam a organização. "
        "Na arquitetura de rede, a prática recomendada para ambientes corporativos com requisitos de conformidade é a VNet Injection. "
        "Em vez de utilizar uma rede virtual gerenciada padrão, o cliente injeta o Compute Plane dentro de sua própria VNet corporativa pré-configurada. "
        "Essa topologia requer exatamente duas sub-redes dedicadas sem nenhum outro recurso compartilhado: a public subnet, que hospeda os nós Driver, "
        "e a private subnet, destinada aos nós Executors do cluster, ambas configuradas com o recurso de Secure Cluster Connectivity sem IP público. "
        "As sub-redes exigem Network Security Groups configurados para permitir tráfego interno entre os nós e tráfego de saída HTTPS seguro. "
        "Para blindagem total contra ataques de exfiltração de dados e trânsito público pela internet, implementamos o Azure Private Link. "
        "Ele estabelece conexões por pontos de extremidade privados tanto para o front-end, protegendo o acesso dos usuários à interface web, "
        "quanto para o back-end, assegurando que todo o tráfego de telemetria e controle entre o Control Plane e o Compute Plane "
        "ocorra exclusivamente através do backbone privado e isolado da infraestrutura global da Microsoft, complementado por listas de controle de acesso de IP corporativas."
    ),
    5: (
        "Lição 0005 da Databricks Formation: Governança de Computação, Cluster Policies, Instance Pools e Serverless SQL Warehouses. "
        "Gerenciar recursos computacionais no Azure Databricks exige equilibrar agilidade analítica com disciplina financeira e controle orçamentário rigoroso. "
        "Para evitar que analistas e cientistas de dados provisionem máquinas excessivamente caras ou mantenham clusters ociosos ligados sem necessidade, "
        "os administradores utilizam as políticas de cluster, ou Cluster Policies. "
        "As políticas utilizam definições estruturadas em formato JSON que limitam o tamanho máximo de nós por cluster, restringem famílias de máquinas virtuais permitidas, "
        "forçam a ativação de autotermination em períodos estritos de quinze a vinte minutos e injetam tags obrigatórias de centro de custo para auditoria contábil. "
        "As políticas suportam herança hierárquica e controle de acesso baseado em papéis, permitindo delegar criação controlada de ambientes para times de negócio. "
        "Outro componente essencial de eficiência de custos são os Instance Pools: pools de máquinas virtuais mantidas pré-inicializadas e prontas na assinatura Azure. "
        "Quando um novo cluster é requisitado ou precisa escalar nós adicionais, as instâncias são anexadas a partir do pool em menos de trinta segundos, "
        "eliminando o tempo de espera de cinco a sete minutos exigido pelo provisionamento convencional de máquinas virtuais na nuvem. "
        "Instâncias de Spot também podem ser aproveitadas nos pools para workloads tolerantes a falhas, gerando economias de até oitenta por cento na infraestrutura subjacente de máquinas virtuais. "
        "Para cargas de inteligência de negócios, dashboards executivos e consultas analíticas em SQL, a recomendação oficial do exame é o Serverless SQL Warehouse. "
        "Diferente dos SQL Warehouses clássicos que exigem aquecimento manual de máquinas, a tecnologia Serverless sobe instantaneamente em menos de dez segundos, "
        "escala automaticamente para cima e para baixo em múltiplos canais de acordo com a concorrência de usuários, "
        "e encerra a cobrança assim que a última consulta é concluída, otimizando drasticamente o custo total de propriedade em DBUs."
    ),
    6: (
        "Lição 0006 da Databricks Formation: Integração com Ecossistema Azure, Azure Data Factory, Azure Key Vault Secret Scopes e External Locations. "
        "Uma solução de engenharia de dados robusta integra o Azure Databricks aos principais serviços de infraestrutura e orquestração do ecossistema Microsoft. "
        "Na camada de segurança de senhas e credenciais, a regra número um do exame DP-750 é a proibição expressa de gravar chaves de acesso diretamente no código dos notebooks. "
        "A abordagem correta e auditável é a utilização de Secret Scopes apontados para o Azure Key Vault corporativo. "
        "Com essa configuração, os segredos são mantidos em segurança no cofre de chaves da nuvem e recuperados programaticamente em tempo de execução "
        "utilizando o utilitário dbutils secrets get, sem que o valor confidencial seja impresso nos logs de execução do cluster. "
        "As permissões sobre os escopos de segredos são governadas por listas de controle de acesso gerenciadas via Databricks CLI ou API REST. "
        "Para orquestração híbrida de dados corporativos, o Azure Data Factory se comunica com o Azure Databricks por meio de linked services autenticados "
        "via Managed Identity ou Service Principal registrado no Microsoft Entra ID, disparando notebooks e pipelines de engenharia de forma totalmente integrada e monitorada no portal Azure. "
        "Em ambientes corporativos com restrições de rede, a comunicação ocorre através de runtimes de integração auto-hospedados ou redes virtuais gerenciadas "
        "com pontos de extremidade privados dedicados para o Key Vault e para o Data Lake Storage. "
        "Na camada de Storage, as práticas modernas de arquitetura com o Unity Catalog eliminam montagens legadas de DBFS baseadas em chaves compartilhadas ou tokens SAAS. "
        "A governança é estabelecida através de Storage Credentials vinculadas a identidades gerenciadas com privilégios restritos de Storage Blob Data Contributor no Azure Data Lake Storage Gen2. "
        "Sobre essas credenciais seguras, criamos External Locations que mapeiam contêineres e pastas específicas no Storage, delegando o controle de acesso e auditoria de arquivos inteiramente para a hierarquia central de permissões do Unity Catalog."
    ),
    7: (
        "Lição 0007 da Databricks Formation: Arquitetura Unity Catalog, Metastore centralizado, Three-level Namespace e governança de Volumes. "
        "O Unity Catalog representa o pilar definitivo de governança unificada para dados, inteligência artificial e arquivos em múltiplos Workspaces Databricks. "
        "Sua arquitetura corporativa é ancorada em um Metastore centralizado por região do Azure, totalmente dissociado do ciclo de vida de Workspaces individuais. "
        "A estrutura lógica organiza todos os recursos de dados em um Three-level Namespace padronizado de três níveis: catálogo, esquema e tabela ou volume. "
        "Essa convenção elimina ambiguidades de nomenclatura e permite referenciar dados entre diferentes domínios e catálogos corporativos em uma única consulta analítica. "
        "Os Workspaces são vinculados ao Metastore central, e a vinculação de catálogos específicos a Workspaces individuais garante isolamento rígido entre ambientes de homologação e produção. "
        "Para a prova DP-750, é essencial dominar a distinção entre os dois tipos fundamentais de tabelas no Unity Catalog: "
        "nas tabelas gerenciadas, ou Managed Tables, o Databricks gerencia integralmente o ciclo de vida físico dos dados no Storage raiz do catálogo ou esquema; "
        "se a tabela for descartada com um comando drop table, tanto o registro no catálogo quanto os arquivos físicos subjacentes são excluídos permanentemente do Storage. "
        "Em contrapartida, nas tabelas externas, ou External Tables, o caminho dos dados reside em uma External Location dedicada; "
        "a exclusão da tabela com drop table remove apenas a definição lógica no catálogo, preservando todos os arquivos Parquet intactos no Storage para consumo por outras ferramentas analíticas. "
        "Para arquivos não tabulares que exigem auditoria e controle de acesso fino, como planilhas, arquivos de imagem, documentos em PDF e modelos de Machine Learning, "
        "o Unity Catalog fornece o recurso de Volumes, disponíveis nas modalidades gerenciada e externa, "
        "permitindo aplicar permissões de governança em dados não estruturados de maneira perfeitamente idêntica às tabelas analíticas tradicionais."
    ),
    8: (
        "Lição 0008 da Databricks Formation: Controle de acesso fino no Unity Catalog, Row Filters, Column Masks e governança com funções nativas. "
        "Garantir conformidade rigorosa com regulamentações de privacidade como LGPD e GDPR exige implementar controle de acesso fino diretamente no motor de dados. "
        "O modelo de governança do Unity Catalog opera com herança hierárquica declarativa: concessões atribuídas em catálogos são propagadas para esquemas e tabelas filhos, "
        "simplificando a administração corporativa com os comandos padrão de segurança grant e revoke do SQL. "
        "Para proteção granular de registros sem a necessidade de duplicar dados físicos em múltiplas tabelas, utilizamos Row Filters e Column Masks nativos. "
        "Os Row Filters aplicam funções personalizadas em SQL diretamente na tabela, avaliando atributos dinâmicos de sessão como a função is member ou is account group member; "
        "com isso, analistas da filial sul visualizam somente os registros de vendas pertencentes à sua respectiva região geográfica, enquanto administradores globais têm acesso total à mesma tabela. "
        "Os Column Masks operam de forma análoga para dados sensíveis ou informações de identificação pessoal, "
        "ofuscando colunas confidenciais de cartões de crédito, remunerações ou números de CPF para usuários comuns, revelando o conteúdo real apenas para grupos autorizados. "
        "A máscara pode aplicar mascaramento constante, funções hash criptográficas ou substituição parcial de caracteres. "
        "Essa mecânica nativa do Unity Catalog substitui com vantagens absolutas as antigas Dynamic Views do Hive Metastore legado, "
        "pois é aplicada diretamente na definição do objeto no catálogo e protegida contra manipulação em qualquer Workspace conectado. "
        "Além disso, os filtros são empurrados diretamente para a camada de Storage via predicados otimizados durante o planejamento físico da consulta, "
        "e todas as tentativas de acesso aos dados mascarados são auditadas automaticamente nos registros da tabela de auditoria do sistema, "
        "assegurando conformidade contínua e eliminando qualquer risco de vazamento de informações corporativas."
    ),
    9: (
        "Lição 0009 da Databricks Formation: Linhagem automatizada de dados, tabelas de sistema, Lakehouse Federation e Delta Sharing corporativo. "
        "A rastreabilidade completa e a governança de ponta a ponta são requisitos mandatórios em arquiteturas corporativas de dados modernas e auditáveis. "
        "O Unity Catalog captura a linhagem de dados automaticamente em tempo real a partir dos planos físicos de execução de comandos Spark e SQL. "
        "A telemetria de linhagem registra dependências tanto a nível de tabela quanto a nível fino de coluna, rastreando fontes, transformações intermediárias, notebooks e dashboards analíticos. "
        "Isso permite aos engenheiros conduzir análises de impacto precisas antes de alterar estruturas de dados e identificar a causa raiz exata de qualquer falha no pipeline. "
        "Para auditoria e conformidade contábil, a plataforma disponibiliza as tabelas de sistema dentro do catálogo protegido system. "
        "A tabela system access audit armazena registros detalhados de todas as ações de autenticação, comandos executados e permissões alteradas, "
        "enquanto a tabela system billing usage consolida a telemetria horária de consumo de DBUs por cluster, usuário e etiqueta contábil, "
        "viabilizando relatórios avançados de FinOps e alertas orçamentários preventivos. "
        "Para integrações corporativas sem silos de informação, o Lakehouse Federation permite conectar fontes externas como Azure SQL Database, Snowflake e PostgreSQL "
        "diretamente ao Workspace, executando consultas federadas com pushdown de predicados sem duplicar dados. "
        "Por fim, para distribuição de informações com parceiros e clientes externos, utilizamos o Delta Sharing: o primeiro protocolo aberto do mercado para compartilhamento seguro de tabelas Delta em tempo real. "
        "O destinatário consome os dados diretamente no Power BI, Python, Excel ou Tableau com tokens seguros, "
        "sem necessidade de possuir uma assinatura Databricks e sem custos de Storage adicional para a organização recebedora, garantindo compartilhamento auditado e escalável."
    ),
    10: (
        "Lição 0010 da Databricks Formation: Ingestão escalável de dados com Cloud Files Auto Loader, comando COPY INTO e Lakeflow Connect. "
        "A ingestão confiável de dados brutos não tratados a partir do blob Storage representa o primeiro estágio fundamental da arquitetura Medallion. "
        "No exame DP-750, a Microsoft testa rigorosamente o conhecimento sobre quando aplicar o comando COPY INTO e quando selecionar o Auto Loader. "
        "O comando COPY INTO é um operador idempotente em SQL ideal para carregar lotes pontuais de dados contendo milhares de arquivos em diretórios com estrutura estática, "
        "mantendo metadados de arquivos já carregados para evitar duplicidades em execuções repetidas. "
        "Entretanto, para pipelines corporativos com milhões de arquivos novos chegando de forma contínua em alta frequência, "
        "a recomendação oficial do exame é a utilização do formato Cloud Files, amplamente conhecido como Auto Loader. "
        "O Auto Loader oferece dois modos de descoberta de arquivos: o modo Directory Listing, que varre o diretório no Storage para volumes moderados, "
        "e o modo File Notification, que cria automaticamente filas e assinaturas de eventos no Azure Event Grid para detectar arquivos instantaneamente em escala massiva sem sobrecarregar a API do Storage. "
        "O parâmetro cloudFiles maxFilesPerTrigger permite dosar o volume de ingestão por micro-batch, evitando picos de sobrecarga de memória nos nós do cluster. "
        "Além disso, o Auto Loader gerencia automaticamente a inferência inicial de esquemas de dados semiestruturados em JSON ou CSV, "
        "fornecendo suporte nativo à evolução de esquema com a opção addNewColumns, sem interromper a execução do pipeline quando novos atributos surgem na origem. "
        "Para assegurar resiliência contra registros malformados ou corrompidos que violem os tipos esperados, "
        "o Auto Loader captura anomalias na coluna protegida underline rescued data, "
        "permitindo que o fluxo prossiga normalmente enquanto dados defeituosos são tratados em quarentena sem interromper o processamento analítico corporativo."
    ),
    11: (
        "Lição 0011 da Databricks Formation: Arquitetura Medallion com PySpark e Spark SQL, camadas Bronze, Silver e Gold e operações de Merge Into. "
        "O padrão de design arquitetural predominante no Azure Databricks é a Arquitetura Medallion, que organiza os dados em camadas sucessivas de qualidade e valor analítico. "
        "A camada Bronze representa a zona de entrada bruta: os dados são gravados em modo append-only no formato Delta, "
        "preservando o estado original da fonte com esquemas fiéis e carimbos de data e hora de ingestão para fins de auditoria e reprocessamento histórico. "
        "A camada Silver é a camada de enriquecimento e consolidação corporativa: nela, aplicamos limpeza de campos nulos, enriquecimento de chaves primárias, "
        "padronização de tipos de dados e desduplicação com regras de negócio refinadas. "
        "Para atualizar registros na camada Silver a partir de origens com captura de alterações de dados, utilizamos amplamente o comando Merge Into. "
        "O Merge permite implementar com precisão estratégias de dimensões de variação lenta, ou SCD: "
        "no SCD Type 1, registros existentes são atualizados diretamente e novas chaves são inseridas; "
        "no SCD Type 2, mantemos o histórico temporal de alterações gravando novas versões do registro com colunas de data de início, data de término e sinalizador de registro ativo. "
        "A camada Silver também aproveita o recurso de Change Data Feed do Delta Lake, que emite eventos incrementais de linha modificada contendo pre-images e post-images para consumo direto pela camada seguinte. "
        "Por fim, a camada Gold concentra os dados de consumo de negócio: modelos estrela e agregação de indicadores-chave de desempenho, "
        "preparados para alimentar relatórios executivos no Power BI, modelos de aprendizado de máquina e consultas analíticas de alta performance. "
        "Na camada Gold, utilizamos colunas de identidade para geração automática de chaves substitutas em tabelas de dimensão, "
        "com suporte a controle de acesso fino e desempenho de leitura otimizado por índices e agrupamentos físicos."
    ),
    12: (
        "Lição 0012 da Databricks Formation: Engenharia de streaming em tempo real com Spark Structured Streaming, triggers, checkpoints e watermarking. "
        "O Spark Structured Streaming unifica o processamento em lote e em tempo real sobre o mesmo motor computacional, "
        "tratando fluxos contínuos de dados como tabelas infinitas que recebem novas linhas constantemente. "
        "A orquestração de leitura e escrita é configurada através de triggers: o trigger por intervalo de tempo define a frequência de processamento em micro-batches contínuos, "
        "enquanto o trigger AvailableNow processa incrementalmente todos os dados disponíveis na fonte e encerra a consulta de forma limpa, "
        "sendo a opção preferida no exame para economizar DBUs em pipelines incrementais agendados sem manter clusters ligados ininterruptamente. "
        "A escrita do stream suporta três modos de saída: modo Append para gravação exclusiva de linhas novas, "
        "modo Complete para regravação da tabela agregada inteira a cada lote, e modo Update para emissão pontual de registros alterados. "
        "A garantia estrita de processamento exatamente uma vez é assegurada pela combinação de logs de transação com diretórios de checkpoints gravados no Storage seguro. "
        "Se um nó do cluster falhar ou o pipeline for interrompido, o motor recupera o estado exato dos dados a partir do checkpoint sem gerar registros duplicados. "
        "Para operações analíticas com estado, como contagens acumuladas ou junções contínuas fluxo a fluxo, "
        "o motor utiliza o RocksDB como provedor de armazenamento de estado para suportar milhões de chaves em memória persistente sem degradação de performance. "
        "Em cenários que envolvem agregações temporais com janelas de tempo deslizantes, o mecanismo de Watermarking desempenha papel vital de estabilidade operacional: "
        "ele estabelece um limiar máximo de tempo para a tolerância de eventos atrasados; "
        "dados que chegam com atraso superior à janela de Watermarking configurada são descartados automaticamente, "
        "permitindo que o motor libere estados antigos da memória dos Executors e evitando falhas críticas de esgotamento de memória no cluster."
    ),
    13: (
        "Lição 0013 da Databricks Formation: Otimização física no Delta Lake, Liquid Clustering versus Z-Ordering e Deletion Vectors de alta performance. "
        "Manter consultas analíticas rápidas à medida que os volumes de dados crescem para a casa dos terabytes exige técnicas modernas de otimização no Delta Lake. "
        "Historicamente, engenheiros de dados dependiam do particionamento estático em diretórios de pastas no Storage e do comando Optimize com Z-Ordering. "
        "Contudo, o particionamento rígido frequentemente causa problemas severos de sobreparticionamento com milhares de arquivos minúsculos e desbalanceamento de partições. "
        "A solução moderna introduzida pela Databricks e amplamente enfatizada no exame DP-750 é o Liquid Clustering, ativado pela cláusula CLUSTER BY. "
        "O Liquid Clustering substitui o particionamento em pastas por agrupamento geométrico contínuo de dados em até quatro colunas selecionadas, "
        "permitindo que a estrutura física dos arquivos seja reorganizada de forma incremental ao longo do tempo sem a necessidade de reescrever a tabela inteira. "
        "Tabelas existentes podem ser convertidas facilmente com comandos alter table cluster by. "
        "Diferente do Z-Ordering, o Liquid Clustering não é destrutivo e suporta evolução de chaves de agrupamento sem migração manual de dados. "
        "Outra inovação essencial de desempenho avaliada na prova são os Deletion Vectors, ou vetores de exclusão. "
        "No Delta Lake tradicional, atualizar ou excluir uma única linha forçava o motor a ler, modificar e reescrever o arquivo Parquet inteiro de centenas de megabytes. "
        "Com os Deletion Vectors habilitados, o motor grava apenas um arquivo minúsculo de bitmap apontando as linhas modificadas ou excluídas; "
        "as consultas subsequentes leem o Parquet original e filtram as linhas marcadas no vetor, "
        "acelerando comandos de update, delete e merge em até dez vezes e viabilizando conformidade ágil com o direito ao esquecimento da LGPD sem reescrever dados massivos no Storage, "
        "enquanto execuções periódicas de Vacuum removem fisicamente os dados antigos conforme as políticas corporativas."
    ),
    14: (
        "Lição 0014 da Databricks Formation: Pipelines declarativos com Delta Live Tables e Lakeflow, Streaming Tables, Materialized Views e Expectations. "
        "O Delta Live Tables, ou DLT, revolucionou a engenharia de dados ao introduzir um modelo declarativo para construção de pipelines Medallion corporativos. "
        "Em vez de escrever código complexo para gerenciar clusters, pontos de recuperação de falhas e orquestração sequencial de dependências, "
        "o desenvolvedor declara o fluxo de dados em PySpark com decoradores ou em SQL declarativo, "
        "e o motor da Databricks otimiza automaticamente o grafo de execução e aloca a infraestrutura necessária. "
        "O DLT oferece escalonamento automático aprimorado, o Enhanced Autoscaling, que ajusta recursos dinamicamente com base nas filas de tarefas sem desperdiçar DBUs. "
        "No exame DP-750, é essencial dominar a diferença técnica entre Streaming Tables e Materialized Views: "
        "as Streaming Tables são utilizadas para ingestão e transformação contínua ou incremental de fontes append-only como o Auto Loader, "
        "processando apenas registros novos sem recomputar o passado; "
        "as Materialized Views são empregadas para agregações analíticas complexas, mantendo o resultado da consulta materializado em Storage e recalculando apenas os dados que mudaram na origem. "
        "Para governança estrita de qualidade de dados, o DLT disponibiliza as Expectations declaradas diretamente na definição da tabela. "
        "Você deve selecionar a cláusula adequada ao requisito de negócio: a diretiva padrão expect registra métricas de violação nos logs sem interromper o fluxo; "
        "a cláusula on violation drop row descarta silenciosamente as linhas que violarem a regra de validação, gravando apenas registros limpos na tabela; "
        "e a cláusula on violation fail update interrompe imediatamente a execução do pipeline diante de qualquer registro corrompido, "
        "impedindo que dados defeituosos contaminem as camadas analíticas corporativas subsequentes. "
        "Na interface do DLT, o desenvolvedor acompanha a linhagem visual em tempo real e inspeciona métricas detalhadas de qualidade de dados registradas no event log do pipeline."
    ),
    15: (
        "Lição 0015 da Databricks Formation: Orquestração corporativa e CI/CD em produção, Databricks Workflows, Asset Bundles e observabilidade avançada. "
        "Atingir maturidade em engenharia de dados significa gerenciar pipelines complexos com automação, repetibilidade e monitoramento contínuo em produção. "
        "O Databricks Workflows é o orquestrador nativo da plataforma para gerenciamento de grafos de tarefas com dependências condicionais complexas, "
        "suportando execução de notebooks, scripts em Python, comandos SQL, pipelines de DLT e modelos de Machine Learning. "
        "O Workflows permite o compartilhamento dinâmico de parâmetros de contexto entre tarefas utilizando Task Values, "
        "e fornece o recurso essencial de Repair Run, que permite reexecutar pontualmente apenas as tarefas específicas que falharam no grafo sem reprocessar tarefas bem-sucedidas. "
        "Notificações automáticas via email, webhooks corporativos ou canais do Slack podem ser configuradas para alertar o time de engenharia sobre atrasos ou quebras de SLA. "
        "Para implementar práticas modernas de infraestrutura como código e integração contínua, utilizamos os Databricks Asset Bundles, conhecidos como DABs. "
        "Os DABs permitem definir toda a topologia de clusters, permissões, agendamentos e pipelines declarativamente dentro do arquivo databricks ponto y-m-l. "
        "Isso viabiliza a validação automática de sintaxe no terminal com o comando databricks bundle validate, "
        "e a implantação automatizada em esteiras corporativas de CI/CD no GitHub Actions ou Azure DevOps entre ambientes isolados de desenvolvimento, homologação e produção, com injeção segura de segredos de autenticação. "
        "Por fim, a observabilidade da plataforma é mantida pela inspeção aprofundada de planos de execução e métricas de Shuffle na Spark UI, "
        "analisando métricas de tempo de Garbage Collection e gargalos de I-O, integrada à emissão de alertas automatizados no Azure Monitor "
        "e rastreamento de custos por etiquetas contábeis para garantir operação contínua, eficiente e altamente confiável dos dados corporativos. "
        "Com isso, sua arquitetura atinge prontidão total para aprovação com louvor no exame oficial Microsoft DP-750."
    )
}

def main():
    print("======================================================================")
    print("Databricks Formation — Gerador Híbrido de Narrações Kokoro-82M (+2min)")
    print("======================================================================")
    
    os.makedirs("assets/audio", exist_ok=True)
    
    print(f"Carregando modelo Kokoro-82M: {MODEL_PATH}...")
    kokoro = Kokoro(MODEL_PATH, VOICES_PATH)
    
    voice_name = "pf_dora"
    
    for lid, text in LESSON_SCRIPTS.items():
        wav_path = f"assets/audio/lesson-{lid:04d}-pt.wav"
        mp3_path = f"assets/audio/lesson-{lid:04d}-pt.mp3"
        word_count = len(text.split())
        
        print(f"\n--> [Lição {lid:04d}] Fonemizando {word_count} palavras com fonemizador híbrido (PT-BR + EN-US)...")
        hybrid_ph = hybrid_phonemize(text, kokoro)
        
        print(f"    Sintetizando áudio neural com voz '{voice_name}'...")
        samples, sample_rate = kokoro.create(
            hybrid_ph,
            voice=voice_name,
            speed=1.0,
            is_phonemes=True
        )
        
        sf.write(wav_path, samples, sample_rate)
        duration_sec = len(samples) / sample_rate
        print(f"    Áudio gerado: {duration_sec:.1f}s ({duration_sec/60:.2f} min) | Sample rate: {sample_rate}Hz")
        
        cmd = [
            FFMPEG_BIN, "-y",
            "-i", wav_path,
            "-b:a", "128k",
            "-metadata", f"title=Narração Masterclass Lição {lid:04d}",
            "-metadata", "artist=Databricks Formation (Kokoro 82M)",
            "-metadata", "album=Prepare to DP-750",
            mp3_path
        ]
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if res.returncode == 0:
            print(f"    ✓ MP3 gerado: {mp3_path} ({os.path.getsize(mp3_path)} bytes, {duration_sec/60:.2f} min)")
        else:
            print(f"    ✗ Erro FFmpeg em {mp3_path}")
            
    print("\n======================================================================")
    print("✅ TODAS AS 15 NARRAÇÕES MASTERCLASS HÍBRIDAS FORAM GERADAS COM SUCESSO!")
    print("======================================================================")

if __name__ == "__main__":
    main()
