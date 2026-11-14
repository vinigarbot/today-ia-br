---
titulo: Diante de pergunta com premissa errada, modelos de IA focam no problema *real* em no máximo 41% das respostas
linha_fina: Teste da Ai2 com 8.115 perguntas mostra que Claude, GPT, Gemini, Qwen e DeepSeek reconhecem o conselho útil, mas tendem a responder ao pedido equivocado do usuário.
editoria: ia
assunto: pesquisa
publicar_em: 2026-11-14 08:00
coletada_em: 2026-11-14 06:06
destaque: Citar uma solução, porém, não significa dar destaque a ela.
---

A Ai2 divulgou nesta sexta-feira (13) o XYBench, um teste de referência com 8.115 perguntas que avalia como assistentes de IA respondem quando o próprio pedido do usuário se apoia num equívoco. O anúncio saiu na página da organização no Hugging Face, com artigo científico, dados e código, e o trabalho foi feito com pesquisadores da Carnegie Mellon, da Nvidia e da Johns Hopkins [1].

Segundo a Ai2, os cinco modelos avaliados, Claude Sonnet 4.6, GPT-5, Gemini 3.1 Pro, Qwen3.5-9B e DeepSeek-V4 Pro, costumam até mencionar uma saída para o problema verdadeiro, mas concentram a resposta no caminho equivocado que o usuário trouxe. Em comparação com respostas escritas por pessoas, todos foram menos propensos a desviar o usuário desse caminho [1]. A organização informa que o trabalho recebeu o prêmio de melhor artigo de recurso na conferência EMNLP 2026 [1].

## O que é o "problema XY"

O nome vem de uma situação conhecida em fóruns de programação: a pessoa quer alcançar um objetivo (X), supõe que certo método (Y) vai funcionar e pede ajuda só com esse método. O exemplo da Ai2 é o de quem pergunta como engrossar uma cobertura que escorre do bolinho, quando o problema real é que o bolinho ainda está quente demais [1].

Para montar o teste, a equipe reuniu perguntas reais de fóruns e gerou outras a partir de guias do WikiHow. Em cada uma, identificou o pedido declarado e o objetivo que dá para deduzir pelo contexto, e descartou os casos em que responder ao pé da letra já bastaria [1]. As perguntas de fórum usaram como referência as respostas mais bem avaliadas pelos próprios usuários; as do WikiHow foram criadas com o Claude Sonnet 4.5 e depois refinadas [1].

:::dados Perguntas do XYBench por origem [1]
WikiHow (geradas) | 6272
Stack Overflow | 1557
Stack Exchange | 184
Curadas à mão | 102
:::

## Os resultados

O teste mede três coisas: se a resposta traz solução para o pedido declarado e para o objetivo real, em qual dos dois ela põe o foco e se ela desencoraja o caminho errado [1]. Nas perguntas do Stack Overflow, soluções para o pedido declarado apareceram em 75% a 86% das respostas, contra 59% a 71% para o objetivo real [1].

Citar uma solução, porém, não significa dar destaque a ela. Ainda no Stack Overflow, os modelos se concentraram principalmente no objetivo real em apenas 35% a 41% das respostas, ou seja, no máximo 41%, e no pedido declarado em 47% a 57%; no restante, dividiram o peso entre os dois [1].

A equipe também testou o efeito de entregar ao modelo, junto com a pergunta, o pedido e o objetivo já explicitados. No caso do Sonnet 4.6, a presença de solução para o objetivo real subiu de 59% para 67%, mas a taxa de identificação do equívoco caiu de 47% para 34%. Mesmo assim, nenhum modelo alcançou as respostas humanas nesse quesito [1].

## Sabem reconhecer, mas não escrevem

Num outro experimento, os mesmos cinco modelos e mais o GPT-4.1 receberam cada pergunta com duas respostas prontas, uma presa ao pedido literal e outra que explicava o equívoco. No Stack Overflow, todos escolheram a segunda em 71% a 84% dos casos [1]. Para a Ai2, a diferença em relação aos 35% a 41% das respostas escritas pelos modelos mostra uma distância entre reconhecer o conselho útil e produzi-lo, algo que um teste de múltipla escolha sozinho não captaria [1].

## Limites

A avaliação automática foi feita pelo Claude Sonnet 4.5 no papel de juiz. Dois revisores humanos conferiram 500 respostas, e a concordância com o juiz variou de 97,5% a 100% na presença de solução, de 84,6% a 93,3% na identificação do equívoco e de 74,2% a 79,8% no foco da resposta [1].

O XYBench cobre só perguntas em inglês, a maioria sobre problemas práticos, e cada modelo deu uma única resposta por pergunta, sem conversa de várias rodadas. A extensão para outros idiomas e culturas, o que incluiria o português, é apontada pela própria Ai2 como trabalho futuro [1].

## Fontes

1. [XYBench: Helping with the problem behind the question (Ai2, no Hugging Face)](https://huggingface.co/blog/allenai/xybench)
