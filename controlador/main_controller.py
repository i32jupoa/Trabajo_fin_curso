# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QFileDialog
from PyQt6.QtCore import QThread, pyqtSignal
from vista.dialogos_view import DialogoHipotesis, DialogoTexto, DialogoPDFs, DialogoWeb

# Hilo para que la UI no se bloquee mientras la IA piensa
class WorkerIA(QThread):
    finished = pyqtSignal()
    
    def __init__(self, modelo):
        super().__init__()
        self.modelo = modelo
        
    def run(self):
        self.modelo.generar_diagnostico_ia()
        self.finished.emit()

class ControladorNutricion:
    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista
        self.hilo_ia = WorkerIA(self.modelo)
        self.hilo_ia.finished.connect(self.on_ia_terminada)
        self.accion_pendiente = "" # Para saber qué ventana abrir tras pensar
        self.conectar_senales()

    def conectar_senales(self):
        self.vista.btn_evaluar.clicked.connect(self.procesar_hipotesis)
        self.vista.btn_diagnosticar.clicked.connect(lambda: self.iniciar_procesamiento_ia("diagnostico"))
        self.vista.btn_justificacion.clicked.connect(lambda: self.iniciar_procesamiento_ia("justificacion"))
        self.vista.btn_pdfs.clicked.connect(self.abrir_gestion_pdfs)
        self.vista.btn_web.clicked.connect(self.abrir_fuentes_web)
        self.vista.radio_web.toggled.connect(self.cambiar_modo)

    def actualizar_datos_basicos(self):
        sintomas = self.vista.obtener_sintomas_marcados()
        imc = self.vista.spin_imc.value()
        sueno = self.vista.spin_sueno.value()
        dieta = {
            "carne": self.vista.combo_carne.currentText(),
            "pescado": self.vista.combo_pescado.currentText(),
            "frutas_verduras": self.vista.combo_frutas.currentText(),
            "lacteos": self.vista.combo_lacteos.currentText()
        }
        self.modelo.actualizar_datos_paciente(sintomas, imc, sueno, dieta)

    def cambiar_modo(self):
        self.modelo.set_modo_web(self.vista.radio_web.isChecked())

    def procesar_hipotesis(self):
        self.actualizar_datos_basicos()
        self.modelo.simular_hipotesis_base() # Rápido, sin IA pesada
        dialogo = DialogoHipotesis(self.vista)
        dialogo.tabla.setRowCount(len(self.modelo.hipotesis))
        for row, (nombre, prob, estado) in enumerate(self.modelo.hipotesis):
            dialogo.tabla.setItem(row, 0, QTableWidgetItem(nombre))
            dialogo.tabla.setItem(row, 1, QTableWidgetItem(prob))
            dialogo.tabla.setItem(row, 2, QTableWidgetItem(estado))
        dialogo.exec()

    # --- INICIO BLOQUE ASÍNCRONO ---
    def iniciar_procesamiento_ia(self, accion):
        self.actualizar_datos_basicos()
        self.accion_pendiente = accion
        
        # Bloquear botones y avisar al usuario
        self.vista.btn_diagnosticar.setText("Generando IA...")
        self.vista.btn_diagnosticar.setEnabled(False)
        self.vista.btn_justificacion.setEnabled(False)
        
        self.hilo_ia.start() # Lanza la IA en segundo plano

    def on_ia_terminada(self):
        # Desbloquear botones
        self.vista.btn_diagnosticar.setText("2. Diagnosticar")
        self.vista.btn_diagnosticar.setEnabled(True)
        self.vista.btn_justificacion.setEnabled(True)
        
        # Abrir la ventana solicitada
        if self.accion_pendiente == "diagnostico":
            dialogo = DialogoTexto("Diagnóstico Final (LLM)", self.vista)
            dialogo.texto.setText(self.modelo.diagnostico_final)
            dialogo.exec()
        elif self.accion_pendiente == "justificacion":
            dialogo = DialogoTexto("Justificación y Razonamiento", self.vista)
            dialogo.texto.setText(self.modelo.justificacion)
            dialogo.exec()
    # --- FIN BLOQUE ASÍNCRONO ---

    def abrir_gestion_pdfs(self):
        dialogo = DialogoPDFs(self.vista)
        dialogo.lista_pdfs.addItems(self.modelo.pdfs_cargados)
        
        def anadir_pdf():
            rutas, _ = QFileDialog.getOpenFileNames(dialogo, "Seleccionar PDFs", "", "PDF Files (*.pdf)")
            for ruta in rutas:
                if ruta not in self.modelo.rutas_pdfs:
                    self.modelo.rutas_pdfs.append(ruta) # Guarda ruta absoluta para el modelo
                    nombre = ruta.split("/")[-1]
                    self.modelo.pdfs_cargados.append(nombre)
                    dialogo.lista_pdfs.addItem(nombre)
                    
        def eliminar_pdf():
            items_seleccionados = dialogo.lista_pdfs.selectedItems()
            for item in items_seleccionados:
                idx = self.modelo.pdfs_cargados.index(item.text())
                self.modelo.pdfs_cargados.pop(idx)
                self.modelo.rutas_pdfs.pop(idx)
                dialogo.lista_pdfs.takeItem(dialogo.lista_pdfs.row(item))
                
        def vaciar():
            self.modelo.pdfs_cargados.clear()
            self.modelo.rutas_pdfs.clear()
            dialogo.lista_pdfs.clear()
            
        dialogo.btn_anadir.clicked.connect(anadir_pdf)
        dialogo.btn_eliminar.clicked.connect(eliminar_pdf)
        dialogo.btn_vaciar.clicked.connect(vaciar)
        dialogo.exec()

    def abrir_fuentes_web(self):
        if not self.modelo.modo_web:
            QMessageBox.warning(self.vista, "Modo Local", "El Modo Web está desactivado. Actívelo en la ventana principal.")
            return
        dialogo = DialogoWeb(self.vista)
        dialogo.tabla.setRowCount(len(self.modelo.fuentes_web))
        for row, (titulo, url, fecha) in enumerate(self.modelo.fuentes_web):
            dialogo.tabla.setItem(row, 0, QTableWidgetItem(titulo))
            dialogo.tabla.setItem(row, 1, QTableWidgetItem(url))
            dialogo.tabla.setItem(row, 2, QTableWidgetItem(fecha))
        dialogo.exec()