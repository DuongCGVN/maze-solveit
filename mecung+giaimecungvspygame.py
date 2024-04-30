import pygame as pg
import random,time

class Root():
    def __init__(giatribatbien, value, nhanhbome = None):
        giatribatbien.value = value
        giatribatbien.child = []
        giatribatbien.nhanhbome = nhanhbome

    def themnhanhcon(trucapbanthan, giatri):
        trucapbanthan.child.append(Root(giatri,trucapbanthan))
        return trucapbanthan.child[-1]

    def nhanhcon(self):
        return self.child

class taovagiaimecung():
    isMage = False
    diemketthuc = 399
    rows, cols = 20, 20
    def __init__(self, screen):
        self.screen = screen
        self.clock = pg.time.Clock()
        self.danhgiasudungsaikhicotheve()
        self.taomecung()
        self.isMage = True

    def danhgiasudungsaikhicotheve(self):
        self.start, self.end = None, None
        self.solveCan = None
        self.canvas = pg.Surface((402, 402))
        self.canvas.fill("#000000")
        for i in range(21):
            pg.draw.line(self.canvas, "#ffffff", (i * 20, 0), (i * 20, 400), 2)
            pg.draw.line(self.canvas, "#ffffff", (0, i*20), (400, i*20), 2)

    def veduongchinh(self):
        self.screen.fill("#200000")
        self.screen.blit(self.canvas, (0, 0))
        if self.solveCan is not None:
            self.screen.blit(self.solveCan, (0, 0))
        if self.start is not None:
            pg.draw.circle(self.screen, "#ffffff", ((self.start%self.cols) * 20 + 10, (self.start//self.cols) * 20 + 10)
                           , 5)
        if self.end is not None:
            pg.draw.rect(self.screen, "#ffffff", ((self.end % self.cols) * 20 + 5, (self.end // self.cols) * 20 + 5,
                                                 10, 10))
        pg.display.update()

    def chuongtrinhchinh(self):
        self.running = True
        while self.running:
            self.clock.tick(60)
            for eve in pg.event.get():
                if eve.type == pg.QUIT:
                    self.running = False
                if eve.type == pg.MOUSEBUTTONDOWN:
                    pos = self.ghinhotrucmecung(eve.pos[0], eve.pos[1])
                    if pos != -1:
                        if eve.button == 1:
                            if self.start == pos:
                                self.start = None
                            else:
                                self.start = pos
                            if self.start == self.end:
                                self.end = None
                        if eve.button == 3:
                            if self.end == pos:
                                self.end = None
                            else:
                                self.end = pos
                            if self.end == self.start:
                                self.start = None
                if eve.type == pg.KEYDOWN:
                    if eve.key == pg.K_SPACE:
                        self.danhgiasudungsaikhicotheve()
                        self.taomecung()
                        self.isMage = True
                    if eve.key == pg.K_RETURN:
                        if self.start is None or self.end is None:
                            self.danhgiasudungdankhigiai()
                        else:
                            self.timduong(self.start, self.end)
            self.veduongchinh()

    def ghinhotrucmecung(self, toadox, toadoy):
        col, row = toadox//20, toadoy//20
        if col >= self.cols or row >= self.rows:
            return -1
        else:
            return row * self.cols + col

    def timduong(self, start, end):
        if not self.isMage:
            return
        batdau = self.giaimecung(self.maze, start, "0")
        ketthuc = self.giaimecung(self.maze, end, "0")
        if batdau is False or ketthuc is False:
            return
        batdau = batdau.split("/")
        ketthuc = ketthuc.split("/")
        i = 0
        while (i < len(batdau) and i < len(ketthuc)) and batdau[i] == ketthuc[i]:
            i += 1
        path = []
        ii = len(batdau) - 1
        while ii >= i:
            path.append(batdau[ii])
            ii -= 1
        path.append(batdau[i-1])
        ii = i
        while ii < len(ketthuc):
            path.append(ketthuc[ii])
            ii += 1
        self.solveCan = pg.Surface((402, 402), pg.SRCALPHA)
        for ind in path:
            pg.draw.circle(self.solveCan, "#ffffff", ((int(ind)%20) * 20 + 10, (int(ind)//20) * 20 + 10), 3)
        for i in range(len(path)-1):
            s, e = int(path[i]), int(path[i+1])
            pg.draw.line(self.solveCan, "#ffffff", ((s%20) * 20 + 10, (s//20) * 20 + 10),
                         ((e%20) * 20 + 10, (e//20) * 20 + 10), 1)

    def bienthu(self, ind):
        toadochinhxac = []
        for i in (ind + 1, ind - 1):
            if i//20 == ind//20:
                toadochinhxac.append(i)
        for i in (ind + 20, ind - 20):
            if 0 <= i < 400:
                toadochinhxac.append(i)
        return toadochinhxac

    def taomecung(self):
        self.maze = Root(0)
        self.taotuongvoihinh(0, [], self.maze)

    def taotuongvoihinh(self, nhanhchinh, closed, dieukiendambaokhongngocut):
        closed.append(nhanhchinh)
        nhanhcon = self.bienthu(nhanhchinh)
        random.shuffle(nhanhcon)
        for child in nhanhcon:
            if child not in closed:
                row = nhanhchinh // 20
                col = nhanhchinh % 20
                if abs(nhanhchinh - child) == 1:
                    pg.draw.line(self.canvas, "#000000", ((col + 1 * (child > nhanhchinh)) * 20, row*20 + 2),
                                 ((col + 1 * (child>nhanhchinh)) * 20, (row+1)*20-1), 2)
                else:
                    pg.draw.line(self.canvas, "#000000", (col * 20 + 2, (row + 1 * (child > nhanhchinh)) * 20),
                                 ((col + 1) * 20 - 1, (row + 1 * (child > nhanhchinh)) * 20), 2)
                self.veduongchinh()
                pg.time.delay(10) 
                childTree = dieukiendambaokhongngocut.themnhanhcon(child)
                self.taotuongvoihinh(child, closed, childTree)

    def giaimecung(self, root, diemketthuc, path):
        if root.value == diemketthuc:
            return path
        nhanhcon = root.nhanhcon()
        for child in nhanhcon:
            toadochinhxacult = self.giaimecung(child, diemketthuc, path + f"/{child.value}")
            if toadochinhxacult is not False:
                return toadochinhxacult
        return False

    def danhgiasudungdankhigiai(self):
        if not self.isMage:
            return
        self.solveCan = pg.Surface((402, 402), pg.SRCALPHA)
        path = self.find_solution(self.maze, self.diemketthuc, "0")
        if path is False:
            return
        path = path.split("/")
        for ind in path:
            pg.draw.circle(self.solveCan, "#ffffff", ((int(ind)%20) * 20 + 10, (int(ind)//20) * 20 + 10), 3)
        for i in range(len(path)-1):
            s, e = int(path[i]), int(path[i+1])
            pg.draw.line(self.solveCan, "#ffffff", ((s%20) * 20 + 10, (s//20) * 20 + 10),
                         ((e%20) * 20 + 10, (e//20) * 20 + 10), 1)



pg.init()
screen = pg.display.set_mode((402, 402))
pg.display.set_caption("Dự án tạo và giải mê cung bản 2")
taovagiaimecung = taovagiaimecung(screen)
taovagiaimecung.chuongtrinhchinh()