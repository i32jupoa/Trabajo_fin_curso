# -*- coding: utf-8 -*-
class ModeloNutricion:
    def __init__(self):
        # Datos de entrada del paciente
        self.sintomas_seleccionados = []
        self.imc = 22.0
        self.horas_sueno = 7
        self.dieta = {}
        self.modo_web = False 
        
        # Datos de salida (LLM simulado y estado)
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

    def simular_evaluacion_llm(self):
        sintomas = self.sintomas_seleccionados
        dieta = self.dieta
        self.hipotesis = []
        self.fuentes_web = []
        diagnosticos_text = []
        justificaciones_text = []

        # Lógica 1: Anemia (Falta de hierro / B12)
        if ("Fatiga extrema" in sintomas or "Palidez" in sintomas) and (dieta.get("carne") == "Raramente / Nunca"):
            self.hipotesis.append(("Anemia ferropénica / Déficit B12", "95%", "Muy Probable"))
            diagnosticos_text.append("Déficit severo de hierro o B12 derivado de una ingesta nula de carnes rojas.")
            justificaciones_text.append("La fatiga y palidez cruzada con la exclusión de carne en la dieta es el principal indicador de Anemia.")
            self.fuentes_web.append(("Anemia por deficiencia de vitaminas - Mayo Clinic", "https://www.mayoclinic.org/", "2026-03-17"))

        # Lógica 2: Vitamina C (Escorbuto leve)
        if ("Sangrado frecuente de encías" in sintomas or "Retraso en cicatrización" in sintomas) and (dieta.get("frutas_verduras") == "Raramente / Nunca"):
            self.hipotesis.append(("Déficit de Vitamina C", "88%", "Posible"))
            diagnosticos_text.append("Posible déficit de Vitamina C afectando a mucosas.")
            justificaciones_text.append("El sangrado de encías sumado a la nula ingesta de frutas frescas apunta directamente a un cuadro carencial de Vitamina C.")

        # Lógica 3: Minerales (Falta de Calcio/Magnesio)
        if ("Uñas frágiles con manchas" in sintomas or "Calambres musculares" in sintomas) and (dieta.get("lacteos") == "Raramente / Nunca"):
            self.hipotesis.append(("Déficit de Calcio / Magnesio", "75%", "Posible"))
            diagnosticos_text.append("Desmineralización o desequilibrio electrolítico por bajo consumo de lácteos.")
            justificaciones_text.append("Las uñas frágiles y calambres coinciden con un bajo consumo de lácteos, indicando posible falta de calcio biodisponible.")

        # Lógica 4: Omega 3 y Pescado
        if ("Niebla mental" in sintomas) and (dieta.get("pescado") == "Raramente / Nunca"):
            self.hipotesis.append(("Déficit de Ácidos Grasos (Omega-3)", "60%", "Posible"))
            diagnosticos_text.append("Deterioro cognitivo leve asociado a carencia de grasas esenciales.")
            justificaciones_text.append("La falta de concentración se correlaciona con carencia de Omega-3 por evitar el pescado.")

        # Resolver el diagnóstico final
        if not self.hipotesis:
            self.hipotesis = [("Dieta equilibrada (Sin déficit cruzado aparente)", "90%", "Seleccionada")]
            self.diagnostico_final = "No se detectan déficits nutricionales graves correlacionados con la dieta y síntomas."
            self.justificacion = f"IMC: {self.imc}. Horas de sueño: {self.horas_sueno}.\nAunque puede haber síntomas leves, no cruzan con carencias alimenticias evidentes."
        else:
            self.hipotesis.sort(key=lambda x: int(x[1].strip('%')), reverse=True) # Ordenar por probabilidad
            self.hipotesis[0] = (self.hipotesis[0][0], self.hipotesis[0][1], "Seleccionada (Principal)")
            self.diagnostico_final = "\n\n".join(diagnosticos_text)
            self.justificacion = "El LLM simulado ha cruzado sus hábitos alimenticios con sus síntomas físicos:\n\n" + "\n".join(justificaciones_text)