import os

from blockchainlogs.BlockChainLogs import BlockChainLogs


def process() -> None:
    """

    :return:
    """
    block = BlockChainLogs()
    block.add_block(data={"test": "11111"})
    ch_bl = os.getcwd() + "/logs/2021/11/22" + "/1637532168.197918"
    print(block.check_block(file_path=ch_bl))
    print(block.get_error())


if __name__ == '__main__':
    process()
