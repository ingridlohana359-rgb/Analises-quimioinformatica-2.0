from rdkit import Chem
import pandas as pd

def process_and_filter_compounds(df):
    validos = []
    excluidos = []
    
    for _, row in df.iterrows():
        smiles = row['SMILES']
        if not smiles:
            excluidos.append({**row, 'Motivo_Exclusao': 'SMILES nulo ou não retornado'})
            continue
            
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            excluidos.append({**row, 'Motivo_Exclusao': 'SMILES inválido estruturalmente pelo RDKit'})
        else:
            validos.append((mol, row))
            
    df_excluidos = pd.DataFrame(excluidos)
    return validos, df_excluidos
