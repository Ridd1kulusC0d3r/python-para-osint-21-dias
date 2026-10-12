# 🏆 Desafio de boas-vindas — Dia 0: Meu verificador de ambiente

**Sem carta** · desafio de aquecimento (rank S simbólico, não conta nas 63 cartas)

## A missão

A Iara tem um costume: todo analista novo do NFA entrega, no primeiro dia, um **relatório do próprio
ambiente**. Assim, quando algo der errado no Dia 9, ela sabe se o problema é o código ou a máquina.

Faça a sua versão do `br/01_verifica_ambiente.py`:

1. Crie um parâmetro `MEU_NOME` e coloque o seu nome (ou apelido) no topo do relatório.
2. Verifique se **`git`** e **`pip`** estão instalados.
3. Teste uma lista de sites que **você** escolher (parâmetro `SERVICOS_EXTRAS`, separados por vírgula).
   Use só sites públicos e institucionais.
4. Grave tudo em `saidas/meu_ambiente.txt`, com data e hora de Brasília, em UTF-8.
5. Com `OSINT_OFFLINE=1`, pule os testes de internet sem dar erro.

## Critérios

- [ ] Só biblioteca padrão
- [ ] Sem `input()`: tudo vem dos parâmetros
- [ ] O arquivo abre com os acentos certos
- [ ] Roda sem internet

## Dica

`shutil.which("git")` devolve o caminho do programa, ou `None` se ele não existir. Já o `pip` pode ser
testado com `subprocess.run([sys.executable, "-m", "pip", "--version"])`: assim você confere o pip
**do mesmo Python** que está rodando o script (no Windows, isso evita muita confusão).

<details>
<summary>🔒 Gabarito (tente antes de abrir!)</summary>

Veja [`desafio_gabarito.py`](desafio_gabarito.py). No notebook, ele está numa célula escondida.

Pontos-chave da solução:

- Uma função `anotar()` imprime **e** guarda cada linha numa lista; no fim, `"\n".join(linhas)` vira o relatório.
- `sys.executable` é o caminho do Python atual: usar `-m pip` com ele garante que você testa o pip certo.
- `write_text(..., encoding="utf-8")` grava o relatório de uma vez, sem esquecer de fechar o arquivo.

</details>
