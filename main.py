import pygame
import sys

from sprites.covered import Covered
from sprites.game import Game
from mapset import getmap
from sprites.counter import Counter

pygame.init()


# Константы/Constants
WIDTH = 10*70
HEIGHT = 10*70+70
FPS = 60

poss = [(100000, 100000)]
posd = [(100000, 100000)]

# Создание окна/Window creating
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mine sweeper")
clock = pygame.time.Clock()


def main():

    file = open('comm.txt', 'w')
    file.write('')
    file.close()

    file = open('info.txt', 'w')
    file.write('0')
    file.close()

    # Спрайты/Sprites
    covered = pygame.sprite.Group()
    blanks_covered = []
    gameover = Game('GAME OVER')
    win = Game('YOU WIN')
    counterlabel = Counter('123')

    mapa = getmap([])
    coords = []
    # setup
    counter = 0
    for y in range(0, HEIGHT, 70):
        for x in range(0, WIDTH, 70):
            counter+=1
            if x == 0:
                if y == 0:
                    coords.append(x)
                    coords.append(y+70)
                else:

                    coords.append(x)
                    coords.append(y+70)

            elif y == 0:
                coords.append(x)
                coords.append(y+70)
            else:
                coords.append(x)
                coords.append(y+70)

    # ASSIGN
    for line in range(10):
        for column in range(10):
            u = Covered(mapa[line][column])
            u.rect.x = coords[0]
            u.rect.y = coords[1]
            covered.add(u)
            del coords[0]
            del coords[0]

    # COORD:

    count = 0
    up = True

    while True:
        group = pygame.sprite.Group()
        count += 1

        prevx = 100000
        prevy = 100000
        trigg = False
        if count == 2:
            break
        else:
            for sprite in covered:
                if sprite.data == ' ':
                    if sprite.rect.x == prevx+70 and sprite.rect.y == prevy:
                        group.add(sprite)
                        trigg = True
                    elif sprite.rect.x == prevx and sprite.rect.y == prevy+70:
                        group.add(sprite)
                        trigg = True
                    else:
                        if sprite.rect.x == prevx and sprite.rect.y == prevy - 70:
                            group.add(sprite)
                            trigg = True
                        elif sprite.rect.x == prevx-70 and sprite.rect.y == prevy:
                            group.add(sprite)
                            trigg = True
                        else:
                            if not trigg:
                                if len(group) != 0:
                                    blanks_covered.append(group)
                                    group = pygame.sprite.Group()
                                prevx = sprite.rect.x
                                prevy = sprite.rect.y
                            else:
                                trigg = False
                                prevx = sprite.rect.x
                                prevy = sprite.rect.y
                    if not trigg:
                        if len(group) != 0:
                            blanks_covered.append(group)
                            group = pygame.sprite.Group()
                        prevx = sprite.rect.x
                        prevy = sprite.rect.y
                    else:
                        trigg = False
                        prevx = sprite.rect.x
                        prevy = sprite.rect.y
            blanks_covered.append(group)


    running = True
    while running:

        file = open('flags.txt')
        dt = file.read().split()
        file.close()

        if dt[0] == dt[1] or int(dt[0]) < int(dt[1]):
            up = False
            gameover.draw(screen)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                main()


        # Частота обновления экрана/Screen refresh rate
        clock.tick(FPS)

        # События/Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    poss.append(pygame.mouse.get_pos())
            keys = pygame.key.get_pressed()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    posd.append(pygame.mouse.get_pos())
        event_list = pygame.event.get()

        # Рендеринг/Rendering
        screen.fill((105, 105, 105))

        # Обновление спрайтов/Updating sprites

        if up:

            file = open('bombs.txt')
            txt = file.read()
            file.close()
            counterlabel.update(int(txt))

            for c in covered:
                c.update(poss[-1])
                if c.clicked == True:
                    poss.append((100000, 100000))


            for c in covered:
                c.upd(posd[-1])
                if c.clicked == True:
                    poss.append((100000, 100000))


            for c in covered:
                if c.data == ' ':
                    file = open('comm.txt')
                    data = file.read().split()
                    file.close()
                    trigg = False

                    for var in range(0, len(data), 2):
                        if int(data[var]) == c.rect.x:
                            if int(data[var+1]) == c.rect.y:
                                for group in blanks_covered:
                                    for sprite in group:
                                        if sprite == c:
                                            for sprite in group:
                                                sprite.image = pygame.image.load('assets/images/blanc.png')
                                                sprite.changed = True
                                            del blanks_covered[blanks_covered.index(group)]


                # if trigg:
                #     if c.left:
                #         for co in covered:
                #             if co.rect.x == c.rect.x-70:
                #                 co.clickvar = True
                #                 co.image = pygame.image.load('assets/images/blanc.png')
                #                 break
                #     if c.right:
                #         for co in covered:
                #             if co.rect.x == c.rect.x+70:
                #                 co.clickvar = True
                #                 co.image = pygame.image.load('assets/images/blanc.png')
                #                 break
                #     if c.up:
                #         for co in covered:
                #             print(c.rect.y, co.rect.y)
                #             if co.rect.y == c.rect.y+70:
                #                 co.clickvar = True
                #                 co.image = pygame.image.load('assets/images/blanc.png')
                #                 break
                #     if c.down:
                #         for co in covered:
                #             if co.rect.y == c.rect.y-70:
                #                 co.clickvar = True
                #                 co.image = pygame.image.load('assets/images/blanc.png')
                #                 break

        for f in covered:
            f.o()
        covered.draw(screen)
        counterlabel.draw(screen, 310, 0)

        for c in covered:
            if c.gameover == True:
                up = False
                gameover.draw(screen)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    main()

        results = []

        for c in covered:
            results.append(c.done)


        file = open('info.txt')
        if int(file.read()) == 100:
            up = False
            win.draw(screen)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                main()
        file.close()

        # Обновление экрана/Screen Refresh
        pygame.display.update()


if __name__ == "__main__":
    main()
