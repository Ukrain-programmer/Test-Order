from abc import ABC, abstractmethod
from configparser import ConfigParser
import math
from datetime import timedelta, datetime
class Config:
    config_dic = None


    def __init__(self):
        self.pars_file()

    def pars_file(self):
        file = 'config.ini'
        config = ConfigParser()
        try:
            config.read(file)
        except Exception as ex:
            print(ex)

        dictionary_instrument =  self.__get_dictionary_instrument(config["Instruments"]["USDPLN"],
                                                          config["Instruments"]["EURPLN"],
                                                          config["Instruments"]["EURUSD"],
                                                          config["Instruments"]["GBPUSD"]
                                                          , config["Instruments"]["USDCHF"],
                                                          config["Instruments"]["USDJPY"],
                                                          config["Instruments"]["EURCHF"],
                                                          config["Instruments"]["EURJPY"],
                                                          config["Instruments"]["GBRJPY"]
                                                          , config["Instruments"]["AUDUSD"],
                                                          config["Instruments"]["USDCAD"])

        self.config_dic = {'count_rec_before': int(config["Count"]["count_rec_before"]),
                      'count_rec_intime': int(config["Count"]["count_rec_intime"]),
                      # 0 - fill 1 - partialFill 2 - cancel
                      'count_rec_after': int(config["Count"]["count_rec_after"]),
                      'count_order_before': int(config["Count"]["count_order_before"]),
                      'count_order_intime': int(config["Count"]["count_order_intime"]),
                      'status_new': config["Status"]["New"], 'status_inProcess': config["Status"]["InProcess"],
                      'status_Fill': config["Status"]["StatusFill"].split(","), 'status_done': config["Status"]["Done"],
                      'dictionary_instrument': dictionary_instrument,
                      'Side': config["Side"]["Options"].split(","), 'Max_volum': int(config["Volume"]["Max_volum"]),
                      'Min_volum': int(config["Volume"]["Min_volum"]),
                      'Date': config["Date"]["Date"], 'Note': config["Note"]["Notes"].split(","),
                      'Tag': config["Tag"]["Tags"].split(",")}


    def __get_dictionary_instrument(self, USDPLN, EURPLN, EURUSD, GBPUSD, USDCHF, USDJPY, EURCHF, EURJPY, GBRJPY, AUDUSD,
                                  USDCAD):
        dictionary_instrument = {1: USDPLN, 2: EURPLN, 3: EURUSD, 4: GBPUSD, 5: USDCHF, 6: USDJPY, 7: EURCHF,
                                 8: EURJPY,
                                 9: GBRJPY, 10: AUDUSD, 11: USDCAD}
        for i in dictionary_instrument:
            dictionary_instrument[i] = list(map(str, dictionary_instrument[i].split(";")))

        return dictionary_instrument

    def getByName(self, name):
        return self.config_dic[name]


class InitNumForGenerator:
    total = None
    a_LCG = None
    c_LCG = None
    m_LCG = None
    def __init__(self, total, a_LCG, c_LCG, m_LCG):
        self.total = total
        self.a_LCG = a_LCG
        self.c_LCG = c_LCG
        self.m_LCG = m_LCG
        self.serial_number_list = None
        self.psevdo_number_list = None
        self.__serial_number()
        self.__psevdo_random()

    def __serial_number(self):
        self.serial_number_list = [num + 1 for num in range(self.total)]


    def __psevdo_random(self):
        psevodo_number = []
        psevodo_number.append((self.a_LCG * self.serial_number_list[0] + self.c_LCG) % self.m_LCG)
        for num in range(len(self.serial_number_list) - 1):
            psevodo_number.append((self.a_LCG * psevodo_number[num] + self.c_LCG) % self.m_LCG)
        self.psevdo_number_list = psevodo_number

    def get_low_random(self):
        psevdo_low_random_list = []
        for num in range(len(self.psevdo_number_list)):
            psevdo_low_random_list.append((self.psevdo_number_list[num] / self.m_LCG))
        return psevdo_low_random_list

    def get_psevdo_randon_list(self):
        return self.psevdo_number_list

    def get_psevdo_random_transform_f_list(self, digist):
        list = self.get_low_random()
        param = '%.' + str(digist) + 'f'
        for i in range(len(list)):
            list[i] = float(param % list[i])
        return list


