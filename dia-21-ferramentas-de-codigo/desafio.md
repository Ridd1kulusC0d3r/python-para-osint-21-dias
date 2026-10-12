# 🏆 Desafio S — Dia 21: O guardião do repositório

**Carta 63 · Rank S**

## A missão

O curso acabou, mas o repositório vai continuar recebendo contribuições: novos exercícios, correções,
dias extras. A Iara quer um **guardião**: um script que leia todos os exercícios BR e aponte quem
quebrou as regras do [`CONTRIBUTING.md`](../CONTRIBUTING.md), **sem executar nada**.

Escreva um script que, para cada `dia-*/br/*.py` do repositório:

1. Confira a **sintaxe** com `ast.parse` (e não pare se um arquivo tiver erro).
2. Exija **docstring** no topo com a palavra "Carta" (o Dia 0 é exceção: não tem cartas).
3. Acuse qualquer chamada a **`input()`**.
4. Acuse **imports fora da biblioteca padrão**, exceto os que estão dentro de um
   `try/except ImportError` (como o `IPython` e o `google.colab`, que são opcionais).
5. Acuse **`open()` em modo texto** e `read_text()`/`write_text()` **sem `encoding=`**.
6. Imprima um placar por dia e grave `saidas/revisao_codigo.csv`.

## Critérios de rank S

- [ ] Só biblioteca padrão; nenhum script analisado é executado ou importado
- [ ] `open(arquivo, "rb")` **não** é acusado (modo binário não tem encoding)
- [ ] Um `import requests` solto é acusado; um `from IPython.display import HTML` dentro de `try/except ImportError` não é
- [ ] Funciona no Python 3.9 (dica: `sys.stdlib_module_names` só existe a partir do 3.10)
- [ ] Testado com um arquivo "ruim" feito por você (cada regra acusada pelo menos uma vez)

## Dica

`ast.walk(arvore)` visita todos os nós. Os que interessam: `ast.Call` (chamadas de função; olhe
`no.func` e `no.keywords`), `ast.Import`, `ast.ImportFrom` e `ast.Try` (com `no.handlers`).
`ast.get_docstring(arvore)` devolve a docstring do módulo.

<details>
<summary>🔒 Gabarito (tente antes de abrir!)</summary>

Veja [`desafio_gabarito.py`](desafio_gabarito.py). No notebook, ele está numa célula escondida.

Pontos-chave da solução:

- `imports_opcionais()` percorre cada `ast.Try` cujo `except` trata `ImportError`
  (ou `Exception`) e anota os módulos importados ali dentro.
- O modo do `open` vem do 2º argumento posicional **ou** de `mode=`; se for uma variável, assume-se
  o padrão `"r"` (texto).
- `getattr(sys, "stdlib_module_names", ())` com uma lista mínima de reserva mantém a compatibilidade
  com o 3.9.
- No repositório inteiro, o resultado esperado é **zero apontamentos**. Para ver o guardião
  trabalhando, crie um arquivo com `import requests`, `input()` e `open("x.txt", "w")` e revise-o
  com a função `revisar()`.

</details>
