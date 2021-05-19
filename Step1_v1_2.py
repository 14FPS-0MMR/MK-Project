import os
import sys
import random
import numpy as np
import math
import time
from PyQt5 import QtGui
from PyQt5 import QtCore
from Equation import Expression
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QVBoxLayout, \
    QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QProgressBar, QMessageBox
from scipy.optimize import minimize
os.environ['QT_MAC_WANTS_LAYER'] = '1'

#sin(x1+x2^2)

def get_rand_number(min_value, max_value):
    range = max_value - min_value
    choice = random.uniform(0,1)
    return min_value + range*choice

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Лабораторная работа №1.'
        self.left = 10
        self.top = 50
        self.width = 1100
        self.height = 600
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        
        layout = QVBoxLayout()

        #  ----------- generator params ---------
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        
        self.label_start_data = QLabel("ИСХОДНЫЕ ДАННЫЕ", self)
        self.label_start_data.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        self.label_start_data.move(10,5)
        self.label_start_data.setFixedSize(250, 40)
        
        self.label_ur = QLabel("Уравнение", self)
        self.label_ur.setFont(QtGui.QFont("Arial", 11))
        self.label_ur.move(10,40)
        self.label_ur.setFixedSize(100, 20)
        
        self.equetion = QLineEdit("0.26*((x1)^2+(x2)^2)-0.48*x1*x2", self)
        self.equetion.setFont(QtGui.QFont("ARIAL", 10))
        self.equetion.move(110,40)
        self.equetion.setFixedSize(500, 20)
        
        
        
        self.label_per = QLabel("Переменные", self)
        self.label_per.setFont(QtGui.QFont("Arial", 11))
        self.label_per.move(10,65)
        self.label_per.setFixedSize(100, 20)
        
        self.variables = QLineEdit("x1,x2", self)
        self.variables.setFont(QtGui.QFont("ARIAL", 10))
        self.variables.move(110,65)
        self.variables.setFixedSize(500, 20)
        
        

        self.label_range = QLabel("Ограничения", self)
        self.label_range.setFont(QtGui.QFont("Arial", 11))
        self.label_range.move(10,90)
        self.label_range.setFixedSize(100, 20)
         
        self.ranges = QLineEdit("-10<x1<10,-10<x2<10", self)
        self.ranges.setFont(QtGui.QFont("Arial", 10))
        self.ranges.move(110,90)
        self.ranges.setFixedSize(500, 20)     
        
       
        
        
        
        # Блок интерфейса Монте-Карло
        
        self.label_MonteKarlo = QLabel("МОНТЕ-КАРЛО", self)
        self.label_MonteKarlo.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        self.label_MonteKarlo.move(125,160)
        self.label_MonteKarlo.setFixedSize(250, 40)  
        
      
        self.label_per = QLabel("Количество итераций", self)
        self.label_per.setFont(QtGui.QFont("Arial", 11))
        self.label_per.move(10,195)
        self.label_per.setFixedSize(200, 20)
        
        self.n = QLineEdit("1000", self)
        self.n.setFont(QtGui.QFont("Arial", 10))
        self.n.move(180,195)
        self.n.setFixedSize(100, 20)
        
        
        
        self.label_T_DOWN = QLabel("Параметр снижения температуры", self)
        self.label_T_DOWN.setFont(QtGui.QFont("Arial", 11))
        self.label_T_DOWN.move(550,220)
        self.label_T_DOWN.setFixedSize(250, 20)    
        
        
        
        

        #Поле вывода             
        self.label_ansv1 = QLabel("Результаты:", self)
        self.label_ansv1.setFont(QtGui.QFont("Arial", 11, QtGui.QFont.Bold))
        self.label_ansv1.move(10,352)
        self.label_ansv1.setFixedSize(100, 20)

        self.min = QLabel("Минимальное значение функции", self)
        self.min.setFont(QtGui.QFont("Arial", 10))
        self.min.move(10,370)
        self.min.setFixedSize(1000, 20)
        
        self.min11 = QLabel(self)
        self.min11.setFont(QtGui.QFont("Arial", 10))
        self.min11.move(210,370)
        self.min11.setFixedSize(1000, 20)
        
        self.vars = QLabel("Точки", self)
        self.vars.setFont(QtGui.QFont("Arial", 10))
        self.vars.move(10,390)
        self.vars.setFixedSize(1000, 20)
        
        self.vars11 = QLabel(self)
        self.vars11.setFont(QtGui.QFont("Arial", 10))
        self.vars11.move(50,390)
        self.vars11.setFixedSize(1200, 20)
                  
        self.time = QLabel("Время выполнения (секунды) ", self)
        self.time.setFont(QtGui.QFont("Arial", 10))
        self.time.move(10,410)
        self.time.setFixedSize(1000, 20)
        
        self.time11 = QLabel(self)
        self.time11.setFont(QtGui.QFont("Arial", 10))
        self.time11.move(195,410)
        self.time11.setFixedSize(1000, 20)
                      
      



        
        
        self.calculateButton = QPushButton("Расчёт", self)
        self.calculateButton.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        self.calculateButton.move(10,300)
        self.calculateButton.setFixedSize(350, 50)            
        self.calculateButton.clicked.connect(self.calculate)
        



