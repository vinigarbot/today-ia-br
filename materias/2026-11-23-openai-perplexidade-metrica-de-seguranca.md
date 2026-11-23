---
titulo: OpenAI revela números internos de pré-treino e propõe *limite* comum ao setor com base na perplexidade
linha_fina: O cientista-chefe da empresa diz que modelos abaixo de 0,8 de log-perplexidade já mostraram capacidades novas em segurança cibernética e matemática e pede regras comuns entre laboratórios.
editoria: ia
assunto: seguranca
publicar_em: 2026-11-23 08:00
coletada_em: 2026-11-23 06:07
destaque: A proposta é que os desenvolvedores se comprometam a não passar de um certo patamar até que a capacidade de entender e monitorar a IA atinja um marco concreto.
---

A OpenAI publicou neste domingo (22) um texto assinado pelo seu cientista-chefe, Jakub Pachocki, que divulga medições internas do pré-treino dos seus modelos e propõe que o setor adote a perplexidade como métrica comum para comparar desenvolvedores e embasar padrões de segurança compartilhados [1]. Segundo o texto, abrir esses números deixa os concorrentes com uma visão mais clara da posição da empresa, mas a urgência de criar medidas de segurança comuns pesou mais [1].

## O que é a métrica e o que os números mostram

A perplexidade mede, em média, quão bem um modelo prevê o próximo pedaço de texto (o token); quanto menor, melhores as previsões [1]. Na prática, a OpenAI acompanha o logaritmo dessa medida, também chamado de perda de entropia cruzada, calculado num conjunto de dados separado do treino e tirado do código interno da própria empresa [1].

De acordo com Pachocki, o GPT-3.5, base do ChatGPT original, ficava em cerca de 0,99 nessa escala, e o GPT-4, em cerca de 0,91 [1]. Abaixo de 0,8, a empresa diz ter visto surgir capacidades que considera transformadoras em segurança cibernética e matemática [1]. O texto afirma que não era possível saber de antemão que essas capacidades apareceriam nesses patamares [1].

:::dados Log-perplexidade no conjunto de avaliação interno da OpenAI (menor é melhor) [1]
GPT-3.5 | 0,99
GPT-4 | 0,91
Modelo usado em problemas de matemática | 0,76
:::

O caso citado como exemplo é o da matemática: há mais de um ano a empresa submete problemas em aberto aos seus modelos, e, ao passar para um modelo com log-perplexidade de cerca de 0,76, passou a obter resultados que o texto chama de inovadores [1]. A partir disso, Pachocki considera plausível uma aceleração parecida na pesquisa sobre o próprio pré-treino, com uma sequência de avanços fundamentais que poderia começar já em 2027 [1]. Ele avalia que o progresso em alinhamento e monitoramento dificilmente acompanharia esse ritmo [1].

Numa nota, a empresa afirma que a queda acentuada das perdas em 2026 vem principalmente de investimentos de longo prazo em pesquisa e em capacidade de computação, e só em parte menor da automação, embora já haja contribuições relevantes de IA no projeto dos modelos mais recentes [1].

## A proposta de limite

Extrapolando o progresso recente, o texto prevê novas capacidades transformadoras na faixa de 0,68 a 0,7, sem saber quais serão e reconhecendo que talvez nem estejam sendo testadas hoje [1]. Ao mesmo tempo, espera piora nas formas atuais de auditoria de alinhamento e modelos mais conscientes de quando estão sendo avaliados ou treinados [1].

Por isso, Pachocki propõe que os laboratórios de ponta definam juntos normas para avaliar esses modelos e testar as suas garantias de segurança antes do primeiro uso, com padrões comuns de transparência [1]. A proposta é que os desenvolvedores se comprometam a não passar de um certo patamar até que a capacidade de entender e monitorar a IA atinja um marco concreto [1]. Como exemplo de marco, o texto cita um sucessor dos monitores de cadeia de pensamento, que acompanham o raciocínio intermediário dos modelos [1]. A ideia é que esse primeiro limite abra caminho para limites sucessivos que ditem o ritmo do desenvolvimento [1].

## Limites e o que ainda não se sabe

O próprio texto lista os problemas da métrica [1]:

- cada laboratório usa conjuntos de avaliação e misturas de dados de treino diferentes, o que dificulta a comparação [1];
- a perplexidade não corresponde diretamente a uma tarefa útil; o interesse está em prever o surgimento de capacidades novas [1];
- ela não capta avanços fora do pré-treino, como o raciocínio em cadeia, que aumenta muito as capacidades sem reduzir a perplexidade [1];
- não se sabe qual é o piso da medida, e, perto dele, ganhos pequenos podem corresponder a saltos grandes de capacidade [1].

A empresa também reconhece que medir modelos antigos, como o GPT-2 e o GPT-3, num conjunto de código é um retrato ruim das capacidades gerais deles, já que não foram treinados para isso [1]. Os valores são da própria OpenAI, sem verificação independente, e o texto não traz compromisso de outros laboratórios com a proposta [1].

## Fontes

1. [Perplexity and Intelligence — OpenAI](https://openai.com/index/perplexity-and-intelligence)
