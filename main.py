import os
import sys
import pygame
import requests


def get_map():
    map_request = f"https://static-maps.yandex.ru/1.x/?ll={f'{coords[0]},{coords[1]}'}&l=map&z={z}"
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


coords = [37.622504, 55.753215]
z = 9
map_file = "map.png"

pygame.init()
get_map()
image = pygame.image.load(map_file)
screen = pygame.display.set_mode(image.get_size())
pygame.display.set_caption("Большая задача по Maps API")
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if z < 17:
                    z += 1
            if event.key == pygame.K_PAGEDOWN:
                if z > 1:
                    z -= 1
            if event.key == pygame.K_LEFT:
                coords[0] -= 0.001
            if event.key == pygame.K_RIGHT:
                coords[0] += 0.001
            if event.key == pygame.K_UP:
                coords[1] += 0.001
            if event.key == pygame.K_DOWN:
                coords[1] -= 0.001
    get_map()
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()
os.remove(map_file)
