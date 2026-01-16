# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import io

# Configuración de la página
st.set_page_config(
    page_title="Panel de control de Ausentismo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stPlotlyChart {
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .css-1d391kg {
        padding-top: 3rem;
    }
    .filter-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Datos procesados directamente
    data = [
       
        # Carrillo Fabian
        {'Empleado': 'Carrillo Fabian', 'Mes': 'Abril', 'Ausente': 0, 'Vacaciones': 10, 'ART': 0, 'Razon': '', 'Total': 10},
        {'Empleado': 'Carrillo Fabian', 'Mes': 'Mayo', 'Ausente': 0, 'Vacaciones': 12, 'ART': 0, 'Razon': '', 'Total': 12},
       
        # Gomez
        {'Empleado': 'Gomez', 'Mes': 'Enero', 'Ausente': 0, 'Vacaciones': 17, 'ART': 0, 'Razon': '', 'Total': 17},
        {'Empleado': 'Gomez', 'Mes': 'Agosto', 'Ausente': 0, 'Vacaciones': 14, 'ART': 0, 'Razon': '', 'Total': 14},
       
        # Marcantonio Claudio
        {'Empleado': 'Marcantonio Claudio', 'Mes': 'Marzo', 'Ausente': 0, 'Vacaciones': 0, 'ART': 7, 'Razon': '', 'Total': 7},
        {'Empleado': 'Marcantonio Claudio', 'Mes': 'Agosto', 'Ausente': 3, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Cuidado hija enferma', 'Total': 3},
       
        # Marcantonio Eder
        {'Empleado': 'Marcantonio Eder', 'Mes': 'Junio', 'Ausente': 0, 'Vacaciones': 15, 'ART': 0, 'Razon': '', 'Total': 15},
        {'Empleado': 'Marcantonio Eder', 'Mes': 'Julio', 'Ausente': 0, 'Vacaciones': 25, 'ART': 0, 'Razon': '', 'Total': 25},
        
        # Pedernera Esteban
        {'Empleado': 'Pedernera Esteban', 'Mes': 'Febrero', 'Ausente': 0, 'Vacaciones': 14, 'ART': 0, 'Razon': '', 'Total': 14},
        {'Empleado': 'Pedernera Esteban', 'Mes': 'Mayo', 'Ausente': 0, 'Vacaciones': 0, 'ART': 7, 'Razon': '', 'Total': 7},
        {'Empleado': 'Pedernera Esteban', 'Mes': 'Junio', 'Ausente': 0, 'Vacaciones': 7, 'ART': 1, 'Razon': '', 'Total': 8},
        {'Empleado': 'Pedernera Esteban', 'Mes': 'Julio', 'Ausente': 0, 'Vacaciones': 17, 'ART': 0, 'Razon': '', 'Total': 17},
        {'Empleado': 'Pedernera Esteban', 'Mes': 'Octubre', 'Ausente': 0, 'Vacaciones': 0, 'ART': 3, 'Razon': '', 'Total': 3},
        {'Empleado': 'Pedernera Esteban', 'Mes': 'Noviembre', 'Ausente': 0, 'Vacaciones': 18, 'ART': 0, 'Razon': '', 'Total': 18},

        # Salas Mario
        {'Empleado': 'Salas Mario', 'Mes': 'Enero', 'Ausente': 0, 'Vacaciones': 9, 'ART': 0, 'Razon': '', 'Total': 9},
        {'Empleado': 'Salas Mario', 'Mes': 'Agosto', 'Ausente': 5, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Cuidado madre enferma', 'Total': 5},
        {'Empleado': 'Salas Mario', 'Mes': 'Septiembre', 'Ausente': 3, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Duelo', 'Total': 3},
       
        # Vilches Jonatan
        {'Empleado': 'Vilches Jonatan', 'Mes': 'Marzo', 'Ausente': 0, 'Vacaciones': 26, 'ART': 0, 'Razon': '', 'Total': 26},
        {'Empleado': 'Vilches Jonatan', 'Mes': 'Abril', 'Ausente': 0, 'Vacaciones': 2, 'ART': 0, 'Razon': '', 'Total': 2},
        
        # Diaz Raul
        {'Empleado': 'Diaz Raul', 'Mes': 'Enero', 'Ausente': 3, 'Vacaciones': 7, 'ART': 0, 'Razon': 'Cuidado sobrino', 'Total': 10},
        {'Empleado': 'Diaz Raul', 'Mes': 'Febrero', 'Ausente': 0, 'Vacaciones': 14, 'ART': 0, 'Razon': '', 'Total': 14},
        
        # Cuadrado Denis
        {'Empleado': 'Cuadrado Denis', 'Mes': 'Enero', 'Ausente': 1, 'Vacaciones': 0, 'ART': 10, 'Razon': 'Permiso gremial', 'Total': 11},
        {'Empleado': 'Cuadrado Denis', 'Mes': 'Febrero', 'Ausente': 1, 'Vacaciones': 0, 'ART': 10, 'Razon': 'Permiso gremial', 'Total': 11},
        {'Empleado': 'Cuadrado Denis', 'Mes': 'Marzo', 'Ausente': 2, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Permiso gremial', 'Total': 2},
        {'Empleado': 'Cuadrado Denis', 'Mes': 'Abril', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Permiso gremial', 'Total': 1},
        {'Empleado': 'Cuadrado Denis', 'Mes': 'Mayo', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Permiso gremial', 'Total': 1},
        {'Empleado': 'Cuadrado Denis', 'Mes': 'Junio', 'Ausente': 3, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Permiso gremial / Enfermo', 'Total': 3},
        {'Empleado': 'Cuadrado Denis', 'Mes': 'Agosto', 'Ausente': 2, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Permiso gremial', 'Total': 2},
        {'Empleado': 'Cuadrado Denis', 'Mes': 'Septiembre', 'Ausente': 3, 'Vacaciones': 0, 'ART': 1, 'Razon': 'Audiencia SRT / Audiencia Ministerio gremio', 'Total': 4},
        {'Empleado': 'Cuadrado Denis', 'Mes': 'Octubre', 'Ausente': 1, 'Vacaciones': 0, 'ART': 5, 'Razon': 'Permiso gremial', 'Total': 6},    
        {'Empleado': 'Cuadrado Denis', 'Mes': 'Noviembre', 'Ausente': 8, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Accidente laboral. Medico laboralista', 'Total': 8},
        {'Empleado': 'Cuadrado Denis', 'Mes': 'Diciembre', 'Ausente': 1, 'Vacaciones': 0, 'ART': 4, 'Razon': 'Permiso gremial', 'Total': 5},
        
        # Allais Joaquin
        {'Empleado': 'Allais Joaquin', 'Mes': 'Enero', 'Ausente': 20, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Cuidado hijo enfermo', 'Total': 20},
        {'Empleado': 'Allais Joaquin', 'Mes': 'Febrero', 'Ausente': 26, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Cuidado hijo enfermo', 'Total': 26},
        {'Empleado': 'Allais Joaquin', 'Mes': 'Marzo', 'Ausente': 21, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Cuidado hijo enfermo', 'Total': 21},
        {'Empleado': 'Allais Joaquin', 'Mes': 'Abril', 'Ausente': 0, 'Vacaciones': 12, 'ART': 0, 'Razon': '', 'Total': 12},
        {'Empleado': 'Allais Joaquin', 'Mes': 'Julio', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Cuidado hijo enfermo', 'Total': 1},
        {'Empleado': 'Allais Joaquin', 'Mes': 'Agosto', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Cuidado hijo enfermo', 'Total': 1},
        {'Empleado': 'Allais Joaquin', 'Mes': 'Septiembre', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Cuidado hijo enfermo', 'Total': 1},
        {'Empleado': 'Allais Joaquin', 'Mes': 'Diciembre', 'Ausente': 1, 'Vacaciones': 2, 'ART': 0, 'Razon': 'Cuidado hijo enfermo', 'Total': 3},

        # Lescano
        {'Empleado': 'Lescano', 'Mes': 'Enero', 'Ausente': 26, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Enfermedad. Accidente moto', 'Total': 26},
        {'Empleado': 'Lescano', 'Mes': 'Febrero', 'Ausente': 10, 'Vacaciones': 14, 'ART': 0, 'Razon': 'Enfermedad. Accidente moto', 'Total': 24},
        {'Empleado': 'Lescano', 'Mes': 'Agosto', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Enfermo', 'Total': 1},
        {'Empleado': 'Lescano', 'Mes': 'Octubre', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Permiso. Devuelve hs', 'Total': 1},
        
        # Montiel Mayco
        {'Empleado': 'Montiel Mayco', 'Mes': 'Marzo', 'Ausente': 25, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Licencia Casamiento', 'Total': 25},
        {'Empleado': 'Montiel Mayco', 'Mes': 'Julio', 'Ausente': 0, 'Vacaciones': 16, 'ART': 0, 'Razon': '', 'Total': 16},
        {'Empleado': 'Montiel Mayco', 'Mes': 'Agosto', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Permiso. Devuelve hs', 'Total': 1},
        {'Empleado': 'Montiel Mayco', 'Mes': 'Octubre', 'Ausente': 15, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Enfermo. Medico laboralista', 'Total': 15},
    
        # Romero Alejandro
        {'Empleado': 'Romero Alejandro', 'Mes': 'Mayo', 'Ausente': 0, 'Vacaciones': 21, 'ART': 0, 'Razon': '', 'Total': 21},
        {'Empleado': 'Romero Alejandro', 'Mes': 'Julio', 'Ausente': 1, 'Vacaciones': 0, 'ART': 4, 'Razon': 'Duelo', 'Total': 5},
        {'Empleado': 'Romero Alejandro', 'Mes': 'Septiembre', 'Ausente': 3, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Duelo', 'Total': 3},

        # Villafañe
        {'Empleado': 'Villafañe', 'Mes': 'Marzo', 'Ausente': 0, 'Vacaciones': 0, 'ART': 3, 'Razon': '', 'Total': 3},

        # Godoy Agustin
        {'Empleado': 'Godoy Agustin', 'Mes': 'Enero', 'Ausente': 0, 'Vacaciones': 5, 'ART': 0, 'Razon': '', 'Total': 5},
        {'Empleado': 'Godoy Agustin', 'Mes': 'Febrero', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Enfermo', 'Total': 1},
        {'Empleado': 'Godoy Agustin', 'Mes': 'Mayo', 'Ausente': 0, 'Vacaciones': 0, 'ART': 14, 'Razon': '', 'Total': 14},
        {'Empleado': 'Godoy Agustin', 'Mes': 'Julio', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Enfermo', 'Total': 1},
        {'Empleado': 'Godoy Agustin', 'Mes': 'Agosto', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Cuidado hijo enfermo', 'Total': 1},
        {'Empleado': 'Godoy Agustin', 'Mes': 'Septiembre', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Audiencia SRT', 'Total': 1},
        {'Empleado': 'Godoy Agustin', 'Mes': 'Noviembre', 'Ausente': 0, 'Vacaciones': 0, 'ART': 17, 'Razon': '', 'Total': 17},

        # Imberti Axel
        {'Empleado': 'Imberti Axel', 'Mes': 'Enero', 'Ausente': 0, 'Vacaciones': 14, 'ART': 0, 'Razon': '', 'Total': 14},
        {'Empleado': 'Imberti Axel', 'Mes': 'Julio', 'Ausente': 0, 'Vacaciones': 1, 'ART': 0, 'Razon': '', 'Total': 1},
        {'Empleado': 'Imberti Axel', 'Mes': 'Agosto', 'Ausente': 3, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Enfermo', 'Total': 3},
        {'Empleado': 'Imberti Axel', 'Mes': 'Diciembre', 'Ausente': 0, 'Vacaciones': 13, 'ART': 0, 'Razon': '', 'Total': 13},

        # Biolatto
        {'Empleado': 'Biolatto', 'Mes': 'Febrero', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Enfermo', 'Total': 1},
        {'Empleado': 'Biolatto', 'Mes': 'Abril', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Enfermo', 'Total': 1},
        {'Empleado': 'Biolatto', 'Mes': 'Julio', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Permiso. Devuelve hs', 'Total': 1},
        {'Empleado': 'Biolatto', 'Mes': 'Agosto', 'Ausente': 2, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Enfermo', 'Total': 2},
        {'Empleado': 'Biolatto', 'Mes': 'Octubre', 'Ausente': 0, 'Vacaciones': 0, 'ART': 26, 'Razon': '', 'Total': 26},
        {'Empleado': 'Biolatto', 'Mes': 'Noviembre', 'Ausente': 0, 'Vacaciones': 19, 'ART': 0, 'Razon': '', 'Total': 19},
        {'Empleado': 'Biolatto', 'Mes': 'Diciembre', 'Ausente': 0, 'Vacaciones': 5, 'ART': 0, 'Razon': '', 'Total': 5},

        # Aubert
        {'Empleado': 'Aubert', 'Mes': 'Mayo', 'Ausente': 0, 'Vacaciones': 16, 'ART': 0, 'Razon': '', 'Total': 16},
        {'Empleado': 'Aubert', 'Mes': 'Diciembre', 'Ausente': 0, 'Vacaciones': 14, 'ART': 0, 'Razon': '', 'Total': 14},

        # Montiel Jonas
        {'Empleado': 'Montiel Jonas', 'Mes': 'Abril', 'Ausente': 0, 'Vacaciones': 14, 'ART': 0, 'Razon': '', 'Total': 14},

        # Carrillo Tito
        {'Empleado': 'Carrillo Tito', 'Mes': 'Enero', 'Ausente': 0, 'Vacaciones': 0, 'ART': 26, 'Razon': '', 'Total': 26},
        {'Empleado': 'Carrillo Tito', 'Mes': 'Febrero', 'Ausente': 0, 'Vacaciones': 0, 'ART': 10, 'Razon': '', 'Total': 10},
        {'Empleado': 'Carrillo Tito', 'Mes': 'Agosto', 'Ausente': 0, 'Vacaciones': 7, 'ART': 0, 'Razon': '', 'Total': 7},
        {'Empleado': 'Carrillo Tito', 'Mes': 'Octubre', 'Ausente': 0, 'Vacaciones': 10, 'ART': 0, 'Razon': '', 'Total': 10},

        # Aguilera Facundo
        {'Empleado': 'Aguilera Facundo', 'Mes': 'Enero', 'Ausente': 0, 'Vacaciones': 7, 'ART': 0, 'Razon': '', 'Total': 7},
        {'Empleado': 'Aguilera Facundo', 'Mes': 'Febrero', 'Ausente': 0, 'Vacaciones': 14, 'ART': 0, 'Razon': '', 'Total': 14},
        {'Empleado': 'Aguilera Facundo', 'Mes': 'Diciembre', 'Ausente': 4, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Enfermo', 'Total': 4},

        # Elizagaray Santi
        {'Empleado': 'Elizagaray Santi', 'Mes': 'Enero', 'Ausente': 0, 'Vacaciones': 7, 'ART': 0, 'Razon': '', 'Total': 7},

        # Ron Octavio
        {'Empleado': 'Ron Octavio', 'Mes': 'Junio', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Permiso mudanza', 'Total': 1},
        {'Empleado': 'Ron Octavio', 'Mes': 'Noviembre', 'Ausente': 0, 'Vacaciones': 11, 'ART': 0, 'Razon': '', 'Total': 11},

        # Crespin Sebastian
        {'Empleado': 'Crespin Sebastian', 'Mes': 'Enero', 'Ausente': 0, 'Vacaciones': 14, 'ART': 0, 'Razon': '', 'Total': 14},
        {'Empleado': 'Crespin Sebastian', 'Mes': 'Mayo', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Enfermo', 'Total': 1},
        {'Empleado': 'Crespin Sebastian', 'Mes': 'Agosto', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Permiso Donacion sangre', 'Total': 1},

        # Vega David
        {'Empleado': 'Vega David', 'Mes': 'Julio', 'Ausente': 1, 'Vacaciones': 16, 'ART': 0, 'Razon': 'Licencia paternidad', 'Total': 17},

        # Arana Nicolas
        {'Empleado': 'Arana Nicolas', 'Mes': 'Mayo', 'Ausente': 2, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Enfermo', 'Total': 2},
        {'Empleado': 'Arana Nicolas', 'Mes': 'Junio', 'Ausente': 0, 'Vacaciones': 7, 'ART': 0, 'Razon': '', 'Total': 7},
        {'Empleado': 'Arana Nicolas', 'Mes': 'Octubre', 'Ausente': 9, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Enfermo. Medico laboralista', 'Total': 9},

        # Barrionuevo Sacha
        {'Empleado': 'Barrionuevo Sacha', 'Mes': 'Julio', 'Ausente': 0, 'Vacaciones': 5, 'ART': 0, 'Razon': '', 'Total': 5},

        # Torres Lucas
        {'Empleado': 'Torres Lucas', 'Mes': 'Julio', 'Ausente': 0, 'Vacaciones': 4, 'ART': 0, 'Razon': '', 'Total': 4},
        
        # Barcelona Leandro
        {'Empleado': 'Barcelona Leandro', 'Mes': 'Julio', 'Ausente': 0, 'Vacaciones': 0, 'ART': 0, 'Razon': '', 'Total': 0},
        
        # Bertaina Maxi
        {'Empleado': 'Bertaina Maxi', 'Mes': 'Julio', 'Ausente': 0, 'Vacaciones': 0, 'ART': 0, 'Razon': '', 'Total': 0},
        
    ]
    
    df = pd.DataFrame(data)
    
    # Calcular totales por empleado
    totals = df.groupby('Empleado').agg({
        'Ausente': 'sum',
        'Vacaciones': 'sum',
        'ART': 'sum',
        'Total': 'sum'
    }).reset_index()
    
    # Agregar columnas adicionales para análisis
    df['Con_Causa'] = df['Ausente'].apply(lambda x: x > 0)
    df['Razon_Categoria'] = df['Razon'].apply(categorizar_razon)
    
    return df, totals

def categorizar_razon(razon):
    """Categoriza las razones de ausencia"""
    if not razon:
        return 'Sin motivo específico'
    razon_lower = razon.lower()
    
    if 'gremial' in razon_lower:
        return 'Permiso gremial'
    elif 'cuidado' in razon_lower:
        return 'Cuidado familiar'
    elif 'enfermo' in razon_lower or 'enfermedad' in razon_lower:
        return 'Enfermedad'
    elif 'duelo' in razon_lower:
        return 'Duelo'
    elif 'permiso' in razon_lower:
        return 'Permiso personal'
    elif 'audiencia' in razon_lower or 'srt' in razon_lower:
        return 'Audiencias/Trámites'
    elif 'licencia' in razon_lower:
        return 'Licencia especial'
    elif 'laboral' in razon_lower or 'accidente' in razon_lower:
        return 'Accidente laboral'
    else:
        return 'Otros'

# Cargar datos
try:
    df, totals = load_data()
    
    # Título principal
    st.markdown('<h1 class="main-header">📊 Panel de control de Ausentismo</h1>', unsafe_allow_html=True)
    
    # Sidebar con filtros
    st.sidebar.header("🔍 Filtros Básicos")
    
    # Filtro de empleado
    all_employees = ["Todos"] + sorted(totals['Empleado'].tolist())
    selected_employee = st.sidebar.selectbox("👤 Empleado", all_employees)
    
    # Filtro de mes
    months_order = ['Todos', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    selected_month = st.sidebar.selectbox("📅 Mes", months_order)
    
    # NUEVOS FILTROS AVANZADOS
    st.sidebar.header("🎯 Filtros Avanzados")
    
    # Filtro por tipo de ausencia
    absence_types = st.sidebar.multiselect(
        "Tipo de Ausencia a Analizar",
        options=['Todos', 'Ausente', 'Vacaciones', 'ART'],
        default=['Todos']
    )
    
    # Filtro por categoría de razón
    razones_categorias = ['Todos'] + sorted(df[df['Razon'] != '']['Razon_Categoria'].unique().tolist())
    selected_categoria = st.sidebar.selectbox("Categoría de Razón", razones_categorias)
    
    # Filtro por rango de días
    st.sidebar.header("📊 Rango de Días")
    min_days = st.sidebar.number_input("Mínimo de días", min_value=0, max_value=365, value=0)
    max_days = st.sidebar.number_input("Máximo de días", min_value=0, max_value=365, value=365)
    
    # Filtro para métrica del top
    top_metric_options = {
        'Total': 'Total',
        'Ausente con causa': 'Ausente',
        'Vacaciones': 'Vacaciones',
        'ART': 'ART',
        'Promedio por mes': 'Promedio_Mes'
    }
    selected_top_metric = st.sidebar.selectbox(
        "Métrica para Top Empleados",
        list(top_metric_options.keys()),
        index=0
    )
    
    # Filtro para mostrar solo ausencias con causa
    show_only_with_reason = st.sidebar.checkbox("Mostrar solo ausencias con causa justificada")
    
    # Aplicar filtros básicos
    filtered_df = df.copy()
    filtered_totals = totals.copy()
    
    if selected_employee != "Todos":
        filtered_df = filtered_df[filtered_df['Empleado'] == selected_employee]
        filtered_totals = filtered_totals[filtered_totals['Empleado'] == selected_employee]
    
    if selected_month != "Todos":
        filtered_df = filtered_df[filtered_df['Mes'] == selected_month]
    
    # Aplicar filtros avanzados
    # Filtro por tipo de ausencia
    if 'Todos' not in absence_types and absence_types:
        # Filtrar por los tipos seleccionados
        # Para el top, necesitamos recalcular los totales
        filtered_totals['Total_Filtrado'] = 0
        for tipo in absence_types:
            if tipo in filtered_totals.columns:
                filtered_totals['Total_Filtrado'] += filtered_totals[tipo]
        filtered_totals = filtered_totals[filtered_totals['Total_Filtrado'] > 0]
    
    # Filtro por categoría de razón
    if selected_categoria != "Todos":
        razones_filtradas = df[df['Razon_Categoria'] == selected_categoria]['Razon'].unique()
        filtered_df = filtered_df[filtered_df['Razon'].isin(razones_filtradas) | (filtered_df['Razon'] == '')]
    
    # Filtro por rango de días
    filtered_totals = filtered_totals[
        (filtered_totals['Total'] >= min_days) & 
        (filtered_totals['Total'] <= max_days)
    ]
    
    # Filtrar solo ausencias con causa
    if show_only_with_reason:
        filtered_df = filtered_df[filtered_df['Ausente'] > 0]
    
    # Métricas principales
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="👥 Total Empleados",
            value=len(filtered_totals),
            delta=f"{len(filtered_totals[filtered_totals['Total'] > 0])} con faltas"
        )
    
    with col2:
        total_days = filtered_totals['Total'].sum()
        avg_days = total_days/len(filtered_totals) if len(filtered_totals) > 0 else 0
        st.metric(
            label="📅 Días Totales",
            value=f"{total_days:,}",
            delta=f"Promedio: {avg_days:.1f}"
        )
    
    with col3:
        vac_percent = filtered_totals['Vacaciones'].sum()/total_days*100 if total_days > 0 else 0
        st.metric(
            label="🏖️ Vacaciones",
            value=f"{filtered_totals['Vacaciones'].sum():,}",
            delta=f"{vac_percent:.1f}%"
        )
    
    with col4:
        art_percent = filtered_totals['ART'].sum()/total_days*100 if total_days > 0 else 0
        st.metric(
            label="⚠️ ART",
            value=f"{filtered_totals['ART'].sum():,}",
            delta=f"{art_percent:.1f}%"
        )
    
    with col5:
        # Calcular días totales trabajables
        num_empleados = len(filtered_totals) if len(filtered_totals) > 0 else 30
        dias_trabajables = 5 * 52 * num_empleados  # 260 días por empleado
        
        # Días de ausentismo (Ausente + ART, SIN vacaciones)
        dias_ausentismo = filtered_totals['Ausente'].sum() + filtered_totals['ART'].sum()
        
        # Porcentaje
        porcentaje_ausentismo = (dias_ausentismo / dias_trabajables * 100) if dias_trabajables > 0 else 0
        
        st.metric(
            label="📊 % Ausentismo",
            value=f"{porcentaje_ausentismo:.2f}%",
            delta=f"{dias_ausentismo} días"
        )

    # Tabs principales
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Panel de control", "👤 Análisis Individual", "🔍 Análisis Detallado", "💾 Exportar"])
    
    with tab1:
        # Gráficos principales
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Top empleados con métrica seleccionada
            st.subheader(f"🏆 Top Empleados - {selected_top_metric}")
            
            # Preparar datos para el top según la métrica seleccionada
            if selected_top_metric == 'Promedio por mes':
                # Calcular promedio por mes
                top_data = filtered_totals.copy()
                top_data['Meses_Con_Ausencias'] = filtered_df.groupby('Empleado')['Mes'].nunique()
                top_data['Promedio_Mes'] = top_data['Total'] / top_data['Meses_Con_Ausencias']
                top_data = top_data.nlargest(10, 'Promedio_Mes')
                metric_col = 'Promedio_Mes'
            else:
                metric_col = top_metric_options[selected_top_metric]
                top_data = filtered_totals.nlargest(10, metric_col)
            
            if not top_data.empty:
                fig_top = px.bar(
                    top_data, x=metric_col, y='Empleado', orientation='h',
                    color=metric_col, color_continuous_scale='Reds',
                    text=metric_col, height=400
                )
                fig_top.update_layout(showlegend=False)
                fig_top.update_traces(textposition='outside')
                st.plotly_chart(fig_top, use_container_width=True)
            else:
                st.info("No hay datos para mostrar")
        
        with col2:
            # Distribución por tipo (puede ser filtrada)
            st.subheader("📊 Distribución por tipo")
            if 'Todos' in absence_types or not absence_types:
                # Mostrar todos los tipos
                total_types = filtered_totals[['Ausente', 'Vacaciones', 'ART']].sum()
                tipos_a_mostrar = ['Ausente', 'Vacaciones', 'ART']
            else:
                # Mostrar solo los tipos seleccionados
                total_types = filtered_totals[absence_types].sum()
                tipos_a_mostrar = absence_types
            
            if total_types.sum() > 0:
                fig_pie = px.pie(
                    values=[total_types[tipo] for tipo in tipos_a_mostrar],
                    names=tipos_a_mostrar,
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("No hay datos para mostrar")
        
        # Evolución mensual con opción de seleccionar tipos
        st.subheader("📅 Evolución mensual")
        
        # Selector para tipos en el gráfico de evolución
        tipos_evolucion = st.multiselect(
            "Selecciona tipos para la evolución mensual",
            options=['Ausente', 'Vacaciones', 'ART'],
            default=['Ausente', 'Vacaciones', 'ART']
        )
        
        if tipos_evolucion:
            monthly = filtered_df.groupby('Mes')[tipos_evolucion].sum()
            months_order_list = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                                'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
            monthly = monthly.reindex([m for m in months_order_list if m in monthly.index], fill_value=0)
            
            if not monthly.empty:
                fig_monthly = px.bar(
                    monthly, barmode='group',
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    height=400
                )
                fig_monthly.update_layout(xaxis_title="Mes", yaxis_title="Días")
                st.plotly_chart(fig_monthly, use_container_width=True)
            else:
                st.info("No hay datos mensuales para mostrar")
    
    with tab2:
        if selected_employee != "Todos":
            st.header(f"👤 Análisis detallado - {selected_employee}")
            
            emp_data = filtered_df[filtered_df['Empleado'] == selected_employee]
            emp_total = filtered_totals[filtered_totals['Empleado'] == selected_employee]
            
            if not emp_total.empty:
                emp_total_row = emp_total.iloc[0]
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total de días", emp_total_row['Total'])
                with col2:
                    st.metric("Días ausente", emp_total_row['Ausente'])
                with col3:
                    st.metric("Días de vacaciones", emp_total_row['Vacaciones'])
                with col4:
                    st.metric("Días ART", emp_total_row['ART'])
                with col5:
                    # Días trabajables por empleado individual (260 por año)
                    dias_trabajables_emp = 260
                    
                    # Ausentismo individual (Ausente + ART, sin vacaciones)
                    dias_ausentismo_emp = emp_total_row['Ausente'] + emp_total_row['ART']
                    
                    # Porcentaje individual
                    porcentaje_ausentismo_emp = (dias_ausentismo_emp / dias_trabajables_emp * 100) if dias_trabajables_emp > 0 else 0
                    
                    st.metric(
                        "% Ausentismo", 
                        f"{porcentaje_ausentismo_emp:.2f}%"
                    )
                # Gráficos del empleado
                col1, col2 = st.columns(2)
                
                with col1:
                    # Distribución
                    fig_emp_pie = px.pie(
                        values=[emp_total_row['Ausente'], emp_total_row['Vacaciones'], emp_total_row['ART']],
                        names=['Ausente', 'Vacaciones', 'ART'],
                        color_discrete_sequence=px.colors.qualitative.Set3,
                        title=f"Distribución - {selected_employee}"
                    )
                    st.plotly_chart(fig_emp_pie, use_container_width=True)
                
                with col2:
                    # Evolución mensual
                    monthly_emp = emp_data.groupby('Mes')[['Ausente', 'Vacaciones', 'ART']].sum()
                    months_order_list = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                                        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
                    monthly_emp = monthly_emp.reindex([m for m in months_order_list if m in monthly_emp.index], fill_value=0)
                    
                    if not monthly_emp.empty:
                        fig_emp_monthly = px.bar(
                            monthly_emp, barmode='group',
                            color_discrete_sequence=px.colors.qualitative.Set3,
                            title=f"Evolución mensual - {selected_employee}"
                        )
                        st.plotly_chart(fig_emp_monthly, use_container_width=True)
                    else:
                        st.info("No hay datos mensuales para este empleado")
                
                # Razones de ausencia con análisis
                razones = emp_data[emp_data['Razon'] != ''][['Mes', 'Ausente', 'Razon', 'Razon_Categoria']]
                if not razones.empty:
                    st.subheader("📝 Razones de ausencia")
                    
                    # Resumen por categoría
                    st.write("**Resumen por categoría:**")
                    categoria_resumen = razones.groupby('Razon_Categoria')['Ausente'].sum().reset_index()
                    st.dataframe(categoria_resumen)
                    
                    st.write("**Detalle por mes:**")
                    for _, row in razones.iterrows():
                        st.write(f"**{row['Mes']}**: {row['Ausente']} días - {row['Razon']} (*{row['Razon_Categoria']}*)")
            else:
                st.info("No hay datos para este empleado")
        else:
            st.info("👆 Selecciona un empleado en el sidebar para ver su análisis detallado")
    
    with tab3:
        st.header("🔍 Análisis Detallado")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Análisis de razones por categoría
            st.subheader("📋 Análisis de Razones por Categoría")
            razones_analisis = filtered_df[filtered_df['Razon'] != ''].copy()
            
            if not razones_analisis.empty:
                # Gráfico de razones por categoría
                razones_cat = razones_analisis.groupby('Razon_Categoria')['Ausente'].sum().reset_index()
                razones_cat = razones_cat.sort_values('Ausente', ascending=False)
                
                fig_razones = px.bar(
                    razones_cat, x='Ausente', y='Razon_Categoria', orientation='h',
                    color='Ausente', color_continuous_scale='Blues',
                    title="Días de ausencia por categoría de razón"
                )
                st.plotly_chart(fig_razones, use_container_width=True)
                
                # Tabla detallada
                st.subheader("📊 Detalle por Razón")
                razones_detalle = razones_analisis.groupby(['Razon_Categoria', 'Razon'])['Ausente'].sum().reset_index()
                st.dataframe(razones_detalle.sort_values('Ausente', ascending=False))
            else:
                st.info("No hay ausencias con razones especificadas en los filtros actuales")
        
        with col2:
            # Análisis comparativo por mes
            st.subheader("📅 Comparativa Mensual")
            
            # Selector de métrica para comparación
            comparacion_metric = st.selectbox(
                "Métrica para comparación mensual",
                ['Total', 'Ausente', 'Vacaciones', 'ART'],
                key='comparacion_metric'
            )
            
            monthly_comparison = filtered_df.groupby('Mes')[comparacion_metric].sum()
            months_order_list = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                                'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
            monthly_comparison = monthly_comparison.reindex([m for m in months_order_list if m in monthly_comparison.index], fill_value=0)
            
            if not monthly_comparison.empty:
                fig_comparison = px.line(
                    x=monthly_comparison.index,
                    y=monthly_comparison.values,
                    markers=True,
                    title=f"Evolución de {comparacion_metric} por mes"
                )
                fig_comparison.update_layout(xaxis_title="Mes", yaxis_title="Días")
                st.plotly_chart(fig_comparison, use_container_width=True)
            else:
                st.info("No hay datos para la comparación mensual")
            
            # Estadísticas descriptivas
            st.subheader("📈 Estadísticas Descriptivas")
            if not filtered_totals.empty:
                stats_data = {
                    'Métrica': ['Total', 'Ausente', 'Vacaciones', 'ART'],
                    'Promedio': [
                        filtered_totals['Total'].mean(),
                        filtered_totals['Ausente'].mean(),
                        filtered_totals['Vacaciones'].mean(),
                        filtered_totals['ART'].mean()
                    ],
                    'Máximo': [
                        filtered_totals['Total'].max(),
                        filtered_totals['Ausente'].max(),
                        filtered_totals['Vacaciones'].max(),
                        filtered_totals['ART'].max()
                    ],
                    'Mínimo': [
                        filtered_totals['Total'].min(),
                        filtered_totals['Ausente'].min(),
                        filtered_totals['Vacaciones'].min(),
                        filtered_totals['ART'].min()
                    ],
                    'Desviación': [
                        filtered_totals['Total'].std(),
                        filtered_totals['Ausente'].std(),
                        filtered_totals['Vacaciones'].std(),
                        filtered_totals['ART'].std()
                    ]
                }
                stats_df = pd.DataFrame(stats_data)
                st.dataframe(stats_df.round(2))
    
    with tab4:
        st.header("💾 Exportar datos")
        
        # Preparar datos para exportar
        excel_buffer = io.BytesIO()
        
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            filtered_totals.to_excel(writer, sheet_name='Resumen_por_empleado', index=False)
            filtered_df.to_excel(writer, sheet_name='Detalle_mensual', index=False)
            
            # Resumen mensual
            monthly_export = filtered_df.groupby('Mes')[['Ausente', 'Vacaciones', 'ART']].sum()
            monthly_export.to_excel(writer, sheet_name='Resumen_mensual')
            
            # Análisis de razones
            if 'Razon_Categoria' in filtered_df.columns:
                razones_export = filtered_df[filtered_df['Razon'] != ''].groupby(['Razon_Categoria', 'Razon']).agg({
                    'Ausente': 'sum',
                    'Empleado': 'count'
                }).rename(columns={'Empleado': 'Cantidad_Registros'})
                razones_export.to_excel(writer, sheet_name='Analisis_Razones')
        
        excel_buffer.seek(0)
        
        st.download_button(
            label="📥 Descargar Excel con todos los datos",
            data=excel_buffer,
            file_name=f"analisis_ausentismo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        # Opciones de exportación específicas
        col1, col2 = st.columns(2)
        
        with col1:
            # Exportar solo resumen
            if st.button("📋 Exportar solo resumen por empleado"):
                csv_resumen = filtered_totals.to_csv(index=False)
                st.download_button(
                    label="⬇️ Descargar CSV Resumen",
                    data=csv_resumen,
                    file_name=f"resumen_ausentismo_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            # Exportar detalle
            if st.button("📄 Exportar detalle completo"):
                csv_detalle = filtered_df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Descargar CSV Detalle",
                    data=csv_detalle,
                    file_name=f"detalle_ausentismo_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        
        # Vista previa de datos
        if st.checkbox("👁️ Ver vista previa de datos"):
            st.subheader("Resumen por empleado")
            st.dataframe(filtered_totals)
            
            st.subheader("Detalle mensual")
            st.dataframe(filtered_df)
            
            if 'Razon_Categoria' in filtered_df.columns:
                st.subheader("Análisis de razones")
                razones_preview = filtered_df[filtered_df['Razon'] != ''].groupby('Razon_Categoria')['Ausente'].sum().reset_index()
                st.dataframe(razones_preview)

except Exception as e:
    st.error(f"Error al cargar los datos: {str(e)}")
    st.info("Por favor, verifica que todos los datos estén correctamente procesados.")

# Footer
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center'>
        <p>Dashboard creado con Streamlit • 📊 Datos actualizados a {datetime.now().strftime("%d/%m/%Y %H:%M")}</p>
    </div>
    """,
    unsafe_allow_html=True
)