PROJETO today.ia.br — retomada em chat local (estado em 22/10/2026)

Venho de uma sessão na nuvem. Todo o trabalho dela está no arquivo today-ia-br.zip, que baixei. Leia este texto inteiro antes de agir.

O QUE É
Portal em português só sobre IA, no domínio today.ia.br (já registrado por mim no Registro.br, válido até 22/10/2027). Cripto, bitcoin, bolsa, games e futebol entram apenas quando a notícia envolver IA. Nada de cotação direta. Receita com AdSense. Nada pago neste projeto além do domínio: fontes, hospedagem e ferramentas só em plano gratuito. Um portal em inglês (.ai) só depois, se este for bem.

DECISÕES JÁ TOMADAS (todas minhas)
- Volume: 1 a 2 matérias por dia.
- Produção automática com IA, com aprovação minha antes de publicar. O que eu não aprovar não vai ao ar.
- Travas do gerador: nada sem link da fonte original; somente fontes oficiais (empresas de IA, órgãos públicos, dados abertos); nada de copiar trechos de outros veículos; proibida linguagem de recomendação de investimento ("compre", "venda", "vale a pena investir", "preço-alvo"); aviso "Produzida com IA e revisada antes da publicação" em toda matéria e "Não é recomendação de investimento" quando tocar em cripto ou bolsa.
- Títulos: gancho com trava. Pode número, contraste, consequência e proximidade. Não pode afirmar o que a fonte não diz; "você não vai acreditar", "chocante", "urgente"; maiúsculas ou emojis; esconder o assunto real. O texto sempre entrega o que o título promete.
- Anúncios: bastante espaço, dentro da política do AdSense e do padrão Better Ads. Na matéria: topo 970×250, dois no texto 336×280, lateral fixa 300×600, bloco de 4 patrocinados no fim, âncora no celular. Na inicial: topo, nativo no feed, meio 970×90, bloco patrocinado, âncora no celular.
- Maquete v3 aprovada (pasta maquete/ do zip, com fotos em maquete/fotos). Conceito "redação à vista": fundo quase preto, verde-ácido #c6ff3a como sinal, ciano #6be4ff nos cruzamentos (ia×cripto etc.); fontes Bricolage Grotesque, Martian Mono e Instrument Serif itálico; mapa de atenção do título, linha do dia de 24 horas, assinatura gerada por matéria, trilha da matéria com o ajuste humano visível, radar regulatório do PL 2338/2023 com dados abertos da Câmara.
- Premissa: o visual não pode lembrar o Mall Journal (malljournal.com.br) nem outro site.
- Fontes testadas e gratuitas: RSS da OpenAI (https://openai.com/news/rss.xml) e do Google DeepMind (https://deepmind.google/blog/rss.xml); páginas de notícias da Anthropic e da Meta AI; dados abertos da Câmara (PL 2338/2023 = id 2487262) e do Senado. Faltam umas 10 fontes oficiais a mais (Microsoft, Nvidia, Hugging Face, Mistral, AWS, MCTI, ANPD), a montar com o gerador.

ARQUITETURA PROPOSTA DO GERADOR (sem custo; ainda não construída)
- Redação: tarefa agendada do Claude Code na nuvem, todo dia às 06:00, dentro da minha assinatura. Coleta as fontes, escreve 1 a 2 matérias e abre um pull request por matéria.
- Aprovação: eu leio o pull request no app do GitHub pelo celular; aprovar = merge; corrigir = comentário ou edição. O histórico do git vira a trilha da matéria.
- Publicação: GitHub Actions (cota gratuita) gera o site estático e publica às 08:00 e às 18:00 só o que foi aprovado e já passou do horário.
- Hospedagem: Cloudflare Pages (gratuito, aceita repositório privado), com o DNS do today.ia.br no Cloudflare (gratuito).

PENDÊNCIA DA VEZ (Sonnet · baixo: é git e navegador)
1. Descompactar o today-ia-br.zip em Desktop\Projeto Portal IA\today-ia-br (o LEIA-ME.md dentro dele é o estado completo do projeto).
2. Pelo meu Chrome, criar no GitHub o repositório privado vinigarbot/today-ia-br, sem README nem licença, e liberar o acesso do aplicativo do Claude a ele (github.com/settings/installations).
3. Iniciar o git na pasta, fazer o primeiro commit e enviar ao repositório. Autorizo este primeiro envio.
4. Conferir no GitHub que tudo chegou e me avisar.

DEPOIS
- Gerador: site estático a partir da maquete, travas e fila de aprovação por pull request (Opus · extra).
- Tarefa agendada das 06:00 (só com meu ok, porque roda sozinha).
- Hospedagem no Cloudflare Pages e apontamento do today.ia.br (conta e DNS são meus; deixar o passo a passo pronto).
- Política de privacidade, aviso de não recomendação de investimento e página "Como usamos IA" (Opus · alto).
- Lista completa de fontes oficiais de IA (Opus · alto).
