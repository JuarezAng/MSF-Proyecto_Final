"""
Proyecto final: Asma bronquial

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Juarez Salazar Angel Eduardo
Número de control: 22210417
Correo institucional: l22210417@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""

# Instalar librerías en consola si es necesario
# !pip install control
# !pip install slycot

import numpy as np
import math
import matplotlib.pyplot as plt
import control as ctrl

# Parámetros de simulación
x0, t0, tF, dt = 0, 0, 30, 1E-3
N = round((tF - t0) / dt) + 1
t = np.linspace(t0, tF, N)

# Entrada senoidal simulando el esfuerzo respiratorio
f = 0.2  # frecuencia en Hz
u = np.sin(2 * math.pi * f * t)

# Modelo fisiológico
def sys_model(Rv, L, Rt, C):
    num = [Rt, 0]
    den = [L * Rt * C, Rt + Rv, 1]
    return ctrl.tf(num, den)

# Parámetros:
# Paciente sano (referencia)
Rv_sano, L_sano, Rt_sano, C_sano = 5, 0.1, 2, 0.2

# Paciente con asma bronquial (mayor resistencia y menor compliance)
Rv_asma, L_asma, Rt_asma, C_asma = 5, 0.1, 12, 0.05

# Sistemas
sistema_sano = sys_model(Rv_sano, L_sano, Rt_sano, C_sano)
sistema_asma = sys_model(Rv_asma, L_asma, Rt_asma, C_asma)

# Controlador PID para el paciente asmático
Kp = 1382.64
Ki = 23796.16
Kd = 7.06
PID = ctrl.tf([Kd, Kp, Ki], [1, 0])

# Aplicar el PID al sistema con asma
sistema_asma_pid = ctrl.series(PID, sistema_asma)
sistema_asma_lazo_cerrado = ctrl.feedback(sistema_asma_pid, 1)



# Respuestas
t_out, resp_sano = ctrl.forced_response(sistema_sano, t, u, x0)
t_out, resp_asma = ctrl.forced_response(sistema_asma, t, u, x0)
t_out, resp_asma_pid = ctrl.forced_response(sistema_asma_lazo_cerrado, t, u, x0)


max_asma = np.max(np.abs(resp_asma))
max_asma_pid = np.max(np.abs(resp_asma_pid))
escala = max_asma / max_asma_pid
resp_asma_pid_escalada = resp_asma_pid * escala

# Gráficas
plt.figure(figsize=(10,5))
plt.plot(t_out, resp_sano, '-', color=[0.1, 0.5, 0.7], linewidth=2, label='Paciente sano')
plt.plot(t_out, resp_asma, '-', color=[1, 0, 0], linewidth=2, label='Asma bronquial (sin control)')
plt.plot(t_out, resp_asma_pid_escalada, '--', color=[0, 0.6, 0.2], linewidth=2, label='PID')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.xlim(0, 30)
plt.ylim(-1.5, 1.5)
plt.xlabel('t [s]')
plt.ylabel('V(t) [V]')
plt.title('Respuesta del sistema respiratorio: sano vs asma')
plt.legend()
plt.show()
