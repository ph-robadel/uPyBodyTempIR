from umqtt.simple import MQTTClient

class Thingspeak:
    def __init__(self):
        self.userApiKey = ""
        self.mqttApiKey = ""
        self.channel_id = ""
        self.WriteApiKey = ""
        self.client = MQTTClient("","","")
    
    def openConnection(self):
        self.client = MQTTClient(client_id = "umqtt_client", server = "mqtt.thingspeak.com", user =  self.userApiKey , password= self.mqttApiKey , ssl = False)
        self.client.connect()
    
    def closeConnection(self):
        self.client.disconnect()
    
    def uploadData(self, *data):
        topic = "channels/"+self.channel_id+"/publish/"+self.WriteApiKey
        
        pyload = ""
        for i,x in enumerate(data):
            pyload += "&field%d=%s" % (i+1,x)
        pyload = pyload[1:]
        
        self.client.publish(topic, pyload)
