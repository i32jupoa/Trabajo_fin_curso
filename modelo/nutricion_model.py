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
        
        if not self.modo_web:
            self._generar_diagnostico_fallback()
            return

        texto_pdf = self.extraer_texto_pdfs()
        
        # PROMPT DE INGENIERÍA CLÍNICA (FUERZA ESTRUCTURA PROFESIONAL)
        prompt = (
            "EMITE UN INFORME MÉDICO NUTRICIONAL FORMAL EN ESPAÑOL.\n\n"
            "DATOS TÉCNICOS:\n"
            f"- IMC: {self.imc} | Sueño: {self.horas_sueno}h.\n"
            f"- Síntomas: {', '.join(self.sintomas_seleccionados) if self.sintomas_seleccionados else 'Asintomático'}.\n"
            f"- Frecuencia Dieta: Basura {self.dieta.get('bolleria')}, Verduras {self.dieta.get('verduras')}, "
            f"Carne {self.dieta.get('carne')}, Pescado {self.dieta.get('pescado')}.\n"
        )
        
        if texto_pdf: prompt += f"CONTEXTO ADICIONAL (PDF): {texto_pdf}\n\n"
            
        prompt += (
            "ESCRIBE EL INFORME SIGUIENDO ESTE ESQUEMA EXACTO:\n"
            "1. IMPRESIÓN CLÍNICA: (Análisis del estado nutricional actual)\n"
            "2. CORRELACIÓN DIETA-SÍNTOMAS: (Explica por qué su alimentación causa esos signos físicos)\n"
            "3. VALORACIÓN DEL DESCANSO: (Impacto de las horas de sueño en su metabolismo)\n"
            "4. RECOMENDACIÓN:\n\n"
            "INFORME MÉDICO:\n"
        )

        try:
            respuesta = requests.post("http://localhost:11434/api/generate", 
                                      json={"model": "tinyllama", "prompt": prompt, "stream": False}, timeout=45)
            respuesta.raise_for_status()
            resultado_llm = respuesta.json().get("response", "")
            
            # Limpiamos posibles restos del prompt que la IA a veces repite
            limpio = resultado_llm.replace("INFORME MÉDICO:", "").strip()
            
            self.diagnostico_final = "DIAGNÓSTICO AVANZADO (Inteligencia Artificial):\n" + limpio.split("2.")[0]
            self.justificacion = "ANÁLISIS CLÍNICO DETALLADO (TinyLlama):\n" + limpio
            
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
        """Genera un informe clínico profesional basado en el motor de reglas local"""
        self.diagnostico_final = "INFORME DEL SISTEMA EXPERTO LOCAL (Reglas Clínicas)\n"
        self.diagnostico_final += "================================================\n\n"
        
        # 1. Análisis Biométrico (IMC)
        cat_imc = "Normopeso"
        if self.imc < 18.5: cat_imc = "Bajo Peso (Riesgo de Desnutrición)"
        elif 25 <= self.imc < 30: cat_imc = "Sobrepeso Grado I"
        elif self.imc >= 30: cat_imc = "Obesidad Clínica"
        
        self.diagnostico_final += f"VALORACIÓN ANTROPOMÉTRICA:\n"
        self.diagnostico_final += f"- El paciente presenta un IMC de {self.imc}, clasificado como {cat_imc}.\n"
        
        # 2. Análisis de Descanso
        if self.horas_sueno < 6:
            self.diagnostico_final += f"- Alerta: Privación de sueño ({self.horas_sueno}h). Interferencia directa en la recuperación metabólica.\n"
        else:
            self.diagnostico_final += f"- Patrón de descanso adecuado ({self.horas_sueno}h).\n"

        self.diagnostico_final += "\nDIAGNÓSTICO PRESUNTIVO:\n"
        
        # 3. Lógica de Diagnóstico Principal
        if self.hipotesis and self.hipotesis[0][0] != "Estado Nutricional Aparentemente Adecuado":
            principal = self.hipotesis[0]
            self.diagnostico_final += f"Se detecta con una probabilidad del {principal[1]}: {principal[0]}.\n"
            
            # Justificación Detallada
            self.justificacion = "JUSTIFICACIÓN TÉCNICA DEL MOTOR DE INFERENCIA:\n"
            self.justificacion += "-------------------------------------------\n"
            
            # Cruce de datos para la justificación
            d = self.dieta
            s = self.sintomas_seleccionados
            
            if "Fatiga extrema" in s and d.get("carne") in ["0 días (Nunca)", "1-2 días"]:
                self.justificacion += "- Correlación detectada entre Fatiga y baja ingesta de proteínas/hierro hemínico.\n"
            
            if d.get("verduras") in ["0 días (Nunca)", "1-2 días"]:
                self.justificacion += "- Déficit crítico de fibra y micronutrientes (vitaminas hidrosolubles).\n"
            
            if d.get("bolleria") in ["3-4 días", "5-6 días", "7 días (Diario)"]:
                self.justificacion += "- Exceso de ácidos grasos trans y azúcares simples, lo que explica el riesgo metabólico.\n"
                
            if "Niebla mental" in s and self.horas_sueno < 6:
                self.justificacion += "- La sintomatología cognitiva (niebla mental) se vincula directamente con el déficit de sueño profundo.\n"

        else:
            self.diagnostico_final += "No se observan patologías nutricionales agudas bajo los parámetros actuales.\n"
            self.justificacion = "El motor de reglas no ha detectado discrepancias significativas entre la ingesta reportada y el estado físico."

        self.justificacion += f"\n\nObservaciones: Este informe ha sido generado mediante el motor de reglas estáticas del sistema ISSBC."