import wmi
import tkinter as tk
from tkinter import ttk
import webbrowser

def get_system_info():
    c = wmi.WMI()

    os_info = c.Win32_OperatingSystem()[0]
    motherboard_info = c.Win32_BaseBoard()[0]
    bios_info = c.Win32_BIOS()[0]

    system_info = {
        'Sistema Operativo:': f'{os_info.Caption} (Build {os_info.BuildNumber})',
        'Motherboard:': motherboard_info.Product,
        'Versión del BIOS:': bios_info.BIOSVersion[1],
    }

    return system_info

def get_cpu_info():
    c = wmi.WMI()
    proc_info = c.Win32_Processor()[0]

    architecture_names = {
        0: "x86 Bits",
        1: "MIPS",
        2: "Alpha",
        3: "PowerPC",
        5: "ARM",
        6: "ia64 (Itanium-based)",
        9: "x64 Bits",
        12: "ARM64",
    }
    architecture = architecture_names.get(proc_info.Architecture, "Desconocida")

    virtualization_enabled = "Habilitado" if proc_info.VirtualizationFirmwareEnabled else "Deshabilitado"

    cpu_info = {
        'Procesador:': proc_info.Name,
        'Socket:': f"{proc_info.SocketDesignation}    Arquitectura: {architecture}    Virtualización: {virtualization_enabled}",
    }

    return cpu_info

def get_gpu_info():
    c = wmi.WMI()
    gpu_info = c.Win32_VideoController()[0]

    adapter_ram_gb = gpu_info.AdapterRAM / (1024 ** 3)

    gpu_info = {
        'Tarjeta Gráfica:': gpu_info.Name,
        'Fabricante:': gpu_info.AdapterCompatibility,
        'Versión del Driver:': gpu_info.DriverVersion,
        'Memoria de Video:': f"{adapter_ram_gb:.2f} GB",
        'Resolución:': f"{gpu_info.CurrentHorizontalResolution} x {gpu_info.CurrentVerticalResolution} ({gpu_info.CurrentRefreshRate} Hz)",
    }

    return gpu_info

def create_gui():
    system_info = get_system_info()
    cpu_info = get_cpu_info()
    gpu_info = get_gpu_info()

    root = tk.Tk()
    root.title("Información del Sistema")
    root.geometry("480x420")
    root.resizable(False, False)

    frame = ttk.Frame(root, padding=10)
    frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    sections = ["Información del Sistema", "Información de la CPU", "Información de la GPU"]
    row_num = 1

    for section in sections:
        section_label = ttk.Label(frame, text=section, font=("Helvetica", 10, "bold"))
        section_label.grid(column=0, row=row_num, columnspan=2, sticky=tk.W, padx=10, pady=5)

        row_num += 1

        if section == "Información del Sistema":
            section_info = system_info
        elif section == "Información de la CPU":
            section_info = cpu_info
        elif section == "Información de la GPU":
            section_info = gpu_info

        for key, value in section_info.items():
            info_label = ttk.Label(frame, text=f"{key} {value}")
            info_label.grid(column=0, row=row_num, columnspan=2, sticky=tk.W, padx=20, pady=2)

            row_num += 1

        if section != sections[-1]:
            separator = ttk.Separator(frame, orient='horizontal')
            separator.grid(column=0, row=row_num, columnspan=2, sticky="ew", pady=10)

            row_num += 1

    row_num += 1

    motherboard_driver_url = f"https://duckduckgo.com/?q=\{system_info['Motherboard:']}%20driver%20download"
    motherboard_driver_button = ttk.Button(frame, text="Descargar Controladores de Motherboard", command=lambda: webbrowser.open(motherboard_driver_url))
    motherboard_driver_button.grid(column=0, row=row_num, columnspan=1, sticky=tk.W, padx=10, pady=(10, 2))

    gpu_name = gpu_info['Tarjeta Gráfica:']
    if "Microsoft" in gpu_name:
        video_driver_url = f"https://duckduckgo.com/?q=\{cpu_info['Procesador:']}%20driver%20download"
        video_driver_button = ttk.Button(frame, text="Descargar Controladores de Video", command=lambda: webbrowser.open(video_driver_url))
    else:
        video_driver_url = f"https://duckduckgo.com/?q=\{gpu_info['Tarjeta Gráfica:']}%20driver%20download"
        video_driver_button = ttk.Button(frame, text="Descargar Controladores de Video", command=lambda: webbrowser.open(video_driver_url))

    video_driver_button.grid(column=1, row=row_num, columnspan=1, sticky=tk.W, padx=10, pady=(10, 2))

    root.mainloop()

if __name__ == "__main__":
    create_gui()