class IGenerator(ABC):
    @abstractmethod
    def getData(self) -> list:
        pass

class ID(IGenerator):
    list_of_id_record =None
    def __init__(self, config):
        self.serial_number_list = [num + 1 for num in range(7200)]
        self.init_num = InitNumForGenerator(2000, 106, 1283, 6075)
        self.id = None
        self.record_row = []
        self.id_record = []
        self.config = config
        self.calc_ID()

    def __id_hex(self):
        rsndom_list = self.init_num.get_psevdo_randon_list()
        self.id = {num + 1: hex(rsndom_list[num]) for num in range(len(rsndom_list))}


    def calc_ID(self):
        self.__id_hex()

        for num in range(len(self.serial_number_list)):
            if self.serial_number_list[num] <= self.config.getByName('count_rec_before'):
                self.record_row.append(int((((self.serial_number_list[num] - 1) / 3) + 1)))
                self.id_record.append(self.id[int((((self.serial_number_list[num] - 1) / 3) + 1))])
            elif (self.serial_number_list[num] - self.config.getByName('count_rec_before')) <= self.config.getByName('count_rec_intime'):
                self.record_row.append(int((((self.serial_number_list[num] - self.config.getByName('count_rec_before') - 1) / 4) + self.config.getByName('count_order_before') + 1)))
                self.id_record.append(self.id[int((((self.serial_number_list[num] - self.config.getByName('count_rec_before') - 1) / 4) + self.config.getByName('count_order_before') + 1))])
            else:
                self.record_row.append(int((((self.serial_number_list[num] - self.config.getByName('count_rec_intime') - self.config.getByName('count_rec_before') - 1) / 3) + self.config.getByName('count_order_before') + self.config.getByName('count_order_intime') + 1)))
                self.id_record.append(self.id[int((((self.serial_number_list[num] - self.config.getByName('count_rec_intime') - self.config.getByName('count_rec_before') - 1) / 3) + self.config.getByName('count_order_before') + self.config.getByName('count_order_intime') + 1))])

    def getData(self):
        return self.id_record

    def get_record_row(self):
        return self.record_row

class Status(IGenerator):
    def __init__(self, config):
        config = config
        self.init = InitNumForGenerator(7200,22695477, 1, math.pow(2, 32))
        self.serial_number_list = [num + 1 for num in range(7200)]
        self.status_row = []
        self.status_record = []
        self.count_rec_before = config.getByName('count_rec_before')
        self.count_rec_intime = config.getByName('count_rec_intime')
        self.count_order_before = config.getByName('count_order_before')
        self.new = config.getByName('status_new')
        self.inProcess = config.getByName('status_inProcess')
        self.statusFill = config.getByName('status_Fill')
        self.done = config.getByName('status_done')
        self.fill_status_num = []
        self.procces()


    def procces(self):
        self.low_random = self.init.get_psevdo_random_transform_f_list(9)
        new_num_status = 1
        inProcess_num_status = 2
        fill_num_status = 3
        for num in range(len(self.serial_number_list)):
            if self.serial_number_list[num] <= self.count_rec_before:
                self.status_row.append(((self.serial_number_list[num] - 1) % 3) + 2)
            elif (self.serial_number_list[num] - self.count_rec_before) <= self.count_rec_intime:
                self.status_row.append(((self.serial_number_list[num] - self.count_rec_before - 1) % 4) + 1)
            else:
                self.status_row.append(((self.serial_number_list[num] - self.count_rec_intime - self.count_order_before - 1) % 3) + 1)
            self.fill_status_num.append(int((4 - 1) * self.low_random[num]))

        for num in range(len(self.serial_number_list)):
            if self.status_row[num] == new_num_status:
                self.status_record.append(self.new)
            elif self.status_row[num] == inProcess_num_status:
                self.status_record.append(self.inProcess)
            elif self.status_row[num] == fill_num_status:
                self.status_record.append(self.statusFill[self.fill_status_num[num]])
            else:
                self.status_record.append(self.done)

    def getData(self):
        return self.status_record

    def get_status_row(self):
        return self.status_row

    def get_fill_status_num(self):
        return self.fill_status_num


