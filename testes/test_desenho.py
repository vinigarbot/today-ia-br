"""Os desenhos do gerador saem iguais aos da maquete (valores de referência tirados do maquete/app.js no Node em 22/10/2026)."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "gerador"))

from desenho import assinatura, codigo_assinatura, hash32, mapa_atencao, sorteio, tokens_titulo  # noqa: E402

REFERENCIA_JS = {
    "raciocinio-empresas": (3901416492, [0.1131, 0.5019, 0.7701, 0.8396, 0.2051]),
    "Os|agentes|de|IA|já|usam|o|computador|sozinhos": (523858300, [0.5975, 0.7907, 0.5753, 0.7038, 0.0912]),
    "ação×ç": (2962684985, [0.1377, 0.755, 0.7019, 0.4654, 0.8842]),
}


class Desenho(unittest.TestCase):
    def test_hash_e_sorteio_iguais_ao_javascript(self):
        for texto, (h, seq) in REFERENCIA_JS.items():
            with self.subTest(texto):
                self.assertEqual(hash32(texto), h)
                r = sorteio(h)
                self.assertEqual([r() for _ in seq], seq)

    def test_assinatura_estavel_e_diferente_por_materia(self):
        self.assertEqual(assinatura("a"), assinatura("a"))
        self.assertNotEqual(assinatura("a"), assinatura("b"))
        self.assertRegex(codigo_assinatura("raciocinio-empresas"), r"^#[0-9a-f]{4}·\d{4}$")

    def test_tokens_param_no_primeiro_ponto_e_em_dez(self):
        self.assertEqual(tokens_titulo("Os agentes de IA já usam o computador sozinhos. E isso muda mais do que parece"),
                         ["Os", "agentes", "de", "IA", "já", "usam", "o", "computador", "sozinhos"])
        self.assertEqual(len(tokens_titulo(" ".join(["palavra"] * 15))), 10)

    def test_mapa_sem_numeros(self):
        # decisão dele de 23/10/2026: é desenho, não atenção medida; nenhum peso escrito no mapa
        mapa = mapa_atencao(tokens_titulo("Os agentes de IA já usam o computador sozinhos"))
        self.assertIn("<path", mapa)
        self.assertNotRegex(mapa, r">\s*\d+[.,]\d+\s*<")

    def test_mapa_escapa_texto_e_exige_duas_palavras(self):
        self.assertEqual(mapa_atencao(["só"]), "")
        self.assertNotIn("<b>", mapa_atencao(["a", "<b>"]))


if __name__ == "__main__":
    unittest.main()
