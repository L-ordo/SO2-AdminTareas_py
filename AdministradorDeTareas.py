import tkinter as tk
from tkinter import ttk
import psutil

# Funci\u00f3n para actualizar la lista de procesos
def actualizar_procesos():
    for item in tree.get_children():
        tree.delete(item)

    for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            # Validar que memory_info no sea None
            memoria = proc.info['memory_info']
            memoria_usada = f"{memoria.rss / (1024 ** 2):.2f} MB" if memoria else "N/A"

            tree.insert("", "end", values=(
                proc.info['pid'],
                proc.info['name'],
                f"{proc.info['cpu_percent']}%",
                memoria_usada
            ))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    ventana.after(2000, actualizar_procesos)  # Actualizar cada 2 segundos

# Funci\u00f3n para finalizar un proceso
def finalizar_proceso():
    seleccion = tree.selection()
    if seleccion:
        pid = int(tree.item(seleccion[0], 'values')[0])
        try:
            proc = psutil.Process(pid)
            proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            print(f"No se pudo finalizar el proceso: {e}")


# Funci\u00f3n para suspender un proceso
def suspender_proceso():
    seleccion = tree.selection()
    if seleccion:
        pid = int(tree.item(seleccion[0], 'values')[0])
        try:
            proc = psutil.Process(pid)
            proc.suspend()
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            print(f"No se pudo suspender el proceso: {e}")


# Funci\u00f3n para reanudar un proceso
def reanudar_proceso():
    seleccion = tree.selection()
    if seleccion:
        pid = int(tree.item(seleccion[0], 'values')[0])
        try:
            proc = psutil.Process(pid)
            proc.resume()
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            print(f"No se pudo reanudar el proceso: {e}")


# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Administrador de Tareas")
ventana.geometry("800x400")

# Crear un \u00e1rbol para mostrar los procesos
columnas = ("PID", "Nombre", "CPU (%)", "Memoria (MB)")
tree = ttk.Treeview(ventana, columns=columnas, show="headings")
for col in columnas:
    tree.heading(col, text=col)
tree.pack(fill=tk.BOTH, expand=True)

# Botones de control
frame_botones = tk.Frame(ventana)
frame_botones.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

boton_finalizar = tk.Button(frame_botones, text="Finalizar Proceso", command=finalizar_proceso)
boton_finalizar.pack(side=tk.LEFT, padx=10)

boton_suspender = tk.Button(frame_botones, text="Suspender Proceso", command=suspender_proceso)
boton_suspender.pack(side=tk.LEFT, padx=10)

boton_reanudar = tk.Button(frame_botones, text="Reanudar Proceso", command=reanudar_proceso)
boton_reanudar.pack(side=tk.LEFT, padx=10)

# Actualizar la lista de procesos en tiempo real
actualizar_procesos()

# Iniciar el bucle principal
ventana.mainloop()