class Instrument(IGenerator):

    def __init__(self, config, id):
        self.init = InitNumForGenerator(2000,22695477, 1, math.pow(2, 32))
        self.record_row = id.get_record_row()
        self.serial_number = 2000
        self.instrument_record_status = None
        self.instrunent_record_prize = None
        self.px_fill_records = []
        self.config = config
        self.procces()

    def procces(self):
        get_name_instrument = 0
        get_spred_instrument = 1
        get_prize_instrument = 2
        psevdo_random_low = self.init.get_low_random()
        dictionary_instrument = self.config.getByName('dictionary_instrument')
        instrument_num_status = []
        instrument_order_status = []
        instrunent_prize = []
        random_fill = []
        puncts = []
        spred = []

        for num in range(self.serial_number):
            instrument_num_status.append(int((12 - 1) * psevdo_random_low[num] + 1))
            instrument_order_status.append(dictionary_instrument[instrument_num_status[num]][get_name_instrument])
            instrunent_prize.append(float(dictionary_instrument[instrument_num_status[num]][get_prize_instrument]))
        self.instrument_record_status = self.get_transform_to_record(instrument_order_status)
        self.instrunent_record_prize = self.get_transform_to_record(instrunent_prize)
        for num in range(self.serial_number):
            random_fill.append(int((101 - 1) * psevdo_random_low[num] + 1))
            spred.append(dictionary_instrument[instrument_num_status[num]][get_spred_instrument])
            if random_fill[num] % 10 == 0:
                puncts.append(0)
            elif psevdo_random_low[num] > 0.5:
                puncts.append(random_fill[num] * float(spred[num]))
            else:
                puncts.append(random_fill[num] * float(spred[num]) * -1)
            self.px_fill_records.append(instrunent_prize[num] + puncts[num])

        self.px_fill_records = self.get_transform_to_record(self.px_fill_records)
        self.px_fill_records = self.__get_transform_to_f3(self.px_fill_records)


    def __get_transform_to_f3(self,list):
        param = '%.' + str(3) + 'f'
        for i in range(len(list)):
            list[i] = float(param % list[i])
        return list

    def get_transform_to_record(self, inform_record):
        transform = []
        for i in self.record_row:
            transform.append(inform_record[i - 1])
        return transform

    def getData(self):
        return self.instrument_record_status, self.instrunent_record_prize, self.px_fill_records

    def get_instrunent_record_prize(self):
        return self.instrunent_record_prize

    def get_px_fill_records(self):
        return self.px_fill_records


class Side(IGenerator):

    def __init__(self, config, id):
        config = config
        self.init = InitNumForGenerator(2000, 1664525, 1013904223, math.pow(2, 32))
        self.list_opt = config.getByName('Side')
        self.record_row = id.get_record_row()
        self.status_side = None
        self.procces()

    def procces(self):
        buy_num_in_optlist = 0
        sell_num_in_optlist = 1
        status_side = self.__get_num_of_status(5, self.init.get_low_random())
        for i in range(len(status_side)):
            if status_side[i] % 2 == 0:
                status_side[i] = self.list_opt[buy_num_in_optlist]
            else:
                status_side[i] = self.list_opt[sell_num_in_optlist]
        self.status_side = self.get_transform_to_record(status_side)


    def get_transform_to_record(self, inform_record):
        transform = []
        for i in self.record_row:
            transform.append(inform_record[i - 1])
        return transform

    def __get_num_of_status(self, to, list):
        done_list = []
        for num in list:
            done_list.append(int((to - 1) * num + 1))
        return done_list

    def getData(self):
        return self.status_side


class Volum_init(IGenerator):

    def __init__(self, config, id):
        config = config
        self.record_row = id.get_record_row()
        self.init = InitNumForGenerator(2000, 106, 1283, 6075)
        self.volum_init_max = config.getByName("Max_volum")
        self.volum_init_min = config.getByName("Min_volum")
        self.volum_for_record = None
        self.volum_for_order = []
        self.prpcess()

    def prpcess(self):
        psevdo_random_low = self.init.get_low_random()
        psevdo_random_low = self.__get_transform_to_f5(psevdo_random_low)

        for num in psevdo_random_low:
            self.volum_for_order.append(int(((self.volum_init_max - self.volum_init_min) * num + self.volum_init_min) / 1000) * 1000)
        self.volum_for_record = self.__get_transform_to_record(self.volum_for_order)


    def __get_transform_to_record(self, inform_record):
        transform = []
        for i in self.record_row:
            transform.append(inform_record[i - 1])
        return transform

    def __get_transform_to_f5(self,list):
        param = '%.' + str(5) + 'f'
        for i in range(len(list)):
            list[i] = float(param % list[i])
        return list

    def getData(self):
        return self.volum_for_record

    def get_volume_init_for_order(self):
        return self.volum_for_order


