import pandas as pd
import os

# Garantir que a pasta outputs existe
os.makedirs("outputs", exist_ok=True)

# Caminho do arquivo consolidado gerado pelo pipeline
caminho_csv = "outputs/resultados_completos.csv"

if not os.path.exists(caminho_csv):
    print(f"Erro: O arquivo {caminho_csv} não foi encontrado.")
    print("Execute o pipeline principal primeiro com: python3 executar_pipeline.py")
else:
    # Ler os dados processados da versão 2.0
    df = pd.read_csv(caminho_csv)
    
    # 1. Gerar a Planilha Excel estruturada para Dashboard
    caminho_excel = "outputs/dashboard_quimioinformatica_v2.xlsx"
    df.to_excel(caminho_excel, index=False, sheet_name="Resultados ADMET")
    print(f"[SUCESSO] Planilha Excel gerada em: {caminho_excel}")

    # 2. Gerar o Relatório Descritivo em HTML/PDF didático
    caminho_html = "outputs/relatorio_v2.html"
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>Relatório Quimioinformática V2.0</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; color: #333; }}
            h1 {{ color: #2c3e50; border-bottom: 2px solid #2980b9; padding-bottom: 10px; }}
            h2 {{ color: #34495e; margin-top: 30px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 14px; }}
            th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
            th {{ background-color: #2980b9; color: white; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            .footer {{ margin-top: 40px; font-size: 12px; color: #7f8c8d; text-align: center; border-top: 1px solid #eee; padding-top: 10px; }}
        </style>
    </head>
    <body>
        <h1>Relatório Técnico: Análise Quimioinformática V2.0</h1>
        <p><b>Projeto:</b> Pipeline Avançado de Triagem, Validação SMILES e Propriedades ADMET</p>
        <p><b>Repositório:</b> Analises-quimioinformatica</p>
        
        <h2>Visão Geral dos Compostos Processados</h2>
        {df.to_html(index=False, border=0)}
        
        <h2>Metodologia, Unidades e Limitações</h2>
        <ul>
            <li><b>Coleta:</b> PubChem PUG REST (com fallback seguro para ConnectivitySMILES).</li>
            <li><b>Validação Estrutural:</b> RDKit (filtragem de estruturas inválidas com auditoria de exclusão).</li>
            <li><b>Descritores:</b> Peso Molecular (g/mol), LogP (lipofilicidade), TPSA (\u00c5\u00b2), Rotatable Bonds, QED Score e Regra de Veber.</li>
            <li><b>Limitações:</b> Estimativas <i>in silico</i> baseadas em topologia molecular e modelos estatísticos abertos.</li>
        </ul>

        <div class="footer">
            <p>Gerado automaticamente pelo ambiente de desenvolvimento Ubuntu | Versão 2.0</p>
        </div>
    </body>
    </html>
    """
    
    with open(caminho_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"[SUCESSO] Relatório gerado em: {caminho_html}")
