#!/usr/bin/env python3

import typer
from rich import print
from rich.prompt import Prompt, Confirm
import random
import urllib.parse
import json
import base64
import os
import requests
import re
from rich.console import Console
from utils import basic_obfuscation, lfi_bypass, rce_bypass, sqli_comment_bypass, unicode_bypass, xxe_bypass

def print_logo():
    """Imprime el logo del proyecto PayloadHub con colores usando rich."""
    console = Console()

    # Definir las líneas del logo en rojo
    red_lines = [
        "██████╗  █████╗ ██╗   ██╗██╗      ██████╗  █████╗ ██████╗",
        "██╔══██╗██╔══██╗╚██╗ ██╔╝██║     ██╔═══██╗██╔══██╗██╔══██╗",
        "██████╔╝███████║ ╚████╔╝ ██║     ██║   ██║███████║██║  ██║",
        "██╔═══╝ ██╔══██║  ╚██╔╝  ██║     ██║   ██║██╔══██║██║  ██║",
        "██║     ██║  ██║   ██║   ███████╗╚██████╔╝██║  ██║██████╔╝",
        "╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝"
    ]

    # Definir las líneas del logo en azul
    blue_lines = [
        "███████╗ ██████╗ ██████╗  ██████╗ ███████╗",
        "██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝",
        "█████╗  ██║   ██║██████╔╝██║  ███╗█████╗",
        "██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝",
        "██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗",
        "╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝"
    ]

    # Imprimir las líneas del logo alternando colores
    for red, blue in zip(red_lines, blue_lines):
        console.print(f"[bold red]{red}[/bold red]   [bold blue]{blue}[/bold blue]")
app = typer.Typer()
# Cargar la base de datos desde el archivo JSON
try:
    with open("payloads_db.json", "r") as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"[red]Error al cargar el archivo JSON: {e}[/red]")
    exit(1)

# Validar que las claves necesarias existan en el archivo JSON
required_keys = ["SQLI", "XSS", "LFI", "RCE", "XXE", "BYPASSES"]
for key in required_keys:
    if key not in data:
        print(f"[red]Error: Falta la clave '{key}' en el archivo JSON.[/red]")
        exit(1)

# Convertir las funciones de bypass de cadenas a funciones ejecutables
BYPASSES = data["BYPASSES"]
for attack_type, bypasses in BYPASSES.items():
    for bypass_name, bypass_function in bypasses.items():
        try:
            BYPASSES[attack_type][bypass_name] = eval(bypass_function)
        except Exception as e:
            print(f"[red]Error al cargar el bypass '{bypass_name}' para '{attack_type}': {e}[/red]")
            exit(1)

payloads = {
    "SQLI": data["SQLI"],
    "XSS": data["XSS"],
    "LFI": data["LFI"],
    "RCE": data["RCE"],
    "XXE": data["XXE"]
}
BYPASSES = data["BYPASSES"]

# Diccionario de funciones de bypass (definir en utils.py)
BYPASS_FUNCTIONS = {
    "SQLI": {
        "basic_obfuscation": basic_obfuscation,
        "unicode_bypass": unicode_bypass,
        "sqli_comment_bypass": sqli_comment_bypass  # Añadido el bypass para comentarios en SQLi
    },
    "XSS": {
        "basic_obfuscation": basic_obfuscation,
        "unicode_bypass": unicode_bypass
    },
    "LFI": {
        "basic_obfuscation": basic_obfuscation,
        "lfi_bypass": lfi_bypass  # Añadido bypass LFI
    },
    "RCE": {
        "rce_bypass": rce_bypass  # Añadido bypass RCE
    },
    "XXE": {
        "xxe_bypass": xxe_bypass  # Añadido bypass XXE
    }
}

def select_attack_type():
    """Permite al usuario seleccionar el tipo de ataque."""
    attack_types = list(payloads.keys())
    print("[bold]SELECCIONA EL TIPO DE ATAQUE:[/bold]")
    for i, attack_type in enumerate(attack_types):
        print(f"{i + 1}. {attack_type}")
    choice = Prompt.ask("Opción", choices=[str(i) for i in range(1, len(attack_types) + 1)])
    return attack_types[int(choice) - 1]

