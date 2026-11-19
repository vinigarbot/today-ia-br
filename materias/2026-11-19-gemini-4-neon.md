---
titulo: Google lança o Gemini 4 *Neon*, com custo por tarefa 32% menor que o do Carbon na configuração padrão
linha_fina: Novo modelo chega à API, ao app Gemini e ao Antigravity a US$ 3 por milhão de tokens de entrada; o Google o posiciona entre o rápido Hydrogen e o Carbon.
editoria: ia
assunto: modelos
publicar_em: 2026-11-19 08:00
coletada_em: 2026-11-19 06:07
destaque: Segundo o Google, o Neon fica entre o Carbon, voltado aos projetos mais longos e difíceis, e o Hydrogen, feito para a execução rápida do dia a dia.
---

O Google lançou em 18 de novembro o Gemini 4 Neon, modelo voltado a programação complexa, análise e fluxos de trabalho de empresas, em anúncio assinado por Koray Kavukcuoglu, vice-presidente sênior do Google DeepMind [1]. Segundo o Google, o Neon fica entre o Carbon, voltado aos projetos mais longos e difíceis, e o Hydrogen, feito para a execução rápida do dia a dia [1].

## Onde está disponível e quanto custa

O modelo começou a ser liberado no mesmo dia na API do Gemini, pelo Google AI Studio e pelo Android Studio, no Gemini for business e no aplicativo Gemini, para assinantes dos planos Google AI Pro e Ultra [1]. Assinantes pagos desses planos também podem usá-lo no Google Antigravity, o ambiente de programação da empresa [1].

Na API, o preço é de US$ 3 por milhão de tokens de entrada e de US$ 15 por milhão de tokens de saída, com janela de contexto de 1 milhão de tokens [1]. Tokens são os pedaços de texto que o modelo processa e que servem de base para a cobrança. Quando a entrada já está em cache, isto é, quando o mesmo conteúdo é reaproveitado entre pedidos, o valor cai para US$ 0,15 por milhão, desconto de 95% [1].

## Custo por tarefa e desempenho

O Neon tem quatro níveis de raciocínio, que permitem trocar mais qualidade por mais gasto de tokens conforme a tarefa [1]. No nível padrão, chamado de alto, o Google diz que o custo por tarefa é 32% menor que o do Gemini 4 Carbon e de 50% a 80% menor que o de modelos concorrentes de ponta, em testes de terceiros [1]. No nível mais alto, o "xhigh", a empresa afirma que o custo por tarefa segue pelo menos 36% abaixo do de concorrentes em suas configurações máximas [1].

Nesse nível mais alto, o modelo marcou 61 pontos no índice de inteligência da Artificial Analysis, o que o deixa em terceiro lugar geral, atrás de modelos maiores e mais lentos, segundo o Google [1]. No índice de programação com agentes da mesma organização, ficou em primeiro, com 58,6 pontos [1].

:::dados Resultados em testes escolhidos pelo Google, em % · Google DeepMind [1]
Terminal-Bench Science | 70,5
Terminal-Bench 4.1 | 65,2
CWE-bench v2 (correção de falhas) | 70,7
AutomationBench | 56,3
:::

Em tarefas de empresa, o Google diz que o Neon alcançou 70,9% no índice da Vals, segundo lugar no ranking, e o primeiro lugar em testes de pesquisa jurídica e de tributação [1]. No AutomationBench, da Zapier, que mede automação de tarefas, ficou em primeiro, com 56,3% [1].

## Segurança digital

Uma versão do modelo voltada à defesa cibernética será liberada nos próximos dias a defensores selecionados, dentro do programa Fairwind [1]. Segundo a empresa, essa versão chegou a 90,5% no SEC-bench Pro, teste de busca de vulnerabilidades em código, com custo por desafio de cerca de metade do de concorrentes [1]. Para entrar no programa, empresas devem procurar a equipe de contas do Google Cloud [1].

## O que o Google diz sobre riscos e o que ainda não se sabe

O Google afirma que manteve no Neon as mesmas proteções do Carbon contra uso indevido em segurança digital e biossegurança, mas com menos recusas a pedidos legítimos: o modelo recusou 1,98% das tarefas do Terminal-Bench 4.0 [1]. Num teste interno de honestidade de agentes, a taxa de aprovação foi de 99,2%, e o modelo tomou atalhos indevidos em 2,45% das tarefas de um teste de trapaça em programação, o menor índice entre os modelos Gemini 4 [1].

Os números de desempenho, custo e segurança vêm do próprio Google e de testes escolhidos pela empresa [1]. O anúncio compara o custo por tarefa com o Carbon, mas não traz os preços por token do Carbon nem detalha como o custo por tarefa foi calculado em cada teste [1]. Também não informa quando a versão para defesa cibernética chega a quem está fora do programa Fairwind [1].

## Fontes

1. [Introducing Gemini 4 Neon](https://deepmind.google/blog/introducing-gemini-4-neon/)
