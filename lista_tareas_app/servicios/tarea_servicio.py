from modelos.tarea import Tarea
from typing import List, Optional

class TareaServicio:
    """
    Capa de Servicios: Gestiona la lógica de negocio y el estado de las tareas.
    Actúa como intermediario entre la UI y los Modelos.
    """
    
    def __init__(self):
        """
        Inicializa el servicio con una base de datos en memoria.
        """
        # Base de datos en memoria (lista de objetos Tarea)
        self._tareas: List[Tarea] = []
        self._contador_id: int = 0  # Para generar IDs únicos automáticamente
    
    def agregar_tarea(self, descripcion: str) -> Tarea:
        """
        Agrega una nueva tarea a la lista.
        
        Args:
            descripcion (str): Descripción de la nueva tarea.
            
        Returns:
            Tarea: El objeto tarea creado.
            
        Raises:
            ValueError: Si la descripción está vacía.
        """
        # Validación de regla de negocio: no permitir tareas vacías
        if not descripcion or not descripcion.strip():
            raise ValueError("La descripción de la tarea no puede estar vacía.")
        
        # Generar ID único automático
        self._contador_id += 1
        
        # Crear el objeto Tarea (el modelo valida los datos internamente)
        nueva_tarea = Tarea(id=self._contador_id, descripcion=descripcion, estado_completado=False)
        
        # Agregar a la "base de datos" en memoria
        self._tareas.append(nueva_tarea)
        
        return nueva_tarea
    
    def obtener_todos(self) -> List[Tarea]:
        """
        Obtiene la lista completa de tareas registradas.
        
        Returns:
            List[Tarea]: Lista de todos los objetos Tarea.
        """
        return self._tareas
    
    def marcar_completada(self, id_tarea: int) -> None:
        """
        Cambia el estado de una tarea a completada.
        
        Args:
            id_tarea (int): El identificador de la tarea a actualizar.
            
        Raises:
            ValueError: Si no se encuentra la tarea con ese ID.
        """
        tarea = self._obtener_por_id(id_tarea)
        
        if tarea:
            tarea.marcar_completada()
        else:
            raise ValueError(f"No se encontró la tarea con ID {id_tarea}.")
    
    def marcar_pendiente(self, id_tarea: int) -> None:
        """
        Cambia el estado de una tarea a pendiente.
        
        Args:
            id_tarea (int): El identificador de la tarea a actualizar.
            
        Raises:
            ValueError: Si no se encuentra la tarea con ese ID.
        """
        tarea = self._obtener_por_id(id_tarea)
        
        if tarea:
            tarea.marcar_pendiente()
        else:
            raise ValueError(f"No se encontró la tarea con ID {id_tarea}.")
    
    def eliminar_tarea(self, id_tarea: int) -> None:
        """
        Elimina una tarea de la lista.
        
        Args:
            id_tarea (int): El identificador de la tarea a eliminar.
            
        Raises:
            ValueError: Si la tarea no existe.
        """
        tarea = self._obtener_por_id(id_tarea)
        
        if tarea:
            self._tareas.remove(tarea)
        else:
            raise ValueError("La tarea no existe o ya fue eliminada.")
    
    def _obtener_por_id(self, id_tarea: int) -> Optional[Tarea]:
        """
        Método auxiliar privado para buscar una tarea por su ID.
        
        Args:
            id_tarea (int): El identificador a buscar.
            
        Returns:
            Optional[Tarea]: El objeto Tarea si se encuentra, None en caso contrario.
        """
        for tarea in self._tareas:
            if tarea.id == id_tarea:
                return tarea
        return None
    
    def obtener_pendientes(self) -> List[Tarea]:
        """
        Obtiene solo las tareas que están pendientes.
        
        Returns:
            List[Tarea]: Lista de tareas con estado_completado = False.
        """
        return [t for t in self._tareas if not t.estado_completado]
    
    def obtener_completadas(self) -> List[Tarea]:
        """
        Obtiene solo las tareas que están completadas.
        
        Returns:
            List[Tarea]: Lista de tareas con estado_completado = True.
        """
        return [t for t in self._tareas if t.estado_completado]