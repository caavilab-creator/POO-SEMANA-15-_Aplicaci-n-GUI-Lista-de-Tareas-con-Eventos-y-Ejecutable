class Tarea:
    """
    Clase que representa una tarea individual en la lista.
    Gestiona los datos básicos: identificador, descripción y estado.
    """
    
    def __init__(self, id: int, descripcion: str, estado_completado: bool = False):
        """
        Inicializa una nueva tarea.
        
        Args:
            id (int): Identificador único de la tarea.
            descripcion (str): Descripción o texto de la tarea.
            estado_completado (bool): Estado de la tarea (False = pendiente, True = completada).
        """
        # Usamos los setters para aplicar validaciones desde la creación
        self.id = id
        self.descripcion = descripcion
        self.estado_completado = estado_completado
    
    @property
    def id(self) -> int:
        """Obtiene el identificador de la tarea."""
        return self._id
    
    @id.setter
    def id(self, value: int):
        """
        Establece el identificador de la tarea.
        
        Args:
            value (int): El nuevo identificador.
            
        Raises:
            ValueError: Si el ID no es un número entero válido.
        """
        if not isinstance(value, int) or value < 0:
            raise ValueError("El ID debe ser un número entero no negativo.")
        self._id = value
    
    @property
    def descripcion(self) -> str:
        """Obtiene la descripción de la tarea."""
        return self._descripcion
    
    @descripcion.setter
    def descripcion(self, value: str):
        """
        Establece la descripción de la tarea con validación.
        
        Args:
            value (str): La nueva descripción.
            
        Raises:
            ValueError: Si la descripción está vacía o es None.
        """
        if not value or not value.strip():
            raise ValueError("La descripción de la tarea no puede estar vacía.")
        self._descripcion = value.strip()
    
    @property
    def estado_completado(self) -> bool:
        """Obtiene el estado de completado de la tarea."""
        return self._estado_completado
    
    @estado_completado.setter
    def estado_completado(self, value: bool):
        """
        Establece el estado de completado de la tarea.
        
        Args:
            value (bool): True si está completada, False si está pendiente.
            
        Raises:
            ValueError: Si el valor no es booleano.
        """
        if not isinstance(value, bool):
            raise ValueError("El estado debe ser un valor booleano (True/False).")
        self._estado_completado = value
    
    def marcar_completada(self):
        """Cambia el estado de la tarea a completada."""
        self.estado_completado = True
    
    def marcar_pendiente(self):
        """Cambia el estado de la tarea a pendiente."""
        self.estado_completado = False
    
    def __str__(self) -> str:
        """
        Representación en string de la tarea.
        
        Returns:
            str: Descripción formateada con el estado.
        """
        estado = "✓ Completada" if self.estado_completado else "○ Pendiente"
        return f"Tarea #{self.id}: {self.descripcion} [{estado}]"