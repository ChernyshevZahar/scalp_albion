from datetime import date
import scapy.all as scapy
import requests
import json


"""
Поргамма для парсинга сетевого трафика в приложение и отправка данных в базу

"""



id_pacet_send = ''

arr_str = ''



# Рабоат с апи


def loginapi(login,password):
    token1 = json.loads(requests.post(url='http://cherny3v.beget.tech/api/auth_token/token/login/',json={'username': login,'password': password  }).text)["auth_token"] 
    return token1

def logout(token1):
    respons = requests.post(url='http://cherny3v.beget.tech/api/auth_token/token/logout/',headers={'Authorization':'Token ' + token1})
    return respons

def AddData(token1, data):
    respons = requests.post(url='http://cherny3v.beget.tech/api/add',headers={'Authorization':'Token ' + token1}, json=data)
    logout(token1)
    return respons

def CheakTop(token1,resurs):
    respons = requests.get(url=f'http://cherny3v.beget.tech/api/top/{resurs}',headers={'Authorization':'Token ' + token1})
    logout(token1)
    return respons

def SendTop(token1,data):
    respons = requests.post(url='http://cherny3v.beget.tech/api/top',headers={'Authorization':'Token ' + token1}, json=data)
    logout(token1)
    return respons

def ChengeTop(token1,data,id):
    respons = requests.patch(url=f'http://cherny3v.beget.tech/api/top/update/{id}',headers={'Authorization':'Token ' + token1}, json=data)
    logout(token1)
    return respons

def update_res(token1,tower,res):
    date = requests.get(url=f'http://cherny3v.beget.tech/api/takeupdate?tower={tower}&resurse={res}',headers={'Authorization':'Token ' + token1}).json()
    requests.patch(url=f'http://cherny3v.beget.tech/api/update/update/{date[0]["id"]}',headers={'Authorization':'Token ' + token1})


# обработка сетевого пакета, подготовка данныз для отправки по апи

def re_arr(arr_str):
    arr_data = []
    arr_2 = arr_str.split('\\')
    arr_3 = []
    for i in arr_2:
        if len(i) > 5:
            arr_3.append(i)
    
    arr_4 = ''.join(arr_3)
    
    arr_5 = arr_4.split('{')
    list_arr = {}
    for i in arr_5:
        try:
            d = i.replace('"','')
            # print(d)
            arr_6 = d.split(",")
            for f in arr_6:
                arr_7 =  f.split(':')
                
                if len(arr_7) > 1:
                    # print(arr_7)
                    list_arr[arr_7[0]] = arr_7[1]
            arr_data.append(list_arr)
            list_arr = {}
            # print(list_arr['ItemTypeId'])
            # print('------------------')
        except Exception as e:
            pass
    return arr_data

data_sell_buy = {}
buy_amount = 0
sell_amount = 0
sell_price = 0
buy_price = 0
b_swich = 0
s_swich = 0
arr_ip = {'5.188.125.52': 'Lymhurst','5.188.125.44':'Fort_Sterling','5.188.125.10':'Bridgewatch','5.188.125.40':'Martlock','5.188.125.39':'Thetford'}
data_res = []
send_res = []
up_res = []

# расчет разницы цены в разных городах

def buy_sell(data):
    global data_sell_buy 
    global b_swich
    global s_swich 
    global buy_amount 
    global sell_amount
    global sell_price
    global buy_price
    try:
        for g in data: 
                try:
                    if g.get('Amount') != 'None':
                        if str(g.get('BuyerName')) != 'null':
                            if sell_amount >= 1000:
                                # print('step sell')
                                if str(g.get('UnitPriceSilver')) != 'None':
                                    sell_price = str(g.get('UnitPriceSilver')).replace('0000','',1)
                                else:
                                    continue
                                list_sell = {'price': int(sell_price), 'num': sell_amount}
                               
                                if 'sell' not in data_sell_buy:
                                    data_sell_buy['sell'] = list_sell
                                    data_sell_buy['type']= str(g.get('ItemTypeId'))
                                    sell_amount = 0
                            else:
                                sell_amount = sell_amount + int(g.get('Amount'))
                                
                        elif str(g.get('SellerName')) != 'null':
                            if buy_amount >= 1000:
                                if str(g.get('UnitPriceSilver')) != 'None':
                                    buy_price = str(g.get('UnitPriceSilver')).replace('0000','',1)
                                else:
                                    continue
                                list_buy = {'price': int(buy_price), 'num': buy_amount}
                                if 'buy' not in data_sell_buy: 
                                    data_sell_buy['buy'] = list_buy
                                    data_sell_buy['type']= str(g.get('ItemTypeId')).replace('@','_')
                                    buy_amount= 0
                            else: 
                                buy_amount = buy_amount + int(g.get('Amount'))


                except Exception as i:
                    # print(i)
                    pass
        return data_sell_buy
    except Exception as w:
        # print(w)
        pass

