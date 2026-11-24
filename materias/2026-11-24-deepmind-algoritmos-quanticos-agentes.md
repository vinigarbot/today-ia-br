---
titulo: Agentes do Gemini 4 cortam em 11,8 vezes o custo de um algoritmo quântico para fusão, com *prova* matemática
linha_fina: Google DeepMind e Google Quantum AI usaram equipes de agentes para enxugar circuitos quânticos de fusão, química e remédios, e cada ganho foi verificado no provador Lean.
editoria: ia
assunto: pesquisa
publicar_em: 2026-11-24 08:00
coletada_em: 2026-11-24 06:07
destaque: Circuitos quânticos que exigem muitos recursos não podem ser testados em computadores comuns nem nos processadores quânticos pequenos que existem hoje.
---

O Google DeepMind divulgou nesta segunda-feira (23) um estudo em que equipes de agentes baseados no Gemini 4 melhoraram algoritmos quânticos conhecidos e reduziram o custo de executá-los [1]. O trabalho foi feito em parceria com o Google Quantum AI, e cada melhoria encontrada pelos agentes foi provada matematicamente no Lean, um programa de verificação formal de demonstrações [1].

O resultado de maior destaque está num cálculo ligado à fusão por confinamento inercial, método que usa lasers para comprimir combustível de hidrogênio até a ignição [1]. Segundo a empresa, os agentes reduziram em 11,8 vezes o custo computacional desse circuito quântico, uma medida que combina a quantidade de qubits e de operações necessárias [1].

## Por que a prova matemática importa

Circuitos quânticos que exigem muitos recursos não podem ser testados em computadores comuns nem nos processadores quânticos pequenos que existem hoje [1]. Por isso, explica o DeepMind, a única forma de garantir que eles funcionam é demonstrar matematicamente que estão corretos [1]. Foi esse o papel do Lean: só entravam no caderno compartilhado do projeto as ideias que passavam pela verificação [1].

A organização do trabalho também chama atenção. Para cada problema, a equipe criou times independentes de agentes, encarregados de buscar melhorias nos algoritmos [1]. A cada quatro horas, agentes de cada time se reuniam numa espécie de conferência virtual para trocar, debater e comparar ideias, e o custo computacional foi caindo à medida que surgiam soluções mais eficientes [1]. Os pesquisadores definiam os problemas e supervisionavam o andamento [1].

## Os ganhos em cada aplicação

Além da fusão, o estudo cobre química e biologia. Para uma molécula sensível à luz, a simulação quântica ficou 8 vezes mais barata, com uma forma mais simples de o algoritmo acompanhar a posição das partículas e as forças elétricas entre elas [1]. No caso do citocromo P450, enzima que decompõe a maior parte dos remédios no corpo humano e é importante no desenvolvimento de medicamentos, o ganho foi de 2,5 vezes [1].

Os agentes também melhoraram peças de uso geral. Numa implementação específica do algoritmo de Grover, usado para buscar itens numa lista sem ordem, a execução ficou 2,57 vezes mais rápida [1]. Numa rotina de cálculo do arco-seno, usada por muitos outros algoritmos para carregar números em estados quânticos, o ganho de velocidade foi de 290 vezes [1].

A quantidade de memória necessária também caiu. No circuito de fusão, o número de qubits com correção de erros passou de 5.650 para 4.338; no do citocromo P450, de 481 para 333 qubits [1].

:::dados Qubits necessários, antes e depois dos agentes · Google DeepMind [1]
Fusão, antes | 5650
Fusão, depois | 4338
Citocromo P450, antes | 481
Citocromo P450, depois | 333
:::

## Limites e o que vem a seguir

O próprio DeepMind reconhece que os ganhos não bastam para tirar essas aplicações do papel agora: rodar as simulações ainda exigiria mais recursos do que os primeiros computadores quânticos com correção de erros devem oferecer [1]. A empresa descreve os resultados como melhorias significativas, mas não indica prazo para que esses cálculos sejam feitos em máquinas reais [1].

Para que outros grupos possam repetir e ampliar o trabalho, a empresa abriu o código da biblioteca em Lean criada para o projeto, além das especificações dos problemas e das soluções verificadas [1]. Segundo o DeepMind, o mesmo método poderia acelerar outras áreas da computação quântica e da pesquisa científica, deixando aos pesquisadores a escolha dos problemas e a interpretação dos resultados [1].

## Fontes

1. [Finding faster quantum algorithms with agents and formal verification — Google DeepMind](https://deepmind.google/blog/finding-faster-quantum-algorithms-with-agents-and-formal-verification/)
