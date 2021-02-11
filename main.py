from configparser import ConfigParser
import csv
import math
from datetime import timedelta, datetime

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

def init():
    numberOforder = []
    return numberOforder

def get_num_of_status(to, list):
    done_list =[]
    for num in list:

        done_list.append(int((to - 1) * num + 1))
    return done_list

def serial_number(count):
    serials_number = [num+1 for num in range(count)]
    return serials_number

def get_low_random(serial_num_random,m):
    psevdo_random =[]
    for num in range(len(serial_num_random)):
        psevdo_random.append((serial_num_random[num]/m))
    return psevdo_random

def get_transform_to_record(record_row, inform_record):
    transform = []
    for i in record_row:
        transform.append(inform_record[i-1])
    return transform

def get_transform_to_f3(list):
    for i in range(len(list)):
        list[i] = float('%.3f' % list[i])
    return list

def psevdo_random(serial,a,c,m):
    psevodo_number = []
    psevodo_number.append((a * serial[0] + c) % m)
    for num in range(len(serial)-1):
        psevodo_number.append((a*psevodo_number[num]+c)%m)
    return psevodo_number

def id(random_id_order, serial_num_record, count_rec_before,count_rec_intime,count_order_before, count_order_intime):
    #num = 0
    id = {num + 1: hex(random_id_order[num]) for num in range(len(random_id_order))}
    record_row = []
    id_record =[]
    id_before = []
    id_intime = []
    id_after = []
    for num in range(len(serial_num_record)):
        id_before.append(int((((serial_num_record[num] - 1) / 3) + 1)))
        id_intime.append(int((((serial_num_record[num] - count_rec_before - 1) / 4) + count_order_before +1)))
        id_after.append(int((((serial_num_record[num] - count_rec_intime - count_rec_before - 1) / 3) + count_order_before + count_order_intime +1)))
        if serial_num_record[num] <= count_rec_before:
            record_row.append(id_before[num])
            id_record.append(id[id_before[num]])
        elif (serial_num_record[num] - count_rec_before) <= count_rec_intime:
            record_row.append(id_intime[num])
            id_record.append(id[id_intime[num]])
        else:
            record_row.append(id_after[num])
            id_record.append(id[id_after[num]])
    return id_record,record_row


def status(serial_num_record,count_rec_before, count_rec_intime ,count_order_before, low_random, new, inProcess, statusFill, done):
    new_num_status = 1
    inProcess_num_status = 2
    fill_num_status = 3
    id_before = []
    id_intime = []
    id_after = []
    status_row = []
    status_record = []
    fill_status_num = []
    for num in range(len(serial_num_record)):
        id_before.append(((serial_num_record[num] -1) % 3)+2)
        id_intime.append(((serial_num_record[num] - count_rec_before - 1) % 4)+1)
        id_after.append(((serial_num_record[num] - count_rec_intime - count_order_before -1) % 3)+1)

        if serial_num_record[num] <= count_rec_before:
            status_row.append(id_before[num])
        elif (serial_num_record[num] - count_rec_before) <= count_rec_intime:
            status_row.append(id_intime[num])
        else:
            status_row.append(id_after[num])
        fill_status_num.append(int((4 - 1)* low_random[num]))
    for num in range(len(serial_num_record)):
        if status_row[num] == new_num_status:
            status_record.append(new)
        elif status_row[num] == inProcess_num_status:
            status_record.append(inProcess)
        elif status_row[num] == fill_num_status:
            status_record.append(statusFill[fill_status_num[num]])
        else: status_record.append(done)

    return status_record, status_row, fill_status_num