class Volum_fill(IGenerator):

    def __init__(self, config, volum, status, id):
        self.init = InitNumForGenerator(2000, 106, 1283, 6075)
        self.volum = volum
        self.config = config
        self.status = status
        self.id = id
        self.fill_volum_records = []
        self.procces()

    def procces(self):
        low_random_orders = self.init.get_psevdo_random_transform_f_list(9)
        volum_init_order = self.volum.get_volume_init_for_order()
        volum_init_min = self.config.getByName("Min_volum")
        volum_for_record = self.volum.getData()
        status_num_record = self.status.get_status_row()
        fill_status_num = self.status.get_fill_status_num()
        partial_fill_volum = []

        for num in range(len(low_random_orders)):
            partial_fill_volum.append(int(((volum_init_order[num] - volum_init_min) * low_random_orders[num] + volum_init_min) / 1000) * 1000)
        partial_fill_volum = self.__get_transform_to_record(partial_fill_volum)
        self.fill_volum_records.append(0)
        num = 1
        while num < len(partial_fill_volum):
            if status_num_record[num] == 1 or status_num_record[num] == 2:
                self.fill_volum_records.append(0)
            elif status_num_record[num] == 4:
                self.fill_volum_records.append(self.fill_volum_records[num - 1])
            else:
                if fill_status_num[num] == 0:
                    self.fill_volum_records.append(volum_for_record[num])
                elif fill_status_num[num] == 1:
                    self.fill_volum_records.append(partial_fill_volum[num])
                elif fill_status_num[num] == 2:
                    self.fill_volum_records.append(0)
            num += 1



    def getData(self):
        return self.fill_volum_records


    def __get_transform_to_record(self, inform_record):
        transform = []
        for i in self.id.get_record_row():
            transform.append(inform_record[i - 1])
        return transform


