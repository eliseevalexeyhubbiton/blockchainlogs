# import os
from blockchainlogs.BlockChainLogs import BlockChainLogs


def process() -> None:
    """

    :return:
    """
    block = BlockChainLogs()
    # block.add_block(data={"test": "11111"})
    # ch_bl = os.getcwd() + "/logs/2021/11/22" + "/1637532168.197918"
    # ch_bl = os.getcwd() + "/logs/2021/11/22" + "/1637533228.935028"
    # ch_bl = os.getcwd() + "/logs/2021/11/03" + "/1637531834.840508"
    print(block.check_all_blocks())
    # print(block.check_block(file_path=ch_bl))
    # print(block._get_previous_file_in_tree(path=ch_bl))
    print(block.get_error())


if __name__ == '__main__':
    process()
