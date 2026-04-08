from pathlib import Path
import sys

import tkinter as tk
from tkinter import ttk

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from model.estudiante import Estudiante
from model.asignatura import Asignatura
from model.nota import Nota
from repository.asignatura_repositorio import AsignaturaRepositorio
from repository.estudiante_repositorio import EstudianteRepositorio
from repository.nota_repositorio import NotaRepositorio
from service.nota_servicio import NotaServicio


estudiante_repo = EstudianteRepositorio()
asignatura_repo = AsignaturaRepositorio()
nota_repo = NotaRepositorio()
servicio = NotaServicio(nota_repo)


def cargar_datos_iniciales():
    estudiante_1 = Estudiante("Juan")
    estudiante_2 = Estudiante("Ana")
    asignatura_1 = Asignatura("Matematicas")
    asignatura_2 = Asignatura("Historia")

    estudiante_repo.agregar(estudiante_1)
    estudiante_repo.agregar(estudiante_2)
    asignatura_repo.agregar(asignatura_1)
    asignatura_repo.agregar(asignatura_2)

    nota_repo.agregar(Nota(estudiante_1.uuid, asignatura_1.uuid, 90))
    nota_repo.agregar(Nota(estudiante_1.uuid, asignatura_2.uuid, 80))
    nota_repo.agregar(Nota(estudiante_2.uuid, asignatura_1.uuid, 95))


