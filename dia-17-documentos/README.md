# Dia 17 — Gerando documentos

> 🃏 Cartas **17 · 38 · 59**  ·  📘 Original: *Day 17. Generating documents*

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-17-documentos/notebook.ipynb)

## 📖 Capítulo 17 — O relatório preliminar

<!-- historia:inicio -->
O telefone da Iara toca às 16h50. Ela escuta, diz "sim, doutora" três vezes e desliga.

— A Delegada Rita quer um **relatório preliminar** amanhã cedo. Nada de dossiê final ainda: só o que
já sabemos, bem organizado, para ela pedir os dados aos bancos.

Você abre um editor de texto e começa a copiar números das saídas dos últimos dias. A Iara põe a mão
sobre o seu teclado.

— Pare. Se você copiar à mão, vai errar um centavo. E quando chegar a denúncia número 38, vai ter que
refazer tudo. Relatório de investigação é **produto de dados**: o script lê as fontes, calcula e
escreve. Rodou de novo, saiu igual. Isso é reprodutibilidade, e é ela que te defende quando alguém
perguntar "de onde saiu esse número?".

Ela aponta para os hashes que você gerou na sala de evidências.

— E coloque isso no rodapé. Quem receber o relatório tem que conseguir provar que as evidências não
mudaram. Formato? A doutora imprime tudo. Mas a planilha vai para o cartório, e lá o Excel é em
português. Pense nisso.
<!-- historia:fim -->

## 🎯 Objetivos

- Gerar DOCX, PDF e XLSX com as bibliotecas do curso original.
- Entender o que mudou do `fpdf` antigo para o `fpdf2`.
- Gerar relatórios em **Markdown** e **HTML** só com a biblioteca padrão.
- Exportar CSV que abre certo no **Excel em português** (`;`, `utf-8-sig`, vírgula decimal).
- Incluir hash SHA-256 e carimbo de tempo no relatório.
- Entender a estrutura interna de um PDF escrevendo um à mão.

## 🧠 Conceito em 2 minutos

<!-- conceito:inicio -->
Um relatório automático tem sempre três partes: **ler** as fontes, **calcular** os números e
**escrever** o documento. Só a terceira muda de formato para formato:

| Formato | Biblioteca | Quando usar |
|---|---|---|
| `.md` (Markdown) | nenhuma (texto puro) | GitHub, Obsidian, notas internas |
| `.html` | nenhuma (texto puro) | relatório bonito, imprimível como PDF pelo navegador |
| `.csv` | `csv` (nativa) | dados para planilha |
| `.docx` | `python-docx` | quando o destinatário vai **editar** no Word |
| `.xlsx` | `XlsxWriter` / `openpyxl` | planilha com fórmulas e formatação |
| `.pdf` | `fpdf2` (ou navegador) | documento final, que não deve ser alterado |

**O Excel brasileiro** espera `;` como separador (porque a vírgula é a casa decimal) e só reconhece
UTF-8 se o arquivo começar com o **BOM** (três bytes invisíveis, `EF BB BF`). Em Python, isso é só
`encoding="utf-8-sig"`.

**Reprodutibilidade:** o mesmo script com os mesmos dados gera os mesmos números. Junte a isso o
**SHA-256** de cada evidência e o **carimbo de data/hora** com fuso, e qualquer pessoa consegue
auditar o seu relatório.
<!-- conceito:fim -->

## 🥋 Nível 1 — Exercício original (cipher387)

| Arquivo | O que faz |
|---|---|
| [`original/create_xlsx.py`](original/create_xlsx.py) | Planilha de funcionários com fórmula de média (`XlsxWriter`) |
| [`original/create_docx.py`](original/create_docx.py) | Documento Word com títulos, parágrafo, quebra de página e imagem (`python-docx`) |
| [`original/create_pdf.py`](original/create_pdf.py) | PDF com uma linha de texto e uma imagem (`fpdf`) |
| [`original/2026_create_pdf.py`](original/2026_create_pdf.py) | **Atualização 2026:** o mesmo PDF sem os parâmetros obsoletos do fpdf2 |
| [`original/histogram.png`](original/histogram.png) | Imagem usada pelos scripts de DOCX e PDF |

```bash
pip install XlsxWriter python-docx fpdf2
cd dia-17-documentos/original      # os scripts procuram histogram.png na pasta atual
python create_xlsx.py
python create_docx.py
python create_pdf.py
python 2026_create_pdf.py
```

> ⚠️ **fpdf × fpdf2.** O PDF do curso manda instalar `fpdf`, um pacote parado desde 2017. Hoje use
> **`fpdf2`**, que continua com `from fpdf import FPDF`. O `create_pdf.py` original roda no fpdf2,
> mas avisa que `txt=` virou `text=` e que `ln=` está obsoleto (use `new_x`/`new_y`). Não instale
> os dois ao mesmo tempo: eles brigam pelo mesmo nome `fpdf`.

