from importlib.resources import path
from tkinter import *
from tkinter import ttk
import tkinter
import re
from tkinter import messagebox
from pytube import YouTube
from tkinter import filedialog
import os
#VENTANA PRINCIPAL
root = Tk()
root.title("Youtube Downloader")
root.iconbitmap("yt.ico")
ancho_ventana = 350
alto_ventana = 410

x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2 - 100

posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
root.geometry(posicion)
root.resizable(0,0)
#===========================================================
#CANVAS
canvas = Canvas(root, width=350, height= 420, bg="#C8C8C8",bd=0, highlightthickness=0)
canvas.grid(row=0,column=0,)


#=====================ELEMENTOS DEL CANVA =======================
#Imagen
img_logo = tkinter.PhotoImage(file = "yt_logo.png")
img_logo = img_logo.subsample(2,2)


#Entry
link_entry = ttk.Entry(canvas, font= "calibri 11", )
label_descarga = ttk.Label(canvas, text="Copie y pegue un link de Youtube:  ",font=("Bahnschrift SemiBold",12), background= "#C8C8C8" )

#titulo video
titulo = StringVar()

label_titulo = ttk.Label(canvas, textvariable= titulo, anchor= CENTER, wraplength=330, justify= "center", background= "#C8C8C8", font=("Bahnschrift SemiBold",10), foreground="#5831D1")


#+++++++++++++++++++++++++fUNCIONES++++++++++++++++++++++++++++++++++++++
#Elegir Ruta
def elegir_ruta():
    global ruta
    ruta = filedialog.askdirectory()
    
def borrar_link():
    link_entry.delete(0,END)

def validar_link():
    global yt
    link = link_entry.get()
    validacion_link = r'^(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(?:\S+)?$'
    regex_link = re.compile(validacion_link)
    
    if not regex_link.search(link):
        messagebox.showwarning("Youtube Downloader", "Ingrese un link válido")
        borrar_link()
       
    else: 
        yt = YouTube(link, on_complete_callback= True)
        titulo.set(yt.title)
        if seleccion.get() == 1:
            if yt.streams.get_by_resolution('1080p') != None:
                descarga = yt.streams.get_by_resolution('1080p')
                elegir_ruta()
                yt.register_on_complete_callback(convert_to_aac)
                descarga.download(output_path=ruta, filename_prefix="www.yanl.com ")
            else:
                descarga = yt.streams.get_by_resolution('720p')
                elegir_ruta()
                yt.register_on_complete_callback(convert_to_aac)
                descarga.download(output_path=ruta, filename_prefix="www.yanl.com ")
        elif seleccion.get() == 2:
            if yt.streams.get_by_resolution('480p') != None:
                descarga = yt.streams.get_by_resolution('480p')
                elegir_ruta()
                yt.register_on_complete_callback(convert_to_aac)
                descarga.download(output_path=ruta, filename_prefix="www.yanl.com ")
            else:
                descarga = yt.streams.get_by_resolution('360p')
                elegir_ruta()
                yt.register_on_complete_callback(convert_to_aac)
                descarga.download(output_path=ruta, filename_prefix="www.yanl.com ")
        elif seleccion.get() == 3:
            descarga = yt.streams.get_lowest_resolution()
            elegir_ruta()
            yt.register_on_complete_callback(convert_to_aac)
            descarga.download(output_path= ruta, filename_prefix="www.yanl.com ")
        elif seleccion.get() == 4:
            descarga = yt.streams.get_audio_only('mp4')
            elegir_ruta()
            yt.register_on_complete_callback(convert_to_aac)
            descarga.download(output_path= ruta)
            # os.rename(ruta+"/"+yt.title+".mp4", ruta +"/"+yt.title+".mp3") 
            title= re.sub(r'[<>:"/\|*?,.【】／]', "" , yt.title)
            os.rename(ruta+title+".mp4", ruta +title+".mp3")
            borrar_link()  


def convert_to_aac(stream, file_handle):
    messagebox.showinfo("Youtube Downloader", "Su descarga se ha completado!")
    return


#Boton


style_boton = ttk.Style()
style_boton.theme_use('winnative')
style_boton.configure("Botones.TButton", font=("Bahnschrift SemiBold",12), width=5, background = '#C8C8C8')

style_boton.map("Botones.TButton", foreground = [('active','#931616',)], background=[('active','#000000')])

boton_descargar = ttk.Button(canvas, text= "Buscar / Descargar" , style= "Botones.TButton", command= validar_link)


#Instrccion
label_final = ttk.Label(canvas, text="Para descargar elija una opcción y descargue!",font=("Bahnschrift SemiBold",11), background= "#C8C8C8" )

#Radio button
seleccion = IntVar()

style_radio_bt = ttk.Style()
style_radio_bt.configure("Botones.TRadiobutton", font= 'calibri 12', background = '#C8C8C8')

radio_button_HD = ttk.Radiobutton(canvas, text="Resolución alta", variable= seleccion, value=1, style= 'Botones.TRadiobutton')
radio_buttons_MD = ttk.Radiobutton(canvas, text="Resolución media", variable= seleccion, value=2, style= 'Botones.TRadiobutton')
radio_buttons_LW= ttk.Radiobutton(canvas, text="Resolución baja", variable= seleccion, value=3, style= 'Botones.TRadiobutton')
radio_buttons_MP3= ttk.Radiobutton(canvas, text="Solo audio", variable= seleccion, value=4, style= 'Botones.TRadiobutton')



#CREACION DE WIDGETS CANVA

canvas.create_image(50,10, image= img_logo, anchor = NW)
canvas.create_window(175, 140, window= label_descarga)
canvas.create_window(175, 170, window= link_entry,width=300)
canvas.create_window(175, 250, window= label_titulo)

canvas.create_window(175, 202, window= boton_descargar, width= 160)

canvas.create_window(180, 290, window= label_final)

canvas.create_window(100, 315, window= radio_button_HD, width= 150)
canvas.create_window(100, 340, window= radio_buttons_MD, width= 150)
canvas.create_window(100, 365, window= radio_buttons_LW, width= 150)
canvas.create_window(100, 390, window= radio_buttons_MP3, width= 150)

#--------------------------------------------------------------------------------









root.mainloop()