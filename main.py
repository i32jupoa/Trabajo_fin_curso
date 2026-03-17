# -*- coding: utf-8 -*-
import sys
from PyQt6.QtWidgets import QApplication

# Importación desde las carpetas (paquetes)
from modelo.nutricion_model import ModeloNutricion
from vista.principal_view import VistaPrincipal
from controlador.main_controller import ControladorNutricion

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Ensamblaje MVC
    modelo = ModeloNutricion()
    vista = VistaPrincipal()
    controlador = ControladorNutricion(modelo, vista)
    
    vista.show()
    sys.exit(app.exec())