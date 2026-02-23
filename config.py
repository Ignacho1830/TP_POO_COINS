# config.py
# Configuración de credenciales para Gmail

# IMPORTANTE: Para usar Gmail con SMTP/IMAP necesitas:
# 1. Activar la verificación en 2 pasos en tu cuenta Google
# 2. Generar una "Contraseña de aplicación" en:
#    https://myaccount.google.com/apppasswords
# 3. Reemplazar los valores a continuación con tus credenciales reales

# Credenciales del profesor
GMAIL_USER = "iblazquez@escuelasproa.edu.ar"  # Reemplazar con tu email
GMAIL_PASSWORD = "vazv gtpc odsp upse"  # Reemplazar con tu contraseña de aplicación (16 caracteres)

# Configuración de servidores Gmail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

# Configuración adicional
MAX_EMAILS_TO_READ = 10  # Cantidad máxima de emails a leer