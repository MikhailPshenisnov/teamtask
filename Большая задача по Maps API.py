import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit
import requests


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.API_KEY = "40d1649f-0493-4b70-98ba-98533de7710b"
        self.coords = [None, None]
        self.pt_coords = [None, None]
        self.z = 9
        self.map_file = "map.png"
        self.types = ["map", "sat", "sat,skl"]
        self.type = self.types[0]
        self.is_map = False
        self.initUi()

    def initUi(self):
        self.setGeometry(400, 400, 600, 450)
        self.setWindowTitle('Большая задача по Maps API')
        self.setFixedSize(self.size())
        self.map = QLabel("", self)
        self.map.setGeometry(0, 0, 600, 450)
        self.map.setPixmap(QPixmap(""))
        self.map_type_button = QPushButton("Сменить слой", self)
        self.map_type_button.setGeometry(10, 10, 100, 20)
        self.map_type_button.clicked.connect(self.change_map_type)
        self.search_line = QLineEdit("", self)
        self.search_line.setGeometry(120, 10, 360, 20)
        self.search_button = QPushButton("Найти", self)
        self.search_button.setGeometry(490, 10, 100, 20)
        self.search_button.clicked.connect(self.get_coords)

    def change_map_type(self):
        if self.is_map:
            if self.type == self.types[0]:
                self.type = self.types[1]
                self.map_file = "map.jpeg"
            elif self.type == self.types[1]:
                self.type = self.types[2]
                self.map_file = "map.jpeg"
            else:
                self.type = self.types[0]
                self.map_file = "map.png"
            self.map.setPixmap(self.get_map())

    def get_coords(self):
        self.coords = [None, None]
        self.pt_coords = [None, None]
        self.is_map = False
        self.type = self.types[0]
        self.z = 9
        self.map_file = "map.png"
        self.map.setPixmap(QPixmap(""))
        address = self.search_line.text()
        geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey={self.API_KEY}&geocode={address}&format=json"
        response = requests.get(geocoder_request)
        if response:
            json_response = response.json()
            if json_response["response"]["GeoObjectCollection"]["featureMember"]:
                toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                if toponym:
                    coords = [float(x) for x in toponym["Point"]["pos"].split()]
                    self.coords = coords.copy()
                    self.pt_coords = coords.copy()
                    self.is_map = True
                    self.map.setPixmap(self.get_map())

    def get_map(self):
        map_request = f"https://static-maps.yandex.ru/1.x/?ll={f'{self.coords[0]},{self.coords[1]}'}" \
                      f"&l={self.type}&z={self.z}&pt={self.pt_coords[0]},{self.pt_coords[1]},pm2rdm"
        response = requests.get(map_request)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        pixmap = QPixmap(self.map_file)
        os.remove(self.map_file)
        return QPixmap(pixmap)

    def keyPressEvent(self, event):
        if self.is_map:
            if event.key() == Qt.Key_PageUp:
                if self.z < 17:
                    self.z += 1
            if event.key() == Qt.Key_PageDown:
                if self.z > 0:
                    self.z -= 1
            # Стрелочки QT не хочет отрабатывать, пожтому WASD
            # Кнопки WASD работают только на английской раскладке
            if event.key() == Qt.Key_W:
                self.coords[1] += 0.001
            if event.key() == Qt.Key_S:
                self.coords[1] -= 0.001
            if event.key() == Qt.Key_A:
                self.coords[0] -= 0.001
            if event.key() == Qt.Key_D:
                self.coords[0] += 0.001
            self.map.setPixmap(self.get_map())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
