#  Pipeline de Triagem Quimioinformática (Versão 2.0)

> Pipeline computacional avançado para triagem virtual de fármacos, análise ADMET, filtragem físico-química e geração de relatórios executivos em Python.

---

##  Sobre o Projeto
Este repositório (`Analises-quimioinformatica-2.0`) representa a evolução natural e o refinamento do projeto original. Enquanto a **Versão 1.0** estabeleceu o marco inicial com painéis executivos funcionais e triagem inicial de compostos, a **Versão 2.0** eleva o rigor científico e a robustez de engenharia de software ao introduzir:
* **Validação Rigorosa de SMILES** (tratamento inteligente de conectividade e formas cânonicas).
* **Filtros Farmacológicos Avançados** (TPSA, QED, Regra de Veber e parâmetros ADMET).
* **Rastreabilidade de Excluídos** (registro transparente dos compostos reprovados e justificativas dos critérios de corte).
* **Arquitetura Modular** com testes unitários alinhados e automação de planilhas e relatórios.

---

##  Evolução: Da Versão 1.0 para a Versão 2.0

| Requisito / Componente | Versão 1.0 | Versão 2.0 (Atual) |
| :--- | :--- | :--- |
| **Arquitetura do Código** | Scripts lineares de consolidação inicial | Arquitetura modularizada (`src/`, testes e scripts desacoplados) |
| **Validação de Moléculas** | Extração direta sem checagem de atributos | Correção do mapeamento PubChem (`ConnectivitySMILES` vs `CanonicalSMILES`) e validação via RDKit |
| **Parâmetros Físico-Químicos** | Foco básico em Peso Molecular e LogP | Inclusão robusta de **TPSA**, **QED** (Drug-likeness) e **Regra de Veber** |
| **Tratamento de Excluídos** | Apenas compostos aprovados exibidos | **Rastreabilidade completa**: salvamento e registro de moléculas reprovadas com os motivos da exclusão |
| **Apresentação de Resultados** | Dashboard Executivo inicial com KPIs | Dashboard Executivo aprimorado, colunas ajustadas e tratamento contra conflitos de tipo no Excel (`openpyxl`) |

---

##  Tecnologias Utilizadas
* **Python 3** — Linguagem principal do pipeline
* **RDKit** — Química computacional, descritores e validação estrutural
* **PubChemPy** — Consulta e integração com a base de dados do PubChem
* **Pandas** — Manipulação, filtragem e estruturação de datasets ADMET
* **OpenPyXL** — Automação e estilização corporativa de dashboards em Excel
* **GitHub** — Versionamento e histórico de código

---

##  Estrutura do Repositório
```text
Analises-quimioinformatica-2.0/
├── data/                    # Datasets de entrada e bases moleculares
├── outputs/                 # Dashboards Excel (.xlsx) e relatórios gerados (incluindo logs de excluídos)
├── src/                     # Módulos centrais do pipeline quimioinformático
├── tests/                   # Casos de teste automatizados
├── executar_pipeline.py     # Script mestre de execução do fluxo completo
├── gerar_relatorio_pdf_excel_v2.py # Script gerador do dashboard executivo v2.0
├── requirements.txt         # Dependências do projeto
└── README.md                # Documentação oficial