def select_payload_type(attack_type):
    """Permite al usuario seleccionar el tipo de payload."""
    payload_types = list(payloads[attack_type].keys())
    print(f"[bold]SELECCIONA EL TIPO DE PAYLOAD PARA {attack_type}:[/bold]")
    for i, payload_type in enumerate(payload_types):
        print(f"{i + 1}. {payload_type}")
    choice = Prompt.ask("Opción", choices=[str(i) for i in range(1, len(payload_types) + 1)])
    return payload_types[int(choice) - 1]

def select_bypasses(attack_type):
    """Permite al usuario seleccionar los bypasses."""
    bypass_names = list(BYPASSES.get(attack_type, {}).keys())
    selected_bypasses = []
    print(f"[bold]Selecciona los bypasses para {attack_type} (deja en blanco para ninguno):[/bold]")
    for i, bypass_name in enumerate(bypass_names):
        if Confirm.ask(f"Aplicar {bypass_name}?"):
            selected_bypasses.append(bypass_name)
    return selected_bypasses

def save_config(config, filename):
    """Guarda la configuración en un archivo JSON."""
    with open(filename, "w") as f:
        json.dump(config, f)
    print(f"[green]Configuración guardada en {filename}[/green]")

def load_config(filename):
    """Carga la configuración desde un archivo JSON."""
    if not os.path.exists(filename):
        print(f"[yellow]Archivo de configuración '{filename}' no encontrado.[/yellow]")
        return None
    with open(filename, "r") as f:
        config = json.load(f)
    print(f"[green]Configuración cargada desde {filename}[/green]")
    return config

def analyze_payload(payload, attack_type):
    """Realiza un análisis avanzado dependiendo del tipo de ataque."""
    analysis_rules = {
        "SQLI": [r"(UNION|SELECT|INSERT|UPDATE|DELETE|DROP|--)", r"OR\s+1=1", r"' OR '1'='1"],
        "XSS": [r"<script>", r"<img", r"<iframe", r"<svg", r"javascript:"],
        "RCE": [r";", r"&&", r"\|\|", r"wget", r"curl", r"bash", r"sh", r"python", r"perl", r"nc", r"telnet"],
        "LFI": [r"\.\./", r"%2e%2e", r"\0", r"%00", r"/etc/passwd", r"/proc/self/environ", r"/var/log"],
        "XXE": [r"<!ENTITY.*SYSTEM", r"DOCTYPE.*SYSTEM"]
    }

    if attack_type not in analysis_rules:
        return "[blue]Análisis no disponible para este tipo de ataque.[/blue]"

    for pattern in analysis_rules[attack_type]:
        if re.search(pattern, payload, re.IGNORECASE):
            return f"[yellow]Posible payload {attack_type} detectado: {pattern}.[/yellow]"

    return f"[green]Payload {attack_type} parece válido.[/green]"

def select_attack_type():
    """Permite al usuario seleccionar el tipo de ataque."""
    attack_types = list(payloads.keys())
    if not attack_types:
        print("[red]Error: No hay tipos de ataque disponibles.[/red]")
        exit(1)

    print("[bold]SELECCIONA EL TIPO DE ATAQUE:[/bold]")
    for i, attack_type in enumerate(attack_types):
        print(f"{i + 1}. {attack_type}")
    choice = Prompt.ask("Opción", choices=[str(i) for i in range(1, len(attack_types) + 1)])
    return attack_types[int(choice) - 1]

def select_payload_type(attack_type):
    """Permite al usuario seleccionar el tipo de payload."""
    payload_types = list(payloads[attack_type].keys())
    if not payload_types:
        print(f"[red]Error: No hay payloads disponibles para el ataque '{attack_type}'.[/red]")
        exit(1)

    print(f"[bold]SELECCIONA EL TIPO DE PAYLOAD PARA {attack_type}:[/bold]")
    for i, payload_type in enumerate(payload_types):
        print(f"{i + 1}. {payload_type}")
    choice = Prompt.ask("Opción", choices=[str(i) for i in range(1, len(payload_types) + 1)])
    return payload_types[int(choice) - 1]

