"""
Por que "Águas Lindas" vai parar depois de "Zé Doca"? Ordenação com acentos.

Carta 34 (rank A) — Jutsu da Lista Ordenada (parte 2)

O que você aprende:
  • que sorted() compara letras pelo código Unicode: maiúsculas antes de minúsculas,
    e letras acentuadas depois do "z";
  • a criar uma "chave de ordenação" sem acento e sem diferença de caixa
    (unicodedata.normalize + casefold);
  • a desempatar palavras iguais sem acento ("Pará" x "para");
  • que locale.strxfrm resolve, mas depende do sistema ter o idioma pt_BR instalado.

Como rodar (dentro da pasta dia-13-listas):
    python br/02_ordenar_com_acento.py
"""

import locale
import unicodedata

CIDADES = ["Zé Doca", "Águas Lindas de Goiás", "Belo Horizonte", "Óbidos",
           "abaetetuba", "Itaúna", "Ibirité", "Ouro Preto", "Uberlândia", "Ubá"]

# ── 1. O problema ─────────────────────────────────────────────────────────
print("❌ sorted() comum:")
for c in sorted(CIDADES):
    print(f"   {c}")
print("\n   Por quê? Cada letra tem um número (ord). Veja:")
for letra in ["B", "Z", "a", "z", "Á", "Ó"]:
    print(f"   ord('{letra}') = {ord(letra)}")
print("   Maiúsculas (65–90) < minúsculas (97–122) < acentuadas (192+).")


# ── 2. A solução: uma chave "sem acento e sem caixa" ──────────────────────
def chave_pt(texto):
    """
    'Águas' → 'aguas'. Passo a passo:
      1. normalize("NFKD") separa a letra do acento: 'Á' vira 'A' + '´' (acento solto);
      2. o filtro joga fora os acentos soltos (combining);
      3. casefold() deixa tudo minúsculo (é um lower() mais caprichado: 'ß' → 'ss').
    Devolve uma TUPLA: (sem acento, original). A segunda parte desempata
    palavras que ficam iguais sem acento, de forma sempre previsível.
    """
    separado = unicodedata.normalize("NFKD", texto)
    sem_acento = "".join(c for c in separado if not unicodedata.combining(c))
    return (sem_acento.casefold(), texto)


print("\n✅ sorted(key=chave_pt):")
for c in sorted(CIDADES, key=chave_pt):
    print(f"   {c:<24} chave → {chave_pt(c)[0]}")

# ── 3. Desempate ──────────────────────────────────────────────────────────
print("\n🔁 Desempate com palavras iguais sem acento:")
print("  ", sorted(["para", "Pará", "pára"], key=chave_pt))

# ── 4. A alternativa do sistema: locale.strxfrm ───────────────────────────
# Se o sistema tiver o idioma pt_BR, o próprio sistema sabe ordenar do jeito brasileiro.
# Em muitos servidores (e no Colab) ele não vem instalado: por isso a chave acima é mais garantida.
print("\n🌐 Tentando locale pt_BR:")
for nome in ("pt_BR.UTF-8", "pt_BR.utf8", "Portuguese_Brazil.1252"):   # Linux/macOS e Windows
    try:
        locale.setlocale(locale.LC_COLLATE, nome)
        print(f"   ✅ locale '{nome}' disponível:")
        print("  ", sorted(CIDADES, key=locale.strxfrm))
        break
    except locale.Error:
        continue
else:
    # O "else" de um for roda quando o laço termina SEM break.
    print("   ⚠️ pt_BR não está instalado neste sistema; fique com a chave_pt.")