class Date(IGenerator):
    def __init__(self, config, id, status, ):
        self.init_order = InitNumForGenerator(2000, 22695477, 1, math.pow(2, 32))
        self.init_record = InitNumForGenerator(7200, 22695477, 1, math.pow(2, 32))
        self.id = id
        self.status = status
        self.config = config
        self.date_for_record = []
        self.date_sec_for_tag = []
        self.procces()


    def procces(self):
        low_random_orders = self.init_order.get_psevdo_random_transform_f_list(9)
        low_random_records = self.init_record.get_psevdo_random_transform_f_list(9)
        status_num_record = self.status.get_status_row()
        date = self.config.getByName("Date")
        sec_for_new = []
        sec_for_inProcess = []
        sec_for_fill = []
        sec_for_done = []
        msec_for_record = []
        date_init = datetime.strptime(date, "%d.%m.%y %H:%M:%S.%f")
        for num in range(len(low_random_orders)):
            sec_for_new.append(int((1000 - 1) * low_random_orders[num] + 1))
            sec_for_inProcess.append(
                int(((500 + sec_for_new[num]) - 1) * low_random_orders[num] + sec_for_new[num]))
            sec_for_fill.append(
                int(((500 + sec_for_inProcess[num]) - 1) * low_random_orders[num] + sec_for_inProcess[num]))
            sec_for_done.append(
                int(((500 + sec_for_fill[num]) - 1) * low_random_orders[num] + sec_for_fill[num]))
        for num in range(len(low_random_records)):
            msec_for_record.append((int((1000 - 1) * low_random_records[num] + 1)))
        sec_for_new_record = self.__get_transform_to_record(sec_for_new)
        sec_for_inProcess_record = self.__get_transform_to_record(sec_for_inProcess)
        sec_for_fill_record = self.__get_transform_to_record(sec_for_fill)
        sec_for_done_record = self.__get_transform_to_record(sec_for_done)
        self.date_sec_for_tag.append(sec_for_new)
        self.date_sec_for_tag.append(sec_for_inProcess)
        self.date_sec_for_tag.append(sec_for_fill)
        self.date_sec_for_tag.append(sec_for_done)
        for num in range(len(low_random_records)):

            if status_num_record[num] == 1:
                self.date_for_record.append((date_init + timedelta(seconds=sec_for_new_record[num],
                                                                   microseconds=msec_for_record[
                                                                                    num] * 1000)).strftime(
                    '%Y-%m-%d %H:%M:%S.%f')[:-3])
            elif status_num_record[num] == 2:
                self.date_for_record.append((date_init + timedelta(seconds=sec_for_inProcess_record[num],
                                                                   microseconds=msec_for_record[
                                                                                    num] * 1000)).strftime(
                    '%Y-%m-%d %H:%M:%S.%f')[:-3])
            elif status_num_record[num] == 3:
                self.date_for_record.append((date_init + timedelta(seconds=sec_for_fill_record[num],
                                                                   microseconds=msec_for_record[
                                                                                    num] * 1000)).strftime(
                    '%Y-%m-%d %H:%M:%S.%f')[:-3])
            else:
                self.date_for_record.append((date_init + timedelta(seconds=sec_for_done_record[num],
                                                                   microseconds=msec_for_record[
                                                                                    num] * 1000)).strftime(
                    '%Y-%m-%d %H:%M:%S.%f')[:-3])

    def __get_transform_to_record(self, inform_record):
        transform = []
        for i in self.id.get_record_row():
            transform.append(inform_record[i - 1])
        return transform

    def getData(self):
        return self.date_for_record

    def get_date_sec_for_tag(self):
        return self.date_sec_for_tag


class Tag(IGenerator):
    def __init__(self, config, date, id):
        self.config = config
        self.date = date
        self.id = id
        self.tag_for_order = []
        self.procces()

    def procces(self):
        lis_tag = self.config.getByName("Tag")
        date_sec_for_tag = self.date.get_date_sec_for_tag()

        for num in range(len(date_sec_for_tag[0])):
            tmp = ""
            for num_list in range(4):
                tmp += (
                    lis_tag[int(str(date_sec_for_tag[num_list][num])[len(str(date_sec_for_tag[num_list][num])) - 1:])])
            self.tag_for_order.append(tmp)
        self.tag_for_order = self.__get_transform_to_record(self.tag_for_order)

    def getData(self):
        return self.tag_for_order

    def __get_transform_to_record(self, inform_record):
        transform = []
        for i in self.id.get_record_row():
            transform.append(inform_record[i - 1])
        return transform

class Note(IGenerator):
    def __init__(self, config, date, id):
        self.config = config
        self.date = date
        self.id = id
        self.note_for_order = []
        self.procces()

    def procces(self):
        list_note = self.config.getByName("Note")
        date_sec_for_note = self.date.get_date_sec_for_tag()
        first_digit = 1
        for num in range(len(date_sec_for_note[0])):
            tmp = ""
            for num_list in range(4):
                tmp += list_note[int(str(date_sec_for_note[num_list][num])[:first_digit])]
            self.note_for_order.append(tmp)
        self.note_for_order = self.__get_transform_to_record(self.note_for_order)


    def getData(self):
        return self.note_for_order

    def __get_transform_to_record(self, inform_record):
        transform = []
        for i in self.id.get_record_row():
            transform.append(inform_record[i - 1])
        return transform

# if __name__ == '__main__':
#     config = Config()
#     id = ID(config)
#    print(id.getData())
#     instrum = Instrument(config,id)
#     a, b, c = instrum.getData()
#     print(a)
#     print(b)
#     print(c)
#    print(instrum.getData())
#     status = Status()
#     volum_init = Volum_init()
#     volum = Volum_fill(config,volum_init,status,id)
#     date = Date(config,id,status)
#     tag = Tag(config, date ,id)
#     note = Note(config,date,id)
#     print(note.getData())
#     print(len(note.getData()))
#     instrument = Instrument()
#     side = Side()
#    print(side.getData())
