# 🔥 PayloadForge – Generador de Payloads Ofensivos para Pentesters

**PayloadForge** es una herramienta interactiva de línea de comandos (CLI) diseñada para generar payloads personalizados orientados a pruebas de penetración.  
Ideal para pentesters y entusiastas de la ciberseguridad que desean automatizar la creación de payloads ofensivos y aplicar técnicas de evasión (bypasses) para pruebas en aplicaciones web.

---

## 🚀 Características

- 🎯 **Tipos de Ataques Soportados**:
  - SQL Injection (SQLi)
  - Cross-Site Scripting (XSS)
  - Local File Inclusion (LFI)
  - Remote Code Execution (RCE)
  - XML External Entity (XXE)

- 🛡️ **Bypasses Incluidos**:
  - Codificación de URL y Unicode
  - Doble codificación
  - Eliminación de espacios y comentarios
  - Bypasses específicos por tipo de ataque

- 🧪 **Modo Simulación**:
  - Ejecuta una simulación controlada del payload para visualizar cómo se comportaría en un entorno real.

- 🔍 **Análisis de Payloads**:
  - Detecta patrones comunes y valida si el payload es potencialmente funcional o peligroso.

- 💾 **Configuraciones Reutilizables**:
  - Guarda tus ataques como archivos `.json` para repetirlos o modificarlos más adelante.

---

## ⚙️ Requisitos

- Python 3.8 o superior
- Librerías requeridas (instalables con `pip`):
  - `typer`
  - `rich`

## ⚙️ Instalación
    git clone https://github.com/Jbloca/Payload-Forge.git
    cd PayloadForge
    
## Coamdno de Uso
  * `./payloadForge.py generate` #Genera un payload de forma interactiva.
  * `./payloadForge.py generate --analyze --simulate` #Generar, analizar y simular un payload.
  * `./payloadForge.py generate --save-as ataqueSQL.json` #Guarda tu configuracion actual.
  *`./payloadForge.py generate --load-from ataqueSQL.json` #Cargar una configuracion guardada previamente.
  * `./payloadForge.py list-payloads` #Listar todos los payloads disponibles.
  * `./payloadForge.py list-bypasses` #Listar todos los bypasses disponibles.

## 📸 Captura de Pantalla
  
## Contribuciones
  ¡Pull requests y sugerencias son bienvenidos!
  Puedes proponer nuevos payloads, bypasses o tipos de ataque.

## 👨‍💻 Autor
  Desarrollado por Jorge Balarezo Cardenas
🔗 LinkedIn • 🧑‍💻 Hacker Ético Junior • 🇵🇪 Perú

## 📄 Licencia
Este proyecto está bajo la licencia MIT.

