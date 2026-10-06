import pubchempy as pcp
import pandas as pd

def fetch_pubchem_data(compound_names):
    dados = []
    for name in compound_names:
        try:
            results = pcp.get_compounds(name, 'name')
            if results:
                comp = results[0]
                # Tratamento seguro para evitar KeyError de SMILES
                smiles = getattr(comp, 'canonical_smiles', None) or getattr(comp, 'connectivity_smiles', None)
                dados.append({
                    'Nome_Original': name,
                    'CID': comp.cid,
                    'SMILES': smiles,
                    'Origem': 'PubChem PUG REST',
                    'Unidades': 'Adimensional / Padrão SMILES',
                    'Limitacoes': 'SMILES canônico pode omitir estereoquímica complexa'
                })
        except Exception as e:
            print(f"Erro ao buscar {name}: {e}")
    return pd.DataFrame(dados)
