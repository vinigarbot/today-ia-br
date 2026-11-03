---
titulo: Falha passou quase dois meses no Transformers; Hugging Face propõe testar com modelos *encolhidos*
linha_fina: Versões reduzidas de modelos reais rodam em processador comum e teriam acusado, em cada versão do código, o erro que deixou o UMT5 ver a resposta no treino.
editoria: ia
assunto: desenvolvimento
publicar_em: 2026-11-03 08:00
coletada_em: 2026-11-03 06:07
destaque: O contrato vale enquanto o exemplo, rodado no modelo reduzido, continuar produzindo os mesmos resultados.
---

A Hugging Face, empresa que mantém a Transformers, uma das bibliotecas de código aberto mais usadas para rodar e treinar modelos de IA, propôs um padrão de testes chamado Model Integration Contracts (contratos de integração de modelos, ou MIC). O anúncio, publicado no blog da empresa nesta terça-feira (3), parte de uma falha que ficou quase dois meses no ramo principal do código sem ser notada [1].

## O erro que motivou a proposta

Em 30 de julho de 2026, a biblioteca passou a usar um mecanismo de atenção do PyTorch, chamado SDPA, no modelo T5. Como efeito colateral, o decodificador do UMT5, modelo da mesma família, passou a enxergar tokens que ainda não deveria ver. Na prática, durante o treino, ele podia olhar a resposta que deveria prever. Nada travou, e a correção só chegou em 28 de setembro [1].

Segundo a empresa, o tamanho do conjunto de testes explica por que isso acontece. A Transformers aceita mais de 750 tipos de modelo e tem mais de 88 mil testes em processador comum no ramo principal, além de mais de 200 mil testes em placas de vídeo numa rodada diária. Rodar tudo a cada proposta de mudança ocuparia placas de vídeo o dia inteiro, e por isso parte dos erros só aparece depois de incorporada ao código [1].

## Como funciona o contrato

A saída proposta é encolher o modelo. Cada contrato reúne três peças: uma versão reduzida de um modelo real, com menos camadas e camadas mais estreitas, mas com todos os tipos de camada do original e com os arquivos de tokenizador sem alteração; um exemplo de uso executável, como gerar texto ou dar um passo de treino; e os resultados de referência desse exemplo, revisados por uma pessoa. O contrato vale enquanto o exemplo, rodado no modelo reduzido, continuar produzindo os mesmos resultados [1].

:::dados Tamanho dos pesos do UMT5, em MB · estudo da Hugging Face [1]
Modelo original | 1227
Versão reduzida para teste | 66
:::

A redução também vale para modelos grandes. No relatório citado pela empresa, o Llama 4 Scout passa de 108,6 bilhões para 44,7 milhões de parâmetros, com a parte de visão indo de 34 para 2 camadas e a de linguagem de 48 para 4 [1].

Ao reaplicar os contratos sobre cinco meses de histórico do código, a versão reduzida do UMT5 acusou a falha em todas as versões entre a introdução do erro e a correção. Num teste à parte, a empresa desfez a correção e a verificação voltou a falhar, numa etapa que levou 13,4 segundos em processador comum, sem contar a preparação [1].

## Agentes rascunham, pessoas aprovam

A Hugging Face criou uma ferramenta de linha de comando, a tmic, que monta o contrato e o modelo reduzido. Para um modelo novo, um modelo de linguagem escreve o rascunho do exemplo de uso, mas resultados esperados que mudem precisam de revisão humana, segundo a empresa [1].

A empresa também comparou duas formas de criar os pesos do modelo reduzido. Com o Whisper, de reconhecimento de fala, a versão de pesos aleatórios pegou 18 de 24 falhas inseridas de propósito, e a versão treinada em poucos exemplos pegou as 24. A própria Hugging Face ressalva que eram falhas sintéticas e que ambas deixaram passar um erro real que só apareceu com o modelo completo [1].

## O que ainda não se sabe

Em 1º de novembro, segundo a empresa, o teste rodava na integração contínua da Transformers apenas avisando sobre falhas, sem impedir a incorporação de mudanças. Ainda faltam medir quantos erros reais ele pega nas propostas de mudança, com que frequência gera alarme falso e quanto trabalho exige a revisão dos resultados de referência. A cobertura de famílias de modelos também é parcial, e os testes atuais continuam valendo [1].

## Fontes

1. [Transformers Model Integration Contracts — blog da Hugging Face](https://huggingface.co/blog/transformers-mic)
