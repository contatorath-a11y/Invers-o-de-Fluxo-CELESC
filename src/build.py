"""Gera as edições da página a partir do mesmo modelo.

  python src/build.py            → index.html (1.0) e verificador/index.html (2.0), publicadas no site
  python src/build.py v3 [--base caminho/base-sc.bin.gz] [--out caminho.html] [--gkey CHAVE]
                                 → 3.0: arquivo único, só para consulta, com a base embutida.
                                   Não vai para o GitHub (padrão: dist/verificador-3.0.html, fora do Git).
"""
import argparse, base64, html, json, pathlib, re

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
SOLTURI = dict(
    TITLE='Verificador de Rede Celesc/Solturi',
    SUBTITLE='Status da rede Celesc no endereço do cliente · Solturi Energia Solar',
    DESC='Ferramenta do time comercial da Solturi Energia Solar: mostra o status de inversão de fluxo do alimentador da Celesc no endereço do cliente.',
    FOOT='Status estimado a partir da base pública da ANEEL (BDGD) e da planilha de inversão de fluxo. A rede muda com obras e manobras; '
         'a palavra final é o parecer de acesso da Celesc. Busca de endereços por © colaboradores do OpenStreetMap.',
    BRANDMARK=f'<img class="brand-logo" src="{data_uri("assets/solturi-logo.jpg", "image/jpeg")}" alt="Solturi Energia Solar">',
    FAVICON=f'<link rel="icon" href="{data_uri("assets/solturi-favicon.png", "image/png")}">')
EDITIONS = {
    'v1': dict(
        edition='v1', out=ROOT / 'index.html',
        TITLE='Localizador de Alimentadores SC',
        SUBTITLE='Endereço ou coordenada → alimentador e subestação, pela base pública BDGD/ANEEL',
        DESC='Estima o alimentador de média tensão que atende um endereço ou coordenada em Santa Catarina, a partir da BDGD publicada pela ANEEL.',
        FOOT='Estimativa a partir da Base de Dados Geográfica da Distribuidora (BDGD), publicada anualmente pela ANEEL. A rede muda: '
             'alimentadores novos e manobras podem alterar o atendimento depois da data-base. Busca de endereços por © colaboradores do OpenStreetMap.',
        BRANDMARK=MARK_V1, FAVICON=''),
    'v2': dict(edition='v2', out=ROOT / 'verificador' / 'index.html', **SOLTURI),
    'v3': dict(edition='v2', out=ROOT / 'dist' / 'verificador-3.0.html',
               **{**SOLTURI, 'SUBTITLE': SOLTURI['SUBTITLE'] + ' · versão 3.0'}),
}


def build(ed, base=None, out=None, gkey=''):
    cfg = EDITIONS[ed]
    page = (tpl.replace('/*__LEAFLET_CSS__*/', '/* Leaflet 1.9.4 (BSD-2) */ ' + css)
               .replace('/*__MUN__*/[]', mun)
               .replace('/*__INV__*/null', invs)
               .replace('{{EDITION}}', cfg['edition'])
               .replace('{{BUILD}}', ed)
               .replace('{{GKEY}}', html.escape(gkey, quote=True)))
    # trechos marcados <!--V2-->…<!--/V2--> só existem nas edições Solturi (2.0 e 3.0)
    page = re.sub(r'<!--V2-->(.*?)<!--/V2-->', (lambda m: m.group(1)) if cfg['edition'] == 'v2' else '', page, flags=re.S)
    for key in ('TITLE', 'SUBTITLE', 'DESC', 'FOOT'):
        page = page.replace('{{' + key + '}}', html.escape(cfg[key], quote=True))
    page = page.replace('{{BRANDMARK}}', cfg['BRANDMARK']).replace('{{FAVICON}}', cfg['FAVICON'])
    blob = ''
    if ed == 'v3':
        raw = pathlib.Path(base or ROOT / 'base-sc.bin.gz').read_bytes()
        assert raw[:2] == b'\x1f\x8b', 'a base precisa ser o arquivo base-sc.bin.gz gerado pela página'
        blob = '<script type="application/octet-stream" id="baseData">' + base64.b64encode(raw).decode() + '</script>\n'
    page = page.replace('<!--BASEDATA-->', blob)
    assert '{{' not in page and '__MUN__' not in page and '__LEAFLET' not in page and '__INV__' not in page
    dest = pathlib.Path(out) if out else cfg['out']
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page, encoding='utf-8')
    print(f'{ed}: {dest} ({len(page) / 1048576:.1f} MB)')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('edition', nargs='?', choices=['v3'])
    ap.add_argument('--base'); ap.add_argument('--out'); ap.add_argument('--gkey', default='')
    a = ap.parse_args()
    if a.edition == 'v3':
        build('v3', a.base, a.out, a.gkey)
    else:
        build('v1'); build('v2')
