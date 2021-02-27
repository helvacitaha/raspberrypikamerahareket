# Bu programı kullanmadan önce,
# (öneridir;) bunun için ayrı bir Gmail hesabı oluşturun.
# Raspberrynizden bu hesaba giriş yapın.
# Profil resminize tıklayıp "google hesabı" bölümüne girin
# "bağlı uygulama ve siteler" sekmesine girin
# "daha az güvenli uygulamalara izin ver" seçeneğine tıklayarak aktif hale getirin.
# Hareket sensörünü GPIO 17 (11. pin) pinine bağlayın

import os # İşletim sistemi ile ilgili olan kütüphane
import glob # Dosya yonetimi icin kutuphane
import picamera # Raspberry Pi kamerası ile ilgili kütüphane
import RPi.GPIO as GPIO # GPIO pinlerini kullanmak için olan kütüphane
import smtplib # E-mail kütüphanesi
from time import sleep #"sleep" komutunun kütüphanesi

# E-mail kütüphaneleri
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

gonderici = 'raspberrypiemailhesap@gmail.com' # gonderen email hesabi
sifre = 'ornekornek1234' # hesabin sifresi
alici = 'tahahelvaciogluethernet@hotmail.com' # 1. alici email adresi
alici2 = 'helvacitaha1337@gmail.com' # 2. alici email adresi
dosyayeri = './Database/.' # Resimleri kaydettigimiz klasor olacak
dosyafix = 'resim'

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # GPIO pinlerinin numaralarinin belirtilme seklini pinlerin sayisina gore ayarliyoruz.
GPIO.setup(11,GPIO.IN) # 11. pini giris pini olarak ayarliyoruz. (pinMode(11,INPUT);)

def mailgonder(): # Mail gonderme fonksiyonu tanimliyoruz
    print ("Mail gonderiliyor") # Maili gonderdigine dair terminale yazi yaziyor. Test icindir.
    if not os.path.exists(dosyayeri): # Eger "dosyayeri" degiskeninde belirttigimiz dosya adinda bir dosya yoksa
        os.makedirs(dosyayeri) # O isimde bir dosya olustur
    dosyalar = sorted(glob.glob(os.path.join(dosyayeri, dosyafix + '[0-9][0-9][0-9].jpg')))
    sayi = 0
    if len(dosyalar)<0:
        sayi = int(dosyalar[-1][-7:-4])+1
        dosyaisim = os.path.join(dosyayeri,dosyafix+'%03d.jpg'%sayi)
    with picamera.PiCamera() as kamera
        resim = kamera.capture(dosyaisim) # Kamerayla fotograf cekip "dosyaisim" degiskeninin icerigi isminde bir dosya olustur.
    mesaj = MIMEMultipart()
    mesaj['From']=gonderici
    mesaj['To']=alici
    mesaj['Subject']='Hareket Algılandı'
    body='Resim eklendi'
    mesaj.attach(MIMEText(body, 'plain'))
    resimdosyasi = open(dosyaisim, 'rb')
    bolum = MIMEBase('application', 'octet-stream')
    bolum.set_payload((resimdosyasi).read())
    encoders.encode_base64(bolum)
    bolum.add_header('Content-Disposition', 'resimdosyasi; dosyaisim= %s' % dosyaisim)
    mesaj.attach(bolum)
    sunucu = smtplib.SMTP('smtp.gmail.com', 587)
    sunucu.starttls()
    sunucu.login(gonderici, sifre)
    yazi = mesaj.as_string()
    sunucu.sendmail(gonderici, alici, yazi)
    sunucu.quit()
    
    mesaj2 = MIMEMultipart()
    mesaj2['From']=gonderici
    mesaj2['To']=alici2
    mesaj2['Subject']='Hareket Algılandı'
    body2='Resim eklendi'
    mesaj2.attach(MIMEText(body2, 'plain'))
    resimdosyasi2 = open(dosyaisim, 'rb')
    bolum2 = MIMEBase('application', 'octet-stream')
    bolum2.set_payload((resimdosyasi).read())
    encoders.encode_base64(bolum2)
    bolum2.add_header('Content-Disposition', 'resimdosyasi; dosyaisim= %s' % dosyaisim)
    mesaj2.attach(bolum2)
    sunucu = smtplib.SMTP('smtp.gmail.com', 587)
    sunucu.starttls()
    sunucu.login(gonderici, sifre)
    yazi2 = mesaj2.as_string()
    sunucu.sendmail(gonderici, alici2, yazi2)
    sunucu.quit()
    
while True: # Sonsuz dongu
    n = GPIO.input(11) # "n" degiskeni olusturup 11. GPIO pininden aldigimiz pini icerisine at.
    if n == 1: # Eger n 1e esit ise,
        print ("Mail gonderiliyor")
        mailgonder() # Mail gonder
    elif i == 0: # Eger n 0a esitse, 
        print ("Hareket algilanmadi.")
        sleep(0.3) # 0.3 saniye bekle
