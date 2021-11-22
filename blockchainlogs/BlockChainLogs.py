import os
import json
import time
import hashlib
import datetime

from pprint import pprint


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
            # check exist file
            path = self._remove_slashes(path=file_path)
            if os.path.exists(path=path) is False:
                self._error = f"(!!) This block not Exist!! Path = {path}."
                return False
            # check first block or not
            with open(file=path, mode="rb") as file:
                if json.load(file)['hash'] == "0000000000000":
                    self._error = "(!!) This First Block!!"
                    return False

            # get list files in dir where checking files
            path_dir = path[:path.rfind('/')]
            files = self._get_files_in_dir(path=path_dir)

            # Check file one or first in dir
            print(f"path = {path}")
            print(f"path_dir = {path_dir}")
            if len(files) == 1 or files.index(path[len(path_dir)+1:]) == 0:
                file_prev = ''
                finder = {
                    "main_dir": path_dir,
                    "current_dir": path_dir,
                    "current_dir_title": path_dir[path_dir.rfind('/')+1:],
                    "list_dirs": self._get_files_in_dir(path=path_dir[:path_dir.rfind('/')]),
                    "previous_dir_title": '',
                    "list_previous_dir": list(),
                }
                pprint(finder)
                # find previous dir with files
                while len(finder["list_previous_dir"]) == 0:
                    print("One file or first in dir-----------")
                    if finder["list_dirs"].index(finder["current_dir_title"]) == 0:
                        print("---------------------------------")
                        finder["current_dir"] = finder["current_dir"][:finder["current_dir"].rfind('/')]
                        dir_previous = finder["current_dir"][finder["current_dir"].rfind('/')+1:]
                        if dir_previous == 'logs':
                            self._error = "(!!) Not files!!"
                            return False
                        finder["current_dir"] = finder["current_dir"][:finder["current_dir"].rfind('/')]
                        list_dirs = self._get_files_in_dir(path=finder["current_dir"])
                        finder["current_dir"] = finder["current_dir"] + '/' + list_dirs[list_dirs.index(dir_previous)-1]
                        print(f'finder["current_dir"] = {finder["current_dir"]}')
                    finder["list_dirs"] = self._get_files_in_dir(path=finder["current_dir"][:finder["current_dir"].rfind('/')])
                    finder["previous_dir_title"] = finder["list_dirs"][finder["list_dirs"].index(finder["current_dir_title"])-1]
                    finder["list_previous_dir"] = self._get_files_in_dir(
                        path=finder["current_dir"][:finder["current_dir"].rfind('/')+1]+finder["previous_dir_title"])
                    finder["current_dir_title"] = finder["previous_dir_title"]
                    finder["current_dir"] = finder["current_dir"][:finder["current_dir"].rfind('/')+1] + finder["previous_dir_title"]
                    pprint(f"finder >>>> {finder}")
                    time.sleep(0.5)
                return self._check_block_and_previous(block_current=path,
                                                      block_previous=finder["current_dir"] + '/'
                                                                     + finder["list_previous_dir"][-1])
            else:
                index_check_file = files.index(path[len(path_dir)+1:])
                file_prev = path_dir + '/' + files[index_check_file-1]
                return self._check_block_and_previous(block_current=path, block_previous=file_prev)
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

    def _check_block_and_previous(self, block_current: str = "", block_previous: str = "") -> bool:
        """

        :param block_current:
        :param block_previous:
        :return:
        """
        print(f"block_current = {block_current}")
        print(f"block_previous = {block_previous}")
        hash_prev_file = self.get_hash_file(file_name=block_previous)
        with open(file=block_current, mode="rb") as file:
            hash_prev_from_current_block = json.load(file)['hash']
        if hash_prev_file == hash_prev_from_current_block:
            return True
        else:
            return False

    # ###################### SERVICE___END ######################
