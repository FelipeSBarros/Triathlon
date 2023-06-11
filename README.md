# Trathlon

Repositório criado para analisar e comparar os dados das provas de triathlon e de treinamento.


## Preparando ambiente de desenvolvimento

```commandline
git clone git@github.com:FelipeSBarros/Triathlon.git
cd Triathlon/triathlon
poetry install
```

## Convertendo GPX para Geopackage

O [convert_gpx2gpkg](./convert_gpx2gpkg.py) irá identificar todos os arquivos `gpx` na pasta **gpx-files** e exportará as camadas `track_points` para o `./data/Triathlon.gpkg`. E ainda converterá o `track_points` em um dados de linha usando o [movingpandas](https://movingpandas.readthedocs.io/en/main/), para poder [calcular alguns parâmetros](convert_gpx2gpkg.py#L55) da trajetória e o salvará no mesmo geopackage.
```commandline
python convert_gpx2gpkg.py
```