#__________________________________________________________________________
#__________________________________________________________________________




        #Блок интерфейса Имитация Отжига
        
        

        self.label_OTZHIG = QLabel("ИМИТАЦИЯ ОТЖИГА", self)
        self.label_OTZHIG.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        self.label_OTZHIG.move(645,160)
        self.label_OTZHIG.setFixedSize(250, 40)
        
        
        self.label_temp = QLabel("Максимальная температура", self)
        self.label_temp.setFont(QtGui.QFont("Arial", 11))
        self.label_temp.move(550,195)
        self.label_temp.setFixedSize(200, 20)
        
        self.temperature = QLineEdit("100000", self)
        self.temperature.setFont(QtGui.QFont("Arial", 10))
        self.temperature.move(800,195)
        self.temperature.setFixedSize(100, 20)
                        
        self.label_T_DOWN = QLabel("Параметр снижения температуры", self)
        self.label_T_DOWN.setFont(QtGui.QFont("Arial", 11))
        self.label_T_DOWN.move(550,220)
        self.label_T_DOWN.setFixedSize(250, 20)        
        
        self.paramTemperature = QLineEdit("0.9", self)
        self.paramTemperature.setFont(QtGui.QFont("Arial", 10))
        self.paramTemperature.move(800,220)
        self.paramTemperature.setFixedSize(100, 20)        
        
        self.label_cycle_otzh = QLabel("Кол-во циклов", self)
        self.label_cycle_otzh.setFont(QtGui.QFont("Arial", 11))
        self.label_cycle_otzh.move(550,245)
        self.label_cycle_otzh.setFixedSize(200, 20)
        
        self.cycle = QLineEdit("70", self)
        self.cycle.setFont(QtGui.QFont("Arial", 10))
        self.cycle.move(800,245)
        self.cycle.setFixedSize(100, 20)

        self.label_eps_area = QLabel("Eps окрестность", self)
        self.label_eps_area.setFont(QtGui.QFont("Arial", 11))
        self.label_eps_area.move(550,270)
        self.label_eps_area.setFixedSize(200, 20)
                
        self.Eps = QLineEdit("0.01", self)
        self.Eps.setFont(QtGui.QFont("Arial", 10))
        self.Eps.move(800,270)
        self.Eps.setFixedSize(100, 20)
        
        
        
        
        
        
        
        
        
        #Поле вывода             
        self.label_ansv1 = QLabel("Результаты:", self)
        self.label_ansv1.setFont(QtGui.QFont("Arial", 11, QtGui.QFont.Bold))
        self.label_ansv1.move(550,352)
        self.label_ansv1.setFixedSize(100, 20)
        
        
        self.min2 = QLabel("Минимальное значение функции", self)
        self.min2.setFont(QtGui.QFont("Arial", 10))
        self.min2.move(550,410)
        self.min2.setFixedSize(1000, 20)
        
        self.min22 = QLabel(self)
        self.min22.setFont(QtGui.QFont("Arial", 10))
        self.min22.move(755,300)
        self.min22.setFixedSize(1200, 372)
               
        self.vars2 = QLabel("Точки", self)
        self.vars2.setFont(QtGui.QFont("Arial", 10))
        self.vars2.move(550,390)
        self.vars2.setFixedSize(1000, 20)
        
        self.vars22 = QLabel(self)
        self.vars22.setFont(QtGui.QFont("Arial", 10))
        self.vars22.move(590,390)
        self.vars22.setFixedSize(1200, 20)
                  
        self.time2 = QLabel("Время выполнения (секунды) ", self)
        self.time2.setFont(QtGui.QFont("Arial", 10))
        self.time2.move(550,370)
        self.time2.setFixedSize(1000, 20)
        
        self.time22 = QLabel(self)
        self.time22.setFont(QtGui.QFont("Arial", 10))
        self.time22.move(740,370)
        self.time22.setFixedSize(1000, 20)
        
        

        self.setCentralWidget(central_widget)
        self.calculateButton1 = QPushButton("Расчёт", self)
        self.calculateButton1.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        self.calculateButton1.move(550,300)
        self.calculateButton1.setFixedSize(350, 50)            
        self.calculateButton1.clicked.connect(self.calculate1)
        
        

        
        
        


        self.setCentralWidget(central_widget)
        self.reference2 = QPushButton('Справка', self)
        self.reference2.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        self.reference2.setToolTip('This is an example button')
        self.reference2.move(645,40)
        self.reference2.setFixedSize(165, 70)
        self.reference2.clicked.connect(self.reference1)
        self.statusBar()
        self.show()
        
    def reference1(self):
        print('evev')
        
        msgBox1 = QMessageBox()
        msgBox1.setText("Справка по вводу:\n\n Функции:\n abs()\n sin()\n cos()\n tan()\n sqrt()\n\n Константы:\n pi\n e\n\n Операторы:\n +\n -\n *\n /\n ^\n")
        msgBox1.exec_()
        

    def calculate(self):# Monte Karlo
        
        try:

            tic = time.perf_counter()
            variables = self.variables.text().split(',')
            fn = Expression(self.equetion.text(), variables)

            func_min = math.inf
            N = int(self.n.text())

            str_ranges=self.ranges.text().split(',')
            ranges = []
            for i in range(0, len(variables)):
                ranges.append({'min': int(str_ranges[i].split('<')[0]), 'max': int(str_ranges[i].split('<')[2])})
            for i in ranges:
                if (ranges[0]['min'] > ranges[0]['max'] or ranges[1]['min'] > ranges[1]['max']):
                    msgBox = QMessageBox()
                    msgBox.setText("Нижняя граница не может быть больше или равной верхней.")
                    msgBox.exec_()
                    raise ValueError

            results = []
            tmp_args1 = {}
            for i in range(1, N):
                tmp_args = {}
                for i, v in enumerate(variables):
                    tmp_args[v] = get_rand_number(min_value=ranges[i]['min'], max_value=ranges[i]['max'])
    
                tmp = fn(**tmp_args)
                if func_min > tmp:
                        func_min = tmp
                        tmp_args1 = tmp_args
    
                results.append(tmp)
    
            toc = time.perf_counter()
            timer = toc -tic
            
            
   
            self.min11.setText("=  {}".format(func_min))
            self.vars11.setText("=  {}".format(tmp_args1))
            self.time11.setText("=  {}".format(timer))
        except ValueError:
            msgBox1 = QMessageBox()
            msgBox1.setText("Ошибка ввода границ")
            msgBox1.exec_()
            
        except NameError:
            msgBox2 = QMessageBox()
            msgBox2.setText("Ошибка ввода функции или границ")
            msgBox2.exec_()
            
            
    def calculate1(self):  # Имитация отжига
        try:
            
            tic = time.perf_counter()
            t_max = float(self.temperature.text())
            if (t_max <= 0):
                msgBox = QMessageBox()
                msgBox.setText("Максимальная температура должна быть больше 0")
                msgBox.exec_()
                raise ValueError
                
            L = int(self.cycle.text())
            r = float(self.paramTemperature.text())
            if (r < 0 or r > 1):
                msgBox1 = QMessageBox()
                msgBox1.setText("Параметр снижения температуры должен лежать в интервале (0;1)")
                msgBox1.exec_()
                raise ValueError
            Eps = float(self.Eps.text())
            if (Eps <= 0 ):
                msgBox2 = QMessageBox()
                msgBox2.setText("Эпсилон окрестность должна быть больше 0")
                msgBox2.exec_()
                raise ValueError
            variables = self.variables.text().split(',')
            fn = Expression(self.equetion.text(), variables)
            
            ranges = []
            str_ranges=self.ranges.text().split(',')
            for i in range(0, len(variables)):
                ranges.append({'min': int(str_ranges[i].split('<')[0]), 'max': int(str_ranges[i].split('<')[2])})
            
            for i in ranges:
                if (ranges[0]['min'] > ranges[0]['max'] or ranges[1]['min'] > ranges[1]['max']):
                    msgBox3 = QMessageBox()
                    msgBox3.setText("Нижняя граница не может быть больше или равной верхней.")
                    msgBox3.exec_()
                    raise ValueError
                    
            for i in range(1, len(variables)):
                tmp_args = {}
                for i, v in enumerate(variables):
                    tmp_args[v] = get_rand_number(min_value=ranges[i]['min'], max_value=ranges[i]['max'])
            
            
                    
            func = fn(**tmp_args)
    
            x_eps1 = [tmp_args[i] for i in tmp_args]
    
            while (t_max > 0.00000001):
                for j in range(L): 
                    for i in range(0, len(variables)):
                        x_eps = [tmp_args[i]+random.uniform(0,1)*Eps-random.uniform(0,1)*Eps for i in tmp_args]
            
                        
                        
                    func_eps = fn(x_eps[0],x_eps[1])
                    df = func_eps - func               
                    if (df <= 0):
                        
                        x_eps1 = x_eps
                    elif (t_max > 0):
                        if (np.e**(-df/t_max) > random.uniform(0, 1)):
                         
                            x_eps1 = x_eps
                        
                
                t_max = r*t_max
                
            toc = time.perf_counter()
            timer = toc -tic
            
            
            res = []
            res = minimize(fn, x_eps1[0],x_eps1[1], method='nelder-mead', options={'xatol': 1e-8, 'disp': True})
            res1,res2,res3,res4,res5,res6,res7,res8 = res
            print(res1)
            
            self.min22.setText("=  {}".format(res))
            self.vars22.setText("=  {}".format(x_eps1))
            self.time22.setText("=  {}".format(timer))
            
        except ValueError:
            msgBox4 = QMessageBox()
            msgBox4.setText("Данные введены неверно")
            msgBox4.exec_()
            
        except NameError:
            msgBox4 = QMessageBox()
            msgBox4.setText("Ошибка ввода функции или границ")
            msgBox4.exec_()
            
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
    
    
    
    
    
    
    
    
    
    
