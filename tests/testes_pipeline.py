import pytest
from src.filter import process_and_filter_compounds
import pandas as pd

def test_valid_smiles():
    # Simula um DataFrame vindo do coletor com um SMILES válido (Aspirina) e um inválido
    df_teste = pd.DataFrame([
        {'Nome_Original': 'Aspirin', 'CID': 2244, 'SMILES': 'CC(=O)OC1=CC=CC=C1C(=O)O', 'Origem': 'Test', 'Unidades': '-', 'Limitacoes': '-'},
        {'Nome_Original': 'Invalido', 'CID': 0, 'SMILES': 'INVALID_SMILES_STRING', 'Origem': 'Test', 'Unidades': '-', 'Limitacoes': '-'}
    ])
    
    validos, excluidos = process_and_filter_compounds(df_teste)
    
    # Validações estritas
    assert len(validos) == 1
    assert len(excluidos) == 1
    assert excluidos.iloc[0]['Motivo_Exclusao'] == 'SMILES inválido estruturalmente pelo RDKit'
