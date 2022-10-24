from typing import TYPE_CHECKING
import gspread

if TYPE_CHECKING:
    from app.globals import MyApp

class GoogleDatabase:
    gp: gspread.Client
    configs_table: gspread.Worksheet
    orders_table: gspread.Worksheet

    def autorize(self,  app: "MyApp"):
        self.gp = gspread.service_account(filename=app.config.google.cred_file)
        self.configs_table = self.gp.open_by_key(app.config.google.configs_table).sheet1  # подключаем таблицу по ID
        self.orders_table = self.gp.open_by_key(app.config.google.orders_table).sheet1

    def gett_last_used_conf(self):
        """ Получает номер последнего использованного конфиг файла"""

        data = self.configs_table.get_all_records()
        last_order = 1
        last_conf = 1
        for conf_file in data: # читаем со второй сроки, в первой имена столбцов
            last_conf +=1
            if conf_file["ORDER_ID"]:
                last_order = conf_file["ORDER_ID"]
            else:
                break
        return last_order, last_conf


       


