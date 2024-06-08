from ftplib import FTP
import os
#FTP ile ilgili bütün fonksiyonları bu sınıfta topladım, işlevleri ise test isimli sınıfta gerçekleştireceğim
#Fonksiyonların çalıştığının doğrulanması
class FTPClient:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.ftp = FTP()
        self.ftp.connect(self.host, 21)  # Burada FTP bağlantısını oluşturdum
        self.ftp.login(self.username, self.password)
    def ftp_dizin_olustur(self, directory):
        if directory not in self.ftp.nlst():
            self.ftp.mkd(directory)
            print(f"\n'{directory}' isimli klasör başarıyla oluşturuldu!\n")
        else:
            print(f"'{directory}' adında bir dizin zaten var.")

    def ftp_isim_degistir(self, old_name, new_name):
        self.ftp.rename(old_name, new_name)

    def ftp_dosyalari_listele(self, directory='.'):
        files = self.ftp.nlst(directory)
        return files

    def ftp_baglantiyi_kes(self):
        self.ftp.quit()

    def ftp_dosya_indir(self, remote_file, local_dir):
        with open(os.path.join(local_dir, os.path.basename(remote_file)), 'wb') as f:
            self.ftp.retrbinary('RETR ' + remote_file, f.write)

    def ftp_dosya_yukle(self, local_file, remote_dir):
        with open(local_file, 'rb') as f:
            self.ftp.cwd(remote_dir)
            self.ftp.storbinary('STOR ' + os.path.basename(local_file), f)
    def ftp_dizin_sil(self, directory):
            self.ftp.rmd(directory)
