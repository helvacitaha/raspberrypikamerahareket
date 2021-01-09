# Bu programı kullanmadan önce,
# (öneridir;) bunun için ayrı bir Gmail hesabı oluşturun.
# Raspberrynizden bu hesaba giriş yapın.
# Profil resminize tıklayıp "google hesabı" bölümüne girin
# "bağlı uygulama ve siteler" sekmesine girin
# "daha az güvenli uygulamalara izin ver" seçeneğine tıklayarak aktif hale getirin.
# Hareket sensörünü GPIO 17 (11. pin) pinine bağlayın

import os
import glob
import picamera
import RPi.GPIO as GPIO
import smtplib
from time import sleep

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

gonderici = 'ornekhesap1@gmail.com'
sifre = 'ornek1234'
alici = 'ornekhesap2@gmail.com'

DIR = './Database/'
FILE_PREFIX = 'resim'
            
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)

def send_mail():
    print 'Mail Gonderiliyor'
    if not os.path.exists(DIR):
        os.makedirs(DIR)
    files = sorted(glob.glob(os.path.join(DIR, FILE_PREFIX + '[0-9][0-9][0-9].jpg')))
    sayi = 0
    
    if len(files) > 0:
        sayi = int(files[-1][-7:-4])+1
    filename = os.path.join(DIR, FILE_PREFIX + '%03d.jpg' % sayi)
    with picamera.PiCamera() as camera:
        pic = camera.capture(filename)
    msg = MIMEMultipart()
    msg['From'] = gonderici
    msg['To'] = alici
    msg['Subject'] = 'Hareket algılandı'
    
    body = 'Picture is Attached.'
    msg.attach(MIMEText(body, 'plain'))
    attachment = open(filename, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename= %s' % filename)
    msg.attach(part)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gonderici, sifre)
    text = msg.as_string()
    server.sendmail(gonderici, alici, text)
    server.quit()

while True:
    deger = GPIO.input(11)
    if deger == 0:
        print "No intruders", i
        sleep(0.3)
    elif deger == 1:
        print "Intruder detected", i
        send_mail()