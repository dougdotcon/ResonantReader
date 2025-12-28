# ResonantReader Backend Architecture

Este diretório contém a lógica "Cérebro" do produto.

## Arquivos

1.  **`engine.py` (The Physics):**
    *   Simula Osciladores de Kuramoto.
    *   Responsável pela "Navegação Ressonante" (King -> Queen).
    *   Atualmente (v2.5) usa dados hardcoded.

2.  **`bitnet_core.py` (The Brain - NEW):**
    *   Implementa o algoritmo **BitNet b1.58** (Pesos Ternários).
    *   Serve para **APRENDER** padrões de textos reais (PDFs).
    *   Economiza 16x de memória comparado a redes normais.

3.  **`bridge.py` (The Glue):**
    *   Conecta o Python ao Frontend (React) gerando o arquivo `constants.ts`.

## Roadmap de Integração (v3.0)

Para transformar o protótipo em produto real:

1.  **Ingestão de Dados:** Criar script que lê PDF e converte em vetores (One-Hot ou TF-IDF).
2.  **Treinamento:** Alimentar esses vetores no `ResonantBitNet` (em `bitnet_core.py`).
3.  **Transferência:** Pegar a matriz aprendida (`J_final`) do BitNet e injetá-la no `K_matrix` do `engine.py`.
4.  **Resultado:** O grafo na tela será o "Mapa Mental" real do PDF do usuário, aprendido via pesos ternários.
