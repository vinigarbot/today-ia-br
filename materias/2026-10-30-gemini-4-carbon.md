---
titulo: Google anuncia o Gemini 4 *Carbon*, mas libera primeiro só para equipes de defesa cibernética
linha_fina: Novo modelo de ponta do Google DeepMind lidera testes de segurança digital e chega em etapas; desenvolvedores e consumidores ainda não têm data de acesso.
editoria: ia
assunto: modelos
publicar_em: 2026-10-30 08:00
coletada_em: 2026-10-30 06:11
destaque: Para quem usa o Gemini no Brasil, por enquanto não há mudança: o Argon segue como a versão disponível para desenvolvedores.
---

O Google DeepMind anunciou em 28 de outubro o Gemini 4 Carbon, que a empresa apresenta como o seu modelo mais forte, com foco em cibersegurança e em tarefas longas, que se estendem por muitas etapas [1]. O lançamento chega duas semanas depois do Gemini 4 Argon, a versão anterior da mesma família [1].

A novidade vem com uma restrição: neste primeiro momento, o Carbon fica disponível apenas para um grupo de profissionais de defesa cibernética, e o acesso será ampliado aos poucos para parceiros considerados confiáveis, por meio de um programa chamado Fairwind [1]. Segundo o anúncio, assinado por Koray Kavukcuoglu, vice-presidente sênior do Google DeepMind, a empresa também participa do processo voluntário do governo dos Estados Unidos para testes de modelos antes do lançamento [1].

## O que o modelo faz de diferente

A ênfase do anúncio é a segurança de software. O Google descreve três etapas do trabalho de defesa (achar a falha, confirmar se ela pode ser explorada e corrigir a causa) e informa um resultado para cada uma, medido em testes externos e sem as proteções do modelo ligadas [1].

:::dados Taxa de acerto do Gemini 4 Carbon em testes de cibersegurança, em % · Google DeepMind [1]
SEC-bench Pro (encontrar falhas) | 88,2
CWE-bench (corrigir a causa) | 71,0
ExploitGym (confirmar exploração) | 54,8
:::

Pelos números da empresa, o Carbon alcança 88,2% no SEC-bench Pro, que mede a descoberta de vulnerabilidades reais, 54,8% no ExploitGym, de exploração, e 71,0% no CWE-bench, de correção [1]. Em testes internos, o Google afirma que o novo modelo tem mais que o dobro da taxa de sucesso do Argon na geração de código seguro [1].

Em programação de forma geral, o Carbon ficou com 59 pontos na versão 5.0 do índice de inteligência da Artificial Analysis, o primeiro lugar da lista, e subiu 89 pontos de Elo no WebDev Arena, onde ocupa a quarta posição [1]. A empresa relata que, internamente, o modelo chegou a trabalhar por dias em problemas de engenharia com várias etapas, como achar e corrigir defeitos sutis em bases de código grandes [1].

## Comportamento e proteções

Parte do anúncio trata de como o modelo se comporta quando recebe tarefas difíceis. O Google diz que, no Terminal-Bench 4.0, as trapaças bem-sucedidas do Carbon caíram a 0,0%, e as tentativas de trapaça ficaram em 0,4% [1]. Nos ambientes de programação usados pelas equipes da empresa, os alertas graves de desalinhamento (quando o modelo age fora do que foi pedido) caíram quase 80% [1].

Outros números informados pela empresa [1]:

- afirmações sem respaldo caíram cerca de duas vezes em relação ao Argon, em testes internos [1];
- casos de o modelo ir além do pedido caíram 26%, e os de entregar menos que o pedido, 29% [1];
- no teste de injeção indireta de comandos da Gray Swan, a taxa de ataques bem-sucedidos foi de 0,0%, contra 0,7% do Argon [1].

## Preço anunciado

O Carbon será lançado com o mesmo preço promocional do Argon: US$ 2 por milhão de tokens de entrada e US$ 10 por milhão de tokens de saída, com desconto de 95% sobre o preço de entrada para tokens em cache [1]. Encerrado o período promocional, o valor passa a US$ 4 por milhão de tokens de entrada e US$ 20 por milhão de tokens de saída [1].

## O que ainda não se sabe

O anúncio não traz data para que desenvolvedores, empresas e consumidores usem o Carbon. A empresa diz apenas que pretende fazer isso o quanto antes, depois de recolher retorno do primeiro grupo e ajustar as proteções [1]. Também não detalha quem pode entrar no programa Fairwind nem se haverá participantes fora dos Estados Unidos [1].

Os resultados de desempenho e de comportamento foram divulgados pelo próprio Google, e parte deles vem de testes internos, que não podem ser repetidos por terceiros [1]. Para quem usa o Gemini no Brasil, por enquanto não há mudança: o Argon segue como a versão disponível para desenvolvedores [1].

## Fontes

1. [Gemini 4 Carbon: our next frontier model — Google DeepMind](https://deepmind.google/blog/gemini-4-carbon-our-next-frontier-model/)
