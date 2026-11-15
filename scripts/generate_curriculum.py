#!/usr/bin/env python3
"""
Databricks Formation — DP-750
Gerador Definitivo das 15 Lições no formato Microsoft Learn com:
- Multi-Lente (6 Níveis de Profundidade)
- 4 Canais VARK ([V], [A], [R], [K])
- Hands-on Lab Walkthrough Passo a Passo estilo Microsoft Learn
- Alerta visual obrigatório de pré-requisito da Azure
- Simuladores Interativos e Quizzes Embaralhados via Fisher-Yates
"""

import os
import sys

# Garante import do diretório local
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.labs_data import LABS_STEPS

LESSONS_DATA = [
    {
        "id": "0001",
        "slug": "0001-arquitetura-azure-databricks-compute-dbus",
        "title": "Lição 0001: Arquitetura Azure Databricks, Control Plane vs Compute Plane & FinOps de DBUs",
        "module": "Módulo 0: Fundamentos de Apache Spark, Delta Lake & Lakehouse",
        "module_id": "modulo-0",
        "next_slug": "0002-anatomia-apache-spark-catalyst-photon",
        "prev_slug": None,
        "summary": "Domine a divisão fundamental entre Control Plane e Compute Plane no Azure Databricks, entenda o modelo de cobrança por DBUs (Databricks Units) e as diferenças arquiteturais entre Classic Compute e Serverless Compute.",
        "lab_file": "lesson_0001_lab.py",
        "junior_text": "Imagine o Azure Databricks como um restaurante com cozinha aberta: o Control Plane é o garçom e o caixa que organizam os pedidos e agendam as entregas. Já o Compute Plane é a cozinha onde os cozinheiros (máquinas virtuais) realmente picam, cozinham e processam os alimentos (seus terabytes de dados). Você só paga pelo tempo que a cozinha fica acesa através dos DBUs!",
        "pleno_text": "No Azure Databricks clássico, o Control Plane reside na assinatura gerenciada pela Microsoft/Databricks, enquanto o Compute Plane é alocado na assinatura Azure do próprio cliente (Customer Subscription) dentro de uma VNet gerenciada ou injetada. O cliente paga o custo da infraestrutura de VM Azure diretamente à Microsoft e a taxa de software Databricks via DBUs (Databricks Units por hora/núcleo). Já na modalidade Serverless, os nós de computação sobem instantaneamente em um pool seguro gerenciado pela Databricks, reduzindo o tempo de startup de 4-6 minutos para menos de 10 segundos.",
        "senior_text": "Pegadinha clássica do exame DP-750: Quando escolher entre All-Purpose Compute e Job Compute? All-Purpose é destinado a desenvolvimento interativo em notebooks e cobra uma taxa de DBU significativamente maior (ex: ~$0.55/DBU). Workloads de produção agendados SEMPRE devem usar Job Clusters (ou Serverless Jobs), cuja taxa de DBU é até 60% menor (~$0.20-0.40/DBU). Outro ponto crítico: os dados brutos e resultados residem no ADLS Gen2 e NUNCA transitam pelo Control Plane, garantindo conformidade com LGPD/GDPR e isolamento de rede.",
        "staff_text": "Sob o capô, a comunicação entre o Control Plane e o Compute Plane ocorre via Secure Cluster Connectivity (No Public IP - NPIP). Os nós do cluster iniciam túneis TLS de saída (outbound) na porta 443 em direção ao Control Plane, dispensando a abertura de portas de entrada no firewall ou NSG do cliente. No Serverless Compute, o isolamento multi-inquilino é garantido via microVMs e namespaces Linux com criptografia de ponta a ponta e credenciais efêmeras do Entra ID trocadas a cada job execution.",
        "clevel_text": "FinOps Strategy: O TCO (Total Cost of Ownership) do Lakehouse é otimizado com auto-termination rigoroso (ex: 15-20 minutos para notebooks interativos), uso obrigatório de Single-Node clusters para tarefas leves de engenharia e substituição de All-Purpose Clusters por Jobs efêmeros. O Serverless Compute elimina o desperdício de clusters ociosos rodando em background, cobrando exatamente pelos segundos de computação consumidos.",
        "quiz": {
            "question": "Uma organização precisa executar um pipeline de engenharia de dados agendado todas as noites que processa 2 TB no Azure Databricks. A equipe de FinOps exige a menor taxa de consumo de DBUs possível sem comprometer o SLA. Qual estratégia de computação atende estritamente a este requisito?",
            "options": [
                {"text": "Criar um Databricks Workflow orquestrado usando um Job Cluster efêmero dimensionado com autoscaling.", "correct": True, "explanation": "Job Clusters efêmeros cobram a menor taxa de DBU por hora (custo de DBU de job é até 60% menor que All-Purpose) e são destruídos automaticamente após a conclusão da execução."},
                {"text": "Configurar um All-Purpose Cluster de alta disponibilidade compartilhado entre o time de dados e mantê-lo ativo 24/7.", "correct": False, "explanation": "All-Purpose clusters têm a taxa de DBU mais cara do Databricks e manter ligado 24/7 viola as diretrizes fundamentais de FinOps do exame DP-750."},
                {"text": "Executar o pipeline dentro de um Databricks Notebook conectado a um Single-Node cluster sem autotermination.", "correct": False, "explanation": "Além de usar a taxa mais cara de All-Purpose, a ausência de autotermination causará cobrança contínua e Single-Node não suporta 2 TB de processamento paralelo."},
                {"text": "Exportar os dados para o Control Plane do Databricks e executar o processamento diretamente na camada de gerenciamento.", "correct": False, "explanation": "O Control Plane não executa transformações de dados de clientes; ele hospeda apenas serviços de governança, agendamento e web UI."}
            ]
        }
    },
    {
        "id": "0002",
        "slug": "0002-anatomia-apache-spark-catalyst-photon",
        "title": "Lição 0002: Anatomia do Apache Spark, Catalyst Optimizer & Photon Vectorized Engine",
        "module": "Módulo 0: Fundamentos de Apache Spark, Delta Lake & Lakehouse",
        "module_id": "modulo-0",
        "next_slug": "0003-protocolo-delta-lake-acid-time-travel",
        "prev_slug": "0001-arquitetura-azure-databricks-compute-dbus",
        "summary": "Compreenda a distribuição física do Apache Spark (Driver, Executors, Jobs, Stages, Tasks), a dinâmica de Shuffle e a revolução da engine Photon C++ integrada ao Catalyst Optimizer.",
        "lab_file": "lesson_0002_lab.py",
        "junior_text": "O Driver do Spark é como o maestro de uma grande orquestra: ele não toca todos os instrumentos sozinho, mas divide a partitura completa em pequenas estrofes (Tasks) e distribui para os músicos (Executors). Cada executor toca sua parte em paralelo, e o resultado final é uma sinfonia executada em segundos!",
        "pleno_text": "Um programa Spark submete Ações (como .count(), .write(), .collect()) que disparam Jobs. Cada Job é fragmentado em Stages divididos por limites de Shuffle (operações de Wide Transformation como groupBy, join, distinct). Os Stages são quebrados em Tasks, que representam a unidade elementar de execução processando uma partição de dados em um Core/Slot de Executor. O Catalyst Optimizer atua compilando a query em 4 fases: Resolved Logical Plan, Analyzed Logical Plan, Optimized Logical Plan (com Predicate Pushdown e Column Pruning) e Physical Plan com geração de código Java bytecode (Tungsten).",
        "senior_text": "No exame DP-750, a chave para performance é evitar Shuffles desnecessários (troca massiva de dados pela rede entre executors). O Photon Engine é o motor de execução nativo da Databricks reescrito do zero em C++, que substitui o Tungsten. Ele opera execução vetorizada (SIMD) processando milhares de linhas por instrução de CPU em memória colunar, acelerando agregações, joins e scans em até 3x a 8x em relação ao Spark tradicional.",
        "staff_text": "O Photon trabalha diretamente no nível da instrução de máquina, eliminando a sobrecarga de Garbage Collection (GC) da JVM e otimizando o branch prediction da CPU. Quando o Catalyst gera o Physical Plan, ele substitui os operadores WholeStageCodegen convencionais por nós Photon (ex: PhotonFilter, PhotonHashAggregate, PhotonShuffleExchangeExec), garantindo fallback transparente para JVM caso uma função não suportada (como uma UDF Python não vetorizada) seja encontrada.",
        "clevel_text": "Embora clusters habilitados com Photon possuam um multiplicador ligeiramente maior na cobrança de DBUs, o ganho de velocidade (redução do tempo de pipeline pela metade ou um terço) resulta em um custo total final menor (menor tempo de VM Azure + menor tempo de cluster ativo).",
        "quiz": {
            "question": "Um engenheiro de dados observa lentidão extrema em uma consulta que realiza agregações massivas e scans em tabelas Delta no Azure Databricks. A equipe precisa acelerar a execução sem alterar o código PySpark existente. Qual modificação de infraestrutura é mais eficiente?",
            "options": [
                {"text": "Habilitar a aceleração Photon no cluster Databricks Runtime (DBR).", "correct": True, "explanation": "O Photon Engine substitui a camada de execução JVM por C++ vetorizado com instruções SIMD sem exigir nenhuma alteração no código PySpark/SQL, acelerando diretamente scans, agregações e joins."},
                {"text": "Aumentar o número de partições de shuffle para 10.000 via spark.sql.shuffle.partitions.", "correct": False, "explanation": "Aumentar excessivamente as partições criará um problema severo de small tasks e sobrecarga de agendamento no Driver."},
                {"text": "Converter o código PySpark para uma UDF Python tradicional linha a linha.", "correct": False, "explanation": "UDFs Python linha a linha forçam a serialização entre JVM/Python, degradam a performance e desabilitam as otimizações do Photon."},
                {"text": "Substituir o cluster distribuído por um cluster de nó único com mais memória RAM.", "correct": False, "explanation": "Um nó único elimina o paralelismo distribuído do Spark e não resolverá pipelines de dados corporativos de grande escala."}
            ]
        }
    },
    {
        "id": "0003",
        "slug": "0003-protocolo-delta-lake-acid-time-travel",
        "title": "Lição 0003: Protocolo Delta Lake, Log Transacional (_delta_log), ACID e Manutenção Física",
        "module": "Módulo 0: Fundamentos de Apache Spark, Delta Lake & Lakehouse",
        "module_id": "modulo-0",
        "next_slug": "0004-workspaces-entra-id-vnet-private-link",
        "prev_slug": "0002-anatomia-apache-spark-catalyst-photon",
        "summary": "Desvende a estrutura atômica do Delta Lake: como os arquivos JSON de commit garantem transações ACID, Time Travel por versão/timestamp e como operar OPTIMIZE e VACUUM com segurança.",
        "lab_file": "lesson_0003_lab.py",
        "junior_text": "Pense no Delta Lake como um caderno de contabilidade com folhas à prova de rasuras: toda vez que você adiciona ou remove dados, em vez de apagar os arquivos antigos, você anota uma nova página no início do livro (o _delta_log). Se alguém pedir para ver como estava o caderno na semana passada, basta folhear até aquela página histórica!",
        "pleno_text": "Uma Delta Table é fisicamente composta por arquivos de dados Parquet e um diretório oculto `_delta_log/`. Cada operação de escrita (append, update, delete, merge) gera um arquivo JSON de commit ordenado monotonicamente (ex: `00000000000000000000.json`). A cada 10 commits, o Delta gera automaticamente um arquivo de checkpoint em Parquet compactando o estado do log para evitar leituras de centenas de JSONs. O Time Travel é realizado via `SELECT * FROM tbl VERSION AS OF 5` ou `TIMESTAMP AS OF '2025-01-01'`. O comando `OPTIMIZE` compacta arquivos pequenos (bin-packing de 1 GB), e o `VACUUM` limpa arquivos marcados como removidos que ultrapassaram o período de retenção (padrão de 7 dias).",
        "senior_text": "Atenção máxima para o exame DP-750: O comando `VACUUM tbl RETAIN 0 HOURS` falhará por padrão por segurança (`spark.databricks.delta.vacuum.parallelDelete.enabled` e `spark.databricks.delta.retentionDurationCheck.enabled = false`). Executar VACUUM com retenção zero ou menor que a duração da transação mais longa corromperá queries concorrentes e DESTRUIRÁ a capacidade de Time Travel para as versões afetadas. Outro ponto vital: Schema Enforcement impede que schemas divergentes corrompam a tabela, a menos que seja explicitamente passado `.option('mergeSchema', 'true')` para Schema Evolution.",
        "staff_text": "Concorrência no Delta Lake é governada por Optimistic Concurrency Control (OCC). Em caso de dois commits simultâneos sobre o mesmo arquivo, o segundo commit verifica se os arquivos lidos no início da transação foram alterados pelo primeiro commit; se não houver conflito de partição ou arquivos (graças a Deletion Vectors ou particionamento independente), o commit é renomeado atomicamente no storage (ex: via PUT condicional no ADLS Gen2).",
        "clevel_text": "Governança e Compliance: O Delta Log oferece trilha de auditoria nativa e imutável para regulamentações (SOX, LGPD). Entretanto, manter retenções de VACUUM desnecessariamente longas em tabelas de alto volume inflaciona os custos de armazenamento no ADLS Gen2.",
        "quiz": {
            "question": "Um engenheiro de dados precisa liberar espaço em disco no ADLS Gen2 removendo arquivos Parquet históricos órfãos de uma tabela Delta atualizada a cada 15 minutos. A empresa exige que os analistas consigam realizar Time Travel dos últimos 3 dias. Qual comando atende perfeitamente ao requisito?",
            "options": [
                {"text": "VACUUM delta.`abfss://...` RETAIN 72 HOURS;", "correct": True, "explanation": "O comando VACUUM com retenção explícita de 72 horas (3 dias) remove apenas os arquivos de dados marcados como excluídos que estão além desse período, preservando a capacidade de Time Travel para os últimos 3 dias."},
                {"text": "OPTIMIZE delta.`abfss://...` ZORDER BY (data_registro);", "correct": False, "explanation": "OPTIMIZE compacta arquivos e reordena dados, mas não remove arquivos antigos do storage sem um comando VACUUM posterior."},
                {"text": "VACUUM delta.`abfss://...` RETAIN 0 HOURS;", "correct": False, "explanation": "VACUUM com zero horas destruirá a capacidade de Time Travel e falhará a menos que travas de segurança do Databricks sejam desativadas."},
                {"text": "DROP TABLE delta.`abfss://...`;", "correct": False, "explanation": "DROP TABLE removerá os metadados da tabela e se for tabela gerenciada apagará todos os dados, destruindo a tabela."}
            ]
        }
    },
    {
        "id": "0004",
        "slug": "0004-workspaces-entra-id-vnet-private-link",
        "title": "Lição 0004: Provisionamento de Workspaces, Microsoft Entra ID (SCIM) & Rede Segura (VNet / Private Link)",
        "module": "Módulo 1: Configurar o Ambiente Azure Databricks (15–20% do Exame)",
        "module_id": "modulo-1",
        "next_slug": "0005-clusters-policies-pools-serverless-sql",
        "prev_slug": "0003-protocolo-delta-lake-acid-time-travel",
        "summary": "Aprenda a arquitetar workspaces corporativos com VNet Injection (duas subnets /26), provisionamento automático de identidades via SCIM e Microsoft Entra ID, e isolamento total via Azure Private Link.",
        "lab_file": "lesson_0004_lab.py",
        "junior_text": "Configurar o workspace com segurança é como construir uma casa com condomínio fechado e guarita: em vez de construir a casa na beira da rodovia pública, você a constrói dentro de uma rede fechada (VNet Injection). Na portaria, um guarda com crachá eletrônico (Microsoft Entra ID) só deixa entrar quem tem autorização corporativa!",
        "pleno_text": "O provisionamento do Azure Databricks pode ocorrer no modo padrão (onde a Databricks cria uma VNet gerenciada dentro do Resource Group gerenciado) ou no modo VNet Injection (Customer-Managed VNet). A VNet Injection exige duas subnets delegadas exclusivas para `Microsoft.Databricks/workspaces`: a Public Subnet (host) e a Private Subnet (container), cada uma com máscara mínima de `/26` (64 IPs) para comportar a escala dos nós de computação. A sincronização de usuários, grupos e Service Principals do Microsoft Entra ID para o Unity Catalog é feita a nível de conta (Account Console) via conector SCIM.",
        "senior_text": "Cenário de Exame DP-750: Quando o tráfego de dados corporativos não pode navegar pela Internet pública sob nenhuma hipótese, deve-se implementar Azure Private Link. Existem dois tipos de conexões Private Link no Databricks: Front-end Private Link (conecta a rede local/usuário via ExpressRoute/VPN ao WebApp/Control Plane) e Back-end Private Link (conecta os nós do Compute Plane na VNet do cliente ao Control Plane e ao storage de infraestrutura). Service Principals configurados no Entra ID com OIDC são a melhor prática para automação de CI/CD sem expor senhas.",
        "staff_text": "Em arquiteturas com VNet Injection e Private Link, o Network Security Group (NSG) das subnets não pode bloquear a comunicação interna entre os nós do cluster na porta 443 e portas de shuffle (portas 43000-45000). O roteamento de saída para serviços Azure (ADLS Gen2, Azure Key Vault) deve ser configurado via Private Endpoints ou Service Endpoints nas subnets para evitar qualquer saída via NAT Gateway público.",
        "clevel_text": "Centralização de Governança: Com o Unity Catalog no nível de conta, não se criam mais usuários manualmente em cada workspace individual. O conector SCIM sincroniza os grupos do Entra ID corporativo diretamente no Account Console da Databricks, garantindo conformidade com processos de onboarding e offboarding imediato de colaboradores.",
        "quiz": {
            "question": "Um arquiteto de dados precisa configurar um novo workspace do Azure Databricks em conformidade com as políticas corporativas de segurança de rede da empresa, que proíbem o provisionamento de VNets automáticas pelo provedor e exigem controle total dos endereços IP. Quais são os requisitos mínimos de subnets para a VNet do cliente?",
            "options": [
                {"text": "A VNet deve conter duas subnets dedicadas delegadas para Microsoft.Databricks/workspaces, cada uma com máscara mínima de /26.", "correct": True, "explanation": "O Azure Databricks VNet Injection exige exatamente duas subnets (public/host e private/container) com delegação para Microsoft.Databricks/workspaces e tamanho mínimo /26 (recomendado /24 para clusters maiores)."},
                {"text": "Uma única subnet compartilhada com o Azure Synapse e ADF com máscara /28.", "correct": False, "explanation": "O Databricks não aceita uma única subnet nem compartilhamento com outros serviços gerenciados, e /28 não possui IPs suficientes."},
                {"text": "Três subnets públicas com endereços IP públicos atribuídos a cada máquina virtual do cluster.", "correct": False, "explanation": "A recomendação é Secure Cluster Connectivity (No Public IP) com duas subnets, sem necessidade de IPs públicos nos nós."},
                {"text": "Duas subnets com tamanho /29 sem necessidade de delegação de serviço no Azure.", "correct": False, "explanation": "Uma subnet /29 fornece apenas 8 endereços IP brutos (menos de 3 usáveis no Azure), insuficiente para o Databricks Runtime."}
            ]
        }
    },
    {
        "id": "0005",
        "slug": "0005-clusters-policies-pools-serverless-sql",
        "title": "Lição 0005: Governança de Computação: Cluster Policies, Pools & Serverless SQL Warehouses",
        "module": "Módulo 1: Configurar o Ambiente Azure Databricks (15–20% do Exame)",
        "module_id": "modulo-1",
        "next_slug": "0006-integracao-azure-keyvault-adls-external",
        "prev_slug": "0004-workspaces-entra-id-vnet-private-link",
        "summary": "Implemente governança estrita de custos e recursos através de Cluster Policies JSON, Databricks Pools para inicialização rápida e Serverless SQL Warehouses de alta concorrência.",
        "lab_file": "lesson_0005_lab.py",
        "junior_text": "Cluster Policies são como o controle parental da sua TV ou o limite do cartão corporativo: você define que ninguém pode ligar uma máquina super cara por engano e que se ninguém mexer no computador por 20 minutos, ele desliga sozinho para não gastar dinheiro à toa!",
        "pleno_text": "No Azure Databricks, administradores utilizam Cluster Policies (definidas em JSON) para padronizar configurações de hardware, impor tags de centros de custo (`custom_tags`), limitar o número máximo de nós de workers e fixar o `autotermination_minutes`. Databricks Pools mantêm um conjunto de instâncias de máquinas virtuais Azure pré-inicializadas e ociosas (idle), reduzindo o tempo de inicialização de novos clusters de minutos para segundos. Para workloads de BI e consultas analíticas SQL, os Serverless SQL Warehouses fornecem elasticidade instantânea, cache inteligente e desligamento automático em até 1 minuto.",
        "senior_text": "No exame DP-750: Cluster Policies são a ferramenta primária para resolver conflitos entre flexibilidade para desenvolvedores e controle orçamentário de FinOps. Por exemplo, pode-se atribuir permissão `CAN_USE` na política 'Personal Compute' para cientistas de dados, enquanto engenheiros de produção usam a política 'Shared Compute'. Em SQL Warehouses, o scaling policy 'Serverless' ajusta clusters adicionais automaticamente quando a fila de queries cresce, garantindo SLA sem intervenção manual.",
        "staff_text": "Internals de Cluster Policies: Utilizam operadores JSON como `fixed`, `allowlist`, `blocklist`, `regex`, `range` e `defaultValue`. Por exemplo, a regra `\"spark_version\": {\"type\": \"fixed\", \"value\": \"auto:latest-lts\"}` força o uso automático da versão Long-Term Support mais recente, prevenindo que equipes utilizem runtimes legados ou não homologados com vulnerabilidades de segurança.",
        "clevel_text": "Impacto no TCO: SQL Warehouses tradicionais exigiam espera de 5 minutos para autostart e tinham tempo mínimo de autostop de 10-15 minutos. Com Serverless SQL Warehouses, o startup leva 5 segundos e o autostop pode ser reduzido para 1 minuto, economizando até 70% do custo de computação ociosa em equipes de Analytics.",
        "quiz": {
            "question": "O gestor de FinOps de uma multinacional identificou que desenvolvedores juniores estão criando clusters com tipos de máquinas GPU de custo elevado e esquecendo-os ligados nos fins de semana. Como o Engenheiro de Dados líder deve solucionar esse problema de forma definitiva e automatizada?",
            "options": [
                {"text": "Criar uma Cluster Policy definindo valores permitidos para node_type_id e um teto rígido em autotermination_minutes, aplicando a permissão CAN_USE ao grupo de desenvolvedores.", "correct": True, "explanation": "Cluster Policies permitem restringir tipos de instâncias VM (node_type_id) via allowlist e impor autotermination_minutes obrigatório, garantindo governança automática."},
                {"text": "Revogar o acesso de todos os desenvolvedores ao Azure Databricks e exigir que submetam tickets no portal Azure.", "correct": False, "explanation": "Solução inviável operacionalmente que paralisa o desenvolvimento e não utiliza os recursos nativos de governança do Databricks."},
                {"text": "Configurar um alerta no Azure Monitor para enviar e-mails diários ao gestor sempre que um cluster GPU for criado.", "correct": False, "explanation": "Alertas por e-mail são reativos e não impedem a criação indevida do recurso nem o desperdício de orçamento."},
                {"text": "Instalar um script Python em cada notebook que roda o comando exit() após 10 minutos.", "correct": False, "explanation": "Scripts dentro de notebooks não impedem a criação do cluster nem garantem autotermination a nível de infraestrutura."}
            ]
        }
    },
    {
        "id": "0006",
        "slug": "0006-integracao-azure-keyvault-adls-external",
        "title": "Lição 0006: Integração com Ecossistema Azure: Azure Key Vault Secret Scopes & ADLS Gen2",
        "module": "Módulo 1: Configurar o Ambiente Azure Databricks (15–20% do Exame)",
        "module_id": "modulo-1",
        "next_slug": "0007-unity-catalog-metastore-namespace-volumes",
        "prev_slug": "0005-clusters-policies-pools-serverless-sql",
        "summary": "Conecte com segurança seu lakehouse ao ecossistema Azure: Secret Scopes protegidos pelo Azure Key Vault, Managed Identities e External Locations com Storage Credentials do Unity Catalog.",
        "lab_file": "lesson_0006_lab.py",
        "junior_text": "Guardar senhas ou chaves de banco de dados escritas no meio do código de um notebook é como deixar a chave da sua casa colada com fita adesiva na porta da frente! O Azure Key Vault é o cofre ultra-seguro do banco, e o Databricks só busca a chave na hora de abrir a porta e a descarta em seguida.",
        "pleno_text": "Para evitar vazamento de credenciais em notebooks ou repositórios Git, cria-se um Secret Scope backed por Azure Key Vault através da URL especial `https://<databricks-instance>#secrets/createScope`. No código PySpark/Python, o segredo é lido dinamicamente com `dbutils.secrets.get(scope='meu-scope', key='minha-chave')`, e o Databricks mascara automaticamente o valor retornado na saída do notebook como `[REDACTED]`. Para conexão com o ADLS Gen2 no Unity Catalog, a arquitetura moderna abandona montagens legadas (`dbutils.fs.mount`) e utiliza Storage Credentials associadas a Azure Managed Identity com permissão Storage Blob Data Contributor.",
        "senior_text": "Pegadinha crítica do DP-750: O uso de montagens `dbutils.fs.mount()` e chaves de acesso (Access Keys) em arquivos de configuração é considerado padrão LEGADO e inseguro. O exame exige Unity Catalog Storage Credentials e External Locations (`CREATE EXTERNAL LOCATION ... URL 'abfss://...' WITH (STORAGE CREDENTIAL ...)`). Dessa forma, o acesso aos arquivos não depende do usuário que rodou o cluster, mas sim do RBAC granular gerenciado centralmente no Metastore.",
        "staff_text": "Ao integrar com Azure Data Factory (ADF), utiliza-se o Databricks Linked Service autenticado via Managed Identity ou Service Principal associado a um Secret no Key Vault. Quando o ADF dispara uma Databricks Notebook Activity, ele pode injetar parâmetros dinâmicos via `baseParameters`, consumidos no notebook via Databricks Widgets (`dbutils.widgets.get('param_name')`).",
        "clevel_text": "Segurança e Conformidade: A integração direta com o Azure Key Vault e Managed Identity garante que tokens nunca sejam compartilhados entre membros do time, viabilizando rotação de segredos em tempo real sem interrupção de pipelines produtivos.",
        "quiz": {
            "question": "Um engenheiro de dados precisa configurar um pipeline no Azure Databricks para ler dados confidenciais de um banco SQL externo. A política corporativa proíbe terminantemente a inclusão de credenciais em texto plano nos notebooks e exige rotação centralizada das chaves no Azure. Qual arquitetura atende a essa exigência?",
            "options": [
                {"text": "Criar um Secret Scope backed por Azure Key Vault e recuperar a senha no notebook usando dbutils.secrets.get().", "correct": True, "explanation": "Azure Key Vault-backed secret scopes garantem que os segredos residam e sejam rotacionados centralmente no Key Vault, sendo recuperados em runtime pelo Databricks e mascarados na interface como [REDACTED]."},
                {"text": "Gravar a senha em um arquivo de texto no DBFS (/FileStore/passwords.txt) e ler com spark.read.text().", "correct": False, "explanation": "Gravar senhas no DBFS expõe as credenciais a qualquer usuário com acesso ao workspace e viola os princípios fundamentais de segurança."},
                {"text": "Declarar a senha como variável de ambiente global pública dentro da Cluster Policy.", "correct": False, "explanation": "Variáveis de ambiente públicas em cluster policies podem ser inspecionadas por desenvolvedores e não permitem rotação segura."},
                {"text": "Passar a senha como comentário de cabeçalho na primeira célula do notebook.", "correct": False, "explanation": "Comentários em notebooks são versionados no Git e totalmente visíveis em texto claro."}
            ]
        }
    },
    {
        "id": "0007",
        "slug": "0007-unity-catalog-metastore-namespace-volumes",
        "title": "Lição 0007: Arquitetura Unity Catalog: Metastore, 3-Level Namespace & Volumes",
        "module": "Módulo 2: Segurança e Governança com Unity Catalog (15–20% do Exame)",
        "module_id": "modulo-2",
        "next_slug": "0008-controle-acesso-fino-row-column-masks",
        "prev_slug": "0006-integracao-azure-keyvault-adls-external",
        "summary": "Aprenda a espinha dorsal do Lakehouse moderno: o Metastore do Unity Catalog, a convenção universal catalog.schema.table, a distinção entre Managed e External Tables e o gerenciamento de arquivos com Volumes.",
        "lab_file": "lesson_0007_lab.py",
        "junior_text": "O Unity Catalog é como a biblioteca central da universidade: antigamente cada sala de aula tinha seus próprios livros espalhados (workspaces isolados). Com o Unity Catalog, existe um catálogo universal com 3 gavetas organizadas: o Armário (Catalog), a Prateleira (Schema) e o Livro (Table). Assim, qualquer estudante autorizado encontra exatamente o que procura!",
        "pleno_text": "O Unity Catalog introduz o modelo de Namespace de 3 Níveis: `catalog.schema.table` (ou `catalog.schema.volume`). Um Metastore é criado por região e vinculado a múltiplos workspaces. Managed Tables têm seus dados armazenados na raiz designada para o schema/catalog no ADLS Gen2; ao executar `DROP TABLE`, os metadados E os arquivos físicos são excluídos. External Tables apontam para um caminho customizado em uma External Location; ao executar `DROP TABLE`, apenas os metadados são apagados, preservando os arquivos no storage. Volumes gerenciam arquivos não-estruturados (como `.csv`, `.json`, `.parquet`, modelos de ML e PDFs) oferecendo governança e paths acessíveis via `/Volumes/catalog/schema/volume_name/arquivo.ext`.",
        "senior_text": "Foco total para o exame DP-750: Não confunda DBFS com Volumes! DBFS raiz é legado e inseguro. Volumes do Unity Catalog suportam permissões RBAC (`READ VOLUME`, `WRITE VOLUME`), auditoria e são o padrão ouro para ler arquivos brutos em landing zones e para machine learning. Tabelas criadas no catálogo legado `hive_metastore` NÃO suportam os recursos avançados de governança, linhagem automática e fine-grained access control do Unity Catalog.",
        "staff_text": "Managed Volumes vs External Volumes: Managed Volumes armazenam arquivos no storage padrão configurado no schema ou catalog pai. External Volumes exigem um caminho explícito dentro de uma External Location registrada. Ambos permitem acesso POSIX-like e operações streaming via `spark.readStream.format('cloudFiles').load('/Volumes/...')`.",
        "clevel_text": "Governança Corporativa: O Unity Catalog elimina a proliferação de silos entre múltiplos workspaces (desenvolvimento, homologação e produção). Um único ponto de controle gerencia acesso e conformidade em toda a organização com trilhas completas de auditoria.",
        "quiz": {
            "question": "Um engenheiro de dados precisa criar uma tabela no Unity Catalog para uma base de parceiros externos onde os arquivos Parquet residem em um container ADLS Gen2 gerenciado pela equipe de infraestrutura. Se a tabela for descartada no futuro (DROP TABLE), os arquivos de dados brutos NÃO podem ser excluídos. Como a tabela deve ser criada?",
            "options": [
                {"text": "Criar uma External Table utilizando a sintaxe CREATE TABLE catalog.schema.table LOCATION 'abfss://...';", "correct": True, "explanation": "External Tables no Unity Catalog preservam os arquivos de dados subjacentes no storage storage quando descartadas com DROP TABLE, removendo apenas a definição de metadados do metastore."},
                {"text": "Criar uma Managed Table usando CREATE TABLE catalog.schema.table AS SELECT * FROM ...;", "correct": False, "explanation": "Managed Tables excluem tanto os metadados quanto todos os arquivos físicos no ADLS Gen2 quando o comando DROP TABLE é executado."},
                {"text": "Criar a tabela no catálogo legado hive_metastore usando o formato Parquet tradicional.", "correct": False, "explanation": "O hive_metastore não é a arquitetura recomendada do Unity Catalog e viola as diretrizes modernas de governança."},
                {"text": "Criar um Managed Volume e montar o diretório no DBFS raiz.", "correct": False, "explanation": "Montagens no DBFS são obsoletas e volumes não são usados para substituir tabelas relacionais governadas."}
            ]
        }
    },
    {
        "id": "0008",
        "slug": "0008-controle-acesso-fino-row-column-masks",
        "title": "Lição 0008: Controle de Acesso Fino: Privilégios Hierárquicos, Row Filters & Column Masks",
        "module": "Módulo 2: Segurança e Governança com Unity Catalog (15–20% do Exame)",
        "module_id": "modulo-2",
        "next_slug": "0009-linhagem-system-tables-delta-sharing",
        "prev_slug": "0007-unity-catalog-metastore-namespace-volumes",
        "summary": "Implemente segurança de nível militar: privilégios hierárquicos (GRANT/REVOKE), mascaramento dinâmico de PII com Column Masks e restrição territorial de linhas com Row Filters SQL.",
        "lab_file": "lesson_0008_lab.py",
        "junior_text": "Imagine um hospital: o médico pode ver o prontuário completo do paciente (Row Filter da ala dele e sem máscara). A recepcionista na entrada pode ver que o paciente chegou, mas o número do cartão de crédito e diagnóstico aparecem com asteriscos (Column Masking). A mesma tabela atende a todos com segurança máxima!",
        "pleno_text": "O Unity Catalog opera um modelo de herança de privilégios estrito: para consultar uma tabela, o usuário precisa de `USE CATALOG` no catálogo pai, `USE SCHEMA` no schema pai e `SELECT` na tabela. Row Filters e Column Masks são definidos através de SQL User-Defined Functions (UDFs). Um Row Filter retorna um valor booleano (`true`/`false`) avaliando a função de contexto `is_account_group_member('grupo')` ou `current_user()`. Uma Column Mask recebe o valor original da coluna e retorna uma versão mascarada caso o usuário não pertença ao grupo privilegiado.",
        "senior_text": "Tema quente no DP-750: Como associar uma máscara a uma tabela existente? Utiliza-se `ALTER TABLE tbl ALTER COLUMN cpf SET MASK mask_cpf_func;` ou durante a criação com `CREATE TABLE`. Para Row Filters: `ALTER TABLE tbl SET ROW FILTER filter_region_func ON (region);`. A grande vantagem sobre as antigas Dynamic Views é que Row Filters e Column Masks funcionam de forma transparente: analistas consultam diretamente a tabela base `catalog.schema.table` sem necessidade de criar e manter centenas de views intermediárias.",
        "staff_text": "Performance e Otimização do Catalyst com Row Filters: O otimizador de consultas do Spark incorpora as regras do Row Filter diretamente no Logical Plan durante a fase de Analysis. Se o usuário só tem permissão para a região 'BR', o Catalyst aplica Predicate Pushdown imediato no scan dos arquivos Delta/Parquet, descartando arquivos de outras regiões no nível de metadados sem sobrecarga de I/O.",
        "clevel_text": "Compliance LGPD/GDPR: A capacidade de mascarar CPF, salários e dados médicos a nível de storage com herança automática simplifica auditorias e garante que desenvolvedores em homologação nunca visualizem dados pessoais de clientes.",
        "quiz": {
            "question": "Um banco precisa compartilhar a tabela 'gold.clientes' com a equipe de marketing. A equipe de segurança exige que analistas de marketing vejam apenas clientes do Brasil (coluna pais = 'BR') e que o número do cartão de crédito (coluna cartao) tenha apenas os 4 últimos dígitos visíveis, enquanto diretores de compliance vejam tudo. Qual é a implementação correta no Unity Catalog?",
            "options": [
                {"text": "Criar uma SQL UDF para Row Filter validando o grupo e país, criar uma SQL UDF de Column Mask para o cartão e associá-las à tabela com ALTER TABLE.", "correct": True, "explanation": "No Unity Catalog moderno, Row Filters e Column Masks nativos com funções SQL baseadas em is_account_group_member() são associados diretamente à tabela, dispensando views duplicadas."},
                {"text": "Criar duas cópias físicas da tabela no ADLS Gen2 e rodar pipelines de replicação diários.", "correct": False, "explanation": "Duplicar dados físicos gera custo duplicado, problemas de integridade e risco severo de vazamento de segurança."},
                {"text": "Instalar uma biblioteca Python de criptografia nos nós do cluster para interceptar as chamadas do Spark.", "correct": False, "explanation": "Customizações nos nós do cluster são frágeis, não integradas à governança e degradam drasticamente o desempenho."},
                {"text": "Conceder privilégio ALL PRIVILEGES e pedir que os analistas apliquem WHERE pais = 'BR' manualmente nas consultas.", "correct": False, "explanation": "Confiar em filtros manuais em consultas de analistas não cumpre nenhuma norma de segurança ou compliance."}
            ]
        }
    },
    {
        "id": "0009",
        "slug": "0009-linhagem-system-tables-delta-sharing",
        "title": "Lição 0009: Linhagem Automatizada, Auditoria com System Tables & Delta Sharing",
        "module": "Módulo 2: Segurança e Governança com Unity Catalog (15–20% do Exame)",
        "module_id": "modulo-2",
        "next_slug": "0010-ingestao-autoloader-copyinto-lakeflow",
        "prev_slug": "0008-controle-acesso-fino-row-column-masks",
        "summary": "Explore a observabilidade profunda do Unity Catalog: rastreamento de linhagem ponta a ponta (coluna e tabela), consultas SQL analíticas em System Tables e compartilhamento seguro via Delta Sharing.",
        "lab_file": "lesson_0009_lab.py",
        "junior_text": "A linhagem de dados é como a árvore genealógica de uma família: você consegue olhar para um gráfico de faturamento e saber exatamente de quais tabelas brutas e arquivos de texto ele se originou, quem mexeu nele e a que horas!",
        "pleno_text": "O Unity Catalog captura linhagem em tempo de execução sem custo adicional de instrumentação, cobrindo tabelas, colunas, notebooks, dashboards e pipelines DLT. As System Tables residem no catálogo especial `system` e incluem `system.access.audit` (logs de auditoria de quem leu ou modificou qualquer tabela), `system.billing.usage` (consumo de DBUs por cluster, SKU e tags de faturamento) e `system.lineage.table_lineage`. Para compartilhamento com terceiros, o Delta Sharing implementa um protocolo aberto REST que permite consultar dados em tempo real a partir do Power BI, Excel, Pandas ou Databricks externo sem cópia de arquivos.",
        "senior_text": "Questão garantida no DP-750: Como monitorar os custos de DBUs de um departamento específico no Azure Databricks? Criam-se tags de cluster obrigatórias via Cluster Policy (ex: `CostCenter = 'Finance'`), que são propagadas automaticamente para a tabela `system.billing.usage`. Uma simples consulta SQL agregando `usage_quantity` filtrando por `custom_tags['CostCenter']` gera relatórios precisos de chargeback. No Delta Sharing, os dados compartilham snapshots protegidos por tokens temporários do ADLS Gen2 com zero egress para destinatários na mesma região.",
        "staff_text": "Lakehouse Federation: O Unity Catalog permite criar Foreign Catalogs conectados a fontes externas (ex: Azure SQL Database, Snowflake, Google BigQuery). As queries SQL rodam com pushdown de predicados na fonte remota, permitindo joins federados entre um Delta Lake local no ADLS Gen2 e uma tabela de CRM legado no SQL Server com governança unificada.",
        "clevel_text": "Monetização de Dados e Auditoria: Delta Sharing transforma o Lakehouse em um hub de troca de dados segura entre parceiros comerciais sem vendor lock-in, enquanto as System Tables garantem conformidade total com auditorias contábeis e de segurança.",
        "quiz": {
            "question": "Um auditor de segurança corporativa exige uma lista completa de todos os usuários que consultaram a tabela sensível 'gold.folha_pagamento' nos últimos 30 dias, incluindo o IP de origem e os comandos SQL executados. Onde o engenheiro de dados deve extrair essas informações?",
            "options": [
                {"text": "Executando uma consulta SQL analítica diretamente na tabela system.access.audit do catálogo system.", "correct": True, "explanation": "A tabela system.access.audit armazena eventos de auditoria centralizados do Unity Catalog com registro de todas as consultas, identidades de usuários, IPs e timestamps."},
                {"text": "Inspecionando os arquivos de log de driver em cada nó de computação via SSH.", "correct": False, "explanation": "Logs de nós de computação não registram auditoria centralizada do Unity Catalog e nós efêmeros têm seus discos apagados."},
                {"text": "Lendo o arquivo _delta_log da tabela no ADLS Gen2.", "correct": False, "explanation": "O _delta_log registra apenas transações de escrita e modificação de metadados ACID, não consultas SELECT de leitura."},
                {"text": "Configurando manualmente triggers Python em cada notebook de cada usuário.", "correct": False, "explanation": "Triggers manuais em notebooks são contornáveis e não capturam acessos via SQL Warehouses, Power BI ou APIs."}
            ]
        }
    },
    {
        "id": "0010",
        "slug": "0010-ingestao-autoloader-copyinto-lakeflow",
        "title": "Lição 0010: Ingestão Escalável: Auto Loader (Cloud Files), COPY INTO & Lakeflow Connect",
        "module": "Módulo 3: Preparar e Processar Dados em Batch e Streaming (30–35% do Exame)",
        "module_id": "modulo-3",
        "next_slug": "0011-medallion-pyspark-sparksql-scd1-scd2",
        "prev_slug": "0009-linhagem-system-tables-delta-sharing",
        "summary": "Domine as técnicas modernas de ingestão de arquivos no Azure Databricks: Auto Loader com inferência de schema e coluna _rescued_data, o comando SQL COPY INTO e as matrizes de decisão para o exame.",
        "lab_file": "lesson_0010_lab.py",
        "junior_text": "O Auto Loader é como a esteira de bagagens inteligente do aeroporto: conforme novos aviões pousam e descarregam malas (arquivos no ADLS Gen2), a esteira detecta sozinha as novas malas e as entrega imediatamente, sem precisar reexaminar as malas que já foram entregues ontem!",
        "pleno_text": "O Auto Loader (formato `cloudFiles` no Apache Spark) ingere de forma incremental e eficiente milhões de novos arquivos que chegam ao armazenamento em nuvem (ADLS Gen2). Ele suporta dois modos de descoberta de arquivos: Directory Listing (ideal para caminhos ordenados e fluxos moderados) e File Notification (configura automaticamente Azure Event Grid e Storage Queues para detectar milhões de arquivos sem varrer diretórios). Suporta inferência de schema, evolução automática com `cloudFiles.schemaEvolutionMode` ('addNewColumns', 'rescue', 'failOnNewColumns') e a coluna especial `_rescued_data`, que preserva dados em formatos incompatíveis ou colunas não previstas em formato JSON.",
        "senior_text": "Matriz de Decisão do Exame DP-750: Quando usar Auto Loader vs COPY INTO? COPY INTO é um comando SQL idempotente ideal para lotes batch simples de arquivos (milhares a poucas centenas de milhares de arquivos com schema estável). Quando o volume atinge milhões de arquivos, a estrutura de diretórios é profunda, o schema evolui frequentemente ou a ingestão exige processamento contínuo em streaming com latência de segundos, o AUTO LOADER É A RESPOSTA CORRETA.",
        "staff_text": "Internals do Auto Loader: O checkpointing gerencia um RocksDB de estado local no executor do Spark armazenando o histórico de arquivos já processados, garantindo semântica exactly-once. A coluna `_rescued_data` evita que pipelines quebrem quando uma string aparece em uma coluna que deveria ser integer: o valor inválido vai para `_rescued_data` e a coluna original recebe null, permitindo auditoria posterior sem interromper o fluxo de ingestão.",
        "clevel_text": "Redução de Custos de Storage: O modo File Notification do Auto Loader elimina milhões de chamadas REST de LIST API no Azure Storage, reduzindo a fatura de transações de armazenamento e evitando limites de throttling do ADLS Gen2.",
        "quiz": {
            "question": "Um provedor de telecomunicações recebe continuamente milhões de arquivos JSON de telemetria por dia no ADLS Gen2 em diretórios aninhados. O schema desses arquivos muda esporadicamente com novos atributos de dispositivos, e o pipeline não pode falhar caso dados corrompidos apareçam. Qual tecnologia deve ser implementada na camada Bronze?",
            "options": [
                {"text": "Spark Structured Streaming com Auto Loader (cloudFiles), habilitando schemaEvolutionMode='addNewColumns' e coluna _rescued_data.", "correct": True, "explanation": "O Auto Loader é a solução recomendada pelo DP-750 para ingestão escalável contínua de milhões de arquivos com detecção de novos campos e captura de dados fora de padrão em _rescued_data."},
                {"text": "Um comando COPY INTO agendado a cada 1 minuto executando sobrescrita completa de tabela.", "correct": False, "explanation": "COPY INTO não escala eficientemente para milhões de arquivos contínuos em tempo real e sobrescrita apagará o histórico."},
                {"text": "Um script Python que lista os arquivos usando dbutils.fs.ls() e faz loops de leitura com spark.read.json().", "correct": False, "explanation": "Listar diretórios com dbutils.fs.ls() para milhões de arquivos sofre severo gargalo no Driver e causa timeouts na API de storage."},
                {"text": "Importar os arquivos manualmente através da interface web do Databricks Workspace.", "correct": False, "explanation": "Upload manual na UI é inviável para fluxos corporativos automatizados e possui limites severos de tamanho de arquivo."}
            ]
        }
    },
    {
        "id": "0011",
        "slug": "0011-medallion-pyspark-sparksql-scd1-scd2",
        "title": "Lição 0011: Arquitetura Medallion: PySpark, Spark SQL & MERGE INTO (SCD1 e SCD2)",
        "module": "Módulo 3: Preparar e Processar Dados em Batch e Streaming (30–35% do Exame)",
        "module_id": "modulo-3",
        "next_slug": "0012-structured-streaming-watermark-joins",
        "prev_slug": "0010-ingestao-autoloader-copyinto-lakeflow",
        "summary": "Construa pipelines com a Arquitetura Medallion (Bronze, Silver, Gold), manipule dados complexos com PySpark/Spark SQL e implemente Slowly Changing Dimensions (SCD Tipo 1 e 2) com MERGE INTO.",
        "lab_file": "lesson_0011_lab.py",
        "junior_text": "A Arquitetura Medallion é como o tratamento de água da sua cidade: a água bruta do rio entra com galhos e terra (Camada Bronze). Passa pela estação de tratamento onde é filtrada e clorada (Camada Silver, limpa e padronizada). Por fim, vai para as garrafas de água mineral pronta para beber na sua mesa (Camada Gold, métricas de negócio prontas para relatórios)!",
        "pleno_text": "A Camada Bronze armazena dados brutos preservando histórico (append-only) com metadados de ingestão (`input_file_name()`, `current_timestamp()`). A Camada Silver limpa, deduplica, tipa e normaliza as entidades através de operações de enriquecimento e MERGE. A Camada Gold consolida modelos analíticos prontos para consumo de BI em formato dimensional (fatos e dimensões agregadas). Para manutenção de dimensões de clientes, o comando `MERGE INTO target USING source ON target.id = source.id` permite aplicar SCD Tipo 1 (sobrescrevendo atributos mutáveis) ou SCD Tipo 2 (mantendo histórico através de linhas com `is_current = false` e data de encerramento de vigência).",
        "senior_text": "Ponto de ouro do exame DP-750: Otimização de comandos MERGE INTO no Delta Lake. Quando a tabela de destino for particionada ou clusterizada, a cláusula ON do MERGE DEVE incluir a coluna de partição ou chave de clustering (`AND target.date = source.date`). Isso permite Partition Pruning e File Pruning, impedindo que o Spark faça Full Table Scan em terabytes de dados históricos para atualizar apenas um lote do dia.",
        "staff_text": "Internals do MERGE: O Delta Lake executa o merge em duas fases: um Inner Join inicial para identificar quais arquivos contêm registros correspondentes (target matching), seguido de uma fase de reescrita onde apenas os arquivos afetados são atualizados e gravados como novos Parquets (ou marcados via Deletion Vectors caso habilitados, reduzindo o I/O em até 80%).",
        "clevel_text": "Alinhamento Estratégico: A separação clara das camadas Medallion permite segregação de custos e acessos: apenas engenheiros têm acesso à camada Bronze; analistas de negócio consomem exclusivamente a camada Gold com respostas em subsegundos e dados 100% auditados.",
        "quiz": {
            "question": "Um engenheiro de dados precisa atualizar uma tabela Delta de clientes na camada Silver para rastrear mudanças de endereço. A empresa exige manter o histórico completo de todos os endereços anteriores que o cliente já teve ao longo do tempo. Qual técnica de modelagem de dados deve ser implementada?",
            "options": [
                {"text": "Implementar Slowly Changing Dimension Tipo 2 (SCD Tipo 2) utilizando MERGE INTO para expirar o registro antigo e inserir uma nova linha com is_current = true.", "correct": True, "explanation": "SCD Tipo 2 preserva o histórico de alterações criando uma nova linha para cada mudança com colunas de controle de validade temporal (start_date, end_date e flag is_current)."},
                {"text": "Executar um UPDATE simples sobrescrevendo a coluna de endereço na linha existente do cliente (SCD Tipo 1).", "correct": False, "explanation": "SCD Tipo 1 sobrescreve o valor anterior, destruindo o histórico de endereços passados do cliente."},
                {"text": "Truncar a tabela e recarregar os dados brutos a partir da landing zone.", "correct": False, "explanation": "Truncar e recarregar é inviável, custoso e apaga todo o histórico consolidado."},
                {"text": "Criar uma nova tabela para cada dia do ano contendo apenas o endereço daquele dia.", "correct": False, "explanation": "Criar tabelas diárias gera proliferação incontrolável de tabelas e impossibilita consultas analíticas eficientes."}
            ]
        }
    },
    {
        "id": "0012",
        "slug": "0012-structured-streaming-watermark-joins",
        "title": "Lição 0012: Engenharia de Tempo Real: Spark Structured Streaming, Watermarking & Joins",
        "module": "Módulo 3: Preparar e Processar Dados em Batch e Streaming (30–35% do Exame)",
        "module_id": "modulo-3",
        "next_slug": "0013-liquid-clustering-deletion-vectors-caching",
        "prev_slug": "0011-medallion-pyspark-sparksql-scd1-scd2",
        "summary": "Processe fluxos contínuos de eventos com Spark Structured Streaming: garantias exactly-once via Checkpointing, controle de atraso com Watermarking e junções temporais stream-stream.",
        "lab_file": "lesson_0012_lab.py",
        "junior_text": "Imagine um caixa de supermercado com uma fila sem fim: em vez de esperar a loja fechar para contar quanto dinheiro entrou (processamento batch), o caixa registra cada produto no exato segundo em que passa no scanner (streaming contínuo). Se um cliente esqueceu um pacote de arroz e chega 10 minutos depois, o caixa aceita; se chegar 3 horas depois, a compra já foi fechada (Watermarking)!",
        "pleno_text": "O Spark Structured Streaming trata streams de dados como uma tabela append-only sem fim. Todo stream produtivo exige a definição de um `checkpointLocation` no ADLS Gen2 para armazenar o progresso do offset e o estado da query, garantindo tolerância a falhas e semântica exactly-once. Os modos de saída (`outputMode`) são: 'append' (novas linhas apenas), 'update' (linhas modificadas) e 'complete' (tabela de agregação inteira recalculada). Em agregações temporais (janelas tumbling ou sliding), o `withWatermark('event_time', '10 minutes')` define o limite máximo de atraso para descartar dados tardios e liberar memória RAM do State Store.",
        "senior_text": "Foco para o exame DP-750: O trigger `availableNow=True` combina o melhor dos dois mundos: ele processa todos os dados pendentes em micro-lotes com lógica de streaming incremental e desliga automaticamente o cluster ao terminar. Isso gera economias astronômicas de FinOps ao substituir clusters de streaming 24/7 por execuções acionadas a cada poucas horas. Em Stream-Stream Joins, o watermark é OBRIGATÓRIO em ambos os fluxos, acompanhado de uma restrição temporal na cláusula ON (ex: `b.time BETWEEN a.time AND a.time + INTERVAL 1 HOUR`).",
        "staff_text": "State Store Provider Internals: Por padrão, o Spark mantém o estado em memória JVM (HDFSBackedStateStoreProvider), que pode sofrer com Garbage Collection em streams de longa duração com milhões de chaves. A Databricks recomenda configurar RocksDB como State Store (`spark.sql.streaming.stateStore.providerClass = '...RocksDBStateStoreProvider'`), gravando o estado em disco local rápido de SSD e sincronizando assincronamente com o ADLS Gen2.",
        "clevel_text": "SLA vs Custo: Nem todo pipeline precisa de latência de 2 segundos. O uso estratégico de triggers `availableNow` em conjunto com Job Clusters reduz o custo de infraestrutura em até 85% para fluxos com tolerância a dados semi-real time (ex: atualizações a cada 1 hora).",
        "quiz": {
            "question": "Um engenheiro de dados está projetando um pipeline em Structured Streaming que consome cliques de usuários de um Azure Event Hubs e agrega acessos por página em janelas de 15 minutos. Devido à instabilidade da rede celular dos usuários, alguns eventos chegam com até 20 minutos de atraso. Como evitar vazamento de memória (OutOfMemory) no cluster sem perder os eventos com atraso aceitável?",
            "options": [
                {"text": "Definir withWatermark('click_time', '20 minutes') antes da agregação da janela temporal no DataFrame de streaming.", "correct": True, "explanation": "O Watermarking informa ao engine de streaming para manter o estado dos eventos atrasados por até 20 minutos, descartando eventos mais antigos que isso e liberando memória no State Store."},
                {"text": "Aumentar a memória RAM do nó Driver para 512 GB e desabilitar o Garbage Collection.", "correct": False, "explanation": "Sem watermarking, o estado cresce indefinidamente até esgotar qualquer quantidade de memória disponível."},
                {"text": "Usar outputMode('complete') sem checkpointing configurado.", "correct": False, "explanation": "O modo complete sem checkpointing acumula todo o histórico e não garante tolerância a falhas nem limpeza de estado."},
                {"text": "Mudar o pipeline para ler os dados exclusivamente em batch uma vez por mês.", "correct": False, "explanation": "Não atende ao requisito de agregação em tempo real de cliques em janelas de 15 minutos."}
            ]
        }
    },
    {
        "id": "0013",
        "slug": "0013-liquid-clustering-deletion-vectors-caching",
        "title": "Lição 0013: Otimização Física: Liquid Clustering vs Partitioning & Deletion Vectors",
        "module": "Módulo 3: Preparar e Processar Dados em Batch e Streaming (30–35% do Exame)",
        "module_id": "modulo-3",
        "next_slug": "0014-delta-live-tables-streaming-views-expectations",
        "prev_slug": "0012-structured-streaming-watermark-joins",
        "summary": "Substitua velhos paradigmas: aprenda como o Liquid Clustering (CLUSTER BY) supera o particionamento Hive e Z-Order, e como Deletion Vectors aceleram mutações no Delta Lake.",
        "lab_file": "lesson_0013_lab.py",
        "junior_text": "Particionar tabelas antigamente era como colocar roupas em gavetas com divisórias de madeira rígidas: se você comprasse muitas meias, a gaveta transbordava (partição gigante), e se tivesse poucas camisetas, ficava muito espaço vazio (small files). O Liquid Clustering é como um tecido elástico inteligente que reorganiza o espaço automaticamente conforme as roupas entram!",
        "pleno_text": "O Liquid Clustering (`CLUSTER BY (col1, col2)`) é a nova geração de layout físico de dados no Delta Lake, substituindo tanto o particionamento tradicional baseado em pastas estilo Hive quanto o comando manual `OPTIMIZE ... ZORDER BY`. Ao contrário do particionamento rígido (que sofre com problemas de alta cardinalidade e skew), o Liquid Clustering ajusta os agrupamentos de dados dinamicamente sem sobrecarga de reescrever a tabela inteira. Deletion Vectors (DVs) permitem marcar linhas excluídas ou atualizadas como vetores de bits (soft-delete em nível de arquivo), permitindo que operações de DELETE e UPDATE concluam em segundos sem reescrever arquivos Parquet inteiros de 1 GB.",
        "senior_text": "Pegadinha clássica do DP-750: Em quais colunas aplicar Liquid Clustering? Em colunas comumente usadas em filtros de consultas WHERE, com alta cardinalidade (como `customer_id`, `device_id`), ou em colunas que crescem monotonicamente (`event_date`). A Databricks recomenda usar Liquid Clustering para todas as novas tabelas Delta. Além disso, Predictive Optimization do Unity Catalog executa automaticamente comandos OPTIMIZE e VACUUM em segundo plano, liberando o time de agendar jobs manuais de manutenção.",
        "staff_text": "Sob o capô, o Liquid Clustering utiliza uma estrutura baseada em curvas de preenchimento de espaço de Hilbert (Hilbert Space-Filling Curves) com múltiplos níveis de agrupamento incremental. Quando novos dados são ingeridos, apenas os clusters afetados sofrem recombinação no próximo `OPTIMIZE`, evitando a reordenação global massiva e custosa característica do Z-Ordering tradicional.",
        "clevel_text": "Redução Massiva de I/O e DBUs: O uso combinado de Liquid Clustering e Deletion Vectors reduz em até 90% o tráfego de gravação em storage ADLS Gen2 e o tempo de execução de operações de CDC/GDPR, resultando em impacto imediato na redução de custos de nuvem.",
        "quiz": {
            "question": "Uma empresa de e-commerce possui uma tabela Delta de 50 TB consultada frequentemente por 'data_pedido', 'pais' e 'categoria_produto'. A equipe sofre com problemas constantes de partições desbalanceadas (data skew) e alto custo para rodar OPTIMIZE ZORDER periodicamente. Qual arquitetura moderna resolve esse cenário?",
            "options": [
                {"text": "Criar a tabela utilizando Liquid Clustering com CLUSTER BY (data_pedido, pais, categoria_produto).", "correct": True, "explanation": "Liquid Clustering (CLUSTER BY) elimina as restrições rígidas de particionamento Hive e a sobrecarga do Z-Ordering, acomodando dados com cardinalidades variáveis e reorganizando arquivos incrementalmente."},
                {"text": "Particionar a tabela em 10 níveis de diretórios no ADLS Gen2.", "correct": False, "explanation": "Criar dezenas de níveis de partição causa o problema severo de 'small files' e degrada drasticamente a performance do catálogo."},
                {"text": "Desabilitar todos os índices e armazenar os dados em formato CSV compactado com GZIP.", "correct": False, "explanation": "CSV não suporta estatísticas colunares, clustering nem ACID, sendo completamente inadequado para 50 TB de dados analíticos."},
                {"text": "Executar VACUUM RETAIN 0 HOURS a cada 10 minutos para apagar arquivos órfãos.", "correct": False, "explanation": "VACUUM limpa arquivos históricos, mas não melhora a organização física nem resolve skew de dados."}
            ]
        }
    },
    {
        "id": "0014",
        "slug": "0014-delta-live-tables-streaming-views-expectations",
        "title": "Lição 0014: Pipelines Declarativos com Delta Live Tables (DLT) & Data Quality Expectations",
        "module": "Módulo 4: Implantar e Manter Pipelines e Workloads (30–35% do Exame)",
        "module_id": "modulo-4",
        "next_slug": "0015-orquestracao-dabs-cicd-system-tables",
        "prev_slug": "0013-liquid-clustering-deletion-vectors-caching",
        "summary": "Construa pipelines confiáveis com Delta Live Tables (Lakeflow): crie Streaming Tables, Materialized Views, garanta qualidade de dados com Expectations e aplique CDC com APPLY CHANGES INTO.",
        "lab_file": "lesson_0014_lab.py",
        "junior_text": "Delta Live Tables (DLT) é como a fábrica automatizada da montadora de carros: em vez de você ligar cada máquina, transportar peças no carrinho de mão e conferir parafuso por parafuso manualmente, você apenas define a planta da fábrica (código declarativo). A linha de produção anda sozinha e descarta peças defeituosas automaticamente (Expectations)!",
        "pleno_text": "Delta Live Tables (DLT) simplifica o desenvolvimento de ETL através de um framework puramente declarativo em SQL (`CREATE OR REFRESH STREAMING TABLE`) ou Python (`@dlt.table`). DLT gerencia automaticamente o grafo acíclico dirigido (DAG), orquestração de dependências, tratamento de erros e infraestrutura de cluster. As Data Quality Expectations garantem governança em três níveis: 1) `@dlt.expect('nome', 'condição')` (apenas registra no log de qualidade), 2) `@dlt.expect_or_drop('nome', 'condição')` (descarta a linha inválida e prossegue), e 3) `@dlt.expect_or_fail('nome', 'condição')` (aborta o pipeline imediatamente). Para ingestão de CDC (Change Data Capture), a instrução `dlt.apply_changes()` processa automaticamente upserts de chaves com SCD Tipo 1 ou Tipo 2.",
        "senior_text": "Questão recorrente no DP-750: Diferença crucial entre Streaming Tables e Materialized Views no DLT! Streaming Tables processam dados de fontes append-only de forma estritamente incremental e mantêm o histórico da tabela mesmo que os dados na fonte original sejam descartados. Materialized Views recalculam os resultados para refletir o estado mais recente dos dados da fonte (ideal para agregações complexas, joins e tabelas Gold de BI).",
        "staff_text": "O DLT grava todas as métricas de execução, qualidade de dados (linhas aprovadas, linhas descartadas) e linhagem em um Event Log em formato Delta Lake armazenado no storage do pipeline. Engenheiros podem consultar esse Event Log via SQL para criar dashboards operacionais de observabilidade corporativa.",
        "clevel_text": "Confiabilidade de Dados (Data Reliability): O DLT transforma a engenharia de dados em um processo auditável com SLAs mensuráveis, eliminando custos de manutenção de scripts manuais de orquestração e garantindo que dados de baixa qualidade nunca alcancem relatórios de diretoria.",
        "quiz": {
            "question": "Um engenheiro de dados está implementando um pipeline Delta Live Tables (DLT) para processar transações financeiras. A regra de negócio exige que se uma transação tiver valor nulo ou negativo (valor <= 0), essa linha específica deve ser descartada do conjunto de dados processado, mas o pipeline deve continuar executando sem falhar. Qual expectation deve ser utilizada?",
            "options": [
                {"text": "CONSTRAINT transacao_valida EXPECT (valor > 0) ON VIOLATION DROP ROW", "correct": True, "explanation": "A cláusula ON VIOLATION DROP ROW (ou @dlt.expect_or_drop em Python) descarta silenciosamente as linhas que violam a condição e continua o processamento das linhas válidas."},
                {"text": "CONSTRAINT transacao_valida EXPECT (valor > 0) ON VIOLATION FAIL UPDATE", "correct": False, "explanation": "ON VIOLATION FAIL UPDATE interrompe e falha o pipeline inteiro na primeira linha inválida encontrada."},
                {"text": "CONSTRAINT transacao_valida EXPECT (valor > 0)", "correct": False, "explanation": "A forma básica sem ação explícita apenas registra métricas no log de eventos, mas mantém as linhas inválidas na tabela de destino."},
                {"text": "THROW ERROR WHEN valor <= 0", "correct": False, "explanation": "Sintaxe inexistente no framework de Expectations do Delta Live Tables."}
            ]
        }
    },
    {
        "id": "0015",
        "slug": "0015-orquestracao-dabs-cicd-system-tables",
        "title": "Lição 0015: Orquestração em Produção: Databricks Workflows, DABs & CI/CD",
        "module": "Módulo 4: Implantar e Manter Pipelines e Workloads (30–35% do Exame)",
        "module_id": "modulo-4",
        "next_slug": None,
        "prev_slug": "0014-delta-live-tables-streaming-views-expectations",
        "summary": "Eleve seus pipelines a nível empresarial: orquestre tarefas com Databricks Workflows (DAGs, Task Values, Repair Run), implemente CI/CD com Databricks Asset Bundles (DABs) e monitore via Spark UI e Azure Monitor.",
        "lab_file": "lesson_0015_lab.py",
        "junior_text": "Databricks Workflows é como o relógio despertador e a agenda do seu celular juntos: ele sabe que às 06:00 da manhã precisa tocar o despertador (Tarefa 1), depois ligar a cafeteira (Tarefa 2) e só depois te avisar que o café está pronto (Tarefa 3). Se faltar luz na cafeteira, ele te avisa e permite tentar de novo só a parte do café sem ter que voltar a dormir e acordar de novo (Repair Run)!",
        "pleno_text": "Databricks Workflows é o orquestrador nativo totalmente gerenciado do Lakehouse. Ele permite criar Jobs compostos por múltiplas tarefas (Notebooks, Python Scripts, DLT Pipelines, SQL Queries, dbt) organizadas em um DAG com dependências condicionais (`Run if: All succeeded`, `At least one succeeded`). Variáveis dinâmicas são passadas entre tarefas downstream através de Task Values (`dbutils.jobs.taskValues.set()` e `.get()`). Em caso de falha de uma tarefa em um job com 10 etapas, a funcionalidade **Repair Run** reexecuta apenas a tarefa com falha e suas dependências, poupando tempo e custo de computação.",
        "senior_text": "Tema central obrigatório do DP-750: **Databricks Asset Bundles (DABs)** é a abordagem moderna padrão de Infrastructure as Code (IaC) e CI/CD para Databricks. O arquivo `databricks.yml` declara pipelines, jobs, permissões e ambientes (`dev`, `staging`, `prod`). Com comandos CLI simples (`databricks bundle validate`, `databricks bundle deploy -t prod`, `databricks bundle run`), integra-se o desenvolvimento diretamente ao Azure DevOps Pipelines ou GitHub Actions sem configurações manuais no portal.",
        "staff_text": "Depuração avançada com Spark UI: Ao investigar gargalos em jobs de produção, o engenheiro de dados deve analisar as abas **Jobs**, **Stages** e **Executors**. A presença de **Spill (Memory)** e **Spill (Disk)** indica que partições de dados excederam a memória do executor e foram despejadas em disco, apontando para necessidade de repartitioning ou aumento de nós de worker. **Data Skew** é visualizado quando uma única task demora 10x mais que as outras no percentil 75/max da Stage UI.",
        "clevel_text": "Maturidade de Engenharia de Dados: O uso de Databricks Asset Bundles (DABs) garante versionamento rigoroso, deploy automatizado sem intervenção humana e testes automatizados antes da ida a produção, reduzindo o tempo de lançamento de novos produtos de dados de meses para dias.",
        "quiz": {
            "question": "Um pipeline de produção no Databricks Workflows composto por 8 tarefas sequenciais falhou na tarefa 6 devido a uma indisponibilidade temporária de rede na API de destino. O tempo total de execução das 5 primeiras tarefas foi de 3 horas. Qual recurso nativo do Databricks permite resolver a falha com o menor custo de computação e tempo?",
            "options": [
                {"text": "Utilizar o recurso 'Repair Run' (Reparar Execução) no Databricks Workflows para reexecutar apenas a tarefa 6 e as tarefas dependentes subsequentes.", "correct": True, "explanation": "O recurso Repair Run permite reexecutar exclusivamente a tarefa que falhou e as etapas downstream, sem gastar tempo e DBUs recalculando as tarefas que já haviam concluído com sucesso."},
                {"text": "Disparar uma nova execução completa do Job desde a tarefa 1.", "correct": False, "explanation": "Reexecutar o Job completo desperdiçará mais de 3 horas de computação e DBUs para rodar tarefas que já haviam concluído com sucesso."},
                {"text": "Recriar manualmente o Job com apenas as tarefas 6, 7 e 8.", "correct": False, "explanation": "Trabalho manual sujeito a erros que quebra o histórico de monitoramento e governança do pipeline corporativo."},
                {"text": "Substituir o Databricks Workflows por um cron job em uma máquina virtual Linux.", "correct": False, "explanation": "Regressão arquitetural que perde toda a integração nativa, autenticação do Entra ID, UI de monitoramento e tolerância a falhas."}
            ]
        }
    }
]

