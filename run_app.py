import os, logging
import sys
from app.globals import app, Config, setup_app
from app.email import send_email
from time import sleep
from app.logger import errors_catching

logging.basicConfig(level=logging.INFO, filename="logs/py_log.log",filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s") 

@errors_catching
def send_config(user):
    print("send mail to "+user["email"])
    app.g_drive.download_conf_file(user["conf"], app)
    to_addr = [user["email"]]
    cc_addr = [app.config.email.email_host_user] 
    subject = "Конфиг для vpn. " + user["conf"]
    file_attach = user["conf"]
    send_email(app, to_addr, subject, file_attach, cc_addr, user["name"])

    app.g_drive.clear_temp()

@errors_catching
def check_orders():
    print("check orders")
    app.database.autorize(app)
    last_order, last_free_conf = app.database.gett_last_used_conf()
    while True:
        last_order += 1
        order = app.database.orders_table.row_values(last_order)
        if order:
            conf = app.database.configs_table.row_values(last_free_conf)
            user = {"name":order[2],"email":order[1],"conf":conf[0]}
            send_config(user)            
            app.database.configs_table.update_cell(last_free_conf, 4, last_order)
            last_free_conf += 1

        else:
            break

@errors_catching
def main():
    conf_file = "config.ini"
    setup_app(os.path.join(os.path.dirname(__file__), conf_file))
    print("Start app")
    while True:
        check_orders()
        sleep(app.config.timeout)



if __name__ == '__main__':
    main()