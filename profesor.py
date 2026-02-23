# profesor.py
from gmail_service import GmailService
import config

class Profesor:
    def __init__(self, nombre, email, usar_gmail_real=False):
        """
        Inicializa un profesor.
        
        Args:
            nombre (str): Nombre del profesor
            email (str): Email del profesor
            usar_gmail_real (bool): Si es True, usa Gmail real. Si es False, simula el envío.
        """
        self.nombre = nombre
        self.email = email
        self.usar_gmail_real = usar_gmail_real
        
        # Si se va a usar Gmail real, crear el servicio
        if self.usar_gmail_real:
            try:
                self.gmail_service = GmailService(config.GMAIL_USER, config.GMAIL_PASSWORD)
                print(f"✅ Servicio de Gmail inicializado para {self.nombre}")
            except Exception as e:
                print(f"⚠️ No se pudo inicializar Gmail: {e}")
                print("Se usará modo simulación")
                self.usar_gmail_real = False

    def asignarTarea(self, estudiante, tarea):
        estudiante.tareas.append(tarea)
        self.enviarMail(
            estudiante.email,
            "Nueva tarea asignada",
            f"Hola {estudiante.nombre},\n\n"
            f"Se te ha asignado una nueva tarea:\n"
            f"📝 {tarea.nombre}\n\n"
            f"Estado actual: {tarea.estado}\n\n"
            f"Saludos,\n{self.nombre}"
        )

    def aprobarTarea(self, estudiante, nombre_tarea):
        for tarea in estudiante.tareas:
            if tarea.nombre == nombre_tarea:
                tarea.estado = "Aprobada"
                self.enviarMail(
                    estudiante.email,
                    "¡Tarea aprobada! ✅",
                    f"Hola {estudiante.nombre},\n\n"
                    f"¡Felicitaciones! Tu tarea ha sido aprobada:\n"
                    f"✅ {tarea.nombre}\n\n"
                    f"Excelente trabajo.\n\n"
                    f"Saludos,\n{self.nombre}"
                )

    def notificarCanje(self, estudiante, beneficio):
        self.enviarMail(
            self.email,
            "Canje de beneficio - Notificación",
            f"Notificación automática:\n\n"
            f"El estudiante {estudiante.nombre} ({estudiante.email}) "
            f"ha canjeado el siguiente beneficio:\n\n"
            f"🎁 {beneficio.nombre}\n"
            f"💰 Valor: {beneficio.valor} monedas\n\n"
            f"Monedas totales del estudiante: {estudiante.monedas}"
        )

    def enviarMail(self, destino, asunto, mensaje):
        """
        Envía un email al destinatario.
        Si usar_gmail_real=True, envía un email real.
        Si usar_gmail_real=False, simula el envío.
        """
        if self.usar_gmail_real:
            # Envío real usando Gmail
            print("\n📧 Enviando email real vía Gmail...")
            self.gmail_service.enviar_email(destino, asunto, mensaje)
        else:
            # Simulación del envío
            print("\n--- 📧 Simulación de envío de mail ---")
            print(f"Para: {destino}")
            print(f"Asunto: {asunto}")
            print(f"Mensaje:\n{mensaje}")
            print("--- Fin del email ---")

    def leerEmails(self, cantidad=5):
        """
        Lee los últimos emails de la bandeja de entrada del profesor.
        Solo funciona si usar_gmail_real=True
        """
        if not self.usar_gmail_real:
            print("\n⚠️ La lectura de emails solo está disponible con Gmail real.")
            print("Inicializa el profesor con usar_gmail_real=True")
            return []
        
        print(f"\n📬 Leyendo últimos {cantidad} emails de {self.email}...")
        emails = self.gmail_service.leer_emails(cantidad=cantidad)
        
        # Mostrar los emails
        if emails:
            print(f"\n📨 Emails recibidos ({len(emails)}):")
            print("=" * 80)
            for i, email_data in enumerate(emails, 1):
                print(f"\n{i}. Asunto: {email_data['asunto']}")
                print(f"   De: {email_data['remitente']}")
                print(f"   Fecha: {email_data['fecha']}")
                print(f"   Contenido: {email_data['cuerpo'][:100]}...")
                print("-" * 80)
        else:
            print("\n📭 No se encontraron emails")
        
        return emails

    def buscarEmailsDeEstudiante(self, estudiante, cantidad=3):
        """
        Busca emails recibidos de un estudiante específico.
        """
        if not self.usar_gmail_real:
            print("\n⚠️ La búsqueda de emails solo está disponible con Gmail real.")
            return []
        
        print(f"\n🔍 Buscando emails de {estudiante.nombre} ({estudiante.email})...")
        emails = self.gmail_service.buscar_emails_de_remitente(estudiante.email, cantidad=cantidad)
        
        if emails:
            print(f"\n✉️ Se encontraron {len(emails)} emails de {estudiante.nombre}:")
            for i, email_data in enumerate(emails, 1):
                print(f"\n{i}. {email_data['asunto']}")
                print(f"   Fecha: {email_data['fecha']}")
        else:
            print(f"\n📭 No se encontraron emails de {estudiante.nombre}")
        
        return emails

    def buscarNotificacionesCanje(self, cantidad=5):
        """
        Busca emails con notificaciones de canje de beneficios.
        """
        if not self.usar_gmail_real:
            print("\n⚠️ La búsqueda de emails solo está disponible con Gmail real.")
            return []
        
        print("\n🔍 Buscando notificaciones de canje...")
        emails = self.gmail_service.buscar_emails_por_asunto("Canje de beneficio", cantidad=cantidad)
        
        if emails:
            print(f"\n🎁 Se encontraron {len(emails)} notificaciones de canje:")
            for i, email_data in enumerate(emails, 1):
                print(f"\n{i}. {email_data['asunto']}")
                print(f"   {email_data['cuerpo'][:150]}...")
        else:
            print("\n📭 No se encontraron notificaciones de canje")
        
        return emails

    def verBeneficiosEstudiante(self, estudiante):
        print(f"\n🎁 Beneficios de {estudiante.nombre}:")
        if estudiante.beneficios:
            for beneficio in estudiante.beneficios:
                print(f"  - {beneficio.nombre} (Valor: {beneficio.valor} monedas)")
        else:
            print("  No tiene beneficios disponibles")