def generate_svg_diagram(lesson):
    lid = lesson["id"]
    return f'''
    <div class="svg-diagram-wrapper">
      <svg viewBox="0 0 960 360" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="grad-db-{lid}" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#1B3139"/>
            <stop offset="100%" stop-color="#111E24"/>
          </linearGradient>
          <linearGradient id="grad-accent-{lid}" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#FF3621"/>
            <stop offset="100%" stop-color="#FF5A36"/>
          </linearGradient>
          <filter id="shadow-{lid}" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
            <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#000000" flood-opacity="0.15"/>
          </filter>
        </defs>

        <rect x="10" y="10" width="940" height="340" rx="12" fill="#F8FAFC" stroke="#D1DDE5" stroke-width="1.5"/>
        <rect x="10" y="10" width="940" height="50" rx="12" fill="url(#grad-db-{lid})"/>
        <rect x="10" y="48" width="940" height="12" fill="#111E24"/>
        <text x="35" y="42" fill="#FFFFFF" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="16" font-weight="700" letter-spacing="0.5">
          ARQUITETURA DE REFERÊNCIA DP-750 — {lid}
        </text>
        <text x="890" y="42" fill="#FF5A36" font-family="monospace" font-size="14" font-weight="700" text-anchor="end">
          AZURE DATABRICKS
        </text>

        <!-- Bloco 1: Controle & Origem -->
        <g transform="translate(40, 85)" filter="url(#shadow-{lid})">
          <rect x="0" y="0" width="260" height="230" rx="8" fill="#FFFFFF" stroke="#0078D4" stroke-width="2"/>
          <rect x="0" y="0" width="260" height="38" rx="8" fill="#0078D4"/>
          <rect x="0" y="30" width="260" height="8" fill="#0078D4"/>
          <text x="130" y="25" fill="#FFFFFF" font-family="sans-serif" font-size="13" font-weight="700" text-anchor="middle">1. CONTROLE &amp; ORIGEM</text>
          
          <rect x="20" y="55" width="220" height="42" rx="6" fill="#F0F6F9" stroke="#BDCBD3"/>
          <text x="30" y="80" fill="#1B3139" font-family="sans-serif" font-size="12" font-weight="600">Microsoft Entra ID / SCIM</text>
          
          <rect x="20" y="110" width="220" height="42" rx="6" fill="#F0F6F9" stroke="#BDCBD3"/>
          <text x="30" y="135" fill="#1B3139" font-family="sans-serif" font-size="12" font-weight="600">Azure Key Vault / Secret</text>
          
          <rect x="20" y="165" width="220" height="42" rx="6" fill="#F0F6F9" stroke="#BDCBD3"/>
          <text x="30" y="190" fill="#1B3139" font-family="sans-serif" font-size="12" font-weight="600">Control Plane (WebApp/UI)</text>
        </g>

        <!-- Seta 1 para 2 -->
        <path d="M 310 200 L 345 200" stroke="#FF3621" stroke-width="3" fill="none" stroke-linecap="round"/>
        <polygon points="345,194 357,200 345,206" fill="#FF3621"/>

        <!-- Bloco 2: Compute Plane -->
        <g transform="translate(360, 85)" filter="url(#shadow-{lid})">
          <rect x="0" y="0" width="260" height="230" rx="8" fill="#FFFFFF" stroke="#FF3621" stroke-width="2"/>
          <rect x="0" y="0" width="260" height="38" rx="8" fill="url(#grad-accent-{lid})"/>
          <rect x="0" y="30" width="260" height="8" fill="#FF5A36"/>
          <text x="130" y="25" fill="#FFFFFF" font-family="sans-serif" font-size="13" font-weight="700" text-anchor="middle">2. COMPUTE PLANE &amp; SPARK</text>
          
          <rect x="20" y="55" width="220" height="42" rx="6" fill="#FFF9F8" stroke="#FFBEB6"/>
          <text x="30" y="80" fill="#C22212" font-family="sans-serif" font-size="12" font-weight="600">Photon Engine C++ / DBR</text>
          
          <rect x="20" y="110" width="220" height="42" rx="6" fill="#FFF9F8" stroke="#FFBEB6"/>
          <text x="30" y="135" fill="#C22212" font-family="sans-serif" font-size="12" font-weight="600">Job Cluster / Serverless</text>
          
          <rect x="20" y="165" width="220" height="42" rx="6" fill="#FFF9F8" stroke="#FFBEB6"/>
          <text x="30" y="190" fill="#C22212" font-family="sans-serif" font-size="12" font-weight="600">Catalyst Logical &amp; Physical</text>
        </g>

        <!-- Seta 2 para 3 -->
        <path d="M 630 200 L 665 200" stroke="#00A972" stroke-width="3" fill="none" stroke-linecap="round"/>
        <polygon points="665,194 677,200 665,206" fill="#00A972"/>

        <!-- Bloco 3: Unity Catalog & Delta -->
        <g transform="translate(680, 85)" filter="url(#shadow-{lid})">
          <rect x="0" y="0" width="240" height="230" rx="8" fill="#FFFFFF" stroke="#00A972" stroke-width="2"/>
          <rect x="0" y="0" width="240" height="38" rx="8" fill="#00A972"/>
          <rect x="0" y="30" width="240" height="8" fill="#00A972"/>
          <text x="120" y="25" fill="#FFFFFF" font-family="sans-serif" font-size="13" font-weight="700" text-anchor="middle">3. UNITY CATALOG &amp; DELTA</text>
          
          <rect x="15" y="55" width="210" height="42" rx="6" fill="#E8F8F2" stroke="#A2E4B8"/>
          <text x="25" y="80" fill="#00703C" font-family="sans-serif" font-size="12" font-weight="600">Namespace: cat.sch.tbl</text>
          
          <rect x="15" y="110" width="210" height="42" rx="6" fill="#E8F8F2" stroke="#A2E4B8"/>
          <text x="25" y="135" fill="#00703C" font-family="sans-serif" font-size="12" font-weight="600">Delta Log (_delta_log JSON)</text>
          
          <rect x="15" y="165" width="210" height="42" rx="6" fill="#E8F8F2" stroke="#A2E4B8"/>
          <text x="25" y="190" fill="#00703C" font-family="sans-serif" font-size="12" font-weight="600">ADLS Gen2 Parquet / DVs</text>
        </g>
      </svg>
      <div class="svg-caption">Figura {lid}.1: Fluxo arquitetural do Azure Databricks detalhando a segregação de responsabilidades do exame DP-750.</div>
    </div>
    '''

