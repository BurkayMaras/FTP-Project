import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QTableWidget, QTableWidgetItem, QFileDialog,QMessageBox,QInputDialog;
from functions import FTPClient
import os
import sys

class FTPClientApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("FTP Client")
        self.resize(800, 600)

        self.delete_directory_button = QPushButton("Delete Directory", self)
        self.delete_directory_button.move(250, 120)
        self.delete_directory_button.clicked.connect(self.delete_directory)


        self.host_label = QLabel("Host:", self)
        self.host_label.move(20, 20)
        self.host_input = QLineEdit(self)
        self.host_input.move(120, 20)

        self.username_label = QLabel("Username:", self)
        self.username_label.move(20, 50)
        self.username_input = QLineEdit(self)
        self.username_input.move(120, 50)

        self.password_label = QLabel("Password:", self)
        self.password_label.move(20, 80)
        self.password_input = QLineEdit(self)
        self.password_input.move(120, 80)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.host_input.setText("ftp.dlptest.com")
        self.username_input.setText("dlpuser")
        self.password_input.setText("rNrKYTX9g7z3RgJRmxWuGHbeu")

        self.connect_button = QPushButton("Connect", self)
        self.connect_button.move(20, 120)
        self.connect_button.clicked.connect(self.connect_ftp)

        self.disconnect_button = QPushButton("Disconnect", self)
        self.disconnect_button.move(120, 120)
        self.disconnect_button.clicked.connect(self.disconnect_ftp)

        self.download_button = QPushButton("Download File", self)
        self.download_button.move(320, 160)
        self.download_button.clicked.connect(self.download_file)

        self.list_button = QPushButton("List Files", self)
        self.list_button.move(20, 160)
        self.list_button.clicked.connect(self.list_files)

        self.upload_button = QPushButton("Upload File", self)
        self.upload_button.move(120, 160)
        self.upload_button.clicked.connect(self.upload_file)

        self.rename_button = QPushButton("Rename File", self)
        self.rename_button.move(220, 160)
        self.rename_button.clicked.connect(self.rename_file)

        self.create_dir_button = QPushButton("Create Directory", self)
        self.create_dir_button.move(420, 160)
        self.create_dir_button.clicked.connect(self.create_directory)

        self.dir_name_input = QLineEdit(self)
        self.dir_name_input.move(420, 120)

        self.table = QTableWidget(self)
        self.table.setGeometry(20, 200, 600, 300)


    def connect_ftp(self):
        host = self.host_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        try:
            self.ftp_client = FTPClient(host, username, password)
            QMessageBox.information(self, "Success", "Connected to FTP server successfully")

            print("Connected to FTP server")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def disconnect_ftp(self):
        self.ftp_client.ftp_baglantiyi_kes()
        print("Disconnected from FTP server")

    def create_directory(self):
            directory_name = self.dir_name_input.text()
            if directory_name:
                try:
                    self.ftp_client.ftp_dizin_olustur(directory_name)
                    QMessageBox.information(self, "Success", f"Directory '{directory_name}' has been created successfully")
                except AttributeError:
                    QMessageBox.warning(self, "Warning", "Please connect to the FTP server first.")
            else:
                QMessageBox.warning(self, "Warning", "Please enter a directory name.")

    def download_file(self):
        selected_item = self.table.currentItem()  # Seçilen öğeyi al
        if selected_item:
            row = selected_item.row()  # Tıklanan satırın indeksini al
            column = selected_item.column()  # Tıklanan sütunun indeksini al

            # Sadece ilk sütun tıklandığında işlem yap
            if column == 0:
                # Dosya ismini al
                file_name = self.table.item(row, column).text().split()[-1]  # Dosya adını al
                print(file_name)

                # İndirme konumu seç
                local_dir = QFileDialog.getExistingDirectory(self, "Select Directory to Save File")

                # Dosya adı ve konumu geçerliyse dosyayı indir
                if local_dir:
                    try:
                        # Dosyayı indir
                        self.ftp_client.ftp_dosya_indir(file_name, local_dir)
                        QMessageBox.information(self, "Success", f"File '{file_name}' has been downloaded successfully")
                    except AttributeError:
                        QMessageBox.warning(self, "Warning", "Please connect to the FTP server first.")
                    except Exception as e:
                        QMessageBox.warning(self, "Warning", "Server üzerinde bu dosyada yetki olmadığı için dosya indirilemedi!")
        else:
            QMessageBox.warning(self, "Warning", "Please select a file to download.")


    def list_files(self):
        try:    
            files = self.ftp_client.ftp_dosyalari_listele()
            for i, file in enumerate(files):
                print(file+"\n")
            self.table.setRowCount(len(files))
            self.table.setColumnCount(1)
            self.table.setHorizontalHeaderLabels(["File Name"])  # Sütun başlığını ayarla
            for i, file in enumerate(files):
                self.table.setItem(i, 0, QTableWidgetItem(file))
                self.table.setColumnWidth(0, 500)  # İlk sütunun genişliğini ayarla
        except AttributeError:
            QMessageBox.warning(self, "Warning", "Please connect to the FTP server first.")


    def upload_file(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

            # Dosya seçme penceresini aç
            file_path, _ = QFileDialog.getOpenFileName(self, "Select File", current_dir, "All Files (*)")
            remote_dir = ''  # Uzak dizini belirtin (isteğe bağlı)

            # Dosya yolu yerine dosya adını al
            file_name = os.path.basename(file_path)

            print(file_name)

            # Dosya yükleme işlemi
            if file_name:
                self.ftp_client.ftp_dosya_yukle(file_path, remote_dir)
                print("Dosya yüklendi!")
        except AttributeError:
            QMessageBox.warning(self, "Warning", "Please connect to the FTP server first.")

    def rename_file(self):
        selected_item = self.table.currentItem()  # Seçilen öğeyi al
        if selected_item:
            row = selected_item.row()  # Tıklanan satırın indeksini al
            column = selected_item.column()  # Tıklanan sütunun indeksini al

            # Sadece ilk sütun tıklandığında işlem yap
            if column == 0:
                # Dosya ismini al
                old_name = self.table.item(row, column).text()
                file_name = old_name.split()[-1]
                print(file_name)

                # Yeni ismi al
                new_name, ok = QInputDialog.getText(self, "Enter New Name", "Enter the new name for the file:")
                print(new_name)
                if ok:
                    try:
                        # Dosya ismini değiştir
                        self.ftp_client.ftp_isim_degistir(file_name, new_name)
                        QMessageBox.information(self, "Success", f"File '{file_name}' has been renamed to '{new_name}'")
                        # Dosyaları yeniden listele
                        self.list_files()
                    except AttributeError:
                        QMessageBox.warning(self, "Warning", "Please connect to the FTP server first.")
        else:
            QMessageBox.warning(self, "Warning", "Please select a file to rename.")

    def delete_directory(self):
        selected_item = self.table.currentItem()  # Seçilen öğeyi al
        if selected_item:
            row = selected_item.row()  # Tıklanan satırın indeksini al
            column = selected_item.column()  # Tıklanan sütunun indeksini al

            if column == 0:
                directory_name = self.table.item(row, column).text().split()[-1]  # Dizin adını al

                try:
                    self.ftp_client.ftp_dizin_sil(directory_name)
                    QMessageBox.information(self, "Success", f"Directory '{directory_name}' has been deleted successfully")
                    self.list_files()  # Dosyaları yeniden listele
                except AttributeError:
                    QMessageBox.warning(self, "Warning", "Please connect to the FTP server first.")
                except Exception as e:
                    QMessageBox.warning(self, "Warning", "sadece klasörleri silmeye yetkiniz vardır!")
        else:
            QMessageBox.warning(self, "Warning", "Please select a directory to delete.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FTPClientApp()
    window.show()
    sys.exit(app.exec_())
