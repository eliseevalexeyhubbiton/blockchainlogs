import os
import json
import time
import hashlib
import datetime


class BlockChainLogs:
    _error = ""
    _dir_for_logs = ""

    def __init__(self, dir_logs: str = "") -> None:
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

    def add_block(self, data=None, ) -> None:
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
            path = self._remove_slashes(path=file_path)
            if os.path.exists(path=path) is False:
                self._error = f"(!!) This block not Exist!! Path = {path}."
                return False
            path = path[:path.rfind('/')]
            files = self._get_files_in_dir(path=path)
            if len(files) == 1:
                print("One file")
            else:
                print("files = ", files)
                print("type = ", type(files[0]))
                print("file_path = ", file_path)
                print("file_path[] = ", file_path[file_path.rfind('/')+1:])
                ind = files.index(file_path[file_path.rfind('/')+1:])
                print(f"ind = {ind}")
                file_prev = path + '/' + files[ind-1]
                print(f"file_prev = {file_prev}")
                hash_prev_file = self.get_hash_file(file_name=file_prev)
                print(f"hash_prev_file = {hash_prev_file}")
                hash_prev_from_current_block = ''
                with open(file=file_path, mode="rb") as file:
                    hash_prev_from_current_block = json.load(file)['hash']
                if hash_prev_file == hash_prev_from_current_block:
                    return True
                else:
                    return False
        except Exception as err:
            self._error = err
            return False

    def check_all_blocks(self):
        pass
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
        return sorted([file for file in files])

    # ###################### SERVICE___END ######################
