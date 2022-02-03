import sqlite3
import sys


from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from scoreboard import Ui_MainWindow

import pygame
from Level1 import Level


class Example(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.level_number = 1
        self.con = sqlite3.connect("game_db.sqlite")
        # Кнопки для оценок
        self.pushButton.clicked.connect(self.start_game)
        self.pushButton_2.clicked.connect(self.update_result)

    def start_game(self):
        self.name = self.lineEdit.text()

        level_map = [
            'XXXXXXXXXXXXXXXXXXXXXXX',
            'X         XXX         X',
            'X   C      E      C   X',
            'X  XXXX         XXXX  X',
            'X          C          X',
            'X         XXX       C X',
            'X        XXXXX        X',
            'X P                   X',
            'XXXX   XXX   XXX   XXXX',
            'X                     X',
            'X         XXX    C    X',
            'X    C     C    XXX   X',
            'X   XXX   XXX   XXX   X',
            'XXXXXXXXXXXXXXXXXXXXXXX'
        ]

        level_map_1 = [
            'XXXXXXXXXXXXXXXXXXXXXXX',
            'X         XXX         X',
            'X   C      E      C   X',
            'X  XXXX         XXXX  X',
            'X          C          X',
            'X         XXX       C X',
            'X        XXXXX        X',
            'X P                   X',
            'XXXX   XXX   XXX   XXXX',
            'X                     X',
            'X         XXX    C    X',
            'X    C     C    XXX   X',
            'X   XXX   XXX   XXX   X',
            'XXXXXXXXXXXXXXXXXXXXXXX'
        ]

        level_map_2 = [
            'XXXXXXXXXXXXXXXXXXXXXXX',
            'X         C         C X',
            'X         C           X',
            'X     XXXXXXXXXXX     X',
            'X     C               X',
            'X               C     X',
            'X     XXXXXXXXXXX     X',
            'X          C          X',
            'X                     X',
            'X     X    C    X     X',
            'X     X         X     X',
            'X     X    E    X     X',
            'X  P  X         X     X',
            'XXXXXXXXXXXXXXXXXXXXXXX'
        ]

        level_map_3 = [
            'XXXXXXXXXXXXXXXXXXXXXXX',
            'X                     X',
            'X                 E   X',
            'X    C          XXXX  X',
            'X   XXXX              X',
            'X                     X',
            'X          C          X',
            'X    C    XXX         X',
            'X   XXX          C    X',
            'X                     X',
            'X                C    X',
            'X    C     C    XXX   X',
            'X P XXX   XXX   XXX   X',
            'XXXXXXXXXXXXXXXXXXXXXXX'
        ]

        if self.buttonGroup.checkedButton().text() == "Уровень 1":
            level_map = level_map_1
            self.level_number = 1
        elif self.buttonGroup.checkedButton().text() == "Уровень 2":
            level_map = level_map_2
            self.level_number = 2
        elif self.buttonGroup.checkedButton().text() == "Уровень 3":
            level_map = level_map_3
            self.level_number = 3




        # игровой цикл



        title_size = 64
        screen_width = len(level_map[0]) * title_size
        screen_height = len(level_map) * title_size

        pygame.init()
        size = screen_width, screen_height
        screen = pygame.display.set_mode(size)
        clock = pygame.time.Clock()
        FPS = 60

        pygame.mixer.music.load('soundtrack.mp3')
        pygame.mixer.music.play(-1)

        level = Level(level_map, screen)

        all_sprites = pygame.sprite.Group()

        score = 0

        running = True
        while running:
            # внутри игрового цикла ещё один цикл
            # приема и обработки сообщений
            for event in pygame.event.get():
                # при закрытии окна
                if event.type == pygame.QUIT:
                    running = False

                # отрисовка и изменение свойств объектов
                # ...

                # обновление экрана
            screen.fill('navy')
            running, score = level.run()

            all_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)

        pygame.mixer.music.stop()
        pygame.quit()

        cur = self.con.cursor()

        result = cur.execute("SELECT name, score, level FROM scoreboard"
                             " WHERE name=? AND level=?",
                             (self.name, self.level_number)).fetchall()
        if not result:
            que = f"INSERT INTO scoreboard VALUES ('{self.name}', {score}, {self.level_number})"
        else:
            que = f"UPDATE scoreboard " \
                  f"SET score = {score}, " \
                  f"WHERE name = '{self.name}' AND level = {self.level_number}"

        cur.execute(que)
        self.con.commit()

    def update_result(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        # result = cur.execute("SELECT Gets.student_id, Gets.subject_id, Gets.Period, Gets.Assessment FROM Gets "
        #                      "JOIN Students ON Gets.student_id = Students.student_id"
        #                      " WHERE Students.Name=?",
        #                     (self.lineEditNameStudent.text(),)).fetchall()
        result = cur.execute("SELECT * FROM scoreboard").fetchall()

        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        # Если запись не нашлась, то не будем ничего делать
        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            return
        else:
            self.statusBar().showMessage('')
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
