---
titulo: Anthropic mostra como o Claude revisa a própria *memória*; num teste, a nota subiu de 13% para 48%
linha_fina: Estudo descreve notas, revisão em segundo plano e wikis montadas pelo próprio modelo, com ganhos em testes de longo prazo e casos em que o recurso não ajudou.
editoria: ia
assunto: pesquisa
publicar_em: 2026-11-07 08:00
coletada_em: 2026-11-07 06:06
---

A Anthropic publicou em 6 de novembro um estudo de engenharia sobre como o Claude guarda e reorganiza o que aprende entre uma sessão de trabalho e outra. O texto descreve três peças: as notas que o modelo escreve durante a tarefa, uma revisão posterior dessas notas, que a empresa chama de "sonhar" (*dreaming*), e estruturas de consulta como wikis montadas pelo próprio modelo [1].

Por memória, a empresa entende o conhecimento que o Claude obtém com a experiência e mantém entre sessões, salvo como texto que ele pode ler depois. Ficam de fora o treinamento dos pesos do modelo, o aprendizado dentro de uma única conversa e os resumos que substituem trechos antigos de um diálogo longo [1].

## O que os testes mostraram

No CL-Bench 1.0, teste em que o agente responde perguntas consultando um banco de dados e recebe a resposta certa depois de cada tentativa, cada pergunta começava numa sessão nova, com acesso apenas a uma pasta de memória que persistia. Segundo a Anthropic, o Claude Opus 5 foi o primeiro modelo da família a fechar o ciclo de aprendizado: registrar o erro, testar hipóteses e transformar o resultado numa regra verificada. O Opus 5.5 e o Sonnet 5.5 fizeram o mesmo e, com memória, tiveram desempenho parecido com o do Opus 5 [1].

Outro teste usou o jogo Pokémon Red como tarefa longa. Por volta do passo 10.000, o Claude Sonnet 3.7 tinha criado 413 arquivos de memória em 225 pastas e conquistado uma insígnia. O Claude Fable 5, no mesmo ponto, tinha nove arquivos em duas pastas, mais um arquivo geral, e quatro insígnias. A diferença, segundo o estudo, está no que cada um guardou: o modelo mais antigo registrava dados que já aparecem na tela, como dinheiro e posição, enquanto o mais novo anotava estratégias e regras testadas [1].

A empresa também relata que orientar o modelo sobre como usar a memória ajudou mais as versões antigas. Pedir ao Sonnet 4.6 que lesse a memória antes de responder e testasse as próprias hipóteses quase dobrou sua nota. Já a regra "registre só os erros" fez o Opus 5 e o Opus 4.7 perderem boa parte do ganho que a memória trazia [1].

## Revisão em segundo plano e wikis

Na revisão em segundo plano, o modelo compara as notas com o registro original das sessões e corrige o que estiver errado. No exemplo do jogo, uma nota equivocada sobre a localização de um prédio fez o Claude voltar três vezes ao ponto de partida; com a nota corrigida pela revisão, ele avançou até a cidade seguinte [1].

O teste com mais números usou cerca de 350 mil documentos internos da Stainless, empresa comprada pela Anthropic em maio, com 25 perguntas sobre esse acervo. Agentes Opus 5 construíram uma wiki ao longo de 128 sessões. Usando só a wiki, a nota passou de 13% para 48% dos critérios avaliados entre a segunda e a 128ª sessão. Somando wiki e busca, a nota chegou a 61%, e cada pergunta gastou cerca de 20 mil *tokens* a menos [1].

:::dados Nota nas 25 perguntas, em % dos critérios avaliados · Anthropic [1]
Só busca | 53
Só wiki, após 128 sessões | 48
Busca e wiki | 61
:::

Em 24 perguntas sobre documentos de uma fusão de empresas, a maioria exigindo cruzar vários arquivos, o Claude acertou 87% dos itens que pediam essa combinação ao consultar a wiki, contra 73% só com busca. Num exercício de parecer jurídico, a primeira versão da wiki registrou 41 de 57 termos contratuais avaliados; depois de o modelo reescrever as instruções de montagem, os 57 apareceram [1].

## Limites e perguntas em aberto

O estudo registra casos em que a wiki não trouxe ganho claro, como uma tarefa jurídica em que cada critério podia ser encontrado por busca simples em um único documento, e outro em que a wiki ficou maior que os próprios arquivos de origem [1].

A Anthropic lembra ainda que a revisão em segundo plano consome processamento, que notas carregadas no início de toda sessão ocupam espaço e podem levar um erro adiante, e que ainda não está definido quando o modelo deve escrever na memória nem como mantê-la atualizada. Os resultados vêm de testes internos da própria empresa [1].

## Fontes

1. [The components of agent memory — Anthropic](https://www.anthropic.com/research/components-of-agent-memory)
