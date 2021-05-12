import requests, zipfile, csv, os
from io import TextIOWrapper
from zda.settings import ZIP_FILE
from datetime import datetime, timedelta
import redis


class Logic:
    def __init__(self):
        print("logic init")
        self.bhav_file_today = self.create_file_name()
        self.client = redis.Redis(host="127.0.0.1", port=6379, db=0)
        self.KEYS = []

    def prev_weekday(self,adate):
        adate -= timedelta(days=1)
        while adate.weekday() > 4:  # Mon-Fri are 0-4
            adate -= timedelta(days=1)
        return adate

    def create_file_name(self):
        print('created file')
        today = datetime.now()
        if today.hour < 18:
            today = self.prev_weekday(today)


        if len(str(today.day)) == 1:
            date_today = "0" + str(today.day)
        else:
            date_today = str(today.day)
        if len(str(today.month)) == 1:
            month_today = "0" + str(today.month)
        else:
            month_today = str(today.month)
        year_today = str(today.year % 100)
        bhav_file = "EQ" + date_today + month_today + year_today + "_CSV.ZIP"
        return bhav_file


    def collect_Bhav_copy_zip(self):
        print('zipcollected')
        bhav_base_url = "https://www.bseindia.com/download/BhavCopy/Equity/"
        headers = {
            "Origin": "https://www.bseindia.com",
            "Referer": "https://www.bseindia.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36",
        }
        link = bhav_base_url + self.bhav_file_today
        csvFile = ZIP_FILE + self.bhav_file_today
        csv_path = csvFile.replace('_CSV.ZIP','.csv')
        #print(csvFile)
        if not os.path.exists(csvFile):
            try:
                #link = bhav_base_url + "EQ060521_CSV.ZIP"
                response = requests.get(link, headers=headers, timeout=10)
                print(link)
                path_to_zip = os.path.join(ZIP_FILE,self.bhav_file_today)
                with open(path_to_zip, "wb") as file:
                    file.write(response.content)
                    file.close()
                with zipfile.ZipFile(path_to_zip, "r") as refFile:
                    for file in refFile.namelist():
                        data = []
                        with refFile.open(file) as final_file:
                            reader = csv.reader(TextIOWrapper(final_file, 'utf-8'))
                            for row in reader:
                                data.append(row)
                        print("ZIP SUCCESSFULLY CREATED")
                        return data
            except Exception as e:
                print('Encountered Exception : ',e)
        print('File Already Exits in database')



    def store_data_redis(self,data):
        if data is not None:
            self.client.flushdb()
            for row in data:
                self.client.hset(str(row[1]),'code', row[0])
                self.client.hset(str(row[1]),'name', row[1])
                self.client.hset(str(row[1]),'open', row[4])
                self.client.hset(str(row[1]),'high', row[5])
                self.client.hset(str(row[1]),'low', row[6])
                self.client.hset(str(row[1]), 'close', row[7])                #print(self.client.hget(row[1],'code'))
           #print(KEYS)

    def run(self):
        print('run in class')
        bhav_obj_data = self.collect_Bhav_copy_zip()
        self.store_data_redis(bhav_obj_data)

def run_logic():                  #runs from shell (only for testing)
    bhav_logic = Logic()
    bhav_logic.run()
