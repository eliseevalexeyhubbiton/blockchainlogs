import os
import json
import time
import hashlib
import datetime


class BlockChainLogs:
    _debug = False
    _error = ""
    _dir_for_logs = ""

    def __init__(self, dir_logs: str = "", debug: bool = False) -> None:
        self.debug(debug=debug)
        if bool(dir_logs) is False:
            dir_logs = os.getcwd()+"/logs"
        self.dir_logs(dir_logs=dir_logs)
        if os.path.exists(dir_logs) is True:
            if os.path.isdir(dir_logs) is False:
                os.remove(dir_logs)
        else:
            os.mkdir(dir_logs)

    def get_error(self) -> str:
        """
        GET now error.
        :return: Error
        """
        return self._error

    def debug(self, debug: bool = False) -> None:
        """
        GET or SET for dir_for_logs.
        :param debug:
        :return:
        """
        self._debug = debug

    def dir_logs(self, dir_logs: str = "") -> str:
        """
        GET or SET for dir_for_logs.
        :param dir_logs: if dir_logs != '' then GET else SET.
        :return: if GET to dir_for_logs else SET.
        """
        if bool(dir_logs) is True:
            self._dir_for_logs = self._remove_slashes(path=dir_logs)
            return ""
        else:
            return self._dir_for_logs

    def get_hash_file(self, file_name: str = "") -> str:
        """
        GET hash 'file_name'.
        :param file_name: file for calculate HASH.
        :return: HASH 'file_name'.
        """
        self._error = ""
        if bool(file_name) is True:
            try:
                file = open(file=file_name, mode="rb").read()
                return hashlib.md5(file).hexdigest()
            except Exception as err:
                self._error = err
                return ''
        else:
            return ''

    def add_block(self, data=None) -> None:
        """

        :param data:
        :return:
        """
        today = datetime.date.today()
        dir_year = '/' + today.strftime('%Y')
        self._check_or_create_dir(path=self._dir_for_logs + dir_year)
        dir_month = '/' + today.strftime('%m')
        self._check_or_create_dir(path=self._dir_for_logs + dir_year + dir_month)
        dir_day = '/' + today.strftime('%d')
        self._check_or_create_dir(path=self._dir_for_logs + dir_year + dir_month + dir_day)
        dir_current = self._dir_for_logs+dir_year+dir_month+dir_day

        files = self._get_files_in_dir(path=dir_current)

        if len(files):
            last_file = files[-1]
            prev_hash = self.get_hash_file(file_name=dir_current + '/' + str(last_file))
        else:
            prev_hash = "0000000000000"

        now_time = time.time()
        data = {
            "time": now_time,
            "hash": prev_hash,
            "data": data,
        }

        with open(file=dir_current + '/' + str(now_time), mode="w") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def check_block(self, file_path: str = "") -> bool:
        """

        :param file_path:
        :return:
        """
        self._error = ''
        try:
            # check exist file
            path = self._remove_slashes(path=file_path)
            if os.path.exists(path=path) is False:
                self._error = f"(!!) This block not Exist!! Path = {path}."
                return False
            # check first block or not
            with open(file=path, mode="rb") as file:
                if json.load(file)['hash'] == "0000000000000":
                    self._error = "(!!) This First Block!!"
                    return True

            # get list files in dir where checking files
            path_dir = path[:path.rfind('/')]
            files = self._get_files_in_dir(path=path_dir)

            # Check file one or first in dir
            if len(files) == 1 or files.index(path[len(path_dir)+1:]) == 0:
                file_prev = self._get_previous_file_in_tree(path=path)
                if file_prev == '' or file_prev is None:
                    return False
                return self._check_block_and_previous(block_current=path, block_previous=file_prev)
            else:
                index_check_file = files.index(path[len(path_dir)+1:])
                file_prev = path_dir + '/' + files[index_check_file-1]
                return self._check_block_and_previous(block_current=path, block_previous=file_prev)
        except Exception as err:
            self._error = err
            return False

    def check_all_blocks(self) -> bool:
        """

        :return:
        """
        self._error = ''
        dir_logs = self._dir_for_logs
        print(f"{dir_logs=}")
        list_years = self._get_dirs_in_dir(path=dir_logs)
        for current_year in list_years:
            list_month = self._get_dirs_in_dir(path=dir_logs + '/' + current_year)
            for current_month in list_month:
                list_days = self._get_dirs_in_dir(path=dir_logs + '/' + current_year + '/' + current_month)
                for current_day in list_days:
                    list_files = self._get_files_in_dir(
                        path=dir_logs + '/' + current_year + '/' + current_month + '/' + current_day)
                    if len(list_files) > 0:
                        for current_file in list_files:
                            result = self.check_block(file_path=dir_logs + '/' + current_year + '/' + current_month + '/' + current_day + '/' + current_file)
                            if result is False:
                                return False
        return True

    # ###################### SERVICE___BEGIN ######################

    @staticmethod
    def _remove_slashes(path: str = "") -> str:
        """
        Delete slash at start and end. After Add one '/' in start.
        :param path: path for analyzing and edit.
        :return: result after edit.
        """
        if bool(path) is False:
            return ""
        while path.rfind('/') == (len(path) - 1):
            path = path[:-1]
        while path.find('/') == 0:
            path = path[1:]
        return '/' + path

    def _check_or_create_dir(self, path: str = "") -> None:
        """

        :param path:
        :return:
        """
        self._error = ''
        path = self._remove_slashes(path=path)
        try:
            if os.path.exists(path) is True:
                if os.path.isdir(path) is False:
                    os.remove(path)
            else:
                os.mkdir(path)
        except Exception as err:
            self._error = err

    @staticmethod
    def _get_files_in_dir(path: str = "") -> list():
        """

        :param path:
        :return:
        """
        files = os.listdir(path)
        return sorted([file for file in files if os.path.isfile(path + '/' + file)])

    @staticmethod
    def _get_dirs_in_dir(path: str = "") -> list():
        """

        :param path:
        :return:
        """
        dirs = os.listdir(path)
        return sorted([directory for directory in dirs if os.path.isdir(path + '/' + directory)])

    def _check_block_and_previous(self, block_current: str = "", block_previous: str = "") -> bool:
        """

        :param block_current:
        :param block_previous:
        :return:
        """
        if self._debug is True:
            print(f"block_current = {block_current}")
            print(f"block_previous = {block_previous}")
        hash_prev_file = self.get_hash_file(file_name=block_previous)
        with open(file=block_current, mode="rb") as file:
            hash_prev_from_current_block = json.load(file)['hash']
        if hash_prev_file == hash_prev_from_current_block:
            return True
        else:
            return False

    def _get_previous_file_in_tree(self, path: str = '') -> str:
        self._error = ''
        dir_logs = path
        # block_name = dir_logs[dir_logs.rfind('/')+1:]
        dir_logs = dir_logs[:dir_logs.rfind('/')]
        block_day = dir_logs[dir_logs.rfind('/')+1:]
        dir_logs = dir_logs[:dir_logs.rfind('/')]
        block_month = dir_logs[dir_logs.rfind('/')+1:]
        dir_logs = dir_logs[:dir_logs.rfind('/')]
        block_year = dir_logs[dir_logs.rfind('/')+1:]
        dir_logs = dir_logs[:dir_logs.rfind('/')]
        list_years = self._get_dirs_in_dir(path=dir_logs)
        list_years.reverse()
        for current_year in list_years[list_years.index(block_year):]:
            list_month = self._get_dirs_in_dir(path=dir_logs + '/' + current_year)
            list_month.reverse()
            if block_month is not None:
                list_month = list_month[list_month.index(block_month):]
                block_month = None
            for current_month in list_month:
                list_days = self._get_dirs_in_dir(path=dir_logs + '/' + current_year + '/' + current_month)
                list_days.reverse()
                if block_day is not None:
                    list_days = list_days[list_days.index(block_day)+1:]
                    block_day = None
                for current_day in list_days:
                    list_files = self._get_files_in_dir(path=dir_logs + '/' + current_year + '/' + current_month + '/' + current_day)
                    if len(list_files) > 0:
                        return dir_logs + '/' + current_year + '/' + current_month + '/' + current_day + '/' + list_files[-1]
        return ''

    # ###################### SERVICE___END ######################
