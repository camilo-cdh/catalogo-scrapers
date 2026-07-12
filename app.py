import json
import streamlit as st

st.set_page_config(page_title="Catálogo Scrapers", layout="wide")
st.title("Catálogo de Productos - Base de datos Proyecto Code con Pebre")

# Cargar JSON
try:
    with open("productos.json", "r", encoding="utf-8") as f:
        productos = json.load(f)
except Exception as e:
    st.error(f"No se pudo cargar productos.json: {e}")
    st.stop()

# Sidebar
st.sidebar.header("Filtros")

def normalizar_categoria(cat):
    return cat if cat else "(sin categoría)"


categorias = ["Todos los productos"] + sorted(set(normalizar_categoria(p.get("categoria", "")) for p in productos))

filtro_categoria = st.sidebar.selectbox("Categoría", categorias, index=0)

if filtro_categoria == "Todos los productos":
    productos_filtrados = productos
else:
    productos_filtrados = [
        p for p in productos
        if normalizar_categoria(p.get("categoria", "")) == filtro_categoria
    ]

st.sidebar.write(f"Productos visibles: {len(productos_filtrados)}")
st.sidebar.markdown("---")

# Botón de descarga del JSON
st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.write(f"**Descarga la base de datos**")
st.sidebar.download_button(
    label="📥 Descargar productos.json",
    data=json.dumps(productos, ensure_ascii=False, indent=2),
    file_name="productos.json",
    mime="application/json"
)

with st.container():
    # Grid 5 por fila
    num_cols = 5
    for i in range(0, len(productos_filtrados), num_cols):
        fila = productos_filtrados[i:i + num_cols]
        cols = st.columns(len(fila))

        for idx, p in enumerate(fila):
            with cols[idx]:
                # Imagen
                imagen_url = p.get("imagen_url", "")
                if imagen_url:
                    st.image(imagen_url, width='stretch')
                else:
                    st.write("Sin imagen")

                # Nombre
                st.subheader(p.get("nombre", ""))

                # Categoría y productor
                st.write(f"**Categoría:** {p.get('categoria', '')}")
                st.write(f"**Productor:** {p.get('productor', '')}")

                # Precio
                precio = p.get("precio", "")
                if isinstance(precio, (int, float)):
                    precio_formateado = f"{precio:,}".replace(",", ".")
                    st.write(f"**Precio:** ${precio_formateado} CLP")
                else:
                    st.write("**Precio:** ")

                # Descripción
                descripcion = p.get("descripcion", "")
                if descripcion:
                    st.write(f"**Descripción:** {descripcion}")

                fuente = p.get('fuente', '')
                fuente_url = p.get("fuente_url", "")

                if fuente_url:
                    st.markdown(f"**Fuente:** [{fuente}]({fuente_url})")

                producto_url = p.get("producto_url", "")
                if producto_url:
                    st.markdown(f"[Ver producto]({producto_url})")
