import network
from time import sleep_ms
import thingspeak
import MLX90615
import statistics
from machine import deepsleep

SSID = ''
PSW = ''

MIN_TEMPERATURE_ACCEPTABLE = 3400   # (34.00 C)
MAX_TEMPERATURE_ACCEPTABLE = 4200   # (42.00 C)
TIME_MS_BETWEEN_TEMPERATURE_MEASUREMENTS = 500 # 0.5 s
NUM_TEMPERATURE_MEASUREMENTS = 8
# version free Thingspeak -> Message update interval limit = Every 15 seconds
TIME_MS_AFTER_TEMPERATURE_MEASUREMENTS = 20000   # 20 s;


sta = network.WLAN(mode=network.WLAN.STA)
sta.connect(SSID, auth=(None, PSW))

print("Conectando na rede {} ...".format(SSID),end="")
for x in range(20):
    if sta.isconnected():
        print("\nConectado em {}!".format(SSID))
        break
    print(".",end="")
    sleep_ms(1000)

if not sta.isconnected():
    print("\Não foi possível se conectar em {}".format(SSID))
else:
    ts = thingspeak.Thingspeak()
    ts.userApiKey = "3SOPC2X6DEHXW2JC"
    ts.mqttApiKey = "K7H9CQYEFCAVZG4F"
    ts.channel_id = "907427"
    ts.WriteApiKey = "O8MFP9ZJUDYTTMEJ"

    try:
        ts.openConnection()
        print("Conectado ao servidor ThingSpeak")
    except:
        print("Não foi possível se conectar ao ThingSpeak") 
        print("Verifique a conexão com a internet e também os dados do ThingSpeak") 
    
    # Algoritmo uPyBodyTempIR https://gitlab.com/rcolistete/computacaofisica-privado/-/tree/master/uPyBodyTempIR#vers%C3%A3o-sem-apds-9960
    print("mensagem de boas-vindas na tela com nome, versão e curta descrição do software")
    flag_exit = False
    numMedida = 0
    while(not flag_exit):
        tObject = 0         # Temperatura do objeto (humana)
        tAmbient = 0        # Temperatura do ambiente
        listTObject = []    # Lista de temperatura do objeto (humana)
        listTAmbient = []   # Lista de temperatura do ambiente
        meanTObjecto = 0    # Média da temperatura do objeto (humana)
        meanTAmbient = 0    # Média da temperatura do ambiente
        stadevTObjecto = 0  # Desvio padrão da temperatura do objeto (humana)
        stadevTAmbient = 0  # Desvio padrão da temperatura do ambiente (humana)
        measurements = 0    # Número de leituras de temperaturas válidas
        numMedida += 1      # Quantidade de vezes que pessoas mediram suas temperaturas

        print("\n-----------------------------------------------------------------------------------------------------------------------")
        print("Número da medida = {}".format(numMedida))
        print("mensagem curta com explicação para se aproximar a testa a 3 cm do sensor, mas sem tocar, ficar parado por tantos segundos")
        while(measurements < NUM_TEMPERATURE_MEASUREMENTS and not flag_exit):
            tObject, tAmbient = MLX90615.Read_MLX90615_Temperatures()
            sleep_ms(TIME_MS_BETWEEN_TEMPERATURE_MEASUREMENTS)
            if(MIN_TEMPERATURE_ACCEPTABLE <= tObject <= MAX_TEMPERATURE_ACCEPTABLE):
                measurements += 1
                listTObject.append(tObject)
                listTAmbient.append(tAmbient)
                
            print("Medindo, fique parado")
            
            # testa condição para habilitar flag_exit; ???
        if(measurements == NUM_TEMPERATURE_MEASUREMENTS):
            meanTObjecto = statistics.mean(listTObject) 
            meanTAmbient = statistics.mean(listTAmbient) 
            
            stadevTObjecto = statistics.pstdev(listTObject)
            stadevTAmbient = statistics.pstdev(listTAmbient)

            #if( (max(listTObject) < meanTObjecto+5) and (min(listTObject) > meanTObjecto-5)):
            if(stadevTObjecto > 5):
                print("Tente de novo, fique parado a 3 cm")
            else:
                print("Media da temperatura = {} °C".format(meanTObjecto / 100))
                print("Incerteza = {}".format(stadevTObjecto/100))
                if(meanTObjecto > 3750):
                    print("FEBRE! Procurar o sistema de saúde")
                
                # Enviar dados via IoT - Thingspeak
                ts.uploadData(meanTObjecto/100.0, stadevTObjecto, meanTAmbient/100.0, stadevTAmbient, numMedida)
            
            print("mensagem para se afastar do medidor, tal que a temperatura do objeto volte a ser próxima da temperatura ambiente")
            sleep_ms(TIME_MS_AFTER_TEMPERATURE_MEASUREMENTS)

            # testa condição para habilitar flag_exit ???

    ts.closeConnection()
    deepsleep(30)
    