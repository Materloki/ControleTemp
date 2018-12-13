# LM35 sensor de temperatura
import machine
from machine import ADC
import time
import math


pwm = machine.Pin(5)
fan = machine.PWM(pwm)	#definindo a fan como pino PWM
rele = machine.Pin(4, machine.Pin.OUT)		#pino de temperatura, sempre ativo
rele.value(1)
fan.freq(1000)			
adc = ADC(0)            #Define o ADC
def temp(value):            #Converte a tensão para temperatura
    return (value/3.1)
T = 0.2
Kp = 0.2
Ki = 0.009		#constantes do controle PI
acao_ant = 0  
erro_ant = 0		#acao e erros anteriores
s = 0
horario = time.localtime()
print(horario)
start = horario[2]
while horario[2] != start + 21:
    if horario[2] - start < 19:
        ref = 37.8
    else:
        ref = 36.8

    reading = adc.read()
    celsius_temp = temp(reading)
    erro = -(ref-celsius_temp)
    acao = acao_ant + (Kp*(erro - erro_ant)) + (Ki*T*erro);
    print (celsius_temp, " ", s)
    if acao > 0.8:		
    	acao = 0.8

    if acao < 0:
    	acao = 0

    s = math.trunc((acao + 0.2)*1023)
    fan.duty(s)

    erro_ant = erro
    acao_ant = acao
    horario = time.localtime()
    time.sleep_ms(500)
print("Ovo pronto ! (Ou galinha, sei lá)")