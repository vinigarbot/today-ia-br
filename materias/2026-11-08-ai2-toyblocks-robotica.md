---
titulo: Ai2 abre simulador de robótica com blocos; descrições escritas pela própria IA elevaram o acerto de 24% para 63%
linha_fina: O ToyBlocks gera tarefas e demonstrações para treinar braços robóticos em simulação e vem com dados, modelos e código abertos; os testes também expõem os limites atuais.
editoria: ia
assunto: pesquisa
publicar_em: 2026-11-08 08:00
coletada_em: 2026-11-08 06:07
destaque: A Ai2 avalia que a capacidade desses modelos de generalizar continua longe de ser um problema resolvido.
---

A Ai2 lançou nesta sexta-feira (6) o ToyBlocks, um ambiente de simulação aberto para estudar como robôs aprendem. O cenário é de propósito simples: um braço robótico e blocos de madeira sobre uma mesa, que o robô precisa empurrar, virar, girar e empilhar. O anúncio saiu na página da organização no Hugging Face [1].

O ToyBlocks é o primeiro de uma família que a Ai2 chama de *FoundationWorlds*: mundos simulados e controlados, acompanhados de ferramentas que criam tarefas e demonstrações de treino de forma automática e de métricas para medir o comportamento do robô. A ideia, segundo a organização, é dar à robótica algo parecido com uma placa de laboratório, em que dá para mudar uma condição de cada vez, repetir o teste e descobrir por que algo falhou [1].

## O que o pacote traz

As demonstrações são gravações de um robô simulado cumprindo tarefas, produzidas sem teleoperação, em que uma pessoa controla o braço a distância. Habilidades curtas, como virar um bloco sem pegá-lo, são aprendidas por aprendizado por reforço no Isaac Lab, ferramenta aberta da Nvidia; um planejador encadeia essas habilidades para resolver tarefas maiores. Segundo a Ai2, centenas de planos rodam em paralelo numa única placa de vídeo, a até 24 vezes a velocidade do tempo real [1].

Os blocos têm letras e figuras nas faces, o que permite tarefas de busca e ordenação: às vezes o robô precisa girar um bloco para ver a face escondida antes de decidir onde colocá-lo [1].

A primeira leva de dados tem 85.336 demonstrações longas, quase 1,6 mil horas de execução e 144 milhões de quadros. Também foram liberados o código de treino e de avaliação, os geradores de tarefas e dois modelos treinados, um baseado no Molmo 2 e outro no ManiFlow. A Ai2 diz mirar uma segunda versão, com mais dados e mais habilidades, em algumas semanas [1].

## O que os testes mostraram

Num dos experimentos, um agente com o Claude Opus 5.5 controlou o robô por meio de ferramentas conectadas pelo MCP, padrão para ligar aplicações de IA a ferramentas externas. Em 30 tarefas clássicas de empilhar blocos, resolveu todas, tanto com descrições em texto quanto olhando imagens da câmera a cada passo [1].

Na tarefa de achar blocos e soletrar palavras de três letras, em que metade dos cenários não tinha todas as letras e o agente devia dizer que a tarefa era impossível, a taxa de acerto foi de 63%. Os erros vieram sobretudo de confundir letras parecidas (13%) e de deixar uma letra na orientação errada (15%) [1].

Quando o próprio agente fez experimentos para entender suas habilidades e reescreveu as descrições delas, o acerto subiu de 24%, com as descrições originais, para 63%, acima dos 36% obtidos com descrições escritas por um especialista humano [1].

:::dados Taxa de acerto do agente conforme a descrição das habilidades, em % [1]
Descrições originais | 24
Escritas por especialista humano | 36
Escritas pelo próprio agente | 63
:::

No mundo físico, com um braço Franka FR3, as habilidades do ManiFlow treinadas só em simulação tiveram acerto parecido com o da simulação: 81,1% contra 80,0%. O sistema completo, com o Molmo 2 planejando e o ManiFlow executando, soletrou as palavras em 50% dos episódios reais (15 de 30) e em 55,5% dos simulados [1].

## Limites e o que ainda não se sabe

A própria Ai2 ressalva que são necessários mais testes para ter confiança estatística nos resultados com o robô real, feitos em apenas 30 cenários e na configuração mais fácil, com as letras visíveis e na posição certa [1].

Nos testes de generalização, modelos que transformam instruções e imagens em ações do robô, conhecidos pela sigla VLA, foram mal nos resultados iniciais quando os blocos apareciam fora da região vista no treino, apesar do pré-treinamento em grandes bases. A Ai2 avalia que a capacidade desses modelos de generalizar continua longe de ser um problema resolvido [1].

O aprendizado por reforço totalmente integrado ainda não faz parte do pacote atual e deve chegar numa próxima versão. Entre os planos estão manipulação com dois braços e mãos robóticas com sensores de força e de toque [1].

## Fontes

1. [ToyBlocks: A controlled world for robot learning and evaluation (Ai2, no Hugging Face)](https://huggingface.co/blog/allenai/toyblocks)