def generate_workspace_mock(lesson):
    lid = lesson["id"]
    return f'''
    <div class="workspace-mock-frame">
      <div class="workspace-mock-header">
        <div class="workspace-mock-dots">
          <div class="mock-dot mock-dot-red"></div>
          <div class="mock-dot mock-dot-yellow"></div>
          <div class="mock-dot mock-dot-green"></div>
        </div>
        <div class="workspace-mock-title">Azure Databricks Workspace — adb-prod-eastus2.azuredatabricks.net ({lesson["id"]})</div>
        <div style="color: #00A972; font-size: 0.72rem; font-weight: 700;">CONNECTED • DBR 15.4 LTS PHOTON</div>
      </div>
      <div style="padding: 1.2rem; background: #141E24; color: #E1E8ED; font-family: monospace; font-size: 0.85rem; line-height: 1.6;">
        <div style="color: #8BA2AD; margin-bottom: 0.8rem;">// Console interativo do Azure Databricks — Simulação da Lição {lid}</div>
        <div style="color: #FF5A36;">%python</div>
        <div><span style="color: #0078D4;">import</span> dlt</div>
        <div><span style="color: #0078D4;">from</span> pyspark.sql.functions <span style="color: #0078D4;">import</span> col, current_timestamp, expr</div>
        <div style="margin: 0.5rem 0; color: #536B75;"># Executando validação de governança e métricas de execução</div>
        <div>spark.conf.set(<span style="color: #FFB900;">"spark.databricks.delta.optimizeWrite.enabled"</span>, <span style="color: #00A972;">"true"</span>)</div>
        <div>spark.conf.set(<span style="color: #FFB900;">"spark.databricks.delta.autoCompact.enabled"</span>, <span style="color: #00A972;">"true"</span>)</div>
        <div style="margin-top: 0.6rem; color: #00A972;">✓ SparkSession ativa: driver 10.0.1.4 | Cluster: Job-Cluster-{lid} | DBUs/h: 1.5</div>
      </div>
    </div>
    '''

