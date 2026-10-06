import os
import openpyxl
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
import pandas as pd

os.makedirs("outputs", exist_ok=True)

dados = {
    "ID": ["PubChem_2244", "PubChem_3672", "PubChem_148"],
    "Peso Molecular": [180.16, 194.19, 151.16],
    "LogP": [1.31, -0.29, 0.46],
    "Status": ["Aprovado", "Aprovado", "Aprovado"],
}

df = pd.DataFrame(dados)
excel_path = "outputs/dashboard_quimioinformatica_v2.xlsx"

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Dashboard Executivo"
ws.views.sheetView[0].showGridLines = True

# Estilos
font_title = Font(name="Calibri", size=14, bold=True, color="1F4E78")
font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
font_bold = Font(name="Calibri", size=11, bold=True, color="000000")
font_normal = Font(name="Calibri", size=11, color="000000")

fill_header = PatternFill(
    start_color="1F4E78", end_color="1F4E78", fill_type="solid"
)
fill_card = PatternFill(
    start_color="E9EDF4", end_color="E9EDF4", fill_type="solid"
)

border_thin = Border(
    left=Side(style="thin", color="D9D9D9"),
    right=Side(style="thin", color="D9D9D9"),
    top=Side(style="thin", color="D9D9D9"),
    bottom=Side(style="thin", color="D9D9D9"),
)

# 1. Título
ws["B2"] = "PAINEL EXECUTIVO: TRIAGEM VIRTUAL DE FÁRMACOS"
ws["B2"].font = font_title

# 2. Cards de KPIs
# Total de Compostos
ws.merge_cells("B4:C4")
ws["B4"] = "Total de Compostos"
ws["B4"].font = font_bold
ws["B4"].alignment = Alignment(horizontal="center", vertical="center")
ws["B4"].fill = fill_card

ws.merge_cells("B5:C5")
ws["B5"] = len(df)
ws["B5"].font = font_title
ws["B5"].alignment = Alignment(horizontal="center", vertical="center")
ws["B5"].fill = fill_card

# Peso Molecular Médio (Calculado direto pelo Python para garantir precisão exata)
ws.merge_cells("E4:F4")
ws["E4"] = "Peso Molecular Médio"
ws["E4"].font = font_bold
ws["E4"].alignment = Alignment(horizontal="center", vertical="center")
ws["E4"].fill = fill_card

ws.merge_cells("E5:F5")
ws["E5"] = df["Peso Molecular"].mean()
ws["E5"].number_format = "0.00"
ws["E5"].font = font_title
ws["E5"].alignment = Alignment(horizontal="center", vertical="center")
ws["E5"].fill = fill_card

# LogP Médio (Calculado direto pelo Python para evitar conflito de texto/número com o Excel)
ws.merge_cells("H4:I4")
ws["H4"] = "LogP Médio"
ws["H4"].font = font_bold
ws["H4"].alignment = Alignment(horizontal="center", vertical="center")
ws["H4"].fill = fill_card

ws.merge_cells("H5:I5")
ws["H5"] = df["LogP"].mean()
ws["H5"].number_format = "0.00"
ws["H5"].font = font_title
ws["H5"].alignment = Alignment(horizontal="center", vertical="center")
ws["H5"].fill = fill_card

for row in range(4, 6):
  for col in [2, 3, 5, 6, 8, 9]:
    ws.cell(row=row, column=col).border = border_thin

# 3. Tabela de Dados
ws["B8"] = "Candidatos Aprovados"
ws["B8"].font = font_bold

headers = ["ID", "Peso Molecular", "LogP", "Status"]
for c_idx, h in enumerate(headers, start=2):
  cell = ws.cell(row=9, column=c_idx, value=h)
  cell.font = font_header
  cell.fill = fill_header
  cell.alignment = Alignment(horizontal="center", vertical="center")

for r_idx, row in df.iterrows():
  row_num = 10 + r_idx
  ws.cell(row=row_num, column=2, value=row["ID"]).alignment = Alignment(
      horizontal="left", vertical="center"
  )
  
  # Forçando valores numéricos puros nas células da tabela
  c_peso = ws.cell(row=row_num, column=3, value=float(row["Peso Molecular"]))
  c_peso.number_format = "0.00"
  c_peso.alignment = Alignment(horizontal="right", vertical="center")

  c_logp = ws.cell(row=row_num, column=4, value=float(row["LogP"]))
  c_logp.number_format = "0.00"
  c_logp.alignment = Alignment(horizontal="right", vertical="center")

  ws.cell(row=row_num, column=5, value=row["Status"]).alignment = Alignment(
      horizontal="center", vertical="center"
  )

  for c_idx in range(2, 6):
    ws.cell(row=row_num, column=c_idx).border = border_thin
    ws.cell(row=row_num, column=c_idx).font = font_normal

# 4. Gráfico de Barras
chart = BarChart()
chart.type = "col"
chart.style = 10
chart.title = "Comparativo de Peso Molecular por Candidato"
chart.y_axis.title = "Peso Molecular (g/mol)"
chart.x_axis.title = "ID do Composto"

data_ref = Reference(ws, min_col=3, min_row=9, max_row=12)
cats_ref = Reference(ws, min_col=2, min_row=10, max_row=12)
chart.add_data(data_ref, titles_from_data=True)
chart.set_categories(cats_ref)
chart.height = 7.5
chart.width = 13

ws.add_chart(chart, "G8")

col_widths = {
    "A": 3,
    "B": 18,
    "C": 16,
    "D": 12,
    "E": 14,
    "F": 12,
    "G": 5,
    "H": 12,
    "I": 12,
    "J": 15,
}
for col, width in col_widths.items():
  ws.column_dimensions[col].width = width

wb.save(excel_path)
print(f"[SUCESSO] Dashboard perfeito gerado em: {excel_path}")
