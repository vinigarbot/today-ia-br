"""Site gerado de ponta a ponta a partir do repositório de exemplo (hora fixa: 23/10/2026 13:40 de Brasília)."""

import io
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "gerador"))
sys.path.insert(0, str(RAIZ / "testes"))

import gerar_site  # noqa: E402
from comum import BRASILIA, ler_hora  # noqa: E402
from montar_exemplo import REDACAO, TRAILER, git, montar as montar_repo  # noqa: E402

AGORA = "2026-10-23 13:40"


def gerar(repo: Path, saida: Path, *extra: str) -> tuple[int, str]:
    texto = io.StringIO()
    with redirect_stdout(texto):
        codigo = gerar_site.main(["--raiz", str(repo), "--saida", str(saida), "--agora", AGORA, "--offline", *extra])
    return codigo, texto.getvalue()


def ler(saida: Path, caminho: str) -> str:
    return (saida / caminho).read_text(encoding="utf-8")


class SiteDeExemplo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        base = Path(cls.tmp.name)
        cls.repo = montar_repo(base / "repo")
        cls.site, cls.previa = base / "site", base / "previa"
        cls.codigo_site, cls.saida_site = gerar(cls.repo, cls.site)
        cls.codigo_previa, _ = gerar(cls.repo, cls.previa, "--rascunhos")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_gera_sem_erro(self):
        self.assertEqual(self.codigo_site, 0, self.saida_site)
        self.assertEqual(self.codigo_previa, 0)
        self.assertIn("5 publicada(s), 1 agendada(s) para hoje", self.saida_site)

    def test_agendada_nao_tem_pagina_mas_aparece_na_inicial(self):
        self.assertFalse((self.site / "fundos-cripto-decisoes-ia").exists())
        self.assertNotIn("fundos-cripto-decisoes-ia", ler(self.site, "sitemap.xml"))
        self.assertNotIn("Fundos de cripto", ler(self.site, "feed.xml"))
        inicial = ler(self.site, "index.html")
        self.assertIn("hoje · 18:00 · agendada", inicial)
        self.assertIn("Revisada 07:52 · sai às 18:00", inicial)
        self.assertNotIn('href="/fundos-cripto-decisoes-ia/"', inicial)

    def test_publicadas_tem_pagina_sitemap_e_feed(self):
        for slug in ("agentes-usam-computador", "modelos-raciocinio-custo", "clubes-ia-lesoes", "dialogos-games-ia", "marco-legal-camara"):
            with self.subTest(slug):
                self.assertTrue((self.site / slug / "index.html").exists())
                self.assertIn(f"/{slug}/", ler(self.site, "sitemap.xml"))
                self.assertIn(f"/{slug}/", ler(self.site, "feed.xml"))

    def test_destaque_da_inicial_e_a_mais_recente(self):
        inicial = ler(self.site, "index.html")
        self.assertIn('<h1><a href="/agentes-usam-computador/">', inicial)
        self.assertIn('class="mapa"', inicial)

    def test_aviso_de_ia_em_toda_materia(self):
        for pagina in self.previa.glob("*/index.html"):
            if pagina.parent.name in gerar_site.EDITORIAS or pagina.parent.name in ("assets", "dados"):
                continue
            with self.subTest(pagina.parent.name):
                self.assertIn(gerar_site.AVISO_IA, pagina.read_text(encoding="utf-8"))

    def test_aviso_de_investimento_so_quando_toca_cripto_ou_bolsa(self):
        self.assertIn(gerar_site.AVISO_INVESTIMENTO, ler(self.previa, "fundos-cripto-decisoes-ia/index.html"))
        self.assertNotIn(gerar_site.AVISO_INVESTIMENTO, ler(self.previa, "modelos-raciocinio-custo/index.html"))

    def test_sem_adsense_configurado_nao_ha_anuncio_nem_espaco(self):
        for pagina in ("index.html", "modelos-raciocinio-custo/index.html"):
            with self.subTest(pagina):
                html = ler(self.site, pagina)
                self.assertNotIn("adsbygoogle", html)
                self.assertNotIn('class="ad ', html)
                self.assertNotIn("data-ad=", html)
        self.assertFalse((self.site / "ads.txt").exists())

    def test_previa_mostra_os_espacos_e_nao_indexa(self):
        materia = ler(self.previa, "modelos-raciocinio-custo/index.html")
        for codigo in ("B1", "B2", "B3", "B4", "B5", "B6"):
            self.assertIn(f'data-ad="{codigo}"', materia)
        self.assertIn('<meta name="robots" content="noindex">', materia)
        self.assertIn("Disallow: /", ler(self.previa, "robots.txt"))
        self.assertIn("X-Robots-Tag: noindex", ler(self.previa, "_headers"))
        self.assertNotIn("noindex", ler(self.site, "modelos-raciocinio-custo/index.html"))
        self.assertIn("Sitemap: https://today.ia.br/sitemap.xml", ler(self.site, "robots.txt"))

    def test_arquivos_da_hospedagem_saem_como_arquivo(self):
        # _headers não tem ponto no nome e chegou a sair como pasta; a Cloudflare só lê o arquivo
        for nome in ("_headers", "robots.txt", "sitemap.xml", "feed.xml", "404.html", "versao.txt"):
            with self.subTest(nome):
                self.assertTrue((self.site / nome).is_file())
        self.assertIn("X-Content-Type-Options: nosniff", ler(self.site, "_headers"))

    def test_anuncios_no_texto_conforme_o_tamanho(self):
        # 6 parágrafos: só o primeiro anúncio no texto; 9: os dois; 3: nenhum (Better Ads no celular)
        agentes = ler(self.previa, "agentes-usam-computador/index.html")
        self.assertIn('data-ad="B2"', agentes)
        self.assertNotIn('data-ad="B3"', agentes)
        clubes = ler(self.previa, "clubes-ia-lesoes/index.html")
        self.assertNotIn('data-ad="B2"', clubes)

    def test_trilha_na_pagina(self):
        html = ler(self.site, "modelos-raciocinio-custo/index.html")
        self.assertIn("<b>7 etapas</b>", html)
        self.assertIn('<span class="del">já substituem advogados na análise</span>', html)
        self.assertIn("Revisada por humano 07:49", html)
        self.assertIn('<li id="f2"><span><a href="https://www.microsoft.com/exemplo/casos-de-uso"', html)

    def test_menu_so_com_editorias_que_tem_materia(self):
        inicial = ler(self.site, "index.html")
        self.assertIn('href="/ia-futebol/"', inicial)
        self.assertNotIn('href="/ia-bolsa/"', inicial)
        self.assertFalse((self.site / "ia-bolsa").exists())
        self.assertNotIn('href="/ia-cripto/"', inicial)  # a única de cripto ainda não saiu

    def test_carimbo_de_versao(self):
        sha = git_sha(self.repo)
        self.assertTrue(ler(self.site, "versao.txt").startswith(sha))
        self.assertIn(f'<meta name="versao" content="{sha[:12]}">', ler(self.site, "index.html"))


