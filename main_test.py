from configparser import ConfigParser
import mysql.connector
import csv
import time
def config_pars():
    file = 'config.ini'
    config = ConfigParser()
    try:
        config.read(file)
    except Exception as ex:
        print(ex)

    dictionary_instrument = get_dictionary_instrument(config["Instruments"]["USDPLN"],config["Instruments"]["EURPLN"],config["Instruments"]["EURUSD"],config["Instruments"]["GBPUSD"]
                            ,config["Instruments"]["USDCHF"],config["Instruments"]["USDJPY"],config["Instruments"]["EURCHF"],config["Instruments"]["EURJPY"],config["Instruments"]["GBRJPY"]
                            ,config["Instruments"]["AUDUSD"],config["Instruments"]["USDCAD"])
    config_dic = {'count_rec_before': int(config["Count"]["count_rec_before"]), 'count_rec_intime': int(config["Count"]["count_rec_intime"]),               # 0 - fill 1 - partialFill 2 - cancel
                  'count_rec_after':int(config["Count"]["count_rec_after"]),'count_order_before':int(config["Count"]["count_order_before"]),
                  'count_order_intime':int(config["Count"]["count_order_intime"]),
                  'status_new': config["Status"]["New"], 'status_inProcess': config["Status"]["InProcess"],
                  'status_Fill': config["Status"]["StatusFill"].split(","), 'status_done': config["Status"]["Done"],'dictionary_instrument': dictionary_instrument,
                  'Side': config["Side"]["Options"].split(","), 'Max_volum': int(config["Volume"]["Max_volum"]), 'Min_volum': int(config["Volume"]["Min_volum"]),
                  'Date': config["Date"]["Date"], 'Note': config["Note"]["Notes"].split(","), 'Tag': config["Tag"]["Tags"].split(",")}

    return config_dic

def get_dictionary_instrument(USDPLN, EURPLN, EURUSD, GBPUSD, USDCHF, USDJPY, EURCHF, EURJPY, GBRJPY, AUDUSD, USDCAD):
    dictionary_instrument = {1: USDPLN , 2: EURPLN, 3:EURUSD, 4: GBPUSD, 5: USDCHF, 6: USDJPY, 7: EURCHF, 8: EURJPY, 9: GBRJPY, 10: AUDUSD, 11: USDCAD}
    for i in dictionary_instrument:
        dictionary_instrument[i] = list(map(str, dictionary_instrument[i].split(";")))
    return dictionary_instrument

def setup():
    table_of_records = []
    return table_of_records

def serial_number(count):
    serials_number = [num+1 for num in range(count)]
    return serials_number

def psevdo_random(serial,a,c,m):
    psevodo_number = []
    psevodo_number.append((a * serial[0] + c) % m)
    for num in range(len(serial)-1):
        psevodo_number.append((a*psevodo_number[num]+c)%m)
    return psevodo_number

def get_low_random(serial_num_random,m):
    psevdo_random =[]
    for num in range(len(serial_num_random)):
        psevdo_random.append((serial_num_random[num]/m))
    return psevdo_random

def init():
    serial_num_order = serial_number(2000)
    random_order_id = psevdo_random(serial_num_order, 106, 1283, 6075)
    serial_num_records = serial_number(7200)
    random_num_record = psevdo_random(serial_num_order, 106, 1283, 6075)
    return

if __name__ == '__main__':
    mydb = mysql.connector.connect(
        host="localhost",
        user="work",
        password="11Tittim"
    )

    #mycursor = mydb.cursor()
    #mycursor.execute('CREATE DATABASE IF NOT EXISTS orders;USE orders;DROP TABLE IF EXISTS orders_history; CREATE TABLE orders_history (Serial_num_of_record INT, ID VARCHAR(10), Instrument VARCHAR(10), Px_Init DOUBLE, Px_Fill DOUBLE, Side VARCHAR(10), Volume_Init DOUBLE, Volume_Fill DOUBLE, Date DATETIME(3), Status VARCHAR(30), Note VARCHAR(255), Tags TEXT);')

    flag = False
    mycursor = mydb.cursor()
    mycursor.execute('USE orders;')
    with open('/home/tim/ProgramsPython/Test orders/Table_sort.csv') as f:
        reader = csv.reader(f)


        mycursor.executemany(reader,[])
        for row in reader:
            if not flag:
                flag = True
                continue
            mycursor.execute("INSERT INTO orders_history"
                             "(Serial_num_of_record, ID, Instrument, Px_Init, Px_Fill, Side, Volume_Init, Volume_Fill, Date, Status, Note, Tags)" 
                             "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", row)

    mydb.commit()
    mycursor.close()
    print("Done")
    #VALUES(INT, VARCHAR(10), VARCHAR(10), DOUBLE, DOUBLE, VARCHAR(10), DOUBLE, DOUBLE, DATETIME(3), VARCHAR(30), VARCHAR(255), TEXT)