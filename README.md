# Localizador de Alimentadores SC

Página única (`index.html`) que estima qual alimentador e qual subestação da Celesc atendem um endereço, uma coordenada ou uma unidade consumidora em Santa Catarina. Depois de identificar o alimentador, a página mostra a **situação estimada de inversão de fluxo** segundo a planilha `Celesc_inversao_de_fluxo.xlsx`.

Tudo roda no navegador. Os arquivos da ANEEL são lidos no computador de quem usa e não são enviados para nenhum servidor.

## Como usar

1. Abra `index.html` no Chrome ou no Edge (direto do disco ou pelo endereço publicado).
2. Arraste para a página os dados públicos da ANEEL:
   - `UCMT_PJ.csv` e `UCBT_PJ.zip` (unidades consumidoras de empresas, com alimentador e coordenadas), no [portal de dados abertos da ANEEL](https://dadosabertos.aneel.gov.br/dataset/base-de-dados-geografica-da-distribuidora-bdgd);
   - a pasta `.gdb` da BDGD da Celesc, do [repositório da ANEEL](https://dadosabertos-aneel.opendata.arcgis.com/search?tags=distribuicao). A página reconhece sozinha as tabelas de medidores (EQME), unidades consumidoras (UCBT_tab, UCMT_tab), alimentadores (CTMT), subestações (SUB) e transformadores (UNTRMT).
3. Consulte por endereço, coordenada, link do Google Maps, rua ou CEP, município, lista em lote ou número da UC ou do medidor.

A base carregada fica guardada no navegador para a próxima visita.

## Inversão de fluxo

Os dados da planilha (991 alimentadores e 336 transformadores de subestação; BDGD de 31/12/2025 e GD da ANEEL de 10/10/2026) vão embutidos na página. O quadro mostra a situação estimada (com folga, atenção, no limite, inversão de fluxo provável, dedicado a usina, sem carga), o índice geração ÷ carga, os números do cálculo e a medição de fluxo reverso no transformador da subestação. As premissas (injeção da GD e limites) podem ser alteradas na própria página.

É uma triagem e não substitui o parecer de acesso da Celesc.

Para atualizar a planilha:

- **Só para quem usa:** arraste o `.xlsx` novo para a página.
- **Para todos, no repositório:**

  ```bash
  pip install openpyxl
  python src/planilha_para_json.py caminho/Celesc_inversao_de_fluxo.xlsx
  python src/build.py
  ```

## Estrutura

| Caminho | Conteúdo |
| --- | --- |
| `index.html` | Página pronta para publicar (gerada; não editar à mão) |
| `src/alimentadores.src.html` | Código-fonte da página |
| `src/build.py` | Gera `index.html` embutindo os dados abaixo |
| `src/data/sc-municipios.json` | Municípios de SC (código IBGE, nome, centro) |
| `src/data/inversao-fluxo.json` | Dados extraídos da planilha de inversão de fluxo |
| `src/planilha_para_json.py` | Converte uma versão nova da planilha para o JSON acima |
| `src/vendor/leaflet-1.9.4.css` | CSS do Leaflet (licença BSD-2), embutido no build |

## Hospedagem

`index.html` é um arquivo estático e pode ser servido por qualquer hospedagem de site estático, como GitHub Pages, Netlify ou Vercel. No Supabase, páginas HTML só são exibidas como página com domínio próprio configurado; no endereço padrão `*.supabase.co`, o HTML é entregue como texto.

## Limitações

- Estimativas por posição dependem da densidade de pontos por perto. A página indica a confiança (alta, média ou baixa).
- A BDGD é uma fotografia anual: obras e manobras depois da data-base não aparecem.
- Mapa (CARTO/OpenStreetMap) e busca de endereços (Nominatim/Photon) precisam de internet.
