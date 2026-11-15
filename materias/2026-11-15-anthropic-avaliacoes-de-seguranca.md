---
titulo: No mesmo modelo, teste de *segurança* da Anthropic variou até 34 pontos conforme a configuração
linha_fina: Guia da empresa mostra por que nota de segurança depende de como o teste é feito e diz que os testes de uma só pergunta já estão saturados.
editoria: ia
assunto: pesquisa
publicar_em: 2026-11-15 08:00
coletada_em: 2026-11-15 06:07
destaque: Uma nota de segurança vale o que vale o teste que a produziu.
---

A Anthropic publicou em 13 de novembro um guia sobre como construir avaliações de segurança de modelos de IA, os testes que medem se um sistema responde de forma adequada a pedidos que podem causar dano. O texto traz recomendações e números das avaliações da própria empresa, incluindo casos em que o resultado mudou só por causa da configuração do teste [1].

O ponto de partida é uma constatação da própria empresa: quando se diz que um modelo é "mais seguro que o antecessor", isso significa que ele teve nota melhor num conjunto de testes que alguém montou. Uma nota de segurança vale o que vale o teste que a produziu [1].

## O mesmo modelo, resultados diferentes

A Anthropic relata que, nos testes do Claude Fable 5.1 com conversas de várias rodadas, a taxa de respostas adequadas chegou a diferir 34 pontos percentuais entre duas configurações: o modelo puro, como os desenvolvedores o acessam pela API, e o Claude.ai, onde se aplica um prompt de sistema, o conjunto de instruções que a empresa coloca antes da conversa [1].

Um dos exemplos citados é o teste sobre suicídio e automutilação. Ao revisar as conversas antes do lançamento do Fable 5.1, a equipe notou que o modelo às vezes validava de forma implícita a automutilação como forma de lidar com o sofrimento, mesmo em respostas que a desencorajavam e indicavam apoio humano. A empresa acrescentou uma instrução específica ao prompt de sistema, entre outros ajustes, e o resultado no Claude.ai ficou bem acima do registrado na API [1].

:::dados Taxa de respostas adequadas em teste sobre suicídio e automutilação, em % [1]
API (modelo puro) | 60
Claude.ai, com o novo prompt de sistema | 94
:::

Por isso, a recomendação é informar sempre a configuração usada no teste, com versão do modelo, parâmetros, prompts, versão do avaliador e datas, e não comparar notas obtidas com avaliadores diferentes [1].

## Testes simples já não separam os modelos

Segundo a empresa, os testes de uma única pergunta estão saturados: na API, as taxas de respostas inofensivas ficam entre 94% e 98% em todos os modelos recentes. Eles seguem úteis para checar se falhas já conhecidas voltaram, mas pouco dizem sobre a diferença entre modelos. Esse conjunto cobre 16 áreas de política de uso, em sete idiomas e em mais de um produto [1].

A alternativa defendida são simulações de conversa com várias rodadas. Um especialista no tema escreve a especificação do cenário, com objetivo, tática, perfil e tom do usuário simulado; um outro modelo Claude faz o papel desse usuário, e um modelo avaliador dá a nota a cada conversa com base em critérios definidos para aquela área de risco. Basta uma resposta inadequada no meio da conversa para que ela toda seja reprovada [1].

O guia também alerta que a recusa nem sempre é a resposta certa. Em conversas sobre suicídio, apenas se negar a responder é considerado uma falha: o adequado é acolher a pessoa e indicar apoio humano. Em biologia e segurança digital, temas de uso duplo, a resposta adequada ajuda no pedido legítimo e retém os detalhes operacionais que serviriam ao uso nocivo [1].

## O que a empresa recomenda medir

Entre as orientações estatísticas, a Anthropic diz tratar 100 itens como o mínimo para um teste complexo de várias rodadas e 1.000 para um teste simples de uma pergunta. Também recomenda registrar antes da coleta quais métricas e comparações serão feitas [1].

O avaliador automático, outro modelo de IA que dá as notas, deve ser conferido contra a avaliação de pessoas, que classificam uma amostra sem ver o veredito da máquina. Se os especialistas humanos concordam entre si e discordam do avaliador, a orientação é revisar os critérios [1].

## Os limites dos números

O próprio guia mostra que diferenças aparentes podem não significar nada. Num teste sobre golpes românticos no Claude.ai, o Claude Opus 5 teve 98% de respostas adequadas e o Opus 5.5, 94%, mas a diferença não foi estatisticamente significativa, e a empresa diz que não pode concluir que um seja melhor que o outro. Em testes de várias rodadas na API, as margens de erro podem passar de 10 pontos percentuais para mais ou para menos [1].

A Anthropic afirma ainda que, após incidentes próprios, reforçou o isolamento dos ambientes de teste, suspendeu temporariamente muitas avaliações que dão acesso à internet aos modelos e passou a monitorar em tempo real as que exigem busca na web. O texto não detalha esses incidentes [1].

Para quem quer começar, a empresa resume três passos: definir por escrito o que se quer medir antes de coletar dados, validar o avaliador contra o julgamento humano e informar a incerteza de cada resultado [1].

## Fontes

1. [Building strong safety evaluations — Anthropic](https://www.anthropic.com/research/building-strong-safety-evaluations)
