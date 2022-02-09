# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 16:59:02 2021

@author: Maho
"""


#---------------------------------------------------------#
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from derstakipUI import *


#-----------------------------------------------------------#

Uygulama=QApplication(sys.argv)
AnaPencere=QMainWindow()
ui=Ui_MainWindow()
ui.setupUi(AnaPencere)
AnaPencere.show()



#----------------------VERİTABANI OLUŞTUR-----------------#
#---------------------------------------------------------#
import sqlite3
global curs        # Global değişken
global conn        # Global değişken

conn=sqlite3.connect('20300031602.db')
curs=conn.cursor()
ogrtable=("CREATE TABLE IF NOT EXISTS yildirim(                  \
                 Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
                 OkulNo TEXT NOT NULL UNIQUE,                     \
                 Adi TEXT NOT NULL,                             \
                 Soyadi TEXT NOT NULL,                          \
                 Ders TEXT NOT NULL,                            \
                 Telefon TEXT NOT NULL,                         \
                 Devam  Text NOT NULL,                                             \
                 Adres TEXT NOT NULL)")

curs.execute(ogrtable)
conn.commit() 


#----------------------KAYDET-----------------------------#
#---------------------------------------------------------#

def temizle():    
    ui.LnaOkulno.clear()
    ui.LnaAdi.clear()
    ui.LnaSoyadi.clear()
    ui.LnaTelefonu.clear()
    ui.LnaAdres.clear()
    ui.CmbDers.setCurrentIndex(-1)


def Kaydet():
    OKULNO=ui.LnaOkulno.text()
    AD=ui.LnaAdi.text()
    Soyad=ui.LnaSoyadi.text()
    DERS=ui.CmbDers.currentText()
    TLF=ui.LnaTelefonu.text()
    Adres=ui.LnaAdres.text()
    
    if ui.ChkBoxDevam.isChecked():
        Devamdurumu="Devam Edildi"
    else:
        Devamdurumu="Devam Edilmedi"
    
        
            
    curs.execute("INSERT INTO yildirim \
                     (OkulNo,Adi,Soyadi,Ders,Telefon,Devam,Adres) \
                      VALUES (?,?,?,?,?,?,?)", \
                      (OKULNO,AD,Soyad,DERS,TLF,Devamdurumu,Adres))
    conn.commit()
    ui.statusbar.showMessage("KAYIT EKLEME İŞLEMİ GERÇEKLEŞTİ...")
    Listele()

#---------------------------------------------------------#  
def Listele():
    
    ui.TblWiBilgiler.clear()
    
    ui.TblWiBilgiler.setHorizontalHeaderLabels(('Kayıt No','Okul No','Öğrenci Adı','Öğrenci Soyadı', \
                                                  'Ders', 'Telefonu','Devam Durumu' ,'Adresi'))
    
    ui.TblWiBilgiler.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    curs.execute("SELECT * FROM yildirim")
    
    for satirIndeks, satirVeri in enumerate(curs):
        for sutunIndeks, sutunVeri in enumerate (satirVeri):
            ui.TblWiBilgiler.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))

    temizle()



#---------------------------------------------------------#
def Doldur():
    secili=ui.TblWiBilgiler.selectedItems()
    ui.LnaOkulno.setText(secili[1].text())
    ui.LnaAdi.setText(secili[2].text())
    ui.LnaSoyadi.setText(secili[3].text())
    ui.CmbDers.setCurrentText(secili[4].text())
    ui.LnaTelefonu.setText(secili[5].text())
    ui.LnaAdres.setText(secili[6].text())    
    
    if secili[7].text()=="Evli":
        ui.ChkBoxDevam.setChecked(True)
    else:
        ui.ChkBoxDevam.setChecked(False)
        
        
        
        #-------------------- Kayıt Düzeltme ------------------------# 
def Duzeltme():
    cevap=QMessageBox.question(AnaPencere,"KAYIT DÜZELTME","Kaydı güncellemek istediğinize emin misiniz?",\
                         QMessageBox.Yes | QMessageBox.No)
    if cevap==QMessageBox.Yes:
        try:
            secili=ui.TblWiBilgiler.selectedItems()
            Id=int(secili[0].text())
            OKULNO=ui.LnaOkulno.text()
            AD=ui.LnaAdi.text()
            Soyad=ui.LnaSoyadi.text()
            TLF=ui.LnaTelefonu.text()
            DERS=ui.CmbDers.currentText()
 
            if ui.ChkBoxDevam.isChecked():
                Devamdurumu="Devam Edildi"
            else:
                Devamdurumu="Devam Edilmedi"
            Adres=ui.LnaAdres.text()
            
            
            

            curs.execute("UPDATE yildirim SET OkulNo=?, Adi=?, Soyadi=?,Ders=?,Telefon=?,Devam=?,Adres=? WHERE Id=?", \
                         (OKULNO,AD,Soyad,DERS,TLF,Devamdurumu,Adres,Id))
            conn.commit()
            
            Listele()
            
        except Exception as Hata:
            ui.statusbar.showMessage("Şöyle bir hata meydana geldi = "+str(Hata))
    else:
        ui.statusbar.showMessage("Güncellme iptal edildi")
    
    
    #-------------------- Kayıt arama ------------------------# 
def Arama():
    ara1=ui.LnaOkulno.text()
    ara2=ui.LnaAdi.text()
    ara3=ui.LnaSoyadi.text()
    curs.execute("SELECT * FROM yildirim WHERE OkulNo=? OR Adi=? OR Soyadi=? OR (Adi=? AND Soyadi=?)",  \
                 (ara1,ara2,ara3,ara2,ara3))
    conn.commit()
    ui.TblWiBilgiler.clear()
    for satirIndeks, satirVeri in enumerate(curs):
        for sutunIndeks, sutunVeri in enumerate (satirVeri):
            ui.TblWiBilgiler.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))
    
    
    
    
    #-------------------- Kayıt Silme ------------------------# 
def Silme():
    cevap=QMessageBox.question(AnaPencere,"KAYIT SİL","Kaydı silmek istediğinize emin misiniz?",\
                         QMessageBox.Yes | QMessageBox.No)
    if cevap==QMessageBox.Yes:
        secili=ui.TblWiBilgiler.selectedItems()
        silinecek=secili[1].text()
        try:
            curs.execute("DELETE FROM yildirim WHERE OkulNo='%s'" %(silinecek))
            conn.commit()
            
            Listele()
            
            ui.statusbar.showMessage("KAYIT SİLME İŞLEMİ BAŞARIYLA GERÇEKLEŞTİ...",10000)
        except Exception as Hata:
            ui.statusbar.showMessage("Şöyle bir hata ile karşılaşıldı:"+str(Hata))
    else:
        ui.statusbar.showMessage("Silme işlemi iptal edildi...",10000)
        
        
        
 
#----------------------ÇIKIŞ-----------------------------#
#---------------------------------------------------------#  
def CIKIS():
    cevap=QMessageBox.question(AnaPencere,"ÇIKIŞ","Programdan çıkmak istediğinize emin misiniz?",QMessageBox.Yes | QMessageBox.No)
    if cevap==QMessageBox.Yes:
        sys.exit(Uygulama.exec_())
        conn.close()
    else:
        AnaPencere.show()
        ui.statusbar.showMessage("Çıkış iptal edildi...",10000)
        
        

# ---------------------------------------------------------#
ui.BtnKaydet.clicked.connect(Kaydet)
ui.BtnListele.clicked.connect(Listele)
ui.BtnSil.clicked.connect(Silme)
ui.BtnAra.clicked.connect(Arama)
ui.BtnGuncelle.clicked.connect(Duzeltme)
ui.TblWiBilgiler.itemSelectionChanged.connect(Doldur)
ui.BtnCikis.clicked.connect(CIKIS)


sys.exit(Uygulama.exec_())