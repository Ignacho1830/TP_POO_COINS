# main.py
from profesor import Profesor
from estudiante import Estudiante
from tarea import Tarea
from beneficio import Beneficio

def ejemplo_modo_simulacion():
    """
    Ejemplo 1: Modo simulación (sin enviar emails reales)
    Útil para desarrollo y pruebas sin configurar Gmail
    """
    print("\n" + "="*80)
    print("EJEMPLO 1: MODO SIMULACIÓN")
    print("="*80)
    
    # Crear profesor en modo simulación (usar_gmail_real=False)
    profesor = Profesor("Carlos Pérez", "profesor@mail.com", usar_gmail_real=False)
    estudiante = Estudiante("Juan González", "juan@mail.com")

    # Crear tarea y beneficio
    tarea1 = Tarea("TP Programación Orientada a Objetos")
    beneficio1 = Beneficio("Punto extra en parcial", 10)

    # Flujo completo
    print("\n--- Asignando tarea ---")
    profesor.asignarTarea(estudiante, tarea1)
    
    print("\n--- Verificando tareas del estudiante ---")
    estudiante.checkearTareas()

    print("\n--- Aprobando tarea ---")
    profesor.aprobarTarea(estudiante, "TP Programación Orientada a Objetos")
    
    print("\n--- Verificando tareas actualizadas ---")
    estudiante.checkearTareas()

    print("\n--- Agregando beneficio ---")
    estudiante.agregarBeneficio(beneficio1)
    profesor.verBeneficiosEstudiante(estudiante)

    print("\n--- Canjeando beneficio ---")
    estudiante.canjearBeneficio(beneficio1, profesor)
    print(f"💰 Monedas del estudiante: {estudiante.monedas}")


def ejemplo_modo_gmail_real():
    """
    Ejemplo 2: Modo Gmail real (enviando y leyendo emails reales)
    IMPORTANTE: Requiere configurar config.py con credenciales válidas
    """
    print("\n" + "="*80)
    print("EJEMPLO 2: MODO GMAIL REAL")
    print("="*80)
    print("\n⚠️  NOTA: Este ejemplo requiere configurar credenciales en config.py")
    print("Si no están configuradas, se ejecutará en modo simulación automáticamente.\n")
    
    # Crear profesor en modo Gmail real (usar_gmail_real=True)
    profesor = Profesor("Carlos Pérez", "profesor@mail.com", usar_gmail_real=True)
    estudiante = Estudiante("María López", "maria@mail.com")

    # Crear y asignar tarea
    tarea1 = Tarea("Investigación sobre APIs REST")
    
    print("\n--- Asignando tarea con email real ---")
    profesor.asignarTarea(estudiante, tarea1)
    
    # Aprobar tarea
    print("\n--- Aprobando tarea con email real ---")
    profesor.aprobarTarea(estudiante, "Investigación sobre APIs REST")
    
    # Agregar y canjear beneficio
    beneficio1 = Beneficio("Extensión de plazo 24hs", 15)
    estudiante.agregarBeneficio(beneficio1)
    
    print("\n--- Canjeando beneficio (genera email de notificación) ---")
    estudiante.canjearBeneficio(beneficio1, profesor)


def ejemplo_lectura_emails():
    """
    Ejemplo 3: Lectura de emails desde Gmail
    Demuestra cómo leer la bandeja de entrada
    """
    print("\n" + "="*80)
    print("EJEMPLO 3: LECTURA DE EMAILS")
    print("="*80)
    print("\n⚠️  NOTA: Este ejemplo requiere configurar credenciales en config.py\n")
    
    # Crear profesor con Gmail habilitado
    profesor = Profesor("Carlos Pérez", "profesor@mail.com", usar_gmail_real=True)
    
    # Leer últimos 5 emails
    print("\n--- Leyendo bandeja de entrada ---")
    profesor.leerEmails(cantidad=5)
    
    # Buscar notificaciones de canje
    print("\n--- Buscando notificaciones de canje ---")
    profesor.buscarNotificacionesCanje(cantidad=3)


def ejemplo_busqueda_emails():
    """
    Ejemplo 4: Búsqueda específica de emails
    """
    print("\n" + "="*80)
    print("EJEMPLO 4: BÚSQUEDA DE EMAILS POR ESTUDIANTE")
    print("="*80)
    print("\n⚠️  NOTA: Este ejemplo requiere configurar credenciales en config.py\n")
    
    profesor = Profesor("Carlos Pérez", "profesor@mail.com", usar_gmail_real=True)
    estudiante = Estudiante("Juan González", "juan@mail.com")
    
    # Buscar emails de un estudiante específico
    print(f"\n--- Buscando emails de {estudiante.nombre} ---")
    profesor.buscarEmailsDeEstudiante(estudiante, cantidad=3)


def menu_interactivo():
    """
    Menú interactivo para elegir qué ejemplo ejecutar
    """
    while True:
        print("\n" + "="*80)
        print("SISTEMA DE GESTIÓN DE TAREAS Y BENEFICIOS CON GMAIL")
        print("="*80)
        print("\n📋 Selecciona una opción:")
        print("\n1. Modo Simulación (sin Gmail real)")
        print("2. Modo Gmail Real (enviar emails)")
        print("3. Leer emails de Gmail")
        print("4. Buscar emails específicos")
        print("5. Ejecutar todos los ejemplos")
        print("0. Salir")
        print("\n" + "-"*80)
        
        opcion = input("\n👉 Ingresa el número de opción: ").strip()
        
        if opcion == "1":
            ejemplo_modo_simulacion()
        elif opcion == "2":
            ejemplo_modo_gmail_real()
        elif opcion == "3":
            ejemplo_lectura_emails()
        elif opcion == "4":
            ejemplo_busqueda_emails()
        elif opcion == "5":
            ejemplo_modo_simulacion()
            ejemplo_modo_gmail_real()
            ejemplo_lectura_emails()
            ejemplo_busqueda_emails()
        elif opcion == "0":
            print("\n👋 ¡Hasta luego!")
            break
        else:
            print("\n❌ Opción no válida. Intenta de nuevo.")
        
        input("\n\n[Presiona ENTER para continuar...]")


if __name__ == "__main__":
    # Puedes elegir entre el menú interactivo o ejecutar ejemplos específicos
    
    # Opción 1: Menú interactivo
    menu_interactivo()
    
    # Opción 2: Ejecutar ejemplos directamente (comenta el menú y descomenta estos)
    # ejemplo_modo_simulacion()
    # ejemplo_modo_gmail_real()
    # ejemplo_lectura_emails()
    # ejemplo_busqueda_emails()