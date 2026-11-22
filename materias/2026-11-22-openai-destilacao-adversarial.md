---
titulo: OpenAI diz ter reduzido de 54,0% para 0,2% o sucesso de ataques que extraem o *raciocínio* do Astra
linha_fina: A empresa detalhou como tenta impedir que outros desenvolvedores treinem modelos com respostas e raciocínio dos seus sem autorização, e por que isso pesa na segurança cibernética.
editoria: ia
assunto: seguranca
publicar_em: 2026-11-22 08:00
coletada_em: 2026-11-22 06:06
destaque: O problema apontado pela OpenAI é que o modelo copiado pode herdar as capacidades sem herdar as travas de segurança do original.
---

A OpenAI publicou nesta sexta-feira (20) um relatório sobre como detecta e bloqueia a chamada destilação adversarial: o uso não autorizado das respostas de um modelo de ponta para treinar outro modelo com capacidades parecidas [1]. Segundo a empresa, num teste interno com ataques automatizados, a taxa média de sucesso das tentativas de extrair o raciocínio protegido de uma conversa anterior caiu de 54,0% no GPT-6 Astra, com as proteções originais, para 0,2% no GPT-6.2 Astra, com as proteções novas [1].

## Por que a empresa trata o tema como segurança

Destilação é uma técnica comum de aprendizado de máquina, em que um modelo aprende com dados produzidos por outro, sejam respostas, raciocínio ou avaliações sobre quais respostas são melhores [1]. O problema apontado pela OpenAI é que o modelo copiado pode herdar as capacidades sem herdar as travas de segurança do original [1]. A empresa cita como áreas mais sensíveis a segurança cibernética e a biologia, em que a mesma habilidade que ajuda quem defende um sistema pode ajudar quem ataca [1].

O foco das defesas é o raciocínio protegido, ou seja, as etapas intermediárias que o modelo gera internamente antes de responder, conhecidas como cadeia de pensamento [1]. De acordo com o relatório, esses registros podem conter informação ausente da resposta final, o que os torna dados de treino especialmente valiosos para um terceiro [1].

Para medir o risco, a OpenAI treinou modelos "alunos" a partir de trajetórias de modelos do nível Astra em tarefas de programação e de defesa cibernética [1]. Depois do ajuste fino supervisionado, o aluno treinado com o raciocínio exato em geral superou o que aprendeu apenas com resumos do raciocínio [1]. Depois de uma etapa de aprendizado por reforço, a vantagem do raciocínio exato se manteve só no maior orçamento de processamento testado; nos orçamentos menores, o aluno treinado com resumos foi melhor [1].

## O que muda nos modelos e na API

As defesas descritas funcionam em dois níveis: em cada pedido, com treinamento do modelo para recusar tentativas de extração, classificadores que examinam entradas e saídas e controles na API; e no conjunto de contas, com investigação de campanhas coordenadas [1]. Os classificadores de saída também verificam os argumentos enviados a ferramentas, porque o modelo pode vazar o raciocínio ali sem que ele apareça na resposta [1].

No GPT-6.2 Astra e no GPT-6.2 Sol, o raciocínio protegido fica atrelado ao histórico da conversa que o produziu [1]. Se uma mensagem anterior for reescrita, a API descarta o raciocínio gerado depois dela, comportamento que já consta da documentação para desenvolvedores [1][2]. Para quem integra a API, isso tem custo: a documentação avisa que, sem esse raciocínio, o modelo pode ter de refazer etapas, o que pode aumentar o consumo de tokens, o gasto e o tempo de resposta, e recomenda apenas acrescentar mensagens, sem editar o histórico [2]. A empresa diz ainda que modelos de famílias mais antigas, com proteções mais fracas, não conseguem ler o raciocínio dos dois modelos novos [1].

:::dados Taxa de sucesso de ataques de extração, em % · teste interno da OpenAI [1]
Pedido anterior, GPT-6 Astra (proteções originais) | 54,0
Pedido anterior, GPT-6.2 Astra (proteções novas) | 0,2
Pedido atual, GPT-6 Astra (proteções originais) | 22,9
Pedido atual, GPT-6.2 Astra (proteções novas) | 0,9
:::

A OpenAI informou que passou a aplicar parte dessas melhorias também ao GPT-6 Astra [1]. Sobre as campanhas, a empresa afirma que suas ações semanais contra elas atingiram de milhares a dezenas de milhares de contas, com aumento significativo no último verão do hemisfério norte [1].

## Limites e o que ainda não se sabe

Os números vêm de avaliações internas da própria OpenAI, feitas com atacantes automatizados e agregadas entre seis modelos atacantes, num ambiente que, segundo a empresa, imita o uso real [1]. Não há, no relatório, verificação independente desses resultados [1]. A empresa também diz que continuará estudando quanto de capacidade se transfere com outros modelos alunos e outras receitas de treinamento, o que indica que a medição do risco ainda está em curso [1].

Para outros desenvolvedores, o relatório recomenda proteger o raciocínio em toda a interação, guardar ataques bem-sucedidos como testes de regressão e combinar a defesa em cada pedido com a investigação de campanhas [1]. A OpenAI afirma ainda apoiar, nos Estados Unidos, projetos de lei que deem ao governo instrumentos para identificar e punir agentes estrangeiros que extraiam capacidades de modelos americanos [1].

## Fontes

1. [Combatting adversarial distillation — OpenAI](https://openai.com/index/combatting-adversarial-distillation)
2. [Keep prefix unchanged — documentação da API da OpenAI](https://developers.openai.com/api/docs/guides/keep-prefix-unchanged)
