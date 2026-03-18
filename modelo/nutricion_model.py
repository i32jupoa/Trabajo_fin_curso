# -*- coding: utf-8 -*-
import requests
import PyPDF2

class ModeloNutricion:
    def __init__(self):
        self.sintomas_seleccionados = []
        self.imc = 22.0
        self.horas_sueno = 7
        self.dieta = {}
        self.modo_web = True # Lo ponemos en True por defecto para que coincida con la interfaz
        
        self.rutas_pdfs = [] 
        self.pdfs_cargados = [] 
        
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
                    for i in range(min(3, len(reader.pages))): 
                        texto_extraido += reader.pages[i].extract_text() + " "
            except Exception as e:
                print(f"Error leyendo PDF: {e}")
        return texto_extraido[:2000]

    def generar_diagnostico_ia(self):
        self.simular_hipotesis_base() 
        
        # --- AQUÍ ESTÁ LA MAGIA DEL MODO RESPALDO ---
        # Si el usuario marca "Modo Respaldo", el programa entra aquí, 
        # genera el texto local al instante y NO llama a la IA.
        if not self.modo_web:
            self._generar_diagnostico_fallback()
            return
        # ---------------------------------------------

        texto_pdf = self.extraer_texto_pdfs()
        
        # PROMPT OPTIMIZADO PARA TINYLLAMA
        prompt = f"Actúa como un médico nutricionista experto. Perfil del paciente: IMC de {self.imc}, duerme {self.horas_sueno} horas/día. "
        prompt += f"Síntomas: {', '.join(self.sintomas_seleccionados) if self.sintomas_seleccionados else 'Asintomático'}. "
        prompt += f"Frecuencia semanal de dieta: Bollería/basura {self.dieta.get('bolleria', '0 días')} a la semana, "
        prompt += f"verduras {self.dieta.get('verduras', '0 días')} a la semana, carne {self.dieta.get('carne', '0 días')}, "
        prompt += f"pescado {self.dieta.get('pescado', '0 días')}. "
        
        if self.modo_web: prompt += "Basa tu respuesta en evidencia médica clínica. "
        if texto_pdf: prompt += f"Aplica este conocimiento extraído de un PDF: {texto_pdf}. "
            
        prompt += "Proporciona un Diagnóstico claro y una Justificación de por qué su dieta, sueño e IMC causan estos síntomas. Responde en español."

        try:
            respuesta = requests.post("http://localhost:11434/api/generate", 
                                      json={"model": "tinyllama", "prompt": prompt, "stream": False}, timeout=45)
            respuesta.raise_for_status()
            resultado_llm = respuesta.json().get("response", "")
            
            self.diagnostico_final = "DIAGNÓSTICO IA (TinyLlama):\n" + resultado_llm.split("\n\n")[0]
            self.justificacion = "JUSTIFICACIÓN CLÍNICA (TinyLlama):\n" + resultado_llm
            if self.modo_web:
                self.fuentes_web = [("Análisis Nutricional IA", "Base de datos LLM Interna", "Actual")]
                
        except Exception as e:
            print(f"Fallo conexión IA: {e}")
            self._generar_diagnostico_fallback()

    def simular_hipotesis_base(self):
        self.hipotesis = []
        d = self.dieta
        s = self.sintomas_seleccionados
        
        alerta_procesados = ["3-4 días", "5-6 días", "7 días (Diario)"]
        carencia_total = ["0 días (Nunca)", "1-2 días"]

        if self.imc >= 25.0 and (d.get("bolleria") in alerta_procesados or d.get("basura") in alerta_procesados):
            prob = "95%" if self.imc >= 30.0 else "80%"
            self.hipotesis.append(("Riesgo de Síndrome Metabólico (Malnutrición por exceso)", prob, "Seleccionada"))

        if self.horas_sueno < 6 and ("Fatiga extrema" in s or "Niebla mental" in s):
            self.hipotesis.append(("Agotamiento crónico por privación de sueño", "90%", "Muy Posible"))

        if ("Fatiga extrema" in s or "Palidez en piel/mucosas" in s) and d.get("carne") in carencia_total:
            self.hipotesis.append(("Anemia ferropénica o déficit de B12", "85%", "Posible"))

        if ("Sangrado de encías" in s or "Estreñimiento crónico" in s) and (d.get("verduras") in carencia_total and d.get("frutas") in carencia_total):
            self.hipotesis.append(("Déficit de Fibra y Vitamina C", "88%", "Posible"))

        if "Niebla mental" in s and d.get("pescado") == "0 días (Nunca)" and d.get("frutos_secos") == "0 días (Nunca)":
            self.hipotesis.append(("Déficit de Ácidos Grasos Esenciales (Omega 3)", "75%", "Posible"))
            
        if self.imc < 18.5:
            self.hipotesis.append(("Riesgo de desnutrición calórico-proteica", "90%", "Alerta"))

        if not self.hipotesis:
            self.hipotesis.append(("Estado Nutricional Aparentemente Adecuado", "95%", "Seleccionada"))
            
        self.hipotesis.sort(key=lambda x: int(x[1].replace('%','')), reverse=True)

    def _generar_diagnostico_fallback(self):
        self.diagnostico_final = "[MODO EXPERTO LOCAL - Basado en Reglas Estrictas]\n\n"
        self.justificacion = "[RAZONAMIENTO DEL SISTEMA EXPERTO LOCAL]\n"
        
        cat_imc = "Normal"
        if self.imc < 18.5: cat_imc = "Bajo Peso (Riesgo de desnutrición)"
        elif self.imc >= 25 and self.imc < 30: cat_imc = "Sobrepeso"
        elif self.imc >= 30: cat_imc = "Obesidad (Riesgo cardiovascular)"

        self.justificacion += f"- Evaluación Biométrica: IMC de {self.imc} ({cat_imc}).\n"
        self.justificacion += f"- Evaluación del Descanso: {self.horas_sueno} horas diarias. "
        self.justificacion += "Insuficiente para recuperación celular.\n" if self.horas_sueno < 6 else "Adecuado.\n"

        if len(self.hipotesis) > 0 and self.hipotesis[0][0] != "Estado Nutricional Aparentemente Adecuado":
            self.diagnostico_final += f"El paciente presenta: {self.hipotesis[0][0]}.\n"
            if len(self.hipotesis) > 1: self.diagnostico_final += f"Comorbilidad asociada: {self.hipotesis[1][0]}.\n"
            
            self.justificacion += "\nCruces detectados (Síntomas vs Dieta):\n"
            if self.dieta.get('bolleria') in ["3-4 días", "5-6 días", "7 días (Diario)"]: self.justificacion += "-> Elevado consumo de ultraprocesados.\n"
            if self.dieta.get('verduras') in ["0 días (Nunca)", "1-2 días"]: self.justificacion += "-> Carencia crítica de micronutrientes y fibra vegetal.\n"
            if self.sintomas_seleccionados: self.justificacion += f"-> Síntomas a vigilar: {', '.join(self.sintomas_seleccionados)}."
        else:
            self.diagnostico_final += "No se detectan alteraciones graves. Mantener el estilo de vida actual."
            self.justificacion += "\nLos hábitos dietéticos y el descanso se encuentran en equilibrio con el estado físico reportado."