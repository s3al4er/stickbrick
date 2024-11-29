import customtkinter as ctk
import serial.tools.list_ports
import subprocess
import threading
import time
import webbrowser

def get_com_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def brick_device():
    selected_port = com_port_var.get()
    delay = int(delay_var.get())
    if not selected_port:
        result_label.configure(text="Выберите COM-порт!", text_color="red")
        return

    firmware_file = "esp32fw.bin"
    esptool_path = "esptool.exe"
    processes_to_kill = ["esptool.exe", "py.exe", "stickbrick.exe", "python3.exe", "python.exe"]
    
    def flash_and_kill():
        try:
            result_label.configure(text="Прошивка началась...", text_color="blue")
            subprocess.Popen([esptool_path, "--port", selected_port, "write_flash", "0x0", firmware_file])
            time.sleep(delay)
            for process in processes_to_kill:
                subprocess.run(["taskkill", "/f", "/im", process])
            result_label.configure(text="Окирпичивание завершено!", text_color="green")
        except Exception as e:
            result_label.configure(text=f"Ошибка: {e}", text_color="red")
    
    threading.Thread(target=flash_and_kill).start()

def refresh_com_ports():
    com_ports = get_com_ports()
    com_port_menu.configure(values=com_ports)
    if com_ports:
        com_port_menu.set(com_ports[0])
    else:
        com_port_menu.set("")

def open_telegram():
    webbrowser.open("https://t.me/stickc10")

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("StickBrick")
app.geometry("400x300")

com_port_var = ctk.StringVar()
delay_var = ctk.StringVar(value="15")

title_label = ctk.CTkLabel(app, text="Выберите COM-порт и нажмите 'Окирпичить'", font=("Arial", 16))
title_label.pack(pady=10)

com_port_menu = ctk.CTkOptionMenu(app, variable=com_port_var, values=get_com_ports())
com_port_menu.pack(pady=10)

refresh_button = ctk.CTkButton(app, text="Обновить COM-порты", command=refresh_com_ports, fg_color="darkgreen", corner_radius=10)
refresh_button.pack(pady=5)

delay_label = ctk.CTkLabel(app, text="Выберите задержку (в секундах):", font=("Arial", 14))
delay_label.pack(pady=5)

delay_menu = ctk.CTkOptionMenu(app, variable=delay_var, values=["5", "10", "15", "20", "30", "60"])
delay_menu.pack(pady=5)

brick_button = ctk.CTkButton(app, text="Окирпичить", command=brick_device, fg_color="darkgreen", corner_radius=10)
brick_button.pack(pady=10)

telegram_button = ctk.CTkButton(app, text="Telegram", command=open_telegram, fg_color="darkgreen", corner_radius=10)
telegram_button.pack(pady=10)

result_label = ctk.CTkLabel(app, text="", font=("Arial", 12))
result_label.pack(pady=10)

refresh_com_ports()

app.mainloop()
