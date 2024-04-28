from enum import Enum


class TextType(Enum):
    ERROR = "error"
    APICALL = "apicall"
    METHOD = "method"
    SERVICE = "service"
    SQL = "sql"
    OBJECT = "object"
    REFERER = "referer"
    USER_AGENT = "ua"
    GROUP = "group"
    CITY = "city"
    SQL_TABLES = "table"
    MARIA = "maria"
    LOGIN = "login"
    DESC = "desc"
    WEB = "web"
    HASH_MSG = "hmsg"
    STACK_ELEMENT = "stackelem"
