# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QFileDialog
from vista.dialogos_view import DialogoHipotesis, DialogoTexto, DialogoPDFs, DialogoWeb

class ControladorNutricion:
    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista
        self.conectar_senales()

    def conectar_senales(self):
        self.vista.btn_evaluar.clicked.connect(self.procesar_hipotesis)
        self.vista.btn_diagnosticar.clicked.connect(self.mostrar_diagnostico)
        self.vista.btn_justificacion.clicked.connect(self.mostrar_justificacion)
        self.vista.btn_pdfs.clicked.connect(self.abrir_gestion_pdfs)
        self.vista.btn_web.clicked.connect(self.abrir_fuentes_web)
        self.vista.radio_web.toggled.connect(self.cambiar_modo)

    def actualizar_modelo_y_simular(self):
        # Actualiza el modelo con la interfaz y lanza el LLM
        sintomas = self.vista.obtener_sintomas_marcados()
        imc = self.vista.spin_imc.value()
        sueno = self.vista.spin_sueno.value()
        self.modelo.actualizar_datos_paciente(sintomas, imc, sueno)
        self.modelo.simular_evaluacion_llm()

    def cambiar_modo(self):
        self.modelo.set_modo_web(self.vista.radio_web.isChecked())

    def procesar_hipotesis(self):
        self.actualizar_modelo_y_simular()
        dialogo = DialogoHipotesis(self.vista)
        # Rellenar tabla con el modelo
        dialogo.tabla.setRowCount(len(self.modelo.hipotesis))
        for row, (nombre, prob, estado) in enumerate(self.modelo.hipotesis):
            dialogo.tabla.setItem(row, 0, QTableWidgetItem(nombre))
            dialogo.tabla.setItem(row, 1, QTableWidgetItem(prob))
            dialogo.tabla.setItem(row, 2, QTableWidgetItem(estado))
        dialogo.exec()

    def mostrar_diagnostico(self):
        self.actualizar_modelo_y_simular()
        dialogo = DialogoTexto("Diagnóstico Final", self.vista)
        dialogo.texto.setText(self.modelo.diagnostico_final)
        dialogo.exec()

    def mostrar_justificacion(self):
        self.actualizar_modelo_y_simular()
        dialogo = DialogoTexto("Justificación del Diagnóstico", self.vista)
        dialogo.texto.setText(self.modelo.justificacion)
        dialogo.exec()

    def abrir_gestion_pdfs(self):
        dialogo = DialogoPDFs(self.vista)
        # Poblar lista
        dialogo.lista_pdfs.addItems(self.modelo.pdfs_cargados)
        
        # Conectar botones del diálogo
        def anadir_pdf():
            ruta, _ = QFileDialog.getOpenFileName(dialogo, "Seleccionar PDF", "", "PDF Files (*.pdf)")
            if ruta:
                nombre_archivo = ruta.split("/")[-1]
                self.modelo.pdfs_cargados.append(nombre_archivo)
                dialogo.lista_pdfs.addItem(nombre_archivo)
                
        def vaciar():
            self.modelo.pdfs_cargados.clear()
            dialogo.lista_pdfs.clear()
            
        dialogo.btn_anadir.clicked.connect(anadir_pdf)
        dialogo.btn_vaciar.clicked.connect(vaciar)
        dialogo.exec()

    def abrir_fuentes_web(self):
        if not self.modelo.modo_web:
            QMessageBox.warning(self.vista, "Atención", "El modo web está desactivado.")
            return
        self.actualizar_modelo_y_simular()
        dialogo = DialogoWeb(self.vista)
        dialogo.tabla.setRowCount(len(self.modelo.fuentes_web))
        for row, (titulo, url, fecha) in enumerate(self.modelo.fuentes_web):
            dialogo.tabla.setItem(row, 0, QTableWidgetItem(titulo))
            dialogo.tabla.setItem(row, 1, QTableWidgetItem(url))
            dialogo.tabla.setItem(row, 2, QTableWidgetItem(fecha))
        dialogo.exec()

        