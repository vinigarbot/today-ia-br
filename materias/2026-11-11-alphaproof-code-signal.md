---
titulo: IA do Google prova em quatro semanas a segurança do código do *Signal*, trabalho que levava anos
linha_fina: O AlphaProof Code, do Google DeepMind, gerou mais de 6 milhões de linhas de prova matemática e deixou só 1% do material para revisão humana.
editoria: ia
assunto: pesquisa
publicar_em: 2026-11-11 08:00
coletada_em: 2026-11-11 06:07
destaque: Segundo a empresa, todo o processo levou quatro semanas, quando tarefas desse porte costumam ocupar equipes de especialistas por anos.
---

O Google DeepMind apresentou em 10 de novembro o AlphaProof Code, um sistema de agentes de IA que, segundo a empresa, provou matematicamente propriedades de segurança do código que roda o protocolo do Signal, a criptografia que protege conversas em aplicativos como o próprio Signal e o Google Messages [1]. O anúncio é assinado pelos pesquisadores Pushmeet Kohli e Swarat Chaudhuri [1].

A técnica usada se chama verificação formal: em vez de testar o programa com exemplos, ela demonstra com rigor matemático que o código faz o que deveria, sem falhas [1]. O Google DeepMind descreve o método como o padrão mais alto de garantia de segurança, mas também como um trabalho difícil e que costuma exigir muita mão de obra especializada [1].

## Como o trabalho foi dividido

O sistema reparte a tarefa como uma equipe de pesquisa faria. Pessoas especialistas, com ajuda de vários modelos de IA, decidem o que precisa ser provado e traduzem as metas de segurança do Signal em especificações matemáticas, todas revisadas por humanos [1]. Depois, agentes movidos pelo Gemini Carbon escrevem as provas em Lean, linguagem de computador feita para conferir demonstrações matemáticas, e produziram mais de 6 milhões de linhas [1].

Na etapa seguinte, os próprios agentes auditaram as provas e apontaram os trechos que mereciam um segundo olhar humano, cerca de 1% do total [1]. O restante é conferido automaticamente pelo Lean, o que permitiu aos especialistas concentrar a revisão onde o julgamento humano faz diferença [1].

Segundo a empresa, todo o processo levou quatro semanas, quando tarefas desse porte costumam ocupar equipes de especialistas por anos [1].

## O que muda em relação ao que já existia

A maior parte das verificações de protocolos criptográficos para no nível do projeto, isto é, confere a ideia, e não o programa que de fato roda nos aparelhos [1]. O Google DeepMind afirma que os agentes foram além e provaram que o código compilado cumpre as propriedades de segurança, como manter as mensagens protegidas antes e depois de um aparelho ser comprometido temporariamente [1]. A empresa lembra que falhas reais muitas vezes ficam justamente nesse intervalo entre o projeto e a implementação [1].

De acordo com o anúncio, é a primeira vez que a IA é usada para verificar formalmente, com essa profundidade, um protocolo criptográfico amplamente usado, e também a primeira vez que a implementação de um protocolo desse tipo é verificada formalmente por qualquer método [1].

Para mostrar que o sistema distingue código correto de código com defeito, os pesquisadores reintroduziram duas falhas reais, já corrigidas no passado, numa cópia isolada do código do Signal [1]. Nos dois casos, o AlphaProof Code produziu uma prova, conferida por máquina, de que a versão com defeito era insegura [1].

O diretor de tecnologia do Signal, Ehren Kret, citado no anúncio, diz que a abordagem amplia o alcance de verificações anteriores, que tratavam de partes menores do código, e que o resultado dá à organização mais confiança nas garantias de privacidade do aplicativo [1].

## Limites e próximos passos

O próprio Google DeepMind afirma que levar a técnica a outros sistemas exige mais pesquisa [1]. A empresa cita como possíveis alvos futuros o software de aparelhos médicos e o de redes de energia, mas não apresenta prazo nem resultado nessas áreas [1].

As especificações do que deveria ser provado foram escritas com participação humana, e a verificação vale para as propriedades escolhidas pelos especialistas [1]. O Google DeepMind informa que vai abrir os arquivos da verificação para uso da comunidade e publicou um artigo técnico com os detalhes [1].

## Fontes

1. [Introducing AlphaProof Code: a breakthrough in verifying complex software at depth — Google DeepMind](https://deepmind.google/blog/introducing-alphaproof-code/)
