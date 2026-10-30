---
titulo: Mistral libera os pesos do Large 4, modelo de 1 trilhão de parâmetros que pode rodar em servidor *próprio*
linha_fina: A Mistral AI publicou a versão final do seu principal modelo com licença que permite uso comercial e diz liderar entre os modelos abertos em programação.
editoria: ia
assunto: modelos
publicar_em: 2026-10-30 18:00
coletada_em: 2026-10-30 06:11
destaque: A principal mudança é o acesso.
---

A Mistral AI publicou em 29 de outubro os pesos do Mistral Large 4, o seu principal modelo, apelidado pela empresa de Le Chonk [1]. Com isso, qualquer organização pode baixar o modelo, ajustá-lo e rodá-lo na própria infraestrutura, em vez de acessá-lo apenas pela API da empresa [1].

O Large 4 tem 1 trilhão de parâmetros, aceita entrada em mais de um formato (multimodal) e já estava em prévia pública desde o começo do mês [1]. Segundo a Mistral, a versão liberada agora passou por mais três semanas de aprendizado por reforço depois da prévia, com ganhos em programação e em cibersegurança defensiva, além de gastar menos tokens para chegar às respostas [1].

## O que muda para quem usa

A principal mudança é o acesso. Os pesos estão no Hugging Face, e a empresa indica as ferramentas vLLM e SGLang para quem quiser hospedar o modelo [1]. A licença, que a Mistral chama de Mistral Ecosystem Open-Weight e descreve como uma versão modificada da MIT, permite usar, modificar, ajustar e comercializar o modelo [1]. A única condição é que empresas que vendem o próprio modelo como serviço precisam de uma licença comercial separada [1].

Para quem prefere não hospedar, o modelo está na API da Mistral, no Mistral Studio, no OpenRouter, nos serviços da Nvidia e no Microsoft Foundry [1]. O preço anunciado na API é de US$ 0,70 por milhão de tokens de entrada, US$ 0,07 para entrada em cache e US$ 2,10 por milhão de tokens de saída [1].

O modelo agora oferece três níveis de raciocínio, para equilibrar custo e qualidade: baixo, para tarefas simples; médio, para o dia a dia; e alto, o padrão, para os casos mais difíceis [1]. A empresa diz ainda que o Large 4 domina mais de 160 idiomas [1].

## Os números divulgados

A Mistral afirma que o Large 4 é o melhor modelo de pesos abertos para programação [1]. Os resultados abaixo foram divulgados pela própria empresa, com testes de terceiros como a Artificial Analysis e a Cognition [1].

:::dados Resultados do Mistral Large 4 em testes, em % · Mistral AI [1]
BrowseComp (navegação na web) | 84,5
FinWorkBench (tarefas de finanças) | 73,3
Cyber Index (cibersegurança) | 51
Coding Agent Index (programação) | 48
Terminal-Bench 4.0 (terminal) | 41
:::

No índice de agentes de programação da Artificial Analysis, o modelo fez 48%, praticamente empatado com o GLM-5.3, o líder entre os abertos, mas usando em média 47% menos tokens por tarefa [1]. No Terminal-Bench 4.0, subiu 13 pontos percentuais em relação à prévia, para 41%, com 30% menos tokens de saída [1]. No teste privado FrontierCode 2.0, da Cognition, que avalia se uma alteração de código seria aceita por quem mantém o projeto, marcou 19,7%, resultado com que, segundo a empresa, assume a liderança desse teste [1].

Em segurança, a Mistral informa que o modelo recusa em média 96,6% dos pedidos maliciosos ligados a ataques cibernéticos e resiste a 97,1% dos ataques no teste de segurança de agentes B3, contra 93,3% na prévia [1].

## Limites e o que ainda falta

A própria empresa reconhece um risco. Ao monitorar o uso real desde a prévia, a Mistral diz ter visto o modelo recusar ataques contra alvos reais, mas identificou potencial de ajuda para quem quer conduzir ataques de verdade, e afirma que está ajustando as proteções e vai continuar fazendo isso nos próximos meses [1].

Uma versão especializada para testes de invasão e avaliação de vulnerabilidades está disponível só para parceiros selecionados, como a Orange Cyberdefense, com triagem e contratos que restringem os testes a sistemas próprios ou autorizados [1].

O relatório técnico completo ainda não foi publicado; a empresa diz que ele sai em breve [1]. Até lá, os números de desempenho são os informados pela Mistral, e a empresa convida a comunidade a fazer as próprias avaliações [1].

## Fontes

1. [Mistral Large 4 (Le Chonk) is now open weight — Mistral AI](https://mistral.ai/news/mistral-large-4-oss/)