def build_hands_on_lab_html(lid):
    lab_info = LABS_STEPS.get(lid, {
        "title": f"Lab {lid}: Laboratório Prático de Engenharia Azure Databricks",
        "duration": "35 minutos",
        "scenario": "Execute exercícios práticos no padrão Microsoft Learn para consolidar a teoria do exame DP-750.",
        "azure_prereq": "Assinatura ativa do Microsoft Azure com Azure Databricks Workspace alocado.",
        "tasks": []
    })

    tasks_html = ""
    for task in lab_info["tasks"]:
        code_block = ""
        if "code" in task:
            code_block = f"""
            <div style="margin: 0.8rem 0;">
              <span style="font-size: 0.75rem; font-weight: 700; color: #536B75; text-transform: uppercase;">Código para colar na célula do Notebook Databricks:</span>
              <pre><code>{task['code']}</code></pre>
            </div>
            """
        
        output_block = ""
        if "expected_output" in task:
            output_block = f"""
            <div style="background: #0B161B; border: 1px solid #253D47; border-radius: 6px; padding: 0.8rem 1rem; margin: 0.6rem 0; font-family: monospace; font-size: 0.82rem; color: #00A972;">
              <span style="color: #8BA2AD; font-size: 0.72rem; display: block; margin-bottom: 0.3rem;">✓ Saída Esperada no Console Databricks:</span>
              {task['expected_output'].replace(chr(10), '<br>')}
            </div>
            """

        tasks_html += f"""
        <div class="lab-task-card">
          <h4>
            <span class="lab-task-number">Tarefa {task['num']}</span>
            {task['title']}
          </h4>
          <p style="white-space: pre-line;">
            {task['instructions']}
          </p>
          {code_block}
          {output_block}
        </div>
        """

    return f"""
    <!-- BANNER DE PRÉ-REQUISITO OBRIGATÓRIO DA AZURE -->
    <div class="lab-prereq-banner">
      <span class="alert-icon">⚠️</span>
      <div>
        <h4>
          PRÉ-REQUISITO OBRIGATÓRIO DA AZURE (Microsoft Learn Standards)
        </h4>
        <p>
          Para realizar este laboratório prático e executar os comandos reais, criar clusters, pipelines Delta Live Tables (DLT) e tabelas do Unity Catalog, <strong>você precisará de um Workspace do Azure Databricks alocado na sua assinatura do Microsoft Azure</strong> (Recomendado tier Premium para suporte completo a Unity Catalog e Serverless Compute).
        </p>
        <div style="margin-top: 0.6rem; font-size: 0.85rem; opacity: 0.9;">
          <strong>Pré-requisitos Técnicos:</strong> {lab_info['azure_prereq']}
        </div>
      </div>
    </div>

    <!-- ESTRUTURA DO LAB PASSO A PASSO -->
    <div class="lab-container">
      <div class="lab-header">
        <div>
          <span style="font-size: 0.72rem; font-weight: 800; background: #0078D4; color: #FFFFFF; padding: 0.2rem 0.5rem; border-radius: 4px; text-transform: uppercase;">
            Hands-on Lab Walkthrough
          </span>
          <h3 style="margin: 0.4rem 0 0 0; font-size: 1.2rem;">{lab_info['title']}</h3>
        </div>
        <div style="text-align: right;">
          <span style="font-size: 0.85rem; font-weight: 600;">⏱️ Tempo Estimado: {lab_info['duration']}</span>
        </div>
      </div>

      <div style="margin-bottom: 1.5rem;">
        <strong style="font-size: 0.95rem;">📖 Cenário do Laboratório:</strong>
        <p style="margin: 0.3rem 0; font-size: 0.92rem; line-height: 1.6;">
          {lab_info['scenario']}
        </p>
      </div>

      <!-- Tarefas Passo a Passo -->
      <div style="margin-top: 1.5rem;">
        {tasks_html}
      </div>
    </div>
    """

