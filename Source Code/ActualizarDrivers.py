import wmi
import winreg
import tkinter as tk
from tkinter import ttk
import webbrowser

# Función para obtener información del sistema utilizando WMI
def get_system_info():
    global motherboard_info
    global proc_info, gpu_info
    c = wmi.WMI()

    computer_info = c.Win32_ComputerSystem()[0]
    os_info = c.Win32_OperatingSystem()[0]
    proc_info = c.Win32_Processor()[0]
    gpu_info = c.Win32_VideoController()[0]
    motherboard_info = c.Win32_BaseBoard()[0]
    bios_info = c.Win32_BIOS()[0]
    bios_version = bios_info.BIOSVersion[1]

    os_name = os_info.Caption
    os_version = f'{os_info.Version} (Build {os_info.BuildNumber})'
    system_ram = float(computer_info.TotalPhysicalMemory) / (1024 ** 3)

    return {
        'Sistema Operativo:': os_name,
        'Versión del SO:': os_version,
        'Motherboard:': motherboard_info.Product,
        'Versión del BIOS:': bios_version,
        'Procesador:': proc_info.Name,
        'Memoria RAM Disponible:': f'{system_ram:.2f} GB',
        'Tarjeta Gráfica:': gpu_info.Name,
    }

# Función para abrir un enlace web para descargar los controladores
def open_driver_download_link(url):
    webbrowser.open(url)

# Función para obtener información del registro y verificar los valores
def check_registry_values():
    registro_path = r'SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000'

    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registro_path, 0, winreg.KEY_READ)

        driver_desc = winreg.QueryValueEx(key, "DriverDesc")[0]
        Provider_Name = winreg.QueryValueEx(key, "ProviderName")[0]

        winreg.CloseKey(key)

        return 0 if driver_desc == "Microsoft Basic Display Adapter" and Provider_Name == "Microsoft" else 1

    except Exception as e:
        print("Error al acceder al registro:", e)
        return -1

# Función para crear la interfaz gráfica y mostrar la información del sistema
def create_gui(system_info):
    global motherboard_info
    global proc_info, gpu_info
    root = tk.Tk()
    root.title("Información del Sistema")
    root.resizable(False, False)

    frame = ttk.Frame(root, padding=10)
    frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    title_label = ttk.Label(frame, text="Información del Sistema", font=("Helvetica", 16))
    title_label.grid(column=0, row=0, columnspan=3)

    row_num = 1
    for key, value in system_info.items():
        label = ttk.Label(frame, text=key)
        label.grid(column=0, row=row_num, sticky=tk.W)

        value_label = ttk.Label(frame, text=value)
        value_label.grid(column=1, row=row_num, sticky=tk.W)

        row_num += 1

    # Botón para descargar controladores de la placa madre
    motherboard_driver_url = f"https://duckduckgo.com/?q=\{motherboard_info.Product}%20driver%20%22download%22"
    motherboard_driver_button = ttk.Button(frame, text="Descargar Controladores de Motherboard", command=lambda: open_driver_download_link(motherboard_driver_url))
    motherboard_driver_button.grid(column=0, row=row_num, columnspan=2, sticky=tk.W)

    # Definir las URL de descarga de controladores de video segun el tipo de grafica
    url_1 = f"https://duckduckgo.com/?q=\{proc_info.Name}%20driver%20%22download%22"
    url_2 = f"https://duckduckgo.com/?q=\{gpu_info.Name}%20driver%20%22download%22"

    # Verificar los valores del registro
    registry_result = check_registry_values()

    # Botón para descargar controladores de video
    video_driver_button = ttk.Button(frame, text="Descargar Controladores de Video", command=lambda: open_driver_download_link(url_1 if registry_result == 0 else url_2))
    video_driver_button.grid(column=0, row=row_num + 1, columnspan=2, sticky=tk.W)

    root.mainloop()

if __name__ == "__main__":
    system_info = get_system_info()
    create_gui(system_info)