# расчет лучшей цены

def just_top(data_api,data,tower):
    id = data_api['id']
    buy = []
    sell = []
    data_api[f'{tower}_sell'] = str(data['sell']['price'])
    data_api[f'{tower}_buy'] = str(data['buy']['price'])
    for i in data_api:
        if f'_sell' in i:
            if data_api[i]:
                sell.append(data_api[i])
        elif f'_buy' in i:
            if data_api[i]:
                buy.append(data_api[i])

    min_price = int(min(buy))
    max_price = int(max(sell))

    data_api['profit'] = max_price - min_price

    for i in list(data_api):
        
        if data_api[i] == str(min_price):
            data_api['SityBuy'] = i
        elif data_api[i] == str(max_price):
            data_api['SitySell'] = i
           

    # print(data_api)
    ChengeTop(loginapi('Dedok123','Voron123'),data_api,id)

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=proccer_sniffer_paket)

# основной код приложения

def proccer_sniffer_paket(pacet):
    global data_sell_buy
    global b_swich
    global s_swich 
    try:
        if pacet['IP'].src in arr_ip:
                global id_pacet_send
                global arr_str
                b = pacet['Raw'].load.decode('ascii', 'ignore') 
                arr_id = str(pacet['Raw'].load).split('\\')
                arr_id2 = []
                for i in range(0,8,1):
                    arr_id2.append(arr_id[i])
                pacet_send = '\\'.join(arr_id2)
                # print(id_pacet_send)
                
                if b.find('TotalPrice') > 1:
                   

                    if id_pacet_send == '':
                        id_pacet_send = pacet_send
                        # print('начало')
                        arr_str = arr_str + str(pacet['Raw'].load)
                    elif id_pacet_send not in pacet_send :
                        id_pacet_send = pacet_send
                        arr_str = arr_str + str(pacet['Raw'].load)
                        
                        data = re_arr(arr_str)
                        data = buy_sell(data)
                        # print(data)
                        if data['type'] not in send_res:
                            post_data = {
                                'tower' : arr_ip[pacet['IP'].src],
                                'resource' : data['type'],
                                'price_sell' : data['sell']['price'],
                                'num_sell' : data['sell']['num'],
                                'price_buy' : data['buy']['price'],
                                'num_buy' : data['buy']['num']
                            }
                            # print('step1')
                            AddData(loginapi('Dedok123','Voron123'), post_data)
                            # print('step2')
                            data_top = CheakTop(loginapi('Dedok123','Voron123'), str(data['type']).replace('@','_'))
                            # print(data_top)
                            if data_top.json():
                                just_top(data_top.json()[0],data,arr_ip[pacet['IP'].src])
                            else:
                                send_top = {}
                                send_top['resurse'] = str(data['type']).replace('@','_')
                                send_top[f'{arr_ip[pacet["IP"].src]}_sell'] = data['sell']['price']
                                send_top[f'{arr_ip[pacet["IP"].src]}_buy'] = data['buy']['price']
                                send_top['is_publisher'] = True
                                SendTop(loginapi('Dedok123','Voron123'),send_top)  
                            send_res.append(data['type'])
                            res_up = str(data['type']).split('_')[1]
                            if res_up not in up_res:
                                update_res(loginapi('Dedok123','Voron123'),arr_ip[pacet['IP'].src],res_up)
                                up_res.append(res_up)

                            print(data['type'] + ' Добавлен')
                            # print(post_data)

                        
                        data_sell_buy = {}
                        

                        arr_str = ''
                        # print('конец')
                    elif b.find(id_pacet_send):
                        arr_str = arr_str + str(pacet['Raw'].load)
                        # print(id_pacet_send)
                    
    except Exception as e:
        # print(e)
        pass



sniff('Realtek 8822CE Wireless LAN 802.11ac PCI-E NIC')