class AppNotas:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Notas")
        self.root.geometry("1180x720")
        self.root.configure(bg="#f4efe6")

        self.estudiante_id_actual = None
        self.asignatura_id_actual = None
        self.nota_id_actual = None

        self.entry_estudiante_nombre = None
        self.entry_asignatura_nombre = None
        self.combo_nota_estudiante = None
        self.combo_nota_asignatura = None
        self.entry_nota_valor = None
        self.tree_estudiantes = None
        self.tree_asignaturas = None
        self.tree_notas = None
        self.tree_notas_estudiante = None
        self.label_promedio = None
        self.label_estado = None

        self._configurar_estilos()
        self._crear_interfaz()
        self._refrescar_todo()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("App.TFrame", background="#f4efe6")
        style.configure(
            "Card.TLabelframe",
            background="#fffaf2",
            borderwidth=2,
            relief="solid",
        )
        style.configure(
            "Card.TLabelframe.Label",
            background="#fffaf2",
            foreground="#7a3e00",
            font=("Segoe UI", 11, "bold"),
        )
        style.configure(
            "App.TLabel",
            background="#f4efe6",
            foreground="#3b2f2f",
            font=("Segoe UI", 10),
        )
        style.configure(
            "Title.TLabel",
            background="#f4efe6",
            foreground="#7a3e00",
            font=("Segoe UI", 18, "bold"),
        )
        style.configure(
            "Accent.TButton",
            background="#c76b29",
            foreground="white",
            padding=6,
            font=("Segoe UI", 10, "bold"),
        )
        style.map(
            "Accent.TButton",
            background=[("active", "#a9551f"), ("pressed", "#8f4518")],
            foreground=[("disabled", "#f3d9c7")],
        )
        style.configure(
            "App.TEntry",
            fieldbackground="white",
            foreground="#2d1f1f",
            bordercolor="#d8b89c",
        )
        style.configure(
            "App.TCombobox",
            fieldbackground="white",
            foreground="#2d1f1f",
            arrowcolor="#7a3e00",
        )
        style.configure(
            "Treeview",
            background="white",
            fieldbackground="white",
            foreground="#2d1f1f",
            rowheight=28,
        )
        style.configure(
            "Treeview.Heading",
            background="#e6c7a8",
            foreground="#4a2c17",
            font=("Segoe UI", 10, "bold"),
        )
        style.map("Treeview", background=[("selected", "#d9823b")], foreground=[("selected", "white")])

    def _crear_interfaz(self):
        principal = ttk.Frame(self.root, padding=10, style="App.TFrame")
        principal.pack(fill="both", expand=True)
        principal.columnconfigure(0, weight=1)
        principal.columnconfigure(1, weight=1)
        principal.rowconfigure(0, weight=1)
        principal.rowconfigure(1, weight=1)

        titulo = ttk.Label(principal, text="Sistema de Gestion de Notas", style="Title.TLabel")
        titulo.grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=(0, 10))

        contenido = ttk.Frame(principal, style="App.TFrame")
        contenido.grid(row=1, column=0, columnspan=2, sticky="nsew")
        contenido.columnconfigure(0, weight=1)
        contenido.columnconfigure(1, weight=1)
        contenido.rowconfigure(0, weight=1)
        contenido.rowconfigure(1, weight=1)

        self._crear_panel_estudiantes(contenido)
        self._crear_panel_asignaturas(contenido)
        self._crear_panel_notas(contenido)
        self._crear_panel_resumen(contenido)

        self.label_estado = ttk.Label(self.root, text="Listo", padding=(10, 0, 10, 10), style="App.TLabel")
        self.label_estado.pack(anchor="w")

    def _crear_panel_estudiantes(self, parent):
        frame = ttk.LabelFrame(parent, text="CRUD de estudiantes", padding=10, style="Card.TLabelframe")
        frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        frame.columnconfigure(0, weight=1)

        ttk.Label(frame, text="Nombre", style="App.TLabel").grid(row=0, column=0, sticky="w")
        self.entry_estudiante_nombre = ttk.Entry(frame, style="App.TEntry")
        self.entry_estudiante_nombre.grid(row=1, column=0, sticky="ew", pady=(0, 8))

        botones = ttk.Frame(frame, style="App.TFrame")
        botones.grid(row=2, column=0, sticky="ew", pady=(0, 8))
        for index in range(4):
            botones.columnconfigure(index, weight=1)

        ttk.Button(botones, text="Crear", command=self.crear_estudiante, style="Accent.TButton").grid(row=0, column=0, sticky="ew", padx=2)
        ttk.Button(botones, text="Actualizar", command=self.actualizar_estudiante, style="Accent.TButton").grid(row=0, column=1, sticky="ew", padx=2)
        ttk.Button(botones, text="Eliminar", command=self.eliminar_estudiante, style="Accent.TButton").grid(row=0, column=2, sticky="ew", padx=2)
        ttk.Button(botones, text="Limpiar", command=self.limpiar_estudiante, style="Accent.TButton").grid(row=0, column=3, sticky="ew", padx=2)

        self.tree_estudiantes = ttk.Treeview(
            frame,
            columns=("uuid", "nombre"),
            show="headings",
            height=12,
        )
        self.tree_estudiantes.heading("uuid", text="UUID")
        self.tree_estudiantes.heading("nombre", text="Nombre")
        self.tree_estudiantes.column("uuid", width=220)
        self.tree_estudiantes.column("nombre", width=160)
        self.tree_estudiantes.grid(row=3, column=0, sticky="nsew")
        self.tree_estudiantes.bind("<<TreeviewSelect>>", self.seleccionar_estudiante)

        frame.rowconfigure(3, weight=1)

    def _crear_panel_asignaturas(self, parent):
        frame = ttk.LabelFrame(parent, text="CRUD de asignaturas", padding=10, style="Card.TLabelframe")
        frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        frame.columnconfigure(0, weight=1)

        ttk.Label(frame, text="Nombre", style="App.TLabel").grid(row=0, column=0, sticky="w")
        self.entry_asignatura_nombre = ttk.Entry(frame, style="App.TEntry")
        self.entry_asignatura_nombre.grid(row=1, column=0, sticky="ew", pady=(0, 8))

        botones = ttk.Frame(frame, style="App.TFrame")
        botones.grid(row=2, column=0, sticky="ew", pady=(0, 8))
        for index in range(4):
            botones.columnconfigure(index, weight=1)

        ttk.Button(botones, text="Crear", command=self.crear_asignatura, style="Accent.TButton").grid(row=0, column=0, sticky="ew", padx=2)
        ttk.Button(botones, text="Actualizar", command=self.actualizar_asignatura, style="Accent.TButton").grid(row=0, column=1, sticky="ew", padx=2)
        ttk.Button(botones, text="Eliminar", command=self.eliminar_asignatura, style="Accent.TButton").grid(row=0, column=2, sticky="ew", padx=2)
        ttk.Button(botones, text="Limpiar", command=self.limpiar_asignatura, style="Accent.TButton").grid(row=0, column=3, sticky="ew", padx=2)

        self.tree_asignaturas = ttk.Treeview(
            frame,
            columns=("uuid", "nombre"),
            show="headings",
            height=12,
        )
        self.tree_asignaturas.heading("uuid", text="UUID")
        self.tree_asignaturas.heading("nombre", text="Nombre")
        self.tree_asignaturas.column("uuid", width=220)
        self.tree_asignaturas.column("nombre", width=160)
        self.tree_asignaturas.grid(row=3, column=0, sticky="nsew")
        self.tree_asignaturas.bind("<<TreeviewSelect>>", self.seleccionar_asignatura)

        frame.rowconfigure(3, weight=1)

    def _crear_panel_notas(self, parent):
        frame = ttk.LabelFrame(parent, text="CRUD de notas", padding=10, style="Card.TLabelframe")
        frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        frame.columnconfigure(0, weight=1)

        formulario = ttk.Frame(frame, style="App.TFrame")
        formulario.grid(row=0, column=0, sticky="ew")
        formulario.columnconfigure(1, weight=1)

        ttk.Label(formulario, text="Estudiante", style="App.TLabel").grid(row=0, column=0, sticky="w")
        self.combo_nota_estudiante = ttk.Combobox(formulario, state="readonly", style="App.TCombobox")
        self.combo_nota_estudiante.grid(row=0, column=1, sticky="ew", padx=(6, 0), pady=2)

        ttk.Label(formulario, text="Asignatura", style="App.TLabel").grid(row=1, column=0, sticky="w")
        self.combo_nota_asignatura = ttk.Combobox(formulario, state="readonly", style="App.TCombobox")
        self.combo_nota_asignatura.grid(row=1, column=1, sticky="ew", padx=(6, 0), pady=2)

        ttk.Label(formulario, text="Calificacion", style="App.TLabel").grid(row=2, column=0, sticky="w")
        self.entry_nota_valor = ttk.Entry(formulario, style="App.TEntry")
        self.entry_nota_valor.grid(row=2, column=1, sticky="ew", padx=(6, 0), pady=2)

        botones = ttk.Frame(frame, style="App.TFrame")
        botones.grid(row=1, column=0, sticky="ew", pady=(8, 8))
        for index in range(4):
            botones.columnconfigure(index, weight=1)

        ttk.Button(botones, text="Crear", command=self.crear_nota, style="Accent.TButton").grid(row=0, column=0, sticky="ew", padx=2)
        ttk.Button(botones, text="Actualizar", command=self.actualizar_nota, style="Accent.TButton").grid(row=0, column=1, sticky="ew", padx=2)
        ttk.Button(botones, text="Eliminar", command=self.eliminar_nota, style="Accent.TButton").grid(row=0, column=2, sticky="ew", padx=2)
        ttk.Button(botones, text="Limpiar", command=self.limpiar_nota, style="Accent.TButton").grid(row=0, column=3, sticky="ew", padx=2)

        self.tree_notas = ttk.Treeview(
            frame,
            columns=("uuid", "estudiante", "asignatura", "valor"),
            show="headings",
            height=10,
        )
        self.tree_notas.heading("uuid", text="UUID")
        self.tree_notas.heading("estudiante", text="Estudiante")
        self.tree_notas.heading("asignatura", text="Asignatura")
        self.tree_notas.heading("valor", text="Calificacion")
        self.tree_notas.column("uuid", width=210)
        self.tree_notas.column("estudiante", width=130)
        self.tree_notas.column("asignatura", width=130)
        self.tree_notas.column("valor", width=90)
        self.tree_notas.grid(row=2, column=0, sticky="nsew")
        self.tree_notas.bind("<<TreeviewSelect>>", self.seleccionar_nota)

        frame.rowconfigure(2, weight=1)

    def _crear_panel_resumen(self, parent):
        frame = ttk.LabelFrame(parent, text="Notas por estudiante y promedio", padding=10, style="Card.TLabelframe")
        frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        frame.columnconfigure(0, weight=1)

        self.label_promedio = ttk.Label(frame, text="Promedio: 0.00", style="Title.TLabel")
        self.label_promedio.grid(row=0, column=0, sticky="w", pady=(0, 8))

        self.tree_notas_estudiante = ttk.Treeview(
            frame,
            columns=("asignatura", "valor"),
            show="headings",
            height=14,
        )
        self.tree_notas_estudiante.heading("asignatura", text="Asignatura")
        self.tree_notas_estudiante.heading("valor", text="Calificacion")
        self.tree_notas_estudiante.column("asignatura", width=220)
        self.tree_notas_estudiante.column("valor", width=120)
        self.tree_notas_estudiante.grid(row=1, column=0, sticky="nsew")

        frame.rowconfigure(1, weight=1)

    def _refrescar_todo(self):
        self.refrescar_estudiantes()
        self.refrescar_asignaturas()
        self.refrescar_notas()
        self._refrescar_combos()
        self.refrescar_resumen_estudiante()

    def refrescar_estudiantes(self):
        self._limpiar_tree(self.tree_estudiantes)
        for estudiante in estudiante_repo.obtener_todos():
            self.tree_estudiantes.insert("", "end", iid=estudiante.uuid, values=(estudiante.uuid, estudiante.nombre))

    def refrescar_asignaturas(self):
        self._limpiar_tree(self.tree_asignaturas)
        for asignatura in asignatura_repo.obtener_todos():
            self.tree_asignaturas.insert("", "end", iid=asignatura.uuid, values=(asignatura.uuid, asignatura.nombre))

    def refrescar_notas(self):
        self._limpiar_tree(self.tree_notas)
        for nota in nota_repo.obtener_todos():
            estudiante = estudiante_repo.obtener_por_uuid(nota.estudiante_uuid)
            asignatura = asignatura_repo.obtener_por_uuid(nota.asignatura_uuid)
            estudiante_nombre = estudiante.nombre if estudiante else "Sin estudiante"
            asignatura_nombre = asignatura.nombre if asignatura else "Sin asignatura"
            self.tree_notas.insert(
                "",
                "end",
                iid=nota.uuid,
                values=(nota.uuid, estudiante_nombre, asignatura_nombre, f"{nota.valor:.2f}"),
            )

    def refrescar_resumen_estudiante(self):
        self._limpiar_tree(self.tree_notas_estudiante)

        if not self.estudiante_id_actual:
            self.label_promedio.config(text="Promedio: 0.00")
            return

        for nota in nota_repo.obtener_por_estudiante(self.estudiante_id_actual):
            asignatura = asignatura_repo.obtener_por_uuid(nota.asignatura_uuid)
            asignatura_nombre = asignatura.nombre if asignatura else "Sin asignatura"
            self.tree_notas_estudiante.insert("", "end", values=(asignatura_nombre, f"{nota.valor:.2f}"))

        promedio = servicio.calcular_promedio(self.estudiante_id_actual)
        self.label_promedio.config(text=f"Promedio: {promedio:.2f}")

    def _refrescar_combos(self):
        estudiantes = [self._formato_combo_estudiante(e) for e in estudiante_repo.obtener_todos()]
        asignaturas = [self._formato_combo_asignatura(a) for a in asignatura_repo.obtener_todos()]
        self.combo_nota_estudiante["values"] = estudiantes
        self.combo_nota_asignatura["values"] = asignaturas

    def crear_estudiante(self):
        nombre = self.entry_estudiante_nombre.get().strip()
        if not nombre:
            self._estado("Ingrese un nombre de estudiante")
            return

        estudiante_repo.agregar(Estudiante(nombre))
        self.limpiar_estudiante()
        self._refrescar_todo()
        self._estado("Estudiante creado")

    def actualizar_estudiante(self):
        if not self.estudiante_id_actual:
            self._estado("Seleccione un estudiante para actualizar")
            return

        nombre = self.entry_estudiante_nombre.get().strip()
        if not nombre:
            self._estado("Ingrese un nombre de estudiante")
            return

        estudiante_repo.actualizar(self.estudiante_id_actual, nombre)
        self._refrescar_todo()
        self._estado("Estudiante actualizado")

    def eliminar_estudiante(self):
        if not self.estudiante_id_actual:
            self._estado("Seleccione un estudiante para eliminar")
            return

        nota_repo.eliminar_por_estudiante(self.estudiante_id_actual)
        estudiante_repo.eliminar(self.estudiante_id_actual)
        self.limpiar_estudiante()
        self.limpiar_nota()
        self._refrescar_todo()
        self._estado("Estudiante eliminado")

    def limpiar_estudiante(self):
        self.estudiante_id_actual = None
        self.entry_estudiante_nombre.delete(0, tk.END)
        self.tree_estudiantes.selection_remove(self.tree_estudiantes.selection())
        self.refrescar_resumen_estudiante()

    def crear_asignatura(self):
        nombre = self.entry_asignatura_nombre.get().strip()
        if not nombre:
            self._estado("Ingrese un nombre de asignatura")
            return

        asignatura_repo.agregar(Asignatura(nombre))
        self.limpiar_asignatura()
        self._refrescar_todo()
        self._estado("Asignatura creada")

    def actualizar_asignatura(self):
        if not self.asignatura_id_actual:
            self._estado("Seleccione una asignatura para actualizar")
            return

        nombre = self.entry_asignatura_nombre.get().strip()
        if not nombre:
            self._estado("Ingrese un nombre de asignatura")
            return

        asignatura_repo.actualizar(self.asignatura_id_actual, nombre)
        self._refrescar_todo()
        self._estado("Asignatura actualizada")

    def eliminar_asignatura(self):
        if not self.asignatura_id_actual:
            self._estado("Seleccione una asignatura para eliminar")
            return

        nota_repo.eliminar_por_asignatura(self.asignatura_id_actual)
        asignatura_repo.eliminar(self.asignatura_id_actual)
        self.limpiar_asignatura()
        self.limpiar_nota()
        self._refrescar_todo()
        self._estado("Asignatura eliminada")

    def limpiar_asignatura(self):
        self.asignatura_id_actual = None
        self.entry_asignatura_nombre.delete(0, tk.END)
        self.tree_asignaturas.selection_remove(self.tree_asignaturas.selection())

    def crear_nota(self):
        estudiante_uuid = self._uuid_desde_combo(self.combo_nota_estudiante.get())
        asignatura_uuid = self._uuid_desde_combo(self.combo_nota_asignatura.get())
        valor = self._leer_valor_nota()

        if not estudiante_uuid:
            self._estado("Seleccione un estudiante para la nota")
            return
        if not asignatura_uuid:
            self._estado("Seleccione una asignatura para la nota")
            return
        if valor is None:
            return

        nota_repo.agregar(Nota(estudiante_uuid, asignatura_uuid, valor))
        self.estudiante_id_actual = estudiante_uuid
        self.limpiar_nota(formatear_estado=False)
        self._refrescar_todo()
        self._estado("Nota creada")

    def actualizar_nota(self):
        if not self.nota_id_actual:
            self._estado("Seleccione una nota para actualizar")
            return

        estudiante_uuid = self._uuid_desde_combo(self.combo_nota_estudiante.get())
        asignatura_uuid = self._uuid_desde_combo(self.combo_nota_asignatura.get())
        valor = self._leer_valor_nota()

        if not estudiante_uuid:
            self._estado("Seleccione un estudiante para la nota")
            return
        if not asignatura_uuid:
            self._estado("Seleccione una asignatura para la nota")
            return
        if valor is None:
            return

        nota_repo.actualizar(self.nota_id_actual, estudiante_uuid, asignatura_uuid, valor)
        self.estudiante_id_actual = estudiante_uuid
        self._refrescar_todo()
        self._estado("Nota actualizada")

    def eliminar_nota(self):
        if not self.nota_id_actual:
            self._estado("Seleccione una nota para eliminar")
            return

        nota_repo.eliminar(self.nota_id_actual)
        self.limpiar_nota(formatear_estado=False)
        self._refrescar_todo()
        self._estado("Nota eliminada")

    def limpiar_nota(self, formatear_estado=True):
        self.nota_id_actual = None
        self.combo_nota_estudiante.set("")
        self.combo_nota_asignatura.set("")
        self.entry_nota_valor.delete(0, tk.END)
        self.tree_notas.selection_remove(self.tree_notas.selection())
        if formatear_estado:
            self._estado("Formulario de nota limpio")

    def seleccionar_estudiante(self, _event=None):
        seleccion = self.tree_estudiantes.selection()
        if not seleccion:
            return

        self.estudiante_id_actual = seleccion[0]
        estudiante = estudiante_repo.obtener_por_uuid(self.estudiante_id_actual)
        if estudiante is None:
            return

        self.entry_estudiante_nombre.delete(0, tk.END)
        self.entry_estudiante_nombre.insert(0, estudiante.nombre)
        self.refrescar_resumen_estudiante()

    def seleccionar_asignatura(self, _event=None):
        seleccion = self.tree_asignaturas.selection()
        if not seleccion:
            return

        self.asignatura_id_actual = seleccion[0]
        asignatura = asignatura_repo.obtener_por_uuid(self.asignatura_id_actual)
        if asignatura is None:
            return

        self.entry_asignatura_nombre.delete(0, tk.END)
        self.entry_asignatura_nombre.insert(0, asignatura.nombre)

    def seleccionar_nota(self, _event=None):
        seleccion = self.tree_notas.selection()
        if not seleccion:
            return

        self.nota_id_actual = seleccion[0]
        nota = nota_repo.obtener_por_uuid(self.nota_id_actual)
        if nota is None:
            return

        estudiante = estudiante_repo.obtener_por_uuid(nota.estudiante_uuid)
        asignatura = asignatura_repo.obtener_por_uuid(nota.asignatura_uuid)

        self.combo_nota_estudiante.set(self._formato_combo_estudiante(estudiante) if estudiante else "")
        self.combo_nota_asignatura.set(self._formato_combo_asignatura(asignatura) if asignatura else "")
        self.entry_nota_valor.delete(0, tk.END)
        self.entry_nota_valor.insert(0, str(nota.valor))

        self.estudiante_id_actual = nota.estudiante_uuid
        estudiante_seleccionado = self.tree_estudiantes.selection()
        if estudiante and estudiante.uuid != (estudiante_seleccionado[0] if estudiante_seleccionado else None):
            self.tree_estudiantes.selection_set(estudiante.uuid)
            self.tree_estudiantes.focus(estudiante.uuid)
            self.entry_estudiante_nombre.delete(0, tk.END)
            self.entry_estudiante_nombre.insert(0, estudiante.nombre)

        self.refrescar_resumen_estudiante()

    def _leer_valor_nota(self):
        try:
            return float(self.entry_nota_valor.get())
        except ValueError:
            self._estado("Ingrese una calificacion numerica valida")
            return None

    def _estado(self, mensaje):
        self.label_estado.config(text=mensaje)

    @staticmethod
    def _limpiar_tree(tree):
        for item in tree.get_children():
            tree.delete(item)

    @staticmethod
    def _uuid_desde_combo(texto):
        if " | " not in texto:
            return None
        return texto.split(" | ", 1)[0]

    @staticmethod
    def _formato_combo_estudiante(estudiante):
        return f"{estudiante.uuid} | {estudiante.nombre}"

    @staticmethod
    def _formato_combo_asignatura(asignatura):
        return f"{asignatura.uuid} | {asignatura.nombre}"


if __name__ == "__main__":
    cargar_datos_iniciales()
    root = tk.Tk()
    app = AppNotas(root)
    root.mainloop()
