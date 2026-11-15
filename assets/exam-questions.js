/**
 * Databricks Formation — Prepare to DP-750
 * Banco Massivo Oficial de Questões (+180Q) e Estudos de Caso Split-Screen
 * Exame Microsoft DP-750: Implementing Data Engineering Solutions Using Azure Databricks
 */

const CASE_STUDIES = [
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
];

const EXAM_QUESTIONS = [
  {
    "id": 1,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Uma organização financeira precisa implantar um Workspace do Azure Databricks com conformidade de segurança bancária. A equipe de infraestrutura de nuvem exige o uso de VNet Injection em uma Virtual Network existente gerenciada pela empresa. Quais são os requisitos obrigatórios para as subnets dessa VNet?",
    "options": [
      {
        "id": "A",
        "text": "Configurar exatamente duas subnets dedicadas (host/public e container/private), com tamanho mínimo /26 cada, delegadas para Microsoft.Databricks/workspaces sem outros recursos alocados nelas.",
        "correct": true,
        "explanation": "Correto. O VNet Injection no Azure Databricks exige exatamente duas subnets exclusivas delegadas para o provedor Microsoft.Databricks/workspaces, cada uma com máscara mínima /26."
      },
      {
        "id": "B",
        "text": "Configurar uma única subnet compartilhada /24 compartilhada entre o cluster Databricks, Azure App Services e gateways de aplicação.",
        "correct": false,
        "explanation": "Incorreto. O Databricks não suporta compartilhamento de subnet com outros serviços devido à deleção e gerenciamento de IPs pelo serviço."
      },
      {
        "id": "C",
        "text": "Configurar quatro subnets /28 independentes para separar Driver, Workers, Storage DBFS e balanceador de carga.",
        "correct": false,
        "explanation": "Incorreto. O requisito oficial são duas subnets (host e container) com tamanho mínimo /26."
      },
      {
        "id": "D",
        "text": "Provisionar subnets sem nenhuma deleção de serviço e gerenciar manualmente todas as rotas BGP da VNet.",
        "correct": false,
        "explanation": "Incorreto. A delegação de serviço para Microsoft.Databricks/workspaces é mandatória para que o Azure provisione os recursos de rede do Compute Plane."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "No Azure Databricks, a VNet Injection exige duas subnets dedicadas: uma pública (host) e uma privada (container). Cada subnet deve ter no mínimo uma máscara /26 (fornecendo 64 IPs, sendo 5 reservados pelo Azure, suportando até 59 nós) e estar delegada exclusivamente para 'Microsoft.Databricks/workspaces'."
  },
  {
    "id": 2,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "A equipe de segurança de redes de uma empresa farmacêutica configurou um Network Security Group (NSG) corporativo para as subnets de um Workspace Azure Databricks com VNet Injection. Após a aplicação, os clusters falham ao iniciar com erro de timeout de conectividade. Qual regra de saída (outbound) do NSG é indispensável para a comunicação segura com o Control Plane?",
    "options": [
      {
        "id": "A",
        "text": "Abrir portas de entrada (inbound) TCP 22 e TCP 8080 públicas para permitir que o Control Plane envie comandos aos nós.",
        "correct": false,
        "explanation": "Incorreto. O Databricks moderno opera com Secure Cluster Connectivity (No Public IP), não exigindo portas de entrada públicas abertas."
      },
      {
        "id": "B",
        "text": "Permitir tráfego de saída (outbound) na porta TCP 443 em direção à tag de serviço do Azure Databricks (AzureDatabricks) ou endereço do Control Plane.",
        "correct": true,
        "explanation": "Correto. A Secure Cluster Connectivity (SCC) utiliza conexões de saída TLS na porta 443 para estabelecer o túnel relay seguro entre o Compute Plane e o Control Plane."
      },
      {
        "id": "C",
        "text": "Habilitar roteamento BGP na porta 1521 para comunicação com o metastore gerenciado.",
        "correct": false,
        "explanation": "Incorreto. A porta 1521 é típica de bancos Oracle e não se aplica à conexão entre planos do Databricks."
      },
      {
        "id": "D",
        "text": "Desabilitar todas as regras de saída e forçar tráfego exclusivamente através de um proxy HTTP sem suporte a WebSockets.",
        "correct": false,
        "explanation": "Incorreto. O Control Plane exige conexões HTTPS/WebSockets sem interceptação com quebra de SSL não suportada."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "No modelo Secure Cluster Connectivity (NPIP), os nós do cluster iniciam conexões de saída na porta 443 para o Control Plane. Se o NSG bloquear a saída HTTPS para a tag de serviço AzureDatabricks ou Storage, os nós não conseguirão se registrar no cluster manager."
  },
  {
    "id": 3,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": "case-04",
    "question": "Uma multinacional quer impedir que o tráfego de usuários navegando na Web UI do Azure Databricks trafegue pela internet pública. Qual funcionalidade do Azure deve ser implementada para garantir acesso estritamente privado ao front-end do workspace a partir da rede corporativa ExpressRoute?",
    "options": [
      {
        "id": "A",
        "text": "Habilitar o Azure Bastion diretamente dentro da máquina virtual do Driver do Spark.",
        "correct": false,
        "explanation": "Incorreto. O Azure Bastion é utilizado para RDP/SSH em VMs individuais, não para conectar usuários à interface web gerenciada do Databricks."
      },
      {
        "id": "B",
        "text": "Configurar uma VPN ponto-a-site ligada diretamente ao storage DBFS raiz.",
        "correct": false,
        "explanation": "Incorreto. O storage DBFS raiz armazena bibliotecas e metadados, mas não hospeda a interface web do workspace."
      },
      {
        "id": "C",
        "text": "Implementar um Azure Private Link com Private Endpoint do tipo Front-end (Web UI & REST API) associado à VNet corporativa.",
        "correct": true,
        "explanation": "Correto. O Front-end Private Link conecta o cliente (navegadores de usuários e chamadas de API) ao Control Plane do Databricks através de um IP privado da VNet."
      },
      {
        "id": "D",
        "text": "Criar um Application Gateway público apontando para o endereço IP público dos nós de computação.",
        "correct": false,
        "explanation": "Incorreto. Os nós de computação não possuem IPs públicos quando SCC está habilitado, e a Web UI reside no Control Plane."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "O Azure Databricks suporta dois tipos de Private Link: Front-end (para tráfego de usuários/APIs até a Web UI no Control Plane) e Back-end (para tráfego dos nós de computação até o Control Plane). Para tráfego de usuários corporativos, o Front-end Private Link é o recurso requerido."
  },
  {
    "id": 4,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Ao configurar Azure Private Link Front-end para um workspace em uma região do Azure, a documentação exige a criação de um workspace especial auxiliar chamado WebAuth Workspace. Qual é a finalidade técnica desse workspace auxiliar?",
    "options": [
      {
        "id": "A",
        "text": "Armazenar todos os arquivos Parquet temporários gerados por queries analíticas de usuários.",
        "correct": false,
        "explanation": "Incorreto. O workspace de WebAuth não armazena dados de negócio nem executa clusters de processamento."
      },
      {
        "id": "B",
        "text": "Substituir o Metastore regional do Unity Catalog para workspaces governados.",
        "correct": false,
        "explanation": "Incorreto. O Unity Catalog possui metastore independente e não se relaciona com o WebAuth workspace."
      },
      {
        "id": "C",
        "text": "Executar os nós executores do Apache Spark em modo isolado multi-inquilino.",
        "correct": false,
        "explanation": "Incorreto. O WebAuth workspace é puramente voltado à autenticação web via rede privada."
      },
      {
        "id": "D",
        "text": "Atuar como ponto de terminação e callback para o fluxo de autenticação OAuth com o Microsoft Entra ID via rede privada.",
        "correct": true,
        "explanation": "Correto. O WebAuth Workspace hospeda o endpoint de callback de autenticação privada do Microsoft Entra ID para que os usuários consigam logar via Private Link."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "No Azure Databricks com Front-end Private Link, o fluxo de login do Microsoft Entra ID (Azure AD) precisa redirecionar o usuário para uma URL segura resolvida na rede privada. O WebAuth workspace é provisionado uma única vez por região para prover esse endpoint privado de autenticação."
  },
  {
    "id": 5,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Um arquiteto de FinOps precisa restringir os desenvolvedores para que só possam criar clusters utilizando máquinas virtuais econômicas de uso geral (Standard_D4ds_v5) e impedir a alocação de nós caros com GPU ou excesso de memória. Qual recurso do Databricks atende a esse controle?",
    "options": [
      {
        "id": "A",
        "text": "Criar uma Cluster Policy no Databricks definindo uma allowlist para o atributo 'node_type_id' contendo apenas 'Standard_D4ds_v5'.",
        "correct": true,
        "explanation": "Correto. Cluster Policies permitem impor regras estritas em formato JSON com allowlist, blocklist ou valores fixos para tipos de nós, versões de DBR e autotermination."
      },
      {
        "id": "B",
        "text": "Criar um script em Python no notebook que verifica o tipo da VM e executa dbutils.fs.rm() se for GPU.",
        "correct": false,
        "explanation": "Incorreto. O script só rodaria após o cluster já ter sido iniciado e gerado cobrança no Azure."
      },
      {
        "id": "C",
        "text": "Excluir as cotas de VM de GPU em toda a assinatura do Azure Subscription.",
        "correct": false,
        "explanation": "Incorreto. Isso impactaria outros serviços de inteligência artificial da empresa fora do Databricks."
      },
      {
        "id": "D",
        "text": "Configurar uma regra de firewall no NSG bloqueando portas de comunicação da GPU.",
        "correct": false,
        "explanation": "Incorreto. O NSG atua na camada de rede TCP/IP, não controlando tipos de instâncias de hardware alocadas."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "As Cluster Policies são o mecanismo oficial de governança e FinOps no Databricks. Através do JSON de política, os administradores definem 'node_type_id': {'type': 'allowlist', 'values': ['Standard_D4ds_v5']}, restringindo a criação de clusters fora da política."
  },
  {
    "id": 6,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": "case-07",
    "question": "A equipe de governança detectou que desenvolvedores deixam clusters interativos All-Purpose ativos durante a noite e fins de semana, inflando a fatura de DBUs. Qual configuração de Cluster Policy garante que nenhum cluster interativo permaneça ocioso por mais de 20 minutos?",
    "options": [
      {
        "id": "A",
        "text": "Instalar um job no Azure Data Factory que envia um comando de kill a cada 24 horas.",
        "correct": false,
        "explanation": "Incorreto. Um job diário ainda permitiria horas desnecessárias de ociosidade contínua."
      },
      {
        "id": "B",
        "text": "Definir o atributo 'autotermination_minutes' na Cluster Policy com valor fixo ou valor máximo de 20 minutos.",
        "correct": true,
        "explanation": "Correto. Impor 'autotermination_minutes': {'type': 'fixed', 'value': 20} ou {'type': 'range', 'maxValue': 20} impede que o usuário desmarque ou aumente o tempo de inatividade."
      },
      {
        "id": "C",
        "text": "Configurar a propriedade 'spark.scheduler.mode' para 'FAIR' nas configurações do Spark.",
        "correct": false,
        "explanation": "Incorreto. O Fair Scheduler gerencia concorrência de queries dentro do cluster, não desligamento de VM."
      },
      {
        "id": "D",
        "text": "Configurar o driver do Spark com memória de 2 GB para provocar OutOfMemory e derrubar o nó.",
        "correct": false,
        "explanation": "Incorreto. Forçar falhas de memória corrompe o desenvolvimento e é uma péssima prática de engenharia."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "O atributo 'autotermination_minutes' em Cluster Policies força o encerramento automático após o período estipulado de inatividade, sendo a principal medida de FinOps contra custos fantasmas de All-Purpose clusters."
  },
  {
    "id": 7,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Uma organização precisa ratear os custos de DBUs e de VMs de cada cluster Databricks entre 5 centros de custo distintos da empresa. Qual estratégia garante que todo cluster criado contenha obrigatoriamente a tag 'CostCenter' preenchida de acordo com uma lista aprovada?",
    "options": [
      {
        "id": "A",
        "text": "Criar uma tabela Delta no Hive Metastore e pedir aos desenvolvedores que insiram manualmente os valores.",
        "correct": false,
        "explanation": "Incorreto. Não impede a criação de clusters desgovernados nem integra automaticamente com o faturamento do Azure."
      },
      {
        "id": "B",
        "text": "Exigir que todos os notebooks comecem com a variável Python cost_center = 'RH'.",
        "correct": false,
        "explanation": "Incorreto. Variáveis de notebook não são propagadas para os metadados de cobrança do Azure e Databricks."
      },
      {
        "id": "C",
        "text": "Definir na Cluster Policy uma regra obrigatória para 'custom_tags.CostCenter' utilizando o operador 'allowlist' com os códigos dos centros de custo.",
        "correct": true,
        "explanation": "Correto. Cluster Policies permitem governar 'custom_tags.<tag_name>', tornando o preenchimento obrigatório e restrito a uma lista de valores permitidos."
      },
      {
        "id": "D",
        "text": "Configurar um alerta no Azure Monitor que envia um e-mail diário com os clusters sem tags.",
        "correct": false,
        "explanation": "Incorreto. É reativo e não impede a criação de recursos fora da conformidade."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "Tags customizadas governadas por Cluster Policies são propagadas automaticamente para as instâncias de VMs no Azure e para a tabela de faturamento system.billing.usage, permitindo rateio contábil exato."
  },
  {
    "id": 8,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Analistas juniores de uma equipe de dados precisam realizar análises exploratórias em arquivos CSV de pequeno porte utilizando Pandas e PySpark básico. Para economizar custos, a gerência exige que esses analistas utilizem clusters compostos por uma única máquina virtual, sem nós workers. Qual configuração deve ser aplicada?",
    "options": [
      {
        "id": "A",
        "text": "Configurar um cluster Standard com 10 workers e desabilitar o nó Driver.",
        "correct": false,
        "explanation": "Incorreto. O Spark não pode operar sem um nó Driver ativo."
      },
      {
        "id": "B",
        "text": "Utilizar um Serverless SQL Warehouse de tamanho 4X-Large.",
        "correct": false,
        "explanation": "Incorreto. 4X-Large aloca dezenas de instâncias e geraria um custo desproporcional para análises leves."
      },
      {
        "id": "C",
        "text": "Executar o código dentro de uma Azure Function sem nenhum runtime Spark.",
        "correct": false,
        "explanation": "Incorreto. A questão exige exploração de dados no Databricks com suporte a PySpark."
      },
      {
        "id": "D",
        "text": "Configurar um cluster Single-Node (definindo spark.databricks.cluster.profile como 'singleNode' e num_workers = 0).",
        "correct": true,
        "explanation": "Correto. Clusters Single-Node operam com 1 única VM executando tanto o Driver quanto os slots locais de execução, eliminando o custo de VMs workers adicionais."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "Clusters Single-Node são a escolha ideal de FinOps para workloads leves, bibliotecas não distribuídas (Pandas, Scikit-learn) ou aprendizado inicial, pois cobram apenas por 1 nó e eliminam sobrecarga de rede."
  },
  {
    "id": 9,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": "case-02",
    "question": "Uma equipe precisa acelerar a inicialização de clusters de desenvolvimento de 6 minutos para menos de 30 segundos, pois os engenheiros iniciam e encerram ambientes frequentemente durante o expediente. Qual funcionalidade do Azure Databricks resolve este gargalo?",
    "options": [
      {
        "id": "A",
        "text": "Criar um Databricks Instance Pool com um número mínimo de instâncias ociosas prontas (Min Idle Instances).",
        "correct": true,
        "explanation": "Correto. Instance Pools mantêm um conjunto de VMs pré-alocadas no Compute Plane prontas para uso, reduzindo o tempo de boot de minutos para segundos."
      },
      {
        "id": "B",
        "text": "Aumentar o tempo de autotermination para 480 minutos em todos os clusters.",
        "correct": false,
        "explanation": "Incorreto. Isso geraria custos abusivos de DBUs e VMs sem resolver o tempo de inicialização a frio."
      },
      {
        "id": "C",
        "text": "Executar todos os comandos em notebooks conectados ao DBFS local via comando %fs.",
        "correct": false,
        "explanation": "Incorreto. O comando %fs é apenas um utilitário de navegação de arquivos e não executa código distribuído."
      },
      {
        "id": "D",
        "text": "Desabilitar o Photon Engine e forçar compilação com Scala 2.11.",
        "correct": false,
        "explanation": "Incorreto. O Photon acelera a execução de queries, e o Scala 2.11 é uma versão legada obsoleta."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "Instance Pools mantêm instâncias de VMs pré-provisionadas na assinatura do Azure. Quando um cluster solicita um nó, a VM já está quente e anexada em segundos. Enquanto ociosa no pool, não há cobrança de DBUs (apenas o custo de infraestrutura de VM da Azure)."
  },
  {
    "id": 10,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "A gerência de TI questiona o custo de manter um Databricks Instance Pool com 4 instâncias ociosas prontas durante o horário comercial. Como é tarifado um nó que reside em um Instance Pool enquanto nenhum cluster está utilizando-o?",
    "options": [
      {
        "id": "A",
        "text": "O cliente paga a taxa máxima de DBUs de All-Purpose multiplicada pelo número de instâncias no pool.",
        "correct": false,
        "explanation": "Incorreto. Não há cobrança de DBUs de software Databricks para nós ociosos em pools."
      },
      {
        "id": "B",
        "text": "O cliente paga o custo normal de máquina virtual do Azure (IaaS), mas paga ZERO DBUs para a Databricks enquanto a instância estiver ociosa no pool.",
        "correct": true,
        "explanation": "Correto. Enquanto uma VM permanece ociosa no pool, ela consome apenas a tarifa da VM da Microsoft; as DBUs Databricks só começam a ser tarifadas no momento em que a VM é alocada para um cluster ativo."
      },
      {
        "id": "C",
        "text": "A cobrança é gratuita tanto na Azure quanto no Databricks durante o período ocioso.",
        "correct": false,
        "explanation": "Incorreto. A VM física alocada no Azure gera cobrança de infraestrutura de computação."
      },
      {
        "id": "D",
        "text": "O custo é cobrado integralmente em storage ADLS Gen2 em vez de computação.",
        "correct": false,
        "explanation": "Incorreto. O pool aloca VMs de computação, não espaço de armazenamento."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "Essa é uma das premissas fundamentais de FinOps no DP-750: Instâncias ociosas em Instance Pools cobram apenas custo de VM Azure à Microsoft e ZERO DBUs ao Databricks. As DBUs só são debitadas quando um cluster anexa a instância."
  },
  {
    "id": 11,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Uma equipe de analistas de Power BI realiza consultas ad-hoc e atualiza painéis executivos frequentemente. As consultas apresentam picos rápidos seguidos por períodos de inatividade. Qual recurso de computação oferece inicialização instantânea (sub-10s) e desligamento automático em até 1 minuto de ociosidade?",
    "options": [
      {
        "id": "A",
        "text": "All-Purpose Cluster com 10 nós e autotermination de 120 minutos.",
        "correct": false,
        "explanation": "Incorreto. Demora 4 a 6 minutos para iniciar e 120 minutos de inatividade geraria enorme desperdício."
      },
      {
        "id": "B",
        "text": "Single-Node cluster com Databricks Runtime for Machine Learning.",
        "correct": false,
        "explanation": "Incorreto. Clusters ML são voltados a treino de modelos e não possuem as otimizações analíticas SQL do warehouse."
      },
      {
        "id": "C",
        "text": "Serverless SQL Warehouse.",
        "correct": true,
        "explanation": "Correto. O Serverless SQL Warehouse aloca computação instantânea no plano serverless da Databricks, escala dinamicamente e desliga automaticamente em 1 a 5 minutos de inatividade."
      },
      {
        "id": "D",
        "text": "Job Cluster efêmero configurado para rodar a cada 30 segundos.",
        "correct": false,
        "explanation": "Incorreto. Jobs efêmeros clássicos têm latência de startup de VM e não atendem a queries interativas de Power BI."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "Serverless SQL Warehouses são a opção recomendada pela Microsoft para BI e relatórios ad-hoc, pois oferecem o menor tempo de inicialização (segundos), escalabilidade elástica e desligamento ultrarrápido (1 minuto)."
  },
  {
    "id": 12,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": "case-05",
    "question": "Em um Serverless SQL Warehouse com autoscaling habilitado, a demanda de consultas cresceu repentinamente devido a 200 analistas acessando simultaneamente um dashboard. O warehouse começou a enfileirar queries. Como a política de escalonamento gerencia clusters adicionais?",
    "options": [
      {
        "id": "A",
        "text": "O warehouse reinicia o cluster principal e aumenta a memória RAM da máquina virtual Driver.",
        "correct": false,
        "explanation": "Incorreto. Clusters de SQL Warehouse não reiniciam nem alteram hardware verticalmente sob carga."
      },
      {
        "id": "B",
        "text": "As consultas excedentes são canceladas automaticamente e retornam código de erro HTTP 429.",
        "correct": false,
        "explanation": "Incorreto. O warehouse enfileira as consultas e escala nós adicionais horizontalmente."
      },
      {
        "id": "C",
        "text": "O warehouse transfere a execução para um cluster All-Purpose do usuário.",
        "correct": false,
        "explanation": "Incorreto. Não há transferência cruzada de carga para clusters de notebooks de usuários."
      },
      {
        "id": "D",
        "text": "O Databricks adiciona clusters de computação adicionais quase instantaneamente para esvaziar a fila de espera quando o tempo estimado de fila ultrapassa o limiar.",
        "correct": true,
        "explanation": "Correto. A política de autoscaling de SQL Warehouses monitora a fila de queries e sobe novos clusters de mesmo tamanho em segundos para manter a concorrência sem gargalos."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "SQL Warehouses escalam horizontalmente adicionando novos clusters do mesmo tamanho (ex: de 1 cluster 'Medium' para 2 ou 3 clusters 'Medium') com base na profundidade da fila de consultas."
  },
  {
    "id": 13,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Um engenheiro de dados precisa integrar um pipeline PySpark a uma base de dados externa utilizando uma senha de banco e um token de API. A política de conformidade proíbe rigorosamente o armazenamento de credenciais em texto claro dentro de notebooks ou scripts Git. Qual é o procedimento oficial?",
    "options": [
      {
        "id": "A",
        "text": "Criar um Secret Scope com backend no Azure Key Vault e ler as credenciais no notebook via dbutils.secrets.get(scope='...', key='...').",
        "correct": true,
        "explanation": "Correto. O Azure Key Vault-backed Secret Scope sincroniza com os segredos do Key Vault e permite recuperação em memória com redação automática de saída."
      },
      {
        "id": "B",
        "text": "Gravar as credenciais em um arquivo .txt armazenado na pasta /dbfs/FileStore/ e ler com open().",
        "correct": false,
        "explanation": "Incorreto. Arquivos no DBFS raiz são inseguros e legíveis por qualquer usuário com acesso ao workspace."
      },
      {
        "id": "C",
        "text": "Passar a senha diretamente como argumento de linha de comando no job agendado.",
        "correct": false,
        "explanation": "Incorreto. Parâmetros de jobs ficam expostos na UI de execução e no histórico do workspace."
      },
      {
        "id": "D",
        "text": "Codificar a senha em Base64 e salvar como uma constante estática no repositório Git.",
        "correct": false,
        "explanation": "Incorreto. Base64 é apenas codificação reversível e não protege segredos corporativos."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "O Azure Key Vault-backed Secret Scope é o padrão do DP-750 para gestão de segredos. Permite recuperar valores dinamicamente via dbutils.secrets.get(), garantindo que os valores sejam automaticamente mascarados ([REDACTED]) em logs e outputs."
  },
  {
    "id": 14,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Qual comando da Databricks CLI cria corretamente um Secret Scope integrado a um Azure Key Vault chamado 'akv-corp-prod'?",
    "options": [
      {
        "id": "A",
        "text": "databricks secrets put --scope corp-secrets --key akv-corp-prod --value AZURE_VAULT",
        "correct": false,
        "explanation": "Incorreto. O comando put armazena um segredo individual em escopo interno Databricks, não cria escopo integrado ao Azure Key Vault."
      },
      {
        "id": "B",
        "text": "databricks secrets create-scope --scope corp-secrets --scope-backend-type AZURE_KEYVAULT --resource-id <vault-id> --dns-name https://akv-corp-prod.vault.azure.net/",
        "correct": true,
        "explanation": "Correto. Essa é a sintaxe exata da Databricks CLI para vincular um escopo ao Key Vault informando o resource-id e dns-name."
      },
      {
        "id": "C",
        "text": "az databricks workspace link-keyvault --workspace-name myws --keyvault akv-corp-prod",
        "correct": false,
        "explanation": "Incorreto. Comando inexistente na Azure CLI."
      },
      {
        "id": "D",
        "text": "databricks keyvault mount --path /mnt/secrets --dns https://akv-corp-prod.vault.azure.net/",
        "correct": false,
        "explanation": "Incorreto. Não se monta Key Vault como sistema de arquivos via DBFS."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "A criação de Secret Scopes respaldados pelo Azure Key Vault é efetuada via Databricks CLI com `--scope-backend-type AZURE_KEYVAULT`, passando o Resource ID da Azure e a URI DNS do cofre."
  },
  {
    "id": 15,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": "case-08",
    "question": "Um desenvolvedor executa o seguinte comando em uma célula de notebook: print(dbutils.secrets.get(scope='financas', key='db_password')). Qual será o valor exibido na saída do notebook?",
    "options": [
      {
        "id": "A",
        "text": "A senha do banco em texto claro.",
        "correct": false,
        "explanation": "Incorreto. O Databricks impede que segredos recuperados por dbutils.secrets sejam vazados no stdout do notebook."
      },
      {
        "id": "B",
        "text": "Uma mensagem de erro de compilação Python.",
        "correct": false,
        "explanation": "Incorreto. O comando é válido e a execução conclui com sucesso, porém o output é redigido."
      },
      {
        "id": "C",
        "text": "[REDACTED]",
        "correct": true,
        "explanation": "Correto. O Azure Databricks possui proteção ativa de Secret Redaction que intercepta a saída e substitui valores lidos via dbutils.secrets por [REDACTED]."
      },
      {
        "id": "D",
        "text": "O hash SHA-256 da senha.",
        "correct": false,
        "explanation": "Incorreto. A plataforma exibe explicitamente a string literal [REDACTED]."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "O Secret Redaction é um recurso de segurança nativo do Databricks: qualquer segredo obtido através de `dbutils.secrets.get` é mascarado automaticamente com `[REDACTED]` se for enviado para o fluxo de saída padrão do notebook."
  },
  {
    "id": 16,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Uma organização precisa executar pipelines de produção em Databricks Workflows sem depender de credenciais de usuários individuais que podem ser demitidos ou ter senhas expiradas. Qual identidade deve ser configurada para execução automatizada?",
    "options": [
      {
        "id": "A",
        "text": "Um Personal Access Token (PAT) gerado pelo usuário administrador do workspace.",
        "correct": false,
        "explanation": "Incorreto. PATs de usuários expiram e tornam os pipelines vulneráveis a desligamentos ou rotações de senha pessoais."
      },
      {
        "id": "B",
        "text": "A conta de root do primeiro desenvolvedor que provisionou o workspace.",
        "correct": false,
        "explanation": "Incorreto. Viola normas de segurança e auditoria corporativa."
      },
      {
        "id": "C",
        "text": "Um usuário convidado externo (Guest User) sem licença atribuída.",
        "correct": false,
        "explanation": "Incorreto. Contas de convidados têm restrições e não servem para governança de produção."
      },
      {
        "id": "D",
        "text": "Um Service Principal do Microsoft Entra ID gerenciado no Databricks Account Console com permissões federadas.",
        "correct": true,
        "explanation": "Correto. Service Principals são identidades gerenciadas sem usuário humano, ideais para CI/CD e execução autônoma de jobs em produção."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "O padrão corporativo oficial do DP-750 é a utilização de Service Principals do Microsoft Entra ID cadastrados no Account Console e associados aos Databricks Jobs."
  },
  {
    "id": 17,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "A equipe de segurança corporativa exige que os usuários e grupos definidos no Microsoft Entra ID da empresa sejam sincronizados automaticamente com o Databricks Account Console. Qual protocolo padrão de identidade deve ser configurado?",
    "options": [
      {
        "id": "A",
        "text": "Configurar sincronização SCIM (System for Cross-domain Identity Management) a partir do Microsoft Entra ID.",
        "correct": true,
        "explanation": "Correto. A integração SCIM entre o Entra ID e o Databricks Account Console automatiza a criação, atualização e revogação de usuários e grupos."
      },
      {
        "id": "B",
        "text": "Configurar um script de FTP que envia um arquivo CSV com as senhas para o /dbfs diariamente.",
        "correct": false,
        "explanation": "Incorreto. Extremamente inseguro e não integra identidades."
      },
      {
        "id": "C",
        "text": "Habilitar autenticação Kerberos diretamente em cada nó Worker do Spark.",
        "correct": false,
        "explanation": "Incorreto. O Databricks em nuvem utiliza OAuth e SCIM com Entra ID, não Kerberos tradicional on-premises."
      },
      {
        "id": "D",
        "text": "Criar os usuários manualmente um a um no painel de cada workspace regional.",
        "correct": false,
        "explanation": "Incorreto. Gestão manual não atende ao requisito de sincronização automática e gera erros operacionais."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "A sincronização SCIM no nível da Conta (Account-level SCIM) conecta o Microsoft Entra ID ao Databricks, garantindo provisionamento e desprovisionamento centralizado de identidades."
  },
  {
    "id": 18,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": "case-03",
    "question": "Um pipeline noturno consome 4 horas de processamento diário em um All-Purpose Cluster com 4 nós. Sabendo que o custo de DBU em All-Purpose é aproximadamente $0.55/DBU e em Job Cluster é aproximadamente $0.20/DBU, qual alteração arquitetural reduz imediatamente a fatura em mais de 50%?",
    "options": [
      {
        "id": "A",
        "text": "Aumentar o número de nós do cluster All-Purpose de 4 para 16 nós.",
        "correct": false,
        "explanation": "Incorreto. Aumentaria expressivamente o custo total de VMs e consumo de DBUs."
      },
      {
        "id": "B",
        "text": "Converter o pipeline para ser orquestrado via Databricks Workflow utilizando um Job Cluster efêmero.",
        "correct": true,
        "explanation": "Correto. Job Clusters cobram uma taxa de DBU significativamente menor do que All-Purpose Clusters e são destruídos imediatamente após o término."
      },
      {
        "id": "C",
        "text": "Manter o cluster All-Purpose ligado 24/7 sem rodar nenhum outro código.",
        "correct": false,
        "explanation": "Incorreto. Resultaria em cobrança contínua e desperdício de orçamento."
      },
      {
        "id": "D",
        "text": "Mudar o formato de armazenamento dos dados de Delta Lake para CSV.",
        "correct": false,
        "explanation": "Incorreto. CSV é lento, não possui otimizações e degradaria severamente a performance."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "All-Purpose Compute é destinado a notebooks interativos e possui a taxa de DBU mais cara. Job Compute possui a menor taxa de DBU por hora (até 60% mais econômica) e é o padrão exigido para pipelines agendados."
  },
  {
    "id": 19,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Um engenheiro de dados precisa executar um script diário de manutenção que realiza apenas chamadas à API REST externa para atualizar metadados em tabelas Delta. O processamento dura 3 minutos e não executa nenhum processamento distribuído. Qual tipo de cluster oferece o menor custo de infraestrutura?",
    "options": [
      {
        "id": "A",
        "text": "Cluster multi-nós com 8 workers acelerados por GPU.",
        "correct": false,
        "explanation": "Incorreto. Custo desnecessário para uma tarefa simples de API e metadados."
      },
      {
        "id": "B",
        "text": "Instance Pool com 20 nós reservadas 24 horas por dia.",
        "correct": false,
        "explanation": "Incorreto. Geraria custo fixo desnecessário de VMs ociosas."
      },
      {
        "id": "C",
        "text": "Single-Node cluster (1 único nó executando driver e executor local).",
        "correct": true,
        "explanation": "Correto. O modo Single-Node aloca apenas 1 VM no Azure, eliminando custos de nós workers para cargas não distribuídas."
      },
      {
        "id": "D",
        "text": "Cluster High Concurrency com isolamento de tabela legado.",
        "correct": false,
        "explanation": "Incorreto. Modo de alta concorrência legado não é recomendado e custa mais caro."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "Single-Node clusters são recomendados para tarefas de nó único (drivers-only, bibliotecas Python simples como requests, manutenção leve), economizando custo de instâncias adicionais."
  },
  {
    "id": 20,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Para onde o Azure Databricks pode enviar automaticamente os logs detalhados de diagnóstico e eventos de auditoria de segurança (login de usuários, criação de clusters, acesso a dados) gerados no workspace?",
    "options": [
      {
        "id": "A",
        "text": "Apenas para o disco rígido local da máquina física do administrador.",
        "correct": false,
        "explanation": "Incorreto. Logs corporativos de nuvem não são baixados para discos locais de administradores."
      },
      {
        "id": "B",
        "text": "Diretamente para um bucket S3 na Amazon Web Services sem passar pelo Azure.",
        "correct": false,
        "explanation": "Incorreto. O Azure Databricks envia diagnósticos nativamente para destinos suportados no Azure Monitor."
      },
      {
        "id": "C",
        "text": "Para o diretório temporário /tmp/logs de cada nó worker descartado.",
        "correct": false,
        "explanation": "Incorreto. O diretório /tmp é volátil e os dados seriam perdidos no desligamento do nó."
      },
      {
        "id": "D",
        "text": "Azure Log Analytics Workspace, Azure Storage Account ou Azure Event Hubs via Diagnostic Settings do recurso no portal Azure.",
        "correct": true,
        "explanation": "Correto. O Azure Databricks integra com o Azure Monitor Diagnostic Settings para exportar logs de auditoria e métricas corporativas."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "Diagnostic Settings no recurso do Azure Databricks permitem encaminhar categorias de log (como audit, clusters, workspace, accounts) para Log Analytics, Storage ou Event Hubs."
  },
  {
    "id": 21,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": "case-06",
    "question": "Uma empresa precisa garantir que o acesso ao Workspace do Azure Databricks seja permitido exclusivamente para requisições originadas dos IPs públicos de sua VPN corporativa e filiais autorizadas. Qual funcionalidade deve ser utilizada?",
    "options": [
      {
        "id": "A",
        "text": "Configurar IP Access Lists no Azure Databricks através da REST API ou do Account Console.",
        "correct": true,
        "explanation": "Correto. IP Access Lists permitem bloquear acessos não autorizados por IP público na camada da Web UI e REST API do workspace."
      },
      {
        "id": "B",
        "text": "Alterar o código Python de cada notebook adicionando um if request.ip == '...'.",
        "correct": false,
        "explanation": "Incorreto. O notebook só executa após o usuário já ter logado no workspace."
      },
      {
        "id": "C",
        "text": "Instalar um antivírus em cada máquina virtual worker do Spark.",
        "correct": false,
        "explanation": "Incorreto. Antivírus de VM não controla acesso HTTP à interface web gerenciada do Databricks."
      },
      {
        "id": "D",
        "text": "Bloquear a porta 443 no roteador de saída de todos os funcionários da empresa.",
        "correct": false,
        "explanation": "Incorreto. Bloquear a porta 443 impediria a navegação na internet de toda a empresa."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "IP Access Lists no Databricks fornecem listas de permissão (allowlist) e bloqueio (blocklist) para controlar quais endereços IP públicos podem acessar o workspace e suas APIs."
  },
  {
    "id": 22,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Init scripts legados armazenados em /dbfs/FileStore/ foram descontinuados para novos recursos de segurança no Databricks. Qual é o local recomendado e governado pelo Unity Catalog para armazenar e referenciar init scripts de cluster?",
    "options": [
      {
        "id": "A",
        "text": "Embutir o código do script dentro de um comentário na célula 1 do notebook.",
        "correct": false,
        "explanation": "Incorreto. Comentários de notebook não são executados na inicialização da máquina virtual do cluster."
      },
      {
        "id": "B",
        "text": "Armazenar o script em um Unity Catalog Volume e referenciá-lo pelo caminho /Volumes/catalog/schema/volume/script.sh.",
        "correct": true,
        "explanation": "Correto. Init scripts armazenados em Unity Catalog Volumes possuem governança de acesso RBAC e auditoria completa."
      },
      {
        "id": "C",
        "text": "Hospedar o script em um servidor HTTP público aberto na internet sem autenticação.",
        "correct": false,
        "explanation": "Incorreto. Violação grave de segurança que expõe o cluster a ataques de injeção de código."
      },
      {
        "id": "D",
        "text": "Gravar o script no registro de DNS do Azure Private Link.",
        "correct": false,
        "explanation": "Incorreto. DNS não armazena scripts executáveis shell."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "O Databricks descontinuou init scripts globais e legados em DBFS. A recomendação moderna é armazenar scripts de inicialização em Volumes do Unity Catalog ou como cluster-scoped scripts governados."
  },
  {
    "id": 23,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Em um cluster clássico do Azure Databricks, onde residem os dados de clientes e onde os nós workers executam suas tarefas?",
    "options": [
      {
        "id": "A",
        "text": "Os nós workers executam na assinatura da Microsoft e todos os dados de clientes são replicados para o Control Plane.",
        "correct": false,
        "explanation": "Incorreto. Dados de clientes nunca trafegam nem residem no Control Plane."
      },
      {
        "id": "B",
        "text": "Os dados residem exclusivamente na memória RAM dos computadores pessoais dos desenvolvedores.",
        "correct": false,
        "explanation": "Incorreto. O processamento é distribuído em nós na nuvem."
      },
      {
        "id": "C",
        "text": "Os nós workers executam na VNet do cliente (Compute Plane) e os dados de negócio residem no ADLS Gen2 do cliente; nenhum dado reside no Control Plane.",
        "correct": true,
        "explanation": "Correto. Esta é a regra de ouro de conformidade do Databricks: dados e computação do cliente residem na infraestrutura do cliente."
      },
      {
        "id": "D",
        "text": "Os dados são convertidos para tabelas MySQL locais em um container Docker único.",
        "correct": false,
        "explanation": "Incorreto. O Lakehouse utiliza Apache Spark, Delta Lake e ADLS Gen2."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "No Azure Databricks clássico, o Compute Plane reside na assinatura Azure do cliente. Os dados de negócio nunca residem no Control Plane, garantindo isolamento estrito e atendimento a regulamentações como LGPD, HIPAA e GDPR."
  },
  {
    "id": 24,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": "case-01",
    "question": "Um arquiteto de dados precisa configurar um cluster para um pipeline crítico de produção com SLA rígido que não pode sofrer nenhuma interrupção ou perda de nós por desalocação de infraestrutura da nuvem. Qual opção de tipo de instância deve ser selecionada?",
    "options": [
      {
        "id": "A",
        "text": "Utilizar instâncias Spot tanto para o Driver quanto para todos os Workers.",
        "correct": false,
        "explanation": "Incorreto. Se o Azure requisitar a VM Spot onde o Driver reside, o cluster inteiro falha imediatamente."
      },
      {
        "id": "B",
        "text": "Utilizar máquinas desligadas do tipo B-Series com CPU burstable variável.",
        "correct": false,
        "explanation": "Incorreto. B-Series têm desempenho imprevisível e não garantem SLAs críticos de engenharia."
      },
      {
        "id": "C",
        "text": "Executar sem Driver utilizando nós somente de armazenamento.",
        "correct": false,
        "explanation": "Incorreto. O Spark exige obrigatoriamente um nó Driver para orquestrar a execução."
      },
      {
        "id": "D",
        "text": "Utilizar instâncias On-Demand tanto para o nó Driver quanto para os nós Workers.",
        "correct": true,
        "explanation": "Correto. Instâncias On-Demand garantem que as VMs não serão preemptadas (desalocadas) pelo Azure, garantindo o SLA do pipeline."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "Embora nós Spot reduzam custos em até 80%, eles podem ser desalocados a qualquer momento pelo Azure. O nó Driver NUNCA deve ser Spot, e workloads de missão crítica com SLA rígido devem utilizar instâncias On-Demand."
  },
  {
    "id": 25,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Por que a Microsoft recomenda a seleção de versões Databricks Runtime com suporte de longo prazo (ex: DBR 15.4 LTS) para pipelines corporativos de produção?",
    "options": [
      {
        "id": "A",
        "text": "DBR LTS oferece suporte estendido por até 3 anos com patches de segurança e estabilidade garantida sem quebras de compatibilidade de APIs.",
        "correct": true,
        "explanation": "Correto. Versões LTS (Long-Term Support) fornecem estabilidade e suporte corporativo sem mudanças inesperadas de bibliotecas e dependências."
      },
      {
        "id": "B",
        "text": "Versões LTS são as únicas que suportam comandos SQL no Databricks.",
        "correct": false,
        "explanation": "Incorreto. Todas as versões suportam SQL."
      },
      {
        "id": "C",
        "text": "Versões LTS são 100% gratuitas e não cobram nenhuma taxa de DBU.",
        "correct": false,
        "explanation": "Incorreto. DBR LTS cobra tarifas normais de DBU conforme o tipo de computação."
      },
      {
        "id": "D",
        "text": "Versões LTS desabilitam o Catalyst Optimizer para evitar compilações lógicas.",
        "correct": false,
        "explanation": "Incorreto. O Catalyst Optimizer é parte fundamental do Apache Spark em todas as versões."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "Ambientes produtivos de missão crítica devem padronizar em Databricks Runtime (DBR) LTS para garantir janelas de suporte corporativo de múltiplos anos e correções contínuas de segurança."
  },
  {
    "id": 26,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Um engenheiro de dados precisa configurar parâmetros avançados de execução do Spark em um cluster. Onde essas configurações devem ser inseridas na interface do Databricks?",
    "options": [
      {
        "id": "A",
        "text": "Em uma planilha Excel compartilhada no SharePoint da equipe.",
        "correct": false,
        "explanation": "Incorreto. Não se integra ao runtime do Databricks."
      },
      {
        "id": "B",
        "text": "No campo 'Spark Config' dentro de 'Advanced Options' na página de configuração do cluster.",
        "correct": true,
        "explanation": "Correto. As opções avançadas do cluster permitem injetar propriedades do Spark (ex: spark.sql.shuffle.partitions) diretamente na inicialização."
      },
      {
        "id": "C",
        "text": "No arquivo hosts do computador do desenvolvedor.",
        "correct": false,
        "explanation": "Incorreto. Arquivo local do sistema operacional do cliente."
      },
      {
        "id": "D",
        "text": "Dentro de uma tag HTML &lt;meta&gt; na página do portal.",
        "correct": false,
        "explanation": "Incorreto. Não afeta a configuração do Apache Spark."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "As configurações globais do cluster Spark (como `spark.sql.adaptive.enabled` ou limites de broadcast) são definidas no painel 'Advanced Options' > 'Spark Config'."
  },
  {
    "id": 27,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": "case-04",
    "question": "Em um cluster que opera no modo de acesso 'Single User' associado ao Unity Catalog, quais linguagens de programação são suportadas para execução de código?",
    "options": [
      {
        "id": "A",
        "text": "Apenas SQL e proíbe qualquer execução de código em Python ou Scala.",
        "correct": false,
        "explanation": "Incorreto. SQL-only é típico de SQL Warehouses, não de clusters Single User."
      },
      {
        "id": "B",
        "text": "Apenas comandos assembly C++ para o Photon.",
        "correct": false,
        "explanation": "Incorreto. Desenvolvedores utilizam linguagens de alto nível."
      },
      {
        "id": "C",
        "text": "Python, SQL, Scala e R.",
        "correct": true,
        "explanation": "Correto. Clusters Single User suportam todas as quatro linguagens principais (Python, SQL, Scala e R) associadas à identidade do usuário."
      },
      {
        "id": "D",
        "text": "Apenas linguagem Bash shell sem acesso a DataFrames.",
        "correct": false,
        "explanation": "Incorreto. O Spark opera com DataFrames e linguagens nativas."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "No Unity Catalog, clusters no modo 'Single User' oferecem suporte total a Python, Scala, SQL e R para o usuário atribuído. Já clusters no modo 'Shared' suportam Python e SQL (com restrições de isolamento multi-usuário)."
  },
  {
    "id": 28,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Qual é a principal vantagem de adotar o Serverless Compute para Databricks Workflows (Serverless Jobs) em relação ao gerenciamento de clusters clássicos de jobs?",
    "options": [
      {
        "id": "A",
        "text": "Permite executar código sem utilizar nenhuma conexão de rede com a nuvem.",
        "correct": false,
        "explanation": "Incorreto. A nuvem e os recursos de rede são utilizados normalmente."
      },
      {
        "id": "B",
        "text": "Gera dados sem necessidade de conta de armazenamento no ADLS Gen2.",
        "correct": false,
        "explanation": "Incorreto. Os dados continuam sendo gravados no storage do cliente."
      },
      {
        "id": "C",
        "text": "Substitui completamente o uso do Unity Catalog por arquivos Parquet sem metadados.",
        "correct": false,
        "explanation": "Incorreto. O Serverless é totalmente integrado ao Unity Catalog."
      },
      {
        "id": "D",
        "text": "Eliminação do tempo de espera de provisionamento de VM (inicialização em segundos), sem gerenciamento de cotas de VMs na assinatura Azure e otimização automática de recursos.",
        "correct": true,
        "explanation": "Correto. O Serverless Jobs sobe em segundos, não consome cotas de VM da assinatura do cliente e elimina o trabalho de gerenciamento de infraestrutura de computação."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "Serverless Jobs oferecem computação elástica imediata, reduzem o TCO eliminando clusters ociosos e removem a complexidade de gerenciar limites de vCPUs no Azure Resource Manager."
  },
  {
    "id": 29,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Um arquiteto precisa auditar todos os gastos de computação da empresa no Databricks agrupados por centro de custo nos últimos 90 dias. Qual tabela de sistema do Unity Catalog deve ser consultada?",
    "options": [
      {
        "id": "A",
        "text": "system.billing.usage",
        "correct": true,
        "explanation": "Correto. A tabela do sistema system.billing.usage armazena o histórico completo de consumo de DBUs, SKUs, clusters, jobs e tags personalizadas."
      },
      {
        "id": "B",
        "text": "system.access.audit",
        "correct": false,
        "explanation": "Incorreto. Esta tabela registra eventos de auditoria de segurança (logins, permissões, leituras), não o faturamento financeiro de DBUs."
      },
      {
        "id": "C",
        "text": "system.lineage.table_lineage",
        "correct": false,
        "explanation": "Incorreto. Esta tabela registra linhagem de dados entre tabelas e colunas."
      },
      {
        "id": "D",
        "text": "system.information_schema.columns",
        "correct": false,
        "explanation": "Incorreto. Registra metadados de colunas de tabelas, não consumo de nuvem."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "A tabela `system.billing.usage` é a base oficial de FinOps no Databricks. Nela encontram-se as colunas `usage_quantity` (DBUs), `sku_name`, `usage_date` e `custom_tags`."
  },
  {
    "id": 30,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": "case-07",
    "question": "Qual é o principal risco arquitetural de armazenar dados corporativos de produção diretamente no DBFS raiz (FileStore ou /mnt) em vez de utilizar o Unity Catalog com External Locations?",
    "options": [
      {
        "id": "A",
        "text": "O DBFS raiz apaga automaticamente todos os arquivos a cada 24 horas.",
        "correct": false,
        "explanation": "Incorreto. O storage do DBFS é persistente, o risco reside na ausência de controle de acesso refinado."
      },
      {
        "id": "B",
        "text": "O DBFS raiz reside na conta de armazenamento gerenciada do workspace, não possui controle de acesso refinado (RBAC) do Unity Catalog e todos os usuários com acesso ao workspace podem ler ou sobrescrever os dados.",
        "correct": true,
        "explanation": "Correto. O DBFS raiz não suporta a governança fina do Unity Catalog e representa risco severo de vazamento ou corrupção de dados corporativos."
      },
      {
        "id": "C",
        "text": "O DBFS raiz não suporta o formato Parquet nem transações ACID.",
        "correct": false,
        "explanation": "Incorreto. O Delta Lake funciona no DBFS, mas sem a governança e segurança moderna do Unity Catalog."
      },
      {
        "id": "D",
        "text": "O DBFS raiz cobra 10x mais caro que o ADLS Gen2 por terabyte armazenado.",
        "correct": false,
        "explanation": "Incorreto. A cobrança de storage é do tipo Azure Storage padrão, o problema é de segurança e governança."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "O exame DP-750 desencoraja expressamente o uso de DBFS raiz para dados de negócio. Dados de produção devem residir em containers governados pelo Unity Catalog (External Locations ou Volumes)."
  },
  {
    "id": 31,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Ao configurar autoscaling em um cluster clássico de engenharia de dados, um desenvolvedor define min_workers = 2 e max_workers = 10. Como o Spark Runtime gerencia a alocação desses nós?",
    "options": [
      {
        "id": "A",
        "text": "O cluster inicia imediatamente com 10 nós e nunca diminui até ser desligado.",
        "correct": false,
        "explanation": "Incorreto. Isso seria dimensionamento fixo com 10 nós, não autoscaling."
      },
      {
        "id": "B",
        "text": "O cluster cria 10 nós Drivers e nenhum nó worker.",
        "correct": false,
        "explanation": "Incorreto. O cluster Spark possui exatamente 1 nó Driver."
      },
      {
        "id": "C",
        "text": "O cluster inicia com 2 nós workers e escala automaticamente até 10 nós conforme a carga de trabalho de estágios de shuffle e volume de partições pendentes, reduzindo novamente quando a carga diminui.",
        "correct": true,
        "explanation": "Correto. O autoscaling elástico do Databricks ajusta dinamicamente a quantidade de nós entre os limites mínimo e máximo com base nas métricas de execução das tarefas."
      },
      {
        "id": "D",
        "text": "O autoscaling apenas altera a velocidade da CPU de cada máquina sem adicionar nós.",
        "correct": false,
        "explanation": "Incorreto. O autoscaling no Databricks é horizontal (adiciona e remove VMs completas)."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "O Autoscaling do Azure Databricks avalia a fila de tarefas e o uso de recursos dos executores para alocar ou desalocar workers dinamicamente entre os limites min e max definidos."
  },
  {
    "id": 32,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Uma equipe precisa garantir que todos os clusters criados no workspace utilizem exclusivamente o runtime acelerado pelo Photon Engine. Qual configuração de Cluster Policy impõe essa exigência?",
    "options": [
      {
        "id": "A",
        "text": "Desinstalar o interpretador Python de todos os nós.",
        "correct": false,
        "explanation": "Incorreto. Inviabilizaria o uso de PySpark no cluster."
      },
      {
        "id": "B",
        "text": "Configurar a porta 8080 para bloquear tráfego de JVM.",
        "correct": false,
        "explanation": "Incorreto. A JVM é necessária para coordenação do cluster."
      },
      {
        "id": "C",
        "text": "Exigir que todas as consultas SQL comecem com a palavra-chave PHOTON_START.",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente."
      },
      {
        "id": "D",
        "text": "Definir uma regra para 'spark_version' com allowlist contendo apenas versões terminadas com '-photon-' (ex: '*photon*').",
        "correct": true,
        "explanation": "Correto. Ao filtrar 'spark_version' para aceitar apenas strings contendo 'photon', os desenvolvedores são impedidos de criar clusters sem o motor Photon C++."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "Em Cluster Policies, regexes ou padrões com wildcard podem ser usados no atributo `spark_version` (ex: `{\"type\": \"pattern\", \"pattern\": \".*photon.*\"}`) para forçar clusters acelerados por Photon."
  },
  {
    "id": 33,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": "case-02",
    "question": "Como o Secure Cluster Connectivity (No Public IP) protege a infraestrutura de computação contra invasões e varreduras de portas vindas da internet pública?",
    "options": [
      {
        "id": "A",
        "text": "Nenhum nó de computação (Driver ou Worker) possui endereço IP público alocado e nenhuma porta de entrada (inbound) precisa ser aberta no NSG corporativo.",
        "correct": true,
        "explanation": "Correto. O modelo NPIP garante isolamento total contra varreduras de rede da internet pública, utilizando apenas conexões TLS de saída para o Control Plane."
      },
      {
        "id": "B",
        "text": "Utilizando criptografia quântica nos cabos submarinos do Azure.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      },
      {
        "id": "C",
        "text": "Exigindo que cada nó worker altere seu endereço MAC a cada 5 segundos.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      },
      {
        "id": "D",
        "text": "Bloqueando todos os pacotes TCP e permitindo apenas tráfego UDP sem confirmação.",
        "correct": false,
        "explanation": "Incorreto. O Spark e a Web utilizam TCP/HTTPS."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "Secure Cluster Connectivity (NPIP) é a configuração padrão de segurança de rede do Azure Databricks: zero IPs públicos nos nós de computação e zero regras de entrada abertas no NSG."
  },
  {
    "id": 34,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Um desenvolvedor precisa clonar um repositório corporativo do GitHub/Azure Repos diretamente no Azure Databricks para editar código e criar branches de desenvolvimento. Qual recurso integrado do workspace provê essa funcionalidade?",
    "options": [
      {
        "id": "A",
        "text": "DBFS FileStore.",
        "correct": false,
        "explanation": "Incorreto. FileStore é apenas uma pasta do DBFS para upload de arquivos estáticos."
      },
      {
        "id": "B",
        "text": "Databricks Git Folders (anteriormente conhecido como Databricks Repos).",
        "correct": true,
        "explanation": "Correto. Git Folders provê integração nativa com Git (GitHub, GitLab, Azure Repos, Bitbucket) diretamente dentro do workspace."
      },
      {
        "id": "C",
        "text": "Azure Key Vault Secret Scopes.",
        "correct": false,
        "explanation": "Incorreto. Key Vault gerencia segredos e senhas, não controle de versão Git."
      },
      {
        "id": "D",
        "text": "Databricks Pools.",
        "correct": false,
        "explanation": "Incorreto. Pools gerenciam VMs ociosas de computação."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "Databricks Git Folders oferece controle de versão completo com suporte a branching, pull requests, commits e sincronização bidirecional com repositórios Git corporativos."
  },
  {
    "id": 35,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Uma organização multinacional possui 3 workspaces do Azure Databricks na região East US 2 (Dev, Staging e Prod). Como deve ser desenhada a governança do Unity Catalog para essa topologia?",
    "options": [
      {
        "id": "A",
        "text": "Criar um Metastore separado para cada workspace e sincronizar via cópia diária de arquivos JSON.",
        "correct": false,
        "explanation": "Incorreto. Metastores separados fragmentam a linhagem e impedem governança e compartilhamento unificados."
      },
      {
        "id": "B",
        "text": "Não utilizar nenhum Metastore e voltar para o Hive Metastore legado.",
        "correct": false,
        "explanation": "Incorreto. O Hive Metastore não oferece governança unificada nem suporte a recursos modernos do DP-750."
      },
      {
        "id": "C",
        "text": "Criar exatamente um Metastore do Unity Catalog na região East US 2 e vinculá-lo aos três workspaces (Dev, Staging e Prod).",
        "correct": true,
        "explanation": "Correto. A melhor prática do Unity Catalog é ter um único Metastore por região geográfica, compartilhado entre múltiplos workspaces da mesma região para unificar governança e linhagem."
      },
      {
        "id": "D",
        "text": "Criar 10 metastores na região West US e conectar via VPN internacional.",
        "correct": false,
        "explanation": "Incorreto. O metastore deve estar na mesma região dos workspaces para evitar latência e custos de saída de rede."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "A recomendação da Microsoft para o DP-750 é ter um único Metastore do Unity Catalog por região, o qual é associado a todos os workspaces daquela região, viabilizando o 3-Level Namespace compartilhado."
  },
  {
    "id": 36,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": "case-05",
    "question": "Em um ambiente com múltiplos workspaces conectados ao mesmo Metastore do Unity Catalog, como os administradores garantem que os analistas do Workspace de Desenvolvimento (Dev) não consigam acessar nem consultar os dados do Catálogo de Produção (prod_catalog)?",
    "options": [
      {
        "id": "A",
        "text": "Desligar os roteadores da VNet do workspace de desenvolvimento.",
        "correct": false,
        "explanation": "Incorreto. Impediria todo o trabalho do ambiente de desenvolvimento."
      },
      {
        "id": "B",
        "text": "Excluir o catálogo de produção durante o expediente de desenvolvimento.",
        "correct": false,
        "explanation": "Incorreto. Destruiria o ambiente de produção."
      },
      {
        "id": "C",
        "text": "Alterar o nome do catálogo para que os desenvolvedores não descubram o nome.",
        "correct": false,
        "explanation": "Incorreto. 'Segurança por obscuridade' é uma péssima prática e não impede acessos."
      },
      {
        "id": "D",
        "text": "Configurar Catalog-Workspace Binding no Unity Catalog, vinculando o catálogo de produção exclusivamente ao workspace de Produção.",
        "correct": true,
        "explanation": "Correto. O Catalog-Workspace Binding restringe quais workspaces específicos têm permissão para acessar determinado catálogo no Metastore compartilhado."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "O recurso Catalog-Workspace Binding permite isolar catálogos por workspace, garantindo que catálogos de produção só sejam visíveis a partir de workspaces aprovados para produção."
  },
  {
    "id": 37,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Uma empresa precisa exportar métricas de execução do Spark e telemetria de seus clusters para o Azure Monitor e Application Insights. Qual biblioteca/ferramenta oficial é suportada para coletar métricas e encaminhá-las nativamente?",
    "options": [
      {
        "id": "A",
        "text": "Azure Databricks Monitoring Library (spark-monitoring) integrada com Log Analytics e Azure Monitor.",
        "correct": true,
        "explanation": "Correto. A biblioteca de monitoramento oficial da Microsoft para Databricks envia métricas do Spark e logs do log4j para o Azure Log Analytics Workspace."
      },
      {
        "id": "B",
        "text": "Instalar um servidor Apache Kafka dentro de cada nó worker para enviar mensagens.",
        "correct": false,
        "explanation": "Incorreto. Complexidade excessiva e alto custo operacional."
      },
      {
        "id": "C",
        "text": "Copiar manualmente os arquivos de log do Driver a cada 10 minutos via terminal SSH.",
        "correct": false,
        "explanation": "Incorreto. Processo manual e incompatível com ambientes modernos em nuvem."
      },
      {
        "id": "D",
        "text": "Configurar um webhook que tira capturas de tela da Spark UI e envia por e-mail.",
        "correct": false,
        "explanation": "Incorreto. Inviável e não estruturado para métricas e alertas."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "A biblioteca oficial 'spark-monitoring' da Microsoft integra o Azure Databricks com o Azure Log Analytics Workspace, permitindo criar dashboards e alertas no Azure Monitor baseados em métricas do Spark."
  },
  {
    "id": 38,
    "domain": 1,
    "domainName": "Domínio 1: Configurar o Ambiente Azure Databricks (15–20%)",
    "type": "multiple",
    "caseStudyId": null,
    "question": "Quais DUAS configurações são exigidas para garantir o menor custo de DBUs e de VMs em um pipeline diário de engenharia de dados que processa arquivos na madrugada? (Selecione duas opções)",
    "options": [
      {
        "id": "A",
        "text": "Utilizar um All-Purpose Cluster de alta disponibilidade ligado continuamente 24 horas por dia.",
        "correct": false,
        "explanation": "Incorreto. Taxa de DBU muito mais cara e desperdício de VMs ligadas sem necessidade."
      },
      {
        "id": "B",
        "text": "Desabilitar o Delta Log e gravar dados em formato texto puro (.txt).",
        "correct": false,
        "explanation": "Incorreto. Degrada o desempenho e perde as garantias ACID do Lakehouse."
      },
      {
        "id": "C",
        "text": "Executar o processamento através do navegador de um desenvolvedor logado no portal.",
        "correct": false,
        "explanation": "Incorreto. Não permite automação nem governança de produção."
      },
      {
        "id": "D",
        "text": "Configurar a execução via Databricks Workflows utilizando um Job Cluster efêmero.",
        "correct": true,
        "explanation": "Correto. Job Clusters cobram a menor taxa de DBU por hora e são destruídos ao final do pipeline."
      },
      {
        "id": "E",
        "text": "Habilitar autotermination imediato ou término automático do job cluster assim que o pipeline concluir.",
        "correct": true,
        "explanation": "Correto. Job clusters efêmeros encerram sua infraestrutura logo após a conclusão da execução, evitando custos ociosos."
      }
    ],
    "correctAnswers": [
      "D",
      "E"
    ],
    "overallExplanation": "Para workloads agendados de engenharia de dados, o exame DP-750 exige a combinação de Databricks Workflows com Job Clusters efêmeros configurados para encerramento automático após o término das tarefas."
  },
  {
    "id": 39,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": "case-08",
    "question": "Um analista de BI tenta consultar uma tabela chamada 'vendas_ouro' no Unity Catalog executando 'SELECT * FROM vendas_ouro;'. A consulta falha com erro informando que a tabela não foi encontrada no catálogo padrão. Qual é a sintaxe oficial recomendada pelo exame DP-750 para referenciar qualquer objeto no Unity Catalog?",
    "options": [
      {
        "id": "A",
        "text": "Montar a tabela no DBFS local com dbutils.fs.mount() e ler via /mnt/vendas_ouro.",
        "correct": false,
        "explanation": "Incorreto. O DBFS mount é um padrão legado desaconselhado pelo exame."
      },
      {
        "id": "B",
        "text": "Executar a query precedida por %sql default.vendas_ouro.",
        "correct": false,
        "explanation": "Incorreto. Apenas 2 níveis aponta para o catálogo padrão da sessão, sem qualificação explícita."
      },
      {
        "id": "C",
        "text": "Utilizar a nomenclatura de 3 níveis totalmente qualificada (Three-Level Namespace): catalog.schema.table (ex: prod_lakehouse.financeiro.vendas_ouro).",
        "correct": true,
        "explanation": "Correto. O Unity Catalog exige ou recomenda fortemente o uso do namespace de 3 níveis (catalog.schema.table) para garantir portabilidade e evitar ambiguidades."
      },
      {
        "id": "D",
        "text": "Converter a tabela para formato CSV e fazer o download no computador do analista.",
        "correct": false,
        "explanation": "Incorreto. Não resolve a consulta no Azure Databricks e viola normas de segurança corporativa."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "No Unity Catalog, o 3-Level Namespace (catalog.schema.table) é a convenção fundamental para identificar unicamente tabelas, views e volumes em qualquer workspace conectado ao metastore."
  },
  {
    "id": 40,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Uma organização de saúde armazena laudos médicos e exames em formato PDF e imagens DICOM que não são dados tabulares. A equipe precisa aplicar controle de acesso governado (RBAC) com auditoria nesses arquivos não estruturados. Qual objeto do Unity Catalog atende perfeitamente a esse requisito?",
    "options": [
      {
        "id": "A",
        "text": "Gravar todos os arquivos em uma coluna do tipo BINARY em uma Managed Table Delta.",
        "correct": false,
        "explanation": "Incorreto. Gravar arquivos pesados em colunas binárias degrada o log de transações e a performance de leitura do Delta Lake."
      },
      {
        "id": "B",
        "text": "Colocar os arquivos no DBFS raiz público FileStore.",
        "correct": false,
        "explanation": "Incorreto. O FileStore não oferece governança RBAC nem auditoria fina do Unity Catalog."
      },
      {
        "id": "C",
        "text": "Exigir que os médicos enviem os arquivos por e-mail para a equipe de TI.",
        "correct": false,
        "explanation": "Incorreto. Inviável e viola regras de conformidade e privacidade."
      },
      {
        "id": "D",
        "text": "Criar um Unity Catalog Volume (Managed ou External Volume).",
        "correct": true,
        "explanation": "Correto. Volumes no Unity Catalog governam arquivos não tabulares (PDFs, imagens, CSVs brutos) com permissões SQL (READ VOLUME, WRITE VOLUME) e auditoria nativa."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "Volumes do Unity Catalog são objetos de primeira classe desenhados especificamente para governar, auditar e acessar arquivos não estruturados e semi-estruturados em caminhos do tipo `/Volumes/catalogo/schema/volume_name/`."
  },
  {
    "id": 41,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Qual é a diferença fundamental entre uma Managed Table e uma External Table no Unity Catalog quando o comando DROP TABLE é executado?",
    "options": [
      {
        "id": "A",
        "text": "Em uma Managed Table, o DROP TABLE exclui os metadados no catálogo E todos os arquivos Parquet de dados do storage; em uma External Table, exclui APENAS os metadados, preservando os arquivos de dados intactos no ADLS Gen2.",
        "correct": true,
        "explanation": "Correto. Essa é a distinção mais testada no DP-750: tabelas gerenciadas perdem dados e metadados no DROP, enquanto tabelas externas mantêm os dados subjacentes."
      },
      {
        "id": "B",
        "text": "Em uma Managed Table, os dados nunca podem ser excluídos mesmo com DROP TABLE.",
        "correct": false,
        "explanation": "Incorreto. O DROP TABLE em Managed Tables remove permanentemente os arquivos de dados do storage gerenciado."
      },
      {
        "id": "C",
        "text": "External Tables não suportam o formato Delta Lake nem comandos SQL.",
        "correct": false,
        "explanation": "Incorreto. External Tables suportam Delta Lake, Parquet, JSON, etc."
      },
      {
        "id": "D",
        "text": "Managed Tables residem exclusivamente na memória RAM volátil do nó Driver.",
        "correct": false,
        "explanation": "Incorreto. Managed Tables persistem dados em arquivos Parquet no ADLS Gen2 subjacente ao metastore."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "Managed Tables têm seu ciclo de vida totalmente gerenciado pelo Unity Catalog (dados e metadados apagados no DROP). External Tables preservam os arquivos de dados no container do ADLS Gen2 caso a tabela seja excluída do catálogo."
  },
  {
    "id": 42,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": "case-03",
    "question": "Um engenheiro de dados precisa configurar o Unity Catalog para acessar um container no ADLS Gen2 ('abfss://raw@datalake.dfs.core.windows.net/'). Qual objeto de infraestrutura do Unity Catalog deve ser criado PRIMEIRO para encapsular as credenciais de autenticação baseadas no Azure Access Connector?",
    "options": [
      {
        "id": "A",
        "text": "External Location.",
        "correct": false,
        "explanation": "Incorreto. A External Location depende de uma Storage Credential pré-existente para se autenticar."
      },
      {
        "id": "B",
        "text": "Storage Credential (utilizando a Managed Identity do Azure Access Connector).",
        "correct": true,
        "explanation": "Correto. A Storage Credential encapsula a identidade gerenciada da Azure; em seguida, a External Location utiliza essa credencial para conceder acesso ao path do storage."
      },
      {
        "id": "C",
        "text": "Catalog.",
        "correct": false,
        "explanation": "Incorreto. O catálogo pode ser criado a qualquer momento, mas o acesso ao storage físico requer a Storage Credential e a External Location."
      },
      {
        "id": "D",
        "text": "Row Filter.",
        "correct": false,
        "explanation": "Incorreto. Row Filter é uma política de segurança de linhas de tabela, não infraestrutura de conexão com o Azure Storage."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "No Unity Catalog, o fluxo de infraestrutura de storage exige primeiro a criação de uma `Storage Credential` (vinculada à Managed Identity do Access Connector com `Storage Blob Data Contributor`) e depois a `External Location` que mapeia a URL do container àquela credencial."
  },
  {
    "id": 43,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Qual comando SQL cria corretamente uma External Location associando o container de dados à credencial de armazenamento 'cred_corp' no Unity Catalog?",
    "options": [
      {
        "id": "A",
        "text": "ATTACH STORAGE 'abfss://raw@datalake.dfs.core.windows.net/' USING PASSWORD 'cred_corp';",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente."
      },
      {
        "id": "B",
        "text": "MOUNT 'abfss://raw@datalake.dfs.core.windows.net/' TO '/mnt/raw' WITH CREDENTIAL cred_corp;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe de montagem legada DBFS, não Unity Catalog."
      },
      {
        "id": "C",
        "text": "CREATE EXTERNAL LOCATION loc_adls_raw URL 'abfss://raw@datalake.dfs.core.windows.net/' WITH (STORAGE CREDENTIAL cred_corp);",
        "correct": true,
        "explanation": "Correto. Essa é a sintaxe oficial ANSI SQL do Unity Catalog para criar uma External Location."
      },
      {
        "id": "D",
        "text": "GRANT ALL PRIVILEGES ON CONTAINER raw TO cred_corp;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inválida no Databricks."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "A sintaxe oficial do Unity Catalog é: `CREATE EXTERNAL LOCATION <nome> URL '<caminho-abfss>' WITH (STORAGE CREDENTIAL <nome-credencial>);`."
  },
  {
    "id": 44,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Um usuário do grupo 'analistas_marketing' precisa consultar a tabela 'prod.crm.clientes'. O administrador concedeu o privilégio 'GRANT SELECT ON TABLE prod.crm.clientes TO analistas_marketing;'. Ao executar a query, o analista recebe erro de acesso negado. Qual concessão adicional é estritamente obrigatória no modelo hierárquico do Unity Catalog?",
    "options": [
      {
        "id": "A",
        "text": "Conceder permissão de Subscription Owner na assinatura do Microsoft Azure.",
        "correct": false,
        "explanation": "Incorreto. Viola o princípio do menor privilégio e não resolve privilégios internos do Unity Catalog."
      },
      {
        "id": "B",
        "text": "Alterar a senha do analista para a mesma senha do Metastore Admin.",
        "correct": false,
        "explanation": "Incorreto. Totalmente inseguro e viola normas de auditoria."
      },
      {
        "id": "C",
        "text": "Mudar o modo do cluster para Unrestricted e desativar o Unity Catalog.",
        "correct": false,
        "explanation": "Incorreto. Viola a governança de dados e desabilita a segurança."
      },
      {
        "id": "D",
        "text": "Conceder USE CATALOG no catálogo 'prod' E conceder USE SCHEMA no schema 'crm' para o grupo 'analistas_marketing'.",
        "correct": true,
        "explanation": "Correto. No Unity Catalog, para atravessar a hierarquia e acessar um objeto folha (tabela/view/volume), o usuário precisa obrigatoriamente de USE CATALOG no catálogo pai e USE SCHEMA no schema pai."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "Essa é a pegadinha clássica de segurança do DP-750: No Unity Catalog, possuir apenas `SELECT` na tabela é insuficiente. É obrigatório ter `USE CATALOG` no catálogo e `USE SCHEMA` no schema pai para poder resolver e ler a tabela."
  },
  {
    "id": 45,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": "case-06",
    "question": "A equipe de segurança corporativa exige que analistas de atendimento ao cliente visualizem apenas os registros de clientes do seu respectivo país (ex: analistas do Brasil só veem clientes onde pais = 'BR'), enquanto gerentes globais visualizam todos os países. Qual funcionalidade moderna do Unity Catalog atende a esse requisito sem criar views duplicadas?",
    "options": [
      {
        "id": "A",
        "text": "Criar uma função SQL (UDF) com is_account_group_member() e associá-la à tabela como um Row Filter.",
        "correct": true,
        "explanation": "Correto. Row Filters no Unity Catalog aplicam predicados de filtragem dinâmicos na tabela física baseados no grupo do usuário atual, sem necessidade de views intermediárias."
      },
      {
        "id": "B",
        "text": "Criar uma view separada para cada um dos 195 países do mundo e conceder permissões manuais.",
        "correct": false,
        "explanation": "Incorreto. Pesadelo de manutenção operacional e inviável em escala."
      },
      {
        "id": "C",
        "text": "Executar um job noturno que divide a tabela em 195 tabelas físicas diferentes no ADLS Gen2.",
        "correct": false,
        "explanation": "Incorreto. Duplica storage, aumenta custos de DBUs e fragmenta a governança."
      },
      {
        "id": "D",
        "text": "Instruir os analistas a sempre lembrarem de digitar WHERE pais = 'BR' em todas as queries.",
        "correct": false,
        "explanation": "Incorreto. Não provê segurança; analistas poderiam alterar a cláusula WHERE e vazar dados de outros países."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "Row Filters no Unity Catalog utilizam UDFs que retornam um booleano: `CREATE FUNCTION filtro(pais STRING) RETURN IF(is_account_group_member('gerentes_globais'), true, pais = 'BR');`. O filtro é vinculado diretamente à tabela via `ALTER TABLE tbl SET ROW FILTER filtro ON (pais);`."
  },
  {
    "id": 46,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Uma tabela de recursos humanos contém a coluna 'salario_base' e 'numero_cpf'. A equipe de auditoria deve ver os valores originais, mas qualquer outro usuário deve ver o CPF mascarado como '***.***.12' e o salário como nulo. Qual funcionalidade do Unity Catalog resolve essa necessidade de conformidade?",
    "options": [
      {
        "id": "A",
        "text": "Excluir as colunas de CPF e salário permanentemente da base de dados.",
        "correct": false,
        "explanation": "Incorreto. Os auditores e o RH precisam consultar esses dados."
      },
      {
        "id": "B",
        "text": "Criar funções SQL de mascaramento dinâmico e aplicá-las às colunas como Column Masks.",
        "correct": true,
        "explanation": "Correto. Column Masks interceptam consultas de usuários não autorizados e retornam valores mascarados ou nulos, preservando os dados brutos para auditoria."
      },
      {
        "id": "C",
        "text": "Criptografar o disco rígido da máquina virtual do analista com BitLocker.",
        "correct": false,
        "explanation": "Incorreto. Não afeta os resultados das queries executadas no Lakehouse."
      },
      {
        "id": "D",
        "text": "Impedir todos os usuários da empresa de acessarem o Databricks.",
        "correct": false,
        "explanation": "Incorreto. Inviabiliza a operação da empresa."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "Column Masks no Unity Catalog permitem definir funções de transformação por coluna vinculadas com `ALTER TABLE tbl ALTER COLUMN cpf SET MASK func_mascara;`, garantindo privacidade de dados PII em conformidade com a LGPD e GDPR."
  },
  {
    "id": 47,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Um arquiteto precisa saber quem foi o usuário que executou um comando DROP TABLE em uma tabela financeira confidencial na semana passada e a partir de qual endereço IP a ação foi disparada. Qual tabela do sistema provê essa trilha de auditoria?",
    "options": [
      {
        "id": "A",
        "text": "system.billing.usage",
        "correct": false,
        "explanation": "Incorreto. system.billing.usage monitora consumo de DBUs para faturamento, não comandos de auditoria DDL/DML."
      },
      {
        "id": "B",
        "text": "system.information_schema.tables",
        "correct": false,
        "explanation": "Incorreto. Mostra metadados de tabelas atuais, não o histórico temporal de ações de auditoria."
      },
      {
        "id": "C",
        "text": "system.access.audit",
        "correct": true,
        "explanation": "Correto. A tabela system.access.audit registra todos os eventos de auditoria do Unity Catalog, incluindo user_identity.email, service_name, action_name, request_params e client_ip_address."
      },
      {
        "id": "D",
        "text": "system.dlt.event_log",
        "correct": false,
        "explanation": "Incorreto. O event log do DLT é restrito a pipelines Delta Live Tables."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "A tabela `system.access.audit` do Unity Catalog é o repositório centralizado de auditoria de conformidade, registrando operações DDL, acessos a dados, alterações de privilégios e IPs de origem."
  },
  {
    "id": 48,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": "case-01",
    "question": "Uma organização precisa compartilhar uma tabela de cotações financeiras em tempo real com três bancos parceiros. Dois desses bancos utilizam AWS e Google Cloud e NÃO possuem Azure Databricks. Qual recurso do Databricks permite esse compartilhamento seguro e sem cópia física de dados?",
    "options": [
      {
        "id": "A",
        "text": "Exportar os dados para arquivos CSV e enviá-los por e-mail com senha no arquivo ZIP.",
        "correct": false,
        "explanation": "Incorreto. Inseguro, sujeito a limites de tamanho de anexo e perda total de governança."
      },
      {
        "id": "B",
        "text": "Montar um servidor FTP Windows Server 2008 dentro da VNet do Databricks.",
        "correct": false,
        "explanation": "Incorreto. Tecnologicamente defasado, inseguro e de alta manutenção."
      },
      {
        "id": "C",
        "text": "Exigir que todos os bancos parceiros comprem assinaturas corporativas do Azure Databricks.",
        "correct": false,
        "explanation": "Incorreto. O Delta Sharing Open Sharing elimina expressamente a necessidade de o destinatário possuir Databricks."
      },
      {
        "id": "D",
        "text": "Delta Sharing no modo Open Sharing (via protocolo REST aberto e arquivo de credencial bearer token).",
        "correct": true,
        "explanation": "Correto. O Delta Sharing é um protocolo aberto que permite a qualquer cliente (Python, Pandas, Power BI, Apache Spark em qualquer nuvem) consultar tabelas compartilhadas diretamente do ADLS Gen2 sem ter Databricks."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "O Delta Sharing oferece compartilhamento aberto (Open Sharing) baseado em padrões abertos REST. O provedor gera um link de ativação onde o destinatário baixa um arquivo de credenciais seguro e acessa a tabela em tempo real sem duplicação de dados."
  },
  {
    "id": 49,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Qual comando SQL cria um compartilhamento no Delta Sharing e adiciona a tabela 'prod.logistica.remessas' a ele?",
    "options": [
      {
        "id": "A",
        "text": "CREATE SHARE share_logistica; ALTER SHARE share_logistica ADD TABLE prod.logistica.remessas;",
        "correct": true,
        "explanation": "Correto. Essa é a sintaxe oficial ANSI SQL do Unity Catalog para criação e inclusão de tabelas em um Share."
      },
      {
        "id": "B",
        "text": "EXPORT TABLE prod.logistica.remessas TO DELTA_SHARE 'share_logistica';",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente."
      },
      {
        "id": "C",
        "text": "GRANT DELTA_SHARING ON TABLE prod.logistica.remessas TO ALL;",
        "correct": false,
        "explanation": "Incorreto. Delta Sharing exige a criação de um objeto Share e posterior atribuição a Recipients."
      },
      {
        "id": "D",
        "text": "CREATE EXTERNAL RECIPIENT ON TABLE prod.logistica.remessas;",
        "correct": false,
        "explanation": "Incorreto. Recipient representa o consumidor externo, não o conjunto de tabelas."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "A gestão de Delta Sharing no Unity Catalog utiliza: `CREATE SHARE <nome_share>;` seguido por `ALTER SHARE <nome_share> ADD TABLE <nome_tabela>;`."
  },
  {
    "id": 50,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Um engenheiro de dados precisa ler um arquivo de configuração JSON armazenado em um Volume do Unity Catalog localizado no caminho: catalogo 'lakehouse', schema 'parametros', volume 'configs', arquivo 'setup.json'. Qual caminho de sistema de arquivos deve ser passado para o código Python?",
    "options": [
      {
        "id": "A",
        "text": "/dbfs/mnt/lakehouse/parametros/configs/setup.json",
        "correct": false,
        "explanation": "Incorreto. /dbfs/mnt é a convenção de montagens legadas descontinuada."
      },
      {
        "id": "B",
        "text": "/Volumes/lakehouse/parametros/configs/setup.json",
        "correct": true,
        "explanation": "Correto. Os Volumes do Unity Catalog são expostos no sistema de arquivos local do cluster através do ponto de montagem padrão /Volumes/<catalog>/<schema>/<volume>/<file>."
      },
      {
        "id": "C",
        "text": "abfss://setup.json@datalake.blob.core.windows.net",
        "correct": false,
        "explanation": "Incorreto. Não utiliza o namespace de 3 níveis do Volume no Unity Catalog."
      },
      {
        "id": "D",
        "text": "http://localhost:8080/configs/setup.json",
        "correct": false,
        "explanation": "Incorreto. Volumes não são acessados via porta HTTP local."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "Volumes no Unity Catalog utilizam a convenção de caminho POSIX padronizada: `/Volumes/<catalog_name>/<schema_name>/<volume_name>/<path_to_file>`."
  },
  {
    "id": 51,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": "case-04",
    "question": "Qual privilégio do Unity Catalog deve ser concedido a um usuário para que ele consiga fazer upload de novos arquivos Parquet para dentro de um Volume existente?",
    "options": [
      {
        "id": "A",
        "text": "SELECT",
        "correct": false,
        "explanation": "Incorreto. SELECT aplica-se a tabelas e views, não a volumes."
      },
      {
        "id": "B",
        "text": "EXECUTE",
        "correct": false,
        "explanation": "Incorreto. EXECUTE aplica-se a funções SQL definidas por usuários (UDFs)."
      },
      {
        "id": "C",
        "text": "WRITE VOLUME",
        "correct": true,
        "explanation": "Correto. O privilégio WRITE VOLUME permite fazer upload, atualizar e excluir arquivos dentro de um volume no Unity Catalog."
      },
      {
        "id": "D",
        "text": "USE CATALOG ONLY",
        "correct": false,
        "explanation": "Incorreto. USE CATALOG apenas permite ver o catálogo, não escrever em volumes."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "As permissões em Unity Catalog Volumes são: `READ VOLUME` (para leitura e download de arquivos) e `WRITE VOLUME` (para gravação, upload e deleção de arquivos)."
  },
  {
    "id": 52,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Uma empresa precisa transferir a propriedade (ownership) de todas as tabelas de um schema para um novo grupo corporativo chamado 'engenharia_dados_lead'. Qual comando SQL transfere corretamente o proprietário de uma tabela?",
    "options": [
      {
        "id": "A",
        "text": "GRANT ALL PRIVILEGES ON TABLE prod.financeiro.contas TO `engenharia_dados_lead`;",
        "correct": false,
        "explanation": "Incorreto. Conceder privilégios não altera o Owner do objeto."
      },
      {
        "id": "B",
        "text": "UPDATE system.information_schema.tables SET owner = 'engenharia_dados_lead';",
        "correct": false,
        "explanation": "Incorreto. Information Schema é somente leitura e não aceita comandos UPDATE diretos."
      },
      {
        "id": "C",
        "text": "DROP TABLE prod.financeiro.contas; CREATE TABLE ...",
        "correct": false,
        "explanation": "Incorreto. Recriar a tabela causaria indisponibilidade e perda de histórico de Delta Log."
      },
      {
        "id": "D",
        "text": "ALTER TABLE prod.financeiro.contas OWNER TO `engenharia_dados_lead`;",
        "correct": true,
        "explanation": "Correto. A instrução ALTER TABLE ... OWNER TO transfere a propriedade do objeto para o novo usuário ou grupo no Unity Catalog."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "No Unity Catalog, o comando oficial para alterar o dono de um objeto securable é `ALTER <OBJECT_TYPE> <object_name> OWNER TO <principal>;`."
  },
  {
    "id": 53,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "A equipe de governança de dados precisa rastrear o impacto de alterar o tipo de dados da coluna 'id_cliente' na tabela Bronze. Eles precisam visualizar todas as tabelas Silver, Gold e relatórios downstream que leem essa coluna. Qual funcionalidade nativa do Unity Catalog provê essa visualização gráfica?",
    "options": [
      {
        "id": "A",
        "text": "Linhagem Automatizada de Dados (Automated Column-Level Lineage) no Catalog Explorer.",
        "correct": true,
        "explanation": "Correto. O Unity Catalog captura e visualiza automaticamente a linhagem em nível de tabela e de coluna gerada por queries, notebooks, workflows e dashboards."
      },
      {
        "id": "B",
        "text": "Exportar todos os scripts PySpark em PDF e realizar busca textual com Ctrl+F.",
        "correct": false,
        "explanation": "Incorreto. Manual, sujeito a falhas e não captura fluxos de dados reais em produção."
      },
      {
        "id": "C",
        "text": "Executar o comando VACUUM em todas as tabelas para ver quais falham.",
        "correct": false,
        "explanation": "Incorreto. VACUUM limpa arquivos órfãos e não provê análise de impacto de colunas."
      },
      {
        "id": "D",
        "text": "Criar um trigger de erro em cada tabela Silver.",
        "correct": false,
        "explanation": "Incorreto. Inviabilizaria o pipeline em produção."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "O Unity Catalog oferece Linhagem de Dados Automatizada (Lineage) nativa em nível de tabela e coluna, sem necessidade de instrumentação de código, permitindo análise completa de impacto upstream e downstream."
  },
  {
    "id": 54,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": "case-07",
    "question": "Para classificar dados em conformidade com políticas de privacidade corporativas, os engenheiros precisam associar metadados indicando que uma coluna contém informações confidenciais (PII = true). Qual comando SQL aplica tags oficiais de governança no Unity Catalog?",
    "options": [
      {
        "id": "A",
        "text": "COMMENT ON COLUMN prod.crm.clientes.email IS 'PII=true';",
        "correct": false,
        "explanation": "Incorreto. COMMENT insere apenas uma descrição em texto livre, não uma Tag de governança indexável."
      },
      {
        "id": "B",
        "text": "ALTER TABLE prod.crm.clientes ALTER COLUMN email SET TAGS ('PII' = 'true', 'Compliance' = 'LGPD');",
        "correct": true,
        "explanation": "Correto. A cláusula SET TAGS no Unity Catalog associa metadados estruturados de chave-valor a tabelas e colunas para catalogação e auditoria."
      },
      {
        "id": "C",
        "text": "LABEL TABLE prod.crm.clientes AS PII;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente no Databricks."
      },
      {
        "id": "D",
        "text": "CREATE TAG ON DATABASE crm VALUES ('PII');",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inválida."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "O Unity Catalog suporta governança através de Tags aplicadas diretamente a catálogos, schemas, tabelas e colunas via `SET TAGS ('chave' = 'valor')`, permitindo busca e classificação no Catalog Explorer."
  },
  {
    "id": 55,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Qual é a permissão máxima que um usuário pode ter em todo o Metastore do Unity Catalog, com capacidade de criar catálogos, associar workspaces e delegar privilégios globais?",
    "options": [
      {
        "id": "A",
        "text": "Workspace Admin.",
        "correct": false,
        "explanation": "Incorreto. O Workspace Admin tem autoridade apenas sobre o workspace específico (criação de clusters, usuários locais), não governança global do Metastore."
      },
      {
        "id": "B",
        "text": "Catalog Owner.",
        "correct": false,
        "explanation": "Incorreto. Tem privilégios apenas dentro do catálogo que possui."
      },
      {
        "id": "C",
        "text": "Metastore Admin (Administrador do Metastore).",
        "correct": true,
        "explanation": "Correto. O Metastore Admin é a identidade com autoridade máxima de governança no Unity Catalog, responsável por gerenciar catálogos, concessões globais e external locations."
      },
      {
        "id": "D",
        "text": "Subscription Reader no Azure.",
        "correct": false,
        "explanation": "Incorreto. Permissão somente leitura no portal Azure."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "No Unity Catalog, o `Metastore Admin` é o papel de mais alto nível de governança, acima dos administradores de workspaces individuais, controlando o metastore compartilhado por múltiplos workspaces."
  },
  {
    "id": 56,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Uma empresa precisa consultar tabelas armazenadas em um banco de dados relacional Azure SQL Database diretamente a partir de consultas SQL no Azure Databricks, sem precisar copiar ou ingerir os dados previamente para o Lakehouse. Qual recurso do Unity Catalog provê essa federação de consultas?",
    "options": [
      {
        "id": "A",
        "text": "Fazer o backup do Azure SQL em fita magnética e restaurar no Databricks.",
        "correct": false,
        "explanation": "Incorreto. Inviável e não é uma solução analítica em nuvem."
      },
      {
        "id": "B",
        "text": "Criar um script em Bash que exporta tabelas para arquivos TXT via FTP a cada minuto.",
        "correct": false,
        "explanation": "Incorreto. Extremamente lento, não escalável e inseguro."
      },
      {
        "id": "C",
        "text": "Desabilitar o Unity Catalog e usar JDBC puro sem governança.",
        "correct": false,
        "explanation": "Incorreto. Perde o catálogo unificado e as políticas de governança centralizadas."
      },
      {
        "id": "D",
        "text": "Lakehouse Federation (criando uma Connection e um Foreign Catalog no Unity Catalog).",
        "correct": true,
        "explanation": "Correto. O Lakehouse Federation permite criar Foreign Catalogs mapeados para fontes externas (Azure SQL, Snowflake, PostgreSQL, etc.), consultando-as com sintaxe SQL unificada sem replicação física."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "Lakehouse Federation no Unity Catalog permite criar conexões com bancos de dados externos e mapeá-los como 'Foreign Catalogs', viabilizando consultas federadas cross-source (ex: unindo Azure SQL com Delta Lake) sem movimentação de dados."
  },
  {
    "id": 57,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": "case-02",
    "question": "Uma organização financeira precisa migrar 500 tabelas legadas do Hive Metastore tradicional (default) para o Unity Catalog. Qual comando automatizado ou ferramenta é fornecida pela Databricks para criar cópias sincronizadas ou atualizar metadados sem duplicar arquivos Parquet?",
    "options": [
      {
        "id": "A",
        "text": "Utilizar o utilitário SYNC (ou Unity Catalog Upgrade Wizard) para sincronizar schemas e tabelas legadas para o Unity Catalog.",
        "correct": true,
        "explanation": "Correto. O comando SYNC e o assistente de atualização de tabelas (Upgrade Wizard) facilitam a transição do Hive Metastore legado para o Unity Catalog de forma assistida."
      },
      {
        "id": "B",
        "text": "Excluir todas as tabelas legadas com DROP DATABASE CASCADE e começar do zero.",
        "correct": false,
        "explanation": "Incorreto. Causaria perda de dados históricos corporativos."
      },
      {
        "id": "C",
        "text": "Criar links simbólicos no Windows Explorer apontando para os arquivos DBFS.",
        "correct": false,
        "explanation": "Incorreto. Não tem relação com o ecossistema de nuvem Databricks."
      },
      {
        "id": "D",
        "text": "Substituir o Spark por um banco de dados Microsoft Access local.",
        "correct": false,
        "explanation": "Incorreto. Incompatível com volumes de Big Data corporativos."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "O comando `SYNC SCHEMA <target> FROM <source>` e o Upgrade Wizard integrado na UI do Databricks permitem migrar metadados de tabelas externas do Hive Metastore diretamente para o Unity Catalog."
  },
  {
    "id": 58,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Um usuário que possui apenas o privilégio 'SELECT' em uma tabela do Unity Catalog tenta executar o comando 'DELETE FROM prod.vendas.pedidos WHERE status = 'CANCELADO';'. O que acontece com a execução?",
    "options": [
      {
        "id": "A",
        "text": "A consulta executa com sucesso, pois SELECT inclui privilégios de exclusão.",
        "correct": false,
        "explanation": "Incorreto. SELECT concede estritamente leitura de dados."
      },
      {
        "id": "B",
        "text": "A consulta falha com erro de permissão negada, pois o comando DELETE exige o privilégio MODIFY na tabela.",
        "correct": true,
        "explanation": "Correto. Operações de modificação de dados (INSERT, UPDATE, DELETE, MERGE) no Unity Catalog exigem o privilégio MODIFY."
      },
      {
        "id": "C",
        "text": "A consulta apaga todos os dados do catálogo inteiro.",
        "correct": false,
        "explanation": "Incorreto. Cláusulas WHERE filtram linhas e privilégios impedem execuções não autorizadas."
      },
      {
        "id": "D",
        "text": "O Databricks reinicia o nó Driver automaticamente.",
        "correct": false,
        "explanation": "Incorreto. Erros de privilégio retornam exceção SQL padrão sem reiniciar hardware."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "No Unity Catalog, o privilégio `SELECT` é de somente leitura. Para alterar dados (operações de escrita, update, delete, merge), o usuário ou grupo deve possuir obrigatoriamente o privilégio `MODIFY`."
  },
  {
    "id": 59,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Como deve ser declarada uma função SQL no Unity Catalog para servir de Column Mask mascarando o endereço de e-mail de usuários para quem não pertence ao grupo 'rh_auditoria'?",
    "options": [
      {
        "id": "A",
        "text": "CREATE MASK FUNCTION email ON TABLE clientes HIDE ALL;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente no SQL do Databricks."
      },
      {
        "id": "B",
        "text": "ALTER FUNCTION email SET PASSWORD 'rh_auditoria';",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inválida."
      },
      {
        "id": "C",
        "text": "CREATE OR REPLACE FUNCTION seguranca.mascarar_email(email STRING) RETURN IF(is_account_group_member('rh_auditoria'), email, '***@empresa.com');",
        "correct": true,
        "explanation": "Correto. Funções de Column Mask recebem o valor original como parâmetro e retornam o valor original se autorizado ou o valor mascarado se o usuário não pertencer ao grupo aprovado."
      },
      {
        "id": "D",
        "text": "DROP COLUMN email WHERE user <> 'rh_auditoria';",
        "correct": false,
        "explanation": "Incorreto. DROP COLUMN remove a coluna da tabela para todos os usuários."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "Funções de mascaramento são UDFs SQL padrão que avaliam o contexto do usuário com `is_account_group_member()` ou `current_user()`, retornando o dado real ou a máscara."
  },
  {
    "id": 60,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": "case-05",
    "question": "Um desenvolvedor precisa revogar o privilégio de criação de tabelas de um grupo de contratados externos no schema 'homologacao'. Qual comando SQL deve ser executado?",
    "options": [
      {
        "id": "A",
        "text": "DELETE PERMISSION CREATE TABLE FROM `contratados_externos`;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inválida."
      },
      {
        "id": "B",
        "text": "DENY CREATE TABLE TO `contratados_externos`;",
        "correct": false,
        "explanation": "Incorreto. O Unity Catalog opera com modelo explícito de concessão (GRANT) e revogação (REVOKE)."
      },
      {
        "id": "C",
        "text": "REMOVE USER FROM SCHEMA dev_catalog.homologacao;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente."
      },
      {
        "id": "D",
        "text": "REVOKE CREATE TABLE ON SCHEMA dev_catalog.homologacao FROM `contratados_externos`;",
        "correct": true,
        "explanation": "Correto. O comando ANSI SQL oficial para remover permissões no Unity Catalog é REVOKE <privilege> ON <securable> FROM <principal>."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "No Unity Catalog, permissões concedidas previamente via `GRANT` são revogadas utilizando a instrução padrão `REVOKE <privilégio> ON <objeto> FROM <identidade>;`."
  },
  {
    "id": 61,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Por que o modelo de governança do Unity Catalog é considerado superior às antigas Table Access Controls (Table ACLs) legadas do Hive Metastore?",
    "options": [
      {
        "id": "A",
        "text": "O Unity Catalog centraliza a governança em múltiplos workspaces e clouds, suporta 3-Level Namespace, Volumes, Row/Column security e Linhagem automática independente do runtime.",
        "correct": true,
        "explanation": "Correto. O Unity Catalog oferece uma plataforma unificada e desacoplada dos workspaces, enquanto Table ACLs legadas eram limitadas ao workspace local e não suportavam arquivos não estruturados ou linhagem."
      },
      {
        "id": "B",
        "text": "Table ACLs legadas exigiam o pagamento de US$ 10.000 adicionais por usuário.",
        "correct": false,
        "explanation": "Incorreto. Table ACLs não tinham custo adicional de licença, eram apenas tecnicamente limitadas."
      },
      {
        "id": "C",
        "text": "O Unity Catalog desliga todos os servidores da nuvem a cada hora.",
        "correct": false,
        "explanation": "Incorreto. O Unity Catalog é um serviço de governança altamente disponível."
      },
      {
        "id": "D",
        "text": "Table ACLs legadas só funcionavam em máquinas locais sem internet.",
        "correct": false,
        "explanation": "Incorreto. Funcionavam na nuvem, porém presas ao workspace legado."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "O Unity Catalog resolve as limitações das Table ACLs legadas, fornecendo governança regional multi-workspace, auditoria centralizada em `system.access.audit`, linhagem ponta a ponta e suporte a volumes."
  },
  {
    "id": 62,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Um arquiteto precisa configurar um alerta que dispara sempre que um usuário do workspace tentar conceder privilégios administrativos a outra pessoa. Qual consulta na tabela system.access.audit filtra essas ações?",
    "options": [
      {
        "id": "A",
        "text": "SELECT * FROM system.billing.usage WHERE sku_name = 'ADMIN_ALERT';",
        "correct": false,
        "explanation": "Incorreto. system.billing.usage monitora apenas cobrança de DBUs."
      },
      {
        "id": "B",
        "text": "SELECT * FROM system.access.audit WHERE service_name = 'unityCatalog' AND action_name IN ('grantPermissions', 'revokePermissions');",
        "correct": true,
        "explanation": "Correto. Ações de controle de acesso do Unity Catalog registram action_name como 'grantPermissions' e 'revokePermissions'."
      },
      {
        "id": "C",
        "text": "SELECT * FROM system.information_schema.table_privileges WHERE is_grantable = 'ALERT';",
        "correct": false,
        "explanation": "Incorreto. Consulta inválida."
      },
      {
        "id": "D",
        "text": "SELECT * FROM system.dlt.event_log WHERE event_type = 'SECURITY';",
        "correct": false,
        "explanation": "Incorreto. DLT event log registra execução de pipelines de dados, não auditoria de governança do catálogo."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "Na tabela `system.access.audit`, os eventos do Unity Catalog contêm `service_name = 'unityCatalog'` e registram concessões e revogações com `action_name` igual a `grantPermissions` ou `revokePermissions`."
  },
  {
    "id": 63,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": "case-08",
    "question": "Ao criar uma tabela externa no Unity Catalog, um engenheiro digita: CREATE TABLE cat.sch.tbl_ext LOCATION 'abfss://raw@datalake.dfs.core.windows.net/vendas'. A query falha com erro informando que o caminho especificado não é coberto por nenhuma External Location aprovada. Como resolver?",
    "options": [
      {
        "id": "A",
        "text": "Adicionar a chave da conta de armazenamento (Storage Account Key) diretamente no comando CREATE TABLE.",
        "correct": false,
        "explanation": "Incorreto. Chaves em texto claro no SQL são bloqueadas e violam a segurança do Unity Catalog."
      },
      {
        "id": "B",
        "text": "Mudar o caminho para um disco rígido C:\\ local da máquina de desenvolvimento.",
        "correct": false,
        "explanation": "Incorreto. Caminhos locais de desktop não são suportados em clusters de nuvem."
      },
      {
        "id": "C",
        "text": "Criar previamente uma External Location no Unity Catalog que englobe o caminho 'abfss://raw@datalake.dfs.core.windows.net/vendas' associada a uma Storage Credential válida.",
        "correct": true,
        "explanation": "Correto. O Unity Catalog proíbe a criação de tabelas externas em caminhos que não estejam explicitamente cobertos por uma External Location registrada e autorizada."
      },
      {
        "id": "D",
        "text": "Excluir o catálogo e utilizar uma pasta temporária do Linux.",
        "correct": false,
        "explanation": "Incorreto. Não cria a tabela corporativa externa necessária."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "Tabelas e volumes externos no Unity Catalog exigem que o caminho de armazenamento na nuvem esteja contido dentro de uma `External Location` previamente registrada e governada."
  },
  {
    "id": 64,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Em uma instituição financeira, pesquisadores precisam analisar dados clínicos, mas não podem ter acesso aos nomes completos dos pacientes. Uma Column Mask foi associada à coluna 'nome_paciente'. O que é retornado para um pesquisador que executa 'SELECT nome_paciente FROM clinica.pacientes;'?",
    "options": [
      {
        "id": "A",
        "text": "Uma mensagem de erro de compilação bloqueando a execução da consulta inteira.",
        "correct": false,
        "explanation": "Incorreto. A consulta executa com sucesso; apenas o conteúdo da coluna mascarada é transformado."
      },
      {
        "id": "B",
        "text": "Todos os dados originais sem nenhuma alteração.",
        "correct": false,
        "explanation": "Incorreto. Usuários não autorizados recebem o valor mascarado."
      },
      {
        "id": "C",
        "text": "O computador do pesquisador é desconectado da rede da empresa.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      },
      {
        "id": "D",
        "text": "O resultado da transformação definida na função de mascaramento (ex: 'PACIENTE_ANONIMO' ou iniciais), enquanto as demais colunas não mascaradas são retornadas normalmente.",
        "correct": true,
        "explanation": "Correto. A Column Mask substitui os valores daquela coluna específica dinamicamente em tempo de execução sem afetar as outras colunas da consulta."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "Column Masks operam de forma transparente: a consulta SQL executa normalmente, mas os valores exibidos para os usuários não privilegiados são os valores substituídos pela função mascaradora."
  },
  {
    "id": 65,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Qual comando SQL lista todas as concessões de privilégios ativas na tabela 'prod.vendas.pedidos'?",
    "options": [
      {
        "id": "A",
        "text": "SHOW GRANTS ON TABLE prod.vendas.pedidos;",
        "correct": true,
        "explanation": "Correto. A instrução SHOW GRANTS exibe todos os usuários e grupos com privilégios concedidos naquele objeto específico."
      },
      {
        "id": "B",
        "text": "LIST PERMISSIONS IN TABLE prod.vendas.pedidos;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente."
      },
      {
        "id": "C",
        "text": "SELECT * FROM sys.permissions_table WHERE name = 'prod.vendas.pedidos';",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inválida no Databricks."
      },
      {
        "id": "D",
        "text": "DESCRIBE HISTORY prod.vendas.pedidos;",
        "correct": false,
        "explanation": "Incorreto. DESCRIBE HISTORY exibe commits de transações do Delta Lake, não concessões de privilégios."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "O comando padrão ANSI SQL no Databricks para inspecionar permissões é `SHOW GRANTS ON <securable_type> <securable_name>;`."
  },
  {
    "id": 66,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": "case-03",
    "question": "Qual objeto do Unity Catalog é o contêiner de mais alto nível na hierarquia de dados, servindo como agrupador de múltiplos schemas e bancos de dados lógicos?",
    "options": [
      {
        "id": "A",
        "text": "Schema.",
        "correct": false,
        "explanation": "Incorreto. Schema é o segundo nível, contido dentro de um Catálogo."
      },
      {
        "id": "B",
        "text": "Catalog (Catálogo).",
        "correct": true,
        "explanation": "Correto. O Catálogo é o primeiro nível da hierarquia de 3 níveis (Catalog -> Schema -> Tabela/View/Volume)."
      },
      {
        "id": "C",
        "text": "Volume.",
        "correct": false,
        "explanation": "Incorreto. Volume é um objeto folha, contido dentro de um Schema."
      },
      {
        "id": "D",
        "text": "Partition.",
        "correct": false,
        "explanation": "Incorreto. Partição é uma divisão física de armazenamento dentro de uma tabela."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "A hierarquia de dados do Unity Catalog é estritamente: Metastore (nível regional) > Catalog (primeiro nível lógico) > Schema (segundo nível lógico) > Table/View/Volume (terceiro nível)."
  },
  {
    "id": 67,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Uma organização multinacional possui cientistas de dados utilizando clusters interativos com Databricks Runtime padrão. Qual modo de acesso ao cluster deve ser configurado para que o cluster respeite 100% as regras de governança do Unity Catalog para um único usuário?",
    "options": [
      {
        "id": "A",
        "text": "Modo 'No Isolation Shared' legado.",
        "correct": false,
        "explanation": "Incorreto. Desabilita as travas de segurança e não é compatível com governança rigorosa do Unity Catalog."
      },
      {
        "id": "B",
        "text": "Modo 'Driver Only' sem suporte a rede.",
        "correct": false,
        "explanation": "Incorreto. Impede a execução de jobs distribuídos."
      },
      {
        "id": "C",
        "text": "Modo de acesso 'Single User' associado à identidade Entra ID do cientista de dados.",
        "correct": true,
        "explanation": "Correto. Clusters Single User são totalmente compatíveis com o Unity Catalog, suportam todas as linguagens (Python, Scala, R, SQL) e operam com o contexto de segurança daquele usuário específico."
      },
      {
        "id": "D",
        "text": "Executar sem nenhuma configuração de modo de acesso.",
        "correct": false,
        "explanation": "Incorreto. O Databricks exige a seleção do modo de acesso (Single User ou Shared) em clusters com Unity Catalog."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "Para desenvolvedores individuais que precisam rodar Python, Scala, R e SQL com suporte completo ao Unity Catalog, o modo 'Single User' é o padrão recomendado."
  },
  {
    "id": 68,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "multiple",
    "caseStudyId": null,
    "question": "Quais DUAS ações são necessárias para que uma aplicação em Python externa conecte-se a uma tabela compartilhada via Delta Sharing sem possuir uma conta no Azure Databricks? (Selecione duas opções)",
    "options": [
      {
        "id": "A",
        "text": "O parceiro externo deve pagar uma licença do Microsoft Windows Server para a Databricks.",
        "correct": false,
        "explanation": "Incorreto. Delta Sharing é um protocolo aberto de código aberto."
      },
      {
        "id": "B",
        "text": "Os arquivos Parquet devem ser convertidos em planilhas do Microsoft Excel .xls.",
        "correct": false,
        "explanation": "Incorreto. Inviável e tecnicamente incorreto."
      },
      {
        "id": "C",
        "text": "O administrador deve liberar acesso irrestrito de escrita em todo o metastore.",
        "correct": false,
        "explanation": "Incorreto. Violação crítica de segurança; o compartilhamento é somente leitura."
      },
      {
        "id": "D",
        "text": "O administrador do Databricks cria um Recipient no Delta Sharing e envia o link de ativação seguro para a organização parceira.",
        "correct": true,
        "explanation": "Correto. O Recipient gera o token de autenticação e credencial de acesso."
      },
      {
        "id": "E",
        "text": "O parceiro externo utiliza o conector de código aberto 'delta-sharing' (ex: delta_sharing.load_as_pandas()) informando o arquivo de credenciais .share baixado.",
        "correct": true,
        "explanation": "Correto. A biblioteca cliente de Delta Sharing lê diretamente os dados autorizados via REST API sem precisar de Databricks."
      }
    ],
    "correctAnswers": [
      "D",
      "E"
    ],
    "overallExplanation": "No Delta Sharing aberto (Open Sharing), o administrador cria um Recipient que gera um perfil de conexão (.share com bearer token). O parceiro externo utiliza qualquer biblioteca compatível (Python, Power BI, Spark) para ler os dados diretamente."
  },
  {
    "id": 69,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": "case-06",
    "question": "Um arquiteto precisa revogar o acesso a uma tabela compartilhada via Delta Sharing para um destinatário parceiro cujo contrato encerrou. Qual comando SQL executa a revogação?",
    "options": [
      {
        "id": "A",
        "text": "REVOKE SELECT ON SHARE share_parceiros FROM RECIPIENT recipient_empresa_b;",
        "correct": true,
        "explanation": "Correto. Permissões de compartilhamento são revogadas com REVOKE SELECT ON SHARE <share> FROM RECIPIENT <recipient>."
      },
      {
        "id": "B",
        "text": "DELETE STORAGE FROM RECIPIENT recipient_empresa_b;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente."
      },
      {
        "id": "C",
        "text": "ALTER TABLE DROP SHARE;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inválida."
      },
      {
        "id": "D",
        "text": "KILL CONNECTION recipient_empresa_b;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "O acesso de um recipient a um share no Unity Catalog é controlado via concessões padrão: `REVOKE SELECT ON SHARE <nome_share> FROM RECIPIENT <nome_recipient>;`."
  },
  {
    "id": 70,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Em um schema governado pelo Unity Catalog, um engenheiro cria uma tabela com: CREATE TABLE cat.sch.tbl (id INT);. Onde os dados físicos dessa tabela serão salvos no ADLS Gen2?",
    "options": [
      {
        "id": "A",
        "text": "No desktop do usuário que digitou o comando.",
        "correct": false,
        "explanation": "Incorreto. Dados residem na nuvem corporativa."
      },
      {
        "id": "B",
        "text": "No caminho de armazenamento raiz padrão configurado para o schema 'sch' ou para o catálogo 'cat' associado ao Metastore.",
        "correct": true,
        "explanation": "Correto. Managed Tables gravam automaticamente seus dados no local de armazenamento gerenciado definido na hierarquia do schema/catálogo/metastore."
      },
      {
        "id": "C",
        "text": "Em um pendrive conectado ao servidor da Microsoft.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      },
      {
        "id": "D",
        "text": "No banco de dados local MySQL do nó Driver.",
        "correct": false,
        "explanation": "Incorreto. O Lakehouse utiliza ADLS Gen2."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "Managed Tables não exigem cláusula LOCATION; o Unity Catalog armazena seus dados no storage gerenciado definido na criação do Schema, do Catálogo ou do Metastore."
  },
  {
    "id": 71,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Qual comando SQL cria um Managed Volume chamado 'raw_logs' dentro do catálogo 'prod' e schema 'telemetria'?",
    "options": [
      {
        "id": "A",
        "text": "CREATE MANAGED FOLDER prod.telemetria.raw_logs;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente; o objeto chama-se VOLUME."
      },
      {
        "id": "B",
        "text": "MKDIR /Volumes/prod/telemetria/raw_logs;",
        "correct": false,
        "explanation": "Incorreto. MKDIR é comando de terminal shell, não comando SQL DDL do catálogo."
      },
      {
        "id": "C",
        "text": "CREATE VOLUME prod.telemetria.raw_logs;",
        "correct": true,
        "explanation": "Correto. A criação de um Managed Volume utiliza a sintaxe direta CREATE VOLUME <catalog>.<schema>.<volume_name>; sem especificar LOCATION."
      },
      {
        "id": "D",
        "text": "MOUNT VOLUME prod.telemetria.raw_logs ON DBFS;",
        "correct": false,
        "explanation": "Incorreto. Volumes não utilizam montagem legada DBFS."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "Para criar um Managed Volume, a instrução SQL oficial é: `CREATE VOLUME <catalog>.<schema>.<volume_name>;`. Caso fosse um External Volume, adicionaria-se a cláusula `LOCATION '<path>'`."
  },
  {
    "id": 72,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": "case-01",
    "question": "Um usuário tenta ler um volume com: SELECT * FROM read_files('/Volumes/prod/raw/dados/*.csv');. Qual permissão mínima ele precisa ter no volume para executar a leitura dos arquivos?",
    "options": [
      {
        "id": "A",
        "text": "MODIFY",
        "correct": false,
        "explanation": "Incorreto. MODIFY é para alterar dados tabulares."
      },
      {
        "id": "B",
        "text": "WRITE VOLUME",
        "correct": false,
        "explanation": "Incorreto. WRITE VOLUME é necessário para gravação e upload, não apenas leitura."
      },
      {
        "id": "C",
        "text": "DROP TABLE",
        "correct": false,
        "explanation": "Incorreto. Permissão destrutiva de exclusão de tabelas."
      },
      {
        "id": "D",
        "text": "READ VOLUME (além de USE CATALOG e USE SCHEMA na hierarquia pai).",
        "correct": true,
        "explanation": "Correto. A permissão de leitura de arquivos em um Volume é o privilégio READ VOLUME."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "A função `read_files()` lê dados de arquivos em volumes e exige o privilégio `READ VOLUME` no volume correspondente, junto com `USE CATALOG` e `USE SCHEMA`."
  },
  {
    "id": 73,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Ao consultar o histórico de linhagem de uma tabela Gold no Catalog Explorer, um analista percebe que a linhagem de colunas está disponível. Qual mecanismo produz esses dados de linhagem?",
    "options": [
      {
        "id": "A",
        "text": "O Unity Catalog analisa os planos lógicos de execução das queries submetidas no Spark e registra automaticamente as dependências de colunas sem overhead de código.",
        "correct": true,
        "explanation": "Correto. A linhagem é gerada de forma automatizada e transparente a partir da instrumentação nativa do Catalyst Optimizer no Unity Catalog."
      },
      {
        "id": "B",
        "text": "O desenvolvedor precisa digitar manualmente a linhagem em um arquivo JSON em cada deploy.",
        "correct": false,
        "explanation": "Incorreto. A linhagem é 100% automatizada."
      },
      {
        "id": "C",
        "text": "Um analista da Microsoft verifica as queries manualmente e atualiza o gráfico.",
        "correct": false,
        "explanation": "Incorreto. Processo automático de software."
      },
      {
        "id": "D",
        "text": "A linhagem só funciona se os dados forem gravados em formato CSV.",
        "correct": false,
        "explanation": "Incorreto. Funciona nativamente com Delta Lake e qualquer formato suportado."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "O motor do Unity Catalog intercepta os planos lógicos resolvidos no Spark e extrai as relações de entrada e saída em tempo real, populando as tabelas de linhagem automaticamente."
  },
  {
    "id": 74,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Como a governança do Unity Catalog trata permissões concedidas a grupos em comparação com permissões concedidas a usuários individuais?",
    "options": [
      {
        "id": "A",
        "text": "O Unity Catalog proíbe o uso de grupos e permite permissões apenas para CPFs individuais.",
        "correct": false,
        "explanation": "Incorreto. Grupos são o padrão recomendado."
      },
      {
        "id": "B",
        "text": "Recomenda-se conceder privilégios exclusivamente a Grupos sincronizados via SCIM do Microsoft Entra ID para simplificar a gestão e auditoria, evitando concessões a usuários individuais.",
        "correct": true,
        "explanation": "Correto. Conceder acessos a grupos (Role-Based Access Control) é a melhor prática oficial do exame DP-750, evitando privilégios órfãos e complexidade de manutenção."
      },
      {
        "id": "C",
        "text": "Grupos só podem ter privilégios de leitura aos domingos.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      },
      {
        "id": "D",
        "text": "Conceder privilégios a grupos dobra o consumo de DBUs do workspace.",
        "correct": false,
        "explanation": "Incorreto. Governança de catálogo não altera a taxa de DBU de clusters."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "A prática recomendada da Microsoft é aplicar RBAC concedendo privilégios a grupos de segurança centralizados gerenciados via Entra ID e propagados pelo SCIM."
  },
  {
    "id": 75,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": "case-04",
    "question": "Um engenheiro precisa remover uma External Location chamada 'loc_antiga' do Unity Catalog. Qual comando SQL realiza essa exclusão de metadados?",
    "options": [
      {
        "id": "A",
        "text": "DELETE FROM system.locations WHERE name = 'loc_antiga';",
        "correct": false,
        "explanation": "Incorreto. Não se excluem objetos do sistema via comando DELETE."
      },
      {
        "id": "B",
        "text": "UNMOUNT loc_antiga;",
        "correct": false,
        "explanation": "Incorreto. UNMOUNT é comando legado do DBFS."
      },
      {
        "id": "C",
        "text": "DROP EXTERNAL LOCATION loc_antiga;",
        "correct": true,
        "explanation": "Correto. A sintaxe oficial para remoção de uma localização externa no catálogo é DROP EXTERNAL LOCATION <nome>;."
      },
      {
        "id": "D",
        "text": "ALTER LOCATION loc_antiga SET DISABLED;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inválida."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "Objetos de infraestrutura de storage no Unity Catalog são removidos com comandos DDL padrão: `DROP EXTERNAL LOCATION <nome>;` e `DROP STORAGE CREDENTIAL <nome>;`."
  },
  {
    "id": 76,
    "domain": 2,
    "domainName": "Domínio 2: Segurança e Governança com Unity Catalog (15–20%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Qual função SQL interna do Databricks retorna o endereço de e-mail do usuário autenticado que está executando a consulta no momento, amplamente utilizada em Row Filters?",
    "options": [
      {
        "id": "A",
        "text": "get_user_ip()",
        "correct": false,
        "explanation": "Incorreto. Retorna endereço IP, não a identidade Entra ID do usuário."
      },
      {
        "id": "B",
        "text": "session_id()",
        "correct": false,
        "explanation": "Incorreto. Retorna identificador da sessão Spark."
      },
      {
        "id": "C",
        "text": "who_is_there()",
        "correct": false,
        "explanation": "Incorreto. Função fictícia."
      },
      {
        "id": "D",
        "text": "current_user()",
        "correct": true,
        "explanation": "Correto. A função SQL current_user() retorna o e-mail/identidade do usuário ativo que disparou a consulta."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "Em funções de segurança de linha e coluna, `current_user()` e `is_account_group_member()` são as funções nativas essenciais para autenticação contextual do solicitante."
  },
  {
    "id": 77,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Uma plataforma de e-commerce deposita continuamente milhares de arquivos JSON com novos pedidos em um container no ADLS Gen2. A equipe de dados precisa ingerir esses arquivos incrementalmente em uma tabela Bronze sem reprocessar arquivos antigos e com suporte automático a novos campos que possam surgir no JSON. Qual tecnologia deve ser implementada?",
    "options": [
      {
        "id": "A",
        "text": "Auto Loader (utilizando spark.readStream com formato 'cloudFiles' e cloudFiles.schemaLocation).",
        "correct": true,
        "explanation": "Correto. O Auto Loader (cloudFiles) é o mecanismo padrão ouro do Azure Databricks para ingestão incremental e escalável de arquivos em nuvem com detecção automática de schema e evolução."
      },
      {
        "id": "B",
        "text": "Comando SQL INSERT INTO executado manualmente em um notebook a cada hora.",
        "correct": false,
        "explanation": "Incorreto. Manual, não escalável e não detecta novos arquivos automaticamente."
      },
      {
        "id": "C",
        "text": "spark.read.json() em batch lendo o diretório inteiro e sobrescrevendo a tabela inteira a cada 5 minutos.",
        "correct": false,
        "explanation": "Incorreto. Reprocessa todos os arquivos antigos continuamente, gerando custos absurdos e latência crescente."
      },
      {
        "id": "D",
        "text": "Criar uma macro no Excel que lê os JSONs via Power Query local.",
        "correct": false,
        "explanation": "Incorreto. Incompatível com pipelines corporativos de Big Data."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "O Auto Loader (`cloudFiles`) processa arquivos de forma incremental e eficiente à medida que chegam ao armazenamento em nuvem, oferecendo detecção automática de arquivos e inferência e evolução contínua de schema."
  },
  {
    "id": 78,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": "case-07",
    "question": "No Auto Loader do Azure Databricks, arquivos JSON chegam com uma coluna inesperada de desconto ('cupom_desconto') que não existia no schema original inferido. Como o Auto Loader lida com isso quando configurado com a opção padrão 'cloudFiles.schemaEvolutionMode' = 'addNewColumns'?",
    "options": [
      {
        "id": "A",
        "text": "O pipeline falha imediatamente e descarta todos os arquivos do lote.",
        "correct": false,
        "explanation": "Incorreto. Isso ocorre apenas no modo 'failOnNewColumns'."
      },
      {
        "id": "B",
        "text": "A nova coluna é adicionada automaticamente ao schema da tabela Delta de destino e o pipeline continua processando sem interrupção.",
        "correct": true,
        "explanation": "Correto. O modo 'addNewColumns' detecta novos campos e estende automaticamente o schema da tabela Delta sem derrubar o stream de produção."
      },
      {
        "id": "C",
        "text": "Os valores da nova coluna são excluídos e ignorados silenciosamente.",
        "correct": false,
        "explanation": "Incorreto. O Auto Loader preserva os novos dados estendendo o schema ou usando a coluna de resgate."
      },
      {
        "id": "D",
        "text": "O cluster é reiniciado e o catálogo é apagado.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "No modo `addNewColumns`, o Auto Loader atualiza o schema de forma não destrutiva, adicionando novas colunas na tabela de destino e garantindo continuidade operacional sem falhas em produção."
  },
  {
    "id": 79,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Durante a ingestão de telemetria com Auto Loader, alguns arquivos JSON contêm dados corrompidos (ex: uma string 'INVALID_DATE' em um campo esperado como DATE). Onde o Auto Loader armazena esses dados fora do padrão para que não quebrem a tipagem da tabela nem sejam perdidos para auditoria?",
    "options": [
      {
        "id": "A",
        "text": "Em um arquivo temporário no desktop do engenheiro de dados.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      },
      {
        "id": "B",
        "text": "Na lixeira do Windows.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      },
      {
        "id": "C",
        "text": "Na coluna especial oculta '_rescued_data', armazenada em formato JSON string.",
        "correct": true,
        "explanation": "Correto. A coluna _rescued_data captura dados corrompidos, incompatíveis com o schema ou não tipados, permitindo que a ingestão continue sem perda de informação."
      },
      {
        "id": "D",
        "text": "No log do driver do Spark em formato de aviso de erro de compilação.",
        "correct": false,
        "explanation": "Incorreto. Os dados são persistidos na própria tabela de dados para consulta posterior."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "A coluna `_rescued_data` é o mecanismo de segurança do Auto Loader: qualquer dado que não corresponda ao schema esperado ou que esteja corrompido é salvo como texto JSON nessa coluna, evitando parada do pipeline e perda de registros."
  },
  {
    "id": 80,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Um container no ADLS Gen2 já acumula mais de 25 milhões de arquivos Parquet em sua árvore de diretórios. Ao usar o Auto Loader no modo padrão de Directory Listing, o Driver do Spark consome muito tempo e memória apenas listando os novos arquivos. Qual modo do Auto Loader deve ser habilitado para contornar esse gargalo?",
    "options": [
      {
        "id": "A",
        "text": "Modo de Força Bruta com 1.000 nós workers dedicados apenas a listar diretórios.",
        "correct": false,
        "explanation": "Incorreto. Extremamente caro e ineficiente."
      },
      {
        "id": "B",
        "text": "Mudar o formato de Parquet para CSV para acelerar a leitura.",
        "correct": false,
        "explanation": "Incorreto. CSV é muito mais lento que Parquet."
      },
      {
        "id": "C",
        "text": "Mover os 25 milhões de arquivos manualmente um a um via portal da Azure.",
        "correct": false,
        "explanation": "Incorreto. Operacionalmente inviável."
      },
      {
        "id": "D",
        "text": "Modo de Notificação de Arquivos (File Notification Mode), configurando 'cloudFiles.useNotifications' = 'true'.",
        "correct": true,
        "explanation": "Correto. O modo de notificação de arquivos utiliza Azure Event Grid e Azure Queue Storage para receber notificações de novos arquivos instantaneamente, sem varreduras dispendiosas no sistema de arquivos."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "Para diretórios que acumulam milhões de arquivos, o Auto Loader oferece o `File Notification Mode`. Ele provisiona automaticamente um Azure Event Grid e uma fila Azure Queue Storage para identificar novos arquivos sem precisar listar o diretório."
  },
  {
    "id": 81,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": "case-02",
    "question": "Um pipeline de ingestão diária precisa carregar novos arquivos de vendas a cada noite. Em vez de manter um cluster ligado em streaming contínuo 24/7, a empresa quer rodar o Auto Loader como um job efêmero na madrugada, processando todos os arquivos acumulados e desligando em seguida. Qual trigger do writeStream atende perfeitamente a esse requisito?",
    "options": [
      {
        "id": "A",
        "text": ".trigger(availableNow=True)",
        "correct": true,
        "explanation": "Correto. O trigger AvailableNow consome todos os dados pendentes em micro-lotes de tamanho ótimo e finaliza a execução do stream automaticamente, ideal para Job Clusters efêmeros."
      },
      {
        "id": "B",
        "text": ".trigger(continuous='1 second')",
        "correct": false,
        "explanation": "Incorreto. Continuous streaming mantém o cluster rodando 24/7."
      },
      {
        "id": "C",
        "text": ".trigger(processingTime='10 minutes')",
        "correct": false,
        "explanation": "Incorreto. Mantém o stream ativo indefinidamente a cada 10 minutos."
      },
      {
        "id": "D",
        "text": ".trigger(never=True)",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "O trigger `availableNow=True` substituiu o legado `once=True`. Ele processa todos os novos dados disponíveis na fonte respeitando limites de rate limit em micro-batches e encerra o pipeline com sucesso, economizando DBUs em jobs agendados."
  },
  {
    "id": 82,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Uma equipe de analistas SQL precisa carregar lotes de arquivos Parquet depositados semanalmente no ADLS Gen2 em uma tabela Delta. O volume é moderado (cerca de 500 arquivos por semana) e o schema é 100% estático. Eles preferem um comando SQL puro e idempotente sem precisar escrever scripts PySpark. Qual comando atende a este cenário?",
    "options": [
      {
        "id": "A",
        "text": "LOAD DATA LOCAL INPATH em arquivos de texto.",
        "correct": false,
        "explanation": "Incorreto. Comando legado do Hive com limitações de performance e localidade."
      },
      {
        "id": "B",
        "text": "COPY INTO prod.bronze.vendas FROM 'abfss://...' FILEFORMAT = PARQUET;",
        "correct": true,
        "explanation": "Correto. O comando COPY INTO é uma instrução SQL idempotente nativa do Databricks, perfeita para cargas em lote regulares com schema estável."
      },
      {
        "id": "C",
        "text": "SELECT * INTO OUTFILE via MySQL.",
        "correct": false,
        "explanation": "Incorreto. Comando de banco relacional tradicional fora do contexto Lakehouse."
      },
      {
        "id": "D",
        "text": "BULK INSERT via T-SQL do SQL Server.",
        "correct": false,
        "explanation": "Incorreto. Comando específico do SQL Server, não do Databricks."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "O comando SQL `COPY INTO` permite carregar dados incrementalmente de forma idempotente (arquivos já carregados são ignorados automaticamente, a menos que `force=true` seja passado), sem exigir código PySpark."
  },
  {
    "id": 83,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Em uma arquitetura Medallion corporativa no Azure Databricks, quais são as características e responsabilidades da camada Bronze?",
    "options": [
      {
        "id": "A",
        "text": "Armazenar agregações de relatórios de BI com joins complexos e métricas de faturamento.",
        "correct": false,
        "explanation": "Incorreto. Essa é a responsabilidade da camada Gold."
      },
      {
        "id": "B",
        "text": "Armazenar apenas dados descartados e inválidos que serão apagados em 24 horas.",
        "correct": false,
        "explanation": "Incorreto. A camada Bronze preserva todos os dados ingeridos."
      },
      {
        "id": "C",
        "text": "Armazenar dados brutos ingeridos das fontes no estado mais próximo possível do original, em modo append-only, com metadados de ingestão (data e hora de carga) e histórico imutável.",
        "correct": true,
        "explanation": "Correto. A camada Bronze representa a verdade histórica dos dados como chegaram da origem, sem transformações de negócio, permitindo reprocessamento a qualquer momento."
      },
      {
        "id": "D",
        "text": "Armazenar arquivos em formato Microsoft Word .docx para leitura humana.",
        "correct": false,
        "explanation": "Incorreto. A arquitetura Medallion utiliza Delta Lake e Parquet."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "Na Arquitetura Medallion: Bronze = dados brutos com metadados de ingestão (Raw / Append-only); Silver = dados limpos, tipados, deduplicados e conformed; Gold = métricas agregadas e modelos dimensionais prontos para consumo de BI."
  },
  {
    "id": 84,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": "case-05",
    "question": "Em uma arquitetura Medallion corporativa, quais são as características e transformações típicas executadas na camada Silver?",
    "options": [
      {
        "id": "A",
        "text": "Ingestão bruta de arquivos JSON corrompidos sem nenhuma validação.",
        "correct": false,
        "explanation": "Incorreto. Responsabilidade da camada Bronze."
      },
      {
        "id": "B",
        "text": "Criação de dashboards visuais com gráficos de pizza para diretoria.",
        "correct": false,
        "explanation": "Incorreto. Dashboards consomem dados da camada Gold."
      },
      {
        "id": "C",
        "text": "Exportação de planilhas para disquetes físicos.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      },
      {
        "id": "D",
        "text": "Limpeza de dados, validação de schema, tipagem estrita de colunas, deduplicação de registros e enriquecimento básico com tabelas de referência.",
        "correct": true,
        "explanation": "Correto. A camada Silver atua como a 'camada de conformidade e integridade', limpando anomalias e provendo dados confiáveis para cientistas e analistas."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "A camada Silver filtra dados inválidos, desaninha estruturas complexas, deduplica eventos e aplica regras de qualidade para criar uma visão consistente e auditada da entidade de negócio."
  },
  {
    "id": 85,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Em uma arquitetura Medallion, qual é o propósito principal da camada Gold?",
    "options": [
      {
        "id": "A",
        "text": "Disponibilizar modelos de dados agregados, tabelas de fatos e dimensões (Star Schema) otimizadas para leitura rápida de BI, relatórios gerenciais e modelos de Machine Learning.",
        "correct": true,
        "explanation": "Correto. A camada Gold contém os dados estruturados prontos para consumo de negócio, com KPIs pré-calculados e alta performance de consulta."
      },
      {
        "id": "B",
        "text": "Armazenar arquivos de log brutos do Apache Spark para diagnóstico de bugs.",
        "correct": false,
        "explanation": "Incorreto. Logs do Spark residem no storage de diagnóstico ou DBFS."
      },
      {
        "id": "C",
        "text": "Guardar backups de senhas de usuários do Entra ID.",
        "correct": false,
        "explanation": "Incorreto. Violação crítica de segurança."
      },
      {
        "id": "D",
        "text": "Executar cópia fiel byte a byte de todas as tabelas do mainframe legado.",
        "correct": false,
        "explanation": "Incorreto. Cópia fiel é o papel da camada Bronze."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "A camada Gold atende aos casos de uso de negócio final: analistas de dados, painéis de Power BI e cientistas de dados encontram métricas consolidadas e dimensões padronizadas."
  },
  {
    "id": 86,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Um engenheiro de dados recebe um DataFrame PySpark contendo uma coluna com uma string JSON aninhada chamada 'dados_cliente'. Qual função do PySpark deve ser utilizada para transformar essa string em uma estrutura colunar (StructType) no DataFrame?",
    "options": [
      {
        "id": "A",
        "text": "to_json(col('dados_cliente'))",
        "correct": false,
        "explanation": "Incorreto. to_json faz o caminho inverso: converte uma coluna Struct ou Array em uma string JSON."
      },
      {
        "id": "B",
        "text": "from_json(col('dados_cliente'), schema_definido)",
        "correct": true,
        "explanation": "Correto. A função from_json analisa a string JSON e a converte em um StructType de acordo com o schema schema_definido."
      },
      {
        "id": "C",
        "text": "json_split(col('dados_cliente'))",
        "correct": false,
        "explanation": "Incorreto. Função inexistente no PySpark."
      },
      {
        "id": "D",
        "text": "cast('json')",
        "correct": false,
        "explanation": "Incorreto. O Spark não possui casting genérico 'json'."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "A função `from_json(coluna, schema)` do PySpark analisa o payload JSON textual e o transforma em colunas estruturadas nativas do Spark conforme o schema fornecido."
  },
  {
    "id": 87,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": "case-08",
    "question": "Uma coluna de pedidos chamada 'itens' contém um Array com múltiplos produtos comprados em um único pedido. O engenheiro precisa transformar esse array para que cada item vire uma linha independente no DataFrame, mantendo o ID do pedido original. Qual função PySpark deve ser usada?",
    "options": [
      {
        "id": "A",
        "text": "flatten(col('itens'))",
        "correct": false,
        "explanation": "Incorreto. flatten achata arrays de arrays em um único array, mas não desdobra em novas linhas."
      },
      {
        "id": "B",
        "text": "split(col('itens'))",
        "correct": false,
        "explanation": "Incorreto. split divide uma string em array de strings com base em um delimitador."
      },
      {
        "id": "C",
        "text": "explode(col('itens'))",
        "correct": true,
        "explanation": "Correto. A função explode cria uma nova linha para cada elemento presente no array da coluna especificada."
      },
      {
        "id": "D",
        "text": "group_by(col('itens'))",
        "correct": false,
        "explanation": "Incorreto. Agrupamento consolida linhas, não expande arrays em linhas."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "A função `explode()` desaninha coleções (arrays ou maps), gerando uma nova linha no DataFrame para cada item da coleção e duplicando as demais colunas da linha original."
  },
  {
    "id": 88,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Para deduplicar uma tabela Silver de clientes mantendo apenas o registro mais recente de cada cliente com base na coluna 'data_atualizacao', qual combinação de Window Function é recomendada no PySpark?",
    "options": [
      {
        "id": "A",
        "text": "Window.orderBy('id_cliente') e somar o total de vendas.",
        "correct": false,
        "explanation": "Incorreto. Não deduplica nem utiliza partição por cliente."
      },
      {
        "id": "B",
        "text": "distinct() em todas as colunas sem critérios de janela.",
        "correct": false,
        "explanation": "Incorreto. distinct só remove linhas 100% idênticas; se a data mudou, o distinct não descarta o registro antigo."
      },
      {
        "id": "C",
        "text": "dropDuplicates(['id_cliente']) sem ordenação prévia.",
        "correct": false,
        "explanation": "Incorreto. dropDuplicates sem ordenação de janela pode reter um registro desatualizado arbitrariamente."
      },
      {
        "id": "D",
        "text": "Window.partitionBy('id_cliente').orderBy(col('data_atualizacao').desc()) e filtrar onde row_number() == 1.",
        "correct": true,
        "explanation": "Correto. Particionar pelo ID e ordenar de forma decrescente pela data permite numerar as linhas e reter exclusivamente a linha mais recente (row_number 1)."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "O padrão ouro de engenharia no DP-750 para deduplicação com controle temporal é particionar por entidade (`partitionBy('id_cliente')`), ordenar decrescente por timestamp (`orderBy(desc)`) e filtrar `row_number() == 1`."
  },
  {
    "id": 89,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Qual função de janela do Spark SQL permite consultar o valor da coluna 'status_pedido' da linha ANTERIOR de um mesmo cliente ordenada cronologicamente, essencial para calcular transições de estado?",
    "options": [
      {
        "id": "A",
        "text": "lag('status_pedido', 1).over(window_spec)",
        "correct": true,
        "explanation": "Correto. A função lag() retorna o valor de uma coluna a uma distância fixa antes da linha atual na janela de ordenação."
      },
      {
        "id": "B",
        "text": "lead('status_pedido', 1).over(window_spec)",
        "correct": false,
        "explanation": "Incorreto. lead() retorna o valor da linha posterior (seguinte), não da anterior."
      },
      {
        "id": "C",
        "text": "first_value().over(window_spec)",
        "correct": false,
        "explanation": "Incorreto. Retorna o primeiro valor absoluto da partição inteira."
      },
      {
        "id": "D",
        "text": "prior_record()",
        "correct": false,
        "explanation": "Incorreto. Função inexistente no Spark SQL."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "A função `lag(col, offset)` acessa valores de linhas anteriores dentro da partição da janela, amplamente utilizada em análise de séries temporais e mudanças de estado."
  },
  {
    "id": 90,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": "case-03",
    "question": "Em um cenário de Slowly Changing Dimension Tipo 1 (SCD1), como o comando Delta Lake MERGE INTO deve atualizar a tabela dimensional quando um cliente existente alterar seu endereço?",
    "options": [
      {
        "id": "A",
        "text": "Inserir uma nova linha marcando a linha antiga com is_current = false e data de término.",
        "correct": false,
        "explanation": "Incorreto. Este é o comportamento de SCD Tipo 2, não SCD Tipo 1."
      },
      {
        "id": "B",
        "text": "Sobrescrever diretamente o endereço antigo do cliente na linha existente (in-place update), mantendo a mesma chave primária sem criar uma nova linha.",
        "correct": true,
        "explanation": "Correto. SCD Tipo 1 reflete apenas o estado atual (sobrescrita), sem manter histórico de versões anteriores."
      },
      {
        "id": "C",
        "text": "Excluir o cliente e apagar todo o histórico de compras passadas dele.",
        "correct": false,
        "explanation": "Incorreto. Viola a integridade referencial."
      },
      {
        "id": "D",
        "text": "Criar uma nova tabela no banco de dados chamada clientes_novo_endereco.",
        "correct": false,
        "explanation": "Incorreto. Não é uma boa prática de modelagem de dados."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "SCD Tipo 1 realiza sobrescrita em linha (`WHEN MATCHED THEN UPDATE SET target.col = source.col`), preservando apenas o valor mais recente e sem reter histórico retroativo."
  },
  {
    "id": 91,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Em um cenário de Slowly Changing Dimension Tipo 2 (SCD2), qual é o objetivo arquitetural de manter as colunas 'start_date', 'end_date' e 'is_current' na tabela dimensional?",
    "options": [
      {
        "id": "A",
        "text": "Acelerar a compactação de arquivos Parquet durante o comando VACUUM.",
        "correct": false,
        "explanation": "Incorreto. VACUUM limpa arquivos órfãos, não tem relação com modelagem dimensional."
      },
      {
        "id": "B",
        "text": "Permitir que o Power BI desabilite o DirectQuery e use apenas CSV.",
        "correct": false,
        "explanation": "Incorreto. Não se relaciona com SCD2."
      },
      {
        "id": "C",
        "text": "Preservar o histórico completo de alterações da entidade ao longo do tempo, permitindo consultar como eram os dados em qualquer data passada e identificando qual versão está ativa no momento.",
        "correct": true,
        "explanation": "Correto. SCD Tipo 2 mantém histórico completo com vigência temporal, essencial para auditoria regulatória e relatórios históricos precisos."
      },
      {
        "id": "D",
        "text": "Garantir que a tabela não consuma memória RAM no nó Driver.",
        "correct": false,
        "explanation": "Incorreto. Não tem relação com consumo de memória de hardware."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "SCD Tipo 2 mantém histórico de alterações criando novas linhas para cada mutação com controle de intervalo de tempo (`start_date`, `end_date`) e flag indicadora de versão atual (`is_current = true`)."
  },
  {
    "id": 92,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Para otimizar o desempenho de uma instrução MERGE INTO no Delta Lake em tabelas com dezenas de terabytes, qual cláusula no predicado ON é crucial para permitir que o motor de consulta aplique Partition Pruning e evite varreduras de tabela inteira?",
    "options": [
      {
        "id": "A",
        "text": "Remover a cláusula ON e utilizar um CROSS JOIN irrestrito.",
        "correct": false,
        "explanation": "Incorreto. Geraria um produto cartesiano gigantesco e esgotaria a memória."
      },
      {
        "id": "B",
        "text": "Executar o MERGE com a opção 'WHEN NOT MATCHED DO NOTHING'.",
        "correct": false,
        "explanation": "Incorreto. Não resolve a poda de arquivos na leitura."
      },
      {
        "id": "C",
        "text": "Utilizar uma tabela sem chave primária nem colunas indexadas.",
        "correct": false,
        "explanation": "Incorreto. Piora ainda mais o tempo de execução."
      },
      {
        "id": "D",
        "text": "Incluir a coluna de partição ou clusterização (ex: target.data_evento = source.data_evento AND target.id = source.id) no predicado ON.",
        "correct": true,
        "explanation": "Correto. Ao incluir a chave de partição/clusterização na condição ON do MERGE, o Delta Lake limita a leitura apenas aos arquivos afetados, evitando full table scans caros."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "Ao adicionar predicados baseados nas colunas de partição ou Liquid Clustering na cláusula `ON` do MERGE, o Catalyst Optimizer consegue realizar partição/file pruning, escaneando apenas as frações da tabela que realmente sofrerão mutação."
  },
  {
    "id": 93,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": "case-06",
    "question": "No Spark Structured Streaming, por que é estritamente obrigatório configurar a opção 'checkpointLocation' apontando para um caminho persistente no ADLS Gen2?",
    "options": [
      {
        "id": "A",
        "text": "O checkpoint armazena o log de offsets de leitura e o estado da consulta, garantindo tolerância a falhas e semântica de processamento exatamente uma vez (exactly-once) em caso de reinicialização.",
        "correct": true,
        "explanation": "Correto. O diretório de checkpoint é indispensável para que o stream saiba de onde parou após falhas ou desligamentos sem duplicar nem perder registros."
      },
      {
        "id": "B",
        "text": "O checkpoint armazena o código fonte em Python para que outros analistas possam ler o notebook.",
        "correct": false,
        "explanation": "Incorreto. O código fica no Git ou Workspace, não no checkpoint do stream."
      },
      {
        "id": "C",
        "text": "Sem o checkpoint, o Spark apaga os dados da tabela de origem.",
        "correct": false,
        "explanation": "Incorreto. A fonte não é apagada, mas a recuperação contra falhas seria impossível."
      },
      {
        "id": "D",
        "text": "O checkpoint serve apenas para registrar o número de telefone do administrador do cluster.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "O `checkpointLocation` grava o log transacional e os arquivos de estado do Structured Streaming em armazenamento persistente, viabilizando recuperação determinística e garantias de idempotência/exactly-once."
  },
  {
    "id": 94,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Qual é a diferença entre os modos de saída 'append', 'update' e 'complete' em consultas do Spark Structured Streaming?",
    "options": [
      {
        "id": "A",
        "text": "'append' apaga a tabela inteira a cada 10 segundos.",
        "correct": false,
        "explanation": "Incorreto. Append apenas anexa novas linhas."
      },
      {
        "id": "B",
        "text": "'append' grava apenas as novas linhas inseridas; 'update' grava apenas as linhas que foram modificadas ou adicionadas desde o último batch; 'complete' reescreve a tabela inteira com todos os resultados agregados a cada batch.",
        "correct": true,
        "explanation": "Correto. Essa é a definição exata dos três OutputModes suportados pelo Structured Streaming."
      },
      {
        "id": "C",
        "text": "'complete' só pode ser usado se a tabela tiver menos de 10 linhas.",
        "correct": false,
        "explanation": "Incorreto. Complete é projetado para agregações com estado."
      },
      {
        "id": "D",
        "text": "'update' só é permitido para arquivos de texto sem cabeçalho.",
        "correct": false,
        "explanation": "Incorreto. Não há restrição de cabeçalho."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "No Structured Streaming: `append` é o padrão para fluxos incrementais sem agregações; `update` emite apenas linhas atualizadas de agregações; `complete` regrava a tabela inteira de agregação a cada micro-lote."
  },
  {
    "id": 95,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Um pipeline de streaming agrega métricas de consumo de dados por dispositivo móvel a cada 5 minutos. O cluster começou a sofrer com vazamento de memória e erros frequentes de OutOfMemory (OOM) no State Store da JVM após alguns dias. Qual mecanismo deve ser aplicado para descartar dados tardios e liberar a memória do State Store?",
    "options": [
      {
        "id": "A",
        "text": "Aumentar o número de nós do cluster para 100 máquinas virtuais a cada hora.",
        "correct": false,
        "explanation": "Incorreto. Apenas postergaria o OOM e aumentaria custos astronomicamente sem resolver a causa raiz."
      },
      {
        "id": "B",
        "text": "Desabilitar o checkpoint e salvar os dados na memória volátil do Driver.",
        "correct": false,
        "explanation": "Incorreto. Viola a tolerância a falhas e pioraria a memória do Driver."
      },
      {
        "id": "C",
        "text": "Aplicar Watermarking na coluna de timestamp do evento utilizando withWatermark('timestamp_evento', '15 minutes').",
        "correct": true,
        "explanation": "Correto. O Watermarking define o limiar de atraso máximo aceitável para dados em streaming, permitindo que o Spark descarte estados antigos da memória e previna OutOfMemory no State Store."
      },
      {
        "id": "D",
        "text": "Parar o streaming e reiniciar o cluster manualmente a cada 30 minutos.",
        "correct": false,
        "explanation": "Incorreto. Incompatível com SLAs de tempo real de produção."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "Sem `watermarking`, o Spark mantém o estado de agregação aberto indefinidamente aguardando eventos atrasados, esgotando a memória RAM dos executores (State Store). O `withWatermark()` estabelece o corte temporal para limpar o estado antigo."
  },
  {
    "id": 96,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": "case-01",
    "question": "Como o Liquid Clustering (CLUSTER BY) soluciona o problema crônico de 'small files' que ocorria no particionamento tradicional Hive quando engenheiros particionavam tabelas por colunas de alta cardinalidade (ex: id_cliente)?",
    "options": [
      {
        "id": "A",
        "text": "O Liquid Clustering compacta todos os dados em um único arquivo de 50 Terabytes.",
        "correct": false,
        "explanation": "Incorreto. Um arquivo de 50 TB eliminaria o paralelismo distribuído do Spark."
      },
      {
        "id": "B",
        "text": "O Liquid Clustering converte automaticamente todas as colunas de alta cardinalidade em números binários de 1 bit.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      },
      {
        "id": "C",
        "text": "O Liquid Clustering exige que o desenvolvedor crie os diretórios manualmente via FTP.",
        "correct": false,
        "explanation": "Incorreto. O processo é 100% gerenciado pelo motor do Delta Lake."
      },
      {
        "id": "D",
        "text": "O Liquid Clustering não cria subdiretórios físicos por valor de chave; ele organiza os dados dentro de arquivos Parquet de tamanho ótimo (~1 GB) utilizando curvas multidimensionais de preenchimento de espaço.",
        "correct": true,
        "explanation": "Correto. Ao contrário do particionamento tradicional que cria uma pasta para cada valor distinto, o Liquid Clustering agrupa registros mantendo arquivos consolidados de tamanho ideal sem fragmentação."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "O Liquid Clustering substitui a estrutura hierárquica rígida de diretórios do Hive por organização física baseada em Z-order/Hilbert curves em arquivos Parquet de tamanho uniforme, eliminando a criação de milhares de pastas e arquivos minúsculos."
  },
  {
    "id": 97,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Uma tabela de logística foi criada com: CREATE TABLE fretes (...) CLUSTER BY (codigo_pais, id_transportadora);. Três meses depois, o padrão de consultas mudou e os analistas passam a filtrar quase que exclusivamente por 'data_envio'. Qual é a vantagem do Liquid Clustering nesse cenário em relação ao particionamento Hive?",
    "options": [
      {
        "id": "A",
        "text": "É possível alterar as chaves de clusterização para 'CLUSTER BY (data_envio)' via simples comando ALTER TABLE sem precisar reescrever a tabela inteira do zero.",
        "correct": true,
        "explanation": "Correto. O Liquid Clustering é dinâmico e suporta evolução de chaves com ALTER TABLE. As novas gravações e os comandos OPTIMIZE incrementais aplicam o novo layout progressivamente."
      },
      {
        "id": "B",
        "text": "A tabela é excluída e o banco de dados é recriado em MySQL.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      },
      {
        "id": "C",
        "text": "O particionamento Hive era melhor pois exigia recriar a tabela em 48 horas de downtime.",
        "correct": false,
        "explanation": "Incorreto. Recriar tabelas com downtime é uma desvantagem severa do Hive legado."
      },
      {
        "id": "D",
        "text": "O Liquid Clustering não permite nenhuma alteração de chaves após a criação.",
        "correct": false,
        "explanation": "Incorreto. A flexibilidade de alteração de chaves é exatamente um dos seus maiores diferenciais."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "No particionamento clássico Hive, alterar a coluna de partição exigia recriar a tabela e mover todos os dados. No Liquid Clustering, basta rodar `ALTER TABLE tbl CLUSTER BY (novas_colunas);` e o layout evolui incrementalmente."
  },
  {
    "id": 98,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "O que são Deletion Vectors no Delta Lake e como eles revolucionam a performance de comandos DELETE, UPDATE e MERGE INTO?",
    "options": [
      {
        "id": "A",
        "text": "São vírus de computador criados para apagar dados de concorrentes.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      },
      {
        "id": "B",
        "text": "São arquivos leves de bitmaps que sinalizam linhas excluídas ou modificadas sem a necessidade de reescrever o arquivo Parquet de 100 MB inteiro no storage.",
        "correct": true,
        "explanation": "Correto. Deletion Vectors introduzem exclusão lógica via bitmaps de bits (Roaring Bitmaps), evitando operações pesadas de Copy-on-Write a cada mutação de poucas linhas."
      },
      {
        "id": "C",
        "text": "São regras de rede no firewall para bloquear tráfego de saída.",
        "correct": false,
        "explanation": "Incorreto. Deletion Vectors são um recurso de armazenamento do Delta Lake."
      },
      {
        "id": "D",
        "text": "São tabelas temporárias que existem apenas no Microsoft Excel.",
        "correct": false,
        "explanation": "Incorreto. Recurso oficial nativo do protocolo Delta Lake."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "Antes dos Deletion Vectors, modificar 1 linha em um arquivo Parquet de 100 MB forçava a reescrita dos 100 MB inteiros. Com Deletion Vectors, grava-se um bitmap levíssimo apontando a linha alterada, acelerando mutações em até 10x."
  },
  {
    "id": 99,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": "case-04",
    "question": "Qual comando habilita explicitamente Deletion Vectors em uma tabela Delta existente no Azure Databricks?",
    "options": [
      {
        "id": "A",
        "text": "ENABLE DELETION VECTORS ON prod.vendas.pedidos;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente."
      },
      {
        "id": "B",
        "text": "OPTIMIZE TABLE prod.vendas.pedidos WITH BITMAP;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inválida."
      },
      {
        "id": "C",
        "text": "ALTER TABLE prod.vendas.pedidos SET TBLPROPERTIES ('delta.enableDeletionVectors' = true);",
        "correct": true,
        "explanation": "Correto. Essa é a propriedade oficial de tabela para ativar Deletion Vectors no Delta Lake."
      },
      {
        "id": "D",
        "text": "SET spark.databricks.deletionVectors = 'yes';",
        "correct": false,
        "explanation": "Incorreto. Deve ser configurado como propriedade da tabela (TBLPROPERTIES)."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "A ativação de Deletion Vectors em tabelas existentes é realizada via `ALTER TABLE <nome> SET TBLPROPERTIES ('delta.enableDeletionVectors' = true);`."
  },
  {
    "id": 100,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Um analista de fraudes precisa consultar o estado exato de uma tabela Delta há 5 dias atrás para reproduzir o saldo bancário de uma conta antes de uma transação contestada. Qual funcionalidade do Delta Lake viabiliza essa consulta?",
    "options": [
      {
        "id": "A",
        "text": "Restauração de fita backup de fita magnética off-line.",
        "correct": false,
        "explanation": "Incorreto. Incompatível com o modelo Lakehouse."
      },
      {
        "id": "B",
        "text": "Executar o comando VACUUM com retenção zero.",
        "correct": false,
        "explanation": "Incorreto. VACUUM com zero destruiria a capacidade de Time Travel."
      },
      {
        "id": "C",
        "text": "Acessar o histórico de navegação do Google Chrome do analista.",
        "correct": false,
        "explanation": "Incorreto. Não tem relação com o banco de dados."
      },
      {
        "id": "D",
        "text": "Delta Lake Time Travel (utilizando SELECT * FROM tbl TIMESTAMP AS OF '2025-01-10' ou VERSION AS OF n).",
        "correct": true,
        "explanation": "Correto. O Time Travel permite consultar versões históricas anteriores da tabela graças ao log imutável de transações (_delta_log)."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "O Delta Lake mantém um histórico transacional completo de commits. O Time Travel permite consultar versões prévias com `TIMESTAMP AS OF` ou `VERSION AS OF`, além de reverter estados com `RESTORE TABLE`."
  },
  {
    "id": 101,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Um engenheiro de dados júnior executa o comando: VACUUM prod.vendas.clientes RETAIN 0 HOURS;. Por padrão, o comando falha imediatamente com uma exceção de segurança. Qual é a razão dessa trava de segurança nativa do Databricks?",
    "options": [
      {
        "id": "A",
        "text": "O Databricks impede por padrão retenções menores que 7 dias (168 horas) para evitar a corrupção de leituras concorrentes em andamento e a destruição irreversível do Time Travel.",
        "correct": true,
        "explanation": "Correto. A trava de retenção padrão impede que transações ativas e históricos recentes de Time Travel sejam destruídos acidentalmente por exclusões prematuras de arquivos."
      },
      {
        "id": "B",
        "text": "O comando VACUUM só pode ser executado às sextas-feiras após as 18 horas.",
        "correct": false,
        "explanation": "Incorreto. VACUUM pode rodar a qualquer momento."
      },
      {
        "id": "C",
        "text": "O comando falha porque o VACUUM foi descontinuado e substituído pelo Excel.",
        "correct": false,
        "explanation": "Incorreto. VACUUM é um comando essencial de manutenção física do Delta Lake."
      },
      {
        "id": "D",
        "text": "A palavra RETAIN só aceita valores em minutos, não em horas.",
        "correct": false,
        "explanation": "Incorreto. RETAIN aceita horas (HOURS)."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "O parâmetro `spark.databricks.delta.retentionDurationCheck.enabled` (padrão true) bloqueia comandos VACUUM com períodos inferiores a 168 horas (7 dias) para garantir que consultas ativas e Time Travel não sejam comprometidos."
  },
  {
    "id": 102,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": "case-07",
    "question": "Qual comando oficial do Delta Lake compacta múltiplos arquivos Parquet pequenos (small files) em arquivos consolidados de tamanho ideal (~1 GB) para acelerar a velocidade de leitura das consultas?",
    "options": [
      {
        "id": "A",
        "text": "COMPACT TABLE prod.vendas.pedidos;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente no Delta Lake."
      },
      {
        "id": "B",
        "text": "OPTIMIZE prod.vendas.pedidos;",
        "correct": true,
        "explanation": "Correto. O comando OPTIMIZE realiza bin-packing, consolidando pequenos arquivos Parquet em arquivos grandes e otimizados de aproximadamente 1 GB."
      },
      {
        "id": "C",
        "text": "ZIP FILES ON prod.vendas.pedidos;",
        "correct": false,
        "explanation": "Incorreto. Não se utiliza ZIP para compactação colunar."
      },
      {
        "id": "D",
        "text": "MERGE SMALL FILES TO ONE;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "O comando `OPTIMIZE` é a instrução oficial de manutenção física para bin-packing de pequenos arquivos gerados por commits frequentes e streams em tabelas Delta."
  },
  {
    "id": 103,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Uma organização precisa capturar todas as alterações de linhas (inserts, updates com valores pré e pós-imagem, e deletes) ocorridas em uma tabela Delta para alimentar um sistema de auditoria externo. Qual recurso nativo do Delta Lake deve ser habilitado na tabela?",
    "options": [
      {
        "id": "A",
        "text": "Tirar um print diário da tela do computador e comparar visualmente.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      },
      {
        "id": "B",
        "text": "Desabilitar transações ACID no cluster.",
        "correct": false,
        "explanation": "Incorreto. Impossível no Delta Lake e corromperia os dados."
      },
      {
        "id": "C",
        "text": "Change Data Feed (CDF), ativando 'delta.enableChangeDataFeed' = true nas propriedades da tabela.",
        "correct": true,
        "explanation": "Correto. O Change Data Feed registra as mutações linha a linha em arquivos de log adicionais, permitindo consumir as alterações (pré e pós-imagem) de forma incremental."
      },
      {
        "id": "D",
        "text": "Configurar um trigger em JavaScript no navegador.",
        "correct": false,
        "explanation": "Incorreto. Não captura alterações no storage de dados."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "O Change Data Feed (CDF) do Delta Lake registra alterações incrementais em tabelas (inserts, updates e deletes) com metadados especiais (`_change_type`), permitindo arquiteturas de CDC eficientes."
  },
  {
    "id": 104,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Como uma aplicação consome as alterações registradas pelo Change Data Feed (CDF) de uma tabela Delta entre a versão 10 e a versão 15?",
    "options": [
      {
        "id": "A",
        "text": "SELECT * FROM prod.vendas.pedidos WHERE cdf_version BETWEEN 10 AND 15;",
        "correct": false,
        "explanation": "Incorreto. cdf_version não é uma coluna nativa da tabela principal."
      },
      {
        "id": "B",
        "text": "READ CHANGES FROM prod.vendas.pedidos;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente."
      },
      {
        "id": "C",
        "text": "FETCH LOGS FROM DELTA 10 TO 15;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inválida."
      },
      {
        "id": "D",
        "text": "SELECT * FROM table_changes('prod.vendas.pedidos', 10, 15);",
        "correct": true,
        "explanation": "Correto. A função table_changes(tabela, start_version, end_version) é a função SQL nativa para ler o feed de alterações do CDF."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "A função `table_changes('nome_da_tabela', start_version, [end_version])` retorna o conjunto de registros alterados acompanhados de colunas como `_change_type`, `_commit_version` e `_commit_timestamp`."
  },
  {
    "id": 105,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": "case-02",
    "question": "Um desenvolvedor tenta gravar um DataFrame PySpark com 5 colunas em uma tabela Delta existente que possui apenas 4 colunas. O comando falha com erro de Schema Mismatch. Qual opção deve ser passada na escrita para que o schema da tabela seja atualizado automaticamente para acomodar a quinta coluna?",
    "options": [
      {
        "id": "A",
        "text": ".option('mergeSchema', 'true')",
        "correct": true,
        "explanation": "Correto. A opção mergeSchema ativa a evolução de schema na escrita, adicionando novas colunas detectadas no DataFrame à tabela Delta de destino."
      },
      {
        "id": "B",
        "text": ".option('forceOverwrite', 'true')",
        "correct": false,
        "explanation": "Incorreto. Não é uma opção padrão do PySpark e sobrescreveria dados em vez de evoluir schema."
      },
      {
        "id": "C",
        "text": ".option('ignoreSchema', 'true')",
        "correct": false,
        "explanation": "Incorreto. Não existe no conector Delta."
      },
      {
        "id": "D",
        "text": ".option('disableACID', 'true')",
        "correct": false,
        "explanation": "Incorreto. Transações ACID não podem ser desativadas."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "O Delta Lake possui Schema Enforcement por padrão para prevenir corrupção acidental de dados. Para autorizar novos campos, o desenvolvedor deve passar explicitamente `.option('mergeSchema', 'true')`."
  },
  {
    "id": 106,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Em uma consulta Spark SQL que realiza um JOIN entre uma tabela de Fatos gigante de 50 Terabytes e uma tabela Dimensional de lojas pequena de apenas 15 Megabytes, o plano físico realiza um Shuffle Hash Join lento pela rede. Como acelerar essa consulta eliminando o shuffle de rede?",
    "options": [
      {
        "id": "A",
        "text": "Aumentar o tamanho da tabela pequena para 100 Terabytes duplicando dados.",
        "correct": false,
        "explanation": "Incorreto. Pioraria drasticamente o desempenho."
      },
      {
        "id": "B",
        "text": "Aplicar um Broadcast Join hint na tabela pequena: /*+ BROADCAST(lojas) */ ou broadcast(df_lojas).",
        "correct": true,
        "explanation": "Correto. O Broadcast Join envia uma cópia da tabela pequena para a memória de cada nó executor, eliminando completamente a troca massiva de dados (shuffle) da tabela gigante pela rede."
      },
      {
        "id": "C",
        "text": "Converter o join em um Cartesian Product irrestrito.",
        "correct": false,
        "explanation": "Incorreto. Produto cartesiano é a operação mais lenta e pesada possível."
      },
      {
        "id": "D",
        "text": "Executar a consulta em um computador sem conexão com a internet.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "O Broadcast Join é uma das técnicas mais eficazes de performance: quando uma das tabelas cabe confortavelmente na memória dos executores (< 10 MB por padrão, configurável até algumas centenas de MB), ela é transmitida a todos os nós, evitando o shuffle da tabela maior."
  },
  {
    "id": 107,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Ao analisar a Spark UI de um job que faz join entre duas tabelas grandes, o engenheiro observa que 199 tasks concluíram em 3 segundos, mas uma única task ficou travada executando por 45 minutos. Qual problema de dados está ocorrendo e como corrigi-lo?",
    "options": [
      {
        "id": "A",
        "text": "O computador do desenvolvedor travou com falta de bateria.",
        "correct": false,
        "explanation": "Incorreto. O processamento ocorre nos nós da nuvem."
      },
      {
        "id": "B",
        "text": "A tabela Delta foi excluída acidentalmente.",
        "correct": false,
        "explanation": "Incorreto. Se fosse excluída, a query falharia imediatamente."
      },
      {
        "id": "C",
        "text": "Data Skew (Desbalanceamento de Chave); aplicar a dica de Skew Join /*+ SKEW('tabela', 'coluna') */ ou técnica de Salting na chave do join.",
        "correct": true,
        "explanation": "Correto. O sintoma clássico de uma task demorando muito mais que as outras é o Data Skew (ex: muitos registros nulos ou valores repetidos na chave). O Skew Join hint divide a partição problemática em sub-partições menores balanceadas."
      },
      {
        "id": "D",
        "text": "O Apache Spark não suporta mais de 100 tarefas simultâneas.",
        "correct": false,
        "explanation": "Incorreto. O Spark suporta milhares de tasks paralelas."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "Data Skew ocorre quando uma chave de junção possui frequência desproporcionalmente alta (ex: `chave IS NULL` ou `codigo_pais = 'BR'`). O hint `/*+ SKEW('tabela', 'coluna') */` instrui o Catalyst a quebrar a partição enviesada em fatias menores balanceadas."
  },
  {
    "id": 108,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": "case-05",
    "question": "O recurso Adaptive Query Execution (AQE) está habilitado por padrão no Azure Databricks Runtime. Qual benefício o AQE traz dinamicamente durante a execução dos estágios de Shuffle?",
    "options": [
      {
        "id": "A",
        "text": "Desliga os nós workers a cada 10 segundos para economizar energia.",
        "correct": false,
        "explanation": "Incorreto. Não desliga nós durante a query."
      },
      {
        "id": "B",
        "text": "Apaga todas as tabelas temporárias criadas pelo usuário.",
        "correct": false,
        "explanation": "Incorreto. Tabelas temporárias duram enquanto a sessão persistir."
      },
      {
        "id": "C",
        "text": "Substitui o código PySpark por comandos em C++ manualmente.",
        "correct": false,
        "explanation": "Incorreto. O Photon faz compilação interna, não substituição manual de código de usuário."
      },
      {
        "id": "D",
        "text": "Coalesce dinâmico de partições de shuffle pós-estágio, convertendo automaticamente centenas de pequenas partições vazias em um número ótimo de partições consolidadas.",
        "correct": true,
        "explanation": "Correto. O AQE avalia estatísticas do shuffle em tempo de execução e junta partições pequenas (Dynamically Coalescing Shuffle Partitions), evitando sobrecarga de agendamento de tasks."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "Adaptive Query Execution (AQE) re-otimiza planos de consulta com base em estatísticas reais obtidas durante a execução de estágios intermediários, combinando partições pequenas e convertendo sort-merge joins em broadcast joins dinamicamente."
  },
  {
    "id": 109,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Qual comando SQL restaura a tabela 'prod.vendas.pedidos' para o estado exato em que ela se encontrava na versão 12 do log de transações Delta?",
    "options": [
      {
        "id": "A",
        "text": "RESTORE TABLE prod.vendas.pedidos TO VERSION AS OF 12;",
        "correct": true,
        "explanation": "Correto. O comando RESTORE TABLE desfaz alterações posteriores e reverte a tabela para a versão indicada no histórico do Delta Lake."
      },
      {
        "id": "B",
        "text": "ROLLBACK TRANSACTION TO 12;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe de banco relacional tradicional, não Delta Lake."
      },
      {
        "id": "C",
        "text": "RECOVER TABLE prod.vendas.pedidos VERSION 12;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente no Databricks."
      },
      {
        "id": "D",
        "text": "UNDO MERGE IN TABLE prod.vendas.pedidos;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "O comando `RESTORE TABLE <nome> TO VERSION AS OF <n>;` reverte o estado dos dados da tabela para a versão histórica especificada, gravando um novo commit de restauração no Delta Log."
  },
  {
    "id": 110,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Em uma tabela de 50 TB no Delta Lake particionada tradicionalmente por 'ano', 'mes' e 'dia', os analistas relatam lentidão crítica em consultas que filtram por 'categoria_produto' e 'id_cliente'. Por que o particionamento Hive não resolve essas consultas e por que o Liquid Clustering é a solução ideal?",
    "options": [
      {
        "id": "A",
        "text": "O particionamento Hive só aceita dados em formato PDF.",
        "correct": false,
        "explanation": "Incorreto. O Hive particiona Parquet, ORC, etc."
      },
      {
        "id": "B",
        "text": "O particionamento Hive só acelera filtros nas colunas de partição de diretório (ano/mes/dia); o Liquid Clustering permite clusterizar por até 4 colunas multidimensionais (ex: categoria_produto, id_cliente) e aplica poda de arquivos eficiente em todas elas simultaneamente.",
        "correct": true,
        "explanation": "Correto. O particionamento Hive é unidimensional e hierárquico. O Liquid Clustering organiza dados em espaço multidimensional, permitindo acelerar queries que filtram por combinações arbitrárias das colunas clusterizadas."
      },
      {
        "id": "C",
        "text": "O Liquid Clustering exige que todos os dados sejam apagados semanalmente.",
        "correct": false,
        "explanation": "Incorreto. Dados são mantidos de forma persistente e segura."
      },
      {
        "id": "D",
        "text": "O particionamento Hive foi proibido pela legislação internacional.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "O particionamento tradicional por data só ajuda queries que filtram por data. O Liquid Clustering (`CLUSTER BY (categoria, cliente, data)`) organiza os blocos de dados considerando todas as chaves ao mesmo tempo, provendo excelente poda de leitura para múltiplos padrões de consulta."
  },
  {
    "id": 111,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": "case-08",
    "question": "O que acontece nos bastidores quando uma transação no Delta Lake grava dados com sucesso na tabela?",
    "options": [
      {
        "id": "A",
        "text": "O cluster envia um e-mail para a Microsoft confirmando que a tabela foi gravada.",
        "correct": false,
        "explanation": "Incorreto. Não há envio de e-mails em commits de dados."
      },
      {
        "id": "B",
        "text": "O Delta Lake converte os arquivos Parquet em planilhas CSV para compatibilidade.",
        "correct": false,
        "explanation": "Incorreto. O Delta Lake utiliza exclusivamente Parquet para persistência colunar."
      },
      {
        "id": "C",
        "text": "Arquivos de dados Parquet são gravados no storage e um arquivo atômico de commit em JSON (ex: 00000000000000000010.json) é gravado no diretório _delta_log/ registrando a adição dos arquivos.",
        "correct": true,
        "explanation": "Correto. O protocolo Delta Lake garante atomicidade gravando os dados em Parquet e confirmando a transação via um arquivo de log JSON monotonicamente crescente no _delta_log/."
      },
      {
        "id": "D",
        "text": "O nó Driver apaga o metastore do Unity Catalog.",
        "correct": false,
        "explanation": "Incorreto. Metadados são preservados."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "Toda transação no Delta Lake é confirmada por um arquivo JSON atômico na pasta `_delta_log/`. Esse log registra quais arquivos Parquet foram adicionados (`add`) e quais foram removidos (`remove`), garantindo as propriedades ACID."
  },
  {
    "id": 112,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "A cada 10 commits no log transacional (_delta_log/), o Delta Lake executa uma ação automática de consolidação do estado. O que é gerado nessa consolidação?",
    "options": [
      {
        "id": "A",
        "text": "Uma cópia física de todos os dados do banco de dados para a lixeira.",
        "correct": false,
        "explanation": "Incorreto. Não descarta dados."
      },
      {
        "id": "B",
        "text": "A exclusão de todas as versões de Time Travel anteriores.",
        "correct": false,
        "explanation": "Incorreto. O Time Travel depende do log e checkpoints, e a limpeza só ocorre via VACUUM explícito."
      },
      {
        "id": "C",
        "text": "A reinicialização forçada do cluster Databricks.",
        "correct": false,
        "explanation": "Incorreto. Checkpoints são criados de forma transparente durante a escrita."
      },
      {
        "id": "D",
        "text": "Um arquivo Parquet de Checkpoint (ex: 00000000000000000010.checkpoint.parquet) compactando o estado consolidado de todos os commits anteriores.",
        "correct": true,
        "explanation": "Correto. Os arquivos de checkpoint em Parquet evitam que o Spark precise ler centenas de arquivos JSON para reconstruir o estado atual da tabela, acelerando drasticamente o tempo de leitura."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "A cada 10 transações, o Delta Lake grava um checkpoint em formato Parquet contendo o estado resumido de todos os arquivos ativos, evitando que leitores precisem reprocessar milhares de arquivos JSON individuais."
  },
  {
    "id": 113,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Um desenvolvedor precisa verificar o histórico completo de commits, autores, comandos e versões de uma tabela Delta. Qual comando SQL provê essa auditoria transacional?",
    "options": [
      {
        "id": "A",
        "text": "DESCRIBE HISTORY prod.vendas.pedidos;",
        "correct": true,
        "explanation": "Correto. A instrução DESCRIBE HISTORY lista todas as operações executadas na tabela Delta (versão, timestamp, userId, operation, operationParameters e notebook)."
      },
      {
        "id": "B",
        "text": "SHOW COMMITS IN prod.vendas.pedidos;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente."
      },
      {
        "id": "C",
        "text": "SELECT * FROM delta.log_history;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inválida no Databricks."
      },
      {
        "id": "D",
        "text": "LIST VERSIONS OF TABLE prod.vendas.pedidos;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "O comando `DESCRIBE HISTORY <nome_tabela>;` expõe a trilha completa de auditoria do Delta Log, revelando quem executou cada operação (ex: WRITE, MERGE, OPTIMIZE, VACUUM) e em qual timestamp."
  },
  {
    "id": 114,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": "case-03",
    "question": "Uma tabela de streaming recebe milhões de eventos por hora. O engenheiro observa que o diretório de dados possui mais de 80.000 arquivos Parquet pequenos de 2 MB cada, degradando o tempo de resposta de queries analíticas. Qual par de comandos deve ser executado periodicamente para sanear a saúde física da tabela?",
    "options": [
      {
        "id": "A",
        "text": "Executar DROP TABLE e recriar a tabela como CSV.",
        "correct": false,
        "explanation": "Incorreto. Causaria perda total de dados e pioraria o desempenho com CSV."
      },
      {
        "id": "B",
        "text": "Executar OPTIMIZE para consolidar os arquivos pequenos em arquivos de ~1 GB e executar VACUUM posteriormente para remover arquivos órfãos antigos.",
        "correct": true,
        "explanation": "Correto. O OPTIMIZE faz o bin-packing consolidando pequenos arquivos e o VACUUM expurga os arquivos antigos que foram substituídos pelos novos arquivos consolidados."
      },
      {
        "id": "C",
        "text": "Desligar o cluster e aguardar o Azure apagar os arquivos automaticamente.",
        "correct": false,
        "explanation": "Incorreto. O storage em nuvem não apaga arquivos sem comando explícito."
      },
      {
        "id": "D",
        "text": "Executar VACUUM RETAIN 0 HOURS seguido de RESTART WORKSPACE.",
        "correct": false,
        "explanation": "Incorreto. VACUUM com zero horas corrompe queries ativas e viola a segurança."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "A rotina padrão de manutenção física do Delta Lake é composta por `OPTIMIZE` (para compactar e bin-pack) e `VACUUM` (para expurgar arquivos substituídos que ultrapassaram o período de retenção)."
  },
  {
    "id": 115,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Qual propriedade de tabela do Delta Lake permite que novas gravações compactem pequenos arquivos automaticamente logo após a escrita de cada micro-lote, mitigando o problema de small files em streaming?",
    "options": [
      {
        "id": "A",
        "text": "spark.streaming.zipFiles = true",
        "correct": false,
        "explanation": "Incorreto. Propriedade inexistente."
      },
      {
        "id": "B",
        "text": "delta.neverSmallFiles = true",
        "correct": false,
        "explanation": "Incorreto. Propriedade inexistente."
      },
      {
        "id": "C",
        "text": "delta.autoCompact = true (combinado com delta.optimizeWrite = true).",
        "correct": true,
        "explanation": "Correto. As propriedades delta.autoCompact e delta.optimizeWrite compactam arquivos automaticamente durante as transações de escrita no Delta Lake."
      },
      {
        "id": "D",
        "text": "storage.compressEverything = true",
        "correct": false,
        "explanation": "Incorreto. Propriedade fictícia."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "`Optimize Write` organiza as partições antes de gravar para gerar arquivos maiores, enquanto `Auto Compact` executa uma compactação leve logo após a transação, mantendo a tabela saudável em streams contínuos."
  },
  {
    "id": 116,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Um engenheiro precisa sobrescrever apenas as vendas do ano de 2024 em uma tabela Delta particionada por 'ano', mantendo os dados dos outros anos 100% intactos. Qual opção do write em PySpark garante essa substituição atômica?",
    "options": [
      {
        "id": "A",
        "text": "df_2024.write.format('delta').mode('overwrite').saveAsTable('vendas')",
        "correct": false,
        "explanation": "Incorreto. O mode('overwrite') sem replaceWhere apagaria a tabela inteira e deixaria apenas os dados de 2024."
      },
      {
        "id": "B",
        "text": "df_2024.write.mode('append').saveAsTable('vendas')",
        "correct": false,
        "explanation": "Incorreto. O modo append duplicaria os registros de 2024 em vez de substituí-los."
      },
      {
        "id": "C",
        "text": "delete from vendas; insert into vendas;",
        "correct": false,
        "explanation": "Incorreto. Apagaria todos os anos antes de inserir."
      },
      {
        "id": "D",
        "text": "df_2024.write.format('delta').mode('overwrite').option('replaceWhere', 'ano = 2024').saveAsTable('vendas')",
        "correct": true,
        "explanation": "Correto. A opção replaceWhere realiza uma sobrescrita atômica e seletiva apenas na partição ou filtro especificado, sem apagar as demais partições da tabela."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "A opção `.option('replaceWhere', 'predicado')` combinada com `.mode('overwrite')` no Delta Lake garante substituição atômica e segura exclusivamente dos dados que atendem à condição do predicado."
  },
  {
    "id": 117,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": "case-06",
    "question": "No Spark Structured Streaming, qual modo de leitura de dados é utilizado para consultar uma tabela Delta que é continuamente atualizada por outro pipeline?",
    "options": [
      {
        "id": "A",
        "text": "spark.readStream.table('prod.silver.pedidos')",
        "correct": true,
        "explanation": "Correto. A API spark.readStream.table() lê uma tabela Delta como uma fonte contínua de streaming, consumindo novos commits em tempo real."
      },
      {
        "id": "B",
        "text": "spark.read.table('prod.silver.pedidos')",
        "correct": false,
        "explanation": "Incorreto. spark.read opera em batch estático, não como streaming contínuo."
      },
      {
        "id": "C",
        "text": "spark.streamFromTable('prod.silver.pedidos')",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente na API do PySpark."
      },
      {
        "id": "D",
        "text": "spark.table('prod.silver.pedidos').toStreaming()",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inválida."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "No PySpark, a leitura de uma tabela Delta governada como fonte de streaming é realizada com `spark.readStream.table('catalogo.schema.tabela')` ou `spark.readStream.format('delta').load('caminho')`."
  },
  {
    "id": 118,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Como o Delta Lake lida com duas gravações concorrentes disparadas exatamente no mesmo milissegundo sobre a mesma tabela, utilizando o protocolo Optimistic Concurrency Control (OCC)?",
    "options": [
      {
        "id": "A",
        "text": "O segundo commit apaga os dados do primeiro commit sem verificar nada.",
        "correct": false,
        "explanation": "Incorreto. O Delta Lake previne sobrescritas silenciosas e perda de dados."
      },
      {
        "id": "B",
        "text": "O primeiro commit conclui com sucesso; o segundo commit verifica se os arquivos que ele leu foram alterados pelo primeiro; se não houver conflito nos arquivos afetados, o segundo commit é confirmado; se houver conflito, ele falha com ConcurrentAppendException ou tenta novamente.",
        "correct": true,
        "explanation": "Correto. O OCC assume que a maioria das transações não colide; em caso de sobreposição direta no mesmo arquivo/partição, uma exceção de conflito de concorrência é disparada."
      },
      {
        "id": "C",
        "text": "O cluster trava permanentemente e exige reinicialização do workspace.",
        "correct": false,
        "explanation": "Incorreto. Concorrência é tratada de forma limpa na camada de transação do storage."
      },
      {
        "id": "D",
        "text": "O Spark converte a tabela para SQLite local.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "O Controle de Concorrência Otimista (OCC) garante transações ACID no Lakehouse. O segundo commit checa o Delta Log para validar se os dados lidos continuam válidos antes de consolidar sua escrita."
  },
  {
    "id": 119,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Qual é a principal recomendação para colunas que devem ser escolhidas para compor o Liquid Clustering (CLUSTER BY) em uma tabela Delta?",
    "options": [
      {
        "id": "A",
        "text": "Escolher 50 colunas com textos gigantes e descrições de produtos.",
        "correct": false,
        "explanation": "Incorreto. Recomenda-se clusterizar por no máximo 4 colunas de tipos numéricos, datas ou strings curtas."
      },
      {
        "id": "B",
        "text": "Escolher apenas colunas que contenham 100% de valores nulos.",
        "correct": false,
        "explanation": "Incorreto. Colunas nulas não proveem nenhum ganho de poda de leitura."
      },
      {
        "id": "C",
        "text": "Escolher colunas frequentemente utilizadas em filtros (WHERE), junções (JOIN) e de alta ou moderada cardinalidade (ex: id_cliente, codigo_pais, data_evento), limitando a até 4 colunas.",
        "correct": true,
        "explanation": "Correto. As colunas ideais para CLUSTER BY são aquelas que os usuários mais utilizam em cláusulas de filtro e junção, com cardinalidade suficiente para permitir boa poda estatística."
      },
      {
        "id": "D",
        "text": "Escolher colunas booleanas com apenas dois valores possíveis (True/False).",
        "correct": false,
        "explanation": "Incorreto. Colunas de cardinalidade binária muito baixa não aproveitam bem o espaço multidimensional do clustering."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "O DP-750 orienta selecionar até 4 colunas com alta/moderada cardinalidade que apareçam frequentemente em predicados de consultas (`WHERE col = ...`) para maximizar o data skipping do Liquid Clustering."
  },
  {
    "id": 120,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": "case-01",
    "question": "Um analista precisa checar quais arquivos Parquet físicos estão atualmente ativos e referenciados pela versão corrente de uma tabela Delta. Qual comando SQL detalha essa estrutura?",
    "options": [
      {
        "id": "A",
        "text": "SHOW DISK FILES ON prod.vendas.pedidos;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente."
      },
      {
        "id": "B",
        "text": "DESCRIBE PHYSICAL STORAGE prod.vendas.pedidos;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inválida."
      },
      {
        "id": "C",
        "text": "LIST DIRECTORY IN TABLE prod.vendas.pedidos;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente."
      },
      {
        "id": "D",
        "text": "SELECT * FROM prod.vendas.pedidos.files;",
        "correct": true,
        "explanation": "Correto. A tabela de metadados especiais <tabela>.files retorna a lista de arquivos Parquet físicos ativos, tamanho em bytes e estatísticas da versão atual."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "O Delta Lake disponibiliza tabelas de metadados auxiliares via notação de ponto, como `tabela.files` (para listar arquivos ativos e estatísticas de min/max) e `tabela.history`."
  },
  {
    "id": 121,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "multiple",
    "caseStudyId": null,
    "question": "Quais DUAS opções garantem que o Auto Loader (cloudFiles) consuma e converta tipos numéricos com inferência estrita de dados em vez de tratar tudo como StringType? (Selecione duas opções)",
    "options": [
      {
        "id": "A",
        "text": ".option('cloudFiles.inferColumnTypes', 'true')",
        "correct": true,
        "explanation": "Correto. Instrui o Auto Loader a inferir os tipos exatos de dados (INT, DOUBLE, DATE) em vez de manter StringType."
      },
      {
        "id": "B",
        "text": ".option('cloudFiles.schemaLocation', 'abfss://checkpoints@adls/schemas/...')",
        "correct": true,
        "explanation": "Correto. O schemaLocation é indispensável para persistir o schema inferido e registrar a evolução entre execuções."
      },
      {
        "id": "C",
        "text": ".option('cloudFiles.allStringsAlways', 'true')",
        "correct": false,
        "explanation": "Incorreto. Opção inexistente que forçaria tudo para string, o oposto do requisitado."
      },
      {
        "id": "D",
        "text": ".option('spark.ignoreTypes', 'true')",
        "correct": false,
        "explanation": "Incorreto. Opção inexistente."
      },
      {
        "id": "E",
        "text": ".option('cloudFiles.deleteCorruptedData', 'true')",
        "correct": false,
        "explanation": "Incorreto. Dados corrompidos devem ser resgatados em _rescued_data, não apagados."
      }
    ],
    "correctAnswers": [
      "A",
      "B"
    ],
    "overallExplanation": "Por padrão, o Auto Loader pode inferir campos JSON como string para evitar falhas. Ao configurar `cloudFiles.inferColumnTypes = true` com um `schemaLocation` persistente, ele infere tipos numéricos e temporais precisos."
  },
  {
    "id": 122,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Um engenheiro de dados executa a query: SELECT * FROM vendas_delta TIMESTAMP AS OF '2023-01-01';. A consulta falha com erro informando que o timestamp solicitado é anterior ao histórico disponível. O que provocou a perda das versões históricas anteriores?",
    "options": [
      {
        "id": "A",
        "text": "O Apache Spark desliga o Time Travel no primeiro dia de cada ano.",
        "correct": false,
        "explanation": "Incorreto. O Time Travel é contínuo e governado pelas políticas de retenção do storage."
      },
      {
        "id": "B",
        "text": "A execução periódica do comando VACUUM com período de retenção que expurgou os arquivos Parquet antigos anteriores à janela configurada.",
        "correct": true,
        "explanation": "Correto. O VACUUM remove permanentemente os arquivos de dados que foram desassociados do log há mais tempo que o período de retenção, impedindo Time Travel para além dessa data."
      },
      {
        "id": "C",
        "text": "A Microsoft desabilita o Delta Log automaticamente em contas gratuitas.",
        "correct": false,
        "explanation": "Incorreto. O Delta Log é parte essencial do formato e não é desabilitado."
      },
      {
        "id": "D",
        "text": "O arquivo de checkpoint Parquet corrompeu todo o metastore.",
        "correct": false,
        "explanation": "Incorreto. Checkpoints são redundantes e auto-recuperáveis."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "O Time Travel no Delta Lake é limitado pela retenção do comando `VACUUM`. Se o VACUUM foi executado expurgando arquivos com mais de 7 dias, consultas de Time Travel buscando dados de anos anteriores não encontrarão os Parquets físicos correspondentes."
  },
  {
    "id": 123,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": "case-04",
    "question": "Ao ler uma tabela Delta através do Databricks Disk Cache (aceleração de cache em disco SSD dos nós de computação), qual é o benefício para consultas analíticas repetitivas?",
    "options": [
      {
        "id": "A",
        "text": "O cache converte as consultas para HTML estático.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      },
      {
        "id": "B",
        "text": "O cache desliga o cluster após 3 segundos.",
        "correct": false,
        "explanation": "Incorreto. Cache não controla desligamento."
      },
      {
        "id": "C",
        "text": "As leituras subsequentes ocorrem diretamente a partir dos discos SSD locais ultrarrápidos das máquinas virtuais do cluster, evitando a latência de rede de download do ADLS Gen2.",
        "correct": true,
        "explanation": "Correto. O Databricks Disk Cache cria réplicas dos blocos de dados Parquet nos discos NVMe/SSD locais dos workers, acelerando consultas repetidas em até 5x a 10x."
      },
      {
        "id": "D",
        "text": "O cache armazena os dados no navegador do usuário.",
        "correct": false,
        "explanation": "Incorreto. O cache reside nos nós de computação do cluster."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "O Databricks Disk Cache utiliza os discos locais SSD/NVMe dos nós workers para armazenar cópias dos blocos remotos de Parquet lidos do ADLS Gen2, eliminando gargalos de rede em leituras subsequentes."
  },
  {
    "id": 124,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Qual comando SQL do Delta Lake restaura a tabela para o estado exato da transação anterior, desfazendo o último comando de DELETE que excluiu registros por engano?",
    "options": [
      {
        "id": "A",
        "text": "CTRL+Z ON prod.vendas.pedidos;",
        "correct": false,
        "explanation": "Incorreto. Não existe comando de atalho de teclado no SQL."
      },
      {
        "id": "B",
        "text": "DELETE UNDO FROM prod.vendas.pedidos;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inválida."
      },
      {
        "id": "C",
        "text": "REBOOT CLUSTER TO RESTORE DATA;",
        "correct": false,
        "explanation": "Incorreto. Reiniciar o cluster não altera os dados persistidos no storage."
      },
      {
        "id": "D",
        "text": "RESTORE TABLE prod.vendas.pedidos TO VERSION AS OF (SELECT max(version) - 1 FROM (DESCRIBE HISTORY prod.vendas.pedidos));",
        "correct": true,
        "explanation": "Correto. O RESTORE TABLE com a versão imediatamente anterior reverte com perfeição o estado da tabela, desfazendo a operação incorreta de exclusão."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "O `RESTORE TABLE` é a ferramenta definitiva de recuperação de desastres do Delta Lake, permitindo retornar a qualquer versão válida registrada no histórico do Delta Log."
  },
  {
    "id": 125,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Em um pipeline de streaming com Auto Loader, como o desenvolvedor garante que arquivos vazios de 0 bytes gerados por falhas de escrita na origem não quebrem o pipeline nem gerem registros nulos?",
    "options": [
      {
        "id": "A",
        "text": ".option('cloudFiles.ignoreCorruptFiles', 'true')",
        "correct": true,
        "explanation": "Correto. A opção ignoreCorruptFiles permite ignorar arquivos danificados ou vazios sem interromper o processamento contínuo dos demais arquivos válidos."
      },
      {
        "id": "B",
        "text": ".option('cloudFiles.crashImmediately', 'true')",
        "correct": false,
        "explanation": "Incorreto. A intenção é não quebrar o pipeline."
      },
      {
        "id": "C",
        "text": ".option('deleteDiskFiles', 'true')",
        "correct": false,
        "explanation": "Incorreto. Opção inexistente."
      },
      {
        "id": "D",
        "text": ".option('skipEverything', 'true')",
        "correct": false,
        "explanation": "Incorreto. Opção fictícia."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "A opção `cloudFiles.ignoreCorruptFiles` ou `cloudFiles.ignoreMissingFiles` oferece resiliência a anomalias temporárias de escrita na fonte sem derrubar o stream de produção."
  },
  {
    "id": 126,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": "case-07",
    "question": "Qual função de agregação de strings no PySpark permite consolidar múltiplos nomes de produtos comprados em um único pedido em uma única string separada por vírgula (ex: 'Notebook, Mouse, Teclado')?",
    "options": [
      {
        "id": "A",
        "text": "string_sum('nome_produto')",
        "correct": false,
        "explanation": "Incorreto. Função inexistente no Spark."
      },
      {
        "id": "B",
        "text": "concat_ws(', ', collect_list('nome_produto'))",
        "correct": true,
        "explanation": "Correto. collect_list() agrega os valores em um array de elementos e concat_ws() une os elementos em uma string delimitada."
      },
      {
        "id": "C",
        "text": "group_concat_excel('nome_produto')",
        "correct": false,
        "explanation": "Incorreto. Função fictícia."
      },
      {
        "id": "D",
        "text": "join_all_strings('nome_produto')",
        "correct": false,
        "explanation": "Incorreto. Função inexistente."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "No PySpark, a combinação de `collect_list()` (ou `collect_set()` para valores distintos) com `concat_ws(separador, array)` é a abordagem padrão para concatenação agregada de strings."
  },
  {
    "id": 127,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Para garantir a máxima performance de leitura em consultas SQL analíticas em uma tabela de Vendas de 100 TB no Azure Databricks, qual combinação de tecnologias modernas do Lakehouse é a recomendação oficial do DP-750?",
    "options": [
      {
        "id": "A",
        "text": "Formato CSV com particionamento Hive em 20 níveis de subpastas.",
        "correct": false,
        "explanation": "Incorreto. CSV é lento, não possui estatísticas colunares e 20 níveis de pastas causa lentidão extrema."
      },
      {
        "id": "B",
        "text": "Tabelas temporárias em memória RAM gravadas em arquivos de texto sem cabeçalho.",
        "correct": false,
        "explanation": "Incorreto. Sem persistência e inviável para 100 TB."
      },
      {
        "id": "C",
        "text": "Formato Delta Lake acelerado por Photon Engine, com Liquid Clustering (CLUSTER BY) e Deletion Vectors habilitados.",
        "correct": true,
        "explanation": "Correto. Essa é a arquitetura moderna padrão ouro: Delta Lake colunar + Photon SIMD em C++ + Liquid Clustering multidimensional + Deletion Vectors para mutações rápidas."
      },
      {
        "id": "D",
        "text": "Formato JSON compactado com GZIP sem índice nem metadados.",
        "correct": false,
        "explanation": "Incorreto. JSON exige parsing de texto caro e não suporta poda eficiente de colunas."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "A pilha de alta performance do Databricks no exame DP-750 combina o motor Photon, o protocolo Delta Lake com Deletion Vectors e o layout físico governado pelo Liquid Clustering."
  },
  {
    "id": 128,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "O que acontece se uma consulta de leitura tentar ler uma tabela Delta enquanto outro pipeline de escrita está adicionando novos arquivos Parquet em um commit em andamento?",
    "options": [
      {
        "id": "A",
        "text": "A consulta de leitura falha com erro de Deadlock no banco de dados.",
        "correct": false,
        "explanation": "Incorreto. Delta Lake não utiliza locks tradicionais pessimistas de banco relacional."
      },
      {
        "id": "B",
        "text": "A consulta de leitura lê metade das linhas novas e metade das antigas gerando inconsistência.",
        "correct": false,
        "explanation": "Incorreto. Viola a garantia de atomicidade e consistência ACID do Delta Lake."
      },
      {
        "id": "C",
        "text": "O cluster de leitura é pausado até o pipeline de escrita terminar.",
        "correct": false,
        "explanation": "Incorreto. Não há bloqueio mútuo entre leitura e escrita."
      },
      {
        "id": "D",
        "text": "A consulta de leitura lê snapshot isolado consistente da versão anterior confirmada no Delta Log, sem sofrer bloqueio (locks) nem ler dados inconsistentes 'fantasmas'.",
        "correct": true,
        "explanation": "Correto. Graças ao isolamento de snapshot (Snapshot Isolation) do Delta Lake, leitores nunca bloqueiam escritores e escritores nunca bloqueiam leitores."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "O Delta Lake implementa Snapshot Isolation: o leitor consulta o snapshot imutável validado pelo último commit JSON confirmado, garantindo leitura consistente mesmo durante escritas massivas simultâneas."
  },
  {
    "id": 129,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": "case-02",
    "question": "Um engenheiro de dados precisa calcular a média móvel de faturamento dos últimos 7 dias para cada loja física. Qual cláusula de Window specification atende a esse cálculo?",
    "options": [
      {
        "id": "A",
        "text": "Window.partitionBy('id_loja').orderBy('data_venda').rowsBetween(-6, 0)",
        "correct": true,
        "explanation": "Correto. A cláusula rowsBetween(-6, 0) define um frame de janela que inclui as 6 linhas anteriores mais a linha atual, totalizando os 7 dias para a média móvel."
      },
      {
        "id": "B",
        "text": "Window.partitionBy('id_loja').unboundedPreceding()",
        "correct": false,
        "explanation": "Incorreto. unboundedPreceding calcularia o acumulado desde o início dos tempos, não a janela móvel de 7 dias."
      },
      {
        "id": "C",
        "text": "Window.orderBy('data_venda').rangeBetween(0, 7)",
        "correct": false,
        "explanation": "Incorreto. Incluiria dias futuros, não os últimos 7 dias."
      },
      {
        "id": "D",
        "text": "GROUP BY id_loja",
        "correct": false,
        "explanation": "Incorreto. GROUP BY simples colapsa as linhas e não mantém a granularidade diária da média móvel."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "A especificação de frame `rowsBetween(-6, 0)` ou `rangeBetween(-INTERVAL 6 DAYS, CURRENT ROW)` em conjunto com `avg()` calcula médias móveis com fidelidade temporal em PySpark e SQL."
  },
  {
    "id": 130,
    "domain": 3,
    "domainName": "Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Qual comando SQL do Delta Lake limpa arquivos físicos órfãos com mais de 30 dias de uma tabela e emite um relatório com a lista de arquivos excluídos?",
    "options": [
      {
        "id": "A",
        "text": "DELETE OLD FILES IN prod.vendas.pedidos OLDER THAN 30 DAYS;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente no Delta Lake."
      },
      {
        "id": "B",
        "text": "VACUUM prod.vendas.pedidos RETAIN 720 HOURS DRY RUN; (para visualizar) e depois VACUUM prod.vendas.pedidos RETAIN 720 HOURS; (para executar).",
        "correct": true,
        "explanation": "Correto. 30 dias equivalem a 720 horas. O modificador DRY RUN permite auditar previamente quais arquivos serão expurgados antes da deleção definitiva."
      },
      {
        "id": "C",
        "text": "PURGE TABLE prod.vendas.pedidos WITH 30 DAYS;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente."
      },
      {
        "id": "D",
        "text": "DROP OBSOLETE FILES ON prod.vendas.pedidos;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "O comando `VACUUM <tabela> RETAIN <n> HOURS DRY RUN` lista os arquivos elegíveis para expurgo sem excluí-los fisicamente, permitindo validação prévia de segurança antes da deleção irreversível."
  },
  {
    "id": 131,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Uma indústria farmacêutica precisa construir um pipeline declarativo de qualidade rigorosa de dados onde a ingestão incremental de sensores laboratoriais seja validada automaticamente. Eles optam por Delta Live Tables (DLT) em Python. Qual decorador define uma tabela gerenciada que consome eventos incrementais contínuos?",
    "options": [
      {
        "id": "A",
        "text": "@spark.streaming_job()",
        "correct": false,
        "explanation": "Incorreto. Decorador inexistente no DLT."
      },
      {
        "id": "B",
        "text": "@azure.databricks_pipeline()",
        "correct": false,
        "explanation": "Incorreto. Decorador inexistente."
      },
      {
        "id": "C",
        "text": "@dlt.table com leitura via dlt.read_stream('tabela_fonte')",
        "correct": true,
        "explanation": "Correto. O decorador @dlt.table combinado com dlt.read_stream() define uma Streaming Table no Delta Live Tables, processando novos registros de forma incremental."
      },
      {
        "id": "D",
        "text": "@pyspark.dataframe_stream()",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente na API do DLT."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "No Delta Live Tables (DLT), `@dlt.table` define uma tabela gerenciada. Quando a função lê de uma fonte de streaming usando `dlt.read_stream()`, o DLT materializa uma Streaming Table incremental."
  },
  {
    "id": 132,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": "case-05",
    "question": "Em um pipeline Delta Live Tables (DLT), qual é a diferença fundamental entre uma Streaming Table e uma Materialized View?",
    "options": [
      {
        "id": "A",
        "text": "Streaming Tables apagam todos os dados após 2 minutos.",
        "correct": false,
        "explanation": "Incorreto. Tabelas de streaming são persistentes."
      },
      {
        "id": "B",
        "text": "Materialized Views não podem ser consultadas via SQL.",
        "correct": false,
        "explanation": "Incorreto. Materialized Views são consultadas com SQL padrão no Unity Catalog."
      },
      {
        "id": "C",
        "text": "Streaming Tables só funcionam com arquivos em disquete.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      },
      {
        "id": "D",
        "text": "Streaming Tables processam dados append-only de forma incremental gravando apenas novas linhas; Materialized Views recalculam agregações e transformações de negócio refletindo o estado atual da fonte.",
        "correct": true,
        "explanation": "Correto. Essa é a distinção central: Streaming Tables são ideais para fluxos contínuos/append-only (Bronze/Silver), enquanto Materialized Views são ideais para agregações e transformações de estado que mudam (Gold/BI)."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "No DLT, Streaming Tables lidam com fontes append-only sem recomputar dados passados. Materialized Views recalculam o resultado da query para refletir atualizações nas fontes (ex: joins, agregações e deduplicações)."
  },
  {
    "id": 133,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Um pipeline DLT na área de saúde precisa validar se a temperatura das vacinas está entre 2°C e 8°C. Se uma medição violar essa regra, a linha inválida deve ser descartada da tabela de destino Silver, mas o pipeline NÃO deve falhar e deve registrar a métrica de descarte no event log. Qual cláusula de Expectation atende a essa regra?",
    "options": [
      {
        "id": "A",
        "text": "@dlt.expect_or_drop('temperatura_valida', 'temperatura BETWEEN 2 AND 8')",
        "correct": true,
        "explanation": "Correto. A cláusula expect_or_drop descarta registros inválidos da tabela alvo, mantendo o pipeline em execução e gravando métricas no log de integridade."
      },
      {
        "id": "B",
        "text": "@dlt.expect_or_fail('temperatura_valida', 'temperatura BETWEEN 2 AND 8')",
        "correct": false,
        "explanation": "Incorreto. expect_or_fail abortaria imediatamente todo o pipeline ao encontrar a primeira linha inválida."
      },
      {
        "id": "C",
        "text": "@dlt.expect('temperatura_valida', 'temperatura BETWEEN 2 AND 8')",
        "correct": false,
        "explanation": "Incorreto. expect simples apenas registra um aviso no log, mas grava a linha inválida na tabela de destino."
      },
      {
        "id": "D",
        "text": "@dlt.drop_everything_if_error()",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "O DLT possui 3 níveis de Data Quality Expectations: `expect` (alerta no log e mantém a linha), `expect_or_drop` (descarta a linha inválida e continua o pipeline) e `expect_or_fail` (aborta o pipeline imediatamente na violação)."
  },
  {
    "id": 134,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Em um pipeline DLT de pagamentos bancários, a regra de conformidade exige que se o campo 'numero_conta' for nulo (IS NULL), o pipeline deve abortar e falhar a execução imediatamente para evitar pagamentos órfãos. Qual cláusula de Expectation deve ser usada?",
    "options": [
      {
        "id": "A",
        "text": "@dlt.expect('conta_obrigatoria', 'numero_conta IS NOT NULL')",
        "correct": false,
        "explanation": "Incorreto. expect simples deixaria a linha nula entrar na tabela."
      },
      {
        "id": "B",
        "text": "@dlt.expect_or_fail('conta_obrigatoria', 'numero_conta IS NOT NULL')",
        "correct": true,
        "explanation": "Correto. A cláusula expect_or_fail interrompe imediatamente a execução da tarefa se qualquer registro violar a regra de qualidade."
      },
      {
        "id": "C",
        "text": "@dlt.expect_or_drop('conta_obrigatoria', 'numero_conta IS NOT NULL')",
        "correct": false,
        "explanation": "Incorreto. expect_or_drop descartaria a linha silenciosamente, sem falhar o pipeline como exigido."
      },
      {
        "id": "D",
        "text": "@dlt.ignore_nulls_always()",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "Quando uma violação de qualidade de dados é inaceitável para o negócio, utiliza-se `@dlt.expect_or_fail(nome, condicao)`, que aborta a execução do pipeline assim que um registro violador é detectado."
  },
  {
    "id": 135,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": "case-08",
    "question": "Uma empresa precisa processar um feed contínuo de Change Data Capture (CDC) gerado por um banco SQL Server contendo inserções, atualizações e exclusões lógicas. Qual função nativa do Delta Live Tables simplifica a aplicação dessas alterações diretamente em uma tabela Silver?",
    "options": [
      {
        "id": "A",
        "text": "dlt.merge_into_manual_sql()",
        "correct": false,
        "explanation": "Incorreto. Função inexistente no DLT."
      },
      {
        "id": "B",
        "text": "spark.sql('COPY INTO ...')",
        "correct": false,
        "explanation": "Incorreto. COPY INTO não processa logs de CDC com deleções e atualizações ordenadas."
      },
      {
        "id": "C",
        "text": "dlt.apply_changes(target='...', source='...', keys=['id'], sequence_by='timestamp', apply_as_deletes='operacao = \"DELETE\"')",
        "correct": true,
        "explanation": "Correto. A API dlt.apply_changes() processa feeds CDC automaticamente, lidando com chegadas fora de ordem (sequence_by), chaves de upsert e deleções para SCD Tipo 1 ou Tipo 2."
      },
      {
        "id": "D",
        "text": "dlt.truncate_and_reload()",
        "correct": false,
        "explanation": "Incorreto. Truncate recarrega tudo do zero, perdendo o benefício incremental do CDC."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "A instrução `dlt.apply_changes()` é o mecanismo nativo do Delta Live Tables para Change Data Capture (CDC), garantindo que inserts, updates e deletes sejam aplicados na ordem cronológica correta definida por `sequence_by`."
  },
  {
    "id": 136,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Ao configurar um pipeline Delta Live Tables no Databricks, qual é a diferença entre os modos 'Development' (Desenvolvimento) e 'Production' (Produção)?",
    "options": [
      {
        "id": "A",
        "text": "O modo 'Production' apaga todas as tabelas a cada 5 minutos.",
        "correct": false,
        "explanation": "Incorreto. Tabelas em produção são persistentes e protegidas."
      },
      {
        "id": "B",
        "text": "O modo 'Development' não suporta linguagem Python.",
        "correct": false,
        "explanation": "Incorreto. Suporta Python e SQL normalmente."
      },
      {
        "id": "C",
        "text": "O modo 'Production' é executado em computadores físicos no escritório da empresa.",
        "correct": false,
        "explanation": "Incorreto. Ambos executam na nuvem Azure."
      },
      {
        "id": "D",
        "text": "O modo 'Development' mantém o cluster ativo mesmo após a conclusão das execuções para acelerar iterações e desabilita retentativas automáticas; o modo 'Production' desliga clusters ociosos e reinicia automaticamente pipelines que sofrem falhas transitórias.",
        "correct": true,
        "explanation": "Correto. O modo Development prioriza agilidade de teste sem reboots de VM; o modo Production prioriza resiliência, SLAs e economia de DBUs."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "No DLT, o modo 'Development' reusa clusters para evitar o tempo de inicialização de VMs a cada clique e pausa retentativas para facilitar o debugging. O modo 'Production' implementa retries automáticos de falhas e desliga clusters ociosos."
  },
  {
    "id": 137,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Um arquiteto precisa auditar as métricas de qualidade de dados de um pipeline DLT (número de linhas lidas, linhas aprovadas e linhas descartadas por cada Expectation). Onde esses dados de telemetria são armazenados automaticamente?",
    "options": [
      {
        "id": "A",
        "text": "No Event Log do Delta Live Tables, armazenado em formato Delta Lake na pasta configurada no pipeline (ou consultável via system.dlt.event_log).",
        "correct": true,
        "explanation": "Correto. O DLT grava todas as métricas de qualidade, linhagem e eventos de execução em uma tabela Delta de Event Log dedicada."
      },
      {
        "id": "B",
        "text": "No bloco de notas do Windows de cada desenvolvedor.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      },
      {
        "id": "C",
        "text": "Apenas na memória RAM volátil que é apagada ao término do job.",
        "correct": false,
        "explanation": "Incorreto. O Event Log é persistido de forma permanente em Delta Lake."
      },
      {
        "id": "D",
        "text": "Em um e-mail diário com anexos em PDF enviado ao suporte da Azure.",
        "correct": false,
        "explanation": "Incorreto. Métricas são estruturadas em tabelas Delta para consulta SQL."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "O Event Log do DLT é uma tabela Delta que registra a saúde e métricas do pipeline. É possível executar consultas SQL sobre ele para calcular a taxa de dados descartados: `SELECT * FROM event_log WHERE event_type = 'expectation_metrics'`."
  },
  {
    "id": 138,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": "case-03",
    "question": "Uma organização precisa orquestrar um workflow complexo de 8 tarefas sequenciais e paralelas, composto por notebooks PySpark, tarefas SQL analíticas, execução de pipeline DLT e notificações por e-mail. Qual serviço do Azure Databricks deve ser utilizado?",
    "options": [
      {
        "id": "A",
        "text": "CRON tab no Linux pessoal do desenvolvedor.",
        "correct": false,
        "explanation": "Incorreto. Não é corporativo, não escala e depende de máquina local ligada."
      },
      {
        "id": "B",
        "text": "Databricks Workflows (Jobs multitarefas com DAG de dependências).",
        "correct": true,
        "explanation": "Correto. O Databricks Workflows é o orquestrador nativo totalmente gerenciado do Lakehouse para orquestrar DAGs de tarefas heterogêneas com dependências e controle de execução."
      },
      {
        "id": "C",
        "text": "Agendador de tarefas do Windows Server local.",
        "correct": false,
        "explanation": "Incorreto. Não gerencia clusters nem integra nativamente com recursos Databricks."
      },
      {
        "id": "D",
        "text": "Databricks FileStore.",
        "correct": false,
        "explanation": "Incorreto. FileStore é apenas armazenamento de arquivos no DBFS."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "O Databricks Workflows é o orquestrador oficial para pipelines de dados corporativos no Lakehouse, suportando múltiplos tipos de tarefas (Notebooks, Scripts, Python Wheels, SQL, DLT, dbt), dependências e monitoramento."
  },
  {
    "id": 139,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Em um Databricks Workflow multitarefas, a Tarefa 1 (Bronze Ingest) calcula o número total de linhas ingeridas e precisa passar esse valor numérico para a Tarefa 2 (Silver Transform) para validação de volume. Qual funcionalidade do Databricks Jobs permite compartilhar variáveis e métricas entre tarefas do mesmo DAG?",
    "options": [
      {
        "id": "A",
        "text": "Gravar o valor em um post-it colado no monitor.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      },
      {
        "id": "B",
        "text": "Passar o valor através da URL do navegador web.",
        "correct": false,
        "explanation": "Incorreto. Jobs em produção rodam de forma autônoma sem navegador."
      },
      {
        "id": "C",
        "text": "Task Values, utilizando dbutils.jobs.taskValues.set(key, value) na tarefa 1 e dbutils.jobs.taskValues.get(taskKey, key) na tarefa 2.",
        "correct": true,
        "explanation": "Correto. Task Values é a funcionalidade oficial para comunicação e passagem de parâmetros dinâmicos entre tarefas de um Databricks Workflow."
      },
      {
        "id": "D",
        "text": "Alterar o nome do cluster para o número de linhas ingeridas.",
        "correct": false,
        "explanation": "Incorreto. Inviável e tecnicamente sem sentido."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "A API `dbutils.jobs.taskValues` foi projetada especificamente para permitir que tarefas em um DAG compartilhem pequenos estados, contadores, IDs ou metadados de execução com tarefas downstream."
  },
  {
    "id": 140,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Um job multitarefa de 6 etapas falhou na etapa 5 devido a um timeout passageiro de conexão com uma API externa. As etapas 1, 2, 3 e 4 foram concluídas com sucesso e consumiram 45 minutos de processamento. Qual ação deve ser executada pelo operador de dados para economizar tempo e custos de DBUs?",
    "options": [
      {
        "id": "A",
        "text": "Reiniciar o job inteiro do zero, recalculando as etapas 1, 2, 3 e 4 novamente.",
        "correct": false,
        "explanation": "Incorreto. Desperdiça 45 minutos de computação e gera custos duplicados de DBUs."
      },
      {
        "id": "B",
        "text": "Excluir o workspace e recriar toda a infraestrutura da nuvem.",
        "correct": false,
        "explanation": "Incorreto. Desproporcional e destrutivo."
      },
      {
        "id": "C",
        "text": "Ignorar o erro e marcar o relatório como concluído.",
        "correct": false,
        "explanation": "Incorreto. Deixaria os dados incompletos em produção."
      },
      {
        "id": "D",
        "text": "Executar um Repair Run (Reparar Execução) no Databricks Workflows, que reexecutará exclusivamente a etapa 5 que falhou e suas dependências downstream.",
        "correct": true,
        "explanation": "Correto. O Repair Run evita o reprocessamento desnecessário das etapas 1 a 4 que já concluíram com sucesso, poupando tempo e DBUs."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "O recurso `Repair Run` é um dos diferenciais mais importantes de confiabilidade do Databricks Workflows: ele permite reexecutar apenas os nós falhados do DAG, aproveitando os outputs válidos das etapas anteriores."
  },
  {
    "id": 141,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": "case-06",
    "question": "Uma equipe de engenharia precisa gerenciar todos os seus recursos de dados (workflows, pipelines DLT, clusters e tabelas) como código (Infrastructure as Code - IaC) com controle de versão Git e automação de CI/CD. Qual ferramenta oficial da Databricks provê essa padronização?",
    "options": [
      {
        "id": "A",
        "text": "Databricks Asset Bundles (DABs) utilizando o arquivo databricks.yml.",
        "correct": true,
        "explanation": "Correto. Databricks Asset Bundles (DABs) é o padrão oficial de IaC e CI/CD para declarar, versionar, validar e implantar pipelines e recursos Databricks em múltiplos ambientes."
      },
      {
        "id": "B",
        "text": "Docker Compose executando containers locais em notebooks.",
        "correct": false,
        "explanation": "Incorreto. Docker Compose não gerencia recursos na nuvem do Azure Databricks."
      },
      {
        "id": "C",
        "text": "Scripts manuais em VBA no Excel.",
        "correct": false,
        "explanation": "Incorreto. Incompatível com DevOps moderno de dados."
      },
      {
        "id": "D",
        "text": "Terraform local sem suporte ao Databricks Provider.",
        "correct": false,
        "explanation": "Incorreto. DABs é a ferramenta nativa de bundles oficial do exame DP-750."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "Databricks Asset Bundles (DABs) permitem definir pipelines, jobs e configurações em arquivos YAML (`databricks.yml`), suportando validação estática (`databricks bundle validate`) e deploys automatizados em CI/CD."
  },
  {
    "id": 142,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Qual comando da Databricks CLI é utilizado para validar a sintaxe dos arquivos YAML, caminhos de notebooks e definições de recursos de um bundle antes de qualquer deploy?",
    "options": [
      {
        "id": "A",
        "text": "databricks bundle test-everything",
        "correct": false,
        "explanation": "Incorreto. Comando inexistente."
      },
      {
        "id": "B",
        "text": "databricks bundle validate",
        "correct": true,
        "explanation": "Correto. O comando databricks bundle validate checa a sintaxe estrutural do databricks.yml e a existência dos recursos sem alterar o ambiente."
      },
      {
        "id": "C",
        "text": "az databricks bundle check-syntax",
        "correct": false,
        "explanation": "Incorreto. Comando inexistente na Azure CLI."
      },
      {
        "id": "D",
        "text": "databricks check --all-yaml",
        "correct": false,
        "explanation": "Incorreto. Comando inexistente."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "A instrução `databricks bundle validate` verifica se a sintaxe do bundle, variáveis e referências a arquivos de código estão corretas, sendo o passo obrigatório inicial em esteiras de CI/CD."
  },
  {
    "id": 143,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Qual comando da Databricks CLI realiza o deploy e a execução imediata de um job chamado 'pipeline_vendas' no ambiente de produção definido como target 'prod'?",
    "options": [
      {
        "id": "A",
        "text": "databricks deploy-all --force-prod --run-now",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente."
      },
      {
        "id": "B",
        "text": "git push origin prod --auto-deploy",
        "correct": false,
        "explanation": "Incorreto. O git push atualiza o repositório, mas o comando oficial de bundle é via Databricks CLI."
      },
      {
        "id": "C",
        "text": "databricks bundle deploy -t prod && databricks bundle run -t prod pipeline_vendas",
        "correct": true,
        "explanation": "Correto. O comando deploy com flag -t prod implanta os recursos no target especificado e bundle run -t prod executa o job."
      },
      {
        "id": "D",
        "text": "az databricks job start --prod pipeline_vendas",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inválida."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "O fluxo de trabalho com DABs utiliza `databricks bundle deploy -t <target>` para publicar a infraestrutura como código e `databricks bundle run -t <target> <job_key>` para disparar a execução."
  },
  {
    "id": 144,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": "case-01",
    "question": "Em um pipeline de CI/CD corporativo no Azure DevOps para deploy de Databricks Asset Bundles em produção, como a esteira deve se autenticar no Azure Databricks sem utilizar senhas de desenvolvedores?",
    "options": [
      {
        "id": "A",
        "text": "Gravar o Personal Access Token (PAT) do estagiário de dados no arquivo README.md.",
        "correct": false,
        "explanation": "Incorreto. Violação gravíssima de segurança."
      },
      {
        "id": "B",
        "text": "Abrir uma sessão de navegador remoto e fazer login com usuário e senha manual a cada deploy.",
        "correct": false,
        "explanation": "Incorreto. Incompatível com automação de CI/CD."
      },
      {
        "id": "C",
        "text": "Desabilitar o firewall e liberar acesso anônimo sem credenciais.",
        "correct": false,
        "explanation": "Incorreto. Inadmissível em ambientes corporativos."
      },
      {
        "id": "D",
        "text": "Utilizar um Service Principal do Microsoft Entra ID com autenticação federada baseada em tokens OIDC (OpenID Connect) ou Client Secret corporativo.",
        "correct": true,
        "explanation": "Correto. Service Principals com federação OIDC garantem autenticação headless segura sem chaves expostas no código do pipeline de CI/CD."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "Esteiras de CI/CD modernas no Azure DevOps e GitHub Actions utilizam Service Principals do Microsoft Entra ID com federação de credenciais de carga de trabalho (OIDC), eliminando segredos hardcoded."
  },
  {
    "id": 145,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Ao analisar a Spark UI de uma consulta lenta, o engenheiro nota que em um dos estágios de Shuffle há a métrica: 'Spill (Memory): 45 GB' e 'Spill (Disk): 18 GB'. O que essa métrica indica e qual é a ação corretiva imediata?",
    "options": [
      {
        "id": "A",
        "text": "Os dados intermediários do shuffle excederam a memória RAM dos slots dos executores e foram gravados no disco local; aumentar o número de partições de shuffle (spark.sql.shuffle.partitions) ou usar VMs com mais memória (Memory-Optimized).",
        "correct": true,
        "explanation": "Correto. Spill ocorre quando os executores ficam sem RAM para acomodar partições de shuffle e são forçados a fazer swap em disco, degradando a performance."
      },
      {
        "id": "B",
        "text": "O cluster sofreu um ataque hacker de vazamento de dados.",
        "correct": false,
        "explanation": "Incorreto. Spill é uma métrica normal de gestão de memória interna do Spark."
      },
      {
        "id": "C",
        "text": "O Databricks apagou os dados do ADLS Gen2.",
        "correct": false,
        "explanation": "Incorreto. Dados persistem no storage."
      },
      {
        "id": "D",
        "text": "A consulta já terminou e não precisa de nenhuma ação.",
        "correct": false,
        "explanation": "Incorreto. Spill para disco é uma das maiores causas de lentidão em pipelines Spark."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "Spill (Memory/Disk) ocorre quando uma partição de dados é grande demais para caber na RAM do executor durante um join ou agregação com shuffle. A solução é aumentar o paralelismo (`spark.sql.shuffle.partitions`) ou migrar para instâncias com maior razão de memória por core."
  },
  {
    "id": 146,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Ao verificar o plano de execução de uma consulta no Spark através de EXPLAIN EXTENDED, o engenheiro procura confirmar se a aceleração do Photon Engine está ativa. Qual indício no plano físico confirma a execução em C++ vetorizado pelo Photon?",
    "options": [
      {
        "id": "A",
        "text": "A palavra 'JAVA_BYTECODE_TUNGSTEN' é repetida em todas as linhas.",
        "correct": false,
        "explanation": "Incorreto. Isso indicaria a execução clássica na JVM sem aceleração Photon."
      },
      {
        "id": "B",
        "text": "Os nós de execução do plano físico possuem o prefixo 'Photon' (ex: PhotonScan, PhotonFilter, PhotonGroupingAgg, PhotonShuffleExchangeExec).",
        "correct": true,
        "explanation": "Correto. O motor Photon substitui os operadores tradicionais de WholeStageCodegen da JVM por nós nativos com prefixo Photon."
      },
      {
        "id": "C",
        "text": "O plano físico é substituído por uma imagem PNG com a foto de uma lâmpada.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      },
      {
        "id": "D",
        "text": "Aparece uma mensagem informando que a consulta será executada no Microsoft Excel.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "Na Spark UI e nos planos físicos do Catalyst, a presença de operadores com prefixo `Photon` (ex: `PhotonFilter`, `PhotonScan`, `PhotonHashAggregate`) atesta que a execução está sendo realizada nativamente pelo motor vetorizado C++."
  },
  {
    "id": 147,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": "case-04",
    "question": "Por que o uso de funções definidas pelo usuário (UDFs) tradicionais escritas em Python nativo (com @udf) pode fazer com que uma consulta perca os benefícios de aceleração do Photon Engine?",
    "options": [
      {
        "id": "A",
        "text": "O Photon desinstala o Python do computador sempre que uma UDF é criada.",
        "correct": false,
        "explanation": "Incorreto. O interpretador Python continua existindo, apenas a query sofre fallback."
      },
      {
        "id": "B",
        "text": "UDFs Python consomem 100% dos créditos da Azure em 1 segundo.",
        "correct": false,
        "explanation": "Incorreto. Resposta exagerada e incorreta."
      },
      {
        "id": "C",
        "text": "UDFs Python tradicionais não podem ser executadas nativamente no motor C++ do Photon e forçam o Spark a serializar dados entre a JVM e o processo Python linha a linha (fallback), degradando a performance.",
        "correct": true,
        "explanation": "Correto. UDFs Python tradicionais forçam a execução fora do Photon, causando perda das otimizações vetorizadas e sobrecarga de serialização IPC."
      },
      {
        "id": "D",
        "text": "O Python não é uma linguagem suportada pelo Apache Spark.",
        "correct": false,
        "explanation": "Incorreto. PySpark é uma das principais interfaces do Spark."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "O motor Photon vetorizado opera nativamente em C++. Funções UDF Python linha a linha exigem serialização de dados via pipes locais, impedindo que os operadores sejam convertidos para nós Photon e desacelerando o processamento."
  },
  {
    "id": 148,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Uma organização precisa monitorar diariamente o custo de DBUs de todos os Databricks Workflows em execução para identificar jobs com custos anômalos. Qual consulta na tabela system.billing.usage calcula o total de DBUs consumidos por cada Job ID nos últimos 7 dias?",
    "options": [
      {
        "id": "A",
        "text": "SELECT * FROM system.access.audit WHERE action_name = 'JOB_COST';",
        "correct": false,
        "explanation": "Incorreto. system.access.audit registra eventos de segurança, não faturamento financeiro de DBUs."
      },
      {
        "id": "B",
        "text": "SELECT job_name, sum(money) FROM azure.billing_portal;",
        "correct": false,
        "explanation": "Incorreto. Consulta fictícia fora do schema de System Tables do Unity Catalog."
      },
      {
        "id": "C",
        "text": "SELECT sum(hours) FROM system.information_schema.jobs;",
        "correct": false,
        "explanation": "Incorreto. Information schema não registra consumo de faturamento."
      },
      {
        "id": "D",
        "text": "SELECT usage_metadata.job_id, SUM(usage_quantity) AS total_dbus FROM system.billing.usage WHERE usage_date >= current_date() - INTERVAL 7 DAYS AND usage_metadata.job_id IS NOT NULL GROUP BY 1 ORDER BY total_dbus DESC;",
        "correct": true,
        "explanation": "Correto. A coluna usage_quantity contém os DBUs e usage_metadata.job_id identifica o Workflow orquestrado."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "A tabela do sistema `system.billing.usage` registra o consumo de DBUs em `usage_quantity` com metadados do job em `usage_metadata.job_id`, permitindo relatórios precisos de FinOps por workload."
  },
  {
    "id": 149,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Um job multitarefa de engenharia de dados precisa ser disparado automaticamente assim que novos arquivos forem depositados em um container específico do ADLS Gen2, sem polling e sem agendamento fixo de horário. Qual tipo de gatilho (Trigger) do Databricks Workflows deve ser configurado?",
    "options": [
      {
        "id": "A",
        "text": "File Arrival Trigger (Gatilho por Chegada de Arquivo).",
        "correct": true,
        "explanation": "Correto. O File Arrival Trigger monitora um caminho de armazenamento e dispara o Databricks Workflow imediatamente após a detecção de novos arquivos."
      },
      {
        "id": "B",
        "text": "Cron Trigger semanal às sextas-feiras.",
        "correct": false,
        "explanation": "Incorreto. O agendamento por Cron é fixo e não reage à chegada imediata de arquivos."
      },
      {
        "id": "C",
        "text": "Trigger manual dependente de clique do usuário.",
        "correct": false,
        "explanation": "Incorreto. Não provê automação contínua de produção."
      },
      {
        "id": "D",
        "text": "Trigger por temperatura do data center.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "Databricks Workflows suporta `File Arrival Triggers`, permitindo que o job seja acionado por eventos de chegada de novos arquivos no storage em nuvem, garantindo baixa latência de orquestração."
  },
  {
    "id": 150,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": "case-07",
    "question": "Qual parâmetro de configuração em um Databricks Workflow impede que múltiplas execuções do mesmo job acumulem-se em fila simultaneamente quando a execução anterior demorar mais do que o esperado?",
    "options": [
      {
        "id": "A",
        "text": "Timeout = 0 seconds.",
        "correct": false,
        "explanation": "Incorreto. Timeout zero cancelaria o job imediatamente."
      },
      {
        "id": "B",
        "text": "Maximum concurrent runs = 1 (Execuções simultâneas máximas = 1).",
        "correct": true,
        "explanation": "Correto. Ao limitar max_concurrent_runs para 1, novas execuções agendadas são ignoradas ou enfileiradas ordenadamente sem sobrecarregar clusters concorrentes."
      },
      {
        "id": "C",
        "text": "Retry limit = 1000.",
        "correct": false,
        "explanation": "Incorreto. Limite alto de retentativas aumentaria a concorrência e o consumo de recursos."
      },
      {
        "id": "D",
        "text": "Auto-delete job on slow run.",
        "correct": false,
        "explanation": "Incorreto. Parâmetro inexistente."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "O atributo `max_concurrent_runs` define o número máximo de instâncias ativas simultâneas de um job. Configurar para 1 previne sobreposição de execuções concorrentes do mesmo pipeline."
  },
  {
    "id": 151,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Em um Databricks Asset Bundle (DABs), como um engenheiro define configurações específicas para o ambiente de desenvolvimento (dev) e sobrescreve para o ambiente de produção (prod) no mesmo arquivo databricks.yml?",
    "options": [
      {
        "id": "A",
        "text": "Criando 50 arquivos databricks.yml com nomes diferentes e copiando manualmente.",
        "correct": false,
        "explanation": "Incorreto. Péssima prática que duplica código e gera erros operacionais."
      },
      {
        "id": "B",
        "text": "Excluindo o arquivo databricks.yml antes de fazer deploy em produção.",
        "correct": false,
        "explanation": "Incorreto. Sem o arquivo de bundle, o deploy de DABs não funciona."
      },
      {
        "id": "C",
        "text": "Utilizando a seção 'targets:' com blocos independentes para 'dev' (ex: mode: development) e 'prod' (ex: mode: production) parametrizando variáveis de catálogo, workspace e clusters.",
        "correct": true,
        "explanation": "Correto. A seção 'targets' do databricks.yml permite declarar múltiplos ambientes mantendo o mesmo código de pipeline e parametrizando recursos."
      },
      {
        "id": "D",
        "text": "Instalando o Azure Databricks dentro de um pendrive USB.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "O recurso de `targets` no DABs (`databricks.yml`) viabiliza a parametrização de múltiplos ambientes (dev, staging, prod) em um único projeto de infraestrutura como código."
  },
  {
    "id": 152,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Ao analisar a Spark UI, um engenheiro observa tarefas que apresentam pausas longas de 'GC Time' (tempo de Garbage Collection da JVM) consumindo mais de 35% do tempo total de execução da task. Qual é a causa raiz provável e a ação corretiva recomendada?",
    "options": [
      {
        "id": "A",
        "text": "Causa: A tela do computador do analista está com brilho excessivo.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      },
      {
        "id": "B",
        "text": "Causa: A tabela Delta foi criada sem nome.",
        "correct": false,
        "explanation": "Incorreto. Tabelas exigem identificadores."
      },
      {
        "id": "C",
        "text": "Causa: O cabo de energia da máquina virtual foi desconectado.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      },
      {
        "id": "D",
        "text": "Causa: Criação excessiva de objetos temporários na memória Java/Scala da JVM; Ação: Migrar para clusters acelerados pelo Photon Engine (que gerencia memória fora da JVM em C++) ou otimizar transformações para evitar instanciação excessiva de objetos.",
        "correct": true,
        "explanation": "Correto. O Photon Engine elimina pausas de Garbage Collection da JVM executando os operadores nativamente em C++ fora da heap do Java."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "Pausas prolongadas de Garbage Collection (GC Time alto na Spark UI) decorrem de saturação da memória heap da JVM do Java. O motor Photon em C++ mitiga esse problema gerenciando a memória fora da JVM."
  },
  {
    "id": 153,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": "case-02",
    "question": "Como um operador do Databricks configura alertas de notificação em um Workflow para ser avisado caso um job crítico falhe ou demore mais de 60 minutos para concluir?",
    "options": [
      {
        "id": "A",
        "text": "Configurar 'Notifications' nas configurações do Job, adicionando e-mails ou webhooks (Slack/Teams) para os eventos 'Failure' e definir 'Duration threshold' para 60 minutos.",
        "correct": true,
        "explanation": "Correto. O Databricks Workflows possui suporte nativo para notificações de falha, sucesso e limite de tempo de duração (duration threshold) via e-mail e webhook."
      },
      {
        "id": "B",
        "text": "Ligar para a central de atendimento da Microsoft a cada hora.",
        "correct": false,
        "explanation": "Incorreto. Incompatível com monitoramento automatizado."
      },
      {
        "id": "C",
        "text": "Criar um loop infinito com while(True) print('alerta').",
        "correct": false,
        "explanation": "Incorreto. Travaria o nó e geraria custos desnecessários."
      },
      {
        "id": "D",
        "text": "Desabilitar o log do Spark para evitar registros de erro.",
        "correct": false,
        "explanation": "Incorreto. Ocultaria problemas e impediria diagnósticos."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "O Databricks Workflows suporta notificações orientadas a eventos e alertas de SLA (duration thresholds), enviando alertas por e-mail ou disparando webhooks para PagerDuty, Slack ou Microsoft Teams."
  },
  {
    "id": 154,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "multiple",
    "caseStudyId": null,
    "question": "Quais DUAS vantagens tornam o Databricks Asset Bundles (DABs) a ferramenta recomendada de automação de engenharia de software para projetos corporativos de Lakehouse? (Selecione duas opções)",
    "options": [
      {
        "id": "A",
        "text": "Exclui todos os dados do cliente após cada commit de Git.",
        "correct": false,
        "explanation": "Incorreto. DABs gerencia pipelines e recursos, não descarta dados de negócio."
      },
      {
        "id": "B",
        "text": "Permite executar o Databricks em computadores Commodore 64 sem nuvem.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      },
      {
        "id": "C",
        "text": "Permite versionar a infraestrutura completa de pipelines, jobs e permissões junto com o código de engenharia no repositório Git.",
        "correct": true,
        "explanation": "Correto. DABs aplica princípios de Infrastructure as Code (IaC) unificando código de negócio e definições de orquestração no mesmo repositório."
      },
      {
        "id": "D",
        "text": "Habilita testes automatizados e validação estática de sintaxe (databricks bundle validate) antes do deploy em ambientes produtivos.",
        "correct": true,
        "explanation": "Correto. A validação estática pré-deploy reduz falhas em produção e integra nativamente em esteiras de CI/CD."
      },
      {
        "id": "E",
        "text": "Substitui o motor Apache Spark por um interpretador de arquivos BAT do MS-DOS.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      }
    ],
    "correctAnswers": [
      "C",
      "D"
    ],
    "overallExplanation": "DABs une Infrastructure as Code (IaC), controle de versão Git, validação prévia de configurações e automação de deploys multi-ambiente, sendo a metodologia oficial do DP-750."
  },
  {
    "id": 155,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Em um pipeline de produção, um notebook executa o comando df.toPandas() em um DataFrame contendo 800 milhões de linhas. O que acontecerá durante a execução e qual é a boa prática recomendada?",
    "options": [
      {
        "id": "A",
        "text": "O comando executará em 1 milissegundo sem usar memória.",
        "correct": false,
        "explanation": "Incorreto. A coleta de centenas de milhões de linhas satura a rede e a memória do Driver."
      },
      {
        "id": "B",
        "text": "O nó Driver alocará automaticamente 500 Terabytes de swap no ADLS Gen2.",
        "correct": false,
        "explanation": "Incorreto. O Driver tentará alocar na memória física da VM e falhará."
      },
      {
        "id": "C",
        "text": "O comando enviará centenas de gigabytes de dados de todos os executores para a memória RAM do nó Driver, causando falha fatal por OutOfMemory (Driver OOM); deve-se evitar toPandas() com grandes volumes ou usar PySpark distribuído.",
        "correct": true,
        "explanation": "Correto. toPandas() coleta todo o dataset distribuído no nó único do Driver; grandes volumes causam Driver OOM imediatamente."
      },
      {
        "id": "D",
        "text": "O Pandas distribuirá o processamento em 100 máquinas virtuais.",
        "correct": false,
        "explanation": "Incorreto. A biblioteca Pandas tradicional opera estritamente em nó único."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "Operações como `df.collect()` e `df.toPandas()` puxam os dados de todos os nós workers para o Driver. Em grandes volumes, isso satura a memória do nó Driver e causa `java.lang.OutOfMemoryError`."
  },
  {
    "id": 156,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": "case-05",
    "question": "Qual recurso de governança do Unity Catalog monitora a linhagem ponta a ponta e permite avaliar o impacto em relatórios de Power BI antes de excluir uma tabela ou coluna da camada Gold?",
    "options": [
      {
        "id": "A",
        "text": "Histórico de navegação do navegador do desenvolvedor.",
        "correct": false,
        "explanation": "Incorreto. Não provê grafo corporativo de dependências."
      },
      {
        "id": "B",
        "text": "Um arquivo de texto README preenchido manualmente em 2019.",
        "correct": false,
        "explanation": "Incorreto. Documentação manual fica rapidamente desatualizada."
      },
      {
        "id": "C",
        "text": "Desligar o banco de dados e esperar reclamações de usuários.",
        "correct": false,
        "explanation": "Incorreto. Abordagem destrutiva e inaceitável em produção."
      },
      {
        "id": "D",
        "text": "Unity Catalog Automated Lineage (Linhagem Automatizada no Catalog Explorer).",
        "correct": true,
        "explanation": "Correto. O Catalog Explorer exibe o grafo visual de dependências upstream e downstream conectando fontes, tabelas Silver, tabelas Gold e relatórios de BI conectados."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "A Linhagem Automatizada do Unity Catalog mapeia as dependências entre consultas, tabelas e visualizações de BI, permitindo análise proativa de impacto antes de qualquer modificação de schema."
  },
  {
    "id": 157,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Um job orquestrado no Databricks Workflows precisa executar uma tarefa condicional: se a Tarefa 1 processar mais de 10.000 registros, executa a Tarefa A; caso contrário, executa a Tarefa B. Qual recurso do orquestrador viabiliza essa lógica?",
    "options": [
      {
        "id": "A",
        "text": "Tarefa do tipo 'If/else condition' (Condição Se/Senão) configurada no DAG do Databricks Workflow.",
        "correct": true,
        "explanation": "Correto. O Databricks Workflows suporta tarefas nativas de condição If/else que avaliam expressões booleanas e direcionam o fluxo de execução no grafo."
      },
      {
        "id": "B",
        "text": "Desconectar o cabo de rede da máquina virtual worker.",
        "correct": false,
        "explanation": "Incorreto. Provocaria falha no cluster."
      },
      {
        "id": "C",
        "text": "Criar dois workspaces Databricks diferentes na Azure.",
        "correct": false,
        "explanation": "Incorreto. Desnecessário e custoso."
      },
      {
        "id": "D",
        "text": "Instalar um robô físico que aperta botões no teclado do servidor.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "Tarefas do tipo `If/else condition` no Databricks Workflows permitem criar fluxos de decisão dinâmicos no DAG baseados em Task Values ou parâmetros do job sem código customizado de controle."
  },
  {
    "id": 158,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Em um pipeline Delta Live Tables em produção, como a equipe garante que tabelas criadas no pipeline sejam publicadas e consultáveis por outros analistas diretamente no Unity Catalog com governança RBAC?",
    "options": [
      {
        "id": "A",
        "text": "Gravar as tabelas em disquetes físicos.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      },
      {
        "id": "B",
        "text": "Configurar a propriedade 'Target' do pipeline DLT para um Catálogo e Schema governados no Unity Catalog (ex: catalog: prod_lakehouse, target schema: gold).",
        "correct": true,
        "explanation": "Correto. Ao definir um catálogo do Unity Catalog e um schema alvo nas configurações do DLT, as tabelas e visões materializadas são registradas com governança unificada."
      },
      {
        "id": "C",
        "text": "Exportar todos os dados para arquivos CSV sem schema.",
        "correct": false,
        "explanation": "Incorreto. Perde governança e desempenho."
      },
      {
        "id": "D",
        "text": "Desativar o Unity Catalog e publicar no Hive Metastore legado.",
        "correct": false,
        "explanation": "Incorreto. O Hive Metastore não possui a governança moderna exigida pelo DP-750."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "O Delta Live Tables integra nativamente com o Unity Catalog: basta configurar o catálogo de destino e schema na interface do pipeline para que as tabelas sejam criadas como securable objects no catálogo."
  },
  {
    "id": 159,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": "case-08",
    "question": "Ao verificar o plano físico de uma consulta de Join entre duas tabelas, o engenheiro identifica o operador 'CartesianProduct'. Qual é a implicação desse operador para o desempenho do cluster?",
    "options": [
      {
        "id": "A",
        "text": "O operador é a otimização mais rápida e eficiente do Apache Spark.",
        "correct": false,
        "explanation": "Incorreto. Produto cartesiano é a operação mais pesada e dispendiosa possível."
      },
      {
        "id": "B",
        "text": "O operador indica que a consulta foi concluída em zero segundos.",
        "correct": false,
        "explanation": "Incorreto. Indica exatamente o oposto: alto risco de timeout e lentidão."
      },
      {
        "id": "C",
        "text": "O operador multiplica cada linha da primeira tabela por todas as linhas da segunda tabela (produto cartesiano O(N*M)), causando consumo massivo de CPU, lentidão crítica e potencial esgotamento de memória.",
        "correct": true,
        "explanation": "Correto. CartesianProduct indica ausência ou ineficácia de predicado de junção, gerando uma explosão de linhas que sobrecarrega os nós do cluster."
      },
      {
        "id": "D",
        "text": "O operador desliga todos os discos SSD dos nós workers.",
        "correct": false,
        "explanation": "Incorreto. Não afeta hardware diretamente."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "A presença de `CartesianProduct` em planos físicos revela queries sem cláusula ON ou com condições booleanas incorretas, gerando multiplicação exponencial de linhas e travamento de clusters."
  },
  {
    "id": 160,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Uma organização multinacional precisa garantir que todos os deploys de código em seu Workspace do Azure Databricks passem por aprovação de Pull Request em repositório Git corporativo, com testes automatizados executando 'databricks bundle validate'. Como essa esteira garante conformidade com o exame DP-750?",
    "options": [
      {
        "id": "A",
        "text": "Exigindo que cada programador altere arquivos .py diretamente no portal da nuvem em produção.",
        "correct": false,
        "explanation": "Incorreto. Prática amadora e perigosa proibida em governança de engenharia de dados."
      },
      {
        "id": "B",
        "text": "Desabilitar o Git e utilizar mensagens de WhatsApp para trocar código.",
        "correct": false,
        "explanation": "Incorreto. Totalmente inadequado e sem conformidade."
      },
      {
        "id": "C",
        "text": "Copiar código via comandos de Ctrl+C e Ctrl+V no bloco de notas.",
        "correct": false,
        "explanation": "Incorreto. Sem rastreabilidade nem controle de versão."
      },
      {
        "id": "D",
        "text": "Implementando automação de CI/CD com Databricks Asset Bundles (DABs) e branch protection rules no Git, eliminando edições manuais diretas em produção.",
        "correct": true,
        "explanation": "Correto. A metodologia oficial exige esteiras declarativas de CI/CD via DABs e Git Folders, prevenindo modificações manuais não auditadas em ambientes produtivos."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "A governança de produção exigida no DP-750 requer automação de CI/CD via Databricks Asset Bundles, proteção de branches no Git e validação automatizada de código antes da promoção para produção."
  },
  {
    "id": 161,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Em um pipeline de streaming com DLT, o cluster precisa escalar trabalhadores de forma dinâmica para absorver picos de tráfego de dados na Black Friday sem exceder o orçamento mensal. Qual recurso de dimensionamento inteligente do DLT deve ser habilitado?",
    "options": [
      {
        "id": "A",
        "text": "Enhanced Autoscaling do Delta Live Tables, que otimiza a alocação de nós minimizando o tempo de resposta e desligando workers ociosos instantaneamente.",
        "correct": true,
        "explanation": "Correto. O Enhanced Autoscaling do DLT é especializado em workloads de streaming, escalando nós com base no atraso do backlog de mensagens sem desperdiçar recursos."
      },
      {
        "id": "B",
        "text": "Manter 500 máquinas ligadas durante todo o ano.",
        "correct": false,
        "explanation": "Incorreto. Geraria custo financeiro abusivo e desperdício de orçamento."
      },
      {
        "id": "C",
        "text": "Desabilitar o autoscaling e fixar em 1 único nó worker.",
        "correct": false,
        "explanation": "Incorreto. Provocaria fila de atraso e perda de SLA na Black Friday."
      },
      {
        "id": "D",
        "text": "Desligar o cluster durante os horários de pico.",
        "correct": false,
        "explanation": "Incorreto. Inviabilizaria as vendas da empresa."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "O `Enhanced Autoscaling` do Delta Live Tables é otimizado especificamente para streaming: ele analisa a taxa de chegada de dados e o tempo de fila para alocar a quantidade exata de nós necessária para cumprir o SLA."
  },
  {
    "id": 162,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": "case-03",
    "question": "Qual comando da Databricks CLI remove com segurança todos os recursos e jobs provisionados por um bundle no ambiente de desenvolvimento após a conclusão dos testes?",
    "options": [
      {
        "id": "A",
        "text": "rm -rf /databricks/all",
        "correct": false,
        "explanation": "Incorreto. Comando perigoso de sistema operacional que não limpa recursos na nuvem."
      },
      {
        "id": "B",
        "text": "databricks bundle destroy -t dev",
        "correct": true,
        "explanation": "Correto. O comando bundle destroy limpa e exclui todos os recursos criados pelo bundle no target especificado sem afetar outros ambientes."
      },
      {
        "id": "C",
        "text": "az databricks delete-everything --force",
        "correct": false,
        "explanation": "Incorreto. Comando inexistente na Azure CLI."
      },
      {
        "id": "D",
        "text": "databricks wipe-clean",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "O comando `databricks bundle destroy -t <target>` remove ordenadamente os jobs, pipelines e recursos provisionados pelo bundle naquele ambiente específico, garantindo higiene de nuvem e controle de custos."
  },
  {
    "id": 163,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Um engenheiro de dados observa falhas intermitentes em uma tarefa de notebook em um Databricks Workflow devido a indisponibilidade momentânea de 30 segundos na conexão com um serviço externo. Qual configuração da tarefa no Workflow resolve o problema sem necessidade de intervenção humana?",
    "options": [
      {
        "id": "A",
        "text": "Contratar um operador humano para ficar vigiando o monitor 24 horas por dia.",
        "correct": false,
        "explanation": "Incorreto. Ineficiente e custoso."
      },
      {
        "id": "B",
        "text": "Excluir a tarefa do pipeline para que o erro não apareça mais.",
        "correct": false,
        "explanation": "Incorreto. Deixaria o pipeline incompleto e sem os dados necessários."
      },
      {
        "id": "C",
        "text": "Configurar política de 'Retries' (Retentativas) na tarefa (ex: 3 tentativas com intervalo de espera).",
        "correct": true,
        "explanation": "Correto. A política nativa de Retries do Databricks Workflows reexecuta automaticamente tarefas que sofreram falhas transitórias com intervalos configurados."
      },
      {
        "id": "D",
        "text": "Desligar o alerta de falhas no e-mail corporativo.",
        "correct": false,
        "explanation": "Incorreto. Ocultar erros é má prática."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "A configuração de `Retries` em tarefas de Databricks Workflows fornece tolerância a falhas transitórias de rede ou APIs de terceiros, reexecutando a tarefa automaticamente conforme o limite estipulado."
  },
  {
    "id": 164,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Como um arquiteto pode verificar se o Unity Catalog está registrando corretamente a linhagem de dados gerada por um pipeline orquestrado pelo Databricks Workflows?",
    "options": [
      {
        "id": "A",
        "text": "Abrindo o arquivo win.ini no Windows.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      },
      {
        "id": "B",
        "text": "Procurando comentários no código fonte de 10 anos atrás.",
        "correct": false,
        "explanation": "Incorreto. Não reflete linhagem ativa do catálogo."
      },
      {
        "id": "C",
        "text": "Perguntando em fóruns públicos da internet.",
        "correct": false,
        "explanation": "Incorreto. Não acessa a linhagem privada da empresa."
      },
      {
        "id": "D",
        "text": "Consultando a tabela de sistema system.lineage.table_lineage ou navegando na aba 'Lineage' da tabela no Catalog Explorer.",
        "correct": true,
        "explanation": "Correto. As tabelas do schema system.lineage e o Catalog Explorer provêm visão completa e auditável da linhagem gerada por qualquer workflow."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "O schema de tabelas do sistema `system.lineage` (`table_lineage` e `column_lineage`) armazena programaticamente todo o histórico de transformações e dependências capturadas pelo Unity Catalog."
  },
  {
    "id": 165,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": "case-06",
    "question": "Em um Databricks Workflow com 4 tarefas em paralelo que convergem para uma tarefa final de agregação, qual condição de execução deve ser definida na tarefa final para que ela execute apenas quando TODAS as 4 tarefas anteriores terminarem com sucesso?",
    "options": [
      {
        "id": "A",
        "text": "Run if dependencies: 'All succeeded' (Todas com sucesso).",
        "correct": true,
        "explanation": "Correto. 'All succeeded' é a condição padrão que exige sucesso completo de todas as tarefas upstream antes de iniciar a etapa dependente."
      },
      {
        "id": "B",
        "text": "Run if dependencies: 'At least one failed'.",
        "correct": false,
        "explanation": "Incorreto. Dispararia se houvesse falha, ideal para tarefas de tratamento de erro ou alerta."
      },
      {
        "id": "C",
        "text": "Run if dependencies: 'None succeeded'.",
        "correct": false,
        "explanation": "Incorreto. Exigiria que todas falhassem."
      },
      {
        "id": "D",
        "text": "Run whenever random() > 0.5.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "No Databricks Workflows, a propriedade `Run if dependencies` controla o disparo condicional: `All succeeded` (padrão), `At least one succeeded`, `None failed`, `All failed` ou `At least one failed`."
  },
  {
    "id": 166,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Um analista precisa validar se o consumo de DBUs de um cluster de produção está seguindo a política de custos estabelecida pelo comitê de FinOps da empresa. Qual informação contida na tabela system.billing.usage identifica a política de cluster aplicada na criação da máquina?",
    "options": [
      {
        "id": "A",
        "text": "A cor do ícone do cluster no navegador web.",
        "correct": false,
        "explanation": "Incorreto. Não é um dado estruturado de faturamento."
      },
      {
        "id": "B",
        "text": "A coluna 'usage_metadata.cluster_policy_id', que registra o ID da Cluster Policy associada à execução.",
        "correct": true,
        "explanation": "Correto. O campo usage_metadata.cluster_policy_id em system.billing.usage permite rastrear se o cluster foi provisionado em conformidade com as políticas aprovadas."
      },
      {
        "id": "C",
        "text": "O endereço MAC da placa de rede física.",
        "correct": false,
        "explanation": "Incorreto. Metadado de baixo nível de rede que não identifica políticas de FinOps."
      },
      {
        "id": "D",
        "text": "O nome do usuário do Skype do desenvolvedor.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "A tabela `system.billing.usage` armazena o `cluster_policy_id` dentro do struct `usage_metadata`, permitindo correlacionar os gastos financeiros com as regras de governança e FinOps da organização."
  },
  {
    "id": 167,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Qual é a principal recomendação para garantir a rastreabilidade e integridade de deploys de código em workspaces de Desenvolvimento, Staging e Produção?",
    "options": [
      {
        "id": "A",
        "text": "Pedir para cada programador enviar seus arquivos .py por e-mail para o diretor de TI aos sábados.",
        "correct": false,
        "explanation": "Incorreto. Manual, inseguro e sem controle de versão."
      },
      {
        "id": "B",
        "text": "Criar apenas 1 único ambiente de desenvolvimento e executar testes diretamente na base de dados de produção dos clientes.",
        "correct": false,
        "explanation": "Incorreto. Viola normas básicas de segurança e governança corporativa."
      },
      {
        "id": "C",
        "text": "Utilizar Databricks Asset Bundles integrados a branches protegidas no Git (ex: main para prod, develop para dev) com deploys automatizados via Service Principal em CI/CD.",
        "correct": true,
        "explanation": "Correto. Este fluxo garante imutabilidade, revisão por pares (code review), testes de integridade e auditoria completa em todos os ambientes."
      },
      {
        "id": "D",
        "text": "Desabilitar o controle de versão e permitir edição anônima de código em produção.",
        "correct": false,
        "explanation": "Incorreto. Totalmente inaceitável em qualquer empresa séria."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "O padrão corporativo oficial do DP-750 para governança de código exige Databricks Asset Bundles (DABs), repositórios Git corporativos e esteiras de CI/CD automatizadas sem intervenção manual em produção."
  },
  {
    "id": 168,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": "case-01",
    "question": "Em uma esteira de CI/CD corporativa, qual comando da Databricks CLI é executado pelo pipeline de build para validar a integridade estrutural e parâmetros do bundle sem conectar a nenhum workspace nem disparar cobrança de DBUs?",
    "options": [
      {
        "id": "A",
        "text": "databricks bundle run --dry-run-all",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente."
      },
      {
        "id": "B",
        "text": "az databricks validate-bundle",
        "correct": false,
        "explanation": "Incorreto. Comando não pertencente à Azure CLI padrão."
      },
      {
        "id": "C",
        "text": "databricks test --syntax-only",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente."
      },
      {
        "id": "D",
        "text": "databricks bundle validate",
        "correct": true,
        "explanation": "Correto. databricks bundle validate valida localmente a consistência do databricks.yml e as referências aos arquivos de projeto sem custos de nuvem."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "O comando `databricks bundle validate` é o primeiro teste executado em pull requests em esteiras de CI/CD para certificar que o arquivo YAML e os artefatos de código estão sintaticamente perfeitos antes do deploy."
  },
  {
    "id": 169,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "O que acontece se uma tarefa em um Databricks Workflow estiver configurada com 'Timeout = 30 minutes' e sua execução atingir 31 minutos?",
    "options": [
      {
        "id": "A",
        "text": "O Databricks Workflows cancela a tarefa automaticamente com status TIMED_OUT e notifica os canais configurados (e-mail/webhook), evitando que jobs travados consumam DBUs indefinidamente.",
        "correct": true,
        "explanation": "Correto. O timeout atua como trava de segurança financeira contra jobs travados em loops infinitos ou esperas de rede."
      },
      {
        "id": "B",
        "text": "O cluster aumenta a memória RAM para 1 Terabyte para forçar o término.",
        "correct": false,
        "explanation": "Incorreto. O timeout encerra a execução por segurança."
      },
      {
        "id": "C",
        "text": "O computador do desenvolvedor é formatado.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      },
      {
        "id": "D",
        "text": "A consulta é enviada para ser processada em um servidor local on-premises.",
        "correct": false,
        "explanation": "Incorreto. Não há transferência automática para on-premises."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "Limites de timeout em tarefas de Databricks Workflows são essenciais para FinOps e governança: encerram execuções anômalas travadas antes que elas consumam orçamento excessivo de computação."
  },
  {
    "id": 170,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Ao analisar a Spark UI de um job com lentidão, o engenheiro percebe na aba 'Storage' que uma tabela em cache está consumindo 98% da memória RAM de todos os executores, forçando os estágios seguintes a sofrerem GC Pause constante. Qual comando deve ser inserido no código para liberar a memória desse cache após o uso?",
    "options": [
      {
        "id": "A",
        "text": "df.delete_all_memory()",
        "correct": false,
        "explanation": "Incorreto. Função inexistente no PySpark."
      },
      {
        "id": "B",
        "text": "df.unpersist() ou spark.catalog.clearCache()",
        "correct": true,
        "explanation": "Correto. unpersist() libera os blocos da memória e do disco alocados pelo cache de um DataFrame, restaurando a capacidade de RAM dos executores."
      },
      {
        "id": "C",
        "text": "reboot_spark_now()",
        "correct": false,
        "explanation": "Incorreto. Função inexistente."
      },
      {
        "id": "D",
        "text": "spark.conf.set('spark.memory.kill', 'true')",
        "correct": false,
        "explanation": "Incorreto. Propriedade fictícia."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "DataFrames persistidos com `.cache()` ou `.persist()` devem ser liberados com `.unpersist()` logo após a etapa que deles necessita, devolvendo memória RAM aos executores para evitar Garbage Collection agressivo."
  },
  {
    "id": 171,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": "case-04",
    "question": "Qual é a principal vantagem de utilizar Serverless Compute para Databricks Workflows em comparação com a criação manual de Job Clusters clássicos?",
    "options": [
      {
        "id": "A",
        "text": "Permite executar código sem nenhum acesso à internet.",
        "correct": false,
        "explanation": "Incorreto. Requer conexão em nuvem normal."
      },
      {
        "id": "B",
        "text": "Desabilita transações ACID para ganhar velocidade.",
        "correct": false,
        "explanation": "Incorreto. Delta Lake ACID permanece 100% ativo."
      },
      {
        "id": "C",
        "text": "Tempo de inicialização imediato (menos de 10 segundos vs 4-6 minutos de VM clássica), sem preocupação com cotas de vCPUs da assinatura Azure e gerenciamento automatizado de performance pela Databricks.",
        "correct": true,
        "explanation": "Correto. O Serverless Jobs elimina o atrito de inicialização a frio de máquinas virtuais clássicas e remove a dependência de cotas de VMs na assinatura da Azure."
      },
      {
        "id": "D",
        "text": "Substitui todas as linguagens por COBOL.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "Serverless Compute para Workflows reduz drasticamente o tempo total de execução de pipelines curtos (eliminando o boot time de 5 minutos de VMs) e abstrai o gerenciamento de infraestrutura da assinatura do cliente."
  },
  {
    "id": 172,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Em um Databricks Workflow, qual é a sintaxe correta para referenciar um parâmetro dinâmico chamado 'data_processamento' passado na execução do job dentro de um comando SQL ou notebook?",
    "options": [
      {
        "id": "A",
        "text": "$$param:data_processamento$$",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente no Databricks."
      },
      {
        "id": "B",
        "text": "SELECT param FROM windows_registry;",
        "correct": false,
        "explanation": "Incorreto. Inexistente."
      },
      {
        "id": "C",
        "text": "#[data_processamento]",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inválida."
      },
      {
        "id": "D",
        "text": "{{job.parameters.data_processamento}}",
        "correct": true,
        "explanation": "Correto. A sintaxe de substituição de parâmetros dinâmicos em Databricks Jobs utiliza chaves duplas: {{job.parameters.<param_name>}}."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "No Databricks Workflows, a interpolação de parâmetros dinâmicos de jobs e tarefas utiliza a sintaxe Jinja-like padrão: `{{job.parameters.<param_name>}}` ou `{{tasks.<task_name>.values.<key>}}`."
  },
  {
    "id": 173,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Um arquiteto precisa auditar quais usuários do Azure Databricks acessaram tabelas com classificação de dados confidenciais nos últimos 30 dias. Qual consulta SQL provê essa resposta?",
    "options": [
      {
        "id": "A",
        "text": "SELECT event_time, user_identity.email, request_params.table_name FROM system.access.audit WHERE service_name = 'unityCatalog' AND action_name = 'getTable' AND event_date >= current_date() - INTERVAL 30 DAYS;",
        "correct": true,
        "explanation": "Correto. system.access.audit armazena o histórico completo de acesso a securables do Unity Catalog, incluindo user_identity.email e table_name."
      },
      {
        "id": "B",
        "text": "SELECT * FROM system.billing.usage WHERE sku_name = 'CONFIDENTIAL';",
        "correct": false,
        "explanation": "Incorreto. system.billing.usage registra custos de faturamento de DBUs."
      },
      {
        "id": "C",
        "text": "SELECT * FROM default.user_history;",
        "correct": false,
        "explanation": "Incorreto. Tabela inexistente no padrão de auditoria do sistema."
      },
      {
        "id": "D",
        "text": "SHOW USERS ON SECRET_DATA;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "A tabela `system.access.audit` registra acessos de leitura e modificação a tabelas do Unity Catalog (`action_name = 'getTable'`, `generateTemporaryTableCredential`, etc.), atendendo a requisitos de conformidade SOX e LGPD."
  },
  {
    "id": 174,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": "case-07",
    "question": "Um engenheiro de dados configura uma tarefa em um Databricks Workflow com 'Retry policy: 3 retries, retry interval: 60 seconds'. A tarefa falha em sua primeira execução devido a uma instabilidade passageira no ADLS Gen2 e tem sucesso na segunda tentativa. Como o Databricks Workflows registra a execução final do job?",
    "options": [
      {
        "id": "A",
        "text": "O job é marcado como 'Critical Failure' e todos os dados são apagados.",
        "correct": false,
        "explanation": "Incorreto. A política de retentativa foi bem-sucedida."
      },
      {
        "id": "B",
        "text": "O job é marcado como 'Success' (Sucesso), registrando no histórico detalhado que a primeira tentativa falhou mas a segunda foi bem-sucedida dentro da política de retry aprovada.",
        "correct": true,
        "explanation": "Correto. A política de retry absorve a falha temporária e conclui a execução com sucesso sem disparar alertas desnecessários de parada de produção."
      },
      {
        "id": "C",
        "text": "O workspace é bloqueado permanentemente.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      },
      {
        "id": "D",
        "text": "A segunda tentativa é cancelada automaticamente.",
        "correct": false,
        "explanation": "Incorreto. A segunda tentativa é executada e tem sucesso."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "Políticas de Retry permitem que falhas transitórias de infraestrutura em nuvem sejam superadas automaticamente; o job é concluído com status de sucesso e os logs detalhados registram a retentativa para auditoria técnica."
  },
  {
    "id": 175,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Em um projeto com Databricks Asset Bundles (DABs), onde ficam definidos os clusters, permissões e tarefas dos jobs que serão sincronizados com o workspace?",
    "options": [
      {
        "id": "A",
        "text": "Em um arquivo de texto no disco C:\\ sem formato definido.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      },
      {
        "id": "B",
        "text": "Dentro de uma chave de registro do Windows.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      },
      {
        "id": "C",
        "text": "No arquivo de manifesto raiz databricks.yml e em arquivos YAML dentro da pasta 'resources/' do bundle.",
        "correct": true,
        "explanation": "Correto. A especificação padrão de DABs organiza recursos em databricks.yml e arquivos modulares dentro do diretório resources/ (ex: resources/*.yml)."
      },
      {
        "id": "D",
        "text": "Em um documento impresso guardado no cofre da empresa.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "O padrão arquitetural de Databricks Asset Bundles armazena as configurações globais em `databricks.yml` e as definições modulares de jobs, pipelines DLT e permissões na pasta `resources/` em formato YAML."
  },
  {
    "id": 176,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Como o Spark UI ajuda um engenheiro de dados a identificar que um estágio de consulta está sofrendo de Data Skew em comparação com um gargalo de falta de nós executores?",
    "options": [
      {
        "id": "A",
        "text": "No Data Skew, todas as tasks demoram exatamente o mesmo tempo de 1 hora.",
        "correct": false,
        "explanation": "Incorreto. Isso indicaria falta de paralelismo geral ou lentidão uniforme de I/O, não skew."
      },
      {
        "id": "B",
        "text": "A Spark UI fica na cor vermelha e fecha o navegador.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      },
      {
        "id": "C",
        "text": "O Spark desliga o nó Driver automaticamente.",
        "correct": false,
        "explanation": "Incorreto. Skew desacelera o estágio, não desliga o nó."
      },
      {
        "id": "D",
        "text": "No Data Skew, a barra de timeline e resumo de tasks exibe uma discrepância extrema (ex: 75th percentile = 2s, Max = 15 minutos), indicando que a imensa maioria das tasks concluiu rápido e apenas uma ou duas concentram volume de dados desproporcional.",
        "correct": true,
        "explanation": "Correto. O descompasso estatístico entre a mediana (ou 75th percentile) e o valor máximo (Max task duration) no estágio da Spark UI é a assinatura inequívoca de Data Skew."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "A tabela de sumário de métricas de tarefas na Spark UI (Min, 25th percentile, Median, 75th percentile, Max) permite identificar Skew imediatamente: quando a duração máxima ou o Shuffle Read Size do Max é ordens de grandeza maior que o 75th percentile."
  },
  {
    "id": 177,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": "case-02",
    "question": "Qual comando SQL do Unity Catalog concede permissão para um engenheiro de DevOps gerenciar e disparar um Databricks Workflow de produção sem torná-lo proprietário nem administrador do workspace?",
    "options": [
      {
        "id": "A",
        "text": "GRANT MANAGE RUN ON JOB <job_id> TO `engenheiro_devops`; (ou configuração de ACL 'Can Manage Run' no Job).",
        "correct": true,
        "explanation": "Correto. A permissão 'Can Manage Run' permite ao usuário ou grupo disparar, pausar e cancelar execuções de um job específico sem acesso a alterar definições de código estruturais."
      },
      {
        "id": "B",
        "text": "GRANT SUBSCRIPTION ADMIN ON CLOUD TO `engenheiro_devops`;",
        "correct": false,
        "explanation": "Incorreto. Violação do princípio do menor privilégio."
      },
      {
        "id": "C",
        "text": "DELETE JOB <job_id>;",
        "correct": false,
        "explanation": "Incorreto. Excluiria o job."
      },
      {
        "id": "D",
        "text": "ALTER WORKSPACE SET ROOT = `engenheiro_devops`;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "As permissões de Databricks Jobs seguem o modelo de controle de acesso granular: `Can View`, `Can Manage Run` (disparar e cancelar execuções) e `Can Manage` (editar e reconfigurar o job)."
  },
  {
    "id": 178,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Ao desenvolver um pipeline de dados em Python, por que é uma péssima prática utilizar laços de repetição 'for row in df.collect():' para aplicar transformações de negócio em vez de usar expressões nativas de DataFrames PySpark?",
    "options": [
      {
        "id": "A",
        "text": "O comando for row in df.collect() é proibido pela Microsoft e desconecta o Azure Databricks.",
        "correct": false,
        "explanation": "Incorreto. Não é proibido por software, mas degrada brutalmente a performance."
      },
      {
        "id": "B",
        "text": "for row in df.collect() força a coleta de todos os dados no nó Driver e executa em nó único em Python puro de forma serial, eliminando todo o paralelismo distribuído do Apache Spark e causando alto risco de OutOfMemory.",
        "correct": true,
        "explanation": "Correto. Essa é uma das maiores falhas de arquitetura de engenharia: transformar um processamento distribuído em um loop sequencial lento no nó único do Driver."
      },
      {
        "id": "C",
        "text": "O comando for row in df.collect() apaga os dados da tabela Delta.",
        "correct": false,
        "explanation": "Incorreto. Não apaga dados, apenas executa de forma lenta e ineficiente."
      },
      {
        "id": "D",
        "text": "Não há nenhuma diferença de velocidade em relação a DataFrames distribuídos.",
        "correct": false,
        "explanation": "Incorreto. A diferença é de minutos ou horas vs milissegundos."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "Transformações em Big Data devem ser expressas através de operações declarativas em DataFrames (`withColumn`, `when`, `expr`, `select`). Coletar dados com `collect()` e iterar em Python serial destrói o paralelismo e causa Driver OOM."
  },
  {
    "id": 179,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Uma organização de seguros precisa treinar um modelo de Machine Learning e alimentar painéis de BI com os mesmos dados da camada Gold. Para garantir governança, eles criam uma tabela gerenciada no Unity Catalog. Qual privilégio deve ser concedido aos cientistas de dados para que possam ler essa tabela em seus notebooks?",
    "options": [
      {
        "id": "A",
        "text": "GRANT DROP TABLE TO `cientistas_dados`;",
        "correct": false,
        "explanation": "Incorreto. Concederia permissão de exclusão acidental da tabela."
      },
      {
        "id": "B",
        "text": "GRANT CREATE CATALOG TO `cientistas_dados`;",
        "correct": false,
        "explanation": "Incorreto. Cientistas de dados não precisam de permissão administrativa de criação de catálogos para consultar tabelas."
      },
      {
        "id": "C",
        "text": "GRANT SELECT ON TABLE prod.analytics.seguros_gold TO `cientistas_dados`; (garantindo também USE CATALOG e USE SCHEMA na hierarquia pai).",
        "correct": true,
        "explanation": "Correto. O privilégio SELECT permite a leitura e consumo dos dados da tabela em notebooks, jobs e dashboards."
      },
      {
        "id": "D",
        "text": "GRANT ALL PRIVILEGES ON METASTORE TO ALL;",
        "correct": false,
        "explanation": "Incorreto. Violação severa de segurança corporativa."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "A leitura de securable objects no Unity Catalog exige `SELECT` no objeto folha, complementado por `USE CATALOG` no catálogo pai e `USE SCHEMA` no schema pai."
  },
  {
    "id": 180,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": "case-05",
    "question": "Qual parâmetro de linha de comando no Databricks Asset Bundles permite implantar o projeto forçando o target 'dev' sem precisar alterar o default no databricks.yml?",
    "options": [
      {
        "id": "A",
        "text": "databricks bundle deploy --target-is-always-dev-no-matter-what",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente."
      },
      {
        "id": "B",
        "text": "databricks deploy /dev",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inválida."
      },
      {
        "id": "C",
        "text": "az databricks deploy dev",
        "correct": false,
        "explanation": "Incorreto. Sintaxe incorreta."
      },
      {
        "id": "D",
        "text": "databricks bundle deploy -t dev",
        "correct": true,
        "explanation": "Correto. A flag -t ou --target especifica explicitamente o target de destino do bundle."
      }
    ],
    "correctAnswers": [
      "D"
    ],
    "overallExplanation": "O seletor `-t` (abreviação de `--target`) direciona as ações do Databricks CLI para o target configurado no `databricks.yml` (ex: `databricks bundle deploy -t dev` ou `databricks bundle deploy -t prod`)."
  },
  {
    "id": 181,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Ao investigar um incidente de segurança, o CISO precisa identificar se alguma credencial de usuário pessoal foi utilizada para modificar pipelines em produção nos últimos 60 dias. Qual consulta SQL provê essa informação na tabela de auditoria?",
    "options": [
      {
        "id": "A",
        "text": "SELECT event_time, user_identity.email, action_name, request_params FROM system.access.audit WHERE service_name = 'jobs' AND user_identity.email NOT LIKE '%@serviceprincipal.azure%' AND event_date >= current_date() - INTERVAL 60 DAYS;",
        "correct": true,
        "explanation": "Correto. A tabela system.access.audit permite isolar ações disparadas por identidades humanas em contraposição a Service Principals aprovados de CI/CD."
      },
      {
        "id": "B",
        "text": "SELECT * FROM system.billing.usage WHERE usage_quantity > 0;",
        "correct": false,
        "explanation": "Incorreto. system.billing.usage analisa cobrança de DBUs, não identidades de auditoria de alteração de jobs."
      },
      {
        "id": "C",
        "text": "SELECT * FROM default.audit_table_local;",
        "correct": false,
        "explanation": "Incorreto. Tabela inexistente no padrão de auditoria do sistema."
      },
      {
        "id": "D",
        "text": "SHOW USERS ON PRODUCTION;",
        "correct": false,
        "explanation": "Incorreto. Sintaxe inexistente."
      }
    ],
    "correctAnswers": [
      "A"
    ],
    "overallExplanation": "A tabela `system.access.audit` registra todas as interações com o serviço de jobs (`service_name = 'jobs'`), possibilitando segregar acessos de desenvolvedores humanos versus Service Principals automatizados."
  },
  {
    "id": 182,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": null,
    "question": "Qual é o comportamento do Databricks Workflows quando a opção 'Continuous' (Execução Contínua) é habilitada em um Job em vez de um agendamento Cron?",
    "options": [
      {
        "id": "A",
        "text": "O job roda uma única vez no dia 1º de janeiro de cada ano.",
        "correct": false,
        "explanation": "Incorreto. Isso seria agendamento anual estático."
      },
      {
        "id": "B",
        "text": "O job é reiniciado imediatamente após a conclusão bem-sucedida da execução anterior (ou reiniciado após breve intervalo em caso de falha), mantendo o pipeline ativo continuamente em tempo real.",
        "correct": true,
        "explanation": "Correto. O modo Continuous mantém o pipeline executando ininterruptamente, ideal para tarefas de streaming que não devem parar."
      },
      {
        "id": "C",
        "text": "O cluster é destruído e o workspace é encerrado.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      },
      {
        "id": "D",
        "text": "A execução é pausada para sempre.",
        "correct": false,
        "explanation": "Incorreto. O modo continuous é estritamente ativo e ininterrupto."
      }
    ],
    "correctAnswers": [
      "B"
    ],
    "overallExplanation": "O gatilho de execução `Continuous` em Databricks Workflows garante que o pipeline permaneça ativo 24/7: assim que uma execução termina ou sofre falha, o orquestrador sobe uma nova execução para manter a continuidade do streaming."
  },
  {
    "id": 183,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "single",
    "caseStudyId": "case-08",
    "question": "Como a funcionalidade Lakehouse Monitoring do Unity Catalog auxilia equipes de engenharia de dados e MLOps a monitorar a saúde de tabelas produtivas ao longo do tempo?",
    "options": [
      {
        "id": "A",
        "text": "Substitui os cientistas de dados por planilhas Excel estáticas.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      },
      {
        "id": "B",
        "text": "Envia uma carta física pelos Correios a cada anomalia detectada.",
        "correct": false,
        "explanation": "Incorreto. Resposta fictícia."
      },
      {
        "id": "C",
        "text": "Gera automaticamente perfis estatísticos, métricas de qualidade de dados, distribuições numéricas e relatórios de data drift (deriva de dados) sem necessidade de scripts manuais.",
        "correct": true,
        "explanation": "Correto. O Lakehouse Monitoring cria monitores automatizados no Unity Catalog que rastreiam completude, deriva estatística de dados e anomalias em tabelas Delta ao longo do tempo."
      },
      {
        "id": "D",
        "text": "Apaga automaticamente todas as linhas com valores maiores que 100.",
        "correct": false,
        "explanation": "Incorreto. Lakehouse Monitoring gera métricas e alertas, não exclui dados arbitrariamente."
      }
    ],
    "correctAnswers": [
      "C"
    ],
    "overallExplanation": "O Unity Catalog Lakehouse Monitoring analisa o histórico de tabelas e calcula métricas contínuas de integridade, volume, distribuições estatísticas e data drift, integrando diretamente com painéis do Databricks SQL."
  },
  {
    "id": 184,
    "domain": 4,
    "domainName": "Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%)",
    "type": "multiple",
    "caseStudyId": null,
    "question": "Um arquiteto de dados precisa desenhar a arquitetura de engenharia de dados corporativa no Azure Databricks para atender com excelência a todos os requisitos do exame oficial Microsoft DP-750. Quais são os QUATRO pilares fundamentais da solução oficial? (Selecione quatro opções)",
    "options": [
      {
        "id": "A",
        "text": "Orquestrar workloads de produção com Databricks Workflows multitarefas, Delta Live Tables (DLT com Expectations), DABs e esteiras automatizadas de CI/CD.",
        "correct": true,
        "explanation": "Correto. Pilar 4: Implantar e Manter Pipelines e Workloads (30-35%)."
      },
      {
        "id": "B",
        "text": "Desativar o Unity Catalog, voltar para montagens DBFS legadas com chaves hardcoded e usar clusters All-Purpose 24/7 sem autotermination.",
        "correct": false,
        "explanation": "Incorreto. Esta alternativa representa todas as más práticas legadas terminantemente reprovadas pelo exame DP-750."
      },
      {
        "id": "C",
        "text": "Configurar ambiente seguro e escalável utilizando VNet Injection (/26), Azure Private Link, Cluster Policies de FinOps e Serverless Compute.",
        "correct": true,
        "explanation": "Correto. Pilar 1: Configurar o Ambiente Azure Databricks (15-20%)."
      },
      {
        "id": "D",
        "text": "Implementar governança unificada no Unity Catalog com 3-Level Namespace, Volumes, Row Filters, Column Masks e auditoria via System Tables.",
        "correct": true,
        "explanation": "Correto. Pilar 2: Segurança e Governança com Unity Catalog (15-20%)."
      },
      {
        "id": "E",
        "text": "Construir pipelines de dados na Arquitetura Medallion utilizando Auto Loader, Delta Lake ACID, Liquid Clustering e Deletion Vectors.",
        "correct": true,
        "explanation": "Correto. Pilar 3: Preparar e Processar Dados em Batch e Streaming (30-35%)."
      }
    ],
    "correctAnswers": [
      "A",
      "C",
      "D",
      "E"
    ],
    "overallExplanation": "Estes quatro pilares correspondem aos quatro domínios oficiais da régua de certificação Microsoft Certified: Azure Databricks Data Engineer Associate (DP-750)."
  }
];

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { CASE_STUDIES, EXAM_QUESTIONS };
}
