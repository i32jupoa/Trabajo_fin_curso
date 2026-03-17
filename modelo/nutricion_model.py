# -*- coding: utf-8 -*-
class ModeloNutricion:
    def __init__(self):
        self.sintomas_seleccionados = []
        self.imc = 22.0
        self.horas_sueno = 7
        self.modo_web = False 
        
        # Datos generados por el sistema (LLM simulado)
        self.pdfs_cargados = [] 
        self.hipotesis = []
        self.diagnostico_final = ""
        self.justificacion = ""
        self.fuentes_web = []

    def actualizar_datos_paciente(self, sintomas, imc, sueno):
        self.sintomas_seleccionados = sintomas
        self.imc = imc
        self.horas_sueno = sueno

    def set_modo_web(self, estado):
        self.modo_web = estado

    def simular_evaluacion_llm(self):
        sintomas = self.sintomas_seleccionados
        self.hipotesis = []
        self.fuentes_web = []
        diagnosticos_text = []

        # Lógica 1: Anemia (Falta de hierro)
        if "Fatiga extrema" in sintomas or "Palidez" in sintomas:
            self.hipotesis.append(("Anemia ferropénica (Déficit de hierro)", "85%", "Posible"))
            diagnosticos_text.append("Déficit de hierro por signos de falta de oxigenación celular.")
            self.fuentes_web.append(("Anemia - MedlinePlus", "https://medlineplus.gov/spanish/anemia.html", "2026-03-17"))

        # Lógica 2: Vitamina C (Escorbuto leve)
        if "Sangrado de encías" in sintomas or "Mala cicatrización" in sintomas:
            self.hipotesis.append(("Déficit de Vitamina C", "75%", "Posible"))
            diagnosticos_text.append("Posible déficit de Vitamina C afectando a mucosas y regeneración de tejidos.")
            self.fuentes_web.append(("Vitamina C - NIH", "https://ods.od.nih.gov/factsheets/VitaminC-DatosEnEspanol/", "2026-03-17"))

        # Lógica 3: Minerales (Magnesio/Potasio)
        if "Calambres musculares" in sintomas or "Estreñimiento crónico" in sintomas:
            self.hipotesis.append(("Déficit de Magnesio / Potasio", "70%", "Posible"))
            diagnosticos_text.append("Desequilibrio de electrolitos (Magnesio/Potasio) evidenciado por disfunción muscular.")

        # Lógica 4: Complejo B (B12)
        if "Hormigueo en extremidades" in sintomas or "Falta de concentración" in sintomas:
            self.hipotesis.append(("Déficit de Vitamina B12", "80%", "Posible"))
            diagnosticos_text.append("Alteraciones neurológicas compatibles con falta de Vitamina B12.")

        # Resolver el diagnóstico final
        if not self.hipotesis:
            self.hipotesis = [("Dieta equilibrada (Sin déficit aparente)", "95%", "Seleccionada")]
            self.diagnostico_final = "No se detectan déficits nutricionales graves con los datos introducidos."
            self.justificacion = f"IMC registrado: {self.imc}. Horas de sueño: {self.horas_sueno}. No se han introducido síntomas físicos de alarma que requieran atención inmediata."
        else:
            # Marcar la primera como seleccionada
            self.hipotesis[0] = (self.hipotesis[0][0], self.hipotesis[0][1], "Seleccionada (Principal)")
            self.diagnostico_final = " | ".join(diagnosticos_text)
            self.justificacion = f"El LLM ha analizado las siguientes evidencias reportadas: {', '.join(sintomas)}. \n\nRazonamiento clínico simulado:\nEl cruce de estos síntomas con la base de datos nutricional apunta a deficiencias sistémicas. IMC reportado: {self.imc}."