"""Trilha e aprovação a partir do git: só o merge humano feito pelo GitHub aprova."""

import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "gerador"))
sys.path.insert(0, str(RAIZ / "testes"))

from comum import ler_materia  # noqa: E402
from montar_exemplo import GITHUB, REDACAO, REVISOR, TRAILER, git, montar as montar_repo  # noqa: E402
from trilha import montar  # noqa: E402

RACIOCINIO = "2026-10-22-modelos-raciocinio-custo.md"
AGENTES = "2026-10-23-agentes-usam-computador.md"


class TrilhaCompleta(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.repo = montar_repo(Path(cls.tmp.name) / "repo")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def trilha(self, nome: str) -> dict:
        return montar(self.repo, ler_materia(self.repo / "materias" / nome))

    def test_aprovacao_ajuste_e_diff(self):
        t = self.trilha(RACIOCINIO)
        self.assertTrue(t["aprovada"])
        self.assertEqual(t["aprovada_em"].strftime("%d/%m %H:%M"), "22/10 07:52")
        self.assertEqual(t["revisada_em"].strftime("%H:%M"), "07:49")
        self.assertEqual(t["ajustes"], 1)
        self.assertEqual(t["diff"], ("já substituem advogados na análise", "auxiliam equipes jurídicas na triagem"))
        self.assertEqual([e["nome"] for e in t["etapas"]],
                         ["Coleta", "Rascunho", "Checagem", "Linguagem proibida", "Revisão humana", "Aprovada"])
        self.assertEqual([e["hora"] for e in t["etapas"]], ["06:02", "06:03", "06:03", "06:03", "07:49", "07:52"])

    def test_aprovada_sem_ajuste(self):
        t = self.trilha(AGENTES)
        self.assertTrue(t["aprovada"])
        self.assertEqual(t["ajustes"], 0)
        self.assertIsNone(t["diff"])
        self.assertEqual(t["etapas"][4]["nota"], "Lida sem ajustes")


class Aprovacao(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "repo"

    def tearDown(self):
        self.tmp.cleanup()

    def trilha(self, nome: str = AGENTES) -> dict:
        return montar(self.repo, ler_materia(self.repo / "materias" / nome))

    def editar(self, nome: str, de: str, para: str, autor, committer, quando: str, mensagem: str = "Edição"):
        arq = self.repo / "materias" / nome
        arq.write_text(arq.read_text(encoding="utf-8").replace(de, para), encoding="utf-8")
        git(self.repo, "commit", "-q", "-am", mensagem, autor=autor, committer=committer, quando=quando)

    def test_sem_merge_nao_esta_aprovada(self):
        montar_repo(self.repo, so=[AGENTES], aprovar=False)
        git(self.repo, "switch", "-q", "materia/" + AGENTES[:-3])
        t = self.trilha()
        self.assertFalse(t["aprovada"])
        self.assertIsNone(t["aprovada_em"])
        self.assertEqual(t["etapas"][-1]["nota"], "Aguardando aprovação")

    def test_merge_feito_pela_maquina_nao_aprova(self):
        montar_repo(self.repo, so=[AGENTES], aprovar=False)
        git(self.repo, "merge", "-q", "--no-ff", "materia/" + AGENTES[:-3], "-m", "Merge" + TRAILER,
            autor=REDACAO, committer=REDACAO, quando="2026-10-23T07:00:00-03:00")
        self.assertFalse(self.trilha()["aprovada"])

    def test_merge_local_de_pessoa_nao_aprova(self):
        # commit local (fora do GitHub) não é prova de que foi ele: falha fechada
        montar_repo(self.repo, so=[AGENTES], aprovar=False)
        git(self.repo, "merge", "-q", "--no-ff", "materia/" + AGENTES[:-3], "-m", "Merge",
            autor=REVISOR, committer=REVISOR, quando="2026-10-23T07:00:00-03:00")
        self.assertFalse(self.trilha()["aprovada"])

    def test_mudanca_da_maquina_depois_da_aprovacao_tira_a_aprovacao(self):
        montar_repo(self.repo, so=[AGENTES])
        self.editar(AGENTES, "Três laboratórios", "Quatro laboratórios", REDACAO, REDACAO,
                    "2026-10-23T09:00:00-03:00", "Troca" + TRAILER)
        t = self.trilha()
        self.assertFalse(t["aprovada"])
        self.assertIsNotNone(t["aprovada_em"])  # a aprovação antiga continua na trilha, mas não vale para o texto novo

    def test_mudanca_da_maquina_aprovada_por_novo_merge_volta_a_valer(self):
        montar_repo(self.repo, so=[AGENTES])
        git(self.repo, "switch", "-q", "-c", "correcao")
        self.editar(AGENTES, "Três laboratórios", "Quatro laboratórios", REDACAO, REDACAO,
                    "2026-10-23T09:00:00-03:00", "Correção" + TRAILER)
        git(self.repo, "switch", "-q", "main")
        git(self.repo, "merge", "-q", "--no-ff", "correcao", "-m", "Merge pull request #9", autor=REVISOR, committer=GITHUB,
            quando="2026-10-23T09:30:00-03:00")
        self.assertTrue(self.trilha()["aprovada"])

    def test_correcao_humana_depois_da_publicacao(self):
        montar_repo(self.repo, so=[AGENTES])
        self.editar(AGENTES, "Três laboratórios", "Quatro laboratórios", REVISOR, GITHUB, "2026-10-23T10:00:00-03:00")
        t = self.trilha()
        self.assertTrue(t["aprovada"])
        self.assertEqual(t["correcoes"], 1)
        self.assertEqual(t["etapas"][-1]["nome"], "Corrigida")
        self.assertEqual(t["aprovada_em"].strftime("%H:%M"), "07:52")

    def test_arquivo_fora_do_git_fica_sem_historico(self):
        montar_repo(self.repo, so=[AGENTES])
        novo = self.repo / "materias" / "2026-10-24-solto.md"
        novo.write_text((self.repo / "materias" / AGENTES).read_text(encoding="utf-8"), encoding="utf-8")
        t = montar(self.repo, ler_materia(novo))
        self.assertTrue(t["sem_historico"])
        self.assertFalse(t["aprovada"])


if __name__ == "__main__":
    unittest.main()
