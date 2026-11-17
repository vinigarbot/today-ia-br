---
titulo: Na estreia no MLPerf, Vera Rubin da Nvidia rende até o *dobro* por GPU em treino de IA
linha_fina: Nvidia diz que a nova plataforma superou a geração GB300 em todos os testes de treino e, num resultado provisório, entregou mais de 10 vezes mais trabalho de agentes por watt.
editoria: ia
assunto: infraestrutura
publicar_em: 2026-11-17 08:00
coletada_em: 2026-11-17 06:07
destaque: A comparação de até 2 vezes vale para o melhor caso, e o resultado com o Kimi K3 é classificado pela empresa como provisório.
---

A Nvidia divulgou nesta segunda-feira (16) os primeiros resultados do Vera Rubin, sua nova plataforma de computação para IA, no MLPerf, conjunto de testes de desempenho usado pela indústria para comparar sistemas de treino e de execução de modelos [1]. Segundo a empresa, o sistema Vera Rubin NVL72 entregou até 2 vezes mais desempenho por GPU que o GB300 NVL72, da geração anterior, na rodada de treino MLPerf Training v6.1 [1].

A Nvidia afirma ainda que foi a única participante com resultados em todos os testes dessa rodada, que incluem grandes modelos de linguagem, geração de imagens, sistemas de recomendação e pós-treino por aprendizado por reforço [1].

## O que os números mostram

O MLPerf Training mede quanto tempo um sistema leva para treinar um modelo até um nível de precisão definido [1]. No teste com o DeepSeek-V3, a Nvidia diz que passou de 256 para 1.024 GPUs Vera Rubin com cerca de 97% de eficiência: com quatro vezes mais chips, o tempo de treino caiu de 16 minutos para cerca de 4 [1].

:::dados Tempo de treino no teste DeepSeek-V3, em minutos · Vera Rubin NVL72 [1]
256 GPUs | 16
1.024 GPUs | 4
:::

Esse tipo de medida importa porque somar GPUs só acelera o treino quando elas conseguem trabalhar juntas sem perder rendimento [1]. A empresa também rodou o mesmo teste com 10.240 GPUs da geração GB300, a maior escala da rodada; a Microsoft, pelo Azure, chegou ao mesmo número de GPUs com sistemas GB200 [1].

Na execução de modelos, a Nvidia estreou no MLPerf Endpoints, teste que usa tarefas reais de programação e de fluxos de trabalho de empresas feitas por agentes de IA e confere se as tarefas foram concluídas corretamente [1]. Segundo a empresa, o Vera Rubin ficou à frente em todos os testes de agentes dessa rodada [1].

O número mais alto vem do Kimi K3, modelo aberto voltado a agentes: nesse caso, o Vera Rubin NVL72 teria entregado mais de 10 vezes a vazão por watt do GB300 NVL72, mantendo a mesma velocidade de resposta [1]. A conta por watt é a que a Nvidia destaca porque centros de dados de IA são limitados pela energia disponível, e mais tokens por watt significam mais agentes atendidos com a mesma infraestrutura [1].

## Novo chip para simulação científica

Na mesma conferência, a SC26, a Nvidia anunciou o Rubin HPC, uma GPU da família Vera Rubin voltada a simulação e processamento de dados em ciência, engenharia e análise [2]. A empresa diz que o chip terá mais de 50 mil núcleos CUDA, número que chama de recorde para uma única GPU, e um recurso para acelerar o acesso a dados esparsos [2]. A previsão de disponibilidade é 2028 [2].

## Limites e o que ainda não se sabe

Os números desta matéria são os que a própria Nvidia apresentou ao divulgar suas submissões [1]. A comparação de até 2 vezes vale para o melhor caso, e o resultado com o Kimi K3 é classificado pela empresa como provisório [1]. O comunicado não informa preço nem data de entrega dos sistemas Vera Rubin, nem traz a comparação com os resultados de outros fabricantes de chips [1].

Segundo a Nvidia, 20 organizações enviaram resultados de treino com sua plataforma, entre elas Google Cloud, Oracle, Dell e a Universidade da Flórida [1]. A empresa afirma que o desempenho do Vera Rubin deve continuar subindo com atualizações de software [1].

## Fontes

1. [NVIDIA Sweeps MLPerf Training and Endpoints as Vera Rubin Debuts With Leading Performance](https://blogs.nvidia.com/blog/mlperf-training-endpoints-vera-rubin/)
2. [NVIDIA Announces Rubin HPC — A New GPU to Accelerate Agents for Science, Engineering and Analytics](https://blogs.nvidia.com/blog/rubin-hpc/)
