---
titulo: OpenAI lança o GPT-6 Rosalind para ciências da vida, com preço *três* vezes maior que o do antecessor
linha_fina: Modelo de raciocínio biológico chega só a organizações aprovadas pela OpenAI para pesquisa interna e custa US$ 15 por milhão de tokens de entrada.
editoria: ia
assunto: modelos
publicar_em: 2026-10-31 08:00
coletada_em: 2026-10-31 06:07
destaque: Na prática, o novo modelo cobra o triplo nas duas pontas.
---

A OpenAI lançou em 30 de outubro o GPT-6 Rosalind, um modelo voltado à pesquisa em ciências da vida [1]. Segundo o registro de mudanças da plataforma de desenvolvedores da empresa, o modelo traz raciocínio especializado em biologia e usa ferramentas científicas para lidar com problemas complexos de pesquisa [1]. O acesso, porém, não é aberto: vale apenas para organizações aprovadas no programa Rosalind Research, por meio do programa de acesso confiável da OpenAI, e só para pesquisa interna feita por usuários autorizados [1].

O novo modelo é o sucessor de uma linha que a OpenAI começou a oferecer em setembro. Em 8 de setembro, a empresa tornou disponível o GPT-Rosalind (identificado na API como `gpt-rosalind-research`), também restrito a pesquisa interna aprovada, com cobrança iniciada em 5 de outubro [1].

## O que muda no preço

A tabela de preços da OpenAI lista o GPT-6 Rosalind a US$ 15 por milhão de tokens de entrada e US$ 75 por milhão de tokens de saída [2]. Os dois modelos anteriores da família, `gpt-rosalind-research` e `gpt-rosalind-discovery`, custam US$ 5 por milhão de tokens de entrada e US$ 25 por milhão de saída [2]. Na prática, o novo modelo cobra o triplo nas duas pontas [2].

:::dados Preço por milhão de tokens de entrada, em US$ [2]
GPT-6 Rosalind | 15
GPT-Rosalind Research | 5
GPT-Rosalind Discovery | 5
:::

O GPT-6 Rosalind também tem preço para o cache de instruções, recurso que guarda partes repetidas de um pedido para cobrá-las mais barato nas chamadas seguintes. A entrada já armazenada em cache sai por US$ 1,50 por milhão de tokens, contra US$ 0,50 dos modelos anteriores [2]. A gravação no cache custa US$ 18,75 por milhão de tokens na opção de 30 minutos e US$ 37,50 na de 12 horas, modalidades que a tabela não prevê para os dois modelos mais antigos [2]. A opção de 12 horas foi lançada pela OpenAI em 20 de outubro e, segundo a empresa, cobra pela gravação 2,5 vezes o preço normal de entrada [1].

A página de preços afirma ainda que todas as organizações elegíveis continuarão recebendo acesso aos modelos GPT-Rosalind mais recentes à medida que forem lançados [2].

## O que ainda não se sabe

A documentação aberta da OpenAI não traz resultados de testes do GPT-6 Rosalind nem compara o desempenho dele com o dos modelos anteriores da família [1][2]. Também não detalha quais ferramentas científicas o modelo usa nem os critérios de aprovação no programa, que ficam numa página da central de ajuda da empresa [2].

Para pesquisadores e empresas de biotecnologia no Brasil, a consequência imediata é que o modelo não está disponível para contratação livre pela API: é preciso passar pelo programa de acesso confiável [1][2]. A documentação consultada não informa se há restrição por país para essa aprovação [1][2].

## Fontes

1. [Changelog da API da OpenAI](https://platform.openai.com/docs/changelog)
2. [Preços da API da OpenAI](https://developers.openai.com/api/docs/pricing)