def instrument(serial_num_order,psevdo_random_low, dictionary_instrument, record_row):
    get_name_instrument = 0
    get_spred_instrument = 1
    get_prize_instrument = 2
    instrument_num_status = []
    instrument_order_status =[]
    instrunent_prize = []
    random_fill =[]
    puncts = []
    spred = []
    px_fill_records = []
    for num in range(len(serial_num_order)):
        instrument_num_status.append(int((12-1)*psevdo_random_low[num]+1))
        instrument_order_status.append(dictionary_instrument[instrument_num_status[num]][get_name_instrument])
        instrunent_prize.append(float(dictionary_instrument[instrument_num_status[num]][get_prize_instrument]))
    instrument_record_status = get_transform_to_record(record_row,instrument_order_status)
    instrunent_record_prize = get_transform_to_record(record_row,instrunent_prize)
    for num in range(len(serial_num_order)):
        random_fill.append(int((101-1)*psevdo_random_low[num]+1))
        spred.append(dictionary_instrument[instrument_num_status[num]][get_spred_instrument])
        if random_fill[num] % 10 == 0:
            puncts.append(0)
        elif psevdo_random_low[num] > 0.5:
            puncts.append(random_fill[num]* float(spred[num]))
        else: puncts.append(random_fill[num]* float(spred[num]) * -1)
        px_fill_records.append(instrunent_prize[num] + puncts[num])

    px_fill_records = get_transform_to_record(record_row, px_fill_records)

    px_fill_records = get_transform_to_f3(px_fill_records)

    return instrument_record_status, instrunent_record_prize, px_fill_records

def side(list_opt, record_row):
    buy_num_in_optlist = 0
    sell_num_in_optlist = 1
    status_side = get_num_of_status(5,get_low_random(psevdo_random(serial_num_order,1664525,1013904223,math.pow(2,32)),math.pow(2,32)))
    for i in range(len(status_side)):
        if status_side[i] % 2 == 0:
            status_side[i] = list_opt[buy_num_in_optlist]
        else: status_side[i] = list_opt[sell_num_in_optlist]
    status_side = get_transform_to_record(record_row, status_side)

    return status_side

def volum_init(volum_init_max, volum_init_min, psevdo_random_low, record_row):
    volum_for_order = []
    psevdo_random_low = get_transform_to_f3(psevdo_random_low)
    for num in psevdo_random_low:
        volum_for_order.append(int(((volum_init_max - volum_init_min) * num + volum_init_min)/1000)*1000)
    volum_for_record = get_transform_to_record(record_row,volum_for_order)

    return volum_for_record, volum_for_order

def volum_fill(low_random_orders, volum_init_order, volum_init_min, status_num_record,fill_status_num, volum_for_record, record_row):
    partial_fill_volum = []
    fill_volum_records =[]
    for num in range(len(low_random_orders)):
        partial_fill_volum.append(int(((volum_init_order[num] - volum_init_min)*low_random_orders[num]+volum_init_min)/1000)*1000)
    partial_fill_volum = get_transform_to_record(record_row, partial_fill_volum)
    fill_volum_records.append(0)
    num = 1
    while num < len(partial_fill_volum):
        if status_num_record[num] == 1 or status_num_record[num] == 2:
            fill_volum_records.append(0)
        elif status_num_record[num] == 4:
            fill_volum_records.append(fill_volum_records[num - 1])
        else:
            if fill_status_num[num] == 0:
                fill_volum_records.append(volum_for_record[num])
            elif fill_status_num[num] == 1:
                fill_volum_records.append(partial_fill_volum[num])
            elif fill_status_num[num] == 2:
                fill_volum_records.append(0)
        num+=1

    return fill_volum_records


def date(low_random_orders, record_row, status_num_record, date, low_random_records):
    sec_for_new =[]
    sec_for_inProcess =[]
    sec_for_fill =[]
    sec_for_done = []
    date_for_record =[]
    date_sec_for_tag = []
    msec_for_record= []
    date_init = datetime.strptime(date, "%d.%m.%y %H:%M:%S.%f")
    for num in range(len(low_random_orders)):
        sec_for_new.append(int((3000 - 1)*low_random_orders[num] + 1))
        sec_for_inProcess.append(int(((1000 + sec_for_new[num])-1)*low_random_orders[num] + sec_for_new[num] + 1))
        sec_for_fill.append(int(((1000 + sec_for_inProcess[num])-1)*low_random_orders[num] + sec_for_inProcess[num] + 1))
        sec_for_done.append(int(((1000 + sec_for_fill[num])-1)*low_random_orders[num] + sec_for_fill[num] + 1))
    for num in range(len(low_random_records)):
        msec_for_record.append((int((3000 - 1)*low_random_records[num] + 1)))
    sec_for_new_record = get_transform_to_record(record_row,sec_for_new)
    sec_for_inProcess_record = get_transform_to_record(record_row,sec_for_inProcess)
    sec_for_fill_record = get_transform_to_record(record_row,sec_for_fill)
    sec_for_done_record = get_transform_to_record(record_row,sec_for_done)
    date_sec_for_tag.append(sec_for_new)
    date_sec_for_tag.append(sec_for_inProcess)
    date_sec_for_tag.append(sec_for_fill)
    date_sec_for_tag.append(sec_for_done)
    for num in range(len(low_random_records)):
        if status_num_record[num] == 1:
            date_for_record.append(date_init+timedelta(seconds=sec_for_new_record[num],microseconds=msec_for_record[num]))
        elif status_num_record[num] == 2:
            date_for_record.append(date_init + timedelta(seconds=sec_for_inProcess_record[num],microseconds=msec_for_record[num]))
        elif status_num_record[num] == 3:
            date_for_record.append(date_init + timedelta(seconds=sec_for_fill_record[num],microseconds=msec_for_record[num]))
        else:  date_for_record.append(date_init+timedelta(seconds=sec_for_done_record[num], microseconds=msec_for_record[num]))

    return date_for_record, date_sec_for_tag

