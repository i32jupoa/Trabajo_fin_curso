# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QGroupBox, QCheckBox, QDoubleSpinBox, QSpinBox, 
                             QRadioButton, QPushButton, QFormLayout, QGridLayout, QComboBox)

class VistaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Diagnóstico Nutricional - ISSBC")
        self.setMinimumSize(650, 600)
        self.inicializarUI()

    def inicializarUI(self):
        widget_central = QWidget()
        layout_principal = QVBoxLayout()

        # --- GRUPO 1: SÍNTOMAS ---
        grupo_sintomas = QGroupBox("Síntomas y Signos Físicos")
        layout_sintomas = QGridLayout()
        self.chk_fatiga = QCheckBox("Fatiga extrema o debilidad")
        self.chk_cabello = QCheckBox("Caída de cabello severa")
        self.chk_palidez = QCheckBox("Palidez en piel o mucosas")
        self.chk_unas = QCheckBox("Uñas frágiles con manchas")
        self.chk_encias = QCheckBox("Sangrado frecuente de encías")
        self.chk_calambres = QCheckBox("Calambres musculares / Espasmos")
        self.chk_hormigueo = QCheckBox("Hormigueo en manos y pies")
        self.chk_cicatrizacion = QCheckBox("Retraso en cicatrización")
        self.chk_concentracion = QCheckBox("Niebla mental (Falta concentración)")
        self.chk_estrenimiento = QCheckBox("Estreñimiento crónico")

        layout_sintomas.addWidget(self.chk_fatiga, 0, 0)
        layout_sintomas.addWidget(self.chk_cabello, 0, 1)
        layout_sintomas.addWidget(self.chk_palidez, 1, 0)
        layout_sintomas.addWidget(self.chk_unas, 1, 1)
        layout_sintomas.addWidget(self.chk_encias, 2, 0)
        layout_sintomas.addWidget(self.chk_calambres, 2, 1)
        layout_sintomas.addWidget(self.chk_hormigueo, 3, 0)
        layout_sintomas.addWidget(self.chk_cicatrizacion, 3, 1)
        layout_sintomas.addWidget(self.chk_concentracion, 4, 0)
        layout_sintomas.addWidget(self.chk_estrenimiento, 4, 1)
        grupo_sintomas.setLayout(layout_sintomas)

        # --- CONTENEDOR MEDIO (Observables + Dieta) ---
        layout_medio = QHBoxLayout()

        # Observables biométricos
        grupo_observables = QGroupBox("Biometría")
        layout_observables = QFormLayout()
        self.spin_imc = QDoubleSpinBox()
        self.spin_imc.setRange(10.0, 50.0)
        self.spin_imc.setValue(22.0)
        self.spin_sueno = QSpinBox()
        self.spin_sueno.setRange(0, 24)
        self.spin_sueno.setValue(7)
        layout_observables.addRow("IMC:", self.spin_imc)
        layout_observables.addRow("Horas sueño:", self.spin_sueno)
        grupo_observables.setLayout(layout_observables)

        # Hábitos Alimenticios (Nuevo)
        grupo_dieta = QGroupBox("Frecuencia de Consumo")
        layout_dieta = QFormLayout()
        opciones_frecuencia = ["Diario", "3-4 veces/semana", "1-2 veces/semana", "Raramente / Nunca"]
        
        self.combo_carne = QComboBox(); self.combo_carne.addItems(opciones_frecuencia)
        self.combo_pescado = QComboBox(); self.combo_pescado.addItems(opciones_frecuencia)
        self.combo_frutas = QComboBox(); self.combo_frutas.addItems(opciones_frecuencia)
        self.combo_lacteos = QComboBox(); self.combo_lacteos.addItems(opciones_frecuencia)

        layout_dieta.addRow("Carne roja / Aves:", self.combo_carne)
        layout_dieta.addRow("Pescado / Azul:", self.combo_pescado)
        layout_dieta.addRow("Frutas / Verduras:", self.combo_frutas)
        layout_dieta.addRow("Lácteos:", self.combo_lacteos)
        grupo_dieta.setLayout(layout_dieta)

        layout_medio.addWidget(grupo_observables)
        layout_medio.addWidget(grupo_dieta)

        # --- GRUPO 3: MODO CONOCIMIENTO ---
        grupo_modo = QGroupBox("Modo de Conocimiento")
        layout_modo = QHBoxLayout()
        self.radio_local = QRadioButton("Modo Local (Solo PDFs)")
        self.radio_web = QRadioButton("Modo Web (PDFs + Internet)")
        self.radio_local.setChecked(True)
        layout_modo.addWidget(self.radio_local)
        layout_modo.addWidget(self.radio_web)
        grupo_modo.setLayout(layout_modo)

        # --- BOTONES DE ACCIÓN ---
        layout_botones = QHBoxLayout()
        self.btn_evaluar = QPushButton("1. Evaluar Hipótesis")
        self.btn_diagnosticar = QPushButton("2. Diagnosticar")
        self.btn_justificacion = QPushButton("3. Ver Justificación")
        layout_botones.addWidget(self.btn_evaluar)
        layout_botones.addWidget(self.btn_diagnosticar)
        layout_botones.addWidget(self.btn_justificacion)

        layout_gestion = QHBoxLayout()
        self.btn_pdfs = QPushButton("Gestión de PDFs")
        self.btn_web = QPushButton("Fuentes Web")
        layout_gestion.addWidget(self.btn_pdfs)
        layout_gestion.addWidget(self.btn_web)

        # Ensamblaje Final
        layout_principal.addWidget(grupo_sintomas)
        layout_principal.addLayout(layout_medio)
        layout_principal.addWidget(grupo_modo)
        layout_principal.addLayout(layout_botones)
        layout_principal.addLayout(layout_gestion)

        widget_central.setLayout(layout_principal)
        self.setCentralWidget(widget_central)

    def obtener_sintomas_marcados(self):
        sintomas = []
        if self.chk_fatiga.isChecked(): sintomas.append("Fatiga extrema")
        if self.chk_cabello.isChecked(): sintomas.append("Caída de cabello severa")
        if self.chk_palidez.isChecked(): sintomas.append("Palidez")
        if self.chk_unas.isChecked(): sintomas.append("Uñas frágiles")
        if self.chk_encias.isChecked(): sintomas.append("Sangrado frecuente de encías")
        if self.chk_calambres.isChecked(): sintomas.append("Calambres musculares")
        if self.chk_hormigueo.isChecked(): sintomas.append("Hormigueo en manos y pies")
        if self.chk_cicatrizacion.isChecked(): sintomas.append("Retraso en cicatrización")
        if self.chk_concentracion.isChecked(): sintomas.append("Niebla mental")
        if self.chk_estrenimiento.isChecked(): sintomas.append("Estreñimiento crónico")
        return sintomas