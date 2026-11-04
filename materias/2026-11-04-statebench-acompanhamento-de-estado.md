---
titulo: Nos casos mais difíceis, modelos de ponta acertam 13% ou menos ao seguir *mudanças* em textos longos
linha_fina: Teste da Ai2 mede se a IA acompanha valores que mudam ao longo de um documento; Gemini, Claude e GPT-6 vão bem no simples e caem quando as mudanças se encadeiam.
editoria: ia
assunto: pesquisa
publicar_em: 2026-11-04 08:00
coletada_em: 2026-11-04 06:07
destaque: Nos problemas mais longos do nível mais difícil, a taxa de acerto caiu para 13% ou menos.
---

A Ai2 apresentou nesta terça-feira (3) o StateBench, um teste de referência que mede se modelos de linguagem conseguem acompanhar como as informações sobre pessoas, objetos ou variáveis mudam ao longo de um documento extenso. O anúncio saiu na página da organização no Hugging Face e vem com relatório técnico, código e base de dados abertos [1].

Na avaliação, quatro modelos de ponta, o Gemini 3.8 Flash, o Claude Opus 5.5 e o GPT-6 nas versões Sol e Luna, foram bem nas tarefas simples, mas perderam precisão quando cada mudança dependia da anterior. Nos problemas mais longos do nível mais difícil, a taxa de acerto caiu para 13% ou menos [1].

## O que o teste mede

A tarefa é conhecida de quem lê código ou um romance policial: saber o valor atual de uma variável que foi reatribuída várias vezes, ou quem está com um objeto depois de ele passar de mão em mão. Segundo a Ai2, alguns casos exigem só achar a última atualização; outros obrigam a seguir uma cadeia de mudanças, em que um passo perdido estraga a resposta final [1].

O StateBench organiza isso em quatro níveis. No primeiro, o valor nunca muda, como uma data de nascimento. No segundo, ele é substituído e basta achar o mais recente, como a regulagem de um termostato. No terceiro, cada atualização parte do valor atual, como o placar de um jogo. No quarto, uma variável pode receber o valor de outra, como no truque de esconder uma bola sob cinco copos e trocá-los de lugar várias vezes [1].

Para a comparação ser justa, os quatro níveis são derivados da mesma sequência, com o mesmo número de variáveis e as atualizações nos mesmos pontos; muda só o tipo de operação [1]. A base publicada no Hugging Face está em inglês, e o conjunto principal de teste tem 16,3 mil linhas [2].

## Arquitetura pesa mais nos níveis difíceis

O estudo também compara arquiteturas. A maioria dos modelos atuais usa a arquitetura transformer, que, segundo a Ai2, tem limites teóricos conhecidos nos casos com longas cadeias de dependência. Por isso a organização testou também modelos recorrentes e híbridos, que carregam uma memória contínua ao longo do texto, como os baseados em Gated DeltaNet [1].

Entre os modelos abertos pré-treinados, de 275 milhões a 7 bilhões de parâmetros, quase todos foram bem no primeiro nível, perderam precisão no segundo à medida que o texto crescia e ficaram no nível do acaso no mais difícil. O formato também influiu: modelos pequenos que quase gabaritaram o primeiro nível num formato de busca em texto longo ficaram perto do acaso no mesmo problema apresentado como edições de planilha [1].

Depois, a equipe treinou do zero modelos de 275 milhões de parâmetros direto nas tarefas, com sequências de até 256 atualizações, e os testou em sequências de até 64 mil, 250 vezes mais longas [1].

:::dados Tamanho das sequências, em número de atualizações · estudo da Ai2 [1]
Maior sequência no treino | 256
Maior sequência no teste | 64000
:::

Os modelos recorrentes e híbridos generalizaram quase sem erro nos três primeiros níveis até dezenas de milhares de atualizações. Os transformers aprenderam os níveis fáceis, pioraram nas sequências longas e nunca aprenderam o mais difícil. Nele, a variante de Gated DeltaNet com memória mais flexível ficou perto do acerto total até cerca de dez vezes o tamanho visto no treino [1].

## Limites e o que ainda não se sabe

A Ai2 aponta como provável causa da queda dos modelos de ponta a sensibilidade das tarefas difíceis: como muitos passos afetam a resposta final, sobra menos margem para perder uma atualização [1].

O teste também supõe um número fixo de variáveis, enquanto em situações reais, como uma conversa longa, novas pessoas e objetos aparecem no caminho; esse cenário ainda não está coberto. Fica em aberto ainda a posição exata de uma versão mais restrita do Gated DeltaNet na hierarquia de níveis [1].

## Fontes

1. [StateBench: Testing how language models track state changes over long documents (Ai2, no Hugging Face)](https://huggingface.co/blog/allenai/statebench)
2. [Base de dados allenai/state-bench (Hugging Face)](https://huggingface.co/datasets/allenai/state-bench)
