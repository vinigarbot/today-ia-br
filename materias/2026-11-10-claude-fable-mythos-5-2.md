---
titulo: Anthropic lança o Claude Fable 5.2, mais barato e até *30%* mais rápido que a versão anterior
linha_fina: Novo modelo de topo custa US$ 8 por milhão de tokens de entrada, lidera a maior parte dos testes da empresa e tem uma versão sem travas, o Mythos 5.2, só para organizações aprovadas.
editoria: ia
assunto: modelos
publicar_em: 2026-11-10 08:00
coletada_em: 2026-11-10 06:07
destaque: Todos os números de desempenho foram medidos pela própria Anthropic ou por clientes que testaram o modelo antes do lançamento.
---

A Anthropic anunciou nesta segunda-feira (9) o Claude Fable 5.2 e o Claude Mythos 5.2, nova versão dos modelos que a empresa reserva para os trabalhos técnicos mais difíceis [1]. Segundo o anúncio, os dois geram respostas até 30% mais rápido que as versões 5.1 e saem por um preço menor: US$ 8 por milhão de tokens de entrada e US$ 40 por milhão de tokens de saída [1].

Fable e Mythos são, na prática, o mesmo modelo [1]. A diferença está nas travas: o Fable vem com bloqueios contra uso indevido em cibersegurança e biologia e fica aberto a todos os usuários, enquanto o Mythos só é liberado para organizações aprovadas nos programas de verificação da empresa para segurança digital e ciências da vida [1].

## O que muda para quem usa

O Fable 5.2 já está disponível em todas as plataformas da empresa, inclusive Amazon Web Services, Google Cloud e Microsoft Azure; na API, o identificador é `claude-fable-5-2` [1]. Há também um modo rápido, que acelera a geração de texto em até 2,5 vezes e custa o dobro: US$ 16 por milhão de tokens de entrada e US$ 80 por milhão de saída [1].

A própria Anthropic diz que o Fable não é o ponto de partida para a maioria das tarefas de programação e de escritório: a recomendação é começar pelo Opus 5.5 e subir para o Fable ou o Mythos apenas quando o trabalho pedir, ou descer para o Sonnet 5.5 e o Haiku 5.5 [1]. O Fable 5.2 também pode atuar como consultor de modelos menores ou como coordenador que distribui tarefas simples para eles [1].

Na semana de lançamento, assinantes de planos pagos elegíveis recebem uso extra do Fable, e nos planos Pro e nos assentos padrão do plano Team o modelo pode ocupar até metade do limite semanal [1].

## Desempenho declarado

Na tabela divulgada pela empresa, o Fable 5.2 fica à frente do Opus 5.5 em quase todas as capacidades avaliadas [1]. No FrontierCode 2.0, que mede se as alterações de código feitas pelo modelo seriam aceitas pelos mantenedores de projetos de código aberto, ele chega a 49,1% no nível de esforço Xhigh, o maior resultado entre os modelos já lançados que a empresa testou [1]. Os números abaixo usam o nível de esforço mais alto de cada modelo, com exceção do Gemini 4 Carbon, medido no esforço médio [1].

:::dados Acerto no FrontierCode 2.0, em % · teste da Anthropic [1]
Claude Fable 5.2 | 49,1
Claude Opus 5.5 | 45,5
GPT-6 Astra | 42,8
Gemini 4 Carbon | 41,1
Claude Fable 5.1 | 32,4
:::

Segundo a Anthropic, no esforço alto o Fable 5.2 empata com o melhor resultado do Opus 5.5 nesse teste por cerca de metade do custo por tarefa [1]. No RoboDojo, que avalia o controle de um robô simulado de dois braços a partir de imagens de câmera, o modelo marcou 64,9%, mais que o dobro dos 27,6% do Fable 5.1 [1].

O anúncio lista ainda resultados obtidos em testes internos antes do lançamento: a formalização da prova do Último Teorema de Fermat em 30 horas por cerca de mil agentes, o projeto de três aparelhos eletrônicos que funcionaram sem ajustes elétricos e a solução de dois problemas em aberto da física de buracos negros [1]. Na segurança digital, o Mythos 5.2 encontrou 10,2% mais vulnerabilidades que o Opus 5.5 num teste interno com 1.829 falhas já publicadas [1].

## Travas e limites

A empresa afirma que as travas do Fable 5.2 bloqueiam cerca de 55% menos pedidos legítimos que as do Fable 5.1, com queda de 60% em cibersegurança e de 40% em biologia [1]. Quando um pedido é barrado, a resposta passa a vir de um modelo anterior: o Opus 4.8 em cibersegurança e o Opus 5 em biologia [1].

A Anthropic também diz ter limitado, no treinamento, os avanços em pesquisas que poderiam acelerar diretamente o desenvolvimento de IA, como a otimização de código para chips aceleradores; nessas áreas, o modelo fica no nível do Opus 5.5 [1]. Nos testes de alinhamento, a empresa avalia como baixo o risco de comportamento inseguro em situações críticas, mas reconhece que os dois modelos desconfiam de que estão sendo avaliados com mais frequência que os anteriores, o que dificulta prever como agirão no uso real [1].

Todos os números de desempenho foram medidos pela própria Anthropic ou por clientes que testaram o modelo antes do lançamento [1]. Os avaliadores externos citados no anúncio não revisaram o texto nem o relatório técnico da empresa [1].

## Fontes

1. [Introducing Claude Fable 5.2 and Claude Mythos 5.2 — Anthropic](https://www.anthropic.com/claude-fable-and-mythos-5-2)
