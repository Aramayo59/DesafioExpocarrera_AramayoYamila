import tkinter as tk
from tkinter import ttk
from ConexionBD import *  # Asegúrate de que esta importación funcione correctamente con tu conexión a la BD

def abrir_ventana_listado():
    root = tk.Toplevel()
    root.title("Listado de personas")
    root.geometry("900x600")  # Ajustamos la ventana para que todo se vea correctamente

    # Estilo para los radio buttons
    style = ttk.Style()
    style.configure("BigFont.TRadiobutton", font=("Helvetica", 14))

    label_seleccionar_carrera = tk.Label(root, text="Seleccionar carrera para filtrar", bg="#b39658", font=("Calibri", 20, "bold"))
    label_seleccionar_carrera.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(10, 0))

    frame_superior = tk.Frame(root)
    frame_superior.grid(row=1, column=0, sticky="nsew", columnspan=3)  # Frame para los radio buttons

    frame_inferior = tk.Frame(root, bg="#dbc79c")
    frame_inferior.grid(row=2, column=0, columnspan=4, sticky="nsew")

    # Creación de la grilla (Treeview) para mostrar los datos
    arbol = ttk.Treeview(frame_inferior, columns=("apellido", "nombre", "dni", "carrera"), show="headings")
    arbol.grid(row=0, column=0, columnspan=4, sticky="nsew")

    arbol.heading("apellido", text="Apellido")
    arbol.heading("nombre", text="Nombre")
    arbol.heading("dni", text="DNI")
    arbol.heading("carrera", text="Carrera")

    def obtener_nombre_carrera(id_carreras):
        """Función que devuelve el nombre de la carrera a partir del ID."""
        carreras = {
            1: "Software",
            2: "Enfermería",
            3: "Diseño de Espacios",
            4: "Guía de Trekking",
            5: "Guía de Turismo",
            6: "Turismo y Hotelería"
        }
        return carreras.get(id_carreras, "Desconocido")

    def mostrar_registros():
        """Función para mostrar los registros en la grilla."""
        for row in arbol.get_children():
            arbol.delete(row)

        carrera_seleccionada = variable_de_filtro_carrera.get()
        print("Carrera seleccionada:", carrera_seleccionada)  # Para verificar qué valor se está utilizando

        if carrera_seleccionada:
            consulta = "SELECT apellido, nombre, dni, id_carreras FROM personas WHERE id_carreras = %s"
            mycursor.execute(consulta, (carrera_seleccionada,))
        else:
            consulta = "SELECT apellido, nombre, dni, id_carreras FROM personas"
            mycursor.execute(consulta)

        for (apellido, nombre, dni, id_carreras) in mycursor:
            nombre_carrera = obtener_nombre_carrera(id_carreras)  # Obtener el nombre de la carrera
            arbol.insert("", "end", values=(apellido, nombre, dni, nombre_carrera))  # Mostrar el nombre de la carrera

    variable_de_filtro_carrera = tk.StringVar()

    carreras = {
        1: "Software",
        2: "Enfermería",
        3: "Diseño de Espacios",
        4: "Guía de Trekking",
        5: "Guía de Turismo",
        6: "Turismo y Hotelería"
    }

    # Crear los radio buttons para las carreras
    for i, (id_carrera, nombre_carrera) in enumerate(carreras.items()):
        filtro_carrera = ttk.Radiobutton(frame_superior, text=nombre_carrera, variable=variable_de_filtro_carrera, value=str(id_carrera), style="BigFont.TRadiobutton", command=mostrar_registros)
        row = i // 3  # Calcular el índice de fila
        col = i % 3  # Calcular el índice de columna
        filtro_carrera.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)  # Configuración de grid

    # Mover el botón cerrar a la parte inferior derecha
    btn_cerrar = tk.Button(root, text="Cerrar", command=root.destroy, font=('Calibri', 15), bg="#F8F8FF", width=10)
    btn_cerrar.grid(row=3, column=3, padx=10, pady=10, sticky="se")  # Ubicado en la parte inferior derecha

    # Asegurarse de que los frames ocupen el mismo tamaño
    frame_superior.grid_columnconfigure(0, weight=1)
    frame_inferior.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)

    mostrar_registros()

    root.mainloop()
