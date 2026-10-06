from rdkit.Chem import Descriptors, Lipinski, QED
import pandas as pd

def calculate_advanced_properties(validos):
    resultados = []
    for mol, row in validos:
        # Descritores Físico-Químicos e ADMET preliminar
        tpsa = Descriptors.TPSA(mol) # Unidade: Angstroms quadrados (A^2)
        rot_bonds = Lipinski.NumRotatableBonds(mol) # Adimensional
        mw = Descriptors.MolWt(mol) # Unidade: g/mol
        logp = Descriptors.MolLogP(mol) # Adimensional (Lipofilicidade)
        qed_val = QED.qed(mol) # Drug-likeness (0 a 1)
        
        # Regra de Veber: TPSA <= 140 A^2 e Rotatable Bonds <= 10
        veber_pass = (tpsa <= 140.0) and (rot_bonds <= 10)
        
        resultados.append({
            **row,
            'Peso_Molecular_g_mol': mw,
            'LogP': logp,
            'TPSA_A2': tpsa,
            'Rotatable_Bonds': rot_bonds,
            'QED_Score': qed_val,
            'Veber_Aprovado': veber_pass,
            'Origem_Calculo': 'RDKit Descriptors',
            'Limitacoes_ADMET': 'Estimativas in silico baseadas em topologia molecular'
        })
    return pd.DataFrame(resultados)
