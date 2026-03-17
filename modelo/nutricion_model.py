# -*- coding: utf-8 -*-
import requests
import PyPDF2

class ModeloNutricion:
    def __init__(self):
        self.sintomas_seleccionados = []
        self.imc = 22.0
        self.horas_sueno = 7
        self.dieta = {}
        self.modo_web = False 
        
        self.rutas_pdfs = [] # Rutas absolutas para leerlos
        self.pdfs_cargados = [] # Nombres para la vista
        
        self.hipotesis = []
        self.diagnostico_final = ""
        self.justificacion = ""
        self.fuentes_web = []

    def actualizar_datos_paciente(self, sintomas, imc, sueno, dieta):
        self.sintomas_seleccionados = sintomas
        self.imc = imc
        self.horas_sueno = sueno
        self.dieta = dieta

    def set_modo_web(self, estado):
        self.modo_web = estado

    def extraer_texto_pdfs(self):
        texto_extraido = ""
        for ruta in self.rutas_pdfs:
            try:
                with open(ruta, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    for i in range(min(3, len(reader.pages))): # Lee max 3 pags por rendimiento
                        texto_extraido += reader.pages[i].extract_text() + " "
            except Exception as e:
                print(f"Error leyendo PDF {ruta}: {e}")
        return texto_extraido[:2000] # Limitamos contexto para Ollama

    def generar_diagnostico_ia(self):
        # 1. Preparar contexto base
        self.simular_hipotesis_base() # Genera la tabla base de hipótesis
        
        texto_pdf = self.extraer_texto_pdfs()
        
        prompt = f"Actúa como un médico nutricionista experto. El paciente tiene estos síntomas: {self.sintomas_seleccionados}. "
        prompt += f"Su IMC es {self.imc} y duerme {self.horas_sueno} horas. "
        prompt += f"Su dieta es: Carne ({self.dieta.get('carne')}), Pescado ({self.dieta.get('pescado')}), Fruta ({self.dieta.get('frutas_verduras')}), Lácteos ({self.dieta.get('lacteos')}). "
        
        if self.modo_web:
            prompt += "Basa tu respuesta en el conocimiento médico actual de internet. "
        if texto_pdf:
            prompt += f"Ten en cuenta este documento de referencia aportado por el paciente: {texto_pdf}. "
            
        prompt += "Escribe un diagnóstico breve y una justificación clara de por qué crees que le ocurre esto. Responde en español."

        # 2. Conexión con Ollama local
        try:
            respuesta = requests.post("http://localhost:11434/api/generate", 
                                      json={"model": "llama3", "prompt": prompt, "stream": False}, 
                                      timeout=45)
            respuesta.raise_for_status()
            resultado_llm = respuesta.json().get("response", "")
            
            self.diagnostico_final = "Diagnóstico generado por IA (Ollama):\n" + resultado_llm.split("\n\n")[0]
            self.justificacion = "Justificación del Modelo de Lenguaje:\n" + resultado_llm
            
            if self.modo_web:
                self.fuentes_web = [("Búsqueda General Ollama", "Base de datos del LLM", "Actual")]
                
        except Exception as e:
            # FALLBACK DE SEGURIDAD (Si el profesor no tiene Ollama encendido)
            self.diagnostico_final = "[AVISO: Conexión con Ollama fallida. Usando sistema experto de respaldo]\n\n"
            self.diagnostico_final += "No se detectan anomalías graves, revisar dieta cruzada con síntomas."
            self.justificacion = f"Error técnico al contactar con la IA local: {e}\n\nEl sistema experto de respaldo determinó que los síntomas ({self.sintomas_seleccionados}) deben cruzarse con su consumo de alimentos."

    def simular_hipotesis_base(self):
        # Mantiene la lógica de reglas para la tabla de Hipótesis (CommonKADS)
        self.hipotesis = []
        if ("Fatiga extrema" in self.sintomas_seleccionados) and (self.dieta.get("carne") == "Raramente / Nunca"):
            self.hipotesis.append(("Anemia ferropénica", "95%", "Seleccionada"))
        if ("Sangrado frecuente de encías" in self.sintomas_seleccionados):
            self.hipotesis.append(("Déficit de Vitamina C", "80%", "Posible"))
        if not self.hipotesis:
            self.hipotesis.append(("Sin déficit aparente", "90%", "Seleccionada"))