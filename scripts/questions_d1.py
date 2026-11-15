#!/usr/bin/env python3
"""
Databricks Formation — Prepare to DP-750
Domínio 1: Configurar o Ambiente Azure Databricks (15–20%) — 38 Questões (1 a 38)
"""

def get_d1_questions():
    d1_specs = [
        # Q1
        {
            "scenario": "Uma organização financeira precisa implantar um Workspace do Azure Databricks com conformidade de segurança bancária. A equipe de infraestrutura de nuvem exige o uso de VNet Injection em uma Virtual Network existente gerenciada pela empresa. Quais são os requisitos obrigatórios para as subnets dessa VNet?",
            "options": [
                ("Configurar exatamente duas subnets dedicadas (host/public e container/private), com tamanho mínimo /26 cada, delegadas para Microsoft.Databricks/workspaces sem outros recursos alocados nelas.", True, "Correto. O VNet Injection no Azure Databricks exige exatamente duas subnets exclusivas delegadas para o provedor Microsoft.Databricks/workspaces, cada uma com máscara mínima /26."),
                ("Configurar uma única subnet compartilhada /24 compartilhada entre o cluster Databricks, Azure App Services e gateways de aplicação.", False, "Incorreto. O Databricks não suporta compartilhamento de subnet com outros serviços devido à deleção e gerenciamento de IPs pelo serviço."),
                ("Configurar quatro subnets /28 independentes para separar Driver, Workers, Storage DBFS e balanceador de carga.", False, "Incorreto. O requisito oficial são duas subnets (host e container) com tamanho mínimo /26."),
                ("Provisionar subnets sem nenhuma deleção de serviço e gerenciar manualmente todas as rotas BGP da VNet.", False, "Incorreto. A delegação de serviço para Microsoft.Databricks/workspaces é mandatória para que o Azure provisione os recursos de rede do Compute Plane.")
            ],
            "explanation": "No Azure Databricks, a VNet Injection exige duas subnets dedicadas: uma pública (host) e uma privada (container). Cada subnet deve ter no mínimo uma máscara /26 (fornecendo 64 IPs, sendo 5 reservados pelo Azure, suportando até 59 nós) e estar delegada exclusivamente para 'Microsoft.Databricks/workspaces'."
        },
        # Q2
        {
            "scenario": "A equipe de segurança de redes de uma empresa farmacêutica configurou um Network Security Group (NSG) corporativo para as subnets de um Workspace Azure Databricks com VNet Injection. Após a aplicação, os clusters falham ao iniciar com erro de timeout de conectividade. Qual regra de saída (outbound) do NSG é indispensável para a comunicação segura com o Control Plane?",
            "options": [
                ("Permitir tráfego de saída (outbound) na porta TCP 443 em direção à tag de serviço do Azure Databricks (AzureDatabricks) ou endereço do Control Plane.", True, "Correto. A Secure Cluster Connectivity (SCC) utiliza conexões de saída TLS na porta 443 para estabelecer o túnel relay seguro entre o Compute Plane e o Control Plane."),
                ("Abrir portas de entrada (inbound) TCP 22 e TCP 8080 públicas para permitir que o Control Plane envie comandos aos nós.", False, "Incorreto. O Databricks moderno opera com Secure Cluster Connectivity (No Public IP), não exigindo portas de entrada públicas abertas."),
                ("Habilitar roteamento BGP na porta 1521 para comunicação com o metastore gerenciado.", False, "Incorreto. A porta 1521 é típica de bancos Oracle e não se aplica à conexão entre planos do Databricks."),
                ("Desabilitar todas as regras de saída e forçar tráfego exclusivamente através de um proxy HTTP sem suporte a WebSockets.", False, "Incorreto. O Control Plane exige conexões HTTPS/WebSockets sem interceptação com quebra de SSL não suportada.")
            ],
            "explanation": "No modelo Secure Cluster Connectivity (NPIP), os nós do cluster iniciam conexões de saída na porta 443 para o Control Plane. Se o NSG bloquear a saída HTTPS para a tag de serviço AzureDatabricks ou Storage, os nós não conseguirão se registrar no cluster manager."
        },
        # Q3
        {
            "scenario": "Uma multinacional quer impedir que o tráfego de usuários navegando na Web UI do Azure Databricks trafegue pela internet pública. Qual funcionalidade do Azure deve ser implementada para garantir acesso estritamente privado ao front-end do workspace a partir da rede corporativa ExpressRoute?",
            "options": [
                ("Implementar um Azure Private Link com Private Endpoint do tipo Front-end (Web UI & REST API) associado à VNet corporativa.", True, "Correto. O Front-end Private Link conecta o cliente (navegadores de usuários e chamadas de API) ao Control Plane do Databricks através de um IP privado da VNet."),
                ("Habilitar o Azure Bastion diretamente dentro da máquina virtual do Driver do Spark.", False, "Incorreto. O Azure Bastion é utilizado para RDP/SSH em VMs individuais, não para conectar usuários à interface web gerenciada do Databricks."),
                ("Configurar uma VPN ponto-a-site ligada diretamente ao storage DBFS raiz.", False, "Incorreto. O storage DBFS raiz armazena bibliotecas e metadados, mas não hospeda a interface web do workspace."),
                ("Criar um Application Gateway público apontando para o endereço IP público dos nós de computação.", False, "Incorreto. Os nós de computação não possuem IPs públicos quando SCC está habilitado, e a Web UI reside no Control Plane.")
            ],
            "explanation": "O Azure Databricks suporta dois tipos de Private Link: Front-end (para tráfego de usuários/APIs até a Web UI no Control Plane) e Back-end (para tráfego dos nós de computação até o Control Plane). Para tráfego de usuários corporativos, o Front-end Private Link é o recurso requerido."
        },
        # Q4
        {
            "scenario": "Ao configurar Azure Private Link Front-end para um workspace em uma região do Azure, a documentação exige a criação de um workspace especial auxiliar chamado WebAuth Workspace. Qual é a finalidade técnica desse workspace auxiliar?",
            "options": [
                ("Atuar como ponto de terminação e callback para o fluxo de autenticação OAuth com o Microsoft Entra ID via rede privada.", True, "Correto. O WebAuth Workspace hospeda o endpoint de callback de autenticação privada do Microsoft Entra ID para que os usuários consigam logar via Private Link."),
                ("Armazenar todos os arquivos Parquet temporários gerados por queries analíticas de usuários.", False, "Incorreto. O workspace de WebAuth não armazena dados de negócio nem executa clusters de processamento."),
                ("Substituir o Metastore regional do Unity Catalog para workspaces governados.", False, "Incorreto. O Unity Catalog possui metastore independente e não se relaciona com o WebAuth workspace."),
                ("Executar os nós executores do Apache Spark em modo isolado multi-inquilino.", False, "Incorreto. O WebAuth workspace é puramente voltado à autenticação web via rede privada.")
            ],
            "explanation": "No Azure Databricks com Front-end Private Link, o fluxo de login do Microsoft Entra ID (Azure AD) precisa redirecionar o usuário para uma URL segura resolvida na rede privada. O WebAuth workspace é provisionado uma única vez por região para prover esse endpoint privado de autenticação."
        },
        # Q5
        {
            "scenario": "Um arquiteto de FinOps precisa restringir os desenvolvedores para que só possam criar clusters utilizando máquinas virtuais econômicas de uso geral (Standard_D4ds_v5) e impedir a alocação de nós caros com GPU ou excesso de memória. Qual recurso do Databricks atende a esse controle?",
            "options": [
                ("Criar uma Cluster Policy no Databricks definindo uma allowlist para o atributo 'node_type_id' contendo apenas 'Standard_D4ds_v5'.", True, "Correto. Cluster Policies permitem impor regras estritas em formato JSON com allowlist, blocklist ou valores fixos para tipos de nós, versões de DBR e autotermination."),
                ("Criar um script em Python no notebook que verifica o tipo da VM e executa dbutils.fs.rm() se for GPU.", False, "Incorreto. O script só rodaria após o cluster já ter sido iniciado e gerado cobrança no Azure."),
                ("Excluir as cotas de VM de GPU em toda a assinatura do Azure Subscription.", False, "Incorreto. Isso impactaria outros serviços de inteligência artificial da empresa fora do Databricks."),
                ("Configurar uma regra de firewall no NSG bloqueando portas de comunicação da GPU.", False, "Incorreto. O NSG atua na camada de rede TCP/IP, não controlando tipos de instâncias de hardware alocadas.")
            ],
            "explanation": "As Cluster Policies são o mecanismo oficial de governança e FinOps no Databricks. Através do JSON de política, os administradores definem 'node_type_id': {'type': 'allowlist', 'values': ['Standard_D4ds_v5']}, restringindo a criação de clusters fora da política."
        },
        # Q6
        {
            "scenario": "A equipe de governança detectou que desenvolvedores deixam clusters interativos All-Purpose ativos durante a noite e fins de semana, inflando a fatura de DBUs. Qual configuração de Cluster Policy garante que nenhum cluster interativo permaneça ocioso por mais de 20 minutos?",
            "options": [
                ("Definir o atributo 'autotermination_minutes' na Cluster Policy com valor fixo ou valor máximo de 20 minutos.", True, "Correto. Impor 'autotermination_minutes': {'type': 'fixed', 'value': 20} ou {'type': 'range', 'maxValue': 20} impede que o usuário desmarque ou aumente o tempo de inatividade."),
                ("Instalar um job no Azure Data Factory que envia um comando de kill a cada 24 horas.", False, "Incorreto. Um job diário ainda permitiria horas desnecessárias de ociosidade contínua."),
                ("Configurar a propriedade 'spark.scheduler.mode' para 'FAIR' nas configurações do Spark.", False, "Incorreto. O Fair Scheduler gerencia concorrência de queries dentro do cluster, não desligamento de VM."),
                ("Configurar o driver do Spark com memória de 2 GB para provocar OutOfMemory e derrubar o nó.", False, "Incorreto. Forçar falhas de memória corrompe o desenvolvimento e é uma péssima prática de engenharia.")
            ],
            "explanation": "O atributo 'autotermination_minutes' em Cluster Policies força o encerramento automático após o período estipulado de inatividade, sendo a principal medida de FinOps contra custos fantasmas de All-Purpose clusters."
        },
        # Q7
        {
            "scenario": "Uma organização precisa ratear os custos de DBUs e de VMs de cada cluster Databricks entre 5 centros de custo distintos da empresa. Qual estratégia garante que todo cluster criado contenha obrigatoriamente a tag 'CostCenter' preenchida de acordo com uma lista aprovada?",
            "options": [
                ("Definir na Cluster Policy uma regra obrigatória para 'custom_tags.CostCenter' utilizando o operador 'allowlist' com os códigos dos centros de custo.", True, "Correto. Cluster Policies permitem governar 'custom_tags.<tag_name>', tornando o preenchimento obrigatório e restrito a uma lista de valores permitidos."),
                ("Criar uma tabela Delta no Hive Metastore e pedir aos desenvolvedores que insiram manualmente os valores.", False, "Incorreto. Não impede a criação de clusters desgovernados nem integra automaticamente com o faturamento do Azure."),
                ("Exigir que todos os notebooks comecem com a variável Python cost_center = 'RH'.", False, "Incorreto. Variáveis de notebook não são propagadas para os metadados de cobrança do Azure e Databricks."),
                ("Configurar um alerta no Azure Monitor que envia um e-mail diário com os clusters sem tags.", False, "Incorreto. É reativo e não impede a criação de recursos fora da conformidade.")
            ],
            "explanation": "Tags customizadas governadas por Cluster Policies são propagadas automaticamente para as instâncias de VMs no Azure e para a tabela de faturamento system.billing.usage, permitindo rateio contábil exato."
        },
        # Q8
        {
            "scenario": "Analistas juniores de uma equipe de dados precisam realizar análises exploratórias em arquivos CSV de pequeno porte utilizando Pandas e PySpark básico. Para economizar custos, a gerência exige que esses analistas utilizem clusters compostos por uma única máquina virtual, sem nós workers. Qual configuração deve ser aplicada?",
            "options": [
                ("Configurar um cluster Single-Node (definindo spark.databricks.cluster.profile como 'singleNode' e num_workers = 0).", True, "Correto. Clusters Single-Node operam com 1 única VM executando tanto o Driver quanto os slots locais de execução, eliminando o custo de VMs workers adicionais."),
                ("Configurar um cluster Standard com 10 workers e desabilitar o nó Driver.", False, "Incorreto. O Spark não pode operar sem um nó Driver ativo."),
                ("Utilizar um Serverless SQL Warehouse de tamanho 4X-Large.", False, "Incorreto. 4X-Large aloca dezenas de instâncias e geraria um custo desproporcional para análises leves."),
                ("Executar o código dentro de uma Azure Function sem nenhum runtime Spark.", False, "Incorreto. A questão exige exploração de dados no Databricks com suporte a PySpark.")
            ],
            "explanation": "Clusters Single-Node são a escolha ideal de FinOps para workloads leves, bibliotecas não distribuídas (Pandas, Scikit-learn) ou aprendizado inicial, pois cobram apenas por 1 nó e eliminam sobrecarga de rede."
        },
        # Q9
        {
            "scenario": "Uma equipe precisa acelerar a inicialização de clusters de desenvolvimento de 6 minutos para menos de 30 segundos, pois os engenheiros iniciam e encerram ambientes frequentemente durante o expediente. Qual funcionalidade do Azure Databricks resolve este gargalo?",
            "options": [
                ("Criar um Databricks Instance Pool com um número mínimo de instâncias ociosas prontas (Min Idle Instances).", True, "Correto. Instance Pools mantêm um conjunto de VMs pré-alocadas no Compute Plane prontas para uso, reduzindo o tempo de boot de minutos para segundos."),
                ("Aumentar o tempo de autotermination para 480 minutos em todos os clusters.", False, "Incorreto. Isso geraria custos abusivos de DBUs e VMs sem resolver o tempo de inicialização a frio."),
                ("Executar todos os comandos em notebooks conectados ao DBFS local via comando %fs.", False, "Incorreto. O comando %fs é apenas um utilitário de navegação de arquivos e não executa código distribuído."),
                ("Desabilitar o Photon Engine e forçar compilação com Scala 2.11.", False, "Incorreto. O Photon acelera a execução de queries, e o Scala 2.11 é uma versão legada obsoleta.")
            ],
            "explanation": "Instance Pools mantêm instâncias de VMs pré-provisionadas na assinatura do Azure. Quando um cluster solicita um nó, a VM já está quente e anexada em segundos. Enquanto ociosa no pool, não há cobrança de DBUs (apenas o custo de infraestrutura de VM da Azure)."
        },
        # Q10
        {
            "scenario": "A gerência de TI questiona o custo de manter um Databricks Instance Pool com 4 instâncias ociosas prontas durante o horário comercial. Como é tarifado um nó que reside em um Instance Pool enquanto nenhum cluster está utilizando-o?",
            "options": [
                ("O cliente paga o custo normal de máquina virtual do Azure (IaaS), mas paga ZERO DBUs para a Databricks enquanto a instância estiver ociosa no pool.", True, "Correto. Enquanto uma VM permanece ociosa no pool, ela consome apenas a tarifa da VM da Microsoft; as DBUs Databricks só começam a ser tarifadas no momento em que a VM é alocada para um cluster ativo."),
                ("O cliente paga a taxa máxima de DBUs de All-Purpose multiplicada pelo número de instâncias no pool.", False, "Incorreto. Não há cobrança de DBUs de software Databricks para nós ociosos em pools."),
                ("A cobrança é gratuita tanto na Azure quanto no Databricks durante o período ocioso.", False, "Incorreto. A VM física alocada no Azure gera cobrança de infraestrutura de computação."),
                ("O custo é cobrado integralmente em storage ADLS Gen2 em vez de computação.", False, "Incorreto. O pool aloca VMs de computação, não espaço de armazenamento.")
            ],
            "explanation": "Essa é uma das premissas fundamentais de FinOps no DP-750: Instâncias ociosas em Instance Pools cobram apenas custo de VM Azure à Microsoft e ZERO DBUs ao Databricks. As DBUs só são debitadas quando um cluster anexa a instância."
        },
        # Q11
        {
            "scenario": "Uma equipe de analistas de Power BI realiza consultas ad-hoc e atualiza painéis executivos frequentemente. As consultas apresentam picos rápidos seguidos por períodos de inatividade. Qual recurso de computação oferece inicialização instantânea (sub-10s) e desligamento automático em até 1 minuto de ociosidade?",
            "options": [
                ("Serverless SQL Warehouse.", True, "Correto. O Serverless SQL Warehouse aloca computação instantânea no plano serverless da Databricks, escala dinamicamente e desliga automaticamente em 1 a 5 minutos de inatividade."),
                ("All-Purpose Cluster com 10 nós e autotermination de 120 minutos.", False, "Incorreto. Demora 4 a 6 minutos para iniciar e 120 minutos de inatividade geraria enorme desperdício."),
                ("Single-Node cluster com Databricks Runtime for Machine Learning.", False, "Incorreto. Clusters ML são voltados a treino de modelos e não possuem as otimizações analíticas SQL do warehouse."),
                ("Job Cluster efêmero configurado para rodar a cada 30 segundos.", False, "Incorreto. Jobs efêmeros clássicos têm latência de startup de VM e não atendem a queries interativas de Power BI.")
            ],
            "explanation": "Serverless SQL Warehouses são a opção recomendada pela Microsoft para BI e relatórios ad-hoc, pois oferecem o menor tempo de inicialização (segundos), escalabilidade elástica e desligamento ultrarrápido (1 minuto)."
        },
        # Q12
        {
            "scenario": "Em um Serverless SQL Warehouse com autoscaling habilitado, a demanda de consultas cresceu repentinamente devido a 200 analistas acessando simultaneamente um dashboard. O warehouse começou a enfileirar queries. Como a política de escalonamento gerencia clusters adicionais?",
            "options": [
                ("O Databricks adiciona clusters de computação adicionais quase instantaneamente para esvaziar a fila de espera quando o tempo estimado de fila ultrapassa o limiar.", True, "Correto. A política de autoscaling de SQL Warehouses monitora a fila de queries e sobe novos clusters de mesmo tamanho em segundos para manter a concorrência sem gargalos."),
                ("O warehouse reinicia o cluster principal e aumenta a memória RAM da máquina virtual Driver.", False, "Incorreto. Clusters de SQL Warehouse não reiniciam nem alteram hardware verticalmente sob carga."),
                ("As consultas excedentes são canceladas automaticamente e retornam código de erro HTTP 429.", False, "Incorreto. O warehouse enfileira as consultas e escala nós adicionais horizontalmente."),
                ("O warehouse transfere a execução para um cluster All-Purpose do usuário.", False, "Incorreto. Não há transferência cruzada de carga para clusters de notebooks de usuários.")
            ],
            "explanation": "SQL Warehouses escalam horizontalmente adicionando novos clusters do mesmo tamanho (ex: de 1 cluster 'Medium' para 2 ou 3 clusters 'Medium') com base na profundidade da fila de consultas."
        },
        # Q13
        {
            "scenario": "Um engenheiro de dados precisa integrar um pipeline PySpark a uma base de dados externa utilizando uma senha de banco e um token de API. A política de conformidade proíbe rigorosamente o armazenamento de credenciais em texto claro dentro de notebooks ou scripts Git. Qual é o procedimento oficial?",
            "options": [
                ("Criar um Secret Scope com backend no Azure Key Vault e ler as credenciais no notebook via dbutils.secrets.get(scope='...', key='...').", True, "Correto. O Azure Key Vault-backed Secret Scope sincroniza com os segredos do Key Vault e permite recuperação em memória com redação automática de saída."),
                ("Gravar as credenciais em um arquivo .txt armazenado na pasta /dbfs/FileStore/ e ler com open().", False, "Incorreto. Arquivos no DBFS raiz são inseguros e legíveis por qualquer usuário com acesso ao workspace."),
                ("Passar a senha diretamente como argumento de linha de comando no job agendado.", False, "Incorreto. Parâmetros de jobs ficam expostos na UI de execução e no histórico do workspace."),
                ("Codificar a senha em Base64 e salvar como uma constante estática no repositório Git.", False, "Incorreto. Base64 é apenas codificação reversível e não protege segredos corporativos.")
            ],
            "explanation": "O Azure Key Vault-backed Secret Scope é o padrão do DP-750 para gestão de segredos. Permite recuperar valores dinamicamente via dbutils.secrets.get(), garantindo que os valores sejam automaticamente mascarados ([REDACTED]) em logs e outputs."
        },
        # Q14
        {
            "scenario": "Qual comando da Databricks CLI cria corretamente um Secret Scope integrado a um Azure Key Vault chamado 'akv-corp-prod'?",
            "options": [
                ("databricks secrets create-scope --scope corp-secrets --scope-backend-type AZURE_KEYVAULT --resource-id <vault-id> --dns-name https://akv-corp-prod.vault.azure.net/", True, "Correto. Essa é a sintaxe exata da Databricks CLI para vincular um escopo ao Key Vault informando o resource-id e dns-name."),
                ("databricks secrets put --scope corp-secrets --key akv-corp-prod --value AZURE_VAULT", False, "Incorreto. O comando put armazena um segredo individual em escopo interno Databricks, não cria escopo integrado ao Azure Key Vault."),
                ("az databricks workspace link-keyvault --workspace-name myws --keyvault akv-corp-prod", False, "Incorreto. Comando inexistente na Azure CLI."),
                ("databricks keyvault mount --path /mnt/secrets --dns https://akv-corp-prod.vault.azure.net/", False, "Incorreto. Não se monta Key Vault como sistema de arquivos via DBFS.")
            ],
            "explanation": "A criação de Secret Scopes respaldados pelo Azure Key Vault é efetuada via Databricks CLI com `--scope-backend-type AZURE_KEYVAULT`, passando o Resource ID da Azure e a URI DNS do cofre."
        },
        # Q15
        {
            "scenario": "Um desenvolvedor executa o seguinte comando em uma célula de notebook: print(dbutils.secrets.get(scope='financas', key='db_password')). Qual será o valor exibido na saída do notebook?",
            "options": [
                ("[REDACTED]", True, "Correto. O Azure Databricks possui proteção ativa de Secret Redaction que intercepta a saída e substitui valores lidos via dbutils.secrets por [REDACTED]."),
                ("A senha do banco em texto claro.", False, "Incorreto. O Databricks impede que segredos recuperados por dbutils.secrets sejam vazados no stdout do notebook."),
                ("Uma mensagem de erro de compilação Python.", False, "Incorreto. O comando é válido e a execução conclui com sucesso, porém o output é redigido."),
                ("O hash SHA-256 da senha.", False, "Incorreto. A plataforma exibe explicitamente a string literal [REDACTED].")
            ],
            "explanation": "O Secret Redaction é um recurso de segurança nativo do Databricks: qualquer segredo obtido através de `dbutils.secrets.get` é mascarado automaticamente com `[REDACTED]` se for enviado para o fluxo de saída padrão do notebook."
        },
        # Q16
        {
            "scenario": "Uma organização precisa executar pipelines de produção em Databricks Workflows sem depender de credenciais de usuários individuais que podem ser demitidos ou ter senhas expiradas. Qual identidade deve ser configurada para execução automatizada?",
            "options": [
                ("Um Service Principal do Microsoft Entra ID gerenciado no Databricks Account Console com permissões federadas.", True, "Correto. Service Principals são identidades gerenciadas sem usuário humano, ideais para CI/CD e execução autônoma de jobs em produção."),
                ("Um Personal Access Token (PAT) gerado pelo usuário administrador do workspace.", False, "Incorreto. PATs de usuários expiram e tornam os pipelines vulneráveis a desligamentos ou rotações de senha pessoais."),
                ("A conta de root do primeiro desenvolvedor que provisionou o workspace.", False, "Incorreto. Viola normas de segurança e auditoria corporativa."),
                ("Um usuário convidado externo (Guest User) sem licença atribuída.", False, "Incorreto. Contas de convidados têm restrições e não servem para governança de produção.")
            ],
            "explanation": "O padrão corporativo oficial do DP-750 é a utilização de Service Principals do Microsoft Entra ID cadastrados no Account Console e associados aos Databricks Jobs."
        },
        # Q17
        {
            "scenario": "A equipe de segurança corporativa exige que os usuários e grupos definidos no Microsoft Entra ID da empresa sejam sincronizados automaticamente com o Databricks Account Console. Qual protocolo padrão de identidade deve ser configurado?",
            "options": [
                ("Configurar sincronização SCIM (System for Cross-domain Identity Management) a partir do Microsoft Entra ID.", True, "Correto. A integração SCIM entre o Entra ID e o Databricks Account Console automatiza a criação, atualização e revogação de usuários e grupos."),
                ("Configurar um script de FTP que envia um arquivo CSV com as senhas para o /dbfs diariamente.", False, "Incorreto. Extremamente inseguro e não integra identidades."),
                ("Habilitar autenticação Kerberos diretamente em cada nó Worker do Spark.", False, "Incorreto. O Databricks em nuvem utiliza OAuth e SCIM com Entra ID, não Kerberos tradicional on-premises."),
                ("Criar os usuários manualmente um a um no painel de cada workspace regional.", False, "Incorreto. Gestão manual não atende ao requisito de sincronização automática e gera erros operacionais.")
            ],
            "explanation": "A sincronização SCIM no nível da Conta (Account-level SCIM) conecta o Microsoft Entra ID ao Databricks, garantindo provisionamento e desprovisionamento centralizado de identidades."
        },
        # Q18
        {
            "scenario": "Um pipeline noturno consome 4 horas de processamento diário em um All-Purpose Cluster com 4 nós. Sabendo que o custo de DBU em All-Purpose é aproximadamente $0.55/DBU e em Job Cluster é aproximadamente $0.20/DBU, qual alteração arquitetural reduz imediatamente a fatura em mais de 50%?",
            "options": [
                ("Converter o pipeline para ser orquestrado via Databricks Workflow utilizando um Job Cluster efêmero.", True, "Correto. Job Clusters cobram uma taxa de DBU significativamente menor do que All-Purpose Clusters e são destruídos imediatamente após o término."),
                ("Aumentar o número de nós do cluster All-Purpose de 4 para 16 nós.", False, "Incorreto. Aumentaria expressivamente o custo total de VMs e consumo de DBUs."),
                ("Manter o cluster All-Purpose ligado 24/7 sem rodar nenhum outro código.", False, "Incorreto. Resultaria em cobrança contínua e desperdício de orçamento."),
                ("Mudar o formato de armazenamento dos dados de Delta Lake para CSV.", False, "Incorreto. CSV é lento, não possui otimizações e degradaria severamente a performance.")
            ],
            "explanation": "All-Purpose Compute é destinado a notebooks interativos e possui a taxa de DBU mais cara. Job Compute possui a menor taxa de DBU por hora (até 60% mais econômica) e é o padrão exigido para pipelines agendados."
        },
        # Q19
        {
            "scenario": "Um engenheiro de dados precisa executar um script diário de manutenção que realiza apenas chamadas à API REST externa para atualizar metadados em tabelas Delta. O processamento dura 3 minutos e não executa nenhum processamento distribuído. Qual tipo de cluster oferece o menor custo de infraestrutura?",
            "options": [
                ("Single-Node cluster (1 único nó executando driver e executor local).", True, "Correto. O modo Single-Node aloca apenas 1 VM no Azure, eliminando custos de nós workers para cargas não distribuídas."),
                ("Cluster multi-nós com 8 workers acelerados por GPU.", False, "Incorreto. Custo desnecessário para uma tarefa simples de API e metadados."),
                ("Instance Pool com 20 nós reservadas 24 horas por dia.", False, "Incorreto. Geraria custo fixo desnecessário de VMs ociosas."),
                ("Cluster High Concurrency com isolamento de tabela legado.", False, "Incorreto. Modo de alta concorrência legado não é recomendado e custa mais caro.")
            ],
            "explanation": "Single-Node clusters são recomendados para tarefas de nó único (drivers-only, bibliotecas Python simples como requests, manutenção leve), economizando custo de instâncias adicionais."
        },
        # Q20
        {
            "scenario": "Para onde o Azure Databricks pode enviar automaticamente os logs detalhados de diagnóstico e eventos de auditoria de segurança (login de usuários, criação de clusters, acesso a dados) gerados no workspace?",
            "options": [
                ("Azure Log Analytics Workspace, Azure Storage Account ou Azure Event Hubs via Diagnostic Settings do recurso no portal Azure.", True, "Correto. O Azure Databricks integra com o Azure Monitor Diagnostic Settings para exportar logs de auditoria e métricas corporativas."),
                ("Apenas para o disco rígido local da máquina física do administrador.", False, "Incorreto. Logs corporativos de nuvem não são baixados para discos locais de administradores."),
                ("Diretamente para um bucket S3 na Amazon Web Services sem passar pelo Azure.", False, "Incorreto. O Azure Databricks envia diagnósticos nativamente para destinos suportados no Azure Monitor."),
                ("Para o diretório temporário /tmp/logs de cada nó worker descartado.", False, "Incorreto. O diretório /tmp é volátil e os dados seriam perdidos no desligamento do nó.")
            ],
            "explanation": "Diagnostic Settings no recurso do Azure Databricks permitem encaminhar categorias de log (como audit, clusters, workspace, accounts) para Log Analytics, Storage ou Event Hubs."
        },
        # Q21
        {
            "scenario": "Uma empresa precisa garantir que o acesso ao Workspace do Azure Databricks seja permitido exclusivamente para requisições originadas dos IPs públicos de sua VPN corporativa e filiais autorizadas. Qual funcionalidade deve ser utilizada?",
            "options": [
                ("Configurar IP Access Lists no Azure Databricks através da REST API ou do Account Console.", True, "Correto. IP Access Lists permitem bloquear acessos não autorizados por IP público na camada da Web UI e REST API do workspace."),
                ("Alterar o código Python de cada notebook adicionando um if request.ip == '...'.", False, "Incorreto. O notebook só executa após o usuário já ter logado no workspace."),
                ("Instalar um antivírus em cada máquina virtual worker do Spark.", False, "Incorreto. Antivírus de VM não controla acesso HTTP à interface web gerenciada do Databricks."),
                ("Bloquear a porta 443 no roteador de saída de todos os funcionários da empresa.", False, "Incorreto. Bloquear a porta 443 impediria a navegação na internet de toda a empresa.")
            ],
            "explanation": "IP Access Lists no Databricks fornecem listas de permissão (allowlist) e bloqueio (blocklist) para controlar quais endereços IP públicos podem acessar o workspace e suas APIs."
        },
        # Q22
        {
            "scenario": "Init scripts legados armazenados em /dbfs/FileStore/ foram descontinuados para novos recursos de segurança no Databricks. Qual é o local recomendado e governado pelo Unity Catalog para armazenar e referenciar init scripts de cluster?",
            "options": [
                ("Armazenar o script em um Unity Catalog Volume e referenciá-lo pelo caminho /Volumes/catalog/schema/volume/script.sh.", True, "Correto. Init scripts armazenados em Unity Catalog Volumes possuem governança de acesso RBAC e auditoria completa."),
                ("Embutir o código do script dentro de um comentário na célula 1 do notebook.", False, "Incorreto. Comentários de notebook não são executados na inicialização da máquina virtual do cluster."),
                ("Hospedar o script em um servidor HTTP público aberto na internet sem autenticação.", False, "Incorreto. Violação grave de segurança que expõe o cluster a ataques de injeção de código."),
                ("Gravar o script no registro de DNS do Azure Private Link.", False, "Incorreto. DNS não armazena scripts executáveis shell.")
            ],
            "explanation": "O Databricks descontinuou init scripts globais e legados em DBFS. A recomendação moderna é armazenar scripts de inicialização em Volumes do Unity Catalog ou como cluster-scoped scripts governados."
        },
        # Q23
        {
            "scenario": "Em um cluster clássico do Azure Databricks, onde residem os dados de clientes e onde os nós workers executam suas tarefas?",
            "options": [
                ("Os nós workers executam na VNet do cliente (Compute Plane) e os dados de negócio residem no ADLS Gen2 do cliente; nenhum dado reside no Control Plane.", True, "Correto. Esta é a regra de ouro de conformidade do Databricks: dados e computação do cliente residem na infraestrutura do cliente."),
                ("Os nós workers executam na assinatura da Microsoft e todos os dados de clientes são replicados para o Control Plane.", False, "Incorreto. Dados de clientes nunca trafegam nem residem no Control Plane."),
                ("Os dados residem exclusivamente na memória RAM dos computadores pessoais dos desenvolvedores.", False, "Incorreto. O processamento é distribuído em nós na nuvem."),
                ("Os dados são convertidos para tabelas MySQL locais em um container Docker único.", False, "Incorreto. O Lakehouse utiliza Apache Spark, Delta Lake e ADLS Gen2.")
            ],
            "explanation": "No Azure Databricks clássico, o Compute Plane reside na assinatura Azure do cliente. Os dados de negócio nunca residem no Control Plane, garantindo isolamento estrito e atendimento a regulamentações como LGPD, HIPAA e GDPR."
        },
        # Q24
        {
            "scenario": "Um arquiteto de dados precisa configurar um cluster para um pipeline crítico de produção com SLA rígido que não pode sofrer nenhuma interrupção ou perda de nós por desalocação de infraestrutura da nuvem. Qual opção de tipo de instância deve ser selecionada?",
            "options": [
                ("Utilizar instâncias On-Demand tanto para o nó Driver quanto para os nós Workers.", True, "Correto. Instâncias On-Demand garantem que as VMs não serão preemptadas (desalocadas) pelo Azure, garantindo o SLA do pipeline."),
                ("Utilizar instâncias Spot tanto para o Driver quanto para todos os Workers.", False, "Incorreto. Se o Azure requisitar a VM Spot onde o Driver reside, o cluster inteiro falha imediatamente."),
                ("Utilizar máquinas desligadas do tipo B-Series com CPU burstable variável.", False, "Incorreto. B-Series têm desempenho imprevisível e não garantem SLAs críticos de engenharia."),
                ("Executar sem Driver utilizando nós somente de armazenamento.", False, "Incorreto. O Spark exige obrigatoriamente um nó Driver para orquestrar a execução.")
            ],
            "explanation": "Embora nós Spot reduzam custos em até 80%, eles podem ser desalocados a qualquer momento pelo Azure. O nó Driver NUNCA deve ser Spot, e workloads de missão crítica com SLA rígido devem utilizar instâncias On-Demand."
        },
        # Q25
        {
            "scenario": "Por que a Microsoft recomenda a seleção de versões Databricks Runtime com suporte de longo prazo (ex: DBR 15.4 LTS) para pipelines corporativos de produção?",
            "options": [
                ("DBR LTS oferece suporte estendido por até 3 anos com patches de segurança e estabilidade garantida sem quebras de compatibilidade de APIs.", True, "Correto. Versões LTS (Long-Term Support) fornecem estabilidade e suporte corporativo sem mudanças inesperadas de bibliotecas e dependências."),
                ("Versões LTS são as únicas que suportam comandos SQL no Databricks.", False, "Incorreto. Todas as versões suportam SQL."),
                ("Versões LTS são 100% gratuitas e não cobram nenhuma taxa de DBU.", False, "Incorreto. DBR LTS cobra tarifas normais de DBU conforme o tipo de computação."),
                ("Versões LTS desabilitam o Catalyst Optimizer para evitar compilações lógicas.", False, "Incorreto. O Catalyst Optimizer é parte fundamental do Apache Spark em todas as versões.")
            ],
            "explanation": "Ambientes produtivos de missão crítica devem padronizar em Databricks Runtime (DBR) LTS para garantir janelas de suporte corporativo de múltiplos anos e correções contínuas de segurança."
        },
        # Q26
        {
            "scenario": "Um engenheiro de dados precisa configurar parâmetros avançados de execução do Spark em um cluster. Onde essas configurações devem ser inseridas na interface do Databricks?",
            "options": [
                ("No campo 'Spark Config' dentro de 'Advanced Options' na página de configuração do cluster.", True, "Correto. As opções avançadas do cluster permitem injetar propriedades do Spark (ex: spark.sql.shuffle.partitions) diretamente na inicialização."),
                ("Em uma planilha Excel compartilhada no SharePoint da equipe.", False, "Incorreto. Não se integra ao runtime do Databricks."),
                ("No arquivo hosts do computador do desenvolvedor.", False, "Incorreto. Arquivo local do sistema operacional do cliente."),
                ("Dentro de uma tag HTML &lt;meta&gt; na página do portal.", False, "Incorreto. Não afeta a configuração do Apache Spark.")
            ],
            "explanation": "As configurações globais do cluster Spark (como `spark.sql.adaptive.enabled` ou limites de broadcast) são definidas no painel 'Advanced Options' > 'Spark Config'."
        },
        # Q27
        {
            "scenario": "Em um cluster que opera no modo de acesso 'Single User' associado ao Unity Catalog, quais linguagens de programação são suportadas para execução de código?",
            "options": [
                ("Python, SQL, Scala e R.", True, "Correto. Clusters Single User suportam todas as quatro linguagens principais (Python, SQL, Scala e R) associadas à identidade do usuário."),
                ("Apenas SQL e proíbe qualquer execução de código em Python ou Scala.", False, "Incorreto. SQL-only é típico de SQL Warehouses, não de clusters Single User."),
                ("Apenas comandos assembly C++ para o Photon.", False, "Incorreto. Desenvolvedores utilizam linguagens de alto nível."),
                ("Apenas linguagem Bash shell sem acesso a DataFrames.", False, "Incorreto. O Spark opera com DataFrames e linguagens nativas.")
            ],
            "explanation": "No Unity Catalog, clusters no modo 'Single User' oferecem suporte total a Python, Scala, SQL e R para o usuário atribuído. Já clusters no modo 'Shared' suportam Python e SQL (com restrições de isolamento multi-usuário)."
        },
        # Q28
        {
            "scenario": "Qual é a principal vantagem de adotar o Serverless Compute para Databricks Workflows (Serverless Jobs) em relação ao gerenciamento de clusters clássicos de jobs?",
            "options": [
                ("Eliminação do tempo de espera de provisionamento de VM (inicialização em segundos), sem gerenciamento de cotas de VMs na assinatura Azure e otimização automática de recursos.", True, "Correto. O Serverless Jobs sobe em segundos, não consome cotas de VM da assinatura do cliente e elimina o trabalho de gerenciamento de infraestrutura de computação."),
                ("Permite executar código sem utilizar nenhuma conexão de rede com a nuvem.", False, "Incorreto. A nuvem e os recursos de rede são utilizados normalmente."),
                ("Gera dados sem necessidade de conta de armazenamento no ADLS Gen2.", False, "Incorreto. Os dados continuam sendo gravados no storage do cliente."),
                ("Substitui completamente o uso do Unity Catalog por arquivos Parquet sem metadados.", False, "Incorreto. O Serverless é totalmente integrado ao Unity Catalog.")
            ],
            "explanation": "Serverless Jobs oferecem computação elástica imediata, reduzem o TCO eliminando clusters ociosos e removem a complexidade de gerenciar limites de vCPUs no Azure Resource Manager."
        },
        # Q29
        {
            "scenario": "Um arquiteto precisa auditar todos os gastos de computação da empresa no Databricks agrupados por centro de custo nos últimos 90 dias. Qual tabela de sistema do Unity Catalog deve ser consultada?",
            "options": [
                ("system.billing.usage", True, "Correto. A tabela do sistema system.billing.usage armazena o histórico completo de consumo de DBUs, SKUs, clusters, jobs e tags personalizadas."),
                ("system.access.audit", False, "Incorreto. Esta tabela registra eventos de auditoria de segurança (logins, permissões, leituras), não o faturamento financeiro de DBUs."),
                ("system.lineage.table_lineage", False, "Incorreto. Esta tabela registra linhagem de dados entre tabelas e colunas."),
                ("system.information_schema.columns", False, "Incorreto. Registra metadados de colunas de tabelas, não consumo de nuvem.")
            ],
            "explanation": "A tabela `system.billing.usage` é a base oficial de FinOps no Databricks. Nela encontram-se as colunas `usage_quantity` (DBUs), `sku_name`, `usage_date` e `custom_tags`."
        },
        # Q30
        {
            "scenario": "Qual é o principal risco arquitetural de armazenar dados corporativos de produção diretamente no DBFS raiz (FileStore ou /mnt) em vez de utilizar o Unity Catalog com External Locations?",
            "options": [
                ("O DBFS raiz reside na conta de armazenamento gerenciada do workspace, não possui controle de acesso refinado (RBAC) do Unity Catalog e todos os usuários com acesso ao workspace podem ler ou sobrescrever os dados.", True, "Correto. O DBFS raiz não suporta a governança fina do Unity Catalog e representa risco severo de vazamento ou corrupção de dados corporativos."),
                ("O DBFS raiz apaga automaticamente todos os arquivos a cada 24 horas.", False, "Incorreto. O storage do DBFS é persistente, o risco reside na ausência de controle de acesso refinado."),
                ("O DBFS raiz não suporta o formato Parquet nem transações ACID.", False, "Incorreto. O Delta Lake funciona no DBFS, mas sem a governança e segurança moderna do Unity Catalog."),
                ("O DBFS raiz cobra 10x mais caro que o ADLS Gen2 por terabyte armazenado.", False, "Incorreto. A cobrança de storage é do tipo Azure Storage padrão, o problema é de segurança e governança.")
            ],
            "explanation": "O exame DP-750 desencoraja expressamente o uso de DBFS raiz para dados de negócio. Dados de produção devem residir em containers governados pelo Unity Catalog (External Locations ou Volumes)."
        },
        # Q31
        {
            "scenario": "Ao configurar autoscaling em um cluster clássico de engenharia de dados, um desenvolvedor define min_workers = 2 e max_workers = 10. Como o Spark Runtime gerencia a alocação desses nós?",
            "options": [
                ("O cluster inicia com 2 nós workers e escala automaticamente até 10 nós conforme a carga de trabalho de estágios de shuffle e volume de partições pendentes, reduzindo novamente quando a carga diminui.", True, "Correto. O autoscaling elástico do Databricks ajusta dinamicamente a quantidade de nós entre os limites mínimo e máximo com base nas métricas de execução das tarefas."),
                ("O cluster inicia imediatamente com 10 nós e nunca diminui até ser desligado.", False, "Incorreto. Isso seria dimensionamento fixo com 10 nós, não autoscaling."),
                ("O cluster cria 10 nós Drivers e nenhum nó worker.", False, "Incorreto. O cluster Spark possui exatamente 1 nó Driver."),
                ("O autoscaling apenas altera a velocidade da CPU de cada máquina sem adicionar nós.", False, "Incorreto. O autoscaling no Databricks é horizontal (adiciona e remove VMs completas).")
            ],
            "explanation": "O Autoscaling do Azure Databricks avalia a fila de tarefas e o uso de recursos dos executores para alocar ou desalocar workers dinamicamente entre os limites min e max definidos."
        },
        # Q32
        {
            "scenario": "Uma equipe precisa garantir que todos os clusters criados no workspace utilizem exclusivamente o runtime acelerado pelo Photon Engine. Qual configuração de Cluster Policy impõe essa exigência?",
            "options": [
                ("Definir uma regra para 'spark_version' com allowlist contendo apenas versões terminadas com '-photon-' (ex: '*photon*').", True, "Correto. Ao filtrar 'spark_version' para aceitar apenas strings contendo 'photon', os desenvolvedores são impedidos de criar clusters sem o motor Photon C++."),
                ("Desinstalar o interpretador Python de todos os nós.", False, "Incorreto. Inviabilizaria o uso de PySpark no cluster."),
                ("Configurar a porta 8080 para bloquear tráfego de JVM.", False, "Incorreto. A JVM é necessária para coordenação do cluster."),
                ("Exigir que todas as consultas SQL comecem com a palavra-chave PHOTON_START.", False, "Incorreto. Sintaxe inexistente.")
            ],
            "explanation": "Em Cluster Policies, regexes ou padrões com wildcard podem ser usados no atributo `spark_version` (ex: `{\"type\": \"pattern\", \"pattern\": \".*photon.*\"}`) para forçar clusters acelerados por Photon."
        },
        # Q33
        {
            "scenario": "Como o Secure Cluster Connectivity (No Public IP) protege a infraestrutura de computação contra invasões e varreduras de portas vindas da internet pública?",
            "options": [
                ("Nenhum nó de computação (Driver ou Worker) possui endereço IP público alocado e nenhuma porta de entrada (inbound) precisa ser aberta no NSG corporativo.", True, "Correto. O modelo NPIP garante isolamento total contra varreduras de rede da internet pública, utilizando apenas conexões TLS de saída para o Control Plane."),
                ("Utilizando criptografia quântica nos cabos submarinos do Azure.", False, "Incorreto. Resposta fictícia."),
                ("Exigindo que cada nó worker altere seu endereço MAC a cada 5 segundos.", False, "Incorreto. Resposta fictícia."),
                ("Bloqueando todos os pacotes TCP e permitindo apenas tráfego UDP sem confirmação.", False, "Incorreto. O Spark e a Web utilizam TCP/HTTPS.")
            ],
            "explanation": "Secure Cluster Connectivity (NPIP) é a configuração padrão de segurança de rede do Azure Databricks: zero IPs públicos nos nós de computação e zero regras de entrada abertas no NSG."
        },
        # Q34
        {
            "scenario": "Um desenvolvedor precisa clonar um repositório corporativo do GitHub/Azure Repos diretamente no Azure Databricks para editar código e criar branches de desenvolvimento. Qual recurso integrado do workspace provê essa funcionalidade?",
            "options": [
                ("Databricks Git Folders (anteriormente conhecido como Databricks Repos).", True, "Correto. Git Folders provê integração nativa com Git (GitHub, GitLab, Azure Repos, Bitbucket) diretamente dentro do workspace."),
                ("DBFS FileStore.", False, "Incorreto. FileStore é apenas uma pasta do DBFS para upload de arquivos estáticos."),
                ("Azure Key Vault Secret Scopes.", False, "Incorreto. Key Vault gerencia segredos e senhas, não controle de versão Git."),
                ("Databricks Pools.", False, "Incorreto. Pools gerenciam VMs ociosas de computação.")
            ],
            "explanation": "Databricks Git Folders oferece controle de versão completo com suporte a branching, pull requests, commits e sincronização bidirecional com repositórios Git corporativos."
        },
        # Q35
        {
            "scenario": "Uma organização multinacional possui 3 workspaces do Azure Databricks na região East US 2 (Dev, Staging e Prod). Como deve ser desenhada a governança do Unity Catalog para essa topologia?",
            "options": [
                ("Criar exatamente um Metastore do Unity Catalog na região East US 2 e vinculá-lo aos três workspaces (Dev, Staging e Prod).", True, "Correto. A melhor prática do Unity Catalog é ter um único Metastore por região geográfica, compartilhado entre múltiplos workspaces da mesma região para unificar governança e linhagem."),
                ("Criar um Metastore separado para cada workspace e sincronizar via cópia diária de arquivos JSON.", False, "Incorreto. Metastores separados fragmentam a linhagem e impedem governança e compartilhamento unificados."),
                ("Não utilizar nenhum Metastore e voltar para o Hive Metastore legado.", False, "Incorreto. O Hive Metastore não oferece governança unificada nem suporte a recursos modernos do DP-750."),
                ("Criar 10 metastores na região West US e conectar via VPN internacional.", False, "Incorreto. O metastore deve estar na mesma região dos workspaces para evitar latência e custos de saída de rede.")
            ],
            "explanation": "A recomendação da Microsoft para o DP-750 é ter um único Metastore do Unity Catalog por região, o qual é associado a todos os workspaces daquela região, viabilizando o 3-Level Namespace compartilhado."
        },
        # Q36
        {
            "scenario": "Em um ambiente com múltiplos workspaces conectados ao mesmo Metastore do Unity Catalog, como os administradores garantem que os analistas do Workspace de Desenvolvimento (Dev) não consigam acessar nem consultar os dados do Catálogo de Produção (prod_catalog)?",
            "options": [
                ("Configurar Catalog-Workspace Binding no Unity Catalog, vinculando o catálogo de produção exclusivamente ao workspace de Produção.", True, "Correto. O Catalog-Workspace Binding restringe quais workspaces específicos têm permissão para acessar determinado catálogo no Metastore compartilhado."),
                ("Desligar os roteadores da VNet do workspace de desenvolvimento.", False, "Incorreto. Impediria todo o trabalho do ambiente de desenvolvimento."),
                ("Excluir o catálogo de produção durante o expediente de desenvolvimento.", False, "Incorreto. Destruiria o ambiente de produção."),
                ("Alterar o nome do catálogo para que os desenvolvedores não descubram o nome.", False, "Incorreto. 'Segurança por obscuridade' é uma péssima prática e não impede acessos.")
            ],
            "explanation": "O recurso Catalog-Workspace Binding permite isolar catálogos por workspace, garantindo que catálogos de produção só sejam visíveis a partir de workspaces aprovados para produção."
        },
        # Q37
        {
            "scenario": "Uma empresa precisa exportar métricas de execução do Spark e telemetria de seus clusters para o Azure Monitor e Application Insights. Qual biblioteca/ferramenta oficial é suportada para coletar métricas e encaminhá-las nativamente?",
            "options": [
                ("Azure Databricks Monitoring Library (spark-monitoring) integrada com Log Analytics e Azure Monitor.", True, "Correto. A biblioteca de monitoramento oficial da Microsoft para Databricks envia métricas do Spark e logs do log4j para o Azure Log Analytics Workspace."),
                ("Instalar um servidor Apache Kafka dentro de cada nó worker para enviar mensagens.", False, "Incorreto. Complexidade excessiva e alto custo operacional."),
                ("Copiar manualmente os arquivos de log do Driver a cada 10 minutos via terminal SSH.", False, "Incorreto. Processo manual e incompatível com ambientes modernos em nuvem."),
                ("Configurar um webhook que tira capturas de tela da Spark UI e envia por e-mail.", False, "Incorreto. Inviável e não estruturado para métricas e alertas.")
            ],
            "explanation": "A biblioteca oficial 'spark-monitoring' da Microsoft integra o Azure Databricks com o Azure Log Analytics Workspace, permitindo criar dashboards e alertas no Azure Monitor baseados em métricas do Spark."
        },
        # Q38
        {
            "scenario": "Quais DUAS configurações são exigidas para garantir o menor custo de DBUs e de VMs em um pipeline diário de engenharia de dados que processa arquivos na madrugada? (Selecione duas opções)",
            "options": [
                ("Configurar a execução via Databricks Workflows utilizando um Job Cluster efêmero.", True, "Correto. Job Clusters cobram a menor taxa de DBU por hora e são destruídos ao final do pipeline."),
                ("Habilitar autotermination imediato ou término automático do job cluster assim que o pipeline concluir.", True, "Correto. Job clusters efêmeros encerram sua infraestrutura logo após a conclusão da execução, evitando custos ociosos."),
                ("Utilizar um All-Purpose Cluster de alta disponibilidade ligado continuamente 24 horas por dia.", False, "Incorreto. Taxa de DBU muito mais cara e desperdício de VMs ligadas sem necessidade."),
                ("Desabilitar o Delta Log e gravar dados em formato texto puro (.txt).", False, "Incorreto. Degrada o desempenho e perde as garantias ACID do Lakehouse."),
                ("Executar o processamento através do navegador de um desenvolvedor logado no portal.", False, "Incorreto. Não permite automação nem governança de produção.")
            ],
            "type": "multiple",
            "explanation": "Para workloads agendados de engenharia de dados, o exame DP-750 exige a combinação de Databricks Workflows com Job Clusters efêmeros configurados para encerramento automático após o término das tarefas."
        }
    ]
    return d1_specs

