import os
import json
import hashlib
import time


class BlockChainLogs:
    _error = ""
    _dir_for_logs = ""
    _files_template_for_logs = ""

    def __init__(self, dir_logs: str = "", files_logs: str = "") -> None:
        if bool(dir_logs) is False:
            dir_logs = os.getcwd()+"/logs"
        self.dir_logs(dir_logs=dir_logs)
        if bool(files_logs) is False:
            files_logs = ""
        self.files_template_logs(files_logs=files_logs)
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

    def files_template_logs(self, files_logs: str = "") -> str:
        """
        GET or SET for dir_for_logs.
        :param files_logs: if files_logs != '' then GET else SET.
        :return: if GET to dir_for_logs else SET.
        """
        if bool(files_logs) is True:
            self._files_template_for_logs = self._remove_slashes(path=files_logs)
            return ""
        else:
            return self._files_template_for_logs

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
        files = os.listdir(self._dir_for_logs)
        files = sorted([float(file) for file in files])

        if len(files):
            last_file = files[-1]
            prev_hash = self.get_hash_file(file_name=str(last_file))
        else:
            prev_hash = "0000000000000"

        now_time = time.time()
        data = {
            "time": now_time,
            "hash": prev_hash,
            "data": data,
        }

        with open(self._dir_for_logs + str(now_time), mode="w") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

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
        while path.find('/') == 1:
            path = path[1:]
        return '/' + path

    # ###################### SERVICE___END ######################
