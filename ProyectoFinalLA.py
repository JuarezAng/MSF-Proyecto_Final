"""
Proyecto final: Fibrosis pulmonar

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Juarez Salazar Angel Eduardo
Número de control: 22210417
Correo institucional: l22210417@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import math
import matplotlib.pyplot as plt
import control as ctrl

x0, t0, tF, dt = 0, 0, 30, 1E-3
N = round((tF - t0) / dt) + 1
t = np.linspace(t0, tF, N)

f = 0.2  # frecuencia en Hz
u = np.sin(2 * math.pi * f * t)

def sys_model(Rv, L, Rt, C):
    num = [Rt, 0]
    den = [L * Rt * C, Rt + Rv, 1]
    sys = ctrl.tf(num, den)
    return sys

#Colores
color = [1,0,0]
color = [0.1,.5,.7]
color = [0.6,.2,.5]

Rv_ctrl, L_ctrl, Rt_ctrl, C_ctrl = 5, 0.1, 2, 0.2
Rv_caso, L_caso, Rt_caso, C_caso = 5, 0.1, 10, 0.05

sys_ctrl = sys_model(Rv_ctrl, L_ctrl, Rt_ctrl, C_ctrl)
sys_caso = sys_model(Rv_caso, L_caso, Rt_caso, C_caso)

t_out, resp_ctrl = ctrl.forced_response(sys_ctrl, t, u, x0)
t_out, resp_caso = ctrl.forced_response(sys_caso, t, u, x0) 

plt.figure(figsize=(10,5))
plt.plot(t_out, resp_ctrl, '-', color = [0.1,.5,.7], linewidth=2, label='Paciente sano')
plt.plot(t_out, resp_caso, '-', color = [1,0,0], linewidth=2, label='Asma bronquial')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.xlim(0, 30)
plt.ylim(-1.5, 1.5)
plt.xlabel('t[s]')
plt.ylabel('V(t)[V]')
plt.legend()
plt.show()
