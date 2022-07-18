import paho.mqtt.client as mqtt
import time
import requests
import json
import pymysql
import xmltodict
import datetime

import logging


juso_db = pymysql.connect(
    user='couter656',
    passwd='!6_ATdm4ElYPO88AlPHTW4S2xW4VCwCV',
    host='10.0.0.5',
    db='embedded',
    charset='utf8'
)


cursor = juso_db.cursor(pymysql.cursors.DictCursor)

mqtt_topic = "zeroweb/status/7345.2.2107000144/sdata/#"
# mqtt_topic1 = "zeroweb/status/7345.2.2107000144/salive/#"
mqtt_topic2 = "zeroweb/status/7345.2.2107000217/sdata/#"
# mqtt_topic3 = "zeroweb/status/7345.2.2107000217/salive/#"
mqtt_topic4 = "zeroweb/status/7345.2.2107000009/sdata/#"
# mqtt_topic5 = "zeroweb/status/7345.2.2107000009/salive/#"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
        client.subscribe(mqtt_topic)
        # client.subscribe(mqtt_topic1)
        client.subscribe(mqtt_topic2)
        # client.subscribe(mqtt_topic3)
        client.subscribe(mqtt_topic4)
        # client.subscribe(mqtt_topic5)

    else:
        print("Bad connection Returned code=", rc)


def serial_loop():
    print("Serial : ", mqtt_topic)
    time.sleep(5)
    return 0


def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))


