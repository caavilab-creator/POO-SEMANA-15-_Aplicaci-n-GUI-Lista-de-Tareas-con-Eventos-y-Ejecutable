import tkinter as tk
from tkinter import ttk, messagebox
from modelos.tarea import Tarea

class AppTareas(tk.Tk):
    """
    Capa UI: Interfaz gráfica de la aplicación Lista de Tareas.
    Gestiona la presentación y captura eventos de teclado/ratón.
    """
    
    def __init__(self, servicio):
        """
        Inicializa la ventana principal de la aplicación.
        
        Args:
            servicio: Instancia de TareaServicio para la lógica de negocio.
        """
        super().__init__()
        self.servicio = servicio
        self._id_tarea_seleccionada = None
        self.title("Lista de Tareas - Sistema CRUD")
        self.geometry("820x520")
        self.configure(bg="#f4f4f9")
        
        self._configurar_interfaz()
        self._aplicar_estilos()
        self._registrar_eventos()
        self._actualizar_tabla()
    
    # ==========================================================
    # ESTILOS
    # ==========================================================
    def _aplicar_estilos(self):
        """Configura los estilos visuales de los componentes Tkinter."""
        style = ttk.Style(self)
        style.theme_use("clam")
        
        # Estilo para el Treeview (tabla de tareas)
        style.configure(
            "Treeview",
            background="#ffffff",
            foreground="#333333",
            rowheight=25
        )
        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold"),
            background="#e0e0e0"
        )
        style.map("Treeview", background=[("selected", "#4a90e2")])
        
        # Estilos para botones con colores distintivos
        style.configure(
            "Agregar.TButton",
            font=("Arial", 10, "bold"),
            background="#4CAF50",
            foreground="white",
            padding=5
        )
        style.configure(
            "Completar.TButton",
            font=("Arial", 10, "bold"),
            background="#2196F3",
            foreground="white",
            padding=5
        )
        style.configure(
            "Eliminar.TButton",
            font=("Arial", 10, "bold"),
            background="#f44336",
            foreground="white",
            padding=5
        )
        style.configure(
            "Limpiar.TButton",
            font=("Arial", 10, "bold"),
            background="#9e9e9e",
            foreground="white",
            padding=5
        )
    
    # ==========================================================
    # INTERFAZ
    # ==========================================================
    def _configurar_interfaz(self):
        """Crea y organiza todos los componentes visuales de la ventana."""
        
        # Frame superior para formulario de entrada
        frame_form = tk.Frame(self, bg="#f4f4f9")
        frame_form.pack(pady=5, padx=20, fill="x")
        
        tk.Label(
            frame_form, text="Descripción:", bg="#f4f4f9", font=("Arial", 10)
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.ent_descripcion = ttk.Entry(frame_form, width=60)
        self.ent_descripcion.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Mensaje guía de eventos (feedback visual)
        self.lbl_estado = tk.Label(
            self,
            text="Listo. Use Enter para añadir, Doble Clic para completar y Delete para eliminar.",
            bg="#f4f4f9",
            fg="#1d3b6b",
            font=("Arial", 10, "italic"),
            anchor="w"
        )
        self.lbl_estado.pack(padx=20, fill="x")
        
        # Frame para botones de acción
        frame_btns = tk.Frame(self, bg="#f4f4f9")
        frame_btns.pack(pady=5, padx=20, fill="x")
        
        self.btn_agregar = ttk.Button(
            frame_btns, text="Añadir Tarea", style="Agregar.TButton", command=self._agregar_tarea
        )
        self.btn_agregar.pack(side=tk.LEFT, padx=5)
        
        self.btn_completar = ttk.Button(
            frame_btns, text="Marcar Completada", style="Completar.TButton", command=self._marcar_completada
        )
        self.btn_completar.pack(side=tk.LEFT, padx=5)
        
        self.btn_eliminar = ttk.Button(
            frame_btns, text="Eliminar", style="Eliminar.TButton", command=self._eliminar_tarea
        )
        self.btn_eliminar.pack(side=tk.LEFT, padx=5)
        
        self.btn_limpiar = ttk.Button(
            frame_btns, text="Limpiar", style="Limpiar.TButton", command=self._limpiar_campos
        )
        self.btn_limpiar.pack(side=tk.RIGHT, padx=5)
        
        # Frame para la tabla de tareas (Treeview)
        frame_tabla = tk.Frame(self, bg="#f4f4f9")
        frame_tabla.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=("id", "descripcion", "estado"),
            show="headings"
        )
        
        self.tabla.heading("id", text="ID")
        self.tabla.heading("descripcion", text="Descripción")
        self.tabla.heading("estado", text="Estado")
        
        self.tabla.column("id", width=50, anchor="center")
        self.tabla.column("descripcion", width=500)
        self.tabla.column("estado", width=150, anchor="center")
        
        self.tabla.pack(fill="both", expand=True)
    
    # ==========================================================
    # REGISTRO DE EVENTOS
    # ==========================================================
    def _registrar_eventos(self):
        """
        Configura los manejadores de eventos usando .bind()
        Requisito obligatorio de la tarea.
        """
        # Selección normal de fila
        self.tabla.bind("<<TreeviewSelect>>", self._seleccionar_fila)
        
        # ✅ ENTER en el campo de entrada -> agregar tarea (Requisito Obligatorio)
        self.ent_descripcion.bind("<Return>", self._evento_enter_agregar)
        
        # ✅ DOBLE CLIC en la tabla -> marcar completada (Requisito Opcional/Extra)
        self.tabla.bind("<Double-1>", self._evento_doble_click_completar)
        
        # DELETE -> eliminar seleccionado desde tabla
        self.tabla.bind("<Delete>", self._evento_delete_eliminar)
        
        # ESCAPE -> limpiar formulario
        self.bind("<Escape>", self._evento_escape_limpiar)
        
        # Confirmar cierre de ventana
        self.protocol("WM_DELETE_WINDOW", self._cerrar_aplicacion)
    
    # ==========================================================
    # MANEJADORES DE EVENTOS
    # ==========================================================
    def _evento_enter_agregar(self, event):
        """
        Manejador para evento de teclado Enter.
        Permite agregar tarea sin hacer clic en el botón.
        """
        self.lbl_estado.config(text="Evento Enter detectado: se intentará añadir la tarea.")
        self._agregar_tarea()
    
    def _evento_doble_click_completar(self, event):
        """
        Manejador para evento de ratón Doble Clic.
        Permite marcar tarea como completada directamente desde la tabla.
        """
        self.lbl_estado.config(text="Evento Doble Clic detectado: marcando tarea como completada.")
        self._marcar_completada()
    
    def _evento_delete_eliminar(self, event):
        """
        Manejador para evento de teclado Delete.
        Permite eliminar tarea seleccionada sin usar el botón.
        """
        self.lbl_estado.config(text="Evento Delete detectado: se intentará eliminar la tarea seleccionada.")
        self._eliminar_tarea()
    
    def _evento_escape_limpiar(self, event):
        """
        Manejador para evento de teclado Escape.
        Limpia el formulario rápidamente.
        """
        self.lbl_estado.config(text="Evento Escape detectado: formulario limpiado.")
        self._limpiar_campos()
    
    # ==========================================================
    # MÉTODOS PRINCIPALES DEL CRUD
    # ==========================================================
    def _agregar_tarea(self):
        """Agrega una nueva tarea usando la capa de servicios."""
        descripcion = self.ent_descripcion.get().strip()
        
        try:
            # El servicio valida y crea la tarea
            nueva_tarea = self.servicio.agregar_tarea(descripcion)
            self._actualizar_tabla()
            self._limpiar_campos()
            self.lbl_estado.config(text=f"Tarea #{nueva_tarea.id} añadida correctamente.")
            messagebox.showinfo("Éxito", f"Tarea #{nueva_tarea.id} registrada correctamente.")
        except ValueError as e:
            self.lbl_estado.config(text=f"Atención: {e}")
            messagebox.showwarning("Atención", str(e))
    
    def _marcar_completada(self):
        """Cambia el estado de la tarea seleccionada a completada."""
        if not self._id_tarea_seleccionada:
            self.lbl_estado.config(text="Debe seleccionar una tarea para marcar como completada.")
            messagebox.showwarning("Atención", "Seleccione una tarea de la tabla para completar.")
            return
        
        try:
            self.servicio.marcar_completada(self._id_tarea_seleccionada)
            self._actualizar_tabla()
            self._limpiar_campos()
            self.lbl_estado.config(text="Tarea marcada como completada.")
            messagebox.showinfo("Éxito", "Tarea completada correctamente.")
        except ValueError as e:
            self.lbl_estado.config(text=f"Error: {e}")
            messagebox.showerror("Error", str(e))
    
    def _eliminar_tarea(self):
        """Elimina la tarea seleccionada de la lista."""
        if not self._id_tarea_seleccionada:
            self.lbl_estado.config(text="Debe seleccionar una tarea para eliminar.")
            messagebox.showwarning("Atención", "Seleccione una tarea de la tabla para eliminar.")
            return
        
        respuesta = messagebox.askyesno(
            "Confirmar",
            f"¿Seguro que desea eliminar la tarea #{self._id_tarea_seleccionada}?"
        )
        
        if respuesta:
            try:
                self.servicio.eliminar_tarea(self._id_tarea_seleccionada)
                self._actualizar_tabla()
                self._limpiar_campos()
                self.lbl_estado.config(text="Tarea eliminada correctamente.")
                messagebox.showinfo("Éxito", "Tarea eliminada.")
            except ValueError as e:
                self.lbl_estado.config(text=f"Error: {e}")
                messagebox.showerror("Error", str(e))
    
    def _limpiar_campos(self):
        """Limpia el campo de entrada y resetea la selección."""
        self._id_tarea_seleccionada = None
        self.ent_descripcion.delete(0, tk.END)
        self.ent_descripcion.focus()
        self.tabla.selection_remove(self.tabla.selection())
    
    def _actualizar_tabla(self):
        """
        Refresca el Treeview con los datos actuales del servicio.
        Incluye feedback visual para tareas completadas.
        """
        # Limpiar tabla actual
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        # Insertar todas las tareas
        for tarea in self.servicio.obtener_todos():
            # ✅ FEEDBACK VISUAL: Cambiar texto según estado
            estado_texto = "✓ Completada" if tarea.estado_completado else "○ Pendiente"
            
            # Insertar fila en la tabla
            item_id = self.tabla.insert("", tk.END, values=(tarea.id, tarea.descripcion, estado_texto))
            
            # ✅ FEEDBACK VISUAL: Cambiar color para tareas completadas
            if tarea.estado_completado:
                self.tabla.item(item_id, tags=('completada',))
        
        # Configurar tag para tareas completadas (texto gris)
        self.tabla.tag_configure('completada', foreground='gray')
    
    def _seleccionar_fila(self, event):
        """Captura la selección de una fila en el Treeview."""
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion[0])
            valores = item["values"]
            self._id_tarea_seleccionada = int(valores[0])
            self.lbl_estado.config(text=f"Tarea #{valores[0]} seleccionada: {valores[1]}")
    
    def _cerrar_aplicacion(self):
        """Maneja el cierre seguro de la aplicación."""
        respuesta = messagebox.askyesno(
            "Salir",
            "¿Está seguro de que desea cerrar la aplicación?"
        )
        if respuesta:
            self.destroy()