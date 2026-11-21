---
titulo: Em teste de química de remédios da OpenAI, modelos montam moléculas, mas acertam só *metade* das escolhas
linha_fina: O MedChemBench reúne 99 problemas tirados de pesquisas publicadas; o melhor modelo passa de 95% na montagem de moléculas e fica perto de 50% ao escolher compostos e prever medidas.
editoria: ia
assunto: pesquisa
publicar_em: 2026-11-21 08:00
coletada_em: 2026-11-21 06:07
destaque: A própria OpenAI afirma que os números não mostram se os modelos são capazes de descobrir remédios novos ou melhorar decisões de laboratório.
---

A OpenAI apresentou em 20 de novembro o MedChemBench, um teste que avalia se modelos de IA conseguem raciocinar como um químico medicinal, o profissional que desenha e ajusta moléculas candidatas a remédio [1]. O conjunto tem 99 problemas montados a partir de 117 artigos científicos e patentes, com 761 estruturas moleculares diferentes [1]. Os resultados foram descritos num artigo assinado por seis pesquisadores da empresa [2].

Na configuração de raciocínio "xhigh", o GPT-6.2 Astra obteve 84,5% da pontuação possível, à frente do GPT-6 Astra, com 83,3%, do GPT-6.1 Sol, com 82,0%, e do GPT-5.6 Sol, com 58,2% [1]. O maior resultado registrado no artigo, que não inclui o GPT-6.2 Astra, foi de 83,83%, do GPT-6 Astra no nível máximo de esforço [2].

:::dados Pontuação geral no MedChemBench, em % do total, no nível xhigh [1]
GPT-6.2 Astra | 84,5
GPT-6 Astra | 83,3
GPT-6.1 Sol | 82,0
GPT-6.1 Terra | 75,1
GPT-5.6 Sol | 58,2
:::

## Como o teste funciona

Em cada problema, o modelo recebe o que os pesquisadores sabiam num certo ponto de um projeto real: a proteína-alvo, os objetivos, os compostos já estudados e parte dos resultados de laboratório [1]. A partir disso, precisa cumprir tarefas de quatro tipos: reconstruir a estrutura das moléculas com as ligações e a disposição espacial corretas, explicar resultados com base nas evidências fornecidas, ordenar e escolher compostos que atendam aos requisitos e prever propriedades numéricas medidas nos estudos originais [1].

A dificuldade central, segundo a OpenAI, é que melhorar uma característica de uma molécula costuma piorar outra: um composto pode agir com força contra uma proteína ligada à doença e, ao mesmo tempo, ser mal absorvido ou se decompor rápido demais no organismo [1]. Um dos problemas usa pesquisas sobre inibidores da PRMT5, proteína estudada em tratamentos contra o câncer, e pede ao modelo que preveja como três compostos parecidos se comportam em três medidas diferentes [1]. As previsões numéricas recebem crédito parcial conforme a distância do valor medido: errar pelo dobro ou pela metade vale meio ponto [2].

## Onde os modelos acertam e onde erram

A montagem das moléculas foi a parte que mais separou os modelos [2]. No nível xhigh, o GPT-6 Astra obteve 95,37% do crédito nessa categoria, enquanto o GPT-6 Luna ficou em 12,42% e quatro modelos mais antigos ficaram entre 8,74% e 17,00% [2]. Num exemplo, a tarefa era juntar uma estrutura central a dois grupos químicos mantendo um anel de 18 átomos: o GPT-6 Astra acertou nas dez tentativas, enquanto o GPT-5.6 Sol e o GPT-5.6 Luna erraram todas, um deles produzindo um anel de 15 átomos e o outro, dois fragmentos soltos [1][2].

Nas demais categorias, a distância entre os modelos foi bem menor, e o teto, mais baixo [2]. Mesmo o GPT-6 Astra conseguiu 50,42% do crédito em ordenar e escolher compostos e 47,02% em prever valores numéricos, contra 91,05% na explicação científica [2].

:::dados Desempenho do GPT-6 Astra por categoria, em % do crédito, no nível xhigh [2]
Estrutura molecular | 95,37
Explicação científica | 91,05
Ordenação e escolha | 50,42
Previsão numérica | 47,02
:::

A empresa também observou que níveis maiores de raciocínio melhoraram as notas, mas as diferenças entre modelos continuaram grandes [1].

## Os limites do resultado

A própria OpenAI afirma que os números não mostram se os modelos são capazes de descobrir remédios novos ou melhorar decisões de laboratório [1]. Como os problemas vêm de pesquisas já publicadas, a empresa diz não poder descartar que os modelos tenham visto esse material antes [1]. Cada resposta foi uma única tentativa, sem ferramentas, sem retorno sobre o acerto e sem novos experimentos [1]. O teste mede, portanto, o raciocínio sobre evidências históricas, e não a descoberta de medicamentos no mundo real [1].

Também foi a própria fabricante que criou o teste e avaliou só os seus modelos: foram onze versões do GPT, em diferentes níveis de esforço de raciocínio [1][2].

## Fontes

1. [Can AI help scientists identify promising drug candidates? (OpenAI)](https://openai.com/index/introducing-medchembench/)
2. [MedChemBench: Evaluating complex multimodal reasoning in medicinal chemistry (artigo, OpenAI)](https://cdn.openai.com/pdf/09c4ec60-a32e-4652-837b-1811368a3bb0/medchembench-paper.pdf)
