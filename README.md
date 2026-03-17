# Trabajo Fin Curso
Álvaro Jurado Pozo (i32jupoa@uco.es)

Ádam Gálvez Redondo (i32garea@uco.es)

# Sistema de Diagnóstico Nutricional - ISSBC

## 1. Dominio elegido y descripción
El dominio seleccionado para este proyecto es el **Diagnóstico de problemas nutricionales básicos**. La aplicación actúa como una interfaz de apoyo clínico que recopila síntomas físicos, signos observables (IMC, calidad del sueño) y hábitos alimenticios (frecuencia de consumo de proteínas, vitaminas, lácteos, etc.) para inferir posibles déficits nutricionales (como anemia o falta de vitaminas). El diagnóstico final y la justificación del razonamiento se simulan mediante la integración futura con un Modelo de Lenguaje Grande (LLM) ejecutado en local.

## 2. Instrucciones de ejecución
Para ejecutar la aplicación correctamente, se requiere tener instalado Python 3 y el framework gráfico PyQt6.
1. Abrir una terminal en el directorio raíz del proyecto (donde se encuentra este `README.md`).
2. Instalar las dependencias necesarias: `pip install PyQt6`
3. Ejecutar el orquestador principal: `python3 main.py`

## 3. Descripción de la arquitectura MVC usada
El proyecto aplica estrictamente el patrón Modelo-Vista-Controlador mediante una separación física en paquetes de Python:
* **Modelo (`modelo/nutricion_model.py`):** Mantiene el estado de la aplicación (síntomas seleccionados, métricas, dieta). Contiene la lógica pura y las estructuras de datos que manejan las hipótesis y simulan la respuesta del LLM. No tiene dependencias de la interfaz gráfica.
* **Vista (`vista/`):** Dividida en `principal_view.py` (ventana principal de recolección de evidencias) y `dialogos_view.py` (ventanas secundarias para mostrar resultados, gestionar PDFs y fuentes web). Construida íntegramente con PyQt6, su única labor es mostrar datos y capturar eventos del usuario.
* **Controlador (`controlador/main_controller.py`):** Actúa como intermediario. Se suscribe a los eventos de la vista (clicks, cambios de estado), extrae sus datos, actualiza el Modelo y determina qué nueva ventana o diálogo debe renderizarse con la información procesada.

## 4. Explicación del modo Local/Web y su reflejo en la UI
La aplicación incorpora un selector de "Modo de Conocimiento" en la interfaz principal (RadioButtons) que permite al usuario acotar el contexto que utilizará el LLM:
* **Modo Local:** El LLM solo basará sus inferencias en las entradas del usuario y en los documentos añadidos mediante la herramienta "Gestión de PDFs". La ventana de "Fuentes Web" se desactiva.
* **Modo Web:** Habilita al LLM para incorporar información fiable obtenida de internet, además de los recursos locales. Al usar este modo, la UI permite abrir la ventana "Fuentes Web", donde se trazan y listan las URLs y títulos de los artículos médicos consultados por la IA para emitir su justificación.
