from typing import Optional
from dataclasses import dataclass
import configparser

#if TYPE_CHECKING:
from app.g_spread_accessor import GoogleDatabase
from app.g_drive_accessor import GoogleDrive

#Настройки доступа к Гугл диску и таблицам
@dataclass
class GoogleConfig:
    configs_table: str
    orders_table: str
    configs_folder: str
    qr_folder: str
    cred_file: str

# Настройки почтового сервера
@dataclass
class EmailConfig:
    email_host: str
    email_port: int
    email_host_user: str
    email_host_password: str
    email_use_tls: bool
    email_use_ssl: bool
    server_email: str
    default_from_email: str


class Config:
    google: GoogleConfig
    email: EmailConfig
    timeout: int   
    
    def __init__(self, config_path: str):
        # Парсинг файла конфигурации
        raw_config = configparser.ConfigParser()  # создаём объекта парсера
        raw_config.read(config_path)  # читаем конфиг       
        self.google = GoogleConfig(
            configs_table=raw_config["google"]["configs_table"],
            orders_table=raw_config["google"]["orders_table"],
            configs_folder=raw_config["google"]["configs_folder"],
            qr_folder=raw_config["google"]["qr_folder"],
            cred_file=raw_config["google"]["cred_file"],
        )
        self.email = EmailConfig(
            email_host = raw_config["email"]["email_host"],
            email_port = int(raw_config["email"]["email_port"]),
            email_host_user = raw_config["email"]["email_host_user"],
            email_host_password = raw_config["email"]["email_host_password"],
            email_use_tls = raw_config["email"]["email_use_tls"] == "True",
            email_use_ssl = raw_config["email"]["email_use_ssl"] == "True",
            server_email = raw_config["email"]["email_host_user"],
            default_from_email = raw_config["email"]["email_host_user"],
        )
        self.timeout = int(raw_config["common"]["timeout"])*60



class MyApp:
    config: Optional[Config] = None
    database: Optional[GoogleDatabase] = None # менеджер доступа к проекту google
    g_drive: Optional[GoogleDrive] = None # менеджер доступа к диску google        

app = MyApp()

def setup_app(config_path) -> MyApp:
    app.config = Config(config_path) 
    app.database = GoogleDatabase()
    app.g_drive = GoogleDrive(app)    