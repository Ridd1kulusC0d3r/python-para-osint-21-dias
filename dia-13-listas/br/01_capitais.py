"""
As operações do original (copy, sort, insert, append, pop) com capitais brasileiras.

Carta 34 (rank A) — Jutsu da Lista Ordenada

O que você aprende:
  • a criar, copiar, ordenar, inserir e remover itens de uma lista;
  • a diferença entre copiar (copy) e só dar outro nome (=);
  • a diferença entre sort() (muda a lista) e sorted() (devolve uma nova);
  • a usar índices, inclusive negativos, e o operador "in".

Como rodar (dentro da pasta dia-13-listas):
    python br/01_capitais.py
"""

# ── 1. Criar a lista ──────────────────────────────────────────────────────
# Uma lista fica entre colchetes; cada item, entre aspas, separado por vírgula.
capitais = ["Belo Horizonte", "São Paulo", "Rio de Janeiro", "Vitória"]
print("1) Sudeste:", capitais)
print(f"   São {len(capitais)} capitais. A primeira é {capitais[0]}; a última é {capitais[-1]}.")
#   capitais[0]  → primeira (a contagem começa em ZERO)
#   capitais[-1] → última (negativo conta de trás para frente)

# ── 2. Copiar: copy() x "=" ───────────────────────────────────────────────
copia = capitais.copy()        # lista NOVA, independente
apelido = capitais             # NÃO é cópia: é outro nome para a MESMA lista
apelido.append("Brasília")     # mexemos pelo "apelido"...
print("\n2) Depois de apelido.append('Brasília'):")
print("   capitais:", capitais)  # ...e a original mudou junto!
print("   copia:   ", copia)     # a cópia de verdade ficou intacta
capitais.pop()                 # desfaz: tira o último item (Brasília)

# ── 3. Acrescentar no fim: append() ───────────────────────────────────────
capitais.append("Curitiba")
print("\n3) append('Curitiba'):", capitais)

# ── 4. Inserir numa posição: insert(posição, item) ────────────────────────
capitais.insert(1, "Salvador")        # entra na posição 1 (a segunda); o resto anda uma casa
print("4) insert(1, 'Salvador'):", capitais)

# ── 5. Remover pela posição: pop(posição) ─────────────────────────────────
removida = capitais.pop(2)            # pop devolve o item removido: dá para guardar
print(f"5) pop(2) removeu '{removida}':", capitais)

# ── 5b. Remover pelo valor: remove(item) ──────────────────────────────────
if "Curitiba" in capitais:            # "in" pergunta se o item está na lista
    capitais.remove("Curitiba")       # remove a PRIMEIRA ocorrência; erro se não existir
print("   remove('Curitiba'):", capitais)

# ── 6. Ordenar: sort() e sorted() ─────────────────────────────────────────
nova = sorted(capitais)               # devolve uma lista nova ordenada
print("\n6) sorted(capitais):", nova)
print("   capitais continua:", capitais)
capitais.sort(reverse=True)           # ordena a própria lista, de Z para A
print("   capitais.sort(reverse=True):", capitais)

# ── 7. Imprimir bonito: * e sep ───────────────────────────────────────────
print("\n7) Com separador:")
print(*sorted(capitais), sep=" · ")   # o * "espalha" a lista em vários argumentos

# ── 8. Bônus: listas de listas (capital, UF) ──────────────────────────────
pares = [["Belo Horizonte", "MG"], ["Vitória", "ES"], ["Salvador", "BA"], ["São Paulo", "SP"]]
pares.sort(key=lambda par: par[1])    # key diz "ordene olhando para..." (aqui, a UF)
print("\n8) Ordenado pela UF:")
for capital, uf in pares:             # "desempacota" cada par em duas variáveis
    print(f"   {uf} → {capital}")