def on_subscribe(client, userdata, mid, granted_qos,):
    print("subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, message):

    print('------------------------------------------------------------------------')
    print("Topic: ", message.topic)
    Data = message.topic[22:32]

    # if DAta10.find("salive") != -1:
    #     DAta1 = message.topic[40:41] + message.topic[42:44]
    #     DAta6 = message.topic[45:46] + message.topic[47:48]
    # elif len(message.topic) < 53:
    #     DAta1 = message.topic[40:41] + message.topic[42:44]
    #     DAta6 = message.topic[45:48] + message.topic[49:50]
    # else:
    #     DAta1 = message.topic[40:41] + message.topic[42:44]
    #     DAta6 = message.topic[45:48] + message.topic[49:50]

    # DAta2 = message.topic[40:41]
    # DAta3 = message.topic[42:44]

    # if len(message.topic) < 52:
    #     DAta4 = message.topic[45:46]
    # elif len(message.topic) < 53:
    #     DAta4 = message.topic[45:48]
    # else:
    #     DAta4 = message.topic[45:48]

    # if len(message.topic) < 52:
    #     DAta5 = message.topic[47:48]
    # elif len(message.topic) < 53:
    #     DAta5 = message.topic[49:50]
    # else:
    #     DAta5 = message.topic[49:50]

    if len(message.topic) < 51:
        Data1 = message.topic[39:40] + message.topic[41:43] + \
            message.topic[44:45] + message.topic[46:47]
    elif len(message.topic) < 52:
        Data1 = message.topic[39:40] + message.topic[41:43] + \
            message.topic[44:46] + message.topic[47:48]
    else:
        Data1 = message.topic[39:40] + message.topic[41:43] + \
            message.topic[44:47] + message.topic[47:48]

    Data2 = message.topic[39:40]
    Data3 = message.topic[41:43]

    if len(message.topic) < 51:
        Data4 = message.topic[44:45]
    elif len(message.topic) < 52:
        Data4 = message.topic[44:46]
    else:
        Data4 = message.topic[44:47]

    if len(message.topic) < 51:
        Data5 = message.topic[46:47]
    elif len(message.topic) < 52:
        Data5 = message.topic[47:48]
    else:
        Data5 = message.topic[48:49]

    #Data5 = message.topic[46:47]
    # print(DAta6)
    # print(DAta7)
    # print(DAta8)
    # print(DAta9)
    # print(DAta10)
    # print(DAta11)
    print('-------------', '\n')
    print(Data)
    print(Data1)
    print(Data2)
    print(Data3)
    print(Data4)
    print(Data5)

    payload = message.payload.decode("utf-8")
    dictionary = xmltodict.parse(payload)
    data = dict(dict(dictionary)['hubthing'])
    for key, value in data.items():
        data[key] = int(value)
    d = datetime.datetime.now()
    print("data : ", data)
    print("Push_time : ", d)
    print('------------------------------------------------------------------------', '\n')
    hub_number = Data
    sensor_id = Data2 + Data3 + Data4 + Data5
    # Sensor_id = DAta2 + DAta3 + DAta4 + DAta5
    child_sensor_type = Data3
    # Child_sensor_type = DAta3
    serial_number = hub_number + "." + sensor_id
    hub_serial_number = Data
    value = data['value']
    alive = data['alive']
    battery = data['battery']
    rssi = data['rssi']
    created_at = d
    active = "1"

    if data.get('temper'):
        temper = data['temper']
        humid = data['humid']
        sql = f"INSERT INTO embedded.temper_sensor (serial_number, value, alive, battery, temper, humid, rssi, created_at) VALUES ({serial_number}, '{value}', '{alive}', '{battery}', '{temper}', '{humid}', '{rssi}', '{created_at}');"
        try:
            sql2 = f"INSERT ignore INTO embedded.hub_sensor (serial_number, child_sensor_id, child_sensor_type, active, created_at) VALUES ('{hub_serial_number}', '{serial_number}', '{child_sensor_type}', '{active}', '{created_at}');"
            cursor.execute(sql2)
            juso_db.commit()
        except Exception as e:
            print(e)

    elif child_sensor_type.find("17") != -1:
        sql = f"INSERT INTO embedded.door_sensor (serial_number, value, alive, battery, rssi, created_at) VALUES ({serial_number}, '{value}', '{alive}', '{battery}', '{rssi}', '{created_at}');"
        try:
            sql2 = f"INSERT ignore INTO embedded.hub_sensor (serial_number, child_sensor_id, child_sensor_type, active, created_at) VALUES ('{hub_serial_number}', '{serial_number}', '{child_sensor_type}', '{active}', '{created_at}');"
            cursor.execute(sql2)
            juso_db.commit()
        except Exception as e:
            print(e)

    elif child_sensor_type.find("34") != -1:
        sql = f"INSERT INTO embedded.sos_sensor (serial_number, value, alive, battery, rssi, created_at) VALUES ({serial_number}, '{value}', '{alive}', '{battery}', '{rssi}', '{created_at}');"
        try:
            sql2 = f"INSERT ignore INTO embedded.hub_sensor (serial_number, child_sensor_id, child_sensor_type, active, created_at) VALUES ('{hub_serial_number}', '{serial_number}', '{child_sensor_type}', '{active}', '{created_at}');"
            cursor.execute(sql2)
            juso_db.commit()
        except Exception as e:
            print(e)

    elif child_sensor_type.find("19") != -1:
        sql = f"INSERT INTO embedded.fire_sensor (serial_number, value, alive, battery, rssi, created_at) VALUES ({serial_number}, '{value}', '{alive}', '{battery}', '{rssi}', '{created_at}');"
        try:
            sql2 = f"INSERT ignore INTO embedded.hub_sensor (serial_number, child_sensor_id, child_sensor_type, active, created_at) VALUES ('{hub_serial_number}', '{serial_number}', '{child_sensor_type}', '{active}', '{created_at}');"
            cursor.execute(sql2)
            juso_db.commit()
        except Exception as e:
            print(e)

    else:
        print("not")

    cursor.execute(sql)
    juso_db.commit()


client = mqtt.Client()

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_subscribe = on_subscribe
client.on_message = on_message

# client.connect('54.180.155.172', 1883)
client.connect('broker.rayhomeiot.com', 1883)

client.loop_forever()
