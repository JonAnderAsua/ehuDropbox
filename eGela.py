from tkinter import messagebox
import requests
import urllib
import urllib.parse #https://stackoverflow.com/questions/28906859/module-has-no-attribute-urlencode
from bs4 import BeautifulSoup
import time
import helper

class eGela:
    _login = 0
    _cookiea = ""
    _refs = []
    _root = None



    def __init__(self, root):
        self._root = root

    def check_credentials(self, username, password, event=None):
        popup, progress_var, progress_bar = helper.progress("check_credentials", "Logging into eGela...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()

        print("##### 1. ESKAERA #####")
        metodoa = 'POST'
        uria = "https://egela.ehu.eus/login/index.php"
        headers = {'Host': 'egela.ehu.eus','Content-Type': 'application/x-www-form-urlencoded', }
        data = {'username': username.get(),'password': password.get()}
        data_encoded = urllib.parse.urlencode(data)
        headers['Content-Length'] = str(len(data_encoded))
        erantzuna = requests.request(metodoa, uria, headers=headers, data=data_encoded, allow_redirects=False)
        kodea = erantzuna.status_code
        deskribapena = erantzuna.reason
        print(str(kodea) + " " + deskribapena)
        cookie = ""
        location = ""
        for goiburua in erantzuna.headers:
            print(goiburua + ": " + erantzuna.headers[goiburua])
            if goiburua == "Set-Cookie":
                cookie = erantzuna.headers[goiburua].split(";")[0]
            elif goiburua == "Location":
                location = erantzuna.headers[goiburua]
        self._cookiea = cookie
        progress = 33
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(1)

        print("\n##### 2. ESKAERA #####")
        metodoa = 'GET'
        uria = location
        goiburuak = {'Host': uria.split('/')[2],'Cookie': cookie}
        erantzuna = requests.request(metodoa, uria, headers=goiburuak, allow_redirects=False)
        kodea = erantzuna.status_code
        deskribapena = erantzuna.reason
        print(str(kodea) + " " + deskribapena)
        for goiburua in erantzuna.headers:
            print(goiburua + ": " + erantzuna.headers[goiburua])
            if goiburua == "Set-Cookie":
                cookie = erantzuna.headers[goiburua].split(";")[0]
            elif goiburua == "Location":
                location = erantzuna.headers[goiburua]

        progress = 66
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)

        print("\n##### 3. ESKAERA #####")
        #metodoa = 'GET'
        uria = location
        goiburuak = {'Host': 'egela.ehu.eus', 'Cookie': self._cookiea}
        erantzuna = requests.request(metodoa, uria, headers=goiburuak, allow_redirects=False)
        kodea = erantzuna.status_code
        deskribapena = erantzuna.reason
        print(str(kodea) + " " + deskribapena)
        #for goiburua in erantzuna.headers:
            #print(goiburua + ": " + erantzuna.headers[goiburua])
        #edukia = erantzuna.content

        progress = 100
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)
        popup.destroy()
        erantzuna.headers['Location'] = 'https://egela.ehu.eus/course/view.php?id=42336' #Web sistemak irakasgaiko id-a
        if erantzuna.headers.__contains__('Location'):
            headers = {'Host': 'egela.ehu.eus', 'Cookie': self._cookiea}
            requests.request('GET', erantzuna.headers['Location'], headers=headers, allow_redirects=False)
            self._login = 1
            self._root.destroy()
        else:
            messagebox.showinfo("Alert Message", "Login incorrect!")

    def get_pdf_refs(self):
        popup, progress_var, progress_bar = helper.progress("get_pdf_refs", "Downloading PDF list...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()

        print("\n##### 4. ESKAERA (Ikasgairen eGelako orrialde nagusia) #####")
        metodoa = 'GET'
        uria = "https://egela.ehu.eus/course/view.php?id=42336"
        goiburuak = {'Host': 'egela.ehu.eus', 'Cookie': self._cookiea}
        erantzuna = requests.request(metodoa, uria, headers=goiburuak, allow_redirects=False)
        kodea = erantzuna.status_code
        deskribapena = erantzuna.reason
        print(str(kodea) + " " + deskribapena)
        for goiburua in erantzuna.headers:
            print(goiburua + ": " + erantzuna.headers[goiburua])
        edukia = erantzuna.content

        print("\n##### HTML-aren azterketa... #####")
        soup = BeautifulSoup(edukia, 'html.parser')
        item_results = soup.find_all('img', {'class': 'iconlarge activityicon'})
        for each in item_results:
            if each['src'].find("/pdf") != -1:
                print("\n##### PDF-a bat aurkitu da! #####")
                pdf_link = each.parent['href']
                uria = pdf_link
                headers = {'Host': 'egela.ehu.eus','Cookie': self._cookiea}
                erantzuna = requests.get(uria, headers=headers, allow_redirects=False)
                print(metodoa + " " + uria)
                kodea = erantzuna.status_code
                deskribapena = erantzuna.reason
                print(str(kodea) + " " + deskribapena)
                edukia = erantzuna.content

                soup2 = BeautifulSoup(edukia, 'html.parser')
                div_pdf = soup2.find('div', {'class': 'resourceworkaround'})
                pdf_link = div_pdf.a['href']
                pdf_izena = pdf_link.split('/')[-1]
                self._refs.append({'link': pdf_link, 'pdf_name': pdf_izena})

            progress += 1.5
            progress_var.set(progress)
            progress_bar.update()
            time.sleep(0.1)

        popup.destroy()
        return self._refs

    def get_pdf(self, selection):
        print("##### PDF-a deskargatzen... #####")
        metodoa = 'GET'
        uria = self._refs[selection]['link']
        print(uria)
        headers = {'Host': 'egela.ehu.eus','Cookie': self._cookiea}
        erantzuna = requests.get(uria, metodoa, headers=headers, allow_redirects=False)
        pdf_file = erantzuna.content
        pdf_name = self._refs[selection]['pdf_name']

        return pdf_name, pdf_file
