# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QTextEdit, 
                             QListWidget, QLabel, QHeaderView)

class DialogoHipotesis(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Hipótesis Posibles")
        self.resize(500, 300)
        layout = QVBoxLayout(self)
        self.tabla = QTableWidget(0, 3)
        self.tabla.setHorizontalHeaderLabels(["Hipótesis", "Probabilidad", "Estado"])
        self.tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla)
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.accept)
        layout.addWidget(btn_cerrar)

class DialogoTexto(QDialog):
    # Reutilizable para Diagnóstico y Justificación
    def __init__(self, titulo, parent=None):
        super().__init__(parent)
        self.setWindowTitle(titulo)
        self.resize(400, 300)
        layout = QVBoxLayout(self)
        self.texto = QTextEdit()
        self.texto.setReadOnly(True)
        layout.addWidget(self.texto)
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.accept)
        layout.addWidget(btn_cerrar)

class DialogoPDFs(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestión de PDFs (Conocimiento Local)")
        self.resize(450, 350)
        layout = QVBoxLayout(self)
        self.lista_pdfs = QListWidget()
        layout.addWidget(self.lista_pdfs)
        
        layout_botones = QHBoxLayout()
        self.btn_anadir = QPushButton("Añadir PDF")
        self.btn_eliminar = QPushButton("Eliminar Seleccionado")
        self.btn_vaciar = QPushButton("Vaciar Lista")
        layout_botones.addWidget(self.btn_anadir)
        layout_botones.addWidget(self.btn_eliminar)
        layout_botones.addWidget(self.btn_vaciar)
        layout.addLayout(layout_botones)

class DialogoWeb(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Fuentes Web Utilizadas")
        self.resize(600, 250)
        layout = QVBoxLayout(self)
        self.tabla = QTableWidget(0, 3)
        self.tabla.setHorizontalHeaderLabels(["Título", "URL", "Fecha Acceso"])
        self.tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla)
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.accept)
        layout.addWidget(btn_cerrar)