# 🏆 Desafio S — Dia 6: Fichário de CNPJs do caso

**Carta 48 · Rank S**

## A missão

O CNPJ do rodapé era falso. A Iara desconfia que **não é o único**: golpista que inventa um número
costuma inventar outros. Ela quer um fichário com todo CNPJ que aparece nos arquivos do caso.

Escreva um script que:

1. Varra os arquivos de `caso/dados/` (`.txt`, `.html`, `.csv`, `.sql`) atrás de CNPJs no formato
   `00.000.000/0000-00`, aceitando também **letras** nas 12 primeiras posições (CNPJ alfanumérico).
2. Guarde **em quais arquivos** cada CNPJ apareceu (um dicionário `cnpj → [arquivos]`).
3. Valide o dígito verificador. **Só consulte a API** para os válidos.
4. Para os válidos, busque na BrasilAPI: razão social, situação cadastral e a lista de sócios (`qsa`).
5. Inclua o CNPJ público de controle `00.000.000/0001-91` para provar que a consulta funciona.
6. Grave `saidas/fichario_cnpjs.json` com `indent=2` e `ensure_ascii=False`, e um resumo
   (`total`, `invalidos`).
7. Funcione **sem internet** usando a amostra de `dados/`.

## Critérios de rank S

- [ ] Só biblioteca padrão
- [ ] Nenhuma consulta é feita para CNPJ com DV inválido
- [ ] Os dois CNPJs que o "Kau" usa saem como 🚩, cada um com o arquivo de origem
- [ ] O JSON final abre no navegador ou no VS Code com os acentos certos

## Dica

`dicionario.setdefault(chave, []).append(valor)` cria a lista na primeira vez e só acrescenta nas
seguintes. É o jeito mais curto de montar "um para muitos".

<details>
<summary>🔒 Gabarito (tente antes de abrir!)</summary>

Veja [`desafio_gabarito.py`](desafio_gabarito.py). No notebook, ele está numa célula escondida.

Pontos-chave da solução:

- A regex `[0-9A-Z]{2}\.[0-9A-Z]{3}\.[0-9A-Z]{3}/[0-9A-Z]{4}-\d{2}` já prepara o terreno para o
  CNPJ alfanumérico (o Dia 11 aprofunda regex).
- O DV usa `ord(caractere) - 48` como valor: funciona para dígitos e letras com os mesmos pesos.
- A lista de sócios é "achatada" numa compreensão de lista com `.get`, então um sócio sem algum
  campo não derruba o fichário.

</details>
