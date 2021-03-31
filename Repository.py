import csv

class Dto:
    def __init__(self, id, instrument, px_init, px_fill, site, volume_init, volum_fill, data, status, note, tag):
        self.id = id
        self.instrument = instrument
        self.px_init = px_init
        self.px_fill = px_fill
        self.site = site
        self.volume_init = volume_init
        self.volum_fill = volum_fill
        self.date = data
        self.status = status
        self.note = note
        self.tag = tag



class Repository:
    dictionary_of_record = None

    def set_to_dictionary(self, dto: Dto):
        self.dictionary_of_record = {'ID': dto.id, 'Instrument': dto.instrument, 'Px_init': dto.px_init, 'Px_fill': dto.px_fill,'Site': dto.site, 'Volume_init': dto.volume_init,
                                     'Volume_fill': dto.volum_fill, 'Date': dto.date, 'Status': dto.status, 'Note': dto.note, 'Tag': dto.tag}

    def to_file_csv(self):
        with open("Table_class.csv", "w") as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow(('ID', 'Instrument', 'Prize', 'Px_fill', 'Site', 'Volume init',
                             'Volume fill', 'Date', 'Status', 'Note', 'Tag'))
            for i in zip(self.dictionary_of_record.get("ID"), self.dictionary_of_record.get("Instrument"), self.dictionary_of_record.get("Px_init"), self.dictionary_of_record.get("Px_fill"),
                         self.dictionary_of_record.get("Site"), self.dictionary_of_record.get("Volume_init"), self.dictionary_of_record.get("Volume_fill"), self.dictionary_of_record.get("Date"),
                         self.dictionary_of_record.get("Status"), self.dictionary_of_record.get("Note"), self.dictionary_of_record.get("Tag")):
                writer.writerow(i)

    def to_DB(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="work",
            password="11Tittim"
        )
        flag = False
        mycursor = mydb.cursor()
        mycursor.execute('USE orders;')
        with open('Table_sort.csv') as f:
            reader = csv.reader(f)

            mycursor.executemany(reader, [])
            for row in reader:
                if not flag:
                    flag = True
                    continue
                mycursor.execute("INSERT INTO orders_history"
                                 "(Serial_num_of_record, ID, Instrument, Px_Init, Px_Fill, Side, Volume_Init, Volume_Fill, Date, Status, Note, Tags)"
                                 "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", row)

        mydb.commit()
        mycursor.close()


    def create_DB(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="work",
            password="11Tittim"
        )

        mycursor = mydb.cursor()
        mycursor.execute(
            'CREATE DATABASE IF NOT EXISTS orders;USE orders;DROP TABLE IF EXISTS orders_history; CREATE TABLE orders_history (Serial_num_of_record INT, ID VARCHAR(10), Instrument VARCHAR(10), Px_Init DOUBLE, Px_Fill DOUBLE, Side VARCHAR(10), Volume_Init DOUBLE, Volume_Fill DOUBLE, Date DATETIME(3), Status VARCHAR(30), Note VARCHAR(255), Tags TEXT);')
        mydb.commit()
        mycursor.close()
        return




