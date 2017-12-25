import os

import hydra_agent.utils.system
from hydra_agent.ring import Ring
from hydra_agent.utils.system import run_command


class LicenseManager(Ring):
    def __init__(self, config):
        super().__init__(config)

    """Получение лицензии из Центра лицензирования. Если параметр "pin" не установлен, то команда будет ожидать пользовательского ввода.
    
        Описание параметров:
        --apartment <значение>
            Квартира/офис.
        --building <значение>
            Корпус/строение/секция.
        --company <значение>
            Наименование огранизации.
        --country <значение>
            Обязательный параметр Наименование страны.
        --district <значение>
            Наименование района.
        --email <значение>
            Адрес электронной почты пользователя.
        --first-name <значение>
            Имя пользователя.
        --house <значение>
            Номер дома/квартала/владения.
        --last-name <значение>
            Фамилия пользователя.
        --middle-name <значение>
            Отчество пользователя.
        --path <значение>
            Путь к файлам лицензий.
        --pin <значение>
            Пин-код. Если не указано, будет ожидаться ввод пин-кода.
        --previous-pin <значение>
            Старый пин-код. Требуется для повторной регистрации лицензии.
        --region <значение>
            Наименование области/республики/края/штата.
        --serial <значение>
            Обязательный параметр Регистрационный номер.
        --street <значение>
            Обязательный параметр Наименование улицы.
        --town <значение>
            Обязательный параметр Наименование города.
        --validate <значение>
            Задает необходимо ли проверять корректность данных об устройствах, получаемых от системы. По умолчанию данные не проверяются.
        --zip-code <значение>
            Обязательный параметр Почтовый индекс.
    """

    def activate(self, parameters):
        pass

    def get(self, name, path=""):
        """Возвращает файл лицензии

        :param str name: Наименование лицензии
        :param str path: Путь к файлам лицензий
        :return bytes: Файл лицензии
        """
        temp_file = hydra_agent.utils.system.temp_file_name()
        args = [self.path, 'license', 'get', '--name', name.strip(), '--license', temp_file]
        if path:
            args.extend(['--path', path.strip()])
        try:
            run_command(args)
            with open(temp_file, 'rb') as f:
                lic = f.read()
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        return lic

    def info(self, name, path=''):
        """Возвращает информацию о лицензии

        :param str name: Наименование лицензии
        :param str path: Путь к файлам лицензий
        :return str: Информация о лицензии
        """
        args = [self.path, 'license', 'info', '--name', name.strip()]
        if path:
            args.extend(['--path', path.strip()])
        r = run_command(args)
        return r

    def list(self, path=''):
        """Возвращает список установленных лицензий

        :param str path: Путь к файлам лицензий
        :return list: Список установленных лицензий
        """
        args = [self.path, 'license', 'list']
        if path:
            args.extend(['--path', path.strip()])
        r = run_command(args)
        return r.split()

    def put(self, license, path=''):
        """Добавляет файл лицензии

        :param bytes license: Файл лицензии
        :param str path: Путь к файлам лицензий
        :return boolean: Результат добавления
        """
        license_file = hydra_agent.utils.system.temp_file_name()
        with open(license_file, 'wb') as f:
            f.write(license)
        args = [self.path, 'license', 'put', '--license', license_file]
        if path:
            args.extend(['--path', path.strip()])
        try:
            run_command(args)
        finally:
            if os.path.exists(license_file):
                os.remove(license_file)
        return True

    def remove(self, name, path=''):
        """Удаляет лицензии

        :param str name: Наименование лицензии
        :param str path: Путь к файлам лицензий
        :return boolean: Результат удаления
        """
        args = [self.path, 'license', 'remove', '--name', name.strip(), '--all']
        if path:
            args.extend(['--path', path.strip()])
        run_command(args)
        return True

    def validate(self, name, path=''):
        """Возвращает список установленных лицензий

        :param str name: Наименование лицензии
        :param str path: Путь к файлам лицензий
        :return boolean: Результат проверки
        """
        args = [self.path, 'license', 'validate', '--name', name.strip()]
        if path:
            args.extend(['--path', path.strip()])
        run_command(args)
        return True