"""Pipeline de Triagem Físico-Química e Drug-Likeness (Versão 2.0 - Rigor Acadêmico)

Autora: Ingrid Lohana Silveira Borges
Descrição: Pipeline modularizado com validação de SMILES, descritores RDKit,
Regra de Veber (TPSA e ligações rotacionáveis), Lipinski, QED,
arredondamento rigoroso e rastreabilidade de compostos excluídos.
"""

from datetime import datetime
import os
import pandas as pd
import pubchempy as pcp
from rdkit import Chem
from rdkit.Chem import Descriptors, QED, rdMolDescriptors

# Criação de diretórios de saída
os.makedirs("outputs", exist_ok=True)

# Lista de compostos para triagem (incluindo teste de exclusão e compostos válidos)
compostos_teste = [
    "Aspirina",
    "Cafeina",
    "Paracetamol",
    "MoleculaInvalidaExemplo",
]

dados_aprovados = []
dados_excluidos = []

print(
    "=== INICIANDO PIPELINE DE TRIAGEM FÍSICO-QUÍMICA E DRUG-LIKENESS (v2.0) ==="
)
data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for nome in compostos_teste:
  try:
    resultados = pcp.get_compounds(nome, "name")
    if not resultados:
      dados_excluidos.append({
          "Composto": nome,
          "Motivo": "Composto não encontrado na base de dados pública PubChem",
          "Data_Consulta": data_atual,
          "Limitacao": "Consulta dependente de indexação externa",
      })
      continue

    comp = resultados[0]

    # Identificação rigorosa da origem do SMILES
    if hasattr(comp, "canonical_smiles") and comp.canonical_smiles:
      smiles = comp.canonical_smiles
      fonte_smiles = "CanonicalSMILES (PubChem)"
    elif hasattr(comp, "connectivity_smiles") and comp.connectivity_smiles:
      smiles = comp.connectivity_smiles
      fonte_smiles = "ConnectivitySMILES (PubChem)"
    else:
      smiles = comp.smiles
      fonte_smiles = "StandardSMILES (PubChem)"

    # Validação estrutural com RDKit
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
      dados_excluidos.append({
          "Composto": nome,
          "SMILES": smiles,
          "Fonte_SMILES": fonte_smiles,
          "Motivo": (
              "SMILES inválido ou não parseável pelo motor RDKit/Chem"
          ),
          "Data_Consulta": data_atual,
          "Limitacao": "Incompatibilidade de representação topológica",
      })
      continue

    # Cálculo rigoroso de descritores com arredondamento estrito (.round(2))
    mw = round(float(Descriptors.ExactMolWt(mol)), 2)
    logp = round(float(Descriptors.MolLogP(mol)), 2)
    tpsa = round(float(Descriptors.TPSA(mol)), 2)
    rot_bonds = int(rdMolDescriptors.CalcNumRotatableBonds(mol))
    hbd = int(rdMolDescriptors.CalcNumHBD(mol))
    hba = int(rdMolDescriptors.CalcNumHBA(mol))
    qed_val = round(float(QED.qed(mol)), 2)

    # Avaliação da Regra de Veber (TPSA <= 140 Å² e Ligações Rotacionáveis <= 10)
    veber_aprovado = tpsa <= 140.0 and rot_bonds <= 10
    criterio_detalhado = (
        f"TPSA: {tpsa} Å² (<=140), RotBonds: {rot_bonds} (<=10)"
        if veber_aprovado
        else (
            f"Falha em Veber -> TPSA: {tpsa} Å² (limite 140), RotBonds:"
            f" {rot_bonds} (limite 10)"
        )
    )

    registro = {
        "ID": f"PubChem_{comp.cid}",
        "Nome": nome,
        "SMILES": smiles,
        "Fonte_SMILES": fonte_smiles,
        "Peso_Molecular (g/mol)": mw,
        "LogP": logp,
        "TPSA (Å²)": tpsa,
        "HBD": hbd,
        "HBA": hba,
        "Rot_Bonds": rot_bonds,
        "QED": qed_val,
        "Status_Veber": (
            "Dentro do critério de Veber"
            if veber_aprovado
            else "Fora dos limites de Veber"
        ),
        "Detalhes_Criterio": criterio_detalhado,
        "Data_Consulta": data_atual,
        "Limitacao": (
            "Estimativa in silico baseada puramente em topologia molecular e"
            " descritores RDKit; não substitui ensaios in vitro."
        ),
    }

    # Critérios combinados de aprovação (Lipinski e Veber)
    if veber_aprovado and mw <= 500 and logp <= 5:
      dados_aprovados.append(registro)
    else:
      registro["Motivo"] = (
          "Violação de limiares físico-químicos estabelecidos"
          " (Lipinski/Veber/MW/LogP)"
      )
      dados_excluidos.append(registro)

  except Exception as e:
    dados_excluidos.append({
        "Composto": nome,
        "Motivo": f"Erro de processamento computacional: {str(e)}",
        "Data_Consulta": data_atual,
        "Limitacao": "Exceção capturada no fluxo de execução",
    })

# Conversão para DataFrames e exportação limpa
df_aprovados = pd.DataFrame(dados_aprovados)
df_excluidos = pd.DataFrame(dados_excluidos)

# Caminhos de saída
excel_path = "outputs/triagem_fisico_quimica_aprovados.xlsx"
csv_excluidos_path = "outputs/compostos_excluidos.csv"

df_aprovados.to_excel(excel_path, index=False)
df_excluidos.to_csv(csv_excluidos_path, index=False)

print("\n[SUCESSO] Triagem Concluída com Rigor Científico Aprimorado!")
print(f"-> Compostos Aprovados salvos em: {excel_path} ({len(df_aprovados)})")
print(
    f"-> Compostos Excluídos registrados em: {csv_excluidos_path}"
    f" ({len(df_excluidos)})"
)