def select_bypasses(attack_type):
    """Permite al usuario seleccionar los bypasses."""
    bypass_names = list(BYPASSES.get(attack_type, {}).keys())
    if not bypass_names:
        print(f"[yellow]No hay bypasses disponibles para el ataque '{attack_type}'.[/yellow]")
        return []

    selected_bypasses = []
    print(f"[bold]Selecciona los bypasses para {attack_type} (deja en blanco para ninguno):[/bold]")
    for bypass_name in bypass_names:
        if Confirm.ask(f"Aplicar {bypass_name}?"):
            selected_bypasses.append(bypass_name)
    return selected_bypasses

def validate_payload(payload):
    """Verifica que el payload no esté vacío o inválido."""
    if not payload or len(payload.strip()) == 0:
        raise ValueError("El payload no puede estar vacío o ser inválido.")
    return payload
        
@app.command()       
def list_payloads():
    """Lista todos los payloads disponibles."""
    print("[bold]Payloads disponibles:[/bold]")
    for attack_type, payload_types in payloads.items():
        print(f"[bold]{attack_type}:[/bold]")
        for payload_type, examples in payload_types.items():
            print(f"  {payload_type}: {', '.join(examples[:3])}...")
@app.command()         
def list_bypasses():
    """Lista todos los bypasses disponibles."""
    print("[bold]Bypasses disponibles:[/bold]")
    for attack_type, bypass_list in BYPASSES.items():
        print(f"[bold]{attack_type}:[/bold]")
        for bypass_name in bypass_list.keys():
            print(f"  - {bypass_name}")
            
@app.command()
def generate(
    save_as: str = typer.Option(None, help="Nombre del archivo para guardar la configuración."),
    load_from: str = typer.Option(None, help="Nombre del archivo para cargar la configuración."),
    analyze: bool = typer.Option(False, help="Analiza el payload generado."),
    simulate: bool = typer.Option(False, help="Ejecuta el payload en modo simulación.")
):
    """Genera un payload personalizado y permite guardar/cargar configuraciones."""
    config = None

    if load_from:
        config = load_config(load_from)
        if not config:
            return

    if not config:
        attack_type = select_attack_type()
        payload_type = select_payload_type(attack_type)
        selected_bypasses = select_bypasses(attack_type)
    else:
        attack_type = config["attack_type"]
        payload_type = config["payload_type"]
        selected_bypasses = config["bypasses"]

    try:
        payload = random.choice(payloads[attack_type][payload_type])
    except KeyError:
        print(f"[red]Error: No se encontró el tipo de payload '{payload_type}' para el ataque '{attack_type}'.[/red]")
        return

    for bypass_name in selected_bypasses:
        try:
            bypass_function = BYPASSES[attack_type][bypass_name]
            payload = bypass_function(payload)
        except KeyError:
            print(f"[red]Error: No se encontró el bypass '{bypass_name}' para el ataque '{attack_type}'.[/red]")
            continue

    print(f"[green]Payload generado:[/green] {payload}")

    if analyze:
        analysis_result = analyze_payload(payload, attack_type)
        print(analysis_result)

    if simulate:
        simulate_payload(payload, attack_type)

    if save_as:
        save_config({
            "attack_type": attack_type,
            "payload_type": payload_type,
            "bypasses": selected_bypasses
        }, save_as)

def simulate_payload(payload, attack_type):
    """Simula la ejecución del payload en un entorno controlado."""
    print(f"[bold blue]Simulando el payload para el ataque '{attack_type}':[/bold blue]")

    if attack_type == "SQLI":
        print(f"[yellow]Simulación SQLi:[/yellow] Ejecutando consulta: SELECT * FROM users WHERE username = '{payload}'")
    elif attack_type == "XSS":
        print(f"[yellow]Simulación XSS:[/yellow] Renderizando en un navegador: {payload}")
    elif attack_type == "LFI":
        print(f"[yellow]Simulación LFI:[/yellow] Intentando acceder al archivo: {payload}")
    elif attack_type == "RCE":
        print(f"[yellow]Simulación RCE:[/yellow] Ejecutando comando: {payload}")
    elif attack_type == "XXE":
        print(f"[yellow]Simulación XXE:[/yellow] Procesando entidad XML: {payload}")
    else:
        print(f"[red]Simulación no disponible para el tipo de ataque '{attack_type}'.[/red]")

    print("[green]Simulación completada.[/green]")

if __name__ == "__main__":
    print_logo()
    app()