def git_sha(repo: Path) -> str:
    import subprocess
    return subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()


class Bloqueios(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_materia_com_erro_impede_tudo(self):
        repo = montar_repo(self.base / "repo", so=["2026-10-21-clubes-ia-lesoes.md"])
        ruim = (RAIZ / "testes" / "exemplos" / "2026-10-20-dialogos-games-ia.md").read_text(encoding="utf-8")
        (repo / "materias" / "2026-10-20-dialogos-games-ia.md").write_text(ruim.replace("titulo: Os", "titulo: Urgente: os"), encoding="utf-8")
        codigo, texto = gerar(repo, self.base / "site")
        self.assertEqual(codigo, 1)
        self.assertIn("expressão proibida", texto)
        self.assertFalse((self.base / "site").exists())

    def test_sem_aprovacao_fica_fora(self):
        repo = montar_repo(self.base / "repo", so=["2026-10-21-clubes-ia-lesoes.md"])
        shutil.copy(RAIZ / "testes" / "exemplos" / "2026-10-20-dialogos-games-ia.md", repo / "materias")
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "-m", "Direto na main" + TRAILER, autor=REDACAO, committer=REDACAO, quando="2026-10-20T06:03:00-03:00")
        codigo, texto = gerar(repo, self.base / "site")
        self.assertEqual(codigo, 0)
        self.assertIn("fora (sem aprovação na versão atual): 2026-10-20-dialogos-games-ia.md", texto)
        self.assertFalse((self.base / "site" / "dialogos-games-ia").exists())
        self.assertTrue((self.base / "site" / "clubes-ia-lesoes").exists())

    def test_html_do_texto_e_escapado(self):
        repo = montar_repo(self.base / "repo", so=["2026-10-21-clubes-ia-lesoes.md"])
        arq = repo / "materias" / "2026-10-21-clubes-ia-lesoes.md"
        arq.write_text(arq.read_text(encoding="utf-8").replace("linha_fina: O que", "linha_fina: <script>alert(1)</script> O que")
                       .replace("lesão muscular [1]", "lesão muscular </script><b>x</b> [1]"), encoding="utf-8")
        codigo, _ = gerar(repo, self.base / "site", "--rascunhos")
        self.assertEqual(codigo, 0)
        html = ler(self.base / "site", "clubes-ia-lesoes/index.html")
        self.assertNotIn("<script>alert(1)", html)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html)
        self.assertNotIn("</script><b>x</b>", html)

    def test_producao_para_com_pendencia_de_lancamento(self):
        repo = montar_repo(self.base / "repo", so=["2026-10-21-clubes-ia-lesoes.md"])
        codigo, texto = gerar(repo, self.base / "site", "--producao")
        self.assertEqual(codigo, 2)
        self.assertIn("Página 'Política de privacidade'", texto)

    def test_producao_para_com_arvore_suja(self):
        repo = montar_repo(self.base / "repo", so=["2026-10-21-clubes-ia-lesoes.md"])
        (repo / "materias" / "rascunho.txt").write_text("solto", encoding="utf-8")
        codigo, texto = gerar(repo, self.base / "site", "--producao")
        self.assertEqual(codigo, 2)
        self.assertIn("árvore limpa", texto)


class Hora(unittest.TestCase):
    def test_brasilia_sem_horario_de_verao(self):
        self.assertEqual(BRASILIA.utcoffset(None), timedelta(hours=-3))
        self.assertEqual(ler_hora("2026-01-15 08:00").utcoffset(), timedelta(hours=-3))

    def test_comparacao_com_hora_em_utc(self):
        # a CI roda em UTC: 11:00 UTC é 08:00 em Brasília, e a matéria das 08:00 já saiu
        publicar = ler_hora("2026-10-23 08:00")
        self.assertTrue(publicar <= datetime(2026, 10, 23, 11, 0, tzinfo=timezone.utc))
        self.assertFalse(publicar <= datetime(2026, 10, 23, 10, 59, tzinfo=timezone.utc))


if __name__ == "__main__":
    unittest.main()
