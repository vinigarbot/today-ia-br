# Matérias do today.ia.br — formato

Uma matéria por arquivo, nesta pasta, com o nome `AAAA-MM-DD-assunto-em-minusculas.md`. A data do nome é a do dia da publicação, e o resto vira o endereço: `today.ia.br/assunto-em-minusculas/`.

Cada matéria chega por pull request. Aprovar é fazer o merge, e o que não for aprovado não vai ao ar. O site é gerado às 08:00 e às 18:00 (horário de Brasília), sempre a partir da `main`, e só publica a matéria aprovada cujo `publicar_em` já passou.

## Modelo

```markdown
---
titulo: Modelos de *raciocínio* custam mais por pergunta e, mesmo assim, saem mais baratos. Entenda a conta
linha_fina: Custos por tarefa, tempo de resposta e os pontos em que esses modelos já substituem fluxos manuais.
editoria: ia
assunto: empresas
publicar_em: 2026-10-23 08:00
coletada_em: 2026-10-23 06:02
destaque: O ganho vem de reduzir a revisão manual, não de eliminar a pessoa do processo.
---

Primeiro parágrafo, com a chamada da fonte no fim da afirmação [1].

## Intertítulo

Outro parágrafo [2][3].

:::dados Tempo relativo por tarefa · teste do fornecedor [3]
Modelo padrão | 100
Raciocínio rápido | 74
:::

- Item de lista, também com fonte [2]

## Fontes

1. [Título do documento oficial](https://openai.com/...)
2. [Título do comunicado](https://www.gov.br/anpd/...)
3. [Título da página de preços](https://...)
```

## Campos do cabeçalho

| Campo | O quê |
|---|---|
| `titulo` | Título. Uma palavra entre `*asteriscos*` sai no itálico verde da marca |
| `linha_fina` | Uma frase abaixo do título; também é a descrição para o Google |
| `editoria` | `ia`, `ia-cripto`, `ia-bolsa`, `ia-games`, `ia-futebol` ou `regulacao` |
| `assunto` | Obrigatório em `ia` e `regulacao`: vira o caminho `~/ia/assunto`. Minúsculas, sem acento, hífen no lugar de espaço |
| `publicar_em` | Dia e hora de entrada no ar, no horário de Brasília. Use 08:00 ou 18:00, os horários em que o site é gerado |
| `coletada_em` | Quando as fontes foram consultadas |
| `destaque` | Opcional: uma frase igual à do próprio texto, repetida em destaque |

## Travas (o gerador confere; com erro, a matéria não passa)

- Toda matéria tem a seção `## Fontes`, numerada a partir de 1, só com `https://` e só com domínio da lista de fontes oficiais (`gerador/fontes_oficiais.json`).
- Todo parágrafo, lista e quadro de dados tem pelo menos uma chamada `[n]`; toda chamada tem a sua fonte e toda fonte é chamada no texto. Link solto no texto não passa.
- Título e linha fina sem "você não vai acreditar", "chocante", "urgente" e as irmãs listadas em `gerador/travas.py`, sem emoji e sem palavra em maiúsculas (siglas curtas como IA, GPT e ANPD passam). Número que está no título tem de estar no texto.
- Nenhuma linguagem de recomendação de investimento ("compre", "vale a pena investir", "preço-alvo", "hora de vender" e afins). Em matéria que toca cripto ou bolsa, "venda", "vender", "comprar" e "pode subir" geram alerta para a revisão.
- Nenhum trecho entre aspas com mais de 25 palavras: matéria própria, nunca cópia.
- Os avisos "Produzida com IA e revisada antes da publicação" (toda matéria) e "Não é recomendação de investimento" (quando toca cripto ou bolsa) são colocados pelo próprio gerador.

## O que só a leitura humana confere (lista do pull request)

- O título afirma só o que a fonte diz e não esconde o assunto real.
- O texto entrega o que o título promete.
- As fontes abertas dizem o que o texto atribui a elas.

## Trilha da matéria

A trilha que o leitor vê sai do histórico do git: o rascunho é o primeiro commit da redação (que sempre leva a linha `Co-Authored-By: Claude`), os ajustes humanos são as edições feitas por você no GitHub, e a aprovação é o merge feito por você. Para a trilha funcionar, o merge tem de ser do tipo "Create a merge commit" (o repositório só aceita esse tipo).
