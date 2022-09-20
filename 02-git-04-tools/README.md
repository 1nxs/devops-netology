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
# Вариант поиска через merge
$ git show b8d720
commit b8d720f8340221f2146e4e4870bf2ee0bc48f2d5
Merge: 56cd7859e0 9ea88f22fc
$ git show 56cd7859e0
commit 56cd7859e05c36c06b56d013b55a252d0bb7e158
$ git show 9ea88f22fc
commit 9ea88f22fc6269854151c571162c5bcf958bee2b
```
```bash
# Вариант поиска без расследований
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
```bash
# Можно посмотреть лог со скобкой
$ git log -S'func providerSource(' --oneline
8c928e8358 main: Consult local directories as potential mirrors of providers

# А можно покопаться в коде :)
$ git log -S'func providerSource' --oneline
5af1e6234a main: Honor explicit provider_installation CLI config when present
8c928e8358 main: Consult local directories as potential mirrors of providers
# Пытаемся убедиться где создание, а где изменение
$ git show 5af1e6234a
$ git show 8c928e8358
$ git grep "func providerSource"
provider_source.go:func providerSource(configs []*cliconfig.ProviderInstallation, services *disco.Disco) (getproviders.Source, tfdiags.Diagnostics) {
provider_source.go:func providerSourceForCLIConfigLocation(loc cliconfig.ProviderInstallationLocation, services *disco.Disco) (getproviders.Source, tfdiags.Diagnostics) {
$ git log -L :'func providerSource':provider_source.go
~
commit 8c928e83589d90a031f811fae52a81be7153e82f
Author: Martin Atkins <mart@degeneration.co.uk>
Date:   Thu Apr 2 18:04:39 2020 -0700
~
diff --git a/provider_source.go b/provider_source.go
--- /dev/null
+++ b/provider_source.go
# Вот тут видно, что файл появился
```
В коммите `8c928e8358`
6. Найдите все коммиты в которых была изменена функция `globalPluginDirs`.
```bash
# Смотрим где объявили функцию
$ git grep "func globalPluginDirs("
plugins.go:func globalPluginDirs() []string {
# Отбираем коммиты с изменениями
$ git log -s -L :globalPluginDirs:plugins.go --oneline
78b1220558 Remove config.go and update things using its aliases
52dbf94834 keep .terraform.d/plugins for discovery
41ab0aef7a Add missing OS_ARCH dir to global plugin paths
66ebff90cd move some more plugin search path logic to command
8364383c35 Push plugin discovery down into command package
```
7. Кто автор функции `synchronizedWriters`?
```bash
$ git log -S"func synchronizedWriters(" --oneline
bdfea50cc8 remove unused
5ac311e2a9 main: synchronize writes to VT100-faker on Windows
$ git show 5ac311e2a9 # Нашли нужный
commit 5ac311e2a91e381e2f52234668b49ba670aa0fe5
Author: Martin Atkins <mart@degeneration.co.uk>
Date:   Wed May 3 16:25:41 2017 -0700
$ git show bdfea50cc8 # тут удаляли файл..не то

# Проверяем 
$ git log -S'func synchronizedWriters' --pretty=format:'%h - %an %ae'
bdfea50cc8 - James Bardin j.bardin@gmail.com
5ac311e2a9 - Martin Atkins mart@degeneration.co.uk
```
Наш пациент `Martin Atkins mart@degeneration.co.uk`
