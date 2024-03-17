import json
import time
import hashlib
import hmac
import base64
import uuid
import requests
import yeelight as yl 


class Api_Sw :
    def __init__(self,token,secret) -> None:
        self.apiHeader = {}
        self.token = token
        self.secret = secret 
    def bot_api (self):
        self.nonce = uuid.uuid4()
        self.t = int(round(time.time() * 1000))
        string_to_sign = '{}{}{}'.format(self.token,self.t, self.nonce)
        string_to_sign = bytes(string_to_sign, 'utf-8')
        self.secret = bytes(self.secret, 'utf-8')
        self.sign = base64.b64encode(hmac.new(self.secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())
        self.apiHeader['Authorization']=self.token
        self.apiHeader['Content-Type']='application/json'
        self.apiHeader['charset']='utf8'
        self.apiHeader['t']=str(self.t)
        self.apiHeader['sign']=str(self.sign, 'utf-8')
        self.apiHeader['nonce']=str(self.nonce)
        pass


class light_command:
    def __init__(self,ip=0) -> None:
        self.bulb = yl.Bulb(ip)
        self.check = False 
    def toggle_yl(self):
        self.bulb.toggle()
        pass
    def toggle_Sw(self,uid,headers):
        self.headers = headers 
        self.uid = str(uid)
        self.url = f'https://api.switch-bot.com/v1.1/devices/{self.uid}/commands'
        self.check = not self.check
        if self.check:
            self.data = {
                "command": "turnOff",
                "parameter": "default",
                "commandType": "command"
            }
        else: 
            self.data = {
                "command": "turnOn",
                "parameter": "default",
                "commandType": "command"
            }
        self.response = requests.post(url = self.url,headers =self.headers , json = self.data )
        if self.response.status_code == 200:
        # Printing the response content (JSON data in this case)
            print(self.response.json())
        else:
            print('Error:', self.response.status_code)



# if __name__ == '__main__':
#     token = 'a541fd31bcc965fe2a3bc0a202f2de67f71e12a62d32a6898a6fd22a73801209a73fd8d7eb3a396f71bebdd6f7762084' 
#     secret = 'a808a7702b8c287c32083ed183b88113'
#     Sw_api = Api_Sw(token = token ,secret = secret)
#     Sw_api.bot_api()
#     ip_yl_desk = '192.168.1.17'
#     ip_yl_bed = '192.168.1.37'
#     desk_lamp = light_command(ip = ip_yl_desk)
#     bed_lamp = light_command(ip = ip_yl_bed)
#     # desk_lamp.toggle_yl()
#     # bed_lamp.toggle_yl()
#     apiHeaders = Sw_api.apiHeader
#     uid = "EB0DF3A977A1"
#     celling_light = light_command()
#     celling_light.toggle_Sw(uid = uid,headers = apiHeaders )
    


    
