import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# Carregar arquivos (coloque o caminho correto localmente ou no servidor do Streamlit)
bairros_cwb = gpd.read_file("https://github.com/LuiizOt/Desenvolvimento_2025/blob/e7c569830872c78fc62183b6a6729b777f34d9e7/DIVISA_DE_BAIRROS.shp").to_crs(epsg=4326)
escolas = gpd.read_file("https://github.com/LuiizOt/Desenvolvimento_2025/blob/e7c569830872c78fc62183b6a6729b777f34d9e7/ESCOLA_MUNICIPAL.shp").to_crs(epsg=4326)

# Sidebar para seleção do bairro
st.sidebar.title('Selecione o Bairro')
bairros_cwb = bairros_cwb.sort_values('NOME')
bairro_nome = st.sidebar.selectbox(
    "Bairro:",
    bairros_cwb['NOME']
)

# Encontrar o código do bairro selecionado
codigo = bairros_cwb[bairros_cwb['NOME'] == bairro_nome]['CODIGO'].values[0]

# Filtrar o bairro selecionado
selecionado = bairros_cwb[bairros_cwb['CODIGO'] == codigo]

# Centroide para centralizar o mapa
centro = selecionado.geometry.iloc[0].centroid
lat, lon = centro.y, centro.x

# Escolas dentro do bairro
e_selec = escolas[escolas.within(selecionado.geometry.iloc[0])]

# Criar o mapa
m = folium.Map(location=[lat, lon], zoom_start=12)

# Adicionar camada do bairro
folium.GeoJson(
    selecionado.__geo_interface__,
    name="Bairro informado",
    style_function=lambda feature: {
        'fillColor': 'blue',
        'color': 'black',
        'fillOpacity': 0.5,
        'weight': 2,
    }
).add_to(m)

# Adicionar marcadores de escolas
for _, escola in e_selec.iterrows():
    coords = escola.geometry
    folium.Marker(
        location=[coords.y, coords.x],
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Exibir o mapa
st_data = st_folium(m, width=700, height=500)
