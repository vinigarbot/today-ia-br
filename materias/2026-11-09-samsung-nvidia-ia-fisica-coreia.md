---
titulo: Samsung reduz simulação de chip de 18 horas para 41 segundos com IA e GPUs da *Nvidia*
linha_fina: Anúncio da Nvidia sobre a Coreia do Sul inclui ainda direção autônoma nível 4 com a Kakao Mobility e robô da LG treinado em fábrica real.
editoria: ia
assunto: empresas
publicar_em: 2026-11-09 08:00
coletada_em: 2026-11-09 06:08
destaque: Por ora, é uma possibilidade apontada pela empresa, não algo em uso.
---

A Nvidia publicou no domingo (8) um balanço de projetos com empresas sul-coreanas que usam computação acelerada, simulação e IA em chão de fábrica, carros e robôs. O número que mais chama a atenção vem da Samsung Electronics: num caso de análise térmica e mecânica de chips, o tempo de simulação caiu de cerca de 18 horas para 41 segundos, um ganho de aproximadamente 1.600 vezes, segundo a Nvidia [1].

O anúncio faz parte de uma série de comunicados da empresa sobre a Coreia do Sul, publicados entre domingo e segunda-feira, que inclui um acordo ampliado com o Ministério de Ciência e TIC do país e investimentos planejados em startups locais [2][3].

## O que a Samsung mediu

Segundo a Nvidia, a Samsung está montando fluxos de análise térmica e mecânica na escala do chip com a ferramenta PhysicsNeMo, da Nvidia [1]. No caso citado, a empresa combinou três coisas: propriedades de material previstas por IA, uma malha de cálculo mais grossa e processamento em GPU [1].

O ponto de partida foi uma simulação de malha fina rodando num processador (CPU) de 32 núcleos, que levava cerca de 18 horas. O resultado final foi uma simulação de malha grossa acelerada por GPU, que terminou em 41 segundos [1].

A mesma parceria cobre outras etapas do desenvolvimento de semicondutores. Na pesquisa de materiais, a plataforma sMOL, da Samsung, executou cálculos selecionados de química quântica até 5 vezes mais rápido do início ao fim com a biblioteca cuEST, da Nvidia [1]. A Samsung também usa bibliotecas da Nvidia para acelerar contas com sistemas lineares esparsos no projeto de dispositivos assistido por computador e estuda outra biblioteca para treinar modelos de IA em escala atômica [1].

A Nvidia diz ainda que, no futuro, seu kit de ferramentas para agentes poderia ligar essas simulações e modelos, de modo que agentes de engenharia rodem análises e comparem alternativas de projeto [1]. Por ora, é uma possibilidade apontada pela empresa, não algo em uso.

## Carro autônomo e robô na fábrica

Os outros dois projetos do comunicado são de outra natureza [1]:

- **Kakao Mobility:** planeja usar a plataforma de referência Hyperion, com o computador de bordo DRIVE AGX Thor, e o sistema de segurança Halos, da Nvidia, para desenvolver um sistema de direção autônoma de nível 4, voltado a futuros serviços de mobilidade no país. O desenvolvimento inicial deve usar veículos de uso específico da Kia e se apoia na experiência da empresa operando no distrito de Gangnam, em Seul [1].
- **LG Electronics:** a Nvidia e a LG demonstraram o robô CLOiD fazendo tarefas de manipulação e de manufatura num ambiente de fábrica real, com o modelo Isaac GR00T. O processo liga coleta de dados reais, ampliação desses dados com o Cosmos, treino do modelo, computação no próprio robô e avaliação em simulação [1].

As equipes pretendem transformar esse ciclo num processo repetível para treinar, avaliar e melhorar robôs de manufatura [1].

## Governo e startups no mesmo pacote

Em paralelo, a Nvidia e o Ministério de Ciência e TIC da Coreia do Sul ampliaram a colaboração no ecossistema de IA soberana do país, de semicondutores e data centers a formação de profissionais, startups, modelos e segurança [2]. O acordo abre caminho para que fabricantes coreanos de chips de IA estudem entrar no ecossistema NVLink Fusion, da Nvidia, e prevê programas de treinamento e certificação [2].

Num fórum organizado com o ministério no centro de convenções Coex, a Nvidia anunciou investimento na Point2, que faz interconexões entre chips e racks baseadas em radiofrequência, e investimentos planejados na Motif Technologies, na RLWRLD e na Upstage [3]. A empresa diz ter mais de 1.000 membros baseados na Coreia no Inception, seu programa de apoio a startups [3].

## O que ainda não se sabe

A comparação de 1.600 vezes não é entre duas máquinas fazendo exatamente a mesma conta: a simulação de 18 horas usava malha fina, e a de 41 segundos, malha grossa com propriedades previstas por IA [1]. O comunicado não informa a diferença de precisão entre os dois resultados nem em quantos casos o método foi testado [1].

Também não há datas para os serviços de nível 4 da Kakao Mobility, nem valores para os investimentos em startups [1][3]. Os números vêm da própria Nvidia e não foram verificados por terceiros [1].

## Fontes

1. [Korea Advances Physical AI Across Industries With NVIDIA](https://blogs.nvidia.com/blog/korea-physical-ai-ecosystem/)
2. [From Chips to Skills, NVIDIA and Korea Expand Sovereign AI Collaboration](https://blogs.nvidia.com/blog/korea-sovereign-ai-collaboration/)
3. [NVIDIA Announces New Planned Investments in Korean Startups at the MSIT-NVIDIA AI Startup Partnership Forum](https://blogs.nvidia.com/blog/korean-startup-investments-msit/)
