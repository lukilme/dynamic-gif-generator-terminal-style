# Dynamic GIF Generator for GitHub README

Este projeto coleta dados de repositórios do GitHub e gera GIFs de dashboard para usar em um README do GitHub.

## Estrutura do projeto

```text
.
├── .github/
│   └── workflows/
├── assets/
│   └── gifs/
├── data/
│   └── github_profile.json
├── github_profile_gif/
│   ├── __init__.py
│   ├── collector.py
│   └── plotter.py
├── plots/
│   └── ... módulos dos gráficos
├── .gitignore
├── main.py
├── plot.py
├── requirements.txt
├── setup.py
└── README.md
```

## Fluxo

1. `main.py` consulta a API do GitHub e salva os dados em `data/github_profile.json`.
2. `plot.py` lê esse arquivo e gera os GIFs em `assets/gifs/`.
3. Os arquivos gerados podem ser inseridos em um README do GitHub com markdown.

## Como executar

```bash
python -m pip install -r requirements.txt
python main.py
python plot.py
```

## Observações

- Os artefatos gerados ficam fora da raiz para manter o projeto mais organizado.
- O diretório `plots/` concentra a lógica dos gráficos.
- `github_profile_gif/` centraliza a coleta e a geração do dashboard.

## Dica para README

```md
![GitHub Stats](assets/gifs/repo_sizes.gif)
```
