---
titulo: Google DeepMind lança o AlphaGenome 2, que acha quase o *dobro* de variantes causais em células imunes
linha_fina: O modelo prevê como mudanças no DNA alteram a atividade de genes em tipos específicos de célula e já está aberto para pesquisa não comercial.
editoria: ia
assunto: pesquisa
publicar_em: 2026-11-12 08:00
coletada_em: 2026-11-12 06:07
destaque: O DeepMind afirma que o AlphaGenome e o AlphaGenome 2 são destinados apenas à pesquisa e não foram validados nem aprovados para uso clínico ou diagnóstico.
---

O Google DeepMind anunciou nesta quarta-feira (11) o AlphaGenome 2, nova versão do seu modelo de IA que lê sequências de DNA e prevê como pequenas variações genéticas mudam a atividade dos genes [1]. A diferença em relação à primeira versão é o foco: em vez de médias de tecidos inteiros, o modelo faz previsões para tipos e estados específicos de célula, como uma célula do músculo do coração ou uma célula de defesa ativada por uma infecção [1].

Segundo a empresa, o modelo foi treinado com dados de humanos e de camundongos, incluindo mais de 107 milhões de perfis de células individuais, de 68 tecidos [1]. Ele está disponível desde já para pesquisa não comercial pela API do AlphaGenome e, para uso comercial, em prévia fechada [1].

## O que muda em relação à primeira versão

O AlphaGenome original recebia um trecho de 1 milhão de letras de DNA e devolvia, de uma só vez, previsões para milhares de experimentos de vários tecidos [1]. De acordo com o DeepMind, esse formato espalhava a capacidade do modelo e dificultava captar diferenças sutis entre tipos de célula parecidos [1].

Na nova versão, o modelo passou a ser condicional: além da sequência de DNA, ele recebe como entrada a condição biológica de interesse, que pode ser um tecido, um tipo de célula ou um estado celular, e faz uma previsão por vez [1]. Isso permite, segundo a empresa, aprender como o mesmo trecho de DNA é lido de forma diferente em cada célula [1].

O AlphaGenome 2 prevê as mesmas medidas da primeira versão, como expressão gênica e acessibilidade da cromatina, e acrescenta a metilação do DNA, que o DeepMind descreve como uma medida muito pedida pelos pesquisadores [1]. O modelo também consegue estimar dados que não foram medidos: a partir da atividade dos genes em células individuais, por exemplo, prevê a acessibilidade da cromatina, o que pode ajudar a escolher quais experimentos fazer em seguida [1].

## Os números divulgados

No conjunto de dados TenK10K, um mapa de 28 tipos de células do sistema imune, o AlphaGenome 2 identificou 30% das variantes causais, contra 16% da primeira versão ajustada com dados de células individuais e de outras ferramentas especializadas [1]. Na indicação de se a variante aumenta ou diminui a atividade de um gene, o índice foi de 43%, contra 23% [1]. É daí que vem a afirmação da empresa de que o novo modelo encontra quase o dobro de variantes [1].

:::dados Acerto no conjunto TenK10K, em % · Google DeepMind [1]
Variantes causais, AlphaGenome 2 | 30
Variantes causais, versão anterior | 16
Direção do efeito, AlphaGenome 2 | 43
Direção do efeito, versão anterior | 23
:::

O DeepMind cita ainda dois testes de caso. Em um, o modelo reproduziu por computador o resultado de um estudo recente que ligou uma variante genética à doença inflamatória intestinal, ao apontar que ela aumenta a atividade do gene ETS2 em macrófagos do intestino, células de defesa, sem afetar muito as demais [1]. No outro, com dados de um estudo sobre a vacina de mRNA contra a covid-19, o modelo separou células T ativadas pela vacina das que estavam em repouso e indicou que uma variante associada à covid-19 grave altera mais a atividade dos genes nas células ativadas [1].

## Novas células sem novo treinamento

Outro ponto destacado é a possibilidade de usar o modelo com dados novos sem treiná-lo de novo. O pesquisador envia um retrato da atividade dos genes de apenas algumas dezenas de células, que é resumido numa representação do estado celular e usado para orientar as previsões [1]. Segundo o DeepMind, nesse uso o AlphaGenome 2 iguala ou supera modelos treinados ou ajustados diretamente com aqueles dados [1].

A empresa também deixou prontas previsões para variantes ligadas a características e doenças, em centenas de tipos de célula e tecido, para que pesquisadores não precisem rodar grandes cálculos por conta própria [1]. Segundo o anúncio, em breve haverá habilidades do AlphaGenome 2 para o Google Antigravity, a plataforma de desenvolvimento com agentes da empresa [1].

## Limites

O DeepMind afirma que o AlphaGenome e o AlphaGenome 2 são destinados apenas à pesquisa e não foram validados nem aprovados para uso clínico ou diagnóstico [1]. Os resultados divulgados são da própria empresa, descritos no anúncio e no artigo científico que o acompanha [1]. O anúncio não informa preço para o uso comercial nem data para o fim da prévia fechada [1].

## Fontes

1. [AlphaGenome 2: Deciphering how cells read DNA to better understand disease — Google DeepMind](https://deepmind.google/blog/alphagenome-2-deciphering-how-cells-read-dna-to-better-understand-disease/)
