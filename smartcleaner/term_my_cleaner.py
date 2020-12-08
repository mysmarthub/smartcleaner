import sys
import shutil
import os
from pathlib import Path

from mycleaner import cleaner, smart


COLUMNS, _ = shutil.get_terminal_size()


def get_path():
    if len(sys.argv) > 1:
        return [path for path in sys.argv[1:] if Path(path).exists() and (Path(path).is_file() or Path(path).is_dir())]


def make_path_obj(path_list):
    return [smart.PathObj(path_obj) for path_obj in path_list]


def logo_dec(func):
    def deco():
        print('My Cleaner'.center(COLUMNS, '='))
        print('Utility for mashing, zeroing, deleting files'.center(COLUMNS, ' '))
        print('Aleksandr Suvorov | myhackband@ya.ru'.center(COLUMNS, '-'))
        print(''.center(COLUMNS, '='))
        func()
        print(''.center(COLUMNS, '='))
        print('The program is complete'.center(COLUMNS, '-'))
    return deco


@logo_dec
def main():
    print('Adding paths...')
    path_list = get_path()
    if path_list:
        print(f'Added paths: {len(path_list)}')
        print('Looking for files...')
        obj_list = make_path_obj(path_list)
        my_cleaner = cleaner.Cleaner()
        num_files = sum([len(files) for path in path_list for p, _, files in os.walk(path)])
        print(f'Files found: {num_files}')
        print(''.center(COLUMNS, '='))
        while True:
            print('Select the desired action:\n0. Exit\n1. Destruction\n2. Zeroing\n3. Normal deletion')
            print(''.center(COLUMNS, '-'))
            try:
                user_input = int(input('Input: '))
                if user_input not in [0, 1, 2, 3]:
                    raise ValueError
                my_cleaner.shreds = int(input('Enter the number of passes to rewrite: '))
            except ValueError:
                print(''.center(COLUMNS, '-'))
                print('Input error!')
                continue
            else:
                for obj in obj_list:
                    print(f'Working with: {obj.path}'.center(COLUMNS, '='))
                    for file in obj.get_files():
                        if user_input == 1:
                            print(f'Destroying the file: {file}')
                            my_cleaner.shred_file(file)
                        elif user_input == 2:
                            print(f'Resetting the file: {file}')
                            my_cleaner.zero_file(file)
                        elif user_input == 3:
                            print(f'Delete files: {file}')
                            my_cleaner.del_file(file)
            print('The work has been completed'.center(COLUMNS, '='))
            print(f'Files were processed: {my_cleaner.count_del_files + my_cleaner.count_zero_files}')
            break
    else:
        print('Error! No paths found')


if __name__ == '__main__':
    main()
