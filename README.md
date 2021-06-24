# Smart Cleaner

***

> Graphical utility for destroying, zeroing, and deleting files, 
> to complicate or completely impossible to restore them.

- [Shred](https://github.com/smartlegion/shred/) - A package of modules for destroying files.
- [Shredi](https://github.com/smartlegion/shredi/) - Console utility for destroying files. Secure file overwriting, deletion, and destruction, both in manual and automatic modes, * without the possibility of recovery.

***

[![PyPI - Downloads](https://img.shields.io/pypi/dm/smartcleaner?label=pypi%20downloads)](https://pypi.org/project/smartcleaner)
[![PyPI](https://img.shields.io/pypi/v/smartcleaner)](https://pypi.org/project/smartcleaner)
[![PyPI - Format](https://img.shields.io/pypi/format/smartcleaner)](https://pypi.org/project/smartcleaner)
[![GitHub](https://img.shields.io/github/license/mysmarthub/smartcleaner)](https://github.com/mysmarthub/smartcleaner)
[![GitHub Repo stars](https://img.shields.io/github/stars/mysmarthub/smartcleaner?style=social)](https://github.com/mysmarthub/smartcleaner)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/mysmarthub/smartcleaner)](https://github.com/mysmarthub/smartcleaner)

[![Download Smart Cleaner](https://a.fsdn.com/con/app/sf-download-button)](https://sourceforge.net/projects/smartcleaner/files/latest/download)
[![Download Smart Cleaner](https://img.shields.io/sourceforge/dt/smartcleaner.svg)](https://sourceforge.net/projects/smartcleaner/files/latest/download)

---

Smart Cleaner (Windows version) download smart_cleaner.exe:
---

[![Download Smart Cleaner (For Windows)](https://a.fsdn.com/con/app/sf-download-button)](https://sourceforge.net/projects/smart-cleaner-for-windows/files/latest/download)
[![Download Smart Cleaner (For Windows)](https://img.shields.io/sourceforge/dt/smart-cleaner-for-windows.svg)](https://sourceforge.net/projects/smart-cleaner-for-windows/files/latest/download)

---

![Smart Cleaner](https://github.com/mysmarthub/smartcleaner/raw/master/images/smart_cleaner_logo.png)

---

# Help the project financially:

- Yandex Money: https://yoomoney.ru/to/4100115206129186

- Visa: `4048 0250 0089 5923`

- https://paypal.me/myhackband

***

# Description:


___Warning:___

__Be extremely careful when working with the utility. 
Destroyed data cannot be restored!__

If you add a folder, all nested files in all nested folders 
will be destroyed recursively!

The program allows you to:

- Moving through the file system, add and exclude files 
and folders for further work with them.

- Destroy files by multiple rewrites using shred on Linux, 
and the reset and delete method on Windows

- Zeroing files, all information from the file is deleted, 
   the file size is 0b (especially convenient for large files 
   to speed up work, first zeroing, then destroying)

- Reset + delete. Before deleting, 
   all information in the file is erased, 
   the file size becomes 0b, and then the file is deleted.

- Deleting folders after destroying all files in them. 
   (If raw files will remain in some folder, and the folder will not be deleted)

- Displays the number of processed files, folders, and errors.

- Displays information about the work and errors that occurred 
   when working with files and folders in the information console.

- Select the number of file overwrites.

- The program uses [Pyside2](https://github.com/PySide)

> It is recommended to use Smart Cleaner on Linux systems. 
> If you need to destroy files in Windows, 
> you can boot from LiveUSB Linux, run Smart Cleaner, 
> mount the desired disk (read + write) and destroy the files.
> 
> If you have Python installed on your Windows system, 
> you can run Smart Cleaner or install it using pip 
> (you will also need to install dependencies), 
> you can also download [smart_cleaner.exe](https://sourceforge.net/projects/smart-cleaner-for-windows/files/latest/download), 
> it does not require the installation of python and additional libraries. 
> 
> [smart_cleaner.exe](https://sourceforge.net/projects/smart-cleaner-for-windows/files/latest/download) it does not require installation, 
> it is started by double-clicking. 
> Some antivirus programs may show it as a threat, 
> but the code is open and the file does not contain any threats, 
> all this is because the utility goes through 
> folders and performs actions with files.

***

# Help:

You can install the program using pip or pip3:

- `pip3 install smartcleaner`

- `smartcleaner`

>To erase/delete some files, you need to run as an administrator:

- `sudo pip install smartcleaner`

- `sudo smartcleaner`

***

- `sudo apt install git`

- `git clone https://github.com/mysmarthub/smartcleaner.git`

- `pip install -r smartcleaner/requirements.txt`
    
- `python smartcleaner/smartcleaner/smart_cleaner.py` or `python3 smartcleaner/smartcleaner/smart_cleaner.py`

>To erase/delete some files, you need to run as an administrator:

- `sudo pip3 install -r requirements.txt`

- `sudo python smartcleaner/smartcleaner/smart_cleaner.py`

***

# Links:

- [GitHub Smart Cleaner](https://github.com/mysmarthub/smartcleaner)

- [PyPi smartcleaner](https://pypi.org/project/smartcleaner/)

- [Smart Cleaner](https://sourceforge.net/projects/smartcleaner/files/latest/download)

- [Smart Cleaner (For Windows)](https://sourceforge.net/projects/smart-cleaner-for-windows/files/latest/download)

***

# Disclaimer of liability:

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

***

# Requirements:


- The program uses [Pyside2](https://github.com/PySide)

- [Python 3+](https://python.org)

***

# Support:

    Email: mysmarthub@ya.ru
    Copyright © 2020 Aleksandr Suvorov
    
    -----------------------------------------------------------------------------
    Licensed under the terms of the BSD 3-Clause License
    (see LICENSE for details)
    https://github.com/mysmarthub
    Copyright © 2020-2021 Aleksandr Suvorov
    -----------------------------------------------------------------------------

