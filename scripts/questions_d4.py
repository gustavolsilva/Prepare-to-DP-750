#!/usr/bin/env python3
"""
Databricks Formation — Prepare to DP-750
Domínio 4: Implantar e Manter Pipelines e Workloads (30–35%) — 54 Questões (131 a 184)
"""

def get_d4_questions():
    d4_specs = [
        # Q131
        {
            "scenario": "Uma indústria farmacêutica precisa construir um pipeline declarativo de qualidade rigorosa de dados onde a ingestão incremental de sensores laboratoriais seja validada automaticamente. Eles optam por Delta Live Tables (DLT) em Python. Qual decorador define uma tabela gerenciada que consome eventos incrementais contínuos?",
            "options": [
                ("@dlt.table com leitura via dlt.read_stream('tabela_fonte')", True, "Correto. O decorador @dlt.table combinado com dlt.read_stream() define uma Streaming Table no Delta Live Tables, processando novos registros de forma incremental."),
                ("@spark.streaming_job()", False, "Incorreto. Decorador inexistente no DLT."),
                ("@azure.databricks_pipeline()", False, "Incorreto. Decorador inexistente."),
                ("@pyspark.dataframe_stream()", False, "Incorreto. Sintaxe inexistente na API do DLT.")
            ],
            "explanation": "No Delta Live Tables (DLT), `@dlt.table` define uma tabela gerenciada. Quando a função lê de uma fonte de streaming usando `dlt.read_stream()`, o DLT materializa uma Streaming Table incremental."
        },
        # Q132
        {
            "scenario": "Em um pipeline Delta Live Tables (DLT), qual é a diferença fundamental entre uma Streaming Table e uma Materialized View?",
            "options": [
                ("Streaming Tables processam dados append-only de forma incremental gravando apenas novas linhas; Materialized Views recalculam agregações e transformações de negócio refletindo o estado atual da fonte.", True, "Correto. Essa é a distinção central: Streaming Tables são ideais para fluxos contínuos/append-only (Bronze/Silver), enquanto Materialized Views são ideais para agregações e transformações de estado que mudam (Gold/BI)."),
                ("Streaming Tables apagam todos os dados após 2 minutos.", False, "Incorreto. Tabelas de streaming são persistentes."),
                ("Materialized Views não podem ser consultadas via SQL.", False, "Incorreto. Materialized Views são consultadas com SQL padrão no Unity Catalog."),
                ("Streaming Tables só funcionam com arquivos em disquete.", False, "Incorreto. Resposta fictícia.")
            ],
            "explanation": "No DLT, Streaming Tables lidam com fontes append-only sem recomputar dados passados. Materialized Views recalculam o resultado da query para refletir atualizações nas fontes (ex: joins, agregações e deduplicações)."
        },
        # Q133
        {
            "scenario": "Um pipeline DLT na área de saúde precisa validar se a temperatura das vacinas está entre 2°C e 8°C. Se uma medição violar essa regra, a linha inválida deve ser descartada da tabela de destino Silver, mas o pipeline NÃO deve falhar e deve registrar a métrica de descarte no event log. Qual cláusula de Expectation atende a essa regra?",
            "options": [
                ("@dlt.expect_or_drop('temperatura_valida', 'temperatura BETWEEN 2 AND 8')", True, "Correto. A cláusula expect_or_drop descarta registros inválidos da tabela alvo, mantendo o pipeline em execução e gravando métricas no log de integridade."),
                ("@dlt.expect_or_fail('temperatura_valida', 'temperatura BETWEEN 2 AND 8')", False, "Incorreto. expect_or_fail abortaria imediatamente todo o pipeline ao encontrar a primeira linha inválida."),
                ("@dlt.expect('temperatura_valida', 'temperatura BETWEEN 2 AND 8')", False, "Incorreto. expect simples apenas registra um aviso no log, mas grava a linha inválida na tabela de destino."),
                ("@dlt.drop_everything_if_error()", False, "Incorreto. Sintaxe inexistente.")
            ],
            "explanation": "O DLT possui 3 níveis de Data Quality Expectations: `expect` (alerta no log e mantém a linha), `expect_or_drop` (descarta a linha inválida e continua o pipeline) e `expect_or_fail` (aborta o pipeline imediatamente na violação)."
        },
        # Q134
        {
            "scenario": "Em um pipeline DLT de pagamentos bancários, a regra de conformidade exige que se o campo 'numero_conta' for nulo (IS NULL), o pipeline deve abortar e falhar a execução imediatamente para evitar pagamentos órfãos. Qual cláusula de Expectation deve ser usada?",
            "options": [
                ("@dlt.expect_or_fail('conta_obrigatoria', 'numero_conta IS NOT NULL')", True, "Correto. A cláusula expect_or_fail interrompe imediatamente a execução da tarefa se qualquer registro violar a regra de qualidade."),
                ("@dlt.expect('conta_obrigatoria', 'numero_conta IS NOT NULL')", False, "Incorreto. expect simples deixaria a linha nula entrar na tabela."),
                ("@dlt.expect_or_drop('conta_obrigatoria', 'numero_conta IS NOT NULL')", False, "Incorreto. expect_or_drop descartaria a linha silenciosamente, sem falhar o pipeline como exigido."),
                ("@dlt.ignore_nulls_always()", False, "Incorreto. Sintaxe inexistente.")
            ],
            "explanation": "Quando uma violação de qualidade de dados é inaceitável para o negócio, utiliza-se `@dlt.expect_or_fail(nome, condicao)`, que aborta a execução do pipeline assim que um registro violador é detectado."
        },
        # Q135
        {
            "scenario": "Uma empresa precisa processar um feed contínuo de Change Data Capture (CDC) gerado por um banco SQL Server contendo inserções, atualizações e exclusões lógicas. Qual função nativa do Delta Live Tables simplifica a aplicação dessas alterações diretamente em uma tabela Silver?",
            "options": [
                ("dlt.apply_changes(target='...', source='...', keys=['id'], sequence_by='timestamp', apply_as_deletes='operacao = \"DELETE\"')", True, "Correto. A API dlt.apply_changes() processa feeds CDC automaticamente, lidando com chegadas fora de ordem (sequence_by), chaves de upsert e deleções para SCD Tipo 1 ou Tipo 2."),
                ("dlt.merge_into_manual_sql()", False, "Incorreto. Função inexistente no DLT."),
                ("spark.sql('COPY INTO ...')", False, "Incorreto. COPY INTO não processa logs de CDC com deleções e atualizações ordenadas."),
                ("dlt.truncate_and_reload()", False, "Incorreto. Truncate recarrega tudo do zero, perdendo o benefício incremental do CDC.")
            ],
            "explanation": "A instrução `dlt.apply_changes()` é o mecanismo nativo do Delta Live Tables para Change Data Capture (CDC), garantindo que inserts, updates e deletes sejam aplicados na ordem cronológica correta definida por `sequence_by`."
        },
        # Q136
        {
            "scenario": "Ao configurar um pipeline Delta Live Tables no Databricks, qual é a diferença entre os modos 'Development' (Desenvolvimento) e 'Production' (Produção)?",
            "options": [
                ("O modo 'Development' mantém o cluster ativo mesmo após a conclusão das execuções para acelerar iterações e desabilita retentativas automáticas; o modo 'Production' desliga clusters ociosos e reinicia automaticamente pipelines que sofrem falhas transitórias.", True, "Correto. O modo Development prioriza agilidade de teste sem reboots de VM; o modo Production prioriza resiliência, SLAs e economia de DBUs."),
                ("O modo 'Production' apaga todas as tabelas a cada 5 minutos.", False, "Incorreto. Tabelas em produção são persistentes e protegidas."),
                ("O modo 'Development' não suporta linguagem Python.", False, "Incorreto. Suporta Python e SQL normalmente."),
                ("O modo 'Production' é executado em computadores físicos no escritório da empresa.", False, "Incorreto. Ambos executam na nuvem Azure.")
            ],
            "explanation": "No DLT, o modo 'Development' reusa clusters para evitar o tempo de inicialização de VMs a cada clique e pausa retentativas para facilitar o debugging. O modo 'Production' implementa retries automáticos de falhas e desliga clusters ociosos."
        },
        # Q137
        {
            "scenario": "Um arquiteto precisa auditar as métricas de qualidade de dados de um pipeline DLT (número de linhas lidas, linhas aprovadas e linhas descartadas por cada Expectation). Onde esses dados de telemetria são armazenados automaticamente?",
            "options": [
                ("No Event Log do Delta Live Tables, armazenado em formato Delta Lake na pasta configurada no pipeline (ou consultável via system.dlt.event_log).", True, "Correto. O DLT grava todas as métricas de qualidade, linhagem e eventos de execução em uma tabela Delta de Event Log dedicada."),
                ("No bloco de notas do Windows de cada desenvolvedor.", False, "Incorreto. Resposta fictícia."),
                ("Apenas na memória RAM volátil que é apagada ao término do job.", False, "Incorreto. O Event Log é persistido de forma permanente em Delta Lake."),
                ("Em um e-mail diário com anexos em PDF enviado ao suporte da Azure.", False, "Incorreto. Métricas são estruturadas em tabelas Delta para consulta SQL.")
            ],
            "explanation": "O Event Log do DLT é uma tabela Delta que registra a saúde e métricas do pipeline. É possível executar consultas SQL sobre ele para calcular a taxa de dados descartados: `SELECT * FROM event_log WHERE event_type = 'expectation_metrics'`."
        },
        # Q138
        {
            "scenario": "Uma organização precisa orquestrar um workflow complexo de 8 tarefas sequenciais e paralelas, composto por notebooks PySpark, tarefas SQL analíticas, execução de pipeline DLT e notificações por e-mail. Qual serviço do Azure Databricks deve ser utilizado?",
            "options": [
                ("Databricks Workflows (Jobs multitarefas com DAG de dependências).", True, "Correto. O Databricks Workflows é o orquestrador nativo totalmente gerenciado do Lakehouse para orquestrar DAGs de tarefas heterogêneas com dependências e controle de execução."),
                ("CRON tab no Linux pessoal do desenvolvedor.", False, "Incorreto. Não é corporativo, não escala e depende de máquina local ligada."),
                ("Agendador de tarefas do Windows Server local.", False, "Incorreto. Não gerencia clusters nem integra nativamente com recursos Databricks."),
                ("Databricks FileStore.", False, "Incorreto. FileStore é apenas armazenamento de arquivos no DBFS.")
            ],
            "explanation": "O Databricks Workflows é o orquestrador oficial para pipelines de dados corporativos no Lakehouse, suportando múltiplos tipos de tarefas (Notebooks, Scripts, Python Wheels, SQL, DLT, dbt), dependências e monitoramento."
        },
        # Q139
        {
            "scenario": "Em um Databricks Workflow multitarefas, a Tarefa 1 (Bronze Ingest) calcula o número total de linhas ingeridas e precisa passar esse valor numérico para a Tarefa 2 (Silver Transform) para validação de volume. Qual funcionalidade do Databricks Jobs permite compartilhar variáveis e métricas entre tarefas do mesmo DAG?",
            "options": [
                ("Task Values, utilizando dbutils.jobs.taskValues.set(key, value) na tarefa 1 e dbutils.jobs.taskValues.get(taskKey, key) na tarefa 2.", True, "Correto. Task Values é a funcionalidade oficial para comunicação e passagem de parâmetros dinâmicos entre tarefas de um Databricks Workflow."),
                ("Gravar o valor em um post-it colado no monitor.", False, "Incorreto. Resposta fictícia."),
                ("Passar o valor através da URL do navegador web.", False, "Incorreto. Jobs em produção rodam de forma autônoma sem navegador."),
                ("Alterar o nome do cluster para o número de linhas ingeridas.", False, "Incorreto. Inviável e tecnicamente sem sentido.")
            ],
            "explanation": "A API `dbutils.jobs.taskValues` foi projetada especificamente para permitir que tarefas em um DAG compartilhem pequenos estados, contadores, IDs ou metadados de execução com tarefas downstream."
        },
        # Q140
        {
            "scenario": "Um job multitarefa de 6 etapas falhou na etapa 5 devido a um timeout passageiro de conexão com uma API externa. As etapas 1, 2, 3 e 4 foram concluídas com sucesso e consumiram 45 minutos de processamento. Qual ação deve ser executada pelo operador de dados para economizar tempo e custos de DBUs?",
            "options": [
                ("Executar um Repair Run (Reparar Execução) no Databricks Workflows, que reexecutará exclusivamente a etapa 5 que falhou e suas dependências downstream.", True, "Correto. O Repair Run evita o reprocessamento desnecessário das etapas 1 a 4 que já concluíram com sucesso, poupando tempo e DBUs."),
                ("Reiniciar o job inteiro do zero, recalculando as etapas 1, 2, 3 e 4 novamente.", False, "Incorreto. Desperdiça 45 minutos de computação e gera custos duplicados de DBUs."),
                ("Excluir o workspace e recriar toda a infraestrutura da nuvem.", False, "Incorreto. Desproporcional e destrutivo."),
                ("Ignorar o erro e marcar o relatório como concluído.", False, "Incorreto. Deixaria os dados incompletos em produção.")
            ],
            "explanation": "O recurso `Repair Run` é um dos diferenciais mais importantes de confiabilidade do Databricks Workflows: ele permite reexecutar apenas os nós falhados do DAG, aproveitando os outputs válidos das etapas anteriores."
        },
        # Q141
        {
            "scenario": "Uma equipe de engenharia precisa gerenciar todos os seus recursos de dados (workflows, pipelines DLT, clusters e tabelas) como código (Infrastructure as Code - IaC) com controle de versão Git e automação de CI/CD. Qual ferramenta oficial da Databricks provê essa padronização?",
            "options": [
                ("Databricks Asset Bundles (DABs) utilizando o arquivo databricks.yml.", True, "Correto. Databricks Asset Bundles (DABs) é o padrão oficial de IaC e CI/CD para declarar, versionar, validar e implantar pipelines e recursos Databricks em múltiplos ambientes."),
                ("Docker Compose executando containers locais em notebooks.", False, "Incorreto. Docker Compose não gerencia recursos na nuvem do Azure Databricks."),
                ("Scripts manuais em VBA no Excel.", False, "Incorreto. Incompatível com DevOps moderno de dados."),
                ("Terraform local sem suporte ao Databricks Provider.", False, "Incorreto. DABs é a ferramenta nativa de bundles oficial do exame DP-750.")
            ],
            "explanation": "Databricks Asset Bundles (DABs) permitem definir pipelines, jobs e configurações em arquivos YAML (`databricks.yml`), suportando validação estática (`databricks bundle validate`) e deploys automatizados em CI/CD."
        },
        # Q142
        {
            "scenario": "Qual comando da Databricks CLI é utilizado para validar a sintaxe dos arquivos YAML, caminhos de notebooks e definições de recursos de um bundle antes de qualquer deploy?",
            "options": [
                ("databricks bundle validate", True, "Correto. O comando databricks bundle validate checa a sintaxe estrutural do databricks.yml e a existência dos recursos sem alterar o ambiente."),
                ("databricks bundle test-everything", False, "Incorreto. Comando inexistente."),
                ("az databricks bundle check-syntax", False, "Incorreto. Comando inexistente na Azure CLI."),
                ("databricks check --all-yaml", False, "Incorreto. Comando inexistente.")
            ],
            "explanation": "A instrução `databricks bundle validate` verifica se a sintaxe do bundle, variáveis e referências a arquivos de código estão corretas, sendo o passo obrigatório inicial em esteiras de CI/CD."
        },
        # Q143
        {
            "scenario": "Qual comando da Databricks CLI realiza o deploy e a execução imediata de um job chamado 'pipeline_vendas' no ambiente de produção definido como target 'prod'?",
            "options": [
                ("databricks bundle deploy -t prod && databricks bundle run -t prod pipeline_vendas", True, "Correto. O comando deploy com flag -t prod implanta os recursos no target especificado e bundle run -t prod executa o job."),
                ("databricks deploy-all --force-prod --run-now", False, "Incorreto. Sintaxe inexistente."),
                ("git push origin prod --auto-deploy", False, "Incorreto. O git push atualiza o repositório, mas o comando oficial de bundle é via Databricks CLI."),
                ("az databricks job start --prod pipeline_vendas", False, "Incorreto. Sintaxe inválida.")
            ],
            "explanation": "O fluxo de trabalho com DABs utiliza `databricks bundle deploy -t <target>` para publicar a infraestrutura como código e `databricks bundle run -t <target> <job_key>` para disparar a execução."
        },
        # Q144
        {
            "scenario": "Em um pipeline de CI/CD corporativo no Azure DevOps para deploy de Databricks Asset Bundles em produção, como a esteira deve se autenticar no Azure Databricks sem utilizar senhas de desenvolvedores?",
            "options": [
                ("Utilizar um Service Principal do Microsoft Entra ID com autenticação federada baseada em tokens OIDC (OpenID Connect) ou Client Secret corporativo.", True, "Correto. Service Principals com federação OIDC garantem autenticação headless segura sem chaves expostas no código do pipeline de CI/CD."),
                ("Gravar o Personal Access Token (PAT) do estagiário de dados no arquivo README.md.", False, "Incorreto. Violação gravíssima de segurança."),
                ("Abrir uma sessão de navegador remoto e fazer login com usuário e senha manual a cada deploy.", False, "Incorreto. Incompatível com automação de CI/CD."),
                ("Desabilitar o firewall e liberar acesso anônimo sem credenciais.", False, "Incorreto. Inadmissível em ambientes corporativos.")
            ],
            "explanation": "Esteiras de CI/CD modernas no Azure DevOps e GitHub Actions utilizam Service Principals do Microsoft Entra ID com federação de credenciais de carga de trabalho (OIDC), eliminando segredos hardcoded."
        },
        # Q145
        {
            "scenario": "Ao analisar a Spark UI de uma consulta lenta, o engenheiro nota que em um dos estágios de Shuffle há a métrica: 'Spill (Memory): 45 GB' e 'Spill (Disk): 18 GB'. O que essa métrica indica e qual é a ação corretiva imediata?",
            "options": [
                ("Os dados intermediários do shuffle excederam a memória RAM dos slots dos executores e foram gravados no disco local; aumentar o número de partições de shuffle (spark.sql.shuffle.partitions) ou usar VMs com mais memória (Memory-Optimized).", True, "Correto. Spill ocorre quando os executores ficam sem RAM para acomodar partições de shuffle e são forçados a fazer swap em disco, degradando a performance."),
                ("O cluster sofreu um ataque hacker de vazamento de dados.", False, "Incorreto. Spill é uma métrica normal de gestão de memória interna do Spark."),
                ("O Databricks apagou os dados do ADLS Gen2.", False, "Incorreto. Dados persistem no storage."),
                ("A consulta já terminou e não precisa de nenhuma ação.", False, "Incorreto. Spill para disco é uma das maiores causas de lentidão em pipelines Spark.")
            ],
            "explanation": "Spill (Memory/Disk) ocorre quando uma partição de dados é grande demais para caber na RAM do executor durante um join ou agregação com shuffle. A solução é aumentar o paralelismo (`spark.sql.shuffle.partitions`) ou migrar para instâncias com maior razão de memória por core."
        },
        # Q146
        {
            "scenario": "Ao verificar o plano de execução de uma consulta no Spark através de EXPLAIN EXTENDED, o engenheiro procura confirmar se a aceleração do Photon Engine está ativa. Qual indício no plano físico confirma a execução em C++ vetorizado pelo Photon?",
            "options": [
                ("Os nós de execução do plano físico possuem o prefixo 'Photon' (ex: PhotonScan, PhotonFilter, PhotonGroupingAgg, PhotonShuffleExchangeExec).", True, "Correto. O motor Photon substitui os operadores tradicionais de WholeStageCodegen da JVM por nós nativos com prefixo Photon."),
                ("A palavra 'JAVA_BYTECODE_TUNGSTEN' é repetida em todas as linhas.", False, "Incorreto. Isso indicaria a execução clássica na JVM sem aceleração Photon."),
                ("O plano físico é substituído por uma imagem PNG com a foto de uma lâmpada.", False, "Incorreto. Resposta fictícia."),
                ("Aparece uma mensagem informando que a consulta será executada no Microsoft Excel.", False, "Incorreto. Resposta fictícia.")
            ],
            "explanation": "Na Spark UI e nos planos físicos do Catalyst, a presença de operadores com prefixo `Photon` (ex: `PhotonFilter`, `PhotonScan`, `PhotonHashAggregate`) atesta que a execução está sendo realizada nativamente pelo motor vetorizado C++."
        },
        # Q147
        {
            "scenario": "Por que o uso de funções definidas pelo usuário (UDFs) tradicionais escritas em Python nativo (com @udf) pode fazer com que uma consulta perca os benefícios de aceleração do Photon Engine?",
            "options": [
                ("UDFs Python tradicionais não podem ser executadas nativamente no motor C++ do Photon e forçam o Spark a serializar dados entre a JVM e o processo Python linha a linha (fallback), degradando a performance.", True, "Correto. UDFs Python tradicionais forçam a execução fora do Photon, causando perda das otimizações vetorizadas e sobrecarga de serialização IPC."),
                ("O Photon desinstala o Python do computador sempre que uma UDF é criada.", False, "Incorreto. O interpretador Python continua existindo, apenas a query sofre fallback."),
                ("UDFs Python consomem 100% dos créditos da Azure em 1 segundo.", False, "Incorreto. Resposta exagerada e incorreta."),
                ("O Python não é uma linguagem suportada pelo Apache Spark.", False, "Incorreto. PySpark é uma das principais interfaces do Spark.")
            ],
            "explanation": "O motor Photon vetorizado opera nativamente em C++. Funções UDF Python linha a linha exigem serialização de dados via pipes locais, impedindo que os operadores sejam convertidos para nós Photon e desacelerando o processamento."
        },
        # Q148
        {
            "scenario": "Uma organização precisa monitorar diariamente o custo de DBUs de todos os Databricks Workflows em execução para identificar jobs com custos anômalos. Qual consulta na tabela system.billing.usage calcula o total de DBUs consumidos por cada Job ID nos últimos 7 dias?",
            "options": [
                ("SELECT usage_metadata.job_id, SUM(usage_quantity) AS total_dbus FROM system.billing.usage WHERE usage_date >= current_date() - INTERVAL 7 DAYS AND usage_metadata.job_id IS NOT NULL GROUP BY 1 ORDER BY total_dbus DESC;", True, "Correto. A coluna usage_quantity contém os DBUs e usage_metadata.job_id identifica o Workflow orquestrado."),
                ("SELECT * FROM system.access.audit WHERE action_name = 'JOB_COST';", False, "Incorreto. system.access.audit registra eventos de segurança, não faturamento financeiro de DBUs."),
                ("SELECT job_name, sum(money) FROM azure.billing_portal;", False, "Incorreto. Consulta fictícia fora do schema de System Tables do Unity Catalog."),
                ("SELECT sum(hours) FROM system.information_schema.jobs;", False, "Incorreto. Information schema não registra consumo de faturamento.")
            ],
            "explanation": "A tabela do sistema `system.billing.usage` registra o consumo de DBUs em `usage_quantity` com metadados do job em `usage_metadata.job_id`, permitindo relatórios precisos de FinOps por workload."
        },
        # Q149
        {
            "scenario": "Um job multitarefa de engenharia de dados precisa ser disparado automaticamente assim que novos arquivos forem depositados em um container específico do ADLS Gen2, sem polling e sem agendamento fixo de horário. Qual tipo de gatilho (Trigger) do Databricks Workflows deve ser configurado?",
            "options": [
                ("File Arrival Trigger (Gatilho por Chegada de Arquivo).", True, "Correto. O File Arrival Trigger monitora um caminho de armazenamento e dispara o Databricks Workflow imediatamente após a detecção de novos arquivos."),
                ("Cron Trigger semanal às sextas-feiras.", False, "Incorreto. O agendamento por Cron é fixo e não reage à chegada imediata de arquivos."),
                ("Trigger manual dependente de clique do usuário.", False, "Incorreto. Não provê automação contínua de produção."),
                ("Trigger por temperatura do data center.", False, "Incorreto. Resposta fictícia.")
            ],
            "explanation": "Databricks Workflows suporta `File Arrival Triggers`, permitindo que o job seja acionado por eventos de chegada de novos arquivos no storage em nuvem, garantindo baixa latência de orquestração."
        },
        # Q150
        {
            "scenario": "Qual parâmetro de configuração em um Databricks Workflow impede que múltiplas execuções do mesmo job acumulem-se em fila simultaneamente quando a execução anterior demorar mais do que o esperado?",
            "options": [
                ("Maximum concurrent runs = 1 (Execuções simultâneas máximas = 1).", True, "Correto. Ao limitar max_concurrent_runs para 1, novas execuções agendadas são ignoradas ou enfileiradas ordenadamente sem sobrecarregar clusters concorrentes."),
                ("Timeout = 0 seconds.", False, "Incorreto. Timeout zero cancelaria o job imediatamente."),
                ("Retry limit = 1000.", False, "Incorreto. Limite alto de retentativas aumentaria a concorrência e o consumo de recursos."),
                ("Auto-delete job on slow run.", False, "Incorreto. Parâmetro inexistente.")
            ],
            "explanation": "O atributo `max_concurrent_runs` define o número máximo de instâncias ativas simultâneas de um job. Configurar para 1 previne sobreposição de execuções concorrentes do mesmo pipeline."
        },
        # Q151
        {
            "scenario": "Em um Databricks Asset Bundle (DABs), como um engenheiro define configurações específicas para o ambiente de desenvolvimento (dev) e sobrescreve para o ambiente de produção (prod) no mesmo arquivo databricks.yml?",
            "options": [
                ("Utilizando a seção 'targets:' com blocos independentes para 'dev' (ex: mode: development) e 'prod' (ex: mode: production) parametrizando variáveis de catálogo, workspace e clusters.", True, "Correto. A seção 'targets' do databricks.yml permite declarar múltiplos ambientes mantendo o mesmo código de pipeline e parametrizando recursos."),
                ("Criando 50 arquivos databricks.yml com nomes diferentes e copiando manualmente.", False, "Incorreto. Péssima prática que duplica código e gera erros operacionais."),
                ("Excluindo o arquivo databricks.yml antes de fazer deploy em produção.", False, "Incorreto. Sem o arquivo de bundle, o deploy de DABs não funciona."),
                ("Instalando o Azure Databricks dentro de um pendrive USB.", False, "Incorreto. Resposta fictícia.")
            ],
            "explanation": "O recurso de `targets` no DABs (`databricks.yml`) viabiliza a parametrização de múltiplos ambientes (dev, staging, prod) em um único projeto de infraestrutura como código."
        },
        # Q152
        {
            "scenario": "Ao analisar a Spark UI, um engenheiro observa tarefas que apresentam pausas longas de 'GC Time' (tempo de Garbage Collection da JVM) consumindo mais de 35% do tempo total de execução da task. Qual é a causa raiz provável e a ação corretiva recomendada?",
            "options": [
                ("Causa: Criação excessiva de objetos temporários na memória Java/Scala da JVM; Ação: Migrar para clusters acelerados pelo Photon Engine (que gerencia memória fora da JVM em C++) ou otimizar transformações para evitar instanciação excessiva de objetos.", True, "Correto. O Photon Engine elimina pausas de Garbage Collection da JVM executando os operadores nativamente em C++ fora da heap do Java."),
                ("Causa: A tela do computador do analista está com brilho excessivo.", False, "Incorreto. Resposta fictícia."),
                ("Causa: A tabela Delta foi criada sem nome.", False, "Incorreto. Tabelas exigem identificadores."),
                ("Causa: O cabo de energia da máquina virtual foi desconectado.", False, "Incorreto. Resposta fictícia.")
            ],
            "explanation": "Pausas prolongadas de Garbage Collection (GC Time alto na Spark UI) decorrem de saturação da memória heap da JVM do Java. O motor Photon em C++ mitiga esse problema gerenciando a memória fora da JVM."
        },
        # Q153
        {
            "scenario": "Como um operador do Databricks configura alertas de notificação em um Workflow para ser avisado caso um job crítico falhe ou demore mais de 60 minutos para concluir?",
            "options": [
                ("Configurar 'Notifications' nas configurações do Job, adicionando e-mails ou webhooks (Slack/Teams) para os eventos 'Failure' e definir 'Duration threshold' para 60 minutos.", True, "Correto. O Databricks Workflows possui suporte nativo para notificações de falha, sucesso e limite de tempo de duração (duration threshold) via e-mail e webhook."),
                ("Ligar para a central de atendimento da Microsoft a cada hora.", False, "Incorreto. Incompatível com monitoramento automatizado."),
                ("Criar um loop infinito com while(True) print('alerta').", False, "Incorreto. Travaria o nó e geraria custos desnecessários."),
                ("Desabilitar o log do Spark para evitar registros de erro.", False, "Incorreto. Ocultaria problemas e impediria diagnósticos.")
            ],
            "explanation": "O Databricks Workflows suporta notificações orientadas a eventos e alertas de SLA (duration thresholds), enviando alertas por e-mail ou disparando webhooks para PagerDuty, Slack ou Microsoft Teams."
        },
        # Q154
        {
            "scenario": "Quais DUAS vantagens tornam o Databricks Asset Bundles (DABs) a ferramenta recomendada de automação de engenharia de software para projetos corporativos de Lakehouse? (Selecione duas opções)",
            "options": [
                ("Permite versionar a infraestrutura completa de pipelines, jobs e permissões junto com o código de engenharia no repositório Git.", True, "Correto. DABs aplica princípios de Infrastructure as Code (IaC) unificando código de negócio e definições de orquestração no mesmo repositório."),
                ("Habilita testes automatizados e validação estática de sintaxe (databricks bundle validate) antes do deploy em ambientes produtivos.", True, "Correto. A validação estática pré-deploy reduz falhas em produção e integra nativamente em esteiras de CI/CD."),
                ("Substitui o motor Apache Spark por um interpretador de arquivos BAT do MS-DOS.", False, "Incorreto. Resposta fictícia."),
                ("Exclui todos os dados do cliente após cada commit de Git.", False, "Incorreto. DABs gerencia pipelines e recursos, não descarta dados de negócio."),
                ("Permite executar o Databricks em computadores Commodore 64 sem nuvem.", False, "Incorreto. Resposta fictícia.")
            ],
            "type": "multiple",
            "explanation": "DABs une Infrastructure as Code (IaC), controle de versão Git, validação prévia de configurações e automação de deploys multi-ambiente, sendo a metodologia oficial do DP-750."
        },
        # Q155
        {
            "scenario": "Em um pipeline de produção, um notebook executa o comando df.toPandas() em um DataFrame contendo 800 milhões de linhas. O que acontecerá durante a execução e qual é a boa prática recomendada?",
            "options": [
                ("O comando enviará centenas de gigabytes de dados de todos os executores para a memória RAM do nó Driver, causando falha fatal por OutOfMemory (Driver OOM); deve-se evitar toPandas() com grandes volumes ou usar PySpark distribuído.", True, "Correto. toPandas() coleta todo o dataset distribuído no nó único do Driver; grandes volumes causam Driver OOM imediatamente."),
                ("O comando executará em 1 milissegundo sem usar memória.", False, "Incorreto. A coleta de centenas de milhões de linhas satura a rede e a memória do Driver."),
                ("O nó Driver alocará automaticamente 500 Terabytes de swap no ADLS Gen2.", False, "Incorreto. O Driver tentará alocar na memória física da VM e falhará."),
                ("O Pandas distribuirá o processamento em 100 máquinas virtuais.", False, "Incorreto. A biblioteca Pandas tradicional opera estritamente em nó único.")
            ],
            "explanation": "Operações como `df.collect()` e `df.toPandas()` puxam os dados de todos os nós workers para o Driver. Em grandes volumes, isso satura a memória do nó Driver e causa `java.lang.OutOfMemoryError`."
        },
        # Q156
        {
            "scenario": "Qual recurso de governança do Unity Catalog monitora a linhagem ponta a ponta e permite avaliar o impacto em relatórios de Power BI antes de excluir uma tabela ou coluna da camada Gold?",
            "options": [
                ("Unity Catalog Automated Lineage (Linhagem Automatizada no Catalog Explorer).", True, "Correto. O Catalog Explorer exibe o grafo visual de dependências upstream e downstream conectando fontes, tabelas Silver, tabelas Gold e relatórios de BI conectados."),
                ("Histórico de navegação do navegador do desenvolvedor.", False, "Incorreto. Não provê grafo corporativo de dependências."),
                ("Um arquivo de texto README preenchido manualmente em 2019.", False, "Incorreto. Documentação manual fica rapidamente desatualizada."),
                ("Desligar o banco de dados e esperar reclamações de usuários.", False, "Incorreto. Abordagem destrutiva e inaceitável em produção.")
            ],
            "explanation": "A Linhagem Automatizada do Unity Catalog mapeia as dependências entre consultas, tabelas e visualizações de BI, permitindo análise proativa de impacto antes de qualquer modificação de schema."
        },
        # Q157
        {
            "scenario": "Um job orquestrado no Databricks Workflows precisa executar uma tarefa condicional: se a Tarefa 1 processar mais de 10.000 registros, executa a Tarefa A; caso contrário, executa a Tarefa B. Qual recurso do orquestrador viabiliza essa lógica?",
            "options": [
                ("Tarefa do tipo 'If/else condition' (Condição Se/Senão) configurada no DAG do Databricks Workflow.", True, "Correto. O Databricks Workflows suporta tarefas nativas de condição If/else que avaliam expressões booleanas e direcionam o fluxo de execução no grafo."),
                ("Desconectar o cabo de rede da máquina virtual worker.", False, "Incorreto. Provocaria falha no cluster."),
                ("Criar dois workspaces Databricks diferentes na Azure.", False, "Incorreto. Desnecessário e custoso."),
                ("Instalar um robô físico que aperta botões no teclado do servidor.", False, "Incorreto. Resposta fictícia.")
            ],
            "explanation": "Tarefas do tipo `If/else condition` no Databricks Workflows permitem criar fluxos de decisão dinâmicos no DAG baseados em Task Values ou parâmetros do job sem código customizado de controle."
        },
        # Q158
        {
            "scenario": "Em um pipeline Delta Live Tables em produção, como a equipe garante que tabelas criadas no pipeline sejam publicadas e consultáveis por outros analistas diretamente no Unity Catalog com governança RBAC?",
            "options": [
                ("Configurar a propriedade 'Target' do pipeline DLT para um Catálogo e Schema governados no Unity Catalog (ex: catalog: prod_lakehouse, target schema: gold).", True, "Correto. Ao definir um catálogo do Unity Catalog e um schema alvo nas configurações do DLT, as tabelas e visões materializadas são registradas com governança unificada."),
                ("Gravar as tabelas em disquetes físicos.", False, "Incorreto. Resposta fictícia."),
                ("Exportar todos os dados para arquivos CSV sem schema.", False, "Incorreto. Perde governança e desempenho."),
                ("Desativar o Unity Catalog e publicar no Hive Metastore legado.", False, "Incorreto. O Hive Metastore não possui a governança moderna exigida pelo DP-750.")
            ],
            "explanation": "O Delta Live Tables integra nativamente com o Unity Catalog: basta configurar o catálogo de destino e schema na interface do pipeline para que as tabelas sejam criadas como securable objects no catálogo."
        },
        # Q159
        {
            "scenario": "Ao verificar o plano físico de uma consulta de Join entre duas tabelas, o engenheiro identifica o operador 'CartesianProduct'. Qual é a implicação desse operador para o desempenho do cluster?",
            "options": [
                ("O operador multiplica cada linha da primeira tabela por todas as linhas da segunda tabela (produto cartesiano O(N*M)), causando consumo massivo de CPU, lentidão crítica e potencial esgotamento de memória.", True, "Correto. CartesianProduct indica ausência ou ineficácia de predicado de junção, gerando uma explosão de linhas que sobrecarrega os nós do cluster."),
                ("O operador é a otimização mais rápida e eficiente do Apache Spark.", False, "Incorreto. Produto cartesiano é a operação mais pesada e dispendiosa possível."),
                ("O operador indica que a consulta foi concluída em zero segundos.", False, "Incorreto. Indica exatamente o oposto: alto risco de timeout e lentidão."),
                ("O operador desliga todos os discos SSD dos nós workers.", False, "Incorreto. Não afeta hardware diretamente.")
            ],
            "explanation": "A presença de `CartesianProduct` em planos físicos revela queries sem cláusula ON ou com condições booleanas incorretas, gerando multiplicação exponencial de linhas e travamento de clusters."
        },
        # Q160
        {
            "scenario": "Uma organização multinacional precisa garantir que todos os deploys de código em seu Workspace do Azure Databricks passem por aprovação de Pull Request em repositório Git corporativo, com testes automatizados executando 'databricks bundle validate'. Como essa esteira garante conformidade com o exame DP-750?",
            "options": [
                ("Implementando automação de CI/CD com Databricks Asset Bundles (DABs) e branch protection rules no Git, eliminando edições manuais diretas em produção.", True, "Correto. A metodologia oficial exige esteiras declarativas de CI/CD via DABs e Git Folders, prevenindo modificações manuais não auditadas em ambientes produtivos."),
                ("Exigindo que cada programador altere arquivos .py diretamente no portal da nuvem em produção.", False, "Incorreto. Prática amadora e perigosa proibida em governança de engenharia de dados."),
                ("Desabilitar o Git e utilizar mensagens de WhatsApp para trocar código.", False, "Incorreto. Totalmente inadequado e sem conformidade."),
                ("Copiar código via comandos de Ctrl+C e Ctrl+V no bloco de notas.", False, "Incorreto. Sem rastreabilidade nem controle de versão.")
            ],
            "explanation": "A governança de produção exigida no DP-750 requer automação de CI/CD via Databricks Asset Bundles, proteção de branches no Git e validação automatizada de código antes da promoção para produção."
        },
        # Q161
        {
            "scenario": "Em um pipeline de streaming com DLT, o cluster precisa escalar trabalhadores de forma dinâmica para absorver picos de tráfego de dados na Black Friday sem exceder o orçamento mensal. Qual recurso de dimensionamento inteligente do DLT deve ser habilitado?",
            "options": [
                ("Enhanced Autoscaling do Delta Live Tables, que otimiza a alocação de nós minimizando o tempo de resposta e desligando workers ociosos instantaneamente.", True, "Correto. O Enhanced Autoscaling do DLT é especializado em workloads de streaming, escalando nós com base no atraso do backlog de mensagens sem desperdiçar recursos."),
                ("Manter 500 máquinas ligadas durante todo o ano.", False, "Incorreto. Geraria custo financeiro abusivo e desperdício de orçamento."),
                ("Desabilitar o autoscaling e fixar em 1 único nó worker.", False, "Incorreto. Provocaria fila de atraso e perda de SLA na Black Friday."),
                ("Desligar o cluster durante os horários de pico.", False, "Incorreto. Inviabilizaria as vendas da empresa.")
            ],
            "explanation": "O `Enhanced Autoscaling` do Delta Live Tables é otimizado especificamente para streaming: ele analisa a taxa de chegada de dados e o tempo de fila para alocar a quantidade exata de nós necessária para cumprir o SLA."
        },
        # Q162
        {
            "scenario": "Qual comando da Databricks CLI remove com segurança todos os recursos e jobs provisionados por um bundle no ambiente de desenvolvimento após a conclusão dos testes?",
            "options": [
                ("databricks bundle destroy -t dev", True, "Correto. O comando bundle destroy limpa e exclui todos os recursos criados pelo bundle no target especificado sem afetar outros ambientes."),
                ("rm -rf /databricks/all", False, "Incorreto. Comando perigoso de sistema operacional que não limpa recursos na nuvem."),
                ("az databricks delete-everything --force", False, "Incorreto. Comando inexistente na Azure CLI."),
                ("databricks wipe-clean", False, "Incorreto. Sintaxe inexistente.")
            ],
            "explanation": "O comando `databricks bundle destroy -t <target>` remove ordenadamente os jobs, pipelines e recursos provisionados pelo bundle naquele ambiente específico, garantindo higiene de nuvem e controle de custos."
        },
        # Q163
        {
            "scenario": "Um engenheiro de dados observa falhas intermitentes em uma tarefa de notebook em um Databricks Workflow devido a indisponibilidade momentânea de 30 segundos na conexão com um serviço externo. Qual configuração da tarefa no Workflow resolve o problema sem necessidade de intervenção humana?",
            "options": [
                ("Configurar política de 'Retries' (Retentativas) na tarefa (ex: 3 tentativas com intervalo de espera).", True, "Correto. A política nativa de Retries do Databricks Workflows reexecuta automaticamente tarefas que sofreram falhas transitórias com intervalos configurados."),
                ("Contratar um operador humano para ficar vigiando o monitor 24 horas por dia.", False, "Incorreto. Ineficiente e custoso."),
                ("Excluir a tarefa do pipeline para que o erro não apareça mais.", False, "Incorreto. Deixaria o pipeline incompleto e sem os dados necessários."),
                ("Desligar o alerta de falhas no e-mail corporativo.", False, "Incorreto. Ocultar erros é má prática.")
            ],
            "explanation": "A configuração de `Retries` em tarefas de Databricks Workflows fornece tolerância a falhas transitórias de rede ou APIs de terceiros, reexecutando a tarefa automaticamente conforme o limite estipulado."
        },
        # Q164
        {
            "scenario": "Como um arquiteto pode verificar se o Unity Catalog está registrando corretamente a linhagem de dados gerada por um pipeline orquestrado pelo Databricks Workflows?",
            "options": [
                ("Consultando a tabela de sistema system.lineage.table_lineage ou navegando na aba 'Lineage' da tabela no Catalog Explorer.", True, "Correto. As tabelas do schema system.lineage e o Catalog Explorer provêm visão completa e auditável da linhagem gerada por qualquer workflow."),
                ("Abrindo o arquivo win.ini no Windows.", False, "Incorreto. Resposta fictícia."),
                ("Procurando comentários no código fonte de 10 anos atrás.", False, "Incorreto. Não reflete linhagem ativa do catálogo."),
                ("Perguntando em fóruns públicos da internet.", False, "Incorreto. Não acessa a linhagem privada da empresa.")
            ],
            "explanation": "O schema de tabelas do sistema `system.lineage` (`table_lineage` e `column_lineage`) armazena programaticamente todo o histórico de transformações e dependências capturadas pelo Unity Catalog."
        },
        # Q165
        {
            "scenario": "Em um Databricks Workflow com 4 tarefas em paralelo que convergem para uma tarefa final de agregação, qual condição de execução deve ser definida na tarefa final para que ela execute apenas quando TODAS as 4 tarefas anteriores terminarem com sucesso?",
            "options": [
                ("Run if dependencies: 'All succeeded' (Todas com sucesso).", True, "Correto. 'All succeeded' é a condição padrão que exige sucesso completo de todas as tarefas upstream antes de iniciar a etapa dependente."),
                ("Run if dependencies: 'At least one failed'.", False, "Incorreto. Dispararia se houvesse falha, ideal para tarefas de tratamento de erro ou alerta."),
                ("Run if dependencies: 'None succeeded'.", False, "Incorreto. Exigiria que todas falhassem."),
                ("Run whenever random() > 0.5.", False, "Incorreto. Resposta fictícia.")
            ],
            "explanation": "No Databricks Workflows, a propriedade `Run if dependencies` controla o disparo condicional: `All succeeded` (padrão), `At least one succeeded`, `None failed`, `All failed` ou `At least one failed`."
        },
        # Q166
        {
            "scenario": "Um analista precisa validar se o consumo de DBUs de um cluster de produção está seguindo a política de custos estabelecida pelo comitê de FinOps da empresa. Qual informação contida na tabela system.billing.usage identifica a política de cluster aplicada na criação da máquina?",
            "options": [
                ("A coluna 'usage_metadata.cluster_policy_id', que registra o ID da Cluster Policy associada à execução.", True, "Correto. O campo usage_metadata.cluster_policy_id em system.billing.usage permite rastrear se o cluster foi provisionado em conformidade com as políticas aprovadas."),
                ("A cor do ícone do cluster no navegador web.", False, "Incorreto. Não é um dado estruturado de faturamento."),
                ("O endereço MAC da placa de rede física.", False, "Incorreto. Metadado de baixo nível de rede que não identifica políticas de FinOps."),
                ("O nome do usuário do Skype do desenvolvedor.", False, "Incorreto. Resposta fictícia.")
            ],
            "explanation": "A tabela `system.billing.usage` armazena o `cluster_policy_id` dentro do struct `usage_metadata`, permitindo correlacionar os gastos financeiros com as regras de governança e FinOps da organização."
        },
        # Q167
        {
            "scenario": "Qual é a principal recomendação para garantir a rastreabilidade e integridade de deploys de código em workspaces de Desenvolvimento, Staging e Produção?",
            "options": [
                ("Utilizar Databricks Asset Bundles integrados a branches protegidas no Git (ex: main para prod, develop para dev) com deploys automatizados via Service Principal em CI/CD.", True, "Correto. Este fluxo garante imutabilidade, revisão por pares (code review), testes de integridade e auditoria completa em todos os ambientes."),
                ("Pedir para cada programador enviar seus arquivos .py por e-mail para o diretor de TI aos sábados.", False, "Incorreto. Manual, inseguro e sem controle de versão."),
                ("Criar apenas 1 único ambiente de desenvolvimento e executar testes diretamente na base de dados de produção dos clientes.", False, "Incorreto. Viola normas básicas de segurança e governança corporativa."),
                ("Desabilitar o controle de versão e permitir edição anônima de código em produção.", False, "Incorreto. Totalmente inaceitável em qualquer empresa séria.")
            ],
            "explanation": "O padrão corporativo oficial do DP-750 para governança de código exige Databricks Asset Bundles (DABs), repositórios Git corporativos e esteiras de CI/CD automatizadas sem intervenção manual em produção."
        },
        # Q168
        {
            "scenario": "Em uma esteira de CI/CD corporativa, qual comando da Databricks CLI é executado pelo pipeline de build para validar a integridade estrutural e parâmetros do bundle sem conectar a nenhum workspace nem disparar cobrança de DBUs?",
            "options": [
                ("databricks bundle validate", True, "Correto. databricks bundle validate valida localmente a consistência do databricks.yml e as referências aos arquivos de projeto sem custos de nuvem."),
                ("databricks bundle run --dry-run-all", False, "Incorreto. Sintaxe inexistente."),
                ("az databricks validate-bundle", False, "Incorreto. Comando não pertencente à Azure CLI padrão."),
                ("databricks test --syntax-only", False, "Incorreto. Sintaxe inexistente.")
            ],
            "explanation": "O comando `databricks bundle validate` é o primeiro teste executado em pull requests em esteiras de CI/CD para certificar que o arquivo YAML e os artefatos de código estão sintaticamente perfeitos antes do deploy."
        },
        # Q169
        {
            "scenario": "O que acontece se uma tarefa em um Databricks Workflow estiver configurada com 'Timeout = 30 minutes' e sua execução atingir 31 minutos?",
            "options": [
                ("O Databricks Workflows cancela a tarefa automaticamente com status TIMED_OUT e notifica os canais configurados (e-mail/webhook), evitando que jobs travados consumam DBUs indefinidamente.", True, "Correto. O timeout atua como trava de segurança financeira contra jobs travados em loops infinitos ou esperas de rede."),
                ("O cluster aumenta a memória RAM para 1 Terabyte para forçar o término.", False, "Incorreto. O timeout encerra a execução por segurança."),
                ("O computador do desenvolvedor é formatado.", False, "Incorreto. Resposta fictícia."),
                ("A consulta é enviada para ser processada em um servidor local on-premises.", False, "Incorreto. Não há transferência automática para on-premises.")
            ],
            "explanation": "Limites de timeout em tarefas de Databricks Workflows são essenciais para FinOps e governança: encerram execuções anômalas travadas antes que elas consumam orçamento excessivo de computação."
        },
        # Q170
        {
            "scenario": "Ao analisar a Spark UI de um job com lentidão, o engenheiro percebe na aba 'Storage' que uma tabela em cache está consumindo 98% da memória RAM de todos os executores, forçando os estágios seguintes a sofrerem GC Pause constante. Qual comando deve ser inserido no código para liberar a memória desse cache após o uso?",
            "options": [
                ("df.unpersist() ou spark.catalog.clearCache()", True, "Correto. unpersist() libera os blocos da memória e do disco alocados pelo cache de um DataFrame, restaurando a capacidade de RAM dos executores."),
                ("df.delete_all_memory()", False, "Incorreto. Função inexistente no PySpark."),
                ("reboot_spark_now()", False, "Incorreto. Função inexistente."),
                ("spark.conf.set('spark.memory.kill', 'true')", False, "Incorreto. Propriedade fictícia.")
            ],
            "explanation": "DataFrames persistidos com `.cache()` ou `.persist()` devem ser liberados com `.unpersist()` logo após a etapa que deles necessita, devolvendo memória RAM aos executores para evitar Garbage Collection agressivo."
        },
        # Q171
        {
            "scenario": "Qual é a principal vantagem de utilizar Serverless Compute para Databricks Workflows em comparação com a criação manual de Job Clusters clássicos?",
            "options": [
                ("Tempo de inicialização imediato (menos de 10 segundos vs 4-6 minutos de VM clássica), sem preocupação com cotas de vCPUs da assinatura Azure e gerenciamento automatizado de performance pela Databricks.", True, "Correto. O Serverless Jobs elimina o atrito de inicialização a frio de máquinas virtuais clássicas e remove a dependência de cotas de VMs na assinatura da Azure."),
                ("Permite executar código sem nenhum acesso à internet.", False, "Incorreto. Requer conexão em nuvem normal."),
                ("Desabilita transações ACID para ganhar velocidade.", False, "Incorreto. Delta Lake ACID permanece 100% ativo."),
                ("Substitui todas as linguagens por COBOL.", False, "Incorreto. Resposta fictícia.")
            ],
            "explanation": "Serverless Compute para Workflows reduz drasticamente o tempo total de execução de pipelines curtos (eliminando o boot time de 5 minutos de VMs) e abstrai o gerenciamento de infraestrutura da assinatura do cliente."
        },
        # Q172
        {
            "scenario": "Em um Databricks Workflow, qual é a sintaxe correta para referenciar um parâmetro dinâmico chamado 'data_processamento' passado na execução do job dentro de um comando SQL ou notebook?",
            "options": [
                ("{{job.parameters.data_processamento}}", True, "Correto. A sintaxe de substituição de parâmetros dinâmicos em Databricks Jobs utiliza chaves duplas: {{job.parameters.<param_name>}}."),
                ("$$param:data_processamento$$", False, "Incorreto. Sintaxe inexistente no Databricks."),
                ("SELECT param FROM windows_registry;", False, "Incorreto. Inexistente."),
                ("#[data_processamento]", False, "Incorreto. Sintaxe inválida.")
            ],
            "explanation": "No Databricks Workflows, a interpolação de parâmetros dinâmicos de jobs e tarefas utiliza a sintaxe Jinja-like padrão: `{{job.parameters.<param_name>}}` ou `{{tasks.<task_name>.values.<key>}}`."
        },
        # Q173
        {
            "scenario": "Um arquiteto precisa auditar quais usuários do Azure Databricks acessaram tabelas com classificação de dados confidenciais nos últimos 30 dias. Qual consulta SQL provê essa resposta?",
            "options": [
                ("SELECT event_time, user_identity.email, request_params.table_name FROM system.access.audit WHERE service_name = 'unityCatalog' AND action_name = 'getTable' AND event_date >= current_date() - INTERVAL 30 DAYS;", True, "Correto. system.access.audit armazena o histórico completo de acesso a securables do Unity Catalog, incluindo user_identity.email e table_name."),
                ("SELECT * FROM system.billing.usage WHERE sku_name = 'CONFIDENTIAL';", False, "Incorreto. system.billing.usage registra custos de faturamento de DBUs."),
                ("SELECT * FROM default.user_history;", False, "Incorreto. Tabela inexistente no padrão de auditoria do sistema."),
                ("SHOW USERS ON SECRET_DATA;", False, "Incorreto. Sintaxe inexistente.")
            ],
            "explanation": "A tabela `system.access.audit` registra acessos de leitura e modificação a tabelas do Unity Catalog (`action_name = 'getTable'`, `generateTemporaryTableCredential`, etc.), atendendo a requisitos de conformidade SOX e LGPD."
        },
        # Q174
        {
            "scenario": "Um engenheiro de dados configura uma tarefa em um Databricks Workflow com 'Retry policy: 3 retries, retry interval: 60 seconds'. A tarefa falha em sua primeira execução devido a uma instabilidade passageira no ADLS Gen2 e tem sucesso na segunda tentativa. Como o Databricks Workflows registra a execução final do job?",
            "options": [
                ("O job é marcado como 'Success' (Sucesso), registrando no histórico detalhado que a primeira tentativa falhou mas a segunda foi bem-sucedida dentro da política de retry aprovada.", True, "Correto. A política de retry absorve a falha temporária e conclui a execução com sucesso sem disparar alertas desnecessários de parada de produção."),
                ("O job é marcado como 'Critical Failure' e todos os dados são apagados.", False, "Incorreto. A política de retentativa foi bem-sucedida."),
                ("O workspace é bloqueado permanentemente.", False, "Incorreto. Resposta fictícia."),
                ("A segunda tentativa é cancelada automaticamente.", False, "Incorreto. A segunda tentativa é executada e tem sucesso.")
            ],
            "explanation": "Políticas de Retry permitem que falhas transitórias de infraestrutura em nuvem sejam superadas automaticamente; o job é concluído com status de sucesso e os logs detalhados registram a retentativa para auditoria técnica."
        },
        # Q175
        {
            "scenario": "Em um projeto com Databricks Asset Bundles (DABs), onde ficam definidos os clusters, permissões e tarefas dos jobs que serão sincronizados com o workspace?",
            "options": [
                ("No arquivo de manifesto raiz databricks.yml e em arquivos YAML dentro da pasta 'resources/' do bundle.", True, "Correto. A especificação padrão de DABs organiza recursos em databricks.yml e arquivos modulares dentro do diretório resources/ (ex: resources/*.yml)."),
                ("Em um arquivo de texto no disco C:\\ sem formato definido.", False, "Incorreto. Resposta fictícia."),
                ("Dentro de uma chave de registro do Windows.", False, "Incorreto. Resposta fictícia."),
                ("Em um documento impresso guardado no cofre da empresa.", False, "Incorreto. Resposta fictícia.")
            ],
            "explanation": "O padrão arquitetural de Databricks Asset Bundles armazena as configurações globais em `databricks.yml` e as definições modulares de jobs, pipelines DLT e permissões na pasta `resources/` em formato YAML."
        },
        # Q176
        {
            "scenario": "Como o Spark UI ajuda um engenheiro de dados a identificar que um estágio de consulta está sofrendo de Data Skew em comparação com um gargalo de falta de nós executores?",
            "options": [
                ("No Data Skew, a barra de timeline e resumo de tasks exibe uma discrepância extrema (ex: 75th percentile = 2s, Max = 15 minutos), indicando que a imensa maioria das tasks concluiu rápido e apenas uma ou duas concentram volume de dados desproporcional.", True, "Correto. O descompasso estatístico entre a mediana (ou 75th percentile) e o valor máximo (Max task duration) no estágio da Spark UI é a assinatura inequívoca de Data Skew."),
                ("No Data Skew, todas as tasks demoram exatamente o mesmo tempo de 1 hora.", False, "Incorreto. Isso indicaria falta de paralelismo geral ou lentidão uniforme de I/O, não skew."),
                ("A Spark UI fica na cor vermelha e fecha o navegador.", False, "Incorreto. Resposta fictícia."),
                ("O Spark desliga o nó Driver automaticamente.", False, "Incorreto. Skew desacelera o estágio, não desliga o nó.")
            ],
            "explanation": "A tabela de sumário de métricas de tarefas na Spark UI (Min, 25th percentile, Median, 75th percentile, Max) permite identificar Skew imediatamente: quando a duração máxima ou o Shuffle Read Size do Max é ordens de grandeza maior que o 75th percentile."
        },
        # Q177
        {
            "scenario": "Qual comando SQL do Unity Catalog concede permissão para um engenheiro de DevOps gerenciar e disparar um Databricks Workflow de produção sem torná-lo proprietário nem administrador do workspace?",
            "options": [
                ("GRANT MANAGE RUN ON JOB <job_id> TO `engenheiro_devops`; (ou configuração de ACL 'Can Manage Run' no Job).", True, "Correto. A permissão 'Can Manage Run' permite ao usuário ou grupo disparar, pausar e cancelar execuções de um job específico sem acesso a alterar definições de código estruturais."),
                ("GRANT SUBSCRIPTION ADMIN ON CLOUD TO `engenheiro_devops`;", False, "Incorreto. Violação do princípio do menor privilégio."),
                ("DELETE JOB <job_id>;", False, "Incorreto. Excluiria o job."),
                ("ALTER WORKSPACE SET ROOT = `engenheiro_devops`;", False, "Incorreto. Sintaxe inexistente.")
            ],
            "explanation": "As permissões de Databricks Jobs seguem o modelo de controle de acesso granular: `Can View`, `Can Manage Run` (disparar e cancelar execuções) e `Can Manage` (editar e reconfigurar o job)."
        },
        # Q178
        {
            "scenario": "Ao desenvolver um pipeline de dados em Python, por que é uma péssima prática utilizar laços de repetição 'for row in df.collect():' para aplicar transformações de negócio em vez de usar expressões nativas de DataFrames PySpark?",
            "options": [
                ("for row in df.collect() força a coleta de todos os dados no nó Driver e executa em nó único em Python puro de forma serial, eliminando todo o paralelismo distribuído do Apache Spark e causando alto risco de OutOfMemory.", True, "Correto. Essa é uma das maiores falhas de arquitetura de engenharia: transformar um processamento distribuído em um loop sequencial lento no nó único do Driver."),
                ("O comando for row in df.collect() é proibido pela Microsoft e desconecta o Azure Databricks.", False, "Incorreto. Não é proibido por software, mas degrada brutalmente a performance."),
                ("O comando for row in df.collect() apaga os dados da tabela Delta.", False, "Incorreto. Não apaga dados, apenas executa de forma lenta e ineficiente."),
                ("Não há nenhuma diferença de velocidade em relação a DataFrames distribuídos.", False, "Incorreto. A diferença é de minutos ou horas vs milissegundos.")
            ],
            "explanation": "Transformações em Big Data devem ser expressas através de operações declarativas em DataFrames (`withColumn`, `when`, `expr`, `select`). Coletar dados com `collect()` e iterar em Python serial destrói o paralelismo e causa Driver OOM."
        },
        # Q179
        {
            "scenario": "Uma organização de seguros precisa treinar um modelo de Machine Learning e alimentar painéis de BI com os mesmos dados da camada Gold. Para garantir governança, eles criam uma tabela gerenciada no Unity Catalog. Qual privilégio deve ser concedido aos cientistas de dados para que possam ler essa tabela em seus notebooks?",
            "options": [
                ("GRANT SELECT ON TABLE prod.analytics.seguros_gold TO `cientistas_dados`; (garantindo também USE CATALOG e USE SCHEMA na hierarquia pai).", True, "Correto. O privilégio SELECT permite a leitura e consumo dos dados da tabela em notebooks, jobs e dashboards."),
                ("GRANT DROP TABLE TO `cientistas_dados`;", False, "Incorreto. Concederia permissão de exclusão acidental da tabela."),
                ("GRANT CREATE CATALOG TO `cientistas_dados`;", False, "Incorreto. Cientistas de dados não precisam de permissão administrativa de criação de catálogos para consultar tabelas."),
                ("GRANT ALL PRIVILEGES ON METASTORE TO ALL;", False, "Incorreto. Violação severa de segurança corporativa.")
            ],
            "explanation": "A leitura de securable objects no Unity Catalog exige `SELECT` no objeto folha, complementado por `USE CATALOG` no catálogo pai e `USE SCHEMA` no schema pai."
        },
        # Q180
        {
            "scenario": "Qual parâmetro de linha de comando no Databricks Asset Bundles permite implantar o projeto forçando o target 'dev' sem precisar alterar o default no databricks.yml?",
            "options": [
                ("databricks bundle deploy -t dev", True, "Correto. A flag -t ou --target especifica explicitamente o target de destino do bundle."),
                ("databricks bundle deploy --target-is-always-dev-no-matter-what", False, "Incorreto. Sintaxe inexistente."),
                ("databricks deploy /dev", False, "Incorreto. Sintaxe inválida."),
                ("az databricks deploy dev", False, "Incorreto. Sintaxe incorreta.")
            ],
            "explanation": "O seletor `-t` (abreviação de `--target`) direciona as ações do Databricks CLI para o target configurado no `databricks.yml` (ex: `databricks bundle deploy -t dev` ou `databricks bundle deploy -t prod`)."
        },
        # Q181
        {
            "scenario": "Ao investigar um incidente de segurança, o CISO precisa identificar se alguma credencial de usuário pessoal foi utilizada para modificar pipelines em produção nos últimos 60 dias. Qual consulta SQL provê essa informação na tabela de auditoria?",
            "options": [
                ("SELECT event_time, user_identity.email, action_name, request_params FROM system.access.audit WHERE service_name = 'jobs' AND user_identity.email NOT LIKE '%@serviceprincipal.azure%' AND event_date >= current_date() - INTERVAL 60 DAYS;", True, "Correto. A tabela system.access.audit permite isolar ações disparadas por identidades humanas em contraposição a Service Principals aprovados de CI/CD."),
                ("SELECT * FROM system.billing.usage WHERE usage_quantity > 0;", False, "Incorreto. system.billing.usage analisa cobrança de DBUs, não identidades de auditoria de alteração de jobs."),
                ("SELECT * FROM default.audit_table_local;", False, "Incorreto. Tabela inexistente no padrão de auditoria do sistema."),
                ("SHOW USERS ON PRODUCTION;", False, "Incorreto. Sintaxe inexistente.")
            ],
            "explanation": "A tabela `system.access.audit` registra todas as interações com o serviço de jobs (`service_name = 'jobs'`), possibilitando segregar acessos de desenvolvedores humanos versus Service Principals automatizados."
        },
        # Q182
        {
            "scenario": "Qual é o comportamento do Databricks Workflows quando a opção 'Continuous' (Execução Contínua) é habilitada em um Job em vez de um agendamento Cron?",
            "options": [
                ("O job é reiniciado imediatamente após a conclusão bem-sucedida da execução anterior (ou reiniciado após breve intervalo em caso de falha), mantendo o pipeline ativo continuamente em tempo real.", True, "Correto. O modo Continuous mantém o pipeline executando ininterruptamente, ideal para tarefas de streaming que não devem parar."),
                ("O job roda uma única vez no dia 1º de janeiro de cada ano.", False, "Incorreto. Isso seria agendamento anual estático."),
                ("O cluster é destruído e o workspace é encerrado.", False, "Incorreto. Resposta fictícia."),
                ("A execução é pausada para sempre.", False, "Incorreto. O modo continuous é estritamente ativo e ininterrupto.")
            ],
            "explanation": "O gatilho de execução `Continuous` em Databricks Workflows garante que o pipeline permaneça ativo 24/7: assim que uma execução termina ou sofre falha, o orquestrador sobe uma nova execução para manter a continuidade do streaming."
        },
        # Q183
        {
            "scenario": "Como a funcionalidade Lakehouse Monitoring do Unity Catalog auxilia equipes de engenharia de dados e MLOps a monitorar a saúde de tabelas produtivas ao longo do tempo?",
            "options": [
                ("Gera automaticamente perfis estatísticos, métricas de qualidade de dados, distribuições numéricas e relatórios de data drift (deriva de dados) sem necessidade de scripts manuais.", True, "Correto. O Lakehouse Monitoring cria monitores automatizados no Unity Catalog que rastreiam completude, deriva estatística de dados e anomalias em tabelas Delta ao longo do tempo."),
                ("Substitui os cientistas de dados por planilhas Excel estáticas.", False, "Incorreto. Resposta fictícia."),
                ("Envia uma carta física pelos Correios a cada anomalia detectada.", False, "Incorreto. Resposta fictícia."),
                ("Apaga automaticamente todas as linhas com valores maiores que 100.", False, "Incorreto. Lakehouse Monitoring gera métricas e alertas, não exclui dados arbitrariamente.")
            ],
            "explanation": "O Unity Catalog Lakehouse Monitoring analisa o histórico de tabelas e calcula métricas contínuas de integridade, volume, distribuições estatísticas e data drift, integrando diretamente com painéis do Databricks SQL."
        },
        # Q184
        {
            "scenario": "Um arquiteto de dados precisa desenhar a arquitetura de engenharia de dados corporativa no Azure Databricks para atender com excelência a todos os requisitos do exame oficial Microsoft DP-750. Quais são os QUATRO pilares fundamentais da solução oficial? (Selecione quatro opções)",
            "options": [
                ("Configurar ambiente seguro e escalável utilizando VNet Injection (/26), Azure Private Link, Cluster Policies de FinOps e Serverless Compute.", True, "Correto. Pilar 1: Configurar o Ambiente Azure Databricks (15-20%)."),
                ("Implementar governança unificada no Unity Catalog com 3-Level Namespace, Volumes, Row Filters, Column Masks e auditoria via System Tables.", True, "Correto. Pilar 2: Segurança e Governança com Unity Catalog (15-20%)."),
                ("Construir pipelines de dados na Arquitetura Medallion utilizando Auto Loader, Delta Lake ACID, Liquid Clustering e Deletion Vectors.", True, "Correto. Pilar 3: Preparar e Processar Dados em Batch e Streaming (30-35%)."),
                ("Orquestrar workloads de produção com Databricks Workflows multitarefas, Delta Live Tables (DLT com Expectations), DABs e esteiras automatizadas de CI/CD.", True, "Correto. Pilar 4: Implantar e Manter Pipelines e Workloads (30-35%)."),
                ("Desativar o Unity Catalog, voltar para montagens DBFS legadas com chaves hardcoded e usar clusters All-Purpose 24/7 sem autotermination.", False, "Incorreto. Esta alternativa representa todas as más práticas legadas terminantemente reprovadas pelo exame DP-750.")
            ],
            "type": "multiple",
            "explanation": "Estes quatro pilares correspondem aos quatro domínios oficiais da régua de certificação Microsoft Certified: Azure Databricks Data Engineer Associate (DP-750)."
        }
    ]
    return d4_specs

