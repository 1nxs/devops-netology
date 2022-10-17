#!/usr/bin/env python3
# * исправлен стоковый путь (windows)
# - лишняя логическая переменная is_change
# - команда brake прерывает обработку при первом же найденом вхождении
# + введена переменная пути к папке
# + добавлена проверка на новые файлы

import os
import sys

target = "./"
# Проверка аргумента пути к репозиторию
# Если аргументы введены, то проверяем директорию
if len(sys.argv) >= 2:
    target = sys.argv[1]
    print(f"Requested target path ===> \033[32m {target}" "\033[0m")
# Если директории не существует - завершаем выполнение скрипта с ошибкой
    if not os.path.isdir(target):
        sys.exit("Target path doesn't exist ===>  " "\033[31m" + target +"\033[0m")

bash_command = ["cd "+target, "git status 2>&1"]
# Если это не GIT репозиторий, прерываем скрипт
result_os = os.popen(' && '.join(bash_command)).read()
if result_os.find('not a git') != -1:
    sys.exit("but it's not a git repository :( " "\033[31m" + target +"\033[0m")
#is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '').replace('#','')
        print(os.path.join(target,prepare_result))
        #break
    elif result.find('new file') != -1:
        prepare_result = result.replace('\tnew file:   ', '').replace('#','')
        print(os.path.join(target, prepare_result))