> 🔍 **Ache o bug do original:** em `create_xlsx.py`, a fórmula sai `=average(B1:B4)`, deixando o
> último funcionário fora da média (e incluindo o cabeçalho B1, que o Excel ignora por ser texto).
> Qual seria o intervalo certo?

O autor lembra que também dá para gerar apresentações com `python-pptx`.

## 🇧🇷 Nível 2 — Camada Brasil

Só **biblioteca padrão**, 100% offline (dados do caso).

| Arquivo | O que faz |
|---|---|
| [`br/01_relatorio_markdown.py`](br/01_relatorio_markdown.py) | Relatório preliminar em `.md`: resumo, tabela por chave PIX, produtos, próximos passos |
| [`br/02_relatorio_html.py`](br/02_relatorio_html.py) | Relatório HTML com cartões de totais, tabela das denúncias, SHA-256 das evidências e carimbo America/Sao_Paulo |
| [`br/03_csv_para_excel_br.py`](br/03_csv_para_excel_br.py) | CSV certo e CSV errado lado a lado; proteção contra CSV injection; resumo por mês |
| [`br/04_pdf_na_unha.py`](br/04_pdf_na_unha.py) | **Bônus:** um PDF de 1 página escrito byte a byte, com autoverificação da tabela xref |

```bash
cd dia-17-documentos
python br/02_relatorio_html.py     # depois abra saidas/relatorio_preliminar.html
python br/04_pdf_na_unha.py
```

**O que você deve ver no caso:** 37 denúncias, **R$ 54.877,40** de prejuízo, 10 em outubro e 27 em
novembro. A chave da Jéssica Prado Lima é a que mais recebeu (16 denúncias, R$ 21.242,10).

## ⚖️ Ética, LGPD e OPSEC

- **Minimização.** O relatório HTML mostra cidade, produto e valor, mas **não** nome nem CPF das
  vítimas: para entender o golpe, quem lê não precisa deles. Dado pessoal só entra no documento que
  realmente precisa dele (o ofício ao banco, por exemplo).
- **Metadados vazam.** DOCX e PDF guardam autor, empresa e datas nas propriedades do arquivo. Antes
  de enviar para fora, confira (Arquivo → Propriedades) e limpe o que não deve sair.
- **CSV injection.** Uma célula que começa com `=`, `+`, `-` ou `@` vira fórmula no Excel. Se o texto
  veio de terceiros (relatos, comentários raspados), proteja com um apóstrofo, como no script 03.
- **Relatório é documento oficial.** Diferencie claramente **fato** ("a chave X recebeu 16 PIX") de
  **hipótese** ("o titular pode ser laranja"). E nunca edite o número à mão depois de gerado.

## 🏆 Nível 3 — Desafio S

[`desafio.md`](desafio.md) — **Fábrica de ofícios**: um modelo, três ofícios (um por instituição de
pagamento), cada um com as transações da sua chave PIX e um índice com hashes.

## 🔎 Inovação OSINT do dia

**HTML → PDF com WeasyPrint.** Se você já tem o relatório em HTML (como o do script 02), a biblioteca
**WeasyPrint** (`pip install weasyprint`, licença BSD) converte para PDF respeitando o CSS, inclusive
regras de impressão como quebra de página e cabeçalho/rodapé (`@page`). Uma linha:
`from weasyprint import HTML; HTML("relatorio.html").write_pdf("relatorio.pdf")`. Assim você mantém
**um só modelo** (HTML) e gera os dois formatos. No Windows ela depende das bibliotecas do Pango;
siga o guia de instalação oficial.

## 📚 Para ir além

- fpdf2 (documentação e guia de migração do fpdf antigo): <https://py-pdf.github.io/fpdf2/>
- python-docx: <https://python-docx.readthedocs.io/>
- XlsxWriter: <https://xlsxwriter.readthedocs.io/>
- Especificação do PDF 1.7 (ISO 32000-1), cópia pública da Adobe: <https://opensource.adobe.com/dc-acrobat-sdk-docs/pdfstandards/PDF32000_2008.pdf>
- OWASP sobre CSV injection: <https://owasp.org/www-community/attacks/CSV_Injection>
- WeasyPrint: <https://doc.courtbouillon.org/weasyprint/>

## ✅ Checklist

- [ ] Gerei XLSX, DOCX e PDF com os scripts originais
- [ ] Rodei o `2026_create_pdf.py` sem avisos de obsoleto
- [ ] Achei o bug da fórmula de média do `create_xlsx.py`
- [ ] Abri o CSV certo e o errado no Excel (ou LibreOffice) e vi a diferença
- [ ] Gerei o relatório HTML e salvei como PDF pelo navegador
- [ ] Abri o PDF feito "na unha"
- [ ] Fiz o desafio S
- [ ] Anotei no meu [`DIARIO.md`](../DIARIO.md)
