# This is a sample Python script.

# Press Alt+Shift+X to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
from os.path import join

import magazines
from aligo import Aligo


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+Shift+B to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ali = Aligo()  # 第一次使用，会弹出二维码，供扫描登录
    user = ali.get_user()  # 获取用户信息
    magazines.fetch_magazines('National+Geographic')
    magazines.fetch_magazines('New+Scientist')
    magazines.fetch_magazines('The+Guardian')

    cd = join(os.path.dirname(__file__), "magazines")
    mm = ali.search_file(
        name='magazines'
    )
    ali.sync_folder(local_folder=cd, remote_folder=mm[0].file_id, flag=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
