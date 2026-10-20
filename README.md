# Localizador de Alimentadores SC

Página única (`index.html`) que estima qual alimentador e qual subestação da Celesc atendem um endereço, uma coordenada, uma rua ou um CEP em Santa Catarina. Depois de identificar o alimentador, a página mostra a **situação estimada de inversão de fluxo** segundo a planilha `Celesc_inversao_de_fluxo.xlsx`.

Tudo roda no navegador. Quando o arquivo `base-sc.bin.gz` está publicado ao lado da página, ela já abre com a base pronta para todos os visitantes.

## Como usar

Abra o site e consulte pela aba **Ponto** (endereço, coordenada, link do Google Maps ou clique no mapa) ou pela aba **Rua ou CEP**.

## Versão 2.0 · Verificador de Rede Celesc/Solturi

Edição para o time comercial da Solturi Energia Solar, publicada em `/verificador/` (a versão 1.0 continua no endereço principal). Usa a mesma base fixa (`base-sc.bin.gz`) e a mesma planilha.

- Mostra só o **status da rede** no local (inversão de fluxo provável, no limite, atenção, com folga, dedicado a usina, sem carga), sem os números do cálculo.
- Avisa quando o ponto fica perto da divisa com outro alimentador de status diferente.
- **Limite para a proposta** (o município é o do local consultado):
  - Na regional de Jaraguá do Sul (Jaraguá do Sul, Corupá, Schroeder e Guaramirim): *no máximo um inversor de 7,5 kW, sem inclusão de beneficiária* para todo alimentador que não esteja "Com folga" (inversão de fluxo provável, no limite, atenção, dedicado a usina, sem carga ou sem status).
  - Nos demais municípios: *no máximo um inversor de 7,5 kW* quando o alimentador estiver com inversão de fluxo provável.
- **Aba "Verificar sistema":** aparece quando o local consultado fica fora da regional de Jaraguá do Sul. Mostra o local, o status e o limite, e abre o [Verificador CELESC e COPEL](https://padraocelesc.lovable.app/verificador) para conferir se o sistema apresentado ao cliente pode ser ligado. A lista da regional fica na constante `REG_JGS` do código-fonte.
- **Google Maps:** com uma chave da Maps JavaScript API em `verificador/config.json`, o mapa passa a ser o do Google (Mapa e Satélite). Sem chave, fica o mapa padrão. Os botões "Abrir no Google Maps" e "Street View" funcionam sempre.
- A caixa de carregamento de dados fica escondida. Para vê-la, abra `/verificador/#admin`.
- Identidade visual a partir do logotipo da Solturi (`src/assets/`).

### Chave do Google Maps

1. No [Google Cloud Console](https://console.cloud.google.com/google/maps-apis), crie um projeto, ative o faturamento (cartão) e ative a **Maps JavaScript API**.
2. Em **Credenciais**, crie uma chave de API. Em *Restrições de aplicativo*, escolha **Sites** e informe `https://contatorath-a11y.github.io/*`. Em *Restrições de API*, deixe só a Maps JavaScript API.
3. No GitHub, abra `verificador/config.json`, clique no lápis, cole a chave entre as aspas de `"googleMapsKey"` e confirme em **Commit changes**.

A chave fica visível no site, como em qualquer página com mapa do Google; a restrição por site impede o uso em outros endereços.

## Versão 3.0 · arquivo único para consulta

A mesma ferramenta da 2.0, num único arquivo HTML com a base embutida, para distribuir ao time por Drive, e-mail ou WhatsApp. Abre direto do computador, sem instalar nada, e serve só para consulta (não tem caixa de carregamento nem `#admin`). Precisa de internet para o mapa, a busca de endereços e o verificador. O arquivo gerado não vai para o GitHub.

```bash
python src/build.py v3 --base caminho/base-sc.bin.gz    # gera dist/verificador-3.0.html
```

## Como publicar ou atualizar a base fixa

1. Abra o site (ou `index.html` direto do disco) no Chrome ou no Edge.
2. Arraste para a caixa de arquivos os dados públicos da ANEEL:
   - `UCMT_PJ.csv`, `UCBT_PJ.zip` e `UCAT_PJ.csv` (unidades consumidoras de empresas, com alimentador e coordenadas), do [portal de dados abertos da ANEEL](https://dadosabertos.aneel.gov.br/dataset/base-de-dados-geografica-da-distribuidora-bdgd);
   - a pasta `.gdb` da BDGD da Celesc, do [repositório da ANEEL](https://dadosabertos-aneel.opendata.arcgis.com/search?tags=distribuicao). A página aproveita os transformadores (UNTRMT), os nomes dos alimentadores (CTMT) e os das subestações (SUB).
3. Quando terminar de carregar, clique em **Gerar arquivo para publicar no site**. O navegador baixa `base-sc.bin.gz`.
4. No GitHub, abra o repositório, clique em **Add file → Upload files**, arraste `base-sc.bin.gz` e confirme em **Commit changes**. O envio pelo site do GitHub aceita arquivos de até 25 MB; acima disso, use o GitHub Desktop.
5. Em um ou dois minutos o GitHub Pages atualiza. Quem abrir o site recebe a base nova; quem já tinha a anterior baixa a nova automaticamente.

Para trocar a base, repita os passos e envie o arquivo novo com o mesmo nome.

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
| `index.html` | Versão 1.0 pronta para publicar (gerada; não editar à mão) |
| `verificador/index.html` | Versão 2.0, Verificador de Rede Celesc/Solturi (gerada; não editar à mão) |
| `verificador/config.json` | Chave do Google Maps da versão 2.0 (editar à mão) |
| `base-sc.bin.gz` | Base fixa de SC carregada automaticamente pela página (gerada pelo botão da página) |
| `src/alimentadores.src.html` | Código-fonte das duas versões |
| `src/build.py` | Gera `index.html` e `verificador/index.html` embutindo os dados abaixo |
| `src/assets/` | Logotipo e ícone da Solturi usados na versão 2.0 |
| `src/data/sc-municipios.json` | Municípios de SC (código IBGE, nome, centro) |
| `src/data/inversao-fluxo.json` | Dados extraídos da planilha de inversão de fluxo |
| `src/planilha_para_json.py` | Converte uma versão nova da planilha para o JSON acima |
| `src/vendor/leaflet-1.9.4.css` | CSS do Leaflet (licença BSD-2), embutido no build |

## Hospedagem

`index.html` é um arquivo estático e pode ser servido por qualquer hospedagem de site estático, como GitHub Pages, Netlify ou Vercel. No Supabase, páginas HTML só são exibidas como página com domínio próprio configurado; no endereço padrão `*.supabase.co`, o HTML é entregue como texto.

## Licença dos dados

Os dados de origem são da ANEEL e publicados sob a licença [ODbL](https://opendatacommons.org/licenses/odbl/). A base derivada (`base-sc.bin.gz`) segue a mesma licença, com crédito à ANEEL.

## Limitações

- Estimativas por posição dependem da densidade de pontos por perto. A página indica a confiança (alta, média ou baixa).
- A BDGD é uma fotografia anual: obras e manobras depois da data-base não aparecem.
- Mapa (CARTO/OpenStreetMap ou Google Maps) e busca de endereços (Nominatim/Photon) precisam de internet.
