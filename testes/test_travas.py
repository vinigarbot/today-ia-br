"""Travas das matérias: cada regra tem um caso que passa e um que não passa."""

import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "gerador"))

from comum import carregar_json, ler_materia, toca_investimento  # noqa: E402
from travas import dominio_oficial, verificar, verificar_todas  # noqa: E402

EXEMPLOS = RAIZ / "testes" / "exemplos"
NOME = "2026-10-23-agentes-usam-computador.md"
BASE = (EXEMPLOS / NOME).read_text(encoding="utf-8")
CFG, OFICIAIS = carregar_json("config.json"), carregar_json("fontes_oficiais.json")


class Travas(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.pasta = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def conferir(self, texto: str, nome: str = NOME):
        arq = self.pasta / nome
        arq.write_text(texto, encoding="utf-8")
        return verificar(ler_materia(arq), CFG, OFICIAIS)

    def trocado(self, velho: str, novo: str, **kw):
        self.assertIn(velho, BASE)
        return self.conferir(BASE.replace(velho, novo, 1), **kw)

    def assertErro(self, resultado, trecho: str):
        erros = resultado[0]
        self.assertTrue(any(trecho in e for e in erros), f"esperava erro com '{trecho}', veio {erros}")

    # ------------------------------------------------ o que passa

    def test_todos_os_exemplos_passam(self):
        for arq in sorted(EXEMPLOS.glob("2*.md")):
            with self.subTest(arq.name):
                self.assertEqual(verificar(ler_materia(arq), CFG, OFICIAIS)[0], [])

    def test_sigla_curta_no_titulo_passa(self):
        self.assertEqual(self.trocado("Os agentes de IA já usam", "Os agentes de IA da ANPD e do GPT já usam")[0], [])

    def test_numero_do_titulo_presente_no_texto_passa(self):
        texto = BASE.replace("Os agentes de IA", "Os 3 agentes de IA", 1).replace("Três laboratórios", "Os 3 laboratórios", 1)
        self.assertEqual(self.conferir(texto)[0], [])

    # ------------------------------------------------ fontes

    def test_fonte_fora_da_lista_nao_passa(self):
        self.assertErro(self.trocado("https://openai.com/exemplo/agentes-no-navegador", "https://www.jornal-qualquer.com.br/agentes"), "fora da lista")

    def test_dominio_parecido_nao_passa(self):
        for url in ("https://openai.com.golpe.net/x", "https://notopenai.com/x", "https://gov.br.golpe.com/x"):
            with self.subTest(url):
                self.assertIsNone(dominio_oficial(url, OFICIAIS))
        self.assertEqual(dominio_oficial("https://www.gov.br/anpd/x", OFICIAIS), "Governo federal")
        self.assertEqual(dominio_oficial("https://www.bcb.gov.br/x", OFICIAIS), "Governo federal")

    def test_fonte_sem_https_nao_passa(self):
        self.assertErro(self.trocado("https://openai.com/exemplo", "http://openai.com/exemplo"), "sem https")

    def test_sem_secao_de_fontes_nao_passa(self):
        self.assertErro(self.conferir(BASE.split("## Fontes")[0]), "Sem a seção")

    def test_fonte_nao_citada_nao_passa(self):
        self.assertErro(self.conferir(BASE.rstrip() + "\n5. [Extra](https://openai.com/exemplo/extra)\n"), "não citada")

    def test_chamada_sem_fonte_nao_passa(self):
        self.assertErro(self.trocado("de um funcionário [4].", "de um funcionário [4][7]."), "Chamada [7]")

    def test_paragrafo_sem_fonte_nao_passa(self):
        self.assertErro(self.trocado("não na execução [2].", "não na execução."), "Trecho sem fonte")

    def test_link_solto_no_texto_nao_passa(self):
        self.assertErro(self.trocado("não na execução [2].", "não na [execução](https://openai.com/x) [2]."), "Link solto")

    def test_numeracao_pulada_nao_passa(self):
        texto = BASE.replace("4. [Orientação", "5. [Orientação").replace("[4].", "[5].")
        self.assertErro(self.conferir(texto), "numeradas")

    def test_linha_de_fonte_fora_do_formato_nao_passa(self):
        self.assertErro(self.conferir(BASE.rstrip() + "\n5. Fonte sem link\n"), "fora do formato")

    # ------------------------------------------------ título

    def test_expressoes_proibidas_no_titulo_nao_passam(self):
        for frase in ("Você não vai acreditar:", "Chocante:", "Urgente:", "Inacreditável:"):
            with self.subTest(frase):
                self.assertErro(self.trocado("titulo: Os agentes", f"titulo: {frase} os agentes"), "expressão proibida")

    def test_expressao_proibida_na_linha_fina_nao_passa(self):
        self.assertErro(self.trocado("linha_fina: Três anúncios", "linha_fina: Urgente: três anúncios"), "expressão proibida")

    def test_titulo_em_maiusculas_nao_passa(self):
        self.assertErro(self.trocado("Os agentes de IA já usam o computador", "OS AGENTES DE IA JÁ USAM O COMPUTADOR"), "maiúsculas")
        self.assertErro(self.trocado("muda mais do que parece", "muda MUITO mais do que parece"), "maiúsculas")

    def test_emoji_no_titulo_nao_passa(self):
        self.assertErro(self.trocado("do que parece", "do que parece 🚀"), "emoji")

    def test_numero_do_titulo_fora_do_texto_nao_passa(self):
        self.assertErro(self.trocado("Os agentes de IA", "Os 5 agentes de IA"), "número 5")

    # ------------------------------------------------ investimento e cópia

    def test_linguagem_de_recomendacao_nao_passa(self):
        for frase in ("compre agora", "vale a pena investir", "o preço-alvo é", "é hora de vender", "invista já"):
            with self.subTest(frase):
                self.assertErro(self.trocado("não na execução [2].", f"não na execução, {frase} [2]."), "recomendação de investimento")

    def test_venda_e_alerta_so_quando_toca_investimento(self):
        erros, alertas = verificar(ler_materia(EXEMPLOS / "2026-10-23-fundos-cripto-decisoes-ia.md"), CFG, OFICIAIS)
        self.assertEqual(erros, [])
        self.assertTrue(any("'venda'" in a for a in alertas), alertas)
        erros, alertas = self.trocado("não na execução [2].", "não na execução, como na venda de licenças [2].")
        self.assertEqual(erros, [])
        self.assertFalse(any("'venda'" in a for a in alertas), alertas)

    def test_acoes_no_sentido_de_atos_nao_viram_bolsa(self):
        texto = ler_materia(EXEMPLOS / NOME)
        self.assertIn("As ações que enviam dados", texto["texto"])
        self.assertFalse(toca_investimento(texto, CFG["termos_investimento"]))
        self.assertTrue(toca_investimento(dict(texto, texto="O mercado de ações reagiu."), CFG["termos_investimento"]))
        self.assertTrue(toca_investimento(dict(texto, texto="O preço do bitcoin."), CFG["termos_investimento"]))

    def test_trecho_literal_longo_nao_passa(self):
        citacao = "“" + " ".join(["palavra"] * 30) + "”"
        self.assertErro(self.trocado("não na execução [2].", f"não na execução: {citacao} [2]."), "aspas")
        curta = "“" + " ".join(["palavra"] * 10) + "”"
        self.assertEqual(self.trocado("não na execução [2].", f"não na execução: {curta} [2].")[0], [])

    def test_destaque_que_nao_esta_no_texto_nao_passa(self):
        self.assertErro(self.trocado("coletada_em:", "destaque: Uma frase que não está no texto.\ncoletada_em:"), "destaque")

    # ------------------------------------------------ cabeçalho e nome

    def test_campo_obrigatorio_faltando_nao_passa(self):
        self.assertErro(self.trocado("coletada_em: 2026-10-23 06:02\n", ""), "'coletada_em'")

    def test_hora_fora_do_formato_nao_passa(self):
        self.assertErro(self.trocado("publicar_em: 2026-10-23 08:00", "publicar_em: 23/10/2026 8h"), "fora do formato")

    def test_data_do_arquivo_diferente_da_publicacao_nao_passa(self):
        self.assertErro(self.conferir(BASE, nome="2026-10-24-agentes-usam-computador.md"), "data do nome")

    def test_nome_de_arquivo_fora_do_formato_nao_passa(self):
        self.assertErro(self.conferir(BASE, nome="2026-10-23-Agentes Usam.md"), "Nome do arquivo")

    def test_editoria_inexistente_nao_passa(self):
        self.assertErro(self.trocado("editoria: ia\n", "editoria: politica\n"), "não existe")

    def test_coleta_depois_da_publicacao_nao_passa(self):
        self.assertErro(self.trocado("coletada_em: 2026-10-23 06:02", "coletada_em: 2026-10-23 09:00"), "não pode ser depois")

    def test_endereco_repetido_nao_passa(self):
        (self.pasta / NOME).write_text(BASE, encoding="utf-8")
        outro = BASE.replace("2026-10-23 08:00", "2026-10-24 08:00").replace("2026-10-23 06:02", "2026-10-24 06:02")
        (self.pasta / "2026-10-24-agentes-usam-computador.md").write_text(outro, encoding="utf-8")
        resultado = verificar_todas([ler_materia(a) for a in sorted(self.pasta.glob("*.md"))], CFG, OFICIAIS)
        for nome, (erros, _) in resultado.items():
            with self.subTest(nome):
                self.assertTrue(any("Já existe" in e for e in erros), erros)

    def test_quadro_de_dados_com_valor_nao_numerico_nao_passa(self):
        bloco = ":::dados Teste [1]\nA | 10\nB | muito\n:::\n\n"
        self.assertErro(self.trocado("## O que muda para quem usa", bloco + "## O que muda para quem usa"), "não é número")


if __name__ == "__main__":
    unittest.main()
