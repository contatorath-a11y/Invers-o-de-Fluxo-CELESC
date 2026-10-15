"""Gera ../index.html a partir do modelo, embutindo municípios, planilha de inversão e o CSS do Leaflet.
Uso: python src/build.py"""
import json, pathlib, re

SRC = pathlib.Path(__file__).resolve().parent
ROOT = SRC.parent

html = (SRC / 'alimentadores.src.html').read_text(encoding='utf-8')
css = (SRC / 'vendor/leaflet-1.9.4.css').read_text(encoding='utf-8')
css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
css = re.sub(r'[^{}]*\{[^{}]*url\([^)]*\)[^{}]*\}', '', css)  # regras com imagens não são usadas
css = re.sub(r'\s+', ' ', css).strip()
mun = (SRC / 'data/sc-municipios.json').read_text(encoding='utf-8')
inv = json.loads((SRC / 'data/inversao-fluxo.json').read_text(encoding='utf-8'))
invs = json.dumps({'params': inv['params'], 'feeders': inv['feeders'], 'ses': inv['ses']},
                  ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')

out = (html.replace('/*__LEAFLET_CSS__*/', '/* Leaflet 1.9.4 (BSD-2) */ ' + css)
           .replace('/*__MUN__*/[]', mun)
           .replace('/*__INV__*/null', invs))
assert '__MUN__' not in out and '__LEAFLET' not in out and '__INV__' not in out
(ROOT / 'index.html').write_text(out, encoding='utf-8')
print('index.html gerado:', len(out), 'bytes')
