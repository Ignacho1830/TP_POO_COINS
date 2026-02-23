# gmail_service.py
import smtplib
import imaplib
import email
from email.message import EmailMessage
from email.header import decode_header
import config

class GmailService:
    """
    Servicio para enviar y leer emails usando Gmail.
    Utiliza SMTP para envío e IMAP para lectura.
    """
    
    def __init__(self, email_usuario, password):
        """
        Inicializa el servicio de Gmail.
        
        Args:
            email_usuario (str): Dirección de email del usuario
            password (str): Contraseña de aplicación de Gmail
        """
        self.email_usuario = email_usuario
        self.password = password
        self.smtp_server = config.SMTP_SERVER
        self.smtp_port = config.SMTP_PORT
        self.imap_server = config.IMAP_SERVER
        self.imap_port = config.IMAP_PORT
    
    def enviar_email(self, destinatario, asunto, mensaje):
        """
        Envía un email usando SMTP de Gmail.
        
        Args:
            destinatario (str): Email del destinatario
            asunto (str): Asunto del email
            mensaje (str): Contenido del mensaje
            
        Returns:
            bool: True si se envió correctamente, False en caso contrario
        """
        try:
            # Crear el mensaje
            msg = EmailMessage()
            msg["From"] = self.email_usuario
            msg["To"] = destinatario
            msg["Subject"] = asunto
            msg.set_content(mensaje)
            
            # Conectar al servidor SMTP de Gmail y enviar
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as servidor:
                servidor.login(self.email_usuario, self.password)
                servidor.send_message(msg)
            
            print(f"\n✅ Email enviado exitosamente a {destinatario}")
            print(f"   Asunto: {asunto}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            print("\n❌ Error de autenticación. Verifica tu email y contraseña de aplicación.")
            return False
        except smtplib.SMTPException as e:
            print(f"\n❌ Error al enviar email: {e}")
            return False
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            return False
    
    def leer_emails(self, cantidad=5, carpeta="INBOX", filtro="ALL"):
        """
        Lee emails de la bandeja de entrada usando IMAP.
        
        Args:
            cantidad (int): Número de emails a leer (por defecto 5)
            carpeta (str): Carpeta a leer (por defecto "INBOX")
            filtro (str): Filtro de búsqueda IMAP (por defecto "ALL")
            
        Returns:
            list: Lista de diccionarios con información de los emails
        """
        emails_leidos = []
        
        try:
            # Conectar al servidor IMAP de Gmail
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self.email_usuario, self.password)
            
            # Seleccionar la carpeta
            mail.select(carpeta)
            
            # Buscar emails según el filtro
            status, mensajes = mail.search(None, filtro)
            
            # Obtener los IDs de los emails
            email_ids = mensajes[0].split()
            
            # Leer los últimos N emails
            for email_id in email_ids[-cantidad:]:
                # Obtener el email
                status, datos = mail.fetch(email_id, "(RFC822)")
                
                # Parsear el email
                email_mensaje = email.message_from_bytes(datos[0][1])
                
                # Decodificar el asunto
                asunto = self._decodificar_asunto(email_mensaje["Subject"])
                
                # Obtener el remitente
                remitente = email_mensaje.get("From")
                
                # Obtener la fecha
                fecha = email_mensaje.get("Date")
                
                # Obtener el cuerpo del mensaje
                cuerpo = self._obtener_cuerpo(email_mensaje)
                
                # Agregar a la lista
                emails_leidos.append({
                    "id": email_id.decode(),
                    "asunto": asunto,
                    "remitente": remitente,
                    "fecha": fecha,
                    "cuerpo": cuerpo[:200] + "..." if len(cuerpo) > 200 else cuerpo
                })
            
            # Cerrar la conexión
            mail.close()
            mail.logout()
            
            print(f"\n✅ Se leyeron {len(emails_leidos)} emails correctamente")
            return emails_leidos
            
        except imaplib.IMAP4.error as e:
            print(f"\n❌ Error de IMAP: {e}")
            return []
        except Exception as e:
            print(f"\n❌ Error al leer emails: {e}")
            return []
    
    def _decodificar_asunto(self, asunto):
        """
        Decodifica el asunto del email si está codificado.
        
        Args:
            asunto (str): Asunto codificado
            
        Returns:
            str: Asunto decodificado
        """
        if asunto is None:
            return "Sin asunto"
        
        asunto_decodificado = ""
        for parte, encoding in decode_header(asunto):
            if isinstance(parte, bytes):
                asunto_decodificado += parte.decode(encoding or "utf-8")
            else:
                asunto_decodificado += parte
        
        return asunto_decodificado
    
    def _obtener_cuerpo(self, email_mensaje):
        """
        Obtiene el cuerpo del email.
        
        Args:
            email_mensaje: Objeto email parseado
            
        Returns:
            str: Cuerpo del mensaje
        """
        cuerpo = ""
        
        if email_mensaje.is_multipart():
            # Si el email es multipart, iterar sobre las partes
            for parte in email_mensaje.walk():
                content_type = parte.get_content_type()
                
                if content_type == "text/plain":
                    try:
                        cuerpo = parte.get_payload(decode=True).decode()
                        break
                    except:
                        pass
        else:
            # Si no es multipart, obtener el payload directamente
            try:
                cuerpo = email_mensaje.get_payload(decode=True).decode()
            except:
                cuerpo = "No se pudo decodificar el mensaje"
        
        return cuerpo
    
    def buscar_emails_por_asunto(self, palabra_clave, cantidad=5):
        """
        Busca emails que contengan una palabra clave en el asunto.
        
        Args:
            palabra_clave (str): Palabra a buscar en el asunto
            cantidad (int): Número máximo de emails a retornar
            
        Returns:
            list: Lista de emails que coinciden con la búsqueda
        """
        filtro = f'SUBJECT "{palabra_clave}"'
        return self.leer_emails(cantidad=cantidad, filtro=filtro)
    
    def buscar_emails_de_remitente(self, remitente, cantidad=5):
        """
        Busca emails de un remitente específico.
        
        Args:
            remitente (str): Email del remitente
            cantidad (int): Número máximo de emails a retornar
            
        Returns:
            list: Lista de emails del remitente
        """
        filtro = f'FROM "{remitente}"'
        return self.leer_emails(cantidad=cantidad, filtro=filtro)
    
    def leer_emails_no_leidos(self, cantidad=5):
        """
        Lee solo los emails no leídos.
        
        Args:
            cantidad (int): Número máximo de emails a retornar
            
        Returns:
            list: Lista de emails no leídos
        """
        return self.leer_emails(cantidad=cantidad, filtro="UNSEEN")


# Función de ayuda para crear una instancia del servicio
def crear_servicio_gmail():
    """
    Crea y retorna una instancia del servicio de Gmail
    usando las credenciales del archivo config.py
    
    Returns:
        GmailService: Instancia del servicio de Gmail
    """
    return GmailService(config.GMAIL_USER, config.GMAIL_PASSWORD)