def main():
    os.makedirs("lessons", exist_ok=True)
    os.makedirs("labs", exist_ok=True)
    
    for lesson in LESSONS_DATA:
        lid = lesson["id"]
        file_path = os.path.join("lessons", f"{lesson['slug']}.html")
        prev_link = f'<a href="{lesson["prev_slug"]}.html" class="nav-btn">← Lição Anterior</a>' if lesson["prev_slug"] else '<span class="nav-btn disabled">← Início</span>'
        next_link = f'<a href="{lesson["next_slug"]}.html" class="nav-btn">Próxima Lição →</a>' if lesson["next_slug"] else '<a href="../reference/01-spark-and-databricks-architecture-visual-guide.html" class="nav-btn">Folhas de Referência →</a>'
        
        hands_on_lab_content = build_hands_on_lab_html(lid)
        
        html_content = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{lesson["title"]} | Databricks Formation DP-750</title>
  <meta name="description" content="{lesson["summary"]}">
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
      <li><a href="../index.html#{lesson["module_id"]}" class="active">{lesson["module"].split(":")[0]}</a></li>
      <li><a href="../simulados/index.html">Simulados Pearson VUE</a></li>
      <li><a href="../reference/01-spark-and-databricks-architecture-visual-guide.html">Folhas de Referência</a></li>
      <li><button type="button" class="theme-toggle-btn" onclick="window.toggleAppTheme()">🌙 Modo Dark</button></li>
    </ul>
  </header>

  <!-- Quick Index Superior (#quick-index) -->
  <nav id="quick-index">
    <div class="quick-index-container">
      <span class="quick-index-label">Lições Rápidas:</span>
      <a href="0001-arquitetura-azure-databricks-compute-dbus.html" class="index-chip {'active' if lid == '0001' else ''}">0001</a>
      <a href="0002-anatomia-apache-spark-catalyst-photon.html" class="index-chip {'active' if lid == '0002' else ''}">0002</a>
      <a href="0003-protocolo-delta-lake-acid-time-travel.html" class="index-chip {'active' if lid == '0003' else ''}">0003</a>
      <a href="0004-workspaces-entra-id-vnet-private-link.html" class="index-chip {'active' if lid == '0004' else ''}">0004</a>
      <a href="0005-clusters-policies-pools-serverless-sql.html" class="index-chip {'active' if lid == '0005' else ''}">0005</a>
      <a href="0006-integracao-azure-keyvault-adls-external.html" class="index-chip {'active' if lid == '0006' else ''}">0006</a>
      <a href="0007-unity-catalog-metastore-namespace-volumes.html" class="index-chip {'active' if lid == '0007' else ''}">0007</a>
      <a href="0008-controle-acesso-fino-row-column-masks.html" class="index-chip {'active' if lid == '0008' else ''}">0008</a>
      <a href="0009-linhagem-system-tables-delta-sharing.html" class="index-chip {'active' if lid == '0009' else ''}">0009</a>
      <a href="0010-ingestao-autoloader-copyinto-lakeflow.html" class="index-chip {'active' if lid == '0010' else ''}">0010</a>
      <a href="0011-medallion-pyspark-sparksql-scd1-scd2.html" class="index-chip {'active' if lid == '0011' else ''}">0011</a>
      <a href="0012-structured-streaming-watermark-joins.html" class="index-chip {'active' if lid == '0012' else ''}">0012</a>
      <a href="0013-liquid-clustering-deletion-vectors-caching.html" class="index-chip {'active' if lid == '0013' else ''}">0013</a>
      <a href="0014-delta-live-tables-streaming-views-expectations.html" class="index-chip {'active' if lid == '0014' else ''}">0014</a>
      <a href="0015-orquestracao-dabs-cicd-system-tables.html" class="index-chip {'active' if lid == '0015' else ''}">0015</a>
      <a href="../simulados/index.html" class="index-chip special">Simulado (+180Q)</a>
    </div>
  </nav>

  <article>
    <!-- Header da Lição -->
    <div id="bloco-contexto" style="margin-bottom: 1.5rem;">
      <span style="font-size: 0.85rem; font-weight: 700; color: #FF3621; text-transform: uppercase; letter-spacing: 0.05em;">{lesson["module"]}</span>
      <h1>{lesson["title"]}</h1>
      <p class="subtitle">{lesson["summary"]}</p>
    </div>

    <!-- Barra de Nível / Lente (Persistência Global no padrão DP-700) -->
    <nav class="lens-selector-bar">
      <span>Nível Ativo:</span>
      <button class="lens-btn active" data-lens="unificado" data-lens-target="all">
        <span>🌐 Visão Unificada</span>
        <span class="lens-key-badge">0</span>
      </button>
      <button class="lens-btn" data-lens="junior" data-lens-target="junior">
        <span>🌱 Júnior</span>
        <span class="lens-key-badge">1</span>
      </button>
      <button class="lens-btn" data-lens="pleno" data-lens-target="pleno">
        <span>🛠️ Pleno</span>
        <span class="lens-key-badge">2</span>
      </button>
      <button class="lens-btn" data-lens="senior" data-lens-target="senior">
        <span>🎯 Sênior &amp; DP-750</span>
        <span class="lens-key-badge">3</span>
      </button>
      <button class="lens-btn" data-lens="staff" data-lens-target="staff">
        <span>⚙️ Staff</span>
        <span class="lens-key-badge">4</span>
      </button>
      <button class="lens-btn" data-lens="clevel" data-lens-target="c-level">
        <span>🏛️ C-Level</span>
        <span class="lens-key-badge">5</span>
      </button>
      <div class="current-lens-badge" id="current-profile-label">🌐 Visão Unificada Completa</div>
    </nav>

    <!-- Barra de Navegação Rápida da Lição -->
    <div class="vark-nav-bar">
      <span>Navegação da Lição:</span>
      <a href="#bloco-audio" class="vark-pill">🎧 Áudio Explicativo</a>
      <a href="#bloco-visual" class="vark-pill">👁️ Arquitetura Visual</a>
      <a href="#bloco-teoria" class="vark-pill">📖 Teoria &amp; Decisões</a>
      <a href="#bloco-pratica" class="vark-pill">🛠️ Lab Hands-on</a>
      <a href="#bloco-quiz" class="vark-pill">🎯 Desafio do Exame</a>
    </div>

    <!-- Narração Técnica em Áudio -->
    <section id="bloco-audio" class="vark-section">
      <span class="vark-badge vark-badge-a">🎧 Narração da Aula &amp; Termos Oficiais</span>
      <p>
        Acompanhe a explicação técnica em áudio desta lição, com pronúncia calibrada dos termos oficiais em inglês do Azure Databricks (ex: <em>Catalyst Optimizer, Photon, Liquid Clustering, Deletion Vectors, Delta Log</em>).
      </p>
      <div class="audio-hint-box">
        <strong>Controle de Reprodução:</strong> Utilize o player na base da tela para iniciar o áudio, ajustar a velocidade (1x, 1.25x, 1.5x, 2x) ou use os botões <strong>Fixar/Desafixar</strong> e <strong>Ocultar</strong> para personalizar sua experiência de leitura.
        <div style="margin-top: 0.75rem; display: flex; gap: 0.6rem; flex-wrap: wrap;">
          <button type="button" class="audio-tool-btn" onclick="window.toggleAudioPlayFromSection()">
            <span>▶️ Ouvir Lição Agora</span>
          </button>
          <button type="button" class="audio-tool-btn" onclick="window.toggleAudioPin()">
            <span class="inline-pin-label">📍 Desafixar da Base</span>
          </button>
          <button type="button" class="audio-tool-btn" onclick="window.toggleAudioHide(true)">
            <span>▼ Ocultar Player</span>
          </button>
        </div>
      </div>
    </section>

    <!-- Arquitetura Visual & Workspace -->
    <section id="bloco-visual" class="vark-section">
      <span class="vark-badge vark-badge-v">👁️ Arquitetura de Referência &amp; Console Interativo</span>
      {generate_svg_diagram(lesson)}
      {generate_workspace_mock(lesson)}
    </section>

    <!-- Conteúdo Teórico Chaveado por Nível -->
    <section id="bloco-teoria" class="vark-section">
      <span class="vark-badge vark-badge-r">📖 Conteúdo Teórico &amp; Matrizes de Decisão</span>

      <!-- 1. TEXTO DA VISÃO UNIFICADA COMPLETA (Padrão DP-700) -->
      <div class="lens-text-content" data-lens="unificado" data-lens-block>
        <div class="unified-lens-box">
          <h3 style="margin-top: 0; font-size: 1.05rem;">🌐 Visão Unificada Completa: Integração Arquitetural de Ponta a Ponta</h3>
          <p style="margin-bottom: 0.75rem; line-height: 1.65;">
            {lesson["summary"]} Esta lição articula a ponte entre os fundamentos conceituais, a prática de engenharia no Azure Databricks e os critérios rigorosos de aprovação no exame Microsoft DP-750.
          </p>
          <p style="margin-bottom: 0.75rem; line-height: 1.65;">
            <strong>No dia a dia prático:</strong> {lesson["pleno_text"]}
          </p>
          <p style="margin-bottom: 0.75rem; line-height: 1.65;">
            <strong>Diretriz oficial DP-750 &amp; Decisão Arquitetural:</strong> {lesson["senior_text"]}
          </p>
          <p style="margin-bottom: 0; line-height: 1.65;">
            <strong>Mecânica Interna &amp; Governança Executiva:</strong> {lesson["staff_text"]} Em termos de FinOps corporativo: {lesson["clevel_text"]}
          </p>
        </div>
      </div>

      <!-- 2. Lente Júnior -->
      <div class="lens-text-content" data-lens="junior" data-lens-block style="display: none; margin-bottom: 2rem;">
        <span class="lens-tag-badge lens-tag-junior">🌱 Lente Júnior: Fundamentos &amp; Analogia do Mundo Real</span>
        <p>{lesson["junior_text"]}</p>
      </div>

      <!-- 3. Lente Pleno -->
      <div class="lens-text-content" data-lens="pleno" data-lens-block style="display: none; margin-bottom: 2rem;">
        <span class="lens-tag-badge lens-tag-pleno">🛠️ Lente Pleno: Engenharia Prática &amp; Implementação</span>
        <p>{lesson["pleno_text"]}</p>
        <label for="sn-{lid}-1" class="margin-toggle sidenote-number"></label>
        <input type="checkbox" id="sn-{lid}-1" class="margin-toggle"/>
        <span class="sidenote">Nota prática de engenharia: A adesão estrita aos padrões de convenção evita regressões em produção e garante portabilidade imediata para ambientes multirregionais no Azure.</span>
      </div>

      <!-- 4. Lente Sênior & Exame DP-750 -->
      <div class="lens-text-content" data-lens="senior" data-lens-block style="display: none; margin-bottom: 2rem;">
        <span class="lens-tag-badge lens-tag-senior">🎯 Lente Sênior: Foco no Exame DP-750 &amp; Pegadinhas Oficiais</span>
        <p>{lesson["senior_text"]}</p>
        <blockquote>
          <strong>⚠️ Dica Crítica de Exame Microsoft DP-750:</strong> Preste extrema atenção aos enunciados que mencionam restrições orçamentárias (FinOps) vs restrições de latência. A resposta tecnicamente mais veloz nem sempre é a correta se violar a diretriz de menor custo de DBUs do enunciado.
        </blockquote>
      </div>

      <!-- 5. Lente Staff / Internals -->
      <div class="lens-text-content" data-lens="staff" data-lens-block style="display: none; margin-bottom: 2rem;">
        <span class="lens-tag-badge lens-tag-staff">⚙️ Lente Staff: Mecânica Interna &amp; Algoritmos Sob o Capô</span>
        <p>{lesson["staff_text"]}</p>
      </div>

      <!-- 6. Lente C-Level / FinOps -->
      <div class="lens-text-content" data-lens="c-level" data-lens-alt="clevel" data-lens-block style="display: none; margin-bottom: 2rem;">
        <span class="lens-tag-badge lens-tag-c-level">🏛️ Lente C-Level: Governança, TCO &amp; FinOps de DBUs</span>
        <p>{lesson["clevel_text"]}</p>
      </div>

      <!-- Tabela ASCII de Alta Densidade Tufte -->
      <div class="fullwidth" style="margin: 2rem 0;">
        <h3>📊 Matriz de Decisão Arquitetural — Lição {lid}</h3>
        <table>
          <thead>
            <tr>
              <th>Critério / Dimensão</th>
              <th>Abordagem Convencional (Legada)</th>
              <th>Padrão Ouro Azure Databricks (DP-750)</th>
              <th>Impacto em FinOps &amp; SLA</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Governança de Dados</strong></td>
              <td>Hive Metastore e montagens DBFS locais</td>
              <td>Unity Catalog (3-Level Namespace: cat.sch.tbl)</td>
              <td>Zero vazamento de credenciais; trilha de auditoria centralizada</td>
            </tr>
            <tr>
              <td><strong>Tipo de Computação</strong></td>
              <td>All-Purpose Clusters com autotermination desligado</td>
              <td>Job Clusters efêmeros ou Serverless Compute</td>
              <td>Redução de até 60% no consumo de DBUs por execução</td>
            </tr>
            <tr>
              <td><strong>Otimização de Armazenamento</strong></td>
              <td>Particionamento rígido com centenas de subdiretórios</td>
              <td>Liquid Clustering (CLUSTER BY) + Deletion Vectors</td>
              <td>Eliminação de skew e mutações sem reescrever Parquets</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- Laboratório Prático Passo a Passo -->
    <section id="bloco-pratica" class="vark-section">
      <span class="vark-badge vark-badge-k">🛠️ Laboratório Prático Passo a Passo (Padrão Microsoft Learn)</span>

      <!-- Hands-on Lab Passo a Passo com Aviso Azure -->
      {hands_on_lab_content}
    </section>

    <!-- Desafio do Exame DP-750 com Embaralhamento Fisher-Yates -->
    <section id="bloco-quiz" class="vark-section">
      <div class="flash-quiz-box">
        <div class="flash-quiz-header">
          <h4 class="flash-quiz-title">🎯 Desafio Flash DP-750</h4>
          <button type="button" class="btn-shuffle" title="Embaralha as alternativas usando o algoritmo Fisher-Yates">
            <span>🔀 Embaralhar Novamente</span>
          </button>
        </div>
        <div class="flash-question-text">{lesson["quiz"]["question"]}</div>
        <div class="flash-options-list">
          {"".join([f'''
          <div class="flash-option-item" data-correct="{'true' if opt['correct'] else 'false'}" data-explanation="{opt['explanation']}">
            <span class="flash-option-marker"></span>
            <span class="flash-option-text">{opt['text']}</span>
          </div>
          ''' for opt in lesson["quiz"]["options"]])}
        </div>
        <div class="flash-feedback-box"></div>
      </div>
    </section>

    <!-- Navegação de Rodapé entre Lições -->
    <footer class="lesson-footer">
      <div>{prev_link}</div>
      <div class="lesson-footer-counter">Lição {lid} de 0015</div>
      <div>{next_link}</div>
    </footer>
  </article>

  <!-- Sticky Audio Player com Narração Neural PT-BR -->
  <aside class="sticky-audio-bar" id="sticky-audio-bar">
    <audio id="lesson-audio" preload="auto">
      <source src="../assets/audio/lesson-{lid}-pt.mp3" type="audio/mpeg">
    </audio>
    <div class="audio-info">
      <span class="audio-icon">🎧</span>
      <div>
        <p class="audio-text-title">Narração da Lição {lid}</p>
        <p class="audio-text-sub">Áudio Neural PT-BR • Pronúncia Técnica Databricks (Kokoro 82M)</p>
      </div>
    </div>
    <div class="audio-controls">
      <button class="audio-btn audio-btn-play" id="btn-audio-play" title="Reproduzir / Pausar Áudio">▶</button>
      <div class="audio-progress-bar" id="audio-progress-bar">
        <div class="audio-progress-fill" id="audio-progress-fill"></div>
      </div>
      <span class="audio-time"><span id="audio-time-current">00:00</span> / <span id="audio-time-total">00:00</span></span>
      <button class="audio-speed-btn" id="btn-audio-speed" title="Velocidade de Reprodução">1x</button>
    </div>
    <div class="audio-actions">
      <button type="button" class="audio-tool-btn" id="btn-audio-pin" title="Alternar entre barra fixa na base ou embutida no final da página">
        <span class="pin-icon">📌</span>
        <span class="pin-label">Fixado</span>
      </button>
      <button type="button" class="audio-tool-btn audio-btn-close" id="btn-audio-hide" title="Ocultar Tocador de Áudio (recolher para pílula flutuante)">
        <span>▼</span>
        <span class="hide-label">Ocultar</span>
      </button>
    </div>
  </aside>

  <!-- Pílula Flutuante Discreta para Reabrir o Player quando Oculto -->
  <button type="button" class="audio-reopen-pill" id="btn-audio-reopen" title="Expandir Tocador de Áudio da Lição" style="display: none;">
    <span class="pill-icon">🎧</span>
    <span class="pill-label">Áudio {lid}</span>
    <span class="pill-play-state" id="pill-play-state">▶</span>
  </button>

</body>
</html>
'''
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content.strip() + "\n")
        print(f"✓ Lição {lid} atualizada no padrão Microsoft Learn: {file_path}")

    # Gera arquivos Markdown dedicados em labs/ para estudo e download rápido
    for lid, lab in LABS_STEPS.items():
        md_path = os.path.join("labs", f"LAB-{lid}.md")
        md_content = f"""# {lab['title']}

> **⚠️ PRÉ-REQUISITO OBRIGATÓRIO DA AZURE (Microsoft Learn Standards):**
> Para realizar este laboratório prático, **você precisará de um Workspace do Azure Databricks alocado na sua assinatura do Microsoft Azure** (Recomendado tier Premium para suporte a Unity Catalog e Serverless Compute).
> **Pré-requisitos Técnicos:** {lab['azure_prereq']}

- **Duração Estimada:** {lab['duration']}
- **Cenário:** {lab['scenario']}

---

"""
        for task in lab['tasks']:
            md_content += f"## Tarefa {task['num']}: {task['title']}\n\n"
            md_content += f"{task['instructions']}\n\n"
            if "code" in task:
                md_content += f"```python\n{task['code'].strip()}\n```\n\n"
            if "expected_output" in task:
                md_content += f"**Saída Esperada:**\n```text\n{task['expected_output'].strip()}\n```\n\n"
            md_content += "---\n\n"

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content.strip() + "\n")
        print(f"✓ Guia Markdown do Lab gerado: {md_path}")

if __name__ == "__main__":
    main()
