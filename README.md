# PayloadHub

**PayloadHub** es una herramienta interactiva de línea de comandos (CLI) diseñada para generar payloads personalizados para pruebas de penetración. Es ideal para pentesters y entusiastas de la seguridad que buscan automatizar la generación de payloads y aplicar técnicas de evasión (bypasses) para pruebas de seguridad en aplicaciones web.

## Características

- **Tipos de Ataques Soportados**:
  - SQL Injection (SQLi)
  - Cross-Site Scripting (XSS)
  - Local File Inclusion (LFI)
  - Remote Code Execution (RCE)
  - XML External Entity (XXE)

- **Bypasses Disponibles**:
  - Técnicas de evasión como codificación de URL, doble codificación, eliminación de espacios, entre otros.
  - Bypasses específicos para cada tipo de ataque.

- **Modo Simulación**:
  - Permite probar los payloads generados en un entorno controlado para entender su comportamiento.

- **Análisis de Payloads**:
  - Detecta patrones comunes en los payloads para identificar posibles problemas o vulnerabilidades.

- **Configuraciones Guardables**:
  - Guarda y carga configuraciones de ataques en archivos JSON para reutilizarlas fácilmente.

## Requisitos

- Python 3.8 o superior
- Librerías requeridas (instalables con `pip`):
  - `typer`
  - `rich`

## Instalación

1. Clona este repositorio:
   ```bash
   git clone [https://github.com/Jbloca/Payload-Forge/edit.git]
   cd PayloadForge
