"""
main.py - Orquestador de la Aplicación Lista de Tareas

Este archivo es el punto de entrada principal de la aplicación.
Responsable de inicializar las capas de servicio y UI, y lanzar el evento principal.

Arquitectura:
    1. Importar servicios (lógica de negocio)
    2. Importar UI (interfaz gráfica)
    3. Instanciar servicios
    4. Inyectar dependencia del servicio en la UI
    5. Iniciar el mainloop de Tkinter
"""

from servicios.tarea_servicio import TareaServicio
from ui.app_tkinter import AppTareas


def main():
    """
    Función principal que orquesta el arranque de la aplicación.
    
    Flujo:
        1. Crea la instancia del servicio (capa de lógica de negocio)
        2. Crea la instancia de la UI inyectando el servicio
        3. Inicia el bucle de eventos de Tkinter
    """
    # ==========================================================
    # 1. INICIALIZAR CAPA DE SERVICIOS
    # ==========================================================
    # El servicio gestiona el estado y la lógica de negocio
    tarea_servicio = TareaServicio()
    
    # ==========================================================
    # 2. INICIALIZAR CAPA DE UI CON INYECCIÓN DE DEPENDENCIA
    # ==========================================================
    # La UI recibe el servicio como parámetro (patrón de inyección de dependencia)
    # Esto permite separar claramente las responsabilidades
    app = AppTareas(tarea_servicio)
    
    # ==========================================================
    # 3. INICIAR BUCLE DE EVENTOS
    # ==========================================================
    # mainloop() mantiene la ventana abierta y escuchando eventos
    app.mainloop()


# ==========================================================
# PUNTO DE ENTRADA
# ==========================================================
if __name__ == "__main__":
    """
    Esta condición asegura que el código solo se ejecute cuando
    se ejecuta directamente este archivo, no cuando se importa.
    
    Es fundamental para:
        - PyInstaller (para generar el .exe correctamente)
        - Testing (para importar clases sin ejecutar la app)
    """
    main()