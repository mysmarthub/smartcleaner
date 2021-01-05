#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details)
# https://github.com/mysmarthub
# Copyright © 2020-2021 Aleksandr Suvorov
# -----------------------------------------------------------------------------
"""Graphical utility for destroying, zeroing, and deleting files,

to complicate or completely impossible to restore them.
"""
import os
import shlex
import sys
import webbrowser

from datetime import datetime

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (QApplication, QFileDialog, QMessageBox, QLabel, QHBoxLayout, QVBoxLayout, QPushButton,
                               QSpinBox, QCheckBox, QTextBrowser, QLCDNumber, QListWidget, QWidget, QAbstractItemView)
from PySide2.QtCore import QThread, Signal


VERSION = '1.1.0'


class PathObj:
    """Creates a path object for the file or folder."""

    @staticmethod
    def files_path_gen(path):
        return (os.path.join(p, file) for p, _, files in os.walk(path) for file in files)

    @staticmethod
    def dirs_path_gen(path):
        return (os.path.join(p, d) for p, dirs, _ in os.walk(path) for d in dirs)

    @staticmethod
    def get_num_of_dirs(path):
        return sum([len(dirs) for _, dirs, _ in os.walk(path)])

    @staticmethod
    def get_num_of_files(path):
        return sum([len(files) for _, _, files in os.walk(path)])

    def __init__(self, path: str):
        """When creating an object, you must specify a path that is checked for existence."""
        self.__path = path

    @property
    def path(self):
        """Path to the file or folder"""
        return self.__path

    def get_files(self) -> iter:
        """Returns the file path generator"""
        if os.path.isfile(self.__path):
            return [self.__path]
        elif os.path.isdir(self.__path):
            return (os.path.join(p, file) for p, _, files in os.walk(self.__path) for file in files)
        else:
            return []

    def get_dirs(self) -> iter:
        """Returns the folder path generator"""
        if os.path.isdir(self.path):
            return self.dirs_path_gen(self.__path)
        return []

    @property
    def num_of_files(self):
        return 1 if os.path.isfile(self.__path) else self.get_num_of_files(self.__path)

    @property
    def num_of_dirs(self):
        return self.get_num_of_dirs(self.__path)

    def __str__(self):
        return f'PathObj({self.__path})'


class DataObj:

    def __init__(self):
        self.__objects = {}

    def get_obj_gen(self):
        return (obj for obj in self.__objects.values())

    def get_obj_dict(self):
        return self.__objects

    def add_path(self, path: str) -> bool:
        if os.path.exists(path) and not self.search_for_duplicates(path) and not os.path.islink(path):
            self.__objects[path] = PathObj(path)
            return True
        return False

    def search_for_duplicates(self, path: str) -> bool:
        """Checking for duplicates"""
        return True if path in self.__objects else False

    def del_path(self, path: str) -> bool:
        """Deleting a path object"""
        if self.search_for_duplicates(path):
            del self.__objects[path]
            return True
        return False

    def get_files(self) -> iter:
        """Returns a generator with file paths from all objects"""
        return (file for obj in self.__objects.values() for file in obj.get_files())

    def get_dirs(self) -> iter:
        """Getting folders"""
        return reversed(sorted(path for obj in self.__objects.values() for path in obj.get_dirs()))

    @property
    def is_any_data(self) -> bool:
        """Checking for data in repositories"""
        return True if self.__objects else False

    def clear_data(self) -> None:
        """Clearing storage"""
        self.__objects.clear()


