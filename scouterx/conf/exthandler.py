from scouterx.conf.configure import Configure


def load_config_text():
    file_path = Configure.get_conf_file_path()
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        # TODO: logging
        return ""


def save_config_text(text):
    try:
        with open(Configure.get_conf_file_path(), 'w') as file:
            file.write(text)
        return True
    except Exception as e:
        # TODO: logging
        return False
