# today.ia.br — Estudo de fontes de IA e cripto (22/10/2026)

> **Atualização (22/10, decisão dele):** o portal passou a ser só de IA, sem cotação direta. As fontes de cotação (CoinMarketCap, Mercado Bitcoin, PTAX) saíram do projeto. Ficam as fontes de IA e os dados abertos da Câmara e do Senado. O restante deste estudo fica como registro.

## Resumo das recomendações
1. Cotação de cripto, fonte principal: CoinMarketCap, plano Basic gratuito. Pela página de preços da própria CoinMarketCap, o plano permite uso comercial, com 15.000 créditos por mês e 50 consultas por minuto.
2. Cotação de cripto, segunda fonte para conferência: API pública do Mercado Bitcoin (preço em reais, sem chave de acesso). Termos de uso ainda não lidos.
3. Dólar: PTAX do Banco Central, pelo portal de dados abertos. Fonte oficial e gratuita.
4. Notícias de IA no exterior: feeds RSS da OpenAI e do Google DeepMind. Anthropic e Meta não têm feed: o gerador acompanha a página de notícias de cada uma.
5. Regulação de IA no Brasil: PL 2338/2023, hoje na Câmara dos Deputados (comissão especial), acompanhado pelas APIs de dados abertos da Câmara e do Senado. Fontes oficiais e gratuitas.
6. Descartadas no lançamento: CoinGecko gratuita (sem licença comercial e com atribuição obrigatória; o plano pago começa em cerca de US$ 35 por mês) e Binance (termos de exibição comercial não encontrados).

Custo previsto no lançamento: zero.
Estimativa de uso: o resumo diário do bitcoin e 1 a 2 matérias de cripto por dia pedem poucas dezenas de consultas por dia, abaixo de 1.500 por mês. O limite gratuito da CoinMarketCap é de 15.000 por mês. Premissa: cerca de 50 consultas por dia, contando testes.

## Testes diretos (22/10, depois da liberação da rede)
| Fonte | Resultado |
|---|---|
| CoinMarketCap, página de preços | Plano Basic gratuito: 15.000 créditos por mês e "Commercial use". A página diz que todos os planos, "the free Basic tier included", têm direito de uso comercial. Condição: os dados ficam dentro do próprio produto, sem revenda ou redistribuição como serviço de dados, para usuários finais em uso pessoal. Um site de notícias se enquadra, na minha leitura. Há também uma API pública sem chave, com limite menor. |
| CoinMarketCap, termos comerciais completos | Não lidos: ficam em pro.coinmarketcap.com, domínio ainda bloqueado. |
| Mercado Bitcoin, API v4 | Respondeu sem chave (BTC-BRL: último R$ 410.984,00 em 22/10). Limite geral de 500 consultas por minuto; os endpoints públicos têm limites próprios, entre 1 e 10 por segundo. A documentação técnica não traz termos de uso; eles ficam em www.mercadobitcoin.com.br, ainda bloqueado. |
| Banco Central, PTAX (Olinda) | Respondeu. Dólar de 21/10/2026: compra R$ 5,0270, venda R$ 5,0277. |
| Câmara, dados abertos | Respondeu. PL 2338/2023 tem o identificador 2487262. |
| Senado, dados abertos | Respondeu. |
| OpenAI, RSS | Respondeu: https://openai.com/news/rss.xml |
| Google DeepMind, RSS | Respondeu: https://deepmind.google/blog/rss.xml |
| Anthropic, página de notícias | Respondeu. |
| Meta AI, blog | Respondeu. |

## Termos de uso lidos na íntegra (22/10)

### CoinMarketCap — Commercial Terms of Use (pro.coinmarketcap.com/user-agreement-commercial)
- Licença para um único site ("no more than one website, domain, subdomain"), com dados exibidos a leitores em uso pessoal. Um portal de notícias com anúncios se enquadra: a licença não proíbe anúncios e permite até cobrar dos usuários.
- Atribuição obrigatória e em destaque: "Data provided by CoinMarketCap.com", com link.
- Armazenamento só temporário, o necessário para exibir. Proibido revender ou distribuir os dados fora do site.
- Acima de 100.000 visitantes únicos por mês, a CoinMarketCap pode exigir a licença Enterprise (paga). Como o projeto não terá nada pago, a troca de fonte fica prevista para esse ponto.
- O cadastro pede nome, dados pessoais e "a method of payment". Conferir no cadastro se o plano gratuito exige cartão; se exigir, decisão dele.
- Foro: Abu Dhabi Global Market.

