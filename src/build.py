"""Gera as duas edições da página a partir do mesmo modelo:
  index.html             → 1.0 · Localizador de Alimentadores SC
  verificador/index.html → 2.0 · Verificador de Rede Celesc/Solturi
Uso: python src/build.py"""
import base64, html, json, pathlib, re

SRC = pathlib.Path(__file__).resolve().parent
ROOT = SRC.parent

tpl = (SRC / 'alimentadores.src.html').read_text(encoding='utf-8')
css = (SRC / 'vendor/leaflet-1.9.4.css').read_text(encoding='utf-8')
css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
css = re.sub(r'[^{}]*\{[^{}]*url\([^)]*\)[^{}]*\}', '', css)  # regras com imagens não são usadas
css = re.sub(r'\s+', ' ', css).strip()
mun = (SRC / 'data/sc-municipios.json').read_text(encoding='utf-8')
inv = json.loads((SRC / 'data/inversao-fluxo.json').read_text(encoding='utf-8'))
invs = json.dumps({'params': inv['params'], 'feeders': inv['feeders'], 'ses': inv['ses']},
                  ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')


def data_uri(path, mime):
    return f'data:{mime};base64,' + base64.b64encode((SRC / path).read_bytes()).decode()


MARK_V1 = ('<svg width="40" height="28" viewBox="0 0 40 28" aria-hidden="true"><circle cx="14" cy="14" r="10" fill="none" '
           'stroke="var(--ink)" stroke-width="2.5"/><circle cx="26" cy="14" r="10" fill="none" stroke="var(--accent)" stroke-width="2.5"/></svg>')
EDITIONS = {
    'v1': dict(
        out=ROOT / 'index.html',
        TITLE='Localizador de Alimentadores SC',
        SUBTITLE='Endereço ou coordenada → alimentador e subestação, pela base pública BDGD/ANEEL',
        DESC='Estima o alimentador de média tensão que atende um endereço ou coordenada em Santa Catarina, a partir da BDGD publicada pela ANEEL.',
        FOOT='Estimativa a partir da Base de Dados Geográfica da Distribuidora (BDGD), publicada anualmente pela ANEEL. A rede muda: '
             'alimentadores novos e manobras podem alterar o atendimento depois da data-base. Busca de endereços por © colaboradores do OpenStreetMap.',
        BRANDMARK=MARK_V1, FAVICON=''),
    'v2': dict(
        out=ROOT / 'verificador' / 'index.html',
        TITLE='Verificador de Rede Celesc/Solturi',
        SUBTITLE='Status da rede Celesc no endereço do cliente · Solturi Energia Solar',
        DESC='Ferramenta do time comercial da Solturi Energia Solar: mostra o status de inversão de fluxo do alimentador da Celesc no endereço do cliente.',
        FOOT='Status estimado a partir da base pública da ANEEL (BDGD) e da planilha de inversão de fluxo. A rede muda com obras e manobras; '
             'a palavra final é o parecer de acesso da Celesc. Busca de endereços por © colaboradores do OpenStreetMap.',
        BRANDMARK=f'<img class="brand-logo" src="{data_uri("assets/solturi-logo.jpg", "image/jpeg")}" alt="Solturi Energia Solar">',
        FAVICON=f'<link rel="icon" href="{data_uri("assets/solturi-favicon.png", "image/png")}">'),
}

for ed, cfg in EDITIONS.items():
    out = (tpl.replace('/*__LEAFLET_CSS__*/', '/* Leaflet 1.9.4 (BSD-2) */ ' + css)
              .replace('/*__MUN__*/[]', mun)
              .replace('/*__INV__*/null', invs)
              .replace('{{EDITION}}', ed))
    for key in ('TITLE', 'SUBTITLE', 'DESC', 'FOOT'):
        out = out.replace('{{' + key + '}}', html.escape(cfg[key], quote=True))
    out = out.replace('{{BRANDMARK}}', cfg['BRANDMARK']).replace('{{FAVICON}}', cfg['FAVICON'])
    assert '{{' not in out and '__MUN__' not in out and '__LEAFLET' not in out and '__INV__' not in out
    cfg['out'].parent.mkdir(parents=True, exist_ok=True)
    cfg['out'].write_text(out, encoding='utf-8')
    print(f'{ed}: {cfg["out"].relative_to(ROOT)} ({len(out)} bytes)')
