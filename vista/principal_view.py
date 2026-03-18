# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QGroupBox, QCheckBox, QDoubleSpinBox, QSpinBox, 
                             QRadioButton, QPushButton, QFormLayout, QGridLayout, 
                             QComboBox, QLabel, QAbstractSpinBox)
from PyQt6.QtCore import Qt

class VistaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Experto de Diagnóstico Nutricional - ISSBC")
        self.setMinimumSize(800, 650)
        self.aplicar_estilos()
        self.inicializarUI()

    def aplicar_estilos(self):
        # Tema "Noche Profunda": Mucho más oscuro y sin absolutamente nada de blanco puro.
        self.setStyleSheet("""
            QWidget { 
                background-color: #121212; /* Fondo casi negro */
                color: #cccccc; /* Textos en gris claro, nada de blanco */
                font-family: Arial;
                font-size: 13px;
            }
            QGroupBox { 
                background-color: #1e1e1e; /* Tarjetas un pelín más claras para separar */
                border: 1px solid #333333; /* Borde muy oscuro */
                margin-top: 15px; 
                font-weight: bold;
                border-radius: 6px;
            }
            QGroupBox::title { 
                subcontrol-origin: margin; 
                left: 10px; 
                color: #5c9dd6; /* Azul apagado para los títulos */
            }
            QPushButton { 
                background-color: #155bb5; /* Azul oscuro para botones */
                color: #e0e0e0; /* Texto de botones gris muy claro */
                padding: 10px; 
                font-weight: bold; 
                border-radius: 4px; 
                border: 1px solid #0f3d7a;
            }
            QPushButton:hover { background-color: #1a6dcc; }
            
            QComboBox, QSpinBox, QDoubleSpinBox { 
                background-color: #252526; /* Fondo de las cajas de texto muy oscuro */
                border: 1px solid #444444; 
                padding: 5px; 
                color: #cccccc;
                border-radius: 3px;
            }
            
            /* --- LOS CUADRITOS Y CÍRCULOS (Adaptados al Modo Noche) --- */
            QCheckBox, QRadioButton { 
                background-color: transparent; 
                color: #cccccc;
                spacing: 8px;
            }
            
            /* Cuadrado del CheckBox (Síntomas) */
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                background-color: #252526; 
                border: 2px solid #555555; 
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                background-color: #155bb5; 
                border: 2px solid #155bb5;
                /* Tick dibujado en gris claro (%23e0e0e0), 0% blanco */
                image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='14' height='14' fill='%23e0e0e0' viewBox='0 0 24 24'><path d='M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z'/></svg>");
            }

            /* Círculo del RadioButton (Motor de Inferencia) */
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
                background-color: #252526;
                border: 2px solid #555555;
                border-radius: 10px; 
            }
            QRadioButton::indicator:checked {
                background-color: #155bb5;
                border: 2px solid #155bb5;
                /* Círculo interior dibujado en gris claro (%23e0e0e0) */
                image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10'><circle cx='5' cy='5' r='4' fill='%23e0e0e0'/></svg>");
            }
        """)

    def inicializarUI(self):
        widget_central = QWidget()
        layout_principal = QVBoxLayout()
        layout_principal.setSpacing(15)
        layout_principal.setContentsMargins(20, 20, 20, 20)

        # --- SÍNTOMAS (Con sus cuadrados nativos visibles) ---
        grupo_sintomas = QGroupBox("1. Síntomas y Signos Físicos Detectados")
        layout_sintomas = QGridLayout()
        layout_sintomas.setSpacing(10)
        
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

        layout_sintomas.addWidget(self.chk_fatiga, 0, 0); layout_sintomas.addWidget(self.chk_cabello, 0, 1)
        layout_sintomas.addWidget(self.chk_palidez, 1, 0); layout_sintomas.addWidget(self.chk_unas, 1, 1)
        layout_sintomas.addWidget(self.chk_encias, 2, 0); layout_sintomas.addWidget(self.chk_calambres, 2, 1)
        layout_sintomas.addWidget(self.chk_hormigueo, 3, 0); layout_sintomas.addWidget(self.chk_cicatrizacion, 3, 1)
        layout_sintomas.addWidget(self.chk_concentracion, 4, 0); layout_sintomas.addWidget(self.chk_estrenimiento, 4, 1)
        grupo_sintomas.setLayout(layout_sintomas)

        # --- BIOMETRÍA Y DIETA ---
        layout_medio = QHBoxLayout()
        layout_medio.setSpacing(20)

        grupo_observables = QGroupBox("2. Biometría y Descanso")
        layout_observables = QFormLayout()
        layout_observables.setSpacing(15)
        self.spin_imc = QDoubleSpinBox()
        self.spin_imc.setRange(10.0, 50.0); self.spin_imc.setValue(22.0)
        
        self.spin_sueno = QSpinBox()
        self.spin_sueno.setRange(0, 24); self.spin_sueno.setValue(7)
        
        # AQUÍ ESTÁ LA MAGIA: Obligamos a que salgan los símbolos + y - explícitamente
        self.spin_imc.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.spin_sueno.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)

        layout_observables.addRow("Índice Masa Corporal (IMC):", self.spin_imc)
        layout_observables.addRow("Horas de sueño diarias:", self.spin_sueno)
        grupo_observables.setLayout(layout_observables)

        grupo_dieta = QGroupBox("3. Frecuencia Semanal de Consumo")
        layout_dieta = QGridLayout()
        layout_dieta.setSpacing(10)
        
        opciones_dias = ["0 días (Nunca)", "1-2 días", "3-4 días", "5-6 días", "7 días (Diario)"]
        
        self.combo_verduras = QComboBox(); self.combo_verduras.addItems(opciones_dias); self.combo_verduras.setCurrentText("3-4 días")
        self.combo_frutas = QComboBox(); self.combo_frutas.addItems(opciones_dias); self.combo_frutas.setCurrentText("3-4 días")
        self.combo_cereales = QComboBox(); self.combo_cereales.addItems(opciones_dias); self.combo_cereales.setCurrentText("3-4 días")
        self.combo_pescado = QComboBox(); self.combo_pescado.addItems(opciones_dias); self.combo_pescado.setCurrentText("1-2 días")
        self.combo_carne = QComboBox(); self.combo_carne.addItems(opciones_dias); self.combo_carne.setCurrentText("3-4 días")
        self.combo_frutos_secos = QComboBox(); self.combo_frutos_secos.addItems(opciones_dias); self.combo_frutos_secos.setCurrentText("1-2 días")
        self.combo_bolleria = QComboBox(); self.combo_bolleria.addItems(opciones_dias); self.combo_bolleria.setCurrentText("1-2 días")
        self.combo_basura = QComboBox(); self.combo_basura.addItems(opciones_dias); self.combo_basura.setCurrentText("1-2 días")

        layout_dieta.addWidget(QLabel("Verduras:"), 0, 0); layout_dieta.addWidget(self.combo_verduras, 0, 1)
        layout_dieta.addWidget(QLabel("Frutas:"), 1, 0); layout_dieta.addWidget(self.combo_frutas, 1, 1)
        layout_dieta.addWidget(QLabel("Cereales:"), 2, 0); layout_dieta.addWidget(self.combo_cereales, 2, 1)
        layout_dieta.addWidget(QLabel("Frutos secos:"), 3, 0); layout_dieta.addWidget(self.combo_frutos_secos, 3, 1)
        
        layout_dieta.addWidget(QLabel("Pescado:"), 0, 2); layout_dieta.addWidget(self.combo_pescado, 0, 3)
        layout_dieta.addWidget(QLabel("Carne/Aves:"), 1, 2); layout_dieta.addWidget(self.combo_carne, 1, 3)
        layout_dieta.addWidget(QLabel("Bollería:"), 2, 2); layout_dieta.addWidget(self.combo_bolleria, 2, 3)
        layout_dieta.addWidget(QLabel("Comida basura:"), 3, 2); layout_dieta.addWidget(self.combo_basura, 3, 3)
        grupo_dieta.setLayout(layout_dieta)

        layout_medio.addWidget(grupo_observables, 1)
        layout_medio.addWidget(grupo_dieta, 2)

        # --- MODO Y ACCIONES ---
        grupo_modo = QGroupBox("4. Motor de Inferencia")
        layout_modo = QHBoxLayout()
        self.radio_local = QRadioButton("Modo Respaldo (Reglas Estrictas)")
        self.radio_web = QRadioButton("Modo Inteligencia Artificial (TinyLlama)")
        self.radio_web.setChecked(True)
        layout_modo.addWidget(self.radio_local)
        layout_modo.addWidget(self.radio_web)
        grupo_modo.setLayout(layout_modo)

        layout_botones = QHBoxLayout()
        self.btn_evaluar = QPushButton("Evaluar Hipótesis Rápidas")
        self.btn_diagnosticar = QPushButton("Generar Diagnóstico IA")
        self.btn_justificacion = QPushButton("Ver Justificación Médica")
        
        layout_botones.addWidget(self.btn_evaluar)
        layout_botones.addWidget(self.btn_diagnosticar)
        layout_botones.addWidget(self.btn_justificacion)

        layout_gestion = QHBoxLayout()
        self.btn_pdfs = QPushButton("Cargar Analíticas / PDFs")
        self.btn_web = QPushButton("Auditar Fuentes")
        
        layout_gestion.addWidget(self.btn_pdfs)
        layout_gestion.addWidget(self.btn_web)

        # Ensamblaje
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
        if self.chk_palidez.isChecked(): sintomas.append("Palidez en piel/mucosas")
        if self.chk_unas.isChecked(): sintomas.append("Uñas frágiles")
        if self.chk_encias.isChecked(): sintomas.append("Sangrado de encías")
        if self.chk_calambres.isChecked(): sintomas.append("Calambres musculares")
        if self.chk_hormigueo.isChecked(): sintomas.append("Hormigueo extremidades")
        if self.chk_cicatrizacion.isChecked(): sintomas.append("Retraso cicatrización")
        if self.chk_concentracion.isChecked(): sintomas.append("Niebla mental")
        if self.chk_estrenimiento.isChecked(): sintomas.append("Estreñimiento crónico")
        return sintomas