class Cleaner:
    """Creates an object for working with file and folder paths

    for further destruction, zeroing, deleting files. Delete a folder.
    """
    def __init__(self, root=False, shreds=30):
        """Accepts an optional parameter when creating an object shred:

        the number of passes to overwrite the file. By default, 30 passes.
        """
        self.errors = []
        self.root = root
        self.shreds = shreds
        self.count_zero_files = 0
        self.count_del_files = 0
        self.count_del_dirs = 0

    @staticmethod
    def replace_path(path: str) -> str:
        return shlex.quote(path)

    @staticmethod
    def check_exist(path):
        if os.path.exists(path):
            return True
        return False

    def zero_file(self, file: str) -> bool:
        """Resets the file to the specified path"""
        try:
            with open(file, 'wb') as f:
                f.write(bytes(0))
        except OSError:
            self.errors.append(f'Zeroing error: {file}')
            return False
        else:
            self.count_zero_files += 1
            return True

    def shred_file(self, path: str) -> bool:
        """Overwrites and deletes the file at the specified path"""
        rep_path = self.replace_path(path)
        if os.name == 'posix':
            if self.root:
                os.system(f'sudo shred -zvuf -n {self.shreds} {rep_path}')
            else:
                os.system(f'shred -zvu -n {self.shreds} {rep_path}')
        else:
            self.del_file(path)
        if self.check_exist(path):
            self.errors.append(f'Do not shred: {path}')
            return False
        else:
            self.count_del_files += 1
            return True

    def del_file(self, path: str) -> bool:
        """Deletes the file at the specified path using normal deletion"""
        try:
            if os.path.islink(path):
                os.unlink(path)
            else:
                self.zero_file(path)
                os.remove(path)
        except OSError:
            self.errors.append(f'Os error! Do not delete: {path}')
            return False
        if self.check_exist(path):
            self.errors.append(f'Do not delete: {path}')
            return False
        else:
            self.count_del_files += 1
            return True

    def del_dir(self, path: str) -> bool:
        """Deletes an empty folder at the specified path"""
        try:
            if os.path.islink(path):
                os.unlink(path)
            else:
                os.rmdir(path)
        except OSError:
            self.errors.append(f'Os error! Do not delete: {path}')
            return False
        else:
            if self.check_exist(path):
                self.errors.append(f'Do not delete: {path}')
                return False
            else:
                self.count_del_dirs += 1
                return True

    def reset_count(self) -> None:
        """Resetting counters"""
        self.count_zero_files = 0
        self.count_del_files = 0
        self.count_del_dirs = 0

    def reset_error_list(self):
        self.errors.clear()


class SmartCleaner(QThread):
    signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.shreds = 30
        self.delete_a_folder = False
        self.cleaner = Cleaner()
        self.path_data = DataObj()
        self.work_method = None

    def run(self):
        self.cleaner.reset_count()
        self.clear_errors()
        self.cleaner.shreds = self.shreds
        self.emit_msg(f'Smart Cleaner report on the work: {datetime.now()}\n'
                      f' Platform: {"Linux" if os.name == "posix" else "Windows or another"} '
                      f"| Overwrites: {self.cleaner.shreds} ")
        self.from_start()
        if not self.work_method == 'zero' and self.delete_a_folder:
            self.del_dirs()
        self.from_finish()

    def from_start(self):
        for file in self.path_data.get_files():
            self.emit_msg(f'Working with the file: {file}')
            if os.path.exists(file):
                status, msg, err_msg = self.start_method(file)
                self.emit_msg(msg)
                if status:
                    self.emit_msg('Completed!')
                else:
                    self.emit_msg(err_msg)
                self.emit_msg(self.get_counts)
            else:
                self.emit_msg('Error! The file does not exist!')

    def from_finish(self):
        if self.cleaner.errors:
            self.emit_msg(f'Errors: {len(self.cleaner.errors)}')
            for err in self.cleaner.errors:
                self.emit_msg(err)
        if self.work_method == 'zero':
            self.emit_msg(f'Reset completed. Reset files: {self.cleaner.count_zero_files} '
                          f'| Errors: {len(self.cleaner.errors)}')
        else:
            self.emit_msg(f'The deletion is complete. Deleted files: {self.cleaner.count_del_files} '
                          f'| Deleted folders: {self.cleaner.count_del_dirs} '
                          f'| Errors: {len(self.cleaner.errors)}')
            self.path_data.clear_data()

    def start_method(self, file):
        if self.work_method == 'zero':
            status = self.cleaner.zero_file(file)
            msg = f'Zeroing the file: {file}'
            err_msg = 'Error updating the file!'
        elif self.work_method == 'shred':
            status = self.cleaner.shred_file(file)
            msg = f'Mashing the file: {file}'
            err_msg = 'Error when deleting the file!'
        else:
            status = self.cleaner.del_file(file)
            msg = f'Delete file: {file}'
            err_msg = 'Error deleting a file'
        return status, msg, err_msg

    @property
    def get_counts(self):
        if self.work_method == 'zero':
            return f'Reset files: {self.cleaner.count_zero_files} ' \
                   f'| Errors: {self.num_errors}'
        elif self.work_method == 'shred':
            return f'Destroyed files: {self.cleaner.count_del_files} ' \
                   f'| Errors: {self.num_errors}'
        else:
            return f'Deleted files: {self.cleaner.count_del_files} ' \
                   f'| Errors: {self.num_errors}'

    def del_dirs(self):
        for path in (self.path_data.get_dirs()):
            self.emit_msg(f'Deleting a folder: {path}')
            if os.path.exists(path):
                if self.cleaner.del_dir(path):
                    self.emit_msg('Completed!')
                else:
                    self.emit_msg('Error when deleting a folder!')
            else:
                self.emit_msg('Error! The folder does not exist!')
            self.emit_msg(f'Deleted folders: {self.cleaner.count_del_dirs} '
                          f'| Errors: {self.num_errors}')

    def emit_msg(self, msg):
        self.signal.emit(msg)

    def get_errors(self) -> list:
        return self.cleaner.errors

    def clear_errors(self) -> None:
        self.cleaner.reset_error_list()

    @property
    def num_errors(self) -> int:
        return len(self.cleaner.errors)


class MyWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Graphical utility for destroying, zeroing, and deleting files')

        self.label_donate = QLabel('Copyright (c) 2021, Aleksandr Suvorov | Donate: 4048 4150 0400 5852')
        self.label_donate.setAlignment(Qt.AlignCenter)

        self.label_logo = QLabel(f'Smart Cleaner<sup> {VERSION}</sup>')
        self.label_logo.setAlignment(Qt.AlignCenter)
        self.label_logo.setStyleSheet('font-size: 48px;')

        self.label_files = QLabel('Files')
        self.label_files.setStyleSheet("color: rgb(84, 180, 40);")

        self.label_dirs = QLabel('Folders')
        self.label_dirs.setStyleSheet("color: rgb(177, 98, 42);")

        self.label_errors = QLabel('Errors')
        self.label_errors.setStyleSheet("color: rgb(255, 68, 44);")

        self.lcd_files = QLCDNumber()
        self.lcd_files.setSegmentStyle(QLCDNumber.Flat)
        self.lcd_files.setStyleSheet("color: rgb(84, 180, 40);")
        self.lcd_dirs = QLCDNumber()
        self.lcd_dirs.setSegmentStyle(QLCDNumber.Flat)
        self.lcd_dirs.setStyleSheet("color: rgb(177, 98, 42);")
        self.lcd_errors = QLCDNumber()
        self.lcd_errors.setSegmentStyle(QLCDNumber.Flat)
        self.lcd_errors.setMinimumHeight(30)
        self.lcd_errors.setStyleSheet("color: rgb(255, 68, 44);")
        self.lcd_files.setDigitCount(15)
        self.lcd_dirs.setDigitCount(15)
        self.lcd_errors.setDigitCount(15)

        self.h_box1 = QHBoxLayout()
        self.h_box1.addWidget(self.label_dirs)
        self.h_box1.addWidget(self.label_files)
        self.h_box1.addWidget(self.label_errors)

        self.h_box2 = QHBoxLayout()
        self.h_box2.addWidget(self.lcd_dirs)
        self.h_box2.addWidget(self.lcd_files)
        self.h_box2.addWidget(self.lcd_errors)

        self.label_cons = QLabel('Information console:')

        self.text_browser = QTextBrowser()
        self.text_browser.setText(f'Smart Cleaner v{VERSION} \nUtility for overwriting, zeroing, and deleting files\n'
                                  f'https://github.com/mysmarthub')

        self.btn_console_clear = QPushButton('Reset')
        self.btn_donate = QPushButton('Donate | Sberbank 4276 4417 5763 7686')
        self.btn_donate.setToolTip('We will be grateful for any financial support.\nThis will help the program '
                                   'develop and remain free.\nThanks!')
        self.btn_exit = QPushButton('Exit')

        self.h_box3 = QHBoxLayout()
        self.h_box3.addWidget(self.btn_donate)
        self.h_box3.addStretch(1)
        self.h_box3.addWidget(self.btn_console_clear)

        self.chb_del_dirs = QCheckBox('Delete folders')
        self.chb_del_dirs.setChecked(True)

        self.label_shred = QLabel('Rewrite:')

        self.spin_box = QSpinBox()
        self.spin_box.setMinimum(1)
        self.spin_box.setMaximum(1000)
        self.spin_box.setValue(30)

        self.h_box4 = QHBoxLayout()
        self.h_box4.addWidget(self.chb_del_dirs)
        self.h_box4.addWidget(self.label_shred)
        self.h_box4.addWidget(self.spin_box)
        self.h_box4.addStretch(1)

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.btn_add_folder = QPushButton('+ Folder')
        self.btn_add_files = QPushButton('+ Files')
        self.btn_remove_item = QPushButton('- Remove')
        self.btn_zero_files = QPushButton('Zeroing')
        self.btn_shred_files = QPushButton('Erasing')
        self.btn_del_files = QPushButton('Delete')

        self.h_box5 = QHBoxLayout()
        self.h_box5.addWidget(self.btn_add_folder)
        self.h_box5.addWidget(self.btn_add_files)
        self.h_box5.addWidget(self.btn_remove_item)
        self.h_box5.addStretch(1)
        self.h_box5.addWidget(self.btn_shred_files)
        self.h_box5.addWidget(self.btn_zero_files)
        self.h_box5.addWidget(self.btn_del_files)
        self.h_box5.addWidget(self.btn_exit)

        self.v_box = QVBoxLayout()
        self.v_box.addWidget(self.label_logo)
        self.v_box.addLayout(self.h_box1)
        self.v_box.addLayout(self.h_box2)
        self.v_box.addWidget(self.label_cons)
        self.v_box.addWidget(self.text_browser)
        self.v_box.addLayout(self.h_box3)
        self.v_box.addLayout(self.h_box4)
        self.v_box.addWidget(self.list_widget)
        self.v_box.addLayout(self.h_box5)
        self.v_box.addWidget(self.label_donate)

        self.setLayout(self.v_box)

        self.smart_cleaner = SmartCleaner()

        self.btn_donate.clicked.connect(lambda: webbrowser.open('https://yoomoney.ru/to/4100115206129186'))
        self.btn_console_clear.clicked.connect(self.clear_console)
        self.btn_add_folder.clicked.connect(self.add_dir)
        self.btn_add_files.clicked.connect(self.add_files)
        self.btn_remove_item.clicked.connect(self.remove_items)
        self.btn_shred_files.clicked.connect(self.shred_start)
        self.btn_zero_files.clicked.connect(self.zeroing_start)
        self.btn_del_files.clicked.connect(self.delete_start)
        self.btn_exit.clicked.connect(self.close)
        self.smart_cleaner.signal.connect(self.update_information)
        self.smart_cleaner.started.connect(self.at_start)
        self.smart_cleaner.finished.connect(self.at_finish)

    def clear_console(self):
        self.lcd_dirs.display(0)
        self.lcd_files.display(0)
        self.lcd_errors.display(0)
        self.text_browser.setText(f'Smart Cleaner v{VERSION} \nUtility for overwriting, zeroing, and deleting files\n'
                                  f'https://github.com/mysmarthub')

    def add_dir(self) -> None:
        path = QFileDialog.getExistingDirectory(self, 'Select the folder to add: ')
        self._add_path(path)

    def add_files(self) -> None:
        path_tuple = QFileDialog.getOpenFileNames(self, 'Select files to add: ')
        for path in path_tuple[0]:
            self._add_path(path)

    def add_item(self, item: str) -> None:
        self.list_widget.addItem(item)

    def remove_items(self) -> None:
        for SelectedItem in self.list_widget.selectedItems():
            self.list_widget.takeItem(self.list_widget.row(SelectedItem))
            self.smart_cleaner.path_data.del_path(SelectedItem.text())
            self.text_browser.append(f'{SelectedItem.text()}\nThe path was successfully deleted!!!')

    def _add_path(self, path: str) -> None:
        if path:
            if self.smart_cleaner.path_data.add_path(path):
                self.add_item(path)
                self.text_browser.append(f'{path}\nThe path was added successfully!')
            else:
                self.text_browser.append(f'Error when adding or the path was added earlier!!!')

    def shred_start(self):
        self.start(method='shred')

    def zeroing_start(self):
        self.start(method='zero')

    def delete_start(self):
        self.start(method='del')

    def start(self, method='shred'):
        if not self.smart_cleaner.path_data.is_any_data:
            self.show_msg('Warning!', 'There is no data for mashing!!!')
        else:
            reply = QMessageBox.question(self, 'Warning!', 'The data will be destroyed, are you sure?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                if method == 'zero':
                    self.text_browser.append('Files are reset to zero.')
                elif method == 'shred':
                    self.text_browser.append('File mashing is started.')
                elif method == 'del':
                    self.text_browser.append('File deletion started.')
                self.smart_cleaner.work_method = method
                self.smart_cleaner.shreds = self.spin_box.value()
                self.smart_cleaner.delete_a_folder = self.chb_del_dirs.isChecked()
                self.smart_cleaner.start()

    def update_information(self, s: str) -> None:
        self.text_browser.append(s)
        self.update_lcd()

    def update_lcd(self) -> None:
        self.lcd_dirs.display(str(self.smart_cleaner.cleaner.count_del_dirs))
        self.lcd_files.display(str(self.smart_cleaner.cleaner.count_del_files))
        self.lcd_errors.display(str(self.smart_cleaner.num_errors))

    def at_start(self):
        self.from_disable(True)

    def at_finish(self) -> None:
        if self.smart_cleaner.work_method != 'zero':
            self.list_widget.clear()
        self.update_lcd()
        self.from_disable(False)
        self.finish_msg()

    def finish_msg(self) -> None:
        if self.smart_cleaner.work_method == 'zero':
            msg = ('Reset', 'Reset files: ')
            count = self.smart_cleaner.cleaner.count_zero_files
        elif self.smart_cleaner.work_method == 'shred':
            msg = ('Mashing', 'Passageways: ')
            count = self.smart_cleaner.cleaner.count_del_files
        else:
            msg = ('Delete', 'Deleted files: ')
            count = self.smart_cleaner.cleaner.count_del_files
        self.show_msg('Warning!',
                      f'{msg[0]} completed successfully!!!\n'
                      f' {msg[1]} {count}\n '
                      f'Deleted folders: {self.smart_cleaner.cleaner.count_del_dirs}\n '
                      f'Errors: {self.smart_cleaner.num_errors}')

    def from_disable(self, status: bool) -> None:
        self.btn_zero_files.setDisabled(status)
        self.btn_remove_item.setDisabled(status)
        self.btn_add_folder.setDisabled(status)
        self.btn_shred_files.setDisabled(status)
        self.btn_console_clear.setDisabled(status)
        self.btn_add_files.setDisabled(status)
        self.btn_del_files.setDisabled(status)
        self.chb_del_dirs.setDisabled(status)
        self.spin_box.setDisabled(status)
        self.list_widget.setDisabled(status)

    def show_msg(self, title: str = 'Warning!', msg: str = 'Message...') -> None:
        QMessageBox.about(self, title, msg)

    def closeEvent(self, event) -> None:
        reply = QMessageBox.question(self, 'Exit', 'Are you sure you want to terminate the program?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.hide()
            self.smart_cleaner.wait(3000)
            event.accept()
        else:
            event.ignore()


def main():
    app = QApplication(sys.argv)
    form = MyWindow()
    form.resize(800, 480)
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
