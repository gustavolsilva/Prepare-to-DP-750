#!/usr/bin/env python3
"""
Databricks Formation — Prepare to DP-750
Domínio 3: Preparar e Processar Dados em Batch e Streaming (30–35%) — 54 Questões (77 a 130)
"""

def get_d3_questions():
    d3_specs = [
        # Q77
        {
            "scenario": "Uma plataforma de e-commerce deposita continuamente milhares de arquivos JSON com novos pedidos em um container no ADLS Gen2. A equipe de dados precisa ingerir esses arquivos incrementalmente em uma tabela Bronze sem reprocessar arquivos antigos e com suporte automático a novos campos que possam surgir no JSON. Qual tecnologia deve ser implementada?",
            "options": [
                ("Auto Loader (utilizando spark.readStream com formato 'cloudFiles' e cloudFiles.schemaLocation).", True, "Correto. O Auto Loader (cloudFiles) é o mecanismo padrão ouro do Azure Databricks para ingestão incremental e escalável de arquivos em nuvem com detecção automática de schema e evolução."),
                ("Comando SQL INSERT INTO executado manualmente em um notebook a cada hora.", False, "Incorreto. Manual, não escalável e não detecta novos arquivos automaticamente."),
                ("spark.read.json() em batch lendo o diretório inteiro e sobrescrevendo a tabela inteira a cada 5 minutos.", False, "Incorreto. Reprocessa todos os arquivos antigos continuamente, gerando custos absurdos e latência crescente."),
                ("Criar uma macro no Excel que lê os JSONs via Power Query local.", False, "Incorreto. Incompatível com pipelines corporativos de Big Data.")
            ],
            "explanation": "O Auto Loader (`cloudFiles`) processa arquivos de forma incremental e eficiente à medida que chegam ao armazenamento em nuvem, oferecendo detecção automática de arquivos e inferência e evolução contínua de schema."
        },
        # Q78
        {
            "scenario": "No Auto Loader do Azure Databricks, arquivos JSON chegam com uma coluna inesperada de desconto ('cupom_desconto') que não existia no schema original inferido. Como o Auto Loader lida com isso quando configurado com a opção padrão 'cloudFiles.schemaEvolutionMode' = 'addNewColumns'?",
            "options": [
                ("A nova coluna é adicionada automaticamente ao schema da tabela Delta de destino e o pipeline continua processando sem interrupção.", True, "Correto. O modo 'addNewColumns' detecta novos campos e estende automaticamente o schema da tabela Delta sem derrubar o stream de produção."),
                ("O pipeline falha imediatamente e descarta todos os arquivos do lote.", False, "Incorreto. Isso ocorre apenas no modo 'failOnNewColumns'."),
                ("Os valores da nova coluna são excluídos e ignorados silenciosamente.", False, "Incorreto. O Auto Loader preserva os novos dados estendendo o schema ou usando a coluna de resgate."),
                ("O cluster é reiniciado e o catálogo é apagado.", False, "Incorreto. Resposta fictícia.")
            ],
            "explanation": "No modo `addNewColumns`, o Auto Loader atualiza o schema de forma não destrutiva, adicionando novas colunas na tabela de destino e garantindo continuidade operacional sem falhas em produção."
        },
        # Q79
        {
            "scenario": "Durante a ingestão de telemetria com Auto Loader, alguns arquivos JSON contêm dados corrompidos (ex: uma string 'INVALID_DATE' em um campo esperado como DATE). Onde o Auto Loader armazena esses dados fora do padrão para que não quebrem a tipagem da tabela nem sejam perdidos para auditoria?",
            "options": [
                ("Na coluna especial oculta '_rescued_data', armazenada em formato JSON string.", True, "Correto. A coluna _rescued_data captura dados corrompidos, incompatíveis com o schema ou não tipados, permitindo que a ingestão continue sem perda de informação."),
                ("Em um arquivo temporário no desktop do engenheiro de dados.", False, "Incorreto. Resposta fictícia."),
                ("Na lixeira do Windows.", False, "Incorreto. Resposta fictícia."),
                ("No log do driver do Spark em formato de aviso de erro de compilação.", False, "Incorreto. Os dados são persistidos na própria tabela de dados para consulta posterior.")
            ],
            "explanation": "A coluna `_rescued_data` é o mecanismo de segurança do Auto Loader: qualquer dado que não corresponda ao schema esperado ou que esteja corrompido é salvo como texto JSON nessa coluna, evitando parada do pipeline e perda de registros."
        },
        # Q80
        {
            "scenario": "Um container no ADLS Gen2 já acumula mais de 25 milhões de arquivos Parquet em sua árvore de diretórios. Ao usar o Auto Loader no modo padrão de Directory Listing, o Driver do Spark consome muito tempo e memória apenas listando os novos arquivos. Qual modo do Auto Loader deve ser habilitado para contornar esse gargalo?",
            "options": [
                ("Modo de Notificação de Arquivos (File Notification Mode), configurando 'cloudFiles.useNotifications' = 'true'.", True, "Correto. O modo de notificação de arquivos utiliza Azure Event Grid e Azure Queue Storage para receber notificações de novos arquivos instantaneamente, sem varreduras dispendiosas no sistema de arquivos."),
                ("Modo de Força Bruta com 1.000 nós workers dedicados apenas a listar diretórios.", False, "Incorreto. Extremamente caro e ineficiente."),
                ("Mudar o formato de Parquet para CSV para acelerar a leitura.", False, "Incorreto. CSV é muito mais lento que Parquet."),
                ("Mover os 25 milhões de arquivos manualmente um a um via portal da Azure.", False, "Incorreto. Operacionalmente inviável.")
            ],
            "explanation": "Para diretórios que acumulam milhões de arquivos, o Auto Loader oferece o `File Notification Mode`. Ele provisiona automaticamente um Azure Event Grid e uma fila Azure Queue Storage para identificar novos arquivos sem precisar listar o diretório."
        },
        # Q81
        {
            "scenario": "Um pipeline de ingestão diária precisa carregar novos arquivos de vendas a cada noite. Em vez de manter um cluster ligado em streaming contínuo 24/7, a empresa quer rodar o Auto Loader como um job efêmero na madrugada, processando todos os arquivos acumulados e desligando em seguida. Qual trigger do writeStream atende perfeitamente a esse requisito?",
            "options": [
                (".trigger(availableNow=True)", True, "Correto. O trigger AvailableNow consome todos os dados pendentes em micro-lotes de tamanho ótimo e finaliza a execução do stream automaticamente, ideal para Job Clusters efêmeros."),
                (".trigger(continuous='1 second')", False, "Incorreto. Continuous streaming mantém o cluster rodando 24/7."),
                (".trigger(processingTime='10 minutes')", False, "Incorreto. Mantém o stream ativo indefinidamente a cada 10 minutos."),
                (".trigger(never=True)", False, "Incorreto. Sintaxe inexistente.")
            ],
            "explanation": "O trigger `availableNow=True` substituiu o legado `once=True`. Ele processa todos os novos dados disponíveis na fonte respeitando limites de rate limit em micro-batches e encerra o pipeline com sucesso, economizando DBUs em jobs agendados."
        },
        # Q82
        {
            "scenario": "Uma equipe de analistas SQL precisa carregar lotes de arquivos Parquet depositados semanalmente no ADLS Gen2 em uma tabela Delta. O volume é moderado (cerca de 500 arquivos por semana) e o schema é 100% estático. Eles preferem um comando SQL puro e idempotente sem precisar escrever scripts PySpark. Qual comando atende a este cenário?",
            "options": [
                ("COPY INTO prod.bronze.vendas FROM 'abfss://...' FILEFORMAT = PARQUET;", True, "Correto. O comando COPY INTO é uma instrução SQL idempotente nativa do Databricks, perfeita para cargas em lote regulares com schema estável."),
                ("LOAD DATA LOCAL INPATH em arquivos de texto.", False, "Incorreto. Comando legado do Hive com limitações de performance e localidade."),
                ("SELECT * INTO OUTFILE via MySQL.", False, "Incorreto. Comando de banco relacional tradicional fora do contexto Lakehouse."),
                ("BULK INSERT via T-SQL do SQL Server.", False, "Incorreto. Comando específico do SQL Server, não do Databricks.")
            ],
            "explanation": "O comando SQL `COPY INTO` permite carregar dados incrementalmente de forma idempotente (arquivos já carregados são ignorados automaticamente, a menos que `force=true` seja passado), sem exigir código PySpark."
        },
        # Q83
        {
            "scenario": "Em uma arquitetura Medallion corporativa no Azure Databricks, quais são as características e responsabilidades da camada Bronze?",
            "options": [
                ("Armazenar dados brutos ingeridos das fontes no estado mais próximo possível do original, em modo append-only, com metadados de ingestão (data e hora de carga) e histórico imutável.", True, "Correto. A camada Bronze representa a verdade histórica dos dados como chegaram da origem, sem transformações de negócio, permitindo reprocessamento a qualquer momento."),
                ("Armazenar agregações de relatórios de BI com joins complexos e métricas de faturamento.", False, "Incorreto. Essa é a responsabilidade da camada Gold."),
                ("Armazenar apenas dados descartados e inválidos que serão apagados em 24 horas.", False, "Incorreto. A camada Bronze preserva todos os dados ingeridos."),
                ("Armazenar arquivos em formato Microsoft Word .docx para leitura humana.", False, "Incorreto. A arquitetura Medallion utiliza Delta Lake e Parquet.")
            ],
            "explanation": "Na Arquitetura Medallion: Bronze = dados brutos com metadados de ingestão (Raw / Append-only); Silver = dados limpos, tipados, deduplicados e conformed; Gold = métricas agregadas e modelos dimensionais prontos para consumo de BI."
        },
        # Q84
        {
            "scenario": "Em uma arquitetura Medallion corporativa, quais são as características e transformações típicas executadas na camada Silver?",
            "options": [
                ("Limpeza de dados, validação de schema, tipagem estrita de colunas, deduplicação de registros e enriquecimento básico com tabelas de referência.", True, "Correto. A camada Silver atua como a 'camada de conformidade e integridade', limpando anomalias e provendo dados confiáveis para cientistas e analistas."),
                ("Ingestão bruta de arquivos JSON corrompidos sem nenhuma validação.", False, "Incorreto. Responsabilidade da camada Bronze."),
                ("Criação de dashboards visuais com gráficos de pizza para diretoria.", False, "Incorreto. Dashboards consomem dados da camada Gold."),
                ("Exportação de planilhas para disquetes físicos.", False, "Incorreto. Resposta fictícia.")
            ],
            "explanation": "A camada Silver filtra dados inválidos, desaninha estruturas complexas, deduplica eventos e aplica regras de qualidade para criar uma visão consistente e auditada da entidade de negócio."
        },
        # Q85
        {
            "scenario": "Em uma arquitetura Medallion, qual é o propósito principal da camada Gold?",
            "options": [
                ("Disponibilizar modelos de dados agregados, tabelas de fatos e dimensões (Star Schema) otimizadas para leitura rápida de BI, relatórios gerenciais e modelos de Machine Learning.", True, "Correto. A camada Gold contém os dados estruturados prontos para consumo de negócio, com KPIs pré-calculados e alta performance de consulta."),
                ("Armazenar arquivos de log brutos do Apache Spark para diagnóstico de bugs.", False, "Incorreto. Logs do Spark residem no storage de diagnóstico ou DBFS."),
                ("Guardar backups de senhas de usuários do Entra ID.", False, "Incorreto. Violação crítica de segurança."),
                ("Executar cópia fiel byte a byte de todas as tabelas do mainframe legado.", False, "Incorreto. Cópia fiel é o papel da camada Bronze.")
            ],
            "explanation": "A camada Gold atende aos casos de uso de negócio final: analistas de dados, painéis de Power BI e cientistas de dados encontram métricas consolidadas e dimensões padronizadas."
        },
        # Q86
        {
            "scenario": "Um engenheiro de dados recebe um DataFrame PySpark contendo uma coluna com uma string JSON aninhada chamada 'dados_cliente'. Qual função do PySpark deve ser utilizada para transformar essa string em uma estrutura colunar (StructType) no DataFrame?",
            "options": [
                ("from_json(col('dados_cliente'), schema_definido)", True, "Correto. A função from_json analisa a string JSON e a converte em um StructType de acordo com o schema schema_definido."),
                ("to_json(col('dados_cliente'))", False, "Incorreto. to_json faz o caminho inverso: converte uma coluna Struct ou Array em uma string JSON."),
                ("json_split(col('dados_cliente'))", False, "Incorreto. Função inexistente no PySpark."),
                ("cast('json')", False, "Incorreto. O Spark não possui casting genérico 'json'.")
            ],
            "explanation": "A função `from_json(coluna, schema)` do PySpark analisa o payload JSON textual e o transforma em colunas estruturadas nativas do Spark conforme o schema fornecido."
        },
        # Q87
        {
            "scenario": "Uma coluna de pedidos chamada 'itens' contém um Array com múltiplos produtos comprados em um único pedido. O engenheiro precisa transformar esse array para que cada item vire uma linha independente no DataFrame, mantendo o ID do pedido original. Qual função PySpark deve ser usada?",
            "options": [
                ("explode(col('itens'))", True, "Correto. A função explode cria uma nova linha para cada elemento presente no array da coluna especificada."),
                ("flatten(col('itens'))", False, "Incorreto. flatten achata arrays de arrays em um único array, mas não desdobra em novas linhas."),
                ("split(col('itens'))", False, "Incorreto. split divide uma string em array de strings com base em um delimitador."),
                ("group_by(col('itens'))", False, "Incorreto. Agrupamento consolida linhas, não expande arrays em linhas.")
            ],
            "explanation": "A função `explode()` desaninha coleções (arrays ou maps), gerando uma nova linha no DataFrame para cada item da coleção e duplicando as demais colunas da linha original."
        },
        # Q88
        {
            "scenario": "Para deduplicar uma tabela Silver de clientes mantendo apenas o registro mais recente de cada cliente com base na coluna 'data_atualizacao', qual combinação de Window Function é recomendada no PySpark?",
            "options": [
                ("Window.partitionBy('id_cliente').orderBy(col('data_atualizacao').desc()) e filtrar onde row_number() == 1.", True, "Correto. Particionar pelo ID e ordenar de forma decrescente pela data permite numerar as linhas e reter exclusivamente a linha mais recente (row_number 1)."),
                ("Window.orderBy('id_cliente') e somar o total de vendas.", False, "Incorreto. Não deduplica nem utiliza partição por cliente."),
                ("distinct() em todas as colunas sem critérios de janela.", False, "Incorreto. distinct só remove linhas 100% idênticas; se a data mudou, o distinct não descarta o registro antigo."),
                ("dropDuplicates(['id_cliente']) sem ordenação prévia.", False, "Incorreto. dropDuplicates sem ordenação de janela pode reter um registro desatualizado arbitrariamente.")
            ],
            "explanation": "O padrão ouro de engenharia no DP-750 para deduplicação com controle temporal é particionar por entidade (`partitionBy('id_cliente')`), ordenar decrescente por timestamp (`orderBy(desc)`) e filtrar `row_number() == 1`."
        },
        # Q89
        {
            "scenario": "Qual função de janela do Spark SQL permite consultar o valor da coluna 'status_pedido' da linha ANTERIOR de um mesmo cliente ordenada cronologicamente, essencial para calcular transições de estado?",
            "options": [
                ("lag('status_pedido', 1).over(window_spec)", True, "Correto. A função lag() retorna o valor de uma coluna a uma distância fixa antes da linha atual na janela de ordenação."),
                ("lead('status_pedido', 1).over(window_spec)", False, "Incorreto. lead() retorna o valor da linha posterior (seguinte), não da anterior."),
                ("first_value().over(window_spec)", False, "Incorreto. Retorna o primeiro valor absoluto da partição inteira."),
                ("prior_record()", False, "Incorreto. Função inexistente no Spark SQL.")
            ],
            "explanation": "A função `lag(col, offset)` acessa valores de linhas anteriores dentro da partição da janela, amplamente utilizada em análise de séries temporais e mudanças de estado."
        },
        # Q90
        {
            "scenario": "Em um cenário de Slowly Changing Dimension Tipo 1 (SCD1), como o comando Delta Lake MERGE INTO deve atualizar a tabela dimensional quando um cliente existente alterar seu endereço?",
            "options": [
                ("Sobrescrever diretamente o endereço antigo do cliente na linha existente (in-place update), mantendo a mesma chave primária sem criar uma nova linha.", True, "Correto. SCD Tipo 1 reflete apenas o estado atual (sobrescrita), sem manter histórico de versões anteriores."),
                ("Inserir uma nova linha marcando a linha antiga com is_current = false e data de término.", False, "Incorreto. Este é o comportamento de SCD Tipo 2, não SCD Tipo 1."),
                ("Excluir o cliente e apagar todo o histórico de compras passadas dele.", False, "Incorreto. Viola a integridade referencial."),
                ("Criar uma nova tabela no banco de dados chamada clientes_novo_endereco.", False, "Incorreto. Não é uma boa prática de modelagem de dados.")
            ],
            "explanation": "SCD Tipo 1 realiza sobrescrita em linha (`WHEN MATCHED THEN UPDATE SET target.col = source.col`), preservando apenas o valor mais recente e sem reter histórico retroativo."
        },
        # Q91
        {
            "scenario": "Em um cenário de Slowly Changing Dimension Tipo 2 (SCD2), qual é o objetivo arquitetural de manter as colunas 'start_date', 'end_date' e 'is_current' na tabela dimensional?",
            "options": [
                ("Preservar o histórico completo de alterações da entidade ao longo do tempo, permitindo consultar como eram os dados em qualquer data passada e identificando qual versão está ativa no momento.", True, "Correto. SCD Tipo 2 mantém histórico completo com vigência temporal, essencial para auditoria regulatória e relatórios históricos precisos."),
                ("Acelerar a compactação de arquivos Parquet durante o comando VACUUM.", False, "Incorreto. VACUUM limpa arquivos órfãos, não tem relação com modelagem dimensional."),
                ("Permitir que o Power BI desabilite o DirectQuery e use apenas CSV.", False, "Incorreto. Não se relaciona com SCD2."),
                ("Garantir que a tabela não consuma memória RAM no nó Driver.", False, "Incorreto. Não tem relação com consumo de memória de hardware.")
            ],
            "explanation": "SCD Tipo 2 mantém histórico de alterações criando novas linhas para cada mutação com controle de intervalo de tempo (`start_date`, `end_date`) e flag indicadora de versão atual (`is_current = true`)."
        },
        # Q92
        {
            "scenario": "Para otimizar o desempenho de uma instrução MERGE INTO no Delta Lake em tabelas com dezenas de terabytes, qual cláusula no predicado ON é crucial para permitir que o motor de consulta aplique Partition Pruning e evite varreduras de tabela inteira?",
            "options": [
                ("Incluir a coluna de partição ou clusterização (ex: target.data_evento = source.data_evento AND target.id = source.id) no predicado ON.", True, "Correto. Ao incluir a chave de partição/clusterização na condição ON do MERGE, o Delta Lake limita a leitura apenas aos arquivos afetados, evitando full table scans caros."),
                ("Remover a cláusula ON e utilizar um CROSS JOIN irrestrito.", False, "Incorreto. Geraria um produto cartesiano gigantesco e esgotaria a memória."),
                ("Executar o MERGE com a opção 'WHEN NOT MATCHED DO NOTHING'.", False, "Incorreto. Não resolve a poda de arquivos na leitura."),
                ("Utilizar uma tabela sem chave primária nem colunas indexadas.", False, "Incorreto. Piora ainda mais o tempo de execução.")
            ],
            "explanation": "Ao adicionar predicados baseados nas colunas de partição ou Liquid Clustering na cláusula `ON` do MERGE, o Catalyst Optimizer consegue realizar partição/file pruning, escaneando apenas as frações da tabela que realmente sofrerão mutação."
        },
        # Q93
        {
            "scenario": "No Spark Structured Streaming, por que é estritamente obrigatório configurar a opção 'checkpointLocation' apontando para um caminho persistente no ADLS Gen2?",
            "options": [
                ("O checkpoint armazena o log de offsets de leitura e o estado da consulta, garantindo tolerância a falhas e semântica de processamento exatamente uma vez (exactly-once) em caso de reinicialização.", True, "Correto. O diretório de checkpoint é indispensável para que o stream saiba de onde parou após falhas ou desligamentos sem duplicar nem perder registros."),
                ("O checkpoint armazena o código fonte em Python para que outros analistas possam ler o notebook.", False, "Incorreto. O código fica no Git ou Workspace, não no checkpoint do stream."),
                ("Sem o checkpoint, o Spark apaga os dados da tabela de origem.", False, "Incorreto. A fonte não é apagada, mas a recuperação contra falhas seria impossível."),
                ("O checkpoint serve apenas para registrar o número de telefone do administrador do cluster.", False, "Incorreto. Resposta fictícia.")
            ],
            "explanation": "O `checkpointLocation` grava o log transacional e os arquivos de estado do Structured Streaming em armazenamento persistente, viabilizando recuperação determinística e garantias de idempotência/exactly-once."
        },
        # Q94
        {
            "scenario": "Qual é a diferença entre os modos de saída 'append', 'update' e 'complete' em consultas do Spark Structured Streaming?",
            "options": [
                ("'append' grava apenas as novas linhas inseridas; 'update' grava apenas as linhas que foram modificadas ou adicionadas desde o último batch; 'complete' reescreve a tabela inteira com todos os resultados agregados a cada batch.", True, "Correto. Essa é a definição exata dos três OutputModes suportados pelo Structured Streaming."),
                ("'append' apaga a tabela inteira a cada 10 segundos.", False, "Incorreto. Append apenas anexa novas linhas."),
                ("'complete' só pode ser usado se a tabela tiver menos de 10 linhas.", False, "Incorreto. Complete é projetado para agregações com estado."),
                ("'update' só é permitido para arquivos de texto sem cabeçalho.", False, "Incorreto. Não há restrição de cabeçalho.")
            ],
            "explanation": "No Structured Streaming: `append` é o padrão para fluxos incrementais sem agregações; `update` emite apenas linhas atualizadas de agregações; `complete` regrava a tabela inteira de agregação a cada micro-lote."
        },
        # Q95
        {
            "scenario": "Um pipeline de streaming agrega métricas de consumo de dados por dispositivo móvel a cada 5 minutos. O cluster começou a sofrer com vazamento de memória e erros frequentes de OutOfMemory (OOM) no State Store da JVM após alguns dias. Qual mecanismo deve ser aplicado para descartar dados tardios e liberar a memória do State Store?",
            "options": [
                ("Aplicar Watermarking na coluna de timestamp do evento utilizando withWatermark('timestamp_evento', '15 minutes').", True, "Correto. O Watermarking define o limiar de atraso máximo aceitável para dados em streaming, permitindo que o Spark descarte estados antigos da memória e previna OutOfMemory no State Store."),
                ("Aumentar o número de nós do cluster para 100 máquinas virtuais a cada hora.", False, "Incorreto. Apenas postergaria o OOM e aumentaria custos astronomicamente sem resolver a causa raiz."),
                ("Desabilitar o checkpoint e salvar os dados na memória volátil do Driver.", False, "Incorreto. Viola a tolerância a falhas e pioraria a memória do Driver."),
                ("Parar o streaming e reiniciar o cluster manualmente a cada 30 minutos.", False, "Incorreto. Incompatível com SLAs de tempo real de produção.")
            ],
            "explanation": "Sem `watermarking`, o Spark mantém o estado de agregação aberto indefinidamente aguardando eventos atrasados, esgotando a memória RAM dos executores (State Store). O `withWatermark()` estabelece o corte temporal para limpar o estado antigo."
        },
        # Q96
        {
            "scenario": "Como o Liquid Clustering (CLUSTER BY) soluciona o problema crônico de 'small files' que ocorria no particionamento tradicional Hive quando engenheiros particionavam tabelas por colunas de alta cardinalidade (ex: id_cliente)?",
            "options": [
                ("O Liquid Clustering não cria subdiretórios físicos por valor de chave; ele organiza os dados dentro de arquivos Parquet de tamanho ótimo (~1 GB) utilizando curvas multidimensionais de preenchimento de espaço.", True, "Correto. Ao contrário do particionamento tradicional que cria uma pasta para cada valor distinto, o Liquid Clustering agrupa registros mantendo arquivos consolidados de tamanho ideal sem fragmentação."),
                ("O Liquid Clustering compacta todos os dados em um único arquivo de 50 Terabytes.", False, "Incorreto. Um arquivo de 50 TB eliminaria o paralelismo distribuído do Spark."),
                ("O Liquid Clustering converte automaticamente todas as colunas de alta cardinalidade em números binários de 1 bit.", False, "Incorreto. Resposta fictícia."),
                ("O Liquid Clustering exige que o desenvolvedor crie os diretórios manualmente via FTP.", False, "Incorreto. O processo é 100% gerenciado pelo motor do Delta Lake.")
            ],
            "explanation": "O Liquid Clustering substitui a estrutura hierárquica rígida de diretórios do Hive por organização física baseada em Z-order/Hilbert curves em arquivos Parquet de tamanho uniforme, eliminando a criação de milhares de pastas e arquivos minúsculos."
        },
        # Q97
        {
            "scenario": "Uma tabela de logística foi criada com: CREATE TABLE fretes (...) CLUSTER BY (codigo_pais, id_transportadora);. Três meses depois, o padrão de consultas mudou e os analistas passam a filtrar quase que exclusivamente por 'data_envio'. Qual é a vantagem do Liquid Clustering nesse cenário em relação ao particionamento Hive?",
            "options": [
                ("É possível alterar as chaves de clusterização para 'CLUSTER BY (data_envio)' via simples comando ALTER TABLE sem precisar reescrever a tabela inteira do zero.", True, "Correto. O Liquid Clustering é dinâmico e suporta evolução de chaves com ALTER TABLE. As novas gravações e os comandos OPTIMIZE incrementais aplicam o novo layout progressivamente."),
                ("A tabela é excluída e o banco de dados é recriado em MySQL.", False, "Incorreto. Resposta fictícia."),
                ("O particionamento Hive era melhor pois exigia recriar a tabela em 48 horas de downtime.", False, "Incorreto. Recriar tabelas com downtime é uma desvantagem severa do Hive legado."),
                ("O Liquid Clustering não permite nenhuma alteração de chaves após a criação.", False, "Incorreto. A flexibilidade de alteração de chaves é exatamente um dos seus maiores diferenciais.")
            ],
            "explanation": "No particionamento clássico Hive, alterar a coluna de partição exigia recriar a tabela e mover todos os dados. No Liquid Clustering, basta rodar `ALTER TABLE tbl CLUSTER BY (novas_colunas);` e o layout evolui incrementalmente."
        },
        # Q98
        {
            "scenario": "O que são Deletion Vectors no Delta Lake e como eles revolucionam a performance de comandos DELETE, UPDATE e MERGE INTO?",
            "options": [
                ("São arquivos leves de bitmaps que sinalizam linhas excluídas ou modificadas sem a necessidade de reescrever o arquivo Parquet de 100 MB inteiro no storage.", True, "Correto. Deletion Vectors introduzem exclusão lógica via bitmaps de bits (Roaring Bitmaps), evitando operações pesadas de Copy-on-Write a cada mutação de poucas linhas."),
                ("São vírus de computador criados para apagar dados de concorrentes.", False, "Incorreto. Resposta fictícia."),
                ("São regras de rede no firewall para bloquear tráfego de saída.", False, "Incorreto. Deletion Vectors são um recurso de armazenamento do Delta Lake."),
                ("São tabelas temporárias que existem apenas no Microsoft Excel.", False, "Incorreto. Recurso oficial nativo do protocolo Delta Lake.")
            ],
            "explanation": "Antes dos Deletion Vectors, modificar 1 linha em um arquivo Parquet de 100 MB forçava a reescrita dos 100 MB inteiros. Com Deletion Vectors, grava-se um bitmap levíssimo apontando a linha alterada, acelerando mutações em até 10x."
        },
        # Q99
        {
            "scenario": "Qual comando habilita explicitamente Deletion Vectors em uma tabela Delta existente no Azure Databricks?",
            "options": [
                ("ALTER TABLE prod.vendas.pedidos SET TBLPROPERTIES ('delta.enableDeletionVectors' = true);", True, "Correto. Essa é a propriedade oficial de tabela para ativar Deletion Vectors no Delta Lake."),
                ("ENABLE DELETION VECTORS ON prod.vendas.pedidos;", False, "Incorreto. Sintaxe inexistente."),
                ("OPTIMIZE TABLE prod.vendas.pedidos WITH BITMAP;", False, "Incorreto. Sintaxe inválida."),
                ("SET spark.databricks.deletionVectors = 'yes';", False, "Incorreto. Deve ser configurado como propriedade da tabela (TBLPROPERTIES).")
            ],
            "explanation": "A ativação de Deletion Vectors em tabelas existentes é realizada via `ALTER TABLE <nome> SET TBLPROPERTIES ('delta.enableDeletionVectors' = true);`."
        },
        # Q100
        {
            "scenario": "Um analista de fraudes precisa consultar o estado exato de uma tabela Delta há 5 dias atrás para reproduzir o saldo bancário de uma conta antes de uma transação contestada. Qual funcionalidade do Delta Lake viabiliza essa consulta?",
            "options": [
                ("Delta Lake Time Travel (utilizando SELECT * FROM tbl TIMESTAMP AS OF '2025-01-10' ou VERSION AS OF n).", True, "Correto. O Time Travel permite consultar versões históricas anteriores da tabela graças ao log imutável de transações (_delta_log)."),
                ("Restauração de fita backup de fita magnética off-line.", False, "Incorreto. Incompatível com o modelo Lakehouse."),
                ("Executar o comando VACUUM com retenção zero.", False, "Incorreto. VACUUM com zero destruiria a capacidade de Time Travel."),
                ("Acessar o histórico de navegação do Google Chrome do analista.", False, "Incorreto. Não tem relação com o banco de dados.")
            ],
            "explanation": "O Delta Lake mantém um histórico transacional completo de commits. O Time Travel permite consultar versões prévias com `TIMESTAMP AS OF` ou `VERSION AS OF`, além de reverter estados com `RESTORE TABLE`."
        },
        # Q101
        {
            "scenario": "Um engenheiro de dados júnior executa o comando: VACUUM prod.vendas.clientes RETAIN 0 HOURS;. Por padrão, o comando falha imediatamente com uma exceção de segurança. Qual é a razão dessa trava de segurança nativa do Databricks?",
            "options": [
                ("O Databricks impede por padrão retenções menores que 7 dias (168 horas) para evitar a corrupção de leituras concorrentes em andamento e a destruição irreversível do Time Travel.", True, "Correto. A trava de retenção padrão impede que transações ativas e históricos recentes de Time Travel sejam destruídos acidentalmente por exclusões prematuras de arquivos."),
                ("O comando VACUUM só pode ser executado às sextas-feiras após as 18 horas.", False, "Incorreto. VACUUM pode rodar a qualquer momento."),
                ("O comando falha porque o VACUUM foi descontinuado e substituído pelo Excel.", False, "Incorreto. VACUUM é um comando essencial de manutenção física do Delta Lake."),
                ("A palavra RETAIN só aceita valores em minutos, não em horas.", False, "Incorreto. RETAIN aceita horas (HOURS).")
            ],
            "explanation": "O parâmetro `spark.databricks.delta.retentionDurationCheck.enabled` (padrão true) bloqueia comandos VACUUM com períodos inferiores a 168 horas (7 dias) para garantir que consultas ativas e Time Travel não sejam comprometidos."
        },
        # Q102
        {
            "scenario": "Qual comando oficial do Delta Lake compacta múltiplos arquivos Parquet pequenos (small files) em arquivos consolidados de tamanho ideal (~1 GB) para acelerar a velocidade de leitura das consultas?",
            "options": [
                ("OPTIMIZE prod.vendas.pedidos;", True, "Correto. O comando OPTIMIZE realiza bin-packing, consolidando pequenos arquivos Parquet em arquivos grandes e otimizados de aproximadamente 1 GB."),
                ("COMPACT TABLE prod.vendas.pedidos;", False, "Incorreto. Sintaxe inexistente no Delta Lake."),
                ("ZIP FILES ON prod.vendas.pedidos;", False, "Incorreto. Não se utiliza ZIP para compactação colunar."),
                ("MERGE SMALL FILES TO ONE;", False, "Incorreto. Sintaxe inexistente.")
            ],
            "explanation": "O comando `OPTIMIZE` é a instrução oficial de manutenção física para bin-packing de pequenos arquivos gerados por commits frequentes e streams em tabelas Delta."
        },
        # Q103
        {
            "scenario": "Uma organização precisa capturar todas as alterações de linhas (inserts, updates com valores pré e pós-imagem, e deletes) ocorridas em uma tabela Delta para alimentar um sistema de auditoria externo. Qual recurso nativo do Delta Lake deve ser habilitado na tabela?",
            "options": [
                ("Change Data Feed (CDF), ativando 'delta.enableChangeDataFeed' = true nas propriedades da tabela.", True, "Correto. O Change Data Feed registra as mutações linha a linha em arquivos de log adicionais, permitindo consumir as alterações (pré e pós-imagem) de forma incremental."),
                ("Tirar um print diário da tela do computador e comparar visualmente.", False, "Incorreto. Resposta fictícia."),
                ("Desabilitar transações ACID no cluster.", False, "Incorreto. Impossível no Delta Lake e corromperia os dados."),
                ("Configurar um trigger em JavaScript no navegador.", False, "Incorreto. Não captura alterações no storage de dados.")
            ],
            "explanation": "O Change Data Feed (CDF) do Delta Lake registra alterações incrementais em tabelas (inserts, updates e deletes) com metadados especiais (`_change_type`), permitindo arquiteturas de CDC eficientes."
        },
        # Q104
        {
            "scenario": "Como uma aplicação consome as alterações registradas pelo Change Data Feed (CDF) de uma tabela Delta entre a versão 10 e a versão 15?",
            "options": [
                ("SELECT * FROM table_changes('prod.vendas.pedidos', 10, 15);", True, "Correto. A função table_changes(tabela, start_version, end_version) é a função SQL nativa para ler o feed de alterações do CDF."),
                ("SELECT * FROM prod.vendas.pedidos WHERE cdf_version BETWEEN 10 AND 15;", False, "Incorreto. cdf_version não é uma coluna nativa da tabela principal."),
                ("READ CHANGES FROM prod.vendas.pedidos;", False, "Incorreto. Sintaxe inexistente."),
                ("FETCH LOGS FROM DELTA 10 TO 15;", False, "Incorreto. Sintaxe inválida.")
            ],
            "explanation": "A função `table_changes('nome_da_tabela', start_version, [end_version])` retorna o conjunto de registros alterados acompanhados de colunas como `_change_type`, `_commit_version` e `_commit_timestamp`."
        },
        # Q105
        {
            "scenario": "Um desenvolvedor tenta gravar um DataFrame PySpark com 5 colunas em uma tabela Delta existente que possui apenas 4 colunas. O comando falha com erro de Schema Mismatch. Qual opção deve ser passada na escrita para que o schema da tabela seja atualizado automaticamente para acomodar a quinta coluna?",
            "options": [
                (".option('mergeSchema', 'true')", True, "Correto. A opção mergeSchema ativa a evolução de schema na escrita, adicionando novas colunas detectadas no DataFrame à tabela Delta de destino."),
                (".option('forceOverwrite', 'true')", False, "Incorreto. Não é uma opção padrão do PySpark e sobrescreveria dados em vez de evoluir schema."),
                (".option('ignoreSchema', 'true')", False, "Incorreto. Não existe no conector Delta."),
                (".option('disableACID', 'true')", False, "Incorreto. Transações ACID não podem ser desativadas.")
            ],
            "explanation": "O Delta Lake possui Schema Enforcement por padrão para prevenir corrupção acidental de dados. Para autorizar novos campos, o desenvolvedor deve passar explicitamente `.option('mergeSchema', 'true')`."
        },
        # Q106
        {
            "scenario": "Em uma consulta Spark SQL que realiza um JOIN entre uma tabela de Fatos gigante de 50 Terabytes e uma tabela Dimensional de lojas pequena de apenas 15 Megabytes, o plano físico realiza um Shuffle Hash Join lento pela rede. Como acelerar essa consulta eliminando o shuffle de rede?",
            "options": [
                ("Aplicar um Broadcast Join hint na tabela pequena: /*+ BROADCAST(lojas) */ ou broadcast(df_lojas).", True, "Correto. O Broadcast Join envia uma cópia da tabela pequena para a memória de cada nó executor, eliminando completamente a troca massiva de dados (shuffle) da tabela gigante pela rede."),
                ("Aumentar o tamanho da tabela pequena para 100 Terabytes duplicando dados.", False, "Incorreto. Pioraria drasticamente o desempenho."),
                ("Converter o join em um Cartesian Product irrestrito.", False, "Incorreto. Produto cartesiano é a operação mais lenta e pesada possível."),
                ("Executar a consulta em um computador sem conexão com a internet.", False, "Incorreto. Resposta fictícia.")
            ],
            "explanation": "O Broadcast Join é uma das técnicas mais eficazes de performance: quando uma das tabelas cabe confortavelmente na memória dos executores (< 10 MB por padrão, configurável até algumas centenas de MB), ela é transmitida a todos os nós, evitando o shuffle da tabela maior."
        },
        # Q107
        {
            "scenario": "Ao analisar a Spark UI de um job que faz join entre duas tabelas grandes, o engenheiro observa que 199 tasks concluíram em 3 segundos, mas uma única task ficou travada executando por 45 minutos. Qual problema de dados está ocorrendo e como corrigi-lo?",
            "options": [
                ("Data Skew (Desbalanceamento de Chave); aplicar a dica de Skew Join /*+ SKEW('tabela', 'coluna') */ ou técnica de Salting na chave do join.", True, "Correto. O sintoma clássico de uma task demorando muito mais que as outras é o Data Skew (ex: muitos registros nulos ou valores repetidos na chave). O Skew Join hint divide a partição problemática em sub-partições menores balanceadas."),
                ("O computador do desenvolvedor travou com falta de bateria.", False, "Incorreto. O processamento ocorre nos nós da nuvem."),
                ("A tabela Delta foi excluída acidentalmente.", False, "Incorreto. Se fosse excluída, a query falharia imediatamente."),
                ("O Apache Spark não suporta mais de 100 tarefas simultâneas.", False, "Incorreto. O Spark suporta milhares de tasks paralelas.")
            ],
            "explanation": "Data Skew ocorre quando uma chave de junção possui frequência desproporcionalmente alta (ex: `chave IS NULL` ou `codigo_pais = 'BR'`). O hint `/*+ SKEW('tabela', 'coluna') */` instrui o Catalyst a quebrar a partição enviesada em fatias menores balanceadas."
        },
        # Q108
        {
            "scenario": "O recurso Adaptive Query Execution (AQE) está habilitado por padrão no Azure Databricks Runtime. Qual benefício o AQE traz dinamicamente durante a execução dos estágios de Shuffle?",
            "options": [
                ("Coalesce dinâmico de partições de shuffle pós-estágio, convertendo automaticamente centenas de pequenas partições vazias em um número ótimo de partições consolidadas.", True, "Correto. O AQE avalia estatísticas do shuffle em tempo de execução e junta partições pequenas (Dynamically Coalescing Shuffle Partitions), evitando sobrecarga de agendamento de tasks."),
                ("Desliga os nós workers a cada 10 segundos para economizar energia.", False, "Incorreto. Não desliga nós durante a query."),
                ("Apaga todas as tabelas temporárias criadas pelo usuário.", False, "Incorreto. Tabelas temporárias duram enquanto a sessão persistir."),
                ("Substitui o código PySpark por comandos em C++ manualmente.", False, "Incorreto. O Photon faz compilação interna, não substituição manual de código de usuário.")
            ],
            "explanation": "Adaptive Query Execution (AQE) re-otimiza planos de consulta com base em estatísticas reais obtidas durante a execução de estágios intermediários, combinando partições pequenas e convertendo sort-merge joins em broadcast joins dinamicamente."
        },
        # Q109
        {
            "scenario": "Qual comando SQL restaura a tabela 'prod.vendas.pedidos' para o estado exato em que ela se encontrava na versão 12 do log de transações Delta?",
            "options": [
                ("RESTORE TABLE prod.vendas.pedidos TO VERSION AS OF 12;", True, "Correto. O comando RESTORE TABLE desfaz alterações posteriores e reverte a tabela para a versão indicada no histórico do Delta Lake."),
                ("ROLLBACK TRANSACTION TO 12;", False, "Incorreto. Sintaxe de banco relacional tradicional, não Delta Lake."),
                ("RECOVER TABLE prod.vendas.pedidos VERSION 12;", False, "Incorreto. Sintaxe inexistente no Databricks."),
                ("UNDO MERGE IN TABLE prod.vendas.pedidos;", False, "Incorreto. Sintaxe inexistente.")
            ],
            "explanation": "O comando `RESTORE TABLE <nome> TO VERSION AS OF <n>;` reverte o estado dos dados da tabela para a versão histórica especificada, gravando um novo commit de restauração no Delta Log."
        },
        # Q110
        {
            "scenario": "Em uma tabela de 50 TB no Delta Lake particionada tradicionalmente por 'ano', 'mes' e 'dia', os analistas relatam lentidão crítica em consultas que filtram por 'categoria_produto' e 'id_cliente'. Por que o particionamento Hive não resolve essas consultas e por que o Liquid Clustering é a solução ideal?",
            "options": [
                ("O particionamento Hive só acelera filtros nas colunas de partição de diretório (ano/mes/dia); o Liquid Clustering permite clusterizar por até 4 colunas multidimensionais (ex: categoria_produto, id_cliente) e aplica poda de arquivos eficiente em todas elas simultaneamente.", True, "Correto. O particionamento Hive é unidimensional e hierárquico. O Liquid Clustering organiza dados em espaço multidimensional, permitindo acelerar queries que filtram por combinações arbitrárias das colunas clusterizadas."),
                ("O particionamento Hive só aceita dados em formato PDF.", False, "Incorreto. O Hive particiona Parquet, ORC, etc."),
                ("O Liquid Clustering exige que todos os dados sejam apagados semanalmente.", False, "Incorreto. Dados são mantidos de forma persistente e segura."),
                ("O particionamento Hive foi proibido pela legislação internacional.", False, "Incorreto. Resposta fictícia.")
            ],
            "explanation": "O particionamento tradicional por data só ajuda queries que filtram por data. O Liquid Clustering (`CLUSTER BY (categoria, cliente, data)`) organiza os blocos de dados considerando todas as chaves ao mesmo tempo, provendo excelente poda de leitura para múltiplos padrões de consulta."
        },
        # Q111
        {
            "scenario": "O que acontece nos bastidores quando uma transação no Delta Lake grava dados com sucesso na tabela?",
            "options": [
                ("Arquivos de dados Parquet são gravados no storage e um arquivo atômico de commit em JSON (ex: 00000000000000000010.json) é gravado no diretório _delta_log/ registrando a adição dos arquivos.", True, "Correto. O protocolo Delta Lake garante atomicidade gravando os dados em Parquet e confirmando a transação via um arquivo de log JSON monotonicamente crescente no _delta_log/."),
                ("O cluster envia um e-mail para a Microsoft confirmando que a tabela foi gravada.", False, "Incorreto. Não há envio de e-mails em commits de dados."),
                ("O Delta Lake converte os arquivos Parquet em planilhas CSV para compatibilidade.", False, "Incorreto. O Delta Lake utiliza exclusivamente Parquet para persistência colunar."),
                ("O nó Driver apaga o metastore do Unity Catalog.", False, "Incorreto. Metadados são preservados.")
            ],
            "explanation": "Toda transação no Delta Lake é confirmada por um arquivo JSON atômico na pasta `_delta_log/`. Esse log registra quais arquivos Parquet foram adicionados (`add`) e quais foram removidos (`remove`), garantindo as propriedades ACID."
        },
        # Q112
        {
            "scenario": "A cada 10 commits no log transacional (_delta_log/), o Delta Lake executa uma ação automática de consolidação do estado. O que é gerado nessa consolidação?",
            "options": [
                ("Um arquivo Parquet de Checkpoint (ex: 00000000000000000010.checkpoint.parquet) compactando o estado consolidado de todos os commits anteriores.", True, "Correto. Os arquivos de checkpoint em Parquet evitam que o Spark precise ler centenas de arquivos JSON para reconstruir o estado atual da tabela, acelerando drasticamente o tempo de leitura."),
                ("Uma cópia física de todos os dados do banco de dados para a lixeira.", False, "Incorreto. Não descarta dados."),
                ("A exclusão de todas as versões de Time Travel anteriores.", False, "Incorreto. O Time Travel depende do log e checkpoints, e a limpeza só ocorre via VACUUM explícito."),
                ("A reinicialização forçada do cluster Databricks.", False, "Incorreto. Checkpoints são criados de forma transparente durante a escrita.")
            ],
            "explanation": "A cada 10 transações, o Delta Lake grava um checkpoint em formato Parquet contendo o estado resumido de todos os arquivos ativos, evitando que leitores precisem reprocessar milhares de arquivos JSON individuais."
        },
        # Q113
        {
            "scenario": "Um desenvolvedor precisa verificar o histórico completo de commits, autores, comandos e versões de uma tabela Delta. Qual comando SQL provê essa auditoria transacional?",
            "options": [
                ("DESCRIBE HISTORY prod.vendas.pedidos;", True, "Correto. A instrução DESCRIBE HISTORY lista todas as operações executadas na tabela Delta (versão, timestamp, userId, operation, operationParameters e notebook)."),
                ("SHOW COMMITS IN prod.vendas.pedidos;", False, "Incorreto. Sintaxe inexistente."),
                ("SELECT * FROM delta.log_history;", False, "Incorreto. Sintaxe inválida no Databricks."),
                ("LIST VERSIONS OF TABLE prod.vendas.pedidos;", False, "Incorreto. Sintaxe inexistente.")
            ],
            "explanation": "O comando `DESCRIBE HISTORY <nome_tabela>;` expõe a trilha completa de auditoria do Delta Log, revelando quem executou cada operação (ex: WRITE, MERGE, OPTIMIZE, VACUUM) e em qual timestamp."
        },
        # Q114
        {
            "scenario": "Uma tabela de streaming recebe milhões de eventos por hora. O engenheiro observa que o diretório de dados possui mais de 80.000 arquivos Parquet pequenos de 2 MB cada, degradando o tempo de resposta de queries analíticas. Qual par de comandos deve ser executado periodicamente para sanear a saúde física da tabela?",
            "options": [
                ("Executar OPTIMIZE para consolidar os arquivos pequenos em arquivos de ~1 GB e executar VACUUM posteriormente para remover arquivos órfãos antigos.", True, "Correto. O OPTIMIZE faz o bin-packing consolidando pequenos arquivos e o VACUUM expurga os arquivos antigos que foram substituídos pelos novos arquivos consolidados."),
                ("Executar DROP TABLE e recriar a tabela como CSV.", False, "Incorreto. Causaria perda total de dados e pioraria o desempenho com CSV."),
                ("Desligar o cluster e aguardar o Azure apagar os arquivos automaticamente.", False, "Incorreto. O storage em nuvem não apaga arquivos sem comando explícito."),
                ("Executar VACUUM RETAIN 0 HOURS seguido de RESTART WORKSPACE.", False, "Incorreto. VACUUM com zero horas corrompe queries ativas e viola a segurança.")
            ],
            "explanation": "A rotina padrão de manutenção física do Delta Lake é composta por `OPTIMIZE` (para compactar e bin-pack) e `VACUUM` (para expurgar arquivos substituídos que ultrapassaram o período de retenção)."
        },
        # Q115
        {
            "scenario": "Qual propriedade de tabela do Delta Lake permite que novas gravações compactem pequenos arquivos automaticamente logo após a escrita de cada micro-lote, mitigando o problema de small files em streaming?",
            "options": [
                ("delta.autoCompact = true (combinado com delta.optimizeWrite = true).", True, "Correto. As propriedades delta.autoCompact e delta.optimizeWrite compactam arquivos automaticamente durante as transações de escrita no Delta Lake."),
                ("spark.streaming.zipFiles = true", False, "Incorreto. Propriedade inexistente."),
                ("delta.neverSmallFiles = true", False, "Incorreto. Propriedade inexistente."),
                ("storage.compressEverything = true", False, "Incorreto. Propriedade fictícia.")
            ],
            "explanation": "`Optimize Write` organiza as partições antes de gravar para gerar arquivos maiores, enquanto `Auto Compact` executa uma compactação leve logo após a transação, mantendo a tabela saudável em streams contínuos."
        },
        # Q116
        {
            "scenario": "Um engenheiro precisa sobrescrever apenas as vendas do ano de 2024 em uma tabela Delta particionada por 'ano', mantendo os dados dos outros anos 100% intactos. Qual opção do write em PySpark garante essa substituição atômica?",
            "options": [
                ("df_2024.write.format('delta').mode('overwrite').option('replaceWhere', 'ano = 2024').saveAsTable('vendas')", True, "Correto. A opção replaceWhere realiza uma sobrescrita atômica e seletiva apenas na partição ou filtro especificado, sem apagar as demais partições da tabela."),
                ("df_2024.write.format('delta').mode('overwrite').saveAsTable('vendas')", False, "Incorreto. O mode('overwrite') sem replaceWhere apagaria a tabela inteira e deixaria apenas os dados de 2024."),
                ("df_2024.write.mode('append').saveAsTable('vendas')", False, "Incorreto. O modo append duplicaria os registros de 2024 em vez de substituí-los."),
                ("delete from vendas; insert into vendas;", False, "Incorreto. Apagaria todos os anos antes de inserir.")
            ],
            "explanation": "A opção `.option('replaceWhere', 'predicado')` combinada com `.mode('overwrite')` no Delta Lake garante substituição atômica e segura exclusivamente dos dados que atendem à condição do predicado."
        },
        # Q117
        {
            "scenario": "No Spark Structured Streaming, qual modo de leitura de dados é utilizado para consultar uma tabela Delta que é continuamente atualizada por outro pipeline?",
            "options": [
                ("spark.readStream.table('prod.silver.pedidos')", True, "Correto. A API spark.readStream.table() lê uma tabela Delta como uma fonte contínua de streaming, consumindo novos commits em tempo real."),
                ("spark.read.table('prod.silver.pedidos')", False, "Incorreto. spark.read opera em batch estático, não como streaming contínuo."),
                ("spark.streamFromTable('prod.silver.pedidos')", False, "Incorreto. Sintaxe inexistente na API do PySpark."),
                ("spark.table('prod.silver.pedidos').toStreaming()", False, "Incorreto. Sintaxe inválida.")
            ],
            "explanation": "No PySpark, a leitura de uma tabela Delta governada como fonte de streaming é realizada com `spark.readStream.table('catalogo.schema.tabela')` ou `spark.readStream.format('delta').load('caminho')`."
        },
        # Q118
        {
            "scenario": "Como o Delta Lake lida com duas gravações concorrentes disparadas exatamente no mesmo milissegundo sobre a mesma tabela, utilizando o protocolo Optimistic Concurrency Control (OCC)?",
            "options": [
                ("O primeiro commit conclui com sucesso; o segundo commit verifica se os arquivos que ele leu foram alterados pelo primeiro; se não houver conflito nos arquivos afetados, o segundo commit é confirmado; se houver conflito, ele falha com ConcurrentAppendException ou tenta novamente.", True, "Correto. O OCC assume que a maioria das transações não colide; em caso de sobreposição direta no mesmo arquivo/partição, uma exceção de conflito de concorrência é disparada."),
                ("O segundo commit apaga os dados do primeiro commit sem verificar nada.", False, "Incorreto. O Delta Lake previne sobrescritas silenciosas e perda de dados."),
                ("O cluster trava permanentemente e exige reinicialização do workspace.", False, "Incorreto. Concorrência é tratada de forma limpa na camada de transação do storage."),
                ("O Spark converte a tabela para SQLite local.", False, "Incorreto. Resposta fictícia.")
            ],
            "explanation": "O Controle de Concorrência Otimista (OCC) garante transações ACID no Lakehouse. O segundo commit checa o Delta Log para validar se os dados lidos continuam válidos antes de consolidar sua escrita."
        },
        # Q119
        {
            "scenario": "Qual é a principal recomendação para colunas que devem ser escolhidas para compor o Liquid Clustering (CLUSTER BY) em uma tabela Delta?",
            "options": [
                ("Escolher colunas frequentemente utilizadas em filtros (WHERE), junções (JOIN) e de alta ou moderada cardinalidade (ex: id_cliente, codigo_pais, data_evento), limitando a até 4 colunas.", True, "Correto. As colunas ideais para CLUSTER BY são aquelas que os usuários mais utilizam em cláusulas de filtro e junção, com cardinalidade suficiente para permitir boa poda estatística."),
                ("Escolher 50 colunas com textos gigantes e descrições de produtos.", False, "Incorreto. Recomenda-se clusterizar por no máximo 4 colunas de tipos numéricos, datas ou strings curtas."),
                ("Escolher apenas colunas que contenham 100% de valores nulos.", False, "Incorreto. Colunas nulas não proveem nenhum ganho de poda de leitura."),
                ("Escolher colunas booleanas com apenas dois valores possíveis (True/False).", False, "Incorreto. Colunas de cardinalidade binária muito baixa não aproveitam bem o espaço multidimensional do clustering.")
            ],
            "explanation": "O DP-750 orienta selecionar até 4 colunas com alta/moderada cardinalidade que apareçam frequentemente em predicados de consultas (`WHERE col = ...`) para maximizar o data skipping do Liquid Clustering."
        },
        # Q120
        {
            "scenario": "Um analista precisa checar quais arquivos Parquet físicos estão atualmente ativos e referenciados pela versão corrente de uma tabela Delta. Qual comando SQL detalha essa estrutura?",
            "options": [
                ("SELECT * FROM prod.vendas.pedidos.files;", True, "Correto. A tabela de metadados especiais <tabela>.files retorna a lista de arquivos Parquet físicos ativos, tamanho em bytes e estatísticas da versão atual."),
                ("SHOW DISK FILES ON prod.vendas.pedidos;", False, "Incorreto. Sintaxe inexistente."),
                ("DESCRIBE PHYSICAL STORAGE prod.vendas.pedidos;", False, "Incorreto. Sintaxe inválida."),
                ("LIST DIRECTORY IN TABLE prod.vendas.pedidos;", False, "Incorreto. Sintaxe inexistente.")
            ],
            "explanation": "O Delta Lake disponibiliza tabelas de metadados auxiliares via notação de ponto, como `tabela.files` (para listar arquivos ativos e estatísticas de min/max) e `tabela.history`."
        },
        # Q121
        {
            "scenario": "Quais DUAS opções garantem que o Auto Loader (cloudFiles) consuma e converta tipos numéricos com inferência estrita de dados em vez de tratar tudo como StringType? (Selecione duas opções)",
            "options": [
                (".option('cloudFiles.inferColumnTypes', 'true')", True, "Correto. Instrui o Auto Loader a inferir os tipos exatos de dados (INT, DOUBLE, DATE) em vez de manter StringType."),
                (".option('cloudFiles.schemaLocation', 'abfss://checkpoints@adls/schemas/...')", True, "Correto. O schemaLocation é indispensável para persistir o schema inferido e registrar a evolução entre execuções."),
                (".option('cloudFiles.allStringsAlways', 'true')", False, "Incorreto. Opção inexistente que forçaria tudo para string, o oposto do requisitado."),
                (".option('spark.ignoreTypes', 'true')", False, "Incorreto. Opção inexistente."),
                (".option('cloudFiles.deleteCorruptedData', 'true')", False, "Incorreto. Dados corrompidos devem ser resgatados em _rescued_data, não apagados.")
            ],
            "type": "multiple",
            "explanation": "Por padrão, o Auto Loader pode inferir campos JSON como string para evitar falhas. Ao configurar `cloudFiles.inferColumnTypes = true` com um `schemaLocation` persistente, ele infere tipos numéricos e temporais precisos."
        },
        # Q122
        {
            "scenario": "Um engenheiro de dados executa a query: SELECT * FROM vendas_delta TIMESTAMP AS OF '2023-01-01';. A consulta falha com erro informando que o timestamp solicitado é anterior ao histórico disponível. O que provocou a perda das versões históricas anteriores?",
            "options": [
                ("A execução periódica do comando VACUUM com período de retenção que expurgou os arquivos Parquet antigos anteriores à janela configurada.", True, "Correto. O VACUUM remove permanentemente os arquivos de dados que foram desassociados do log há mais tempo que o período de retenção, impedindo Time Travel para além dessa data."),
                ("O Apache Spark desliga o Time Travel no primeiro dia de cada ano.", False, "Incorreto. O Time Travel é contínuo e governado pelas políticas de retenção do storage."),
                ("A Microsoft desabilita o Delta Log automaticamente em contas gratuitas.", False, "Incorreto. O Delta Log é parte essencial do formato e não é desabilitado."),
                ("O arquivo de checkpoint Parquet corrompeu todo o metastore.", False, "Incorreto. Checkpoints são redundantes e auto-recuperáveis.")
            ],
            "explanation": "O Time Travel no Delta Lake é limitado pela retenção do comando `VACUUM`. Se o VACUUM foi executado expurgando arquivos com mais de 7 dias, consultas de Time Travel buscando dados de anos anteriores não encontrarão os Parquets físicos correspondentes."
        },
        # Q123
        {
            "scenario": "Ao ler uma tabela Delta através do Databricks Disk Cache (aceleração de cache em disco SSD dos nós de computação), qual é o benefício para consultas analíticas repetitivas?",
            "options": [
                ("As leituras subsequentes ocorrem diretamente a partir dos discos SSD locais ultrarrápidos das máquinas virtuais do cluster, evitando a latência de rede de download do ADLS Gen2.", True, "Correto. O Databricks Disk Cache cria réplicas dos blocos de dados Parquet nos discos NVMe/SSD locais dos workers, acelerando consultas repetidas em até 5x a 10x."),
                ("O cache converte as consultas para HTML estático.", False, "Incorreto. Resposta fictícia."),
                ("O cache desliga o cluster após 3 segundos.", False, "Incorreto. Cache não controla desligamento."),
                ("O cache armazena os dados no navegador do usuário.", False, "Incorreto. O cache reside nos nós de computação do cluster.")
            ],
            "explanation": "O Databricks Disk Cache utiliza os discos locais SSD/NVMe dos nós workers para armazenar cópias dos blocos remotos de Parquet lidos do ADLS Gen2, eliminando gargalos de rede em leituras subsequentes."
        },
        # Q124
        {
            "scenario": "Qual comando SQL do Delta Lake restaura a tabela para o estado exato da transação anterior, desfazendo o último comando de DELETE que excluiu registros por engano?",
            "options": [
                ("RESTORE TABLE prod.vendas.pedidos TO VERSION AS OF (SELECT max(version) - 1 FROM (DESCRIBE HISTORY prod.vendas.pedidos));", True, "Correto. O RESTORE TABLE com a versão imediatamente anterior reverte com perfeição o estado da tabela, desfazendo a operação incorreta de exclusão."),
                ("CTRL+Z ON prod.vendas.pedidos;", False, "Incorreto. Não existe comando de atalho de teclado no SQL."),
                ("DELETE UNDO FROM prod.vendas.pedidos;", False, "Incorreto. Sintaxe inválida."),
                ("REBOOT CLUSTER TO RESTORE DATA;", False, "Incorreto. Reiniciar o cluster não altera os dados persistidos no storage.")
            ],
            "explanation": "O `RESTORE TABLE` é a ferramenta definitiva de recuperação de desastres do Delta Lake, permitindo retornar a qualquer versão válida registrada no histórico do Delta Log."
        },
        # Q125
        {
            "scenario": "Em um pipeline de streaming com Auto Loader, como o desenvolvedor garante que arquivos vazios de 0 bytes gerados por falhas de escrita na origem não quebrem o pipeline nem gerem registros nulos?",
            "options": [
                (".option('cloudFiles.ignoreCorruptFiles', 'true')", True, "Correto. A opção ignoreCorruptFiles permite ignorar arquivos danificados ou vazios sem interromper o processamento contínuo dos demais arquivos válidos."),
                (".option('cloudFiles.crashImmediately', 'true')", False, "Incorreto. A intenção é não quebrar o pipeline."),
                (".option('deleteDiskFiles', 'true')", False, "Incorreto. Opção inexistente."),
                (".option('skipEverything', 'true')", False, "Incorreto. Opção fictícia.")
            ],
            "explanation": "A opção `cloudFiles.ignoreCorruptFiles` ou `cloudFiles.ignoreMissingFiles` oferece resiliência a anomalias temporárias de escrita na fonte sem derrubar o stream de produção."
        },
        # Q126
        {
            "scenario": "Qual função de agregação de strings no PySpark permite consolidar múltiplos nomes de produtos comprados em um único pedido em uma única string separada por vírgula (ex: 'Notebook, Mouse, Teclado')?",
            "options": [
                ("concat_ws(', ', collect_list('nome_produto'))", True, "Correto. collect_list() agrega os valores em um array de elementos e concat_ws() une os elementos em uma string delimitada."),
                ("string_sum('nome_produto')", False, "Incorreto. Função inexistente no Spark."),
                ("group_concat_excel('nome_produto')", False, "Incorreto. Função fictícia."),
                ("join_all_strings('nome_produto')", False, "Incorreto. Função inexistente.")
            ],
            "explanation": "No PySpark, a combinação de `collect_list()` (ou `collect_set()` para valores distintos) com `concat_ws(separador, array)` é a abordagem padrão para concatenação agregada de strings."
        },
        # Q127
        {
            "scenario": "Para garantir a máxima performance de leitura em consultas SQL analíticas em uma tabela de Vendas de 100 TB no Azure Databricks, qual combinação de tecnologias modernas do Lakehouse é a recomendação oficial do DP-750?",
            "options": [
                ("Formato Delta Lake acelerado por Photon Engine, com Liquid Clustering (CLUSTER BY) e Deletion Vectors habilitados.", True, "Correto. Essa é a arquitetura moderna padrão ouro: Delta Lake colunar + Photon SIMD em C++ + Liquid Clustering multidimensional + Deletion Vectors para mutações rápidas."),
                ("Formato CSV com particionamento Hive em 20 níveis de subpastas.", False, "Incorreto. CSV é lento, não possui estatísticas colunares e 20 níveis de pastas causa lentidão extrema."),
                ("Tabelas temporárias em memória RAM gravadas em arquivos de texto sem cabeçalho.", False, "Incorreto. Sem persistência e inviável para 100 TB."),
                ("Formato JSON compactado com GZIP sem índice nem metadados.", False, "Incorreto. JSON exige parsing de texto caro e não suporta poda eficiente de colunas.")
            ],
            "explanation": "A pilha de alta performance do Databricks no exame DP-750 combina o motor Photon, o protocolo Delta Lake com Deletion Vectors e o layout físico governado pelo Liquid Clustering."
        },
        # Q128
        {
            "scenario": "O que acontece se uma consulta de leitura tentar ler uma tabela Delta enquanto outro pipeline de escrita está adicionando novos arquivos Parquet em um commit em andamento?",
            "options": [
                ("A consulta de leitura lê snapshot isolado consistente da versão anterior confirmada no Delta Log, sem sofrer bloqueio (locks) nem ler dados inconsistentes 'fantasmas'.", True, "Correto. Graças ao isolamento de snapshot (Snapshot Isolation) do Delta Lake, leitores nunca bloqueiam escritores e escritores nunca bloqueiam leitores."),
                ("A consulta de leitura falha com erro de Deadlock no banco de dados.", False, "Incorreto. Delta Lake não utiliza locks tradicionais pessimistas de banco relacional."),
                ("A consulta de leitura lê metade das linhas novas e metade das antigas gerando inconsistência.", False, "Incorreto. Viola a garantia de atomicidade e consistência ACID do Delta Lake."),
                ("O cluster de leitura é pausado até o pipeline de escrita terminar.", False, "Incorreto. Não há bloqueio mútuo entre leitura e escrita.")
            ],
            "explanation": "O Delta Lake implementa Snapshot Isolation: o leitor consulta o snapshot imutável validado pelo último commit JSON confirmado, garantindo leitura consistente mesmo durante escritas massivas simultâneas."
        },
        # Q129
        {
            "scenario": "Um engenheiro de dados precisa calcular a média móvel de faturamento dos últimos 7 dias para cada loja física. Qual cláusula de Window specification atende a esse cálculo?",
            "options": [
                ("Window.partitionBy('id_loja').orderBy('data_venda').rowsBetween(-6, 0)", True, "Correto. A cláusula rowsBetween(-6, 0) define um frame de janela que inclui as 6 linhas anteriores mais a linha atual, totalizando os 7 dias para a média móvel."),
                ("Window.partitionBy('id_loja').unboundedPreceding()", False, "Incorreto. unboundedPreceding calcularia o acumulado desde o início dos tempos, não a janela móvel de 7 dias."),
                ("Window.orderBy('data_venda').rangeBetween(0, 7)", False, "Incorreto. Incluiria dias futuros, não os últimos 7 dias."),
                ("GROUP BY id_loja", False, "Incorreto. GROUP BY simples colapsa as linhas e não mantém a granularidade diária da média móvel.")
            ],
            "explanation": "A especificação de frame `rowsBetween(-6, 0)` ou `rangeBetween(-INTERVAL 6 DAYS, CURRENT ROW)` em conjunto com `avg()` calcula médias móveis com fidelidade temporal em PySpark e SQL."
        },
        # Q130
        {
            "scenario": "Qual comando SQL do Delta Lake limpa arquivos físicos órfãos com mais de 30 dias de uma tabela e emite um relatório com a lista de arquivos excluídos?",
            "options": [
                ("VACUUM prod.vendas.pedidos RETAIN 720 HOURS DRY RUN; (para visualizar) e depois VACUUM prod.vendas.pedidos RETAIN 720 HOURS; (para executar).", True, "Correto. 30 dias equivalem a 720 horas. O modificador DRY RUN permite auditar previamente quais arquivos serão expurgados antes da deleção definitiva."),
                ("DELETE OLD FILES IN prod.vendas.pedidos OLDER THAN 30 DAYS;", False, "Incorreto. Sintaxe inexistente no Delta Lake."),
                ("PURGE TABLE prod.vendas.pedidos WITH 30 DAYS;", False, "Incorreto. Sintaxe inexistente."),
                ("DROP OBSOLETE FILES ON prod.vendas.pedidos;", False, "Incorreto. Sintaxe inexistente.")
            ],
            "explanation": "O comando `VACUUM <tabela> RETAIN <n> HOURS DRY RUN` lista os arquivos elegíveis para expurgo sem excluí-los fisicamente, permitindo validação prévia de segurança antes da deleção irreversível."
        }
    ]
    return d3_specs

