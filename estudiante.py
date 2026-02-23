class Estudiante:
    def __init__(self, nombre, email):
        self.nombre = nombre
        self.email = email
        self.tareas = []
        self.beneficios = []
        self.monedas = 0

    def checkearTareas(self):
        print(f"\nTareas de {self.nombre}:")
        for tarea in self.tareas:
            print(f"- {tarea.nombre} | Estado: {tarea.estado}")

    def agregarBeneficio(self, beneficio):
        self.beneficios.append(beneficio)

    def canjearBeneficio(self, beneficio, profesor):
        if beneficio in self.beneficios:
            self.monedas += beneficio.valor
            self.beneficios.remove(beneficio)
            print(f"\n{self.nombre} canjeó el beneficio '{beneficio.nombre}'")
            profesor.notificarCanje(self, beneficio)
        else:
            print("\nBeneficio no disponible")

