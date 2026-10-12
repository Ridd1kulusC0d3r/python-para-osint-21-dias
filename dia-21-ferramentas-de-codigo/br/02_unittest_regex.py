"""
unittest: uma bateria de testes para as expressões regulares do Dia 11.

Carta 42 (rank A) — Jutsu do Revisor (parte 2)

O que você aprende:
  • a organizar testes em uma classe que herda de unittest.TestCase;
  • assertTrue, assertFalse, assertEqual e subTest (vários casos num teste só);
  • a testar o que DEVE casar e, tão importante quanto, o que NÃO deve casar;
  • a rodar os testes sem encerrar o Python (útil no Colab).

Como rodar (dentro da pasta dia-21-ferramentas-de-codigo):
    python br/02_unittest_regex.py
"""

import re
import unittest

# ── Parâmetros ────────────────────────────────────────────────────────────
DETALHADO = True  #@param {type:"boolean"}

# ── Os padrões (versões resumidas das do Dia 11, numa linha cada) ─────────
CPF = re.compile(r"(?<!\d)\d{3}\.?\d{3}\.?\d{3}-?\d{2}(?!\d)")
CNPJ = re.compile(r"(?<!\d)\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}(?!\d)")
CNPJ_ALFA = re.compile(r"(?<![A-Z0-9])[A-Z0-9]{2}\.?[A-Z0-9]{3}\.?[A-Z0-9]{3}/?[A-Z0-9]{4}-?\d{2}(?![A-Z0-9])")
TELEFONE = re.compile(r"(?<!\d)(?:\+?55[\s-]?)?\(?[1-9]\d\)?[\s-]?(?:9[\s-]?)?\d{4}[\s-]?\d{4}(?!\d)")
CEP = re.compile(r"(?<!\d)\d{5}-?\d{3}(?!\d)")
PIX_ALEATORIA = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.IGNORECASE)
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def casa_inteiro(padrao, texto):
    """True se o padrão casa com o texto INTEIRO (fullmatch), não só com um pedaço."""
    return padrao.fullmatch(texto) is not None


class TestaPadroesBR(unittest.TestCase):
    """Cada método que começa com 'test' é um teste. O unittest acha e roda todos."""

    def verificar(self, padrao, deve_casar, nao_deve_casar):
        # subTest: se um caso falhar, os outros continuam sendo testados e aparecem no relatório.
        for texto in deve_casar:
            with self.subTest(deveria_casar=texto):
                self.assertTrue(casa_inteiro(padrao, texto), f"deveria casar: {texto!r}")
        for texto in nao_deve_casar:
            with self.subTest(nao_deveria_casar=texto):
                self.assertFalse(casa_inteiro(padrao, texto), f"NÃO deveria casar: {texto!r}")

    def test_cpf(self):
        self.verificar(CPF, ["973.091.141-08", "97309114108"], ["973.091.141-0", "9730911410812", "abc.def.ghi-jk"])

    def test_cnpj(self):
        self.verificar(CNPJ, ["48.217.093/0001-30", "48217093000130"], ["48.217.093/0001", "4821709300013"])

    def test_cnpj_alfanumerico(self):
        # Formato novo da Receita (a partir de julho/2026): letras nas 12 primeiras posições.
        self.verificar(CNPJ_ALFA, ["12.ABC.345/01DE-35", "12ABC34501DE35"], ["12.ABC.345/01DE-3X", "12.abc.345/01de-35"])

    def test_telefone(self):
        self.verificar(TELEFONE, ["(31) 98888-0101", "+55 31 9 8888-0101", "31988880101", "3133334444"],
                       ["98888", "(01) 98888-0101"])          # DDD não começa com 0

    def test_cep(self):
        self.verificar(CEP, ["30130-010", "30130010"], ["3013-0010", "301300100"])

    def test_pix_aleatoria(self):
        self.verificar(PIX_ALEATORIA, ["f38b2ffc-80a4-df5a-51c9-bc701e7ea419", "F38B2FFC-80A4-DF5A-51C9-BC701E7EA419"],
                       ["f38b2ffc-80a4-df5a-51c9", "g38b2ffc-80a4-df5a-51c9-bc701e7ea419"])

    def test_email(self):
        self.verificar(EMAIL, ["financeiro@megaoferta-brasil.example", "kau.ofertas@example.com"],
                       ["kau.ofertas@", "@example.com", "kau ofertas@example.com"])

    def test_conversa_do_caso(self):
        """Teste de integração: numa linha real da conversa, quantas chaves PIX aparecem?"""
        linha = "Falta o PIX do frete, R$ 89,90 na chave f3f49249-dc28-ff90-a5ae-c7978306d03b"
        self.assertEqual(PIX_ALEATORIA.findall(linha), ["f3f49249-dc28-ff90-a5ae-c7978306d03b"])
        # E o valor "89,90" NÃO pode ser confundido com telefone nem CEP:
        self.assertEqual(TELEFONE.findall(linha), [])
        self.assertEqual(CEP.findall(linha), [])


# ── Rodar ─────────────────────────────────────────────────────────────────
# unittest.main() encerra o Python no fim (sys.exit). No Colab isso "derruba" a célula,
# então montamos a execução à mão: carregar os testes → rodar → olhar o resultado.
suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestaPadroesBR)
resultado = unittest.TextTestRunner(verbosity=2 if DETALHADO else 1).run(suite)
print(f"\n🧪 {resultado.testsRun} testes · {len(resultado.failures)} falhas · {len(resultado.errors)} erros")
if not resultado.wasSuccessful():
    raise SystemExit("❌ Algum padrão quebrou. Leia o relatório acima: ele diz qual texto falhou.")
print("✅ Todos os padrões se comportam como o Dia 11 prometeu.")