### Mercado Bitcoin — Termo de Uso da API (www.mercadobitcoin.com.br/politicas-termo-api)
- Licença gratuita, revogável e intransferível.
- Proíbe "vender, sublicenciar, arrendar ou alugar ou emprestar a API ou usá-la para a prestação de serviços comerciais". Um portal com AdSense pode ser lido como serviço comercial.
- O Mercado Bitcoin pode mudar, limitar, cobrar ou encerrar a API sem aviso.
- Leitura: o uso no portal fica em zona cinzenta, mesmo só para conferência interna. Recomendação: pedir autorização por e-mail antes de usar; até a resposta, não publicar números do Mercado Bitcoin.

## Limite deste estudo
O ambiente na nuvem bloqueia a leitura direta das páginas (só a busca funciona). Os números vieram de resultados de busca, em parte de páginas das próprias empresas e em parte de comparativos de terceiros. Antes de o gerador entrar no ar, os termos de uso de cada fonte precisam ser lidos na íntegra.

## Fontes por tema

### Cripto e bitcoin
| Fonte | Custo | Limite | Uso comercial | Situação |
|---|---|---|---|---|
| CoinMarketCap Basic | Gratuito | 15.000 créditos/mês; 50/min | Permitido, segundo a página de preços; proibido revender os dados como serviço | Ler os termos completos |
| Mercado Bitcoin API v4 (dados públicos) | Gratuito, sem chave | Não informado | Não informado | Ler a documentação e os termos |
| CoinGecko Demo | Gratuito | Cerca de 10.000 créditos/mês | Não, segundo comparativos; exige atribuição | Descartada no lançamento |
| CoinGecko Basic | Cerca de US$ 35/mês (US$ 29 no plano anual) | 100.000 créditos/mês | Sim, segundo comparativo | Reserva, se a CoinMarketCap falhar |
| Binance | Gratuito | — | Termos não encontrados | Descartada no lançamento |

### Dólar
| Fonte | Custo | Observação |
|---|---|---|
| Banco Central — PTAX (dados abertos, série 1 do SGS para o dólar de venda, a confirmar) | Gratuito | Fonte oficial; boletim de fechamento é a média dos boletins do dia |

### IA — exterior
| Fonte | Forma de coleta |
|---|---|
| OpenAI | RSS: https://openai.com/news/rss.xml (segundo diretório de terceiros; testar) |
| Google DeepMind | RSS: https://deepmind.google/blog/rss.xml (segundo diretório de terceiros; testar) |
| Anthropic | Sem RSS; acompanhar a página de notícias |
| Meta AI | Sem RSS; acompanhar a página de notícias |

### IA — Brasil
| Fonte | Observação |
|---|---|
| PL 2338/2023 (marco legal da IA) | Senado encerrou a tramitação e enviou à Câmara em 17/03/2025; em análise por comissão especial na Câmara; sem votação final encontrada até junho de 2026 |
| Dados abertos da Câmara e do Senado | Oficiais e gratuitos; endpoints a confirmar |

## Pontos para decisão
1. Aprovar o conjunto gratuito (CoinMarketCap + Mercado Bitcoin + Banco Central + RSS e páginas oficiais) para o lançamento.
2. Deixar a CoinGecko paga como reserva, sem contratar agora.

## Fontes consultadas
- CoinMarketCap, página de preços da API: https://coinmarketcap.com/api/pricing
- CoinMarketCap Academy, comparativo de planos gratuitos 2026: https://coinmarketcap.com/academy/article/best-free-crypto-api-in-2026-free-tier-comparison
- CoinGecko, preços e limites (terceiro): https://apicostcalc.com/coingecko.html
- Comparativo CoinGecko × CoinStats: https://www.codex.io/blog/coingecko-api-vs-coinstats-api
- Comparativo de APIs financeiras gratuitas: https://qveris.ai/guides/free-financial-api-comparison
- Mercado Bitcoin, diretório de APIs: https://publicapis.io/mercadobitcoin-api
- Mercado Bitcoin, biblioteca pymbtc: https://pypi.org/project/pymbtc
- Banco Central, dados abertos de câmbio: https://dadosabertos.bcb.gov.br/is/dataset/taxas-de-cambio-todos-os-boletins-diarios
- PTAX, definição e cálculo: https://calculacentro.com/indices/dolar
- Feeds RSS de IA (terceiro): https://feeder.co/knowledge-base/rss-content/ai-news-rss-feeds/
- Senado, PL 2338/2023: https://www25.senado.leg.br/web/atividade/materias/-/materia/157233
- Teletime, panorama regulatório de IA (jun/2026): https://teletime.com.br/03/06/2026/panorama-regulatorio-inteligencia-artificial/
- Binance, documentação da API: https://developers.binance.com/en/docs/products/convert/Introduction
