import pyxel,math,random

class Jeu:
    def __init__(self):
        """
Ce jeu consiste a faire avancer le joueur vers l'arrivée en traversant les obstacles.
Pour cela, il faut cliquer avec la souris sur un mur ou plafond pour faire bouger le joueur comme s'il s'accrochait a une liane. Plus le joueur appuie longtemps sur la souris, plus il pourra s’approcher du point clique et plus il pourra partir loin.Il peut egalement se deplacer avec les touches a et d.
Il existe certains sols fait de lave, si le joueur le touche il meurt, l'environnement est également un espace toxique rempli de gaz, au bout d'un certain temps si le joueur n'arrive pas a reprendre de l'air, il meurt par intoxication et doit repartir du départ.

"""

        pyxel.init(128, 128, title="Nuit du c0de 2022")
        self.mini_init()
        self.lava = [[266,110,85,10],[391,110,300,10],[731,110,74,10],[835,110,100,10],[965,110,300,10],[1285,110,280,10]]
        self.obj = [[0,0,100,120],[0,120,1610,8],[205,30,10,5],[215,70,16,60],[226,90,40,30],[311,40,5,5],[351,90,40,30],[446,20,10,10],[536,20,10,10],[626,20,10,10],[691,110,40,10],[765,50,10,2],[765,20,10,2],[805,60,30,80],[865,40,10,2],[915,30,20,5],[935,60,30,60],[985,20,10,5],[1015,110,10,2],[1055,40,10,5],[1095,110,10,2],[1135,40,10,5],[1175,110,10,2],[1235,0,10,5],[1265,20,20,100],[1300,30,10,5],[1325,60,10,5],[1361,90,10,5],[1390,50,10,5],[1450,20,10,5],[1480,45,10,5],[1520,100,10,5],[1545,30,10,5],[1565,0,10,50],[1565,70,10,50]]
        pyxel.run(self.update, self.draw)
        
    def mini_init(self):
        self.heal = [[371,85,5,5],[1275,15,5,5],[820,55,5,5]]
        self.vie = 20
        self.goal = False
        self.p_y = 116
        self.p_x = 155
        self.gtime = 10
        self.memx = 0
        self.memy = 0
        self.gravi = 0
        self.mx = 155
        self.wx = 0
        self.wy =0
        self.time = 0
        self.charge = 0
        self.count = 0
        self.direction = 2
        self.yfin = 0
        self.jump = [False,0,0]
        self.wayer = False
        self.line = False
        self.gaz = []
        pyxel.load("jeu.pyxres")
        
    def gravite(self):
        if not self.col_sol():
            self.gtime += 1
        else:
            self.gtime = 10
            self.gravi = 0
            
        if self.gtime != 10:
            self.p_y += self.gravi
            self.gravi = self.gtime//10
            
    def col_heal(self):
        for i in self.heal:
            if i[0]-4 <= self.p_x <= i[0]+i[2] and i[1] <= self.p_y <= i[1]+i[3]:
                self.vie += 15
                self.heal.remove(i)
                   
    def col_pla(self):
        for i in self.obj:
            if i[0]-4 <= self.p_x <= i[0]+i[2] and i[1] <= self.p_y-1 <= i[1]+i[3]:
                self.p_y = i[1]+i[3]+1
                return True
        return False
    
    def col_sol(self):
        for i in self.obj:
            if i[0]-4 <= self.p_x <= i[0]+i[2] and i[1] <= self.p_y+4 <= i[1]+5:
                self.p_y = i[1]-4
                return True
        return False
    
    def col_mur(self,j):
        for i in self.obj:
            if i[0] <= self.p_x+j <= i[0]+i[2] and i[1] <= self.p_y <= i[1]+i[3]:
                if j == 0:
                    self.p_x = i[0]+i[2]
                else:
                    self.p_x = i[0]-4
                return True
        return False
    
    def col_mouse(self):
        for i in self.obj:
            if i[0] <= pyxel.mouse_x+self.mx <= i[0]+i[2] and i[1] <= pyxel.mouse_y <= i[1]+i[3]:
                return True
        return False
    
    def col_lava(self):
        for i in self.lava:
            if i[0] <= self.p_x <= i[0]+i[2] and i[1] <= self.p_y <= i[1]+i[3]:
                return True
        return False 
    
    def update(self):
        self.col_heal()
        self.time += 1
        if self.time%30 == 0:
            self.vie -= 1
        if self.col_lava() or self.vie == 0:
            self.mini_init()
        if self.p_x > 1600:
            self.goal = True
            
        if self.wayer:
            if self.charge != 0 and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and self.count < 15:
                self.p_x += self.memx
                self.p_y += self.memy
                self.count += 1
                self.yfin = self.p_y
                self.line = True
            elif not self.jump[0]:
                self.charge = 0
                self.count = 0
                d = pyxel.sqrt((self.wx-self.p_x-2)**2 + (self.wy-self.p_y-2)**2)
                self.p_x += self.direction
                if (self.p_x+2-self.wx)/d > 1 or (self.p_x+2-self.wx)/d < -1:
                    self.jump = [True,0,self.p_y]
                    self.line = False
                else:
                    self.p_y = math.cos(math.asin((self.p_x+2-self.wx)/d))*d+self.wy-2
                
                if self.p_y < self.yfin:
                    self.jump = [True,0,self.p_y]
                    self.line = False
                    
            elif self.jump[0] and self.jump[1]<20:
                self.p_x += self.direction//2
                self.jump[1] += 1
                x = self.jump[1]
                self.p_y = self.jump[2]-(-0.1*x**2+2*x)
                
            else:
                self.jump[0] = False 
                self.gtime = 10 
                self.wayer = False
                


            if self.col_mur(4) or self.col_mur(0) or self.col_sol() or self.col_pla():
                self.gtime = 10
                self.line = False
                self.wayer = False
                
        else:
            if pyxel.btn(pyxel.KEY_D):
                if not self.col_mur(4):
                    self.p_x += 1
                for g in self.gaz:
                    g[0]+=1

            if pyxel.btn(pyxel.KEY_A):
                if not self.col_mur(0):
                    self.p_x +=-1
                for g in self.gaz:
                    g[0]+=-1

            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and self.col_mouse() and pyxel.mouse_y < self.p_y:
                self.charge = 1
                self.wx = pyxel.mouse_x+self.mx
                self.wy = pyxel.mouse_y
                if self.p_x+2 > self.wx:
                    self.direction = -2
                else:
                    self.direction = 2
                self.memx = (self.wx - self.p_x)//20
                self.memy = (self.wy - self.p_y)//20
                self.wayer = True
            self.gravite()
            
        self.update_gaz()    
        self.mx = self.p_x-60
        pyxel.camera(self.p_x-60, 0)
        
        
    def update_gaz(self):
        for i in range(5):
            self.gaz.append([128+self.p_x,random.randint(0,128),random.choice([1,2])])
        for g in self.gaz:
            g[0]-=g[2]
            if g[0]<self.p_x-60:
                self.gaz.remove(g)

    
    def draw(self):
        pyxel.cls(0)
        pyxel.rect(self.p_x,self.p_y//1,4,4,7)
        for i in self.obj:
            pyxel.rect(i[0],i[1],i[2],i[3],13)
        for i in self.lava:
            pyxel.rect(i[0],i[1],i[2],i[3],8)
        pyxel.rect(pyxel.mouse_x+self.mx-4, pyxel.mouse_y,8,1,2)
        pyxel.rect(pyxel.mouse_x+self.mx, pyxel.mouse_y-4,1,8,2)
        pyxel.circb(pyxel.mouse_x+self.mx, pyxel.mouse_y,4,2)
        
        if self.line:
            pyxel.line(self.p_x+2,self.p_y+2, self.wx, self.wy,10)
            d = pyxel.sqrt((self.wx-self.p_x-2)**2 + (self.wy-self.p_y-2)**2)
        pyxel.rect(self.p_x-57,2,self.vie,2,14)
        for q in self.heal:
            pyxel.blt(q[0],q[1],0,0,0,8,8)
        for g in self.gaz:
            pyxel.rect(g[0],g[1],g[2],g[2], random.choice([2,11]))
        if self.goal == True:
            pyxel.cls(7)
            pyxel.text(1600,60,'GOAL',8)
            

            

        
        
Jeu()