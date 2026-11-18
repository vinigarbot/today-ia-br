---
titulo: OpenAI lança o GPT-6.2 Astra com preço 20% menor que o do GPT-6 Astra; o *Sol* mantém a tarifa
linha_fina: Os dois modelos chegam à API com janela de 1,05 milhão de tokens, novas regras para instruções e histórico e desconto de até 40% para quem aceita esperar a resposta.
editoria: ia
assunto: modelos
publicar_em: 2026-11-18 08:00
coletada_em: 2026-11-18 06:06
destaque: Para quem usa a API, a mudança que mais exige atenção não está no preço, mas na forma como o histórico da conversa passa a ser tratado.
---

A OpenAI colocou na sua API nesta terça-feira (17) dois modelos da família GPT-6.2: o Astra, indicado para tarefas exigentes de raciocínio e programação, e o Sol, voltado para programação do dia a dia e para fluxos com agentes [1]. A documentação para desenvolvedores passou a apresentar o Astra como o modelo principal da empresa e o Sol como a opção de equilíbrio entre capacidade e custo [4].

Os dois aceitam texto e imagem e respondem em texto, sem suporte a áudio e vídeo [2][3]. Ambos têm janela de contexto de 1,05 milhão de tokens, com até 922 mil tokens de entrada e 128 mil de saída por pedido [2][3]. A data de corte do conhecimento é 18 de maio de 2026 no Astra e 1º de junho de 2026 no Sol [2][3].

## Quanto custa

Na tabela padrão, o GPT-6.2 Astra cobra US$ 8 por milhão de tokens de entrada e US$ 40 por milhão de tokens de saída [2]. O GPT-6 Astra, versão anterior da mesma linha que segue listada na documentação, cobra US$ 10 e US$ 50 [6]. A redução é de 20% nas duas pontas. Na entrada em cache, usada quando o mesmo começo de pedido se repete, o valor cai de US$ 1 para US$ 0,40 por milhão de tokens [2][6].

O GPT-6.2 Sol sai por US$ 2 na entrada e US$ 10 na saída, os mesmos valores do GPT-6.1 Sol [3][7].

:::dados Preço de entrada por milhão de tokens, em US$ · tabela padrão [5]
GPT-6 Astra | 10
GPT-6.2 Astra | 8
GPT-6.1 Sol | 2
GPT-6.2 Sol | 2
:::

As regras de cobrança extra seguem as dos modelos anteriores. Pedidos com mais de 272 mil tokens de entrada pagam o dobro na entrada e no cache e 1,5 vez na saída, sobre o pedido inteiro [2][3]. O processamento em lote custa metade da tabela padrão, e o modo rápido custa o dobro [2][3]. No modo mais veloz, chamado Ultrafast, a tarifa é de três vezes a padrão até 28 de fevereiro de 2027 e passa a seis vezes a partir de 1º de março de 2027 [5].

No mesmo dia, a OpenAI abriu em teste público duas janelas de espera para pedidos feitos em segundo plano: quem aceita receber a resposta em até duas horas paga 30% menos pelos tokens, e quem aceita até oito horas paga 40% menos [1][8]. O desconto vale para o GPT-6.2 Astra, o GPT-6.2 Sol, o GPT-6.1 Terra e o GPT-6 Luna, e exige o processamento padrão [8].

## O que muda para quem já usa a API

Para quem usa a API, a mudança que mais exige atenção não está no preço, mas na forma como o histórico da conversa passa a ser tratado. A partir do GPT-6.2, a API Responses descarta o raciocínio já feito pelo modelo quando o desenvolvedor altera mensagens anteriores da conversa, troca de modelo em certos casos ou muda o usuário ou a organização [4]. Segundo a OpenAI, sem esse raciocínio a qualidade da resposta pode cair e o modelo pode gastar mais tokens refazendo trabalho [4]. A recomendação é manter intacto o começo da conversa, o que também preserva o desconto de cache [4].

A segunda mudança é no campo de instruções gerais da API Responses, que agora entra depois do conteúdo enviado pelo usuário [4]. Para que instruções fixas continuem aproveitando o cache, a empresa orienta colocá-las numa mensagem de desenvolvedor no início da entrada [4].

O guia de migração traz outros ajustes. O uso de ferramentas exige a API Responses, embora os modelos também funcionem na API Chat Completions [1][4]. Parâmetros como `temperature` e `top_p` devem ser retirados dos pedidos, e a API recusa pedidos com o nível de raciocínio "none"; a sugestão é começar no nível médio [2][4].

Sobre o comportamento, a OpenAI descreve o GPT-6.2 Astra como mais conciso e direto por padrão do que os modelos anteriores, e diz que, quando o pedido é ambíguo, ele pode propor um próximo passo e esperar confirmação [4].

## Limites e o que ainda não se sabe

Nenhum dos dois modelos aceita ajuste fino, e a saída direta de ambos é só texto [2][3]. As páginas consultadas não trazem resultados de testes de desempenho nem comparações de qualidade com as versões anteriores [2][3][4]. Também não informam se nem quando os modelos chegam ao ChatGPT.

A página de anúncio no site da OpenAI não pôde ser consultada, porque bloqueia leitura automática; esta matéria se baseia na documentação oficial para desenvolvedores [1].

## Fontes

1. [Changelog da API da OpenAI](https://developers.openai.com/api/docs/changelog)
2. [GPT-6.2 Astra · documentação do modelo](https://developers.openai.com/api/docs/models/gpt-6.2-astra)
3. [GPT-6.2 Sol · documentação do modelo](https://developers.openai.com/api/docs/models/gpt-6.2-sol)
4. [Using GPT-6.2 · guia de uso e migração](https://developers.openai.com/api/docs/guides/latest-model)
5. [Preços da API da OpenAI](https://developers.openai.com/api/docs/pricing)
6. [GPT-6 Astra · documentação do modelo](https://developers.openai.com/api/docs/models/gpt-6-astra)
7. [GPT-6.1 Sol · documentação do modelo](https://developers.openai.com/api/docs/models/gpt-6.1-sol)
8. [Guia do modo em segundo plano da API](https://developers.openai.com/api/docs/guides/background)
