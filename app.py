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
    page_title="Panel de control de Ausentismo 2024-2025",
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
    .year-comparison {
        border-left: 5px solid #1f77b4;
        padding-left: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Datos de 2024
    data_2024 = [
    {'Empleado': 'Carrillo Fabian', 'Mes': 'Mayo', 'Ausente': 0, 'Vacaciones': 16, 'ART': 0, 'Razon': '', 'Total': 16},
    {'Empleado': 'Carrillo Fabian', 'Mes': 'Agosto', 'Ausente': 2, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Duelo', 'Total': 2},
    {'Empleado': 'Carrillo Fabian', 'Mes': 'Octubre', 'Ausente': 0, 'Vacaciones': 14, 'ART': 0, 'Razon': '', 'Total': 14},
    {'Empleado': 'Carrillo Fabian', 'Mes': 'Noviembre', 'Ausente': 0, 'Vacaciones': 0, 'ART': 26, 'Razon': '', 'Total': 26},

    {'Empleado': 'Gomez', 'Mes': 'Febrero', 'Ausente': 0, 'Vacaciones': 11, 'ART': 0, 'Razon': '', 'Total': 11},
    
    {'Empleado': 'Marcantonio Claudio', 'Mes': 'Febrero', 'Ausente': 0, 'Vacaciones': 14, 'ART': 0, 'Razon': '', 'Total': 14},
    {'Empleado': 'Marcantonio Claudio', 'Mes': 'Marzo', 'Ausente': 0, 'Vacaciones': 2, 'ART': 0, 'Razon': '', 'Total': 2},
    {'Empleado': 'Marcantonio Claudio', 'Mes': 'Mayo', 'Ausente': 0, 'Vacaciones': 7, 'ART': 0, 'Razon': '', 'Total': 7},
    {'Empleado': 'Marcantonio Claudio', 'Mes': 'Junio', 'Ausente': 0, 'Vacaciones': 9, 'ART': 0, 'Razon': '', 'Total': 9},
    {'Empleado': 'Marcantonio Claudio', 'Mes': 'Julio', 'Ausente': 3, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Duelo', 'Total': 3},
    {'Empleado': 'Marcantonio Claudio', 'Mes': 'Octubre', 'Ausente': 0, 'Vacaciones': 18, 'ART': 0, 'Razon': '', 'Total': 18},
    {'Empleado': 'Marcantonio Claudio', 'Mes': 'Noviembre', 'Ausente': 0, 'Vacaciones': 17, 'ART': 0, 'Razon': '', 'Total': 17},
    
    {'Empleado': 'Marcantonio Eder', 'Mes': 'Enero', 'Ausente': 0, 'Vacaciones': 14, 'ART': 0, 'Razon': '', 'Total': 14},
    {'Empleado': 'Marcantonio Eder', 'Mes': 'Febrero', 'Ausente': 0, 'Vacaciones': 18, 'ART': 0, 'Razon': '', 'Total': 18},
    {'Empleado': 'Marcantonio Eder', 'Mes': 'Septiembre', 'Ausente': 0, 'Vacaciones': 21, 'ART': 0, 'Razon': '', 'Total': 21},
    
    {'Empleado': 'Pedernera Esteban', 'Mes': 'Febrero', 'Ausente': 0, 'Vacaciones': 1, 'ART': 1, 'Razon': '', 'Total': 2},
    {'Empleado': 'Pedernera Esteban', 'Mes': 'Marzo', 'Ausente': 0, 'Vacaciones': 7, 'ART': 0, 'Razon': '', 'Total': 7},
    {'Empleado': 'Pedernera Esteban', 'Mes': 'Abril', 'Ausente': 0, 'Vacaciones': 14, 'ART': 0, 'Razon': '', 'Total': 14},
    {'Empleado': 'Pedernera Esteban', 'Mes': 'Mayo', 'Ausente': 0, 'Vacaciones': 7, 'ART': 0, 'Razon': '', 'Total': 7},
    {'Empleado': 'Pedernera Esteban', 'Mes': 'Junio', 'Ausente': 0, 'Vacaciones': 7, 'ART': 0, 'Razon': '', 'Total': 7},
    {'Empleado': 'Pedernera Esteban', 'Mes': 'Julio', 'Ausente': 0, 'Vacaciones': 1, 'ART': 0, 'Razon': '', 'Total': 1},

    {'Empleado': 'Salas Mario', 'Mes': 'Junio', 'Ausente': 0, 'Vacaciones': 0, 'ART': 26, 'Razon': '', 'Total': 26},
    {'Empleado': 'Salas Mario', 'Mes': 'Julio', 'Ausente': 26, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Enfermo', 'Total': 26},
    {'Empleado': 'Salas Mario', 'Mes': 'Agosto', 'Ausente': 12, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Enfermo', 'Total': 12},
    {'Empleado': 'Salas Mario', 'Mes': 'Diciembre', 'Ausente': 0, 'Vacaciones': 26, 'ART': 0, 'Razon': '', 'Total': 26},
    
    {'Empleado': 'Vilches Jonatan', 'Mes': 'Mayo', 'Ausente': 0, 'Vacaciones': 21, 'ART': 0, 'Razon': '', 'Total': 21},
    {'Empleado': 'Vilches Jonatan', 'Mes': 'Junio', 'Ausente': 0, 'Vacaciones': 2, 'ART': 0, 'Razon': '', 'Total': 2},
    {'Empleado': 'Vilches Jonatan', 'Mes': 'Agosto', 'Ausente': 0, 'Vacaciones': 7, 'ART': 0, 'Razon': '', 'Total': 7},
    {'Empleado': 'Vilches Jonatan', 'Mes': 'Septiembre', 'Ausente': 0, 'Vacaciones': 14, 'ART': 0, 'Razon': '', 'Total': 14},
    
    {'Empleado': 'Diaz Raul', 'Mes': 'Junio', 'Ausente': 0, 'Vacaciones': 7, 'ART': 0, 'Razon': '', 'Total': 7},
    {'Empleado': 'Diaz Raul', 'Mes': 'Julio', 'Ausente': 0, 'Vacaciones': 17, 'ART': 0, 'Razon': '', 'Total': 17},
    
    {'Empleado': 'Cuadrado Denis', 'Mes': 'Enero', 'Ausente': 0, 'Vacaciones': 14, 'ART': 0, 'Razon': '', 'Total': 14},
    {'Empleado': 'Cuadrado Denis', 'Mes': 'Febrero', 'Ausente': 3, 'Vacaciones': 0, 'ART': 6, 'Razon': 'Permiso gremial', 'Total': 9},
    {'Empleado': 'Cuadrado Denis', 'Mes': 'Marzo', 'Ausente': 0, 'Vacaciones': 0, 'ART': 1, 'Razon': '', 'Total': 1},
    {'Empleado': 'Cuadrado Denis', 'Mes': 'Abril', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Permiso gremial', 'Total': 1},
    {'Empleado': 'Cuadrado Denis', 'Mes': 'Mayo', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Permiso gremial', 'Total': 1},
    {'Empleado': 'Cuadrado Denis', 'Mes': 'Junio', 'Ausente': 2, 'Vacaciones': 9, 'ART': 0, 'Razon': 'Permiso gremial', 'Total': 11},
    {'Empleado': 'Cuadrado Denis', 'Mes': 'Julio', 'Ausente': 2, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Enfermo/ Permiso gremial', 'Total': 2},
    {'Empleado': 'Cuadrado Denis', 'Mes': 'Agosto', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Permiso gremial', 'Total': 1},
    {'Empleado': 'Cuadrado Denis', 'Mes': 'Septiembre', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Permiso gremial', 'Total': 1},
    {'Empleado': 'Cuadrado Denis', 'Mes': 'Octubre', 'Ausente': 2, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Duelo', 'Total': 2},
    {'Empleado': 'Cuadrado Denis', 'Mes': 'Noviembre', 'Ausente': 2, 'Vacaciones': 12, 'ART': 0, 'Razon': 'Permiso gremial', 'Total': 14},
    {'Empleado': 'Cuadrado Denis', 'Mes': 'Diciembre', 'Ausente': 2, 'Vacaciones': 9, 'ART': 0, 'Razon': 'Permiso gremial', 'Total': 11},
    
    {'Empleado': 'Romero Alejandro', 'Mes': 'Enero', 'Ausente': 0, 'Vacaciones': 7, 'ART': 0, 'Razon': '', 'Total': 7},
    {'Empleado': 'Romero Alejandro', 'Mes': 'Agosto', 'Ausente': 0, 'Vacaciones': 3, 'ART': 0, 'Razon': '', 'Total': 3},
    
    {'Empleado': 'Allais Joaquin', 'Mes': 'Enero', 'Ausente': 0, 'Vacaciones': 1, 'ART': 0, 'Razon': '', 'Total': 1},
    {'Empleado': 'Allais Joaquin', 'Mes': 'Marzo', 'Ausente': 0, 'Vacaciones': 14, 'ART': 0, 'Razon': '', 'Total': 14},
    {'Empleado': 'Allais Joaquin', 'Mes': 'Abril', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Enfermo', 'Total': 1},
    {'Empleado': 'Allais Joaquin', 'Mes': 'Julio', 'Ausente': 0, 'Vacaciones': 0, 'ART': 23, 'Razon': '', 'Total': 23},
    {'Empleado': 'Allais Joaquin', 'Mes': 'Agosto', 'Ausente': 0, 'Vacaciones': 0, 'ART': 12, 'Razon': '', 'Total': 12},
    
    {'Empleado': 'Villafañe', 'Mes': 'Febrero', 'Ausente': 0, 'Vacaciones': 14, 'ART': 0, 'Razon': '', 'Total': 14},
    {'Empleado': 'Villafañe', 'Mes': 'Noviembre', 'Ausente': 0, 'Vacaciones': 12, 'ART': 0, 'Razon': '', 'Total': 12},
    {'Empleado': 'Villafañe', 'Mes': 'Diciembre', 'Ausente': 0, 'Vacaciones': 2, 'ART': 0, 'Razon': '', 'Total': 2},
    
    {'Empleado': 'Lescano', 'Mes': 'Enero', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Medico ART', 'Total': 1},
    {'Empleado': 'Lescano', 'Mes': 'Marzo', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Medico ART', 'Total': 1},
    {'Empleado': 'Lescano', 'Mes': 'Abril', 'Ausente': 3, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Enfermo', 'Total': 3},
    {'Empleado': 'Lescano', 'Mes': 'Noviembre', 'Ausente': 19, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Enfermo. Accidente', 'Total': 19},
    {'Empleado': 'Lescano', 'Mes': 'Diciembre', 'Ausente': 26, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Enfermo. Accidente', 'Total': 26},
    
    {'Empleado': 'Montiel Mayco', 'Mes': 'Enero', 'Ausente': 0, 'Vacaciones': 7, 'ART': 5, 'Razon': '', 'Total': 12},
    {'Empleado': 'Montiel Mayco', 'Mes': 'Abril', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Enfermo', 'Total': 1},
    {'Empleado': 'Montiel Mayco', 'Mes': 'Agosto', 'Ausente': 0, 'Vacaciones': 1, 'ART': 0, 'Razon': '', 'Total': 1},
    
    {'Empleado': 'Godoy Agustin', 'Mes': 'Abril', 'Ausente': 1, 'Vacaciones': 2, 'ART': 0, 'Razon': 'Enfermo', 'Total': 3},
    {'Empleado': 'Godoy Agustin', 'Mes': 'Junio', 'Ausente': 0, 'Vacaciones': 0, 'ART': 19, 'Razon': '', 'Total': 19},
    {'Empleado': 'Godoy Agustin', 'Mes': 'Julio', 'Ausente': 1, 'Vacaciones': 0, 'ART': 7, 'Razon': 'Enfermo', 'Total': 8},
    {'Empleado': 'Godoy Agustin', 'Mes': 'Diciembre', 'Ausente': 0, 'Vacaciones': 9, 'ART': 0, 'Razon': '', 'Total': 9},
    
    {'Empleado': 'Imberti Axel', 'Mes': 'Marzo', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Enfermo', 'Total': 1},
    {'Empleado': 'Imberti Axel', 'Mes': 'Junio', 'Ausente': 0, 'Vacaciones': 14, 'ART': 0, 'Razon': '', 'Total': 14},
    {'Empleado': 'Imberti Axel', 'Mes': 'Septiembre', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Cuidado hijo', 'Total': 1},
    
    {'Empleado': 'Biolatto', 'Mes': 'Febrero', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Enfermo', 'Total': 1},
    {'Empleado': 'Biolatto', 'Mes': 'Abril', 'Ausente': 0, 'Vacaciones': 14, 'ART': 0, 'Razon': '', 'Total': 14},
    {'Empleado': 'Biolatto', 'Mes': 'Junio', 'Ausente': 0, 'Vacaciones': 0, 'ART': 8, 'Razon': '', 'Total': 8},
    {'Empleado': 'Biolatto', 'Mes': 'Julio', 'Ausente': 0, 'Vacaciones': 0, 'ART': 26, 'Razon': '', 'Total': 26},
    {'Empleado': 'Biolatto', 'Mes': 'Agosto', 'Ausente': 0, 'Vacaciones': 0, 'ART': 2, 'Razon': '', 'Total': 2},
    {'Empleado': 'Biolatto', 'Mes': 'Septiembre', 'Ausente': 0, 'Vacaciones': 2, 'ART': 0, 'Razon': '', 'Total': 2},
    {'Empleado': 'Biolatto', 'Mes': 'Diciembre', 'Ausente': 0, 'Vacaciones': 14, 'ART': 0, 'Razon': '', 'Total': 14},
    
    {'Empleado': 'Aubert', 'Mes': 'Febrero', 'Ausente': 0, 'Vacaciones': 14, 'ART': 0, 'Razon': '', 'Total': 14},
    {'Empleado': 'Aubert', 'Mes': 'Mayo', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Permiso Universidad', 'Total': 1},
    
    {'Empleado': 'Montiel Jonas', 'Mes': 'Marzo', 'Ausente': 0, 'Vacaciones': 7, 'ART': 0, 'Razon': '', 'Total': 7},
    {'Empleado': 'Montiel Jonas', 'Mes': 'Abril', 'Ausente': 0, 'Vacaciones': 7, 'ART': 0, 'Razon': '', 'Total': 7},
    
    {'Empleado': 'Carrillo Tito', 'Mes': 'Enero', 'Ausente': 0, 'Vacaciones': 0, 'ART': 1, 'Razon': '', 'Total': 1},
    {'Empleado': 'Carrillo Tito', 'Mes': 'Marzo', 'Ausente': 0, 'Vacaciones': 7, 'ART': 0, 'Razon': '', 'Total': 7},
    {'Empleado': 'Carrillo Tito', 'Mes': 'Mayo', 'Ausente': 3, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Enfermo', 'Total': 3},
    
    {'Empleado': 'Aguilera Facundo', 'Mes': 'Enero', 'Ausente': 5, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Efermo. Covid +', 'Total': 5},
    {'Empleado': 'Aguilera Facundo', 'Mes': 'Marzo', 'Ausente': 0, 'Vacaciones': 21, 'ART': 0, 'Razon': '', 'Total': 21},
    {'Empleado': 'Aguilera Facundo', 'Mes': 'Agosto', 'Ausente': 2, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Enfermo', 'Total': 2},
    
    {'Empleado': 'Elizagaray Santi', 'Mes': 'Febrero', 'Ausente': 0, 'Vacaciones': 14, 'ART': 0, 'Razon': '', 'Total': 14},
    
    {'Empleado': 'Ron Octavio', 'Mes': 'Mayo', 'Ausente': 0, 'Vacaciones': 6, 'ART': 0, 'Razon': '', 'Total': 6},
    
    {'Empleado': 'Crespin Sebastian', 'Mes': 'Abril', 'Ausente': 2, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Enfermo', 'Total': 2},
    {'Empleado': 'Crespin Sebastian', 'Mes': 'Junio', 'Ausente': 0, 'Vacaciones': 3, 'ART': 0, 'Razon': '', 'Total': 3},
    {'Empleado': 'Crespin Sebastian', 'Mes': 'Julio', 'Ausente': 1, 'Vacaciones': 0, 'ART': 0, 'Razon': 'Enfermo', 'Total': 1},
    ]
    
    # Datos de 2025 (solo algunos para probar)
    data_2025 = [
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
    
    # Crear DataFrames con columna Año
    df_2024 = pd.DataFrame(data_2024)
    df_2024['Año'] = 2024
    
    df_2025 = pd.DataFrame(data_2025)
    df_2025['Año'] = 2025
    
    # Combinar ambos años
    df = pd.concat([df_2024, df_2025], ignore_index=True)
    
    # Asegurar que las columnas numéricas sean del tipo correcto
    numeric_cols = ['Ausente', 'Vacaciones', 'ART', 'Total']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Calcular totales por empleado y año
    totals = df.groupby(['Empleado', 'Año']).agg({
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
    if not razon or pd.isna(razon):
        return 'Sin motivo específico'
    razon_lower = str(razon).lower()
    
    if 'gremial' in razon_lower:
        return 'Permiso gremial'
    elif 'cuidado' in razon_lower:
        return 'Cuidado familiar'
    elif 'enfermo' in razon_lower or 'enfermedad' in razon_lower or 'covid' in razon_lower:
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
    elif 'medico' in razon_lower or 'art' in razon_lower:
        return 'Médico/ART'
    elif 'universidad' in razon_lower:
        return 'Permiso estudio'
    elif 'mudanza' in razon_lower:
        return 'Permiso personal'
    elif 'donacion' in razon_lower:
        return 'Permiso especial'
    else:
        return 'Otros'

# Cargar datos
try:
    df, totals = load_data()
    
    # Título principal
    st.markdown('<h1 class="main-header">📊 Panel de control de Ausentismo 2024-2025</h1>', unsafe_allow_html=True)
    
    # Sidebar con filtros
    st.sidebar.header("🔍 Filtros Básicos")
    
    # Filtro de año
    years = ["Todos"] + sorted(df['Año'].unique().tolist())
    selected_year = st.sidebar.selectbox("📅 Año", years)
    
    # Filtro de empleado
    if selected_year != "Todos":
        employees = ["Todos"] + sorted(df[df['Año'] == selected_year]['Empleado'].unique().tolist())
    else:
        employees = ["Todos"] + sorted(df['Empleado'].unique().tolist())
    
    selected_employee = st.sidebar.selectbox("👤 Empleado", employees)
    
    # Filtro de mes
    months_order = ['Todos', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    selected_month = st.sidebar.selectbox("📆 Mes", months_order)
    
    # Filtros avanzados
    st.sidebar.header("🎯 Filtros Avanzados")
    
    # Filtro por tipo de ausencia
    absence_types = st.sidebar.multiselect(
        "Tipo de Ausencia",
        options=['Todos', 'Ausente', 'Vacaciones', 'ART'],
        default=['Todos']
    )
    
    # Filtro por categoría de razón
    razones_categorias = ['Todos'] + sorted(df[df['Razon'] != '']['Razon_Categoria'].unique().tolist())
    selected_categoria = st.sidebar.selectbox("Categoría de Razón", razones_categorias)
    
    # Aplicar filtros
    filtered_df = df.copy()
    filtered_totals = totals.copy()
    
    if selected_year != "Todos":
        filtered_df = filtered_df[filtered_df['Año'] == selected_year]
        filtered_totals = filtered_totals[filtered_totals['Año'] == selected_year]
    
    if selected_employee != "Todos":
        filtered_df = filtered_df[filtered_df['Empleado'] == selected_employee]
        filtered_totals = filtered_totals[filtered_totals['Empleado'] == selected_employee]
    
    if selected_month != "Todos":
        filtered_df = filtered_df[filtered_df['Mes'] == selected_month]
    
    if selected_categoria != "Todos":
        razones_filtradas = df[df['Razon_Categoria'] == selected_categoria]['Razon'].unique()
        filtered_df = filtered_df[filtered_df['Razon'].isin(razones_filtradas) | (filtered_df['Razon'] == '')]
    
    # Métricas principales - CORREGIDO
    st.markdown("### 📈 Métricas Generales")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_employees = len(filtered_totals['Empleado'].unique()) if not filtered_totals.empty else 0
        employees_with_absences = len(filtered_totals[filtered_totals['Total'] > 0]) if not filtered_totals.empty else 0
        st.metric(
            label="👥 Total Empleados",
            value=total_employees,
            delta=f"{employees_with_absences} con faltas"
        )
    
    with col2:
        total_days = filtered_totals['Total'].sum() if not filtered_totals.empty else 0
        avg_days = total_days/len(filtered_totals['Empleado'].unique()) if len(filtered_totals['Empleado'].unique()) > 0 else 0
        st.metric(
            label="📅 Días Totales",
            value=f"{int(total_days):,}",
            delta=f"Promedio: {avg_days:.1f}"
        )
    
    with col3:
        vac_days = filtered_totals['Vacaciones'].sum() if not filtered_totals.empty else 0
        vac_percent = vac_days/total_days*100 if total_days > 0 else 0
        st.metric(
            label="🏖️ Vacaciones",
            value=f"{int(vac_days):,}",
            delta=f"{vac_percent:.1f}%"
        )
    
    with col4:
        art_days = filtered_totals['ART'].sum() if not filtered_totals.empty else 0
        art_percent = art_days/total_days*100 if total_days > 0 else 0
        st.metric(
            label="⚠️ ART",
            value=f"{int(art_days):,}",
            delta=f"{art_percent:.1f}%"
        )
    
    with col5:
        # Calcular porcentaje de ausentismo CORREGIDO
        if not filtered_totals.empty and len(filtered_totals['Empleado'].unique()) > 0:
            num_empleados = len(filtered_totals['Empleado'].unique())
            dias_trabajables = 260 * num_empleados  # 260 días por empleado por año
            dias_ausentismo = filtered_totals['Ausente'].sum() + filtered_totals['ART'].sum()
            porcentaje_ausentismo = (dias_ausentismo / dias_trabajables * 100) if dias_trabajables > 0 else 0
        else:
            dias_ausentismo = 0
            porcentaje_ausentismo = 0
        
        st.metric(
            label="📊 % Ausentismo",
            value=f"{porcentaje_ausentismo:.2f}%",
            delta=f"{int(dias_ausentismo)} días"
        )
    
    # Tabs principales
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Panel de control", "👤 Análisis Individual", "📅 Comparación Anual", "🔍 Análisis Detallado", "💾 Exportar"])
    
    with tab1:
        # Gráficos principales
        col1, col2 = st.columns(2)
        
        with col1:
            # Top empleados
            st.subheader("🏆 Top 10 Empleados con más ausencias")
            if not filtered_totals.empty:
                top_employees = filtered_totals.nlargest(10, 'Total')
                
                if not top_employees.empty:
                    fig_top = px.bar(
                        top_employees, x='Total', y='Empleado', orientation='h',
                        color='Total', color_continuous_scale='Reds',
                        text='Total', height=400
                    )
                    fig_top.update_layout(showlegend=False)
                    fig_top.update_traces(textposition='outside')
                    st.plotly_chart(fig_top, use_container_width=True)
                else:
                    st.info("No hay datos para mostrar")
            else:
                st.info("No hay datos para mostrar")
        
        with col2:
            # Distribución por tipo
            st.subheader("📊 Distribución por tipo")
            if not filtered_totals.empty:
                if 'Todos' in absence_types or not absence_types:
                    total_types = filtered_totals[['Ausente', 'Vacaciones', 'ART']].sum()
                    tipos_a_mostrar = ['Ausente', 'Vacaciones', 'ART']
                else:
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
            else:
                st.info("No hay datos para mostrar")
        
        # Evolución mensual - SIMPLIFICADO
        st.subheader("📅 Evolución mensual")
        
        if not filtered_df.empty:
            tipos_evolucion = st.multiselect(
                "Selecciona tipos para la evolución mensual",
                options=['Ausente', 'Vacaciones', 'ART'],
                default=['Ausente', 'Vacaciones', 'ART'],
                key="evolucion_tipos"
            )
            
            if tipos_evolucion:
                # Ordenar meses correctamente
                meses_orden = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                             'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
                
                # Agrupar por mes y calcular sumas
                monthly_data = filtered_df.groupby('Mes')[tipos_evolucion].sum().reset_index()
                
                # Asegurar que todos los meses estén en el orden correcto
                monthly_data['Mes'] = pd.Categorical(monthly_data['Mes'], categories=meses_orden, ordered=True)
                monthly_data = monthly_data.sort_values('Mes')
                
                if not monthly_data.empty:
                    # Crear gráfico
                    fig_monthly = px.bar(
                        monthly_data,
                        x='Mes',
                        y=tipos_evolucion,
                        barmode='group',
                        color_discrete_sequence=px.colors.qualitative.Set3,
                        height=400
                    )
                    fig_monthly.update_layout(
                        xaxis_title="Mes",
                        yaxis_title="Días",
                        xaxis={'categoryorder': 'array', 'categoryarray': meses_orden}
                    )
                    st.plotly_chart(fig_monthly, use_container_width=True)
                else:
                    st.info("No hay datos mensuales para mostrar")
        else:
            st.info("No hay datos para mostrar la evolución mensual")
    
    with tab2:
        if selected_employee != "Todos":
            st.header(f"👤 Análisis detallado - {selected_employee}")
            
            emp_data = filtered_df[filtered_df['Empleado'] == selected_employee]
            emp_total = filtered_totals[filtered_totals['Empleado'] == selected_employee]
            
            if not emp_total.empty:
                for year in sorted(emp_total['Año'].unique()):
                    emp_total_year = emp_total[emp_total['Año'] == year].iloc[0]
                    emp_data_year = emp_data[emp_data['Año'] == year]
                    
                    st.markdown(f"### Año {year}")
                    col1, col2, col3, col4, col5 = st.columns(5)
                    
                    with col1:
                        st.metric("Total de días", int(emp_total_year['Total']))
                    with col2:
                        st.metric("Días ausente", int(emp_total_year['Ausente']))
                    with col3:
                        st.metric("Días de vacaciones", int(emp_total_year['Vacaciones']))
                    with col4:
                        st.metric("Días ART", int(emp_total_year['ART']))
                    with col5:
                        dias_trabajables_emp = 260
                        dias_ausentismo_emp = emp_total_year['Ausente'] + emp_total_year['ART']
                        porcentaje_ausentismo_emp = (dias_ausentismo_emp / dias_trabajables_emp * 100) if dias_trabajables_emp > 0 else 0
                        st.metric("% Ausentismo", f"{porcentaje_ausentismo_emp:.2f}%")
                    
                    # Gráficos del empleado
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Distribución
                        fig_emp_pie = px.pie(
                            values=[emp_total_year['Ausente'], emp_total_year['Vacaciones'], emp_total_year['ART']],
                            names=['Ausente', 'Vacaciones', 'ART'],
                            color_discrete_sequence=px.colors.qualitative.Set3,
                            title=f"Distribución {year}"
                        )
                        st.plotly_chart(fig_emp_pie, use_container_width=True)
                    
                    with col2:
                        # Evolución mensual
                        if not emp_data_year.empty:
                            meses_orden = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                                         'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
                            
                            monthly_emp = emp_data_year.groupby('Mes')[['Ausente', 'Vacaciones', 'ART']].sum().reset_index()
                            monthly_emp['Mes'] = pd.Categorical(monthly_emp['Mes'], categories=meses_orden, ordered=True)
                            monthly_emp = monthly_emp.sort_values('Mes')
                            
                            if not monthly_emp.empty:
                                fig_emp_monthly = px.bar(
                                    monthly_emp,
                                    x='Mes',
                                    y=['Ausente', 'Vacaciones', 'ART'],
                                    barmode='group',
                                    color_discrete_sequence=px.colors.qualitative.Set3,
                                    title=f"Evolución mensual {year}"
                                )
                                fig_emp_monthly.update_layout(
                                    xaxis_title="Mes",
                                    yaxis_title="Días",
                                    xaxis={'categoryorder': 'array', 'categoryarray': meses_orden}
                                )
                                st.plotly_chart(fig_emp_monthly, use_container_width=True)
                            else:
                                st.info("No hay datos mensuales para este año")
                        else:
                            st.info("No hay datos mensuales para este año")
                    
                    # Razones de ausencia
                    razones = emp_data_year[emp_data_year['Razon'] != ''][['Mes', 'Ausente', 'Razon', 'Razon_Categoria']]
                    if not razones.empty:
                        st.subheader(f"📝 Razones de ausencia {year}")
                        
                        # Resumen por categoría
                        st.write("**Resumen por categoría:**")
                        categoria_resumen = razones.groupby('Razon_Categoria')['Ausente'].sum().reset_index()
                        st.dataframe(categoria_resumen)
                        
                        st.write("**Detalle por mes:**")
                        for _, row in razones.iterrows():
                            st.write(f"**{row['Mes']}**: {int(row['Ausente'])} días - {row['Razon']} (*{row['Razon_Categoria']}*)")
                    
                    st.markdown("---")
        else:
            st.info("👆 Selecciona un empleado en el sidebar para ver su análisis detallado")
    
    with tab3:
        st.header("📅 Comparación Anual 2024 vs 2025")
        
        if len(df['Año'].unique()) > 1:
            # Métricas comparativas
            comparison_data = totals.groupby('Año').agg({
                'Empleado': 'nunique',
                'Ausente': 'sum',
                'Vacaciones': 'sum',
                'ART': 'sum',
                'Total': 'sum'
            }).reset_index()
            
            st.write("### 📊 Comparativa General")
            col1, col2, col3, col4, col5 = st.columns(5)
            
            for idx, year in enumerate(sorted(comparison_data['Año'])):
                year_data = comparison_data[comparison_data['Año'] == year].iloc[0]
                
                if idx == 0:
                    with col1:
                        st.metric(f"👥 Empleados {year}", int(year_data['Empleado']))
                    with col2:
                        st.metric(f"📅 Días Totales {year}", f"{int(year_data['Total']):,}")
                    with col3:
                        st.metric(f"🏖️ Vacaciones {year}", f"{int(year_data['Vacaciones']):,}")
                    with col4:
                        st.metric(f"⚠️ ART {year}", f"{int(year_data['ART']):,}")
                    with col5:
                        dias_trabajables = 260 * year_data['Empleado']
                        dias_ausentismo = year_data['Ausente'] + year_data['ART']
                        porcentaje = (dias_ausentismo / dias_trabajables * 100) if dias_trabajables > 0 else 0
                        st.metric(f"📊 % Ausentismo {year}", f"{porcentaje:.2f}%")
            
            # Gráficos comparativos
            st.write("### 📈 Gráficos Comparativos")
            col1, col2 = st.columns(2)
            
            with col1:
                # Preparar datos para gráfico de barras agrupadas
                comparison_melted = pd.melt(
                    comparison_data,
                    id_vars=['Año'],
                    value_vars=['Ausente', 'Vacaciones', 'ART'],
                    var_name='Tipo',
                    value_name='Días'
                )
                
                fig_comparison = px.bar(
                    comparison_melted,
                    x='Año',
                    y='Días',
                    color='Tipo',
                    barmode='group',
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    title="Comparativa de días por tipo"
                )
                st.plotly_chart(fig_comparison, use_container_width=True)
            
            with col2:
                # Calcular porcentaje de ausentismo por año
                comparison_data['% Ausentismo'] = ((comparison_data['Ausente'] + comparison_data['ART']) / 
                                                  (260 * comparison_data['Empleado']) * 100)
                
                fig_trend = px.line(
                    comparison_data,
                    x='Año',
                    y='% Ausentismo',
                    markers=True,
                    title="Tendencia del % de Ausentismo"
                )
                fig_trend.update_traces(line=dict(width=4))
                st.plotly_chart(fig_trend, use_container_width=True)
            
        else:
            st.info("Selecciona 'Todos' en el filtro de año para ver la comparativa anual")
    
    with tab4:
        st.header("🔍 Análisis Detallado")
        
        if not filtered_df.empty:
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
                
                comparacion_metric = st.selectbox(
                    "Métrica para comparación mensual",
                    ['Total', 'Ausente', 'Vacaciones', 'ART'],
                    key='comparacion_metric'
                )
                
                meses_orden = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                             'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
                
                monthly_comparison = filtered_df.groupby('Mes')[comparacion_metric].sum().reset_index()
                monthly_comparison['Mes'] = pd.Categorical(monthly_comparison['Mes'], categories=meses_orden, ordered=True)
                monthly_comparison = monthly_comparison.sort_values('Mes')
                
                if not monthly_comparison.empty:
                    fig_comparison = px.line(
                        monthly_comparison,
                        x='Mes',
                        y=comparacion_metric,
                        markers=True,
                        title=f"Evolución de {comparacion_metric} por mes"
                    )
                    fig_comparison.update_layout(
                        xaxis_title="Mes",
                        yaxis_title="Días",
                        xaxis={'categoryorder': 'array', 'categoryarray': meses_orden}
                    )
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
        else:
            st.info("No hay datos para mostrar en el análisis detallado")
    
    with tab5:
        st.header("💾 Exportar datos")
        
        if not filtered_df.empty:
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
                
                # Datos completos si hay ambos años
                if len(df['Año'].unique()) > 1:
                    df.to_excel(writer, sheet_name='Datos_Completos', index=False)
                    totals.to_excel(writer, sheet_name='Totales_Completos', index=False)
            
            excel_buffer.seek(0)
            
            st.download_button(
                label="📥 Descargar Excel con todos los datos",
                data=excel_buffer,
                file_name=f"analisis_ausentismo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            # Vista previa de datos
            if st.checkbox("👁️ Ver vista previa de datos"):
                st.subheader("Resumen por empleado")
                st.dataframe(filtered_totals)
                
                st.subheader("Detalle mensual")
                st.dataframe(filtered_df)
        else:
            st.info("No hay datos para exportar")

except Exception as e:
    st.error(f"Error al cargar los datos: {str(e)}")
    import traceback
    st.code(traceback.format_exc())
    st.info("Por favor, verifica que todos los datos estén correctamente procesados.")

# Footer
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center'>
        <p>Dashboard creado con Streamlit • 📊 Datos actualizados a {datetime.now().strftime("%d/%m/%Y %H:%M")}</p>
        <p>© 2024-2025 - Sistema de Gestión de Ausentismo</p>
    </div>
    """,
    unsafe_allow_html=True
)