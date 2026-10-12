"""
doctest: exemplos dentro da documentação que viram testes automáticos.

Carta 42 (rank A) — Jutsu do Revisor

O que você aprende:
  • a escrever exemplos no formato ">>> chamada / resultado esperado" dentro da docstring;
  • a rodar todos esses exemplos de uma vez com doctest.testmod();
  • a testar casos de borda (máscara, dígitos iguais, tamanho errado) da função de CPF do Dia 2;
  • que um teste vermelho é um AMIGO: ele avisa antes de o erro chegar ao relatório.

Como rodar (dentro da pasta dia-21-ferramentas-de-codigo):
    python br/01_doctest_cpf.py
    python -m doctest -v br/01_doctest_cpf.py     # mostra cada exemplo testado
"""

import doctest

# ── Parâmetros ────────────────────────────────────────────────────────────
MOSTRAR_CADA_TESTE = False  #@param {type:"boolean"}


def so_digitos(texto):
    """Devolve só os dígitos de um texto.

    >>> so_digitos("973.091.141-08")
    '97309114108'
    >>> so_digitos("sem números")
    ''
    """
    return "".join(c for c in texto if c.isdigit())


def cpf_valido(cpf):
    """Confere os dígitos verificadores de um CPF (a mesma regra do Dia 2, em forma de função).

    Com ou sem máscara, o resultado é o mesmo:

    >>> cpf_valido("973.091.141-08")
    True
    >>> cpf_valido("97309114108")
    True

    Um dígito trocado e a conta não fecha:

    >>> cpf_valido("973.091.141-09")
    False

    Casos de borda (são eles que pegam os bugs):

    >>> cpf_valido("111.111.111-11")      # todos iguais: a conta fecha, mas não vale
    False
    >>> cpf_valido("123.456.789")         # curto demais
    False
    >>> cpf_valido("")
    False

    Do caso: o CPF da DEN-007 não passa (alguém digitou errado na denúncia):

    >>> cpf_valido("084.520.599-47")
    False
    """
    d = [int(c) for c in so_digitos(cpf)]
    if len(d) != 11 or len(set(d)) == 1:
        return False
    for n in (9, 10):                                      # 1º e 2º dígito verificador
        soma = sum(d[i] * (n + 1 - i) for i in range(n))   # pesos 10..2 e depois 11..2
        dv = 0 if soma % 11 < 2 else 11 - soma % 11
        if dv != d[n]:
            return False
    return True


def formatar_cpf(cpf):
    """Põe a máscara 000.000.000-00. Levanta ValueError se não tiver 11 dígitos.

    >>> formatar_cpf("97309114108")
    '973.091.141-08'

    Exceções também são testáveis: o doctest compara a última linha do erro.

    >>> formatar_cpf("123")
    Traceback (most recent call last):
    ...
    ValueError: CPF precisa de 11 dígitos, veio 3
    """
    d = so_digitos(cpf)
    if len(d) != 11:
        raise ValueError(f"CPF precisa de 11 dígitos, veio {len(d)}")
    return f"{d[:3]}.{d[3:6]}.{d[6:9]}-{d[9:]}"


# ── Rodar todos os exemplos ───────────────────────────────────────────────
# testmod() procura ">>>" em todas as docstrings deste arquivo e confere os resultados.
resultado = doctest.testmod(verbose=MOSTRAR_CADA_TESTE)
print(f"🧪 doctest: {resultado.attempted} exemplos testados, {resultado.failed} falharam.")
if resultado.failed:
    raise SystemExit("❌ Algum exemplo da documentação não bate com o código. Leia o relatório acima.")
print("✅ A documentação e o código dizem a mesma coisa.")
print("💡 Experimente: troque '(n + 1 - i)' por '(n - i)' na função e rode de novo. Quem te avisa?")
