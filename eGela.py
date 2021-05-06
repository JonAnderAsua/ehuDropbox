from tkinter import messagebox
import time
import requests
import helper

class eGela:
    _login = 0
    _cookiea = ""
    _refs = []
    _root = None



    def __init__(self, root):
        self._root = root

    def check_credentials(self, username, password, event=None):
        metodoa = "GET"
        goiburuak = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded'}
        datuak = ""
        edukia = ""
        cookie = ""
        uria = "https://egela.ehu.eus/"

        popup, progress_var, progress_bar = helper.progress("check_credentials", "Logging into eGela...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()

        print("##### 1. ESKAERA #####") #https://egela.ehu.eus/
        erantzuna = requests.request(metodoa, uria, allow_redirects=False)
        if()#Codigo 303
        print("Berbideraketa egiten...")
        uria = erantzuna.headers['Location']
        print(uria)
        if ("Set-Cookie" in erantzuna.headers):  # Set-Cookie goiburua badago balioa hartu eta gorde
            print("Cookie-a hartzen")
            cookie = erantzuna.headers['Set-Cookie']

            # MoodleSessionegela=t8c59kd3r8lnn4364ds5s1r5luo81jet; path=/; secure formatua duenez split bat erabili behar dugu
            cookie = cookie.split(";")[0]  # Honekin lehenengo zatia hartuko dugu, balio zaiguna
            print(cookie)
            goiburuak['Cookie'] = cookie

        print("##### 2. ESKAERA #####") #https://egela.ehu.eus/login/index.php
        metodoa = 'POST'
        datuak = {'username': username, 'password': password}
        goiburuak['Content-Length'] = str(len(datuak))
        print(goiburuak['Content-Length'])
        erantzuna = requests.request(metodoa, uria, data=datuak, headers=goiburuak, allow_redirects=False)

        progress = 33
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)

        print("\n##### 3. ESKAERA #####") #https://egela.ehu.eus/login/index.php?testsession=35809
        print("Berbideraketa egiten...")
        metodoa = "GET"
        uria = erantzuna.headers['Location']
        print(uria)
        if ("Set-Cookie" in erantzuna.headers):  # Set-Cookie goiburua badago balioa hartu eta gorde
            print("Cookie-a hartzen")
            cookie = erantzuna.headers['Set-Cookie']

            # MoodleSessionegela=t8c59kd3r8lnn4364ds5s1r5luo81jet; path=/; secure formatua duenez split bat erabili behar dugu
            cookie = cookie.split(";")[0]  # Honekin lehenengo zatia hartuko dugu, balio zaiguna
            print(cookie)
            goiburuak['Cookie'] = cookie

        progress = 66
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)

        print("\n##### 4. ESKAERA #####")

        uria = "https://egela.ehu.eus/"
        erantzuna = requests.request(metodoa, uria, allow_redirects=False)
        progress = 100
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)
        popup.destroy()

        if COMPROBACION_DE_LOG_IN:
            #############################################
            # ACTUALIZAR VARIABLES
            #############################################
            self._root.destroy()
        else:
            messagebox.showinfo("Alert Message", "Login incorrect!")

    def get_pdf_refs(self):
        popup, progress_var, progress_bar = helper.progress("get_pdf_refs", "Downloading PDF list...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()

        print("\n##### 4. ESKAERA (Ikasgairen eGelako orrialde nagusia) #####")
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        #############################################

        progress_step = float(100.0 / len(self._refs))

        print("\n##### HTML-aren azterketa... #####")
        #############################################
        # ANALISIS DE LA PAGINA DEL AULA EN EGELA
        # PARA BUSCAR PDFs
        #############################################

        # ACTUALIZAR BARRA DE PROGRESO
        # POR CADA PDF ANIADIDO EN self._refs
        progress += progress_step
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)

        popup.destroy()
        return self._refs

    def get_pdf(self, selection):
        print("##### PDF-a deskargatzen... #####")
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        #############################################

        return pdf_name, pdf_file
