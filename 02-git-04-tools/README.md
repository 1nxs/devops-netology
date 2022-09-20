# Домашнее задание к занятию «2.4. Инструменты Git»

1. Найдите полный хеш и комментарий коммита, хеш которого начинается на `aefea`.

```bash
$ git show -s --format="%H %B" aefea
aefead2207ef7e2aa5dc81a34aedf0cad4c32545 Update CHANGELOG.md

$ git show aefea
commit aefead2207ef7e2aa5dc81a34aedf0cad4c32545
Author: Alisdair McDiarmid <alisdair@users.noreply.github.com>
Date:   Thu Jun 18 10:29:58 2020 -0400

    Update CHANGELOG.md
```

2. Какому тегу соответствует коммит `85024d3`?

```bash
$ git show 85024d3 --pretty
commit 85024d3100126de36331c6982bfaac02cdab9e76 (tag: v0.12.23)
```

3. Сколько родителей у коммита `b8d720`? Напишите их хеши.
```bash
#Вариант поиска через merge
$ git show b8d720
commit b8d720f8340221f2146e4e4870bf2ee0bc48f2d5
Merge: 56cd7859e0 9ea88f22fc
$ git show 56cd7859e0
commit 56cd7859e05c36c06b56d013b55a252d0bb7e158
$ git show 9ea88f22fc
commit 9ea88f22fc6269854151c571162c5bcf958bee2b
```
```bash
#Вариант поиска без расследований
$ git show --pretty=%P b8d720
56cd7859e05c36c06b56d013b55a252d0bb7e158 9ea88f22fc6269854151c571162c5bcf958bee2b
```
   Два родителя `56cd7859e05c36c06b56d013b55a252d0bb7e158` и `9ea88f22fc6269854151c571162c5bcf958bee2b`
4. Перечислите хеши и комментарии всех коммитов которые были сделаны между тегами  v0.12.23 и v0.12.24.
```bash
$ git log  v0.12.23..v0.12.24  --oneline
33ff1c03bb (tag: v0.12.24) v0.12.24
b14b74c493 [Website] vmc provider links
3f235065b9 Update CHANGELOG.md
6ae64e247b registry: Fix panic when server is unreachable
5c619ca1ba website: Remove links to the getting started guide's old location
06275647e2 Update CHANGELOG.md
d5f9411f51 command: Fix bug when using terraform login on Windows
4b6d06cc5d Update CHANGELOG.md
dd01a35078 Update CHANGELOG.md
225466bc3e Cleanup after v0.12.23 release
```
5. Найдите коммит в котором была создана функция `func providerSource`, ее определение в коде выглядит

так `func providerSource(...)` (вместо троеточего перечислены аргументы).
6. Найдите все коммиты в которых была изменена функция `globalPluginDirs`.
7. Кто автор функции `synchronizedWriters`?
