from main import FTPClient
from ftplib import FTP
ftp_client = FTPClient("ftp.dlptest.com","dlpuser","rNrKYTX9g7z3RgJRmxWuGHbeu")
print("\nBağlantı kuruluyor\n")

#burada FTP sunucusunda ana dizinde bir klasör oluşturulmuştur.
ftp_client.ftp_dizin_olustur('burkay_test_directory6') #!not: eğer bu isimde bir dizin varsa hata verir, bu yüzden testlerin sağlıklı olması adına klasör adını değiştirip deneyebilirsiniz

print("\n\nAşağıdaki çıktıda dosyanın oluştuğu gözükmektedir:\n\n")

print(ftp_client.ftp_dosyalari_listele())  #dosyaları listeleyen fonksiyonu, sonuçların kontrol edilebilmesi için her fonksiyondan sonra çağırdım.


ftp_client.ftp_dosya_yukle('testKlasoru\\remote_fileburkay.txt','')  # Test klasörü dizinimdeki txt dosyasını FTP serverine yükledim.

ftp_client.ftp_dosya_indir('remote_fileburkay.txt', 'downloadedFromFtp')   #Ardından servera yüklediğim bu dosyayı, downloadedFromFtp klasörüme geri indirdim

print("\n\nremote_fileburkay.txt server üzerinde gözükmektedir: \n\n")

print(ftp_client.ftp_dosyalari_listele()) #servera yüklediğim remote file gözükmektedir.


ftp_client.ftp_isim_degistir("remote_fileburkay.txt","remotefileYeniismi.txt") #yüklemiş olduğum dosyanın ismini değiştirdim


print("\n\nYüklenen dosyanın ismi değiştirilmiş yeni liste:\n")

print(ftp_client.ftp_dosyalari_listele())

ftp_client.ftp_dizin_sil("burkay_test_directory6") #Dizin silme işlemi yaptığım fonksiyon

print("Oluşturulan Dizinin silindiği gözükmektedir: \n\n")
print(ftp_client.ftp_dosyalari_listele())

ftp_client.ftp_baglantiyi_kes()