---
titulo: Google leva o Gemini 4 *Hydrogen* à busca de todos; em programação, nota passa do triplo da anterior
linha_fina: Modelo rápido da família Gemini 4 chega à Busca, ao app e à API, custa US$ 1,50 por milhão de tokens de entrada e, segundo o Google, erra menos ao inventar informações.
editoria: ia
assunto: modelos
publicar_em: 2026-11-13 08:00
coletada_em: 2026-11-13 06:07
destaque: Na Busca, o Hydrogen passou a valer para todos os usuários, no mundo inteiro, no que o Google chama de a maior troca de modelo da história do serviço.
---

O Google lançou em 12 de novembro o Gemini 4 Hydrogen, versão mais rápida e mais barata da família Gemini 4, pensada para tarefas do dia a dia, programação e agentes, segundo anúncio assinado por Koray Kavukcuoglu, vice-presidente sênior do Google DeepMind [1]. Com ele, a empresa leva o Gemini 4 a todos os níveis de acesso: Google AI Studio, API do Gemini, Gemini for business, aplicativo Gemini e Busca [1].

## O que muda para quem usa

Na Busca, o Hydrogen passou a valer para todos os usuários, no mundo inteiro, no que o Google chama de a maior troca de modelo da história do serviço [2]. A empresa diz que a ferramenta entende melhor perguntas com várias partes, erros de digitação e pedidos muito específicos, e que as respostas trazem mais imagens, tabelas comparativas e ferramentas montadas para cada consulta [2]. A melhora, segundo o texto, vale para todos os idiomas aceitos hoje pelo Modo IA [2].

O Google também diz ter ampliado a técnica de desdobrar uma pergunta em várias buscas simultâneas sobre os subtemas, o que, segundo a empresa, leva o usuário a um conjunto maior de sites do que antes [2].

No aplicativo Gemini, o modelo aparece na lista de escolha de modelos [1]. Quem usa a versão gratuita recebe o Hydrogen pela seleção automática, quando o sistema avalia que ele é o modelo adequado para o pedido [1]. Assinantes pagos dos planos Google AI Pro e Ultra podem usá-lo também no Google Antigravity, ambiente de programação da empresa, e no Gemini do Google Planilhas [1].

## Preço e desempenho

Na API, o preço é o mesmo em toda a janela de contexto de 1 milhão de tokens: US$ 1,50 por milhão de tokens de entrada e US$ 7,50 por milhão de tokens de saída [1]. Tokens são os pedaços de texto que os modelos processam e que servem de base para a cobrança. O modelo aceita até 1 milhão de tokens de saída e tem quatro níveis de raciocínio, do baixo ao novo nível "xhigh", para equilibrar qualidade, tempo de resposta e custo [1].

O Google o apresenta como sucessor do Gemini 3.8 Flash [1]. Na configuração padrão, segundo a empresa, o Hydrogen termina tarefas 2,5 vezes mais rápido que o 3.8 Flash e reduz em mais de cinco vezes as afirmações inventadas [1].

:::dados Acerto no Terminal-Bench 4.1, em % · Google DeepMind [1]
Gemini 4 Hydrogen | 57
Gemini 3.8 Flash | 18,2
:::

No índice de inteligência da Artificial Analysis, o Hydrogen marcou 51 pontos no nível padrão, um a mais que o Gemini 4 Argon, um dos modelos mais avançados da própria empresa, e 54 no nível mais alto [1]. Parceiros que testaram o modelo antes do lançamento viram tarefas rodarem de 2 a 2,8 vezes mais rápido, com uso de tokens de 12% a 23% menor que o do 3.8 Flash, de acordo com o Google [1].

## Uso combinado com modelos maiores

A empresa sugere usar o Hydrogen sozinho ou como executor ao lado do Gemini 4 Carbon e do Argon, que ficariam com as decisões mais difíceis [1]. Para automatizar essa divisão, lançou o Orchestrator, recurso do Antigravity que alterna entre modelos na mesma sessão [1]. No teste Terminal-Bench 4.0, o recurso chegou perto da taxa de sucesso do Carbon, com consumo de cota 24% menor e conclusão 19% mais rápida, em média [1]. Para desenvolvedores, o modelo está disponível na API pelo AI Studio e pelo Android Studio [3].

## Segurança e o que ainda não se sabe

O Google afirma que o Hydrogen reduz em até 81% os casos em que um agente vai além do que foi pedido e é até duas vezes menos propenso a contornar limites de permissão diante de tarefas bloqueadas [1]. Num teste interno de honestidade de agentes, a taxa foi de 96,7%, e, contra ataques de injeção indireta de instruções, o modelo se mostrou mais de 2,3 vezes mais resistente no teste da Gray Swan [1].

Os números de desempenho e de segurança vêm do próprio Google e de testes escolhidos pela empresa [1]. O anúncio não informa o preço do Gemini 3.8 Flash para comparação direta de custo, nem dá números de qualidade das respostas na Busca [1][2].

## Fontes

1. [Introducing Gemini 4 Hydrogen](https://deepmind.google/blog/introducing-gemini-4-hydrogen/)
2. [Google Search gets a major upgrade with Gemini 4 Hydrogen](https://blog.google/products-and-platforms/products/search/gemini-4-hydrogen-search-upgrade/)
3. [Gemini 4 Hydrogen: everyday coding and agentic workflows for developers](https://blog.google/innovation-and-ai/technology/developers-tools/build-with-gemini-4-hydrogen/)
