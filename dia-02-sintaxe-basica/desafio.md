# 🏆 Desafio S — Dia 2: Classificador de documentos

**Carta 44 · Rank S**

## A missão

Na conversa de WhatsApp do caso aparecem números soltos: "CNPJ da loja", "CNPJ do sócio", o CPF que um
cliente mandou "pra nota", telefones... A Iara quer uma ferramenta que olhe para uma lista misturada e
diga **o que é cada coisa** e **se a conta fecha**.

Escreva um script que, para cada item da lista `DOCUMENTOS`:

1. Limpe pontuação e espaços.
2. Classifique como **CPF** (11 dígitos), **CNPJ numérico** (14 dígitos), **CNPJ alfanumérico**
   (14 posições com letra nas 12 primeiras e 2 DV numéricos), **telefone** ou **desconhecido**.
   Cuidado: um celular com DDD também tem 11 dígitos! Use o formato (parênteses, `+55`) para separar.
3. Diga se é **válido**.
4. Se for inválido, mostre **quais seriam os dígitos verificadores corretos**.
5. No fim, mostre quantos itens de cada tipo apareceram.

Use esta lista (todos os números do caso são fictícios):

```python
DOCUMENTOS = [
    "48.217.093/0001-30", "31.560.427/0001-71", "019.018.791-35", "084.520.599-47",
    "00.000.000/0001-91", "00.000.000/E08G-12", "(31) 98888-0101",
]
```

## Critérios de rank S

- [ ] Só biblioteca padrão
- [ ] Uma função para calcular DV de CPF e outra para DV de CNPJ
- [ ] O CNPJ alfanumérico é tratado com `ord(c) - 48`
- [ ] O telefone (11 dígitos!) não é confundido com CPF
- [ ] Os dois CNPJs do vendedor aparecem como ❌

## Dica

Um dicionário serve de contador: `contagem[tipo] = contagem.get(tipo, 0) + 1`.
E `range(10, 1, -1)` gera os pesos do CPF: 10, 9, 8, ..., 2.

<details>
<summary>🔒 Gabarito (tente antes de abrir!)</summary>

Veja [`desafio_gabarito.py`](desafio_gabarito.py). No notebook, ele está numa célula escondida.

Pontos-chave da solução:

- `"".join(c for c in texto.upper() if c.isalnum())` limpa o texto e já põe as letras em maiúsculas.
- Calcular o DV a partir da base (`dv_cpf(limpo[:9])`) serve para validar **e** para mostrar o final correto.
- Atenção ética: o DV "corrigido" é só um diagnóstico. O número consertado pode pertencer a outra
  pessoa; nunca consulte um documento "adivinhado".

</details>
