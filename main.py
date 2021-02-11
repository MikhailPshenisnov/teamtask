import os
import sys
import pygame
import requests

coords = "37.622504,55.753215"
z = 9

map_request = f"https://static-maps.yandex.ru/1.x/?ll={coords}&l=map&z={z}"
response = requests.get(map_request)
if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)
pygame.init()
image = pygame.image.load(map_file)
screen = pygame.display.set_mode(image.get_size())
pygame.display.set_caption("Стадионы Москвы")
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()
os.remove(map_file)
