from src.coletor_pubchem import fetch_pubchem_data
from src.validador_smiles import process_and_filter_compounds
from src.calculador_propriedades import calculate_advanced_properties

if __name__ == "__main__":
    # Lista de exemplo para análise
    compostos = ['Aspirin', 'Caffeine', 'Paracetamol', 'MoleculaInvalidaExemplo']
    
    print("[1/3] Coletando dados do PubChem...")
    df_raw = fetch_pubchem_data(compostos)
    
    print("[2/3] Validando SMILES e filtrando...")
    validos, df_excluidos = process_and_filter_compounds(df_raw)
    df_excluidos.to_csv("outputs/compostos_excluidos.csv", index=False)
    
    print("[3/3] Calculando TPSA, Veber, QED e ADMET...")
    df_final = calculate_advanced_properties(validos)
    df_final.to_csv("outputs/resultados_completos.csv", index=False)
    
    print("Processo concluído com sucesso! Verifique a pasta 'outputs/'.")