def tag(lis_tag, date_sec_for_tag, record_row):
    tag_for_order = []

    for num in range(len(date_sec_for_tag[0])):
        tmp = ""
        for num_list in range(4):
            tmp += (lis_tag[int(str(date_sec_for_tag[num_list][num])[len(str(date_sec_for_tag[num_list][num]))-1:])])
        tag_for_order.append(tmp)

    return get_transform_to_record(record_row,tag_for_order)


def note(list_note, date_sec_for_note, record_row):
    note_for_order = []
    first_digit = 1
    for num in range(len(date_sec_for_note[0])):
        tmp = ""
        for num_list in range(4):
            tmp += list_note[int(str(date_sec_for_note[num_list][num])[:first_digit])]
        note_for_order.append(tmp)

    return get_transform_to_record(record_row,note_for_order)

if __name__ == '__main__':

    config = config_pars()
    serial_num_order = serial_number(2000)                          #ID
    random_order_id = psevdo_random(serial_num_order,106,1283,6075)
    serial_num_records = serial_number(7200)
    ID,record_row = id(random_order_id,serial_num_records,config['count_rec_before'],config['count_rec_intime'],config['count_order_before'], config['count_order_intime'])


    low_random_records = get_low_random(psevdo_random(serial_num_records,1664525,1013904223,math.pow(2,32)),math.pow(2,32))
    low_random_orders =  get_low_random(psevdo_random(serial_num_order,1664525,1013904223,math.pow(2,32)),math.pow(2,32))
    status_order,status_num_record,fill_status_num = status(serial_num_records,config['count_rec_before'],config['count_rec_intime'],
            config['count_order_before'],low_random_records, config['status_new'], config['status_inProcess'],
            config['status_Fill'], config['status_done'])
    instrument_record_status, instrunent_record_prize, px_fill_records=instrument(serial_num_order, low_random_orders,
                        config['dictionary_instrument'],record_row)

    side_status = side(config['Side'],record_row)

    volum_init_record, volum_init_for_order = volum_init(config["Max_volum"],config["Min_volum"], get_low_random(psevdo_random(serial_num_order,106,1283,6075), 6075), record_row)

    volum_fill_record = volum_fill(low_random_orders,volum_init_for_order, config["Min_volum"], status_num_record, fill_status_num, volum_init_record, record_row)

    date_records,date_sec_for_TagNote = date(low_random_orders,record_row, status_num_record, config["Date"], low_random_records)

    record_tags = tag(config["Tag"], date_sec_for_TagNote, record_row)

    record_notes = note(config["Note"], date_sec_for_TagNote, record_row)

    with open("Table.csv","w") as f:
        writer = csv.writer(f, delimiter = '\t')
        writer.writerow(('Serial number of record','ID','Instrument','Prize', 'Px_fill', 'Side' ,'Volume init','Volume fill','Date','Status', 'Note', 'Tag'))
        for i in zip(serial_num_records, ID, instrument_record_status, instrunent_record_prize, px_fill_records, side_status, volum_init_record ,volum_fill_record, date_records, status_order, record_notes, record_tags):
            writer.writerow(i)

