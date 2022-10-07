# Домашнее задание к занятию "3.5. Файловые системы"

1. Узнайте о [sparse](https://ru.wikipedia.org/wiki/%D0%A0%D0%B0%D0%B7%D1%80%D0%B5%D0%B6%D1%91%D0%BD%D0%BD%D1%8B%D0%B9_%D1%84%D0%B0%D0%B9%D0%BB) (разряженных) файлах.

 - [x] Done\
* это файлы, для которых выделяется пространство на диске только для участков с ненулевыми данными. Экономия, однако.

2. Могут ли файлы, являющиеся жесткой ссылкой на один объект, иметь разные права доступа и владельца? Почему?

* Не могут, так жесткие ссылки имеют один и тот же *индексный дескриптор* `inode` - в нём и хранятся права доступа и имя владельца.

3. Сделайте `vagrant destroy` на имеющийся инстанс Ubuntu. Замените содержимое Vagrantfile следующим:

    ```bash
    Vagrant.configure("2") do |config|
      config.vm.box = "bento/ubuntu-20.04"
      config.vm.provider :virtualbox do |vb|
        lvm_experiments_disk0_path = "/tmp/lvm_experiments_disk0.vmdk"
        lvm_experiments_disk1_path = "/tmp/lvm_experiments_disk1.vmdk"
        vb.customize ['createmedium', '--filename', lvm_experiments_disk0_path, '--size', 2560]
        vb.customize ['createmedium', '--filename', lvm_experiments_disk1_path, '--size', 2560]
        vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 1, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk0_path]
        vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 2, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk1_path]
      end
    end
    ```

    Данная конфигурация создаст новую виртуальную машину с двумя дополнительными неразмеченными дисками по 2.5 Гб.

- [x] Done | [vagrantfile](vagrantfile)

```bash
vagrant@vagrant:~$ lsblk
NAME                      MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
loop0                       7:0    0 67.2M  1 loop /snap/lxd/21835
loop1                       7:1    0 43.6M  1 loop /snap/snapd/14978
loop2                       7:2    0 61.9M  1 loop /snap/core20/1328
loop3                       7:3    0   48M  1 loop /snap/snapd/17029
loop4                       7:4    0 63.2M  1 loop /snap/core20/1623
loop5                       7:5    0 67.8M  1 loop /snap/lxd/22753
sda                         8:0    0   64G  0 disk
├─sda1                      8:1    0    1M  0 part
├─sda2                      8:2    0  1.5G  0 part /boot
└─sda3                      8:3    0 62.5G  0 part
  └─ubuntu--vg-ubuntu--lv 253:0    0 31.3G  0 lvm  /
sdb                         8:16   0  2.5G  0 disk
sdc                         8:32   0  2.5G  0 disk
```

4. Используя `fdisk`, разбейте первый диск на 2 раздела: 2 Гб, оставшееся пространство.

```Bash
vagrant@vagrant:~$ sudo fdisk /dev/sdb

Welcome to fdisk (util-linux 2.34).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Device does not contain a recognized partition table.
Created a new DOS disklabel with disk identifier 0x99e1563b.

Command (m for help): F
Unpartitioned space /dev/sdb: 2.51 GiB, 2683305984 bytes, 5240832 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes

Start     End Sectors  Size
 2048 5242879 5240832  2.5G

Command (m for help): n
Partition type
   p   primary (0 primary, 0 extended, 4 free)
   e   extended (container for logical partitions)
Select (default p): p
Partition number (1-4, default 1):
First sector (2048-5242879, default 2048):
Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-5242879, default 5242879): +2G

Created a new partition 1 of type 'Linux' and of size 2 GiB.

Command (m for help): n
Partition type
   p   primary (1 primary, 0 extended, 3 free)
   e   extended (container for logical partitions)
Select (default p):

Using default response p.
Partition number (2-4, default 2):
First sector (4196352-5242879, default 4196352):
Last sector, +/-sectors or +/-size{K,M,G,T,P} (4196352-5242879, default 5242879):

Created a new partition 2 of type 'Linux' and of size 511 MiB.

Command (m for help): w
The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.

vagrant@vagrant:~$ lsblk
NAME                      MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda                         8:0    0   64G  0 disk
├─sda1                      8:1    0    1M  0 part
├─sda2                      8:2    0  1.5G  0 part /boot
└─sda3                      8:3    0 62.5G  0 part
  └─ubuntu--vg-ubuntu--lv 253:0    0 31.3G  0 lvm  /
sdb                         8:16   0  2.5G  0 disk
├─sdb1                      8:17   0    2G  0 part
└─sdb2                      8:18   0  511M  0 part
sdc                         8:32   0  2.5G  0 disk
```

5. Используя `sfdisk`, перенесите данную таблицу разделов на второй диск.

```bash
vagrant@vagrant:~$ sudo sfdisk -d /dev/sdb > sdb.dump
vagrant@vagrant:~$ sudo sfdisk /dev/sdc < sdb.dump
Checking that no-one is using this disk right now ... OK
---
Device     Boot   Start     End Sectors  Size Id Type
/dev/sdc1          2048 4196351 4194304    2G 83 Linux
/dev/sdc2       4196352 5242879 1046528  511M 83 Linux
```

6. Соберите `mdadm` RAID1 на паре разделов 2 Гб.

```bash
vagrant@vagrant:~$ sudo mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sd[bc]1
vagrant@vagrant:~$ lsblk
---
sdb                         8:16   0  2.5G  0 disk
├─sdb1                      8:17   0    2G  0 part
│ └─md0                     9:0    0    2G  0 raid1
└─sdb2                      8:18   0  511M  0 part
sdc                         8:32   0  2.5G  0 disk
├─sdc1                      8:33   0    2G  0 part
│ └─md0                     9:0    0    2G  0 raid1
└─sdc2                      8:34   0  511M  0 part
```

7. Соберите `mdadm` RAID0 на второй паре маленьких разделов.
```bash
vagrant@vagrant:~$ sudo mdadm --create /dev/md1 --level=0 --raid-devices=2 /dev/sd[bc]2
vagrant@vagrant:~$ lsblk
---
sdb                         8:16   0  2.5G  0 disk
├─sdb1                      8:17   0    2G  0 part
│ └─md0                     9:0    0    2G  0 raid1
└─sdb2                      8:18   0  511M  0 part
  └─md1                     9:1    0 1018M  0 raid0
sdc                         8:32   0  2.5G  0 disk
├─sdc1                      8:33   0    2G  0 part
│ └─md0                     9:0    0    2G  0 raid1
└─sdc2                      8:34   0  511M  0 part
  └─md1                     9:1    0 1018M  0 raid0

```

8. Создайте 2 независимых PV на получившихся md-устройствах.

```bash
vagrant@vagrant:~$ sudo -i
root@vagrant:~# pvcreate /dev/md0
  Physical volume "/dev/md0" successfully created.
root@vagrant:~# pvcreate /dev/md1
  Physical volume "/dev/md1" successfully created.
root@vagrant:~# pvs
  PV         VG        Fmt  Attr PSize    PFree
  /dev/md0             lvm2 ---    <2.00g   <2.00g
  /dev/md1             lvm2 ---  1018.00m 1018.00m
  /dev/sda3  ubuntu-vg lvm2 a--   <62.50g   31.25g
root@vagrant:~#
```

9. Создайте общую volume-group на этих двух PV.
```bash
root@vagrant:~# vgcreate vg35 /dev/md0 /dev/md1
  Volume group "vg35" successfully created
root@vagrant:~# vgs
  VG        #PV #LV #SN Attr   VSize   VFree
  ubuntu-vg   1   1   0 wz--n- <62.50g 31.25g
  vg35        2   0   0 wz--n-  <2.99g <2.99g
```

10. Создайте LV размером 100 Мб, указав его расположение на PV с RAID0.

```bash
root@vagrant:~# lvcreate -L 100m -n lv35-100 vg35 /dev/md1
  Logical volume "lv35-100" created.
root@vagrant:~# lvs -o +devices
  LV        VG        Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert Devices
  ubuntu-lv ubuntu-vg -wi-ao---- <31.25g                                                     /dev/sda3(0)
  lv35-100  vg35      -wi-a----- 100.00m                                                     /dev/md1(0)
```
11. Создайте `mkfs.ext4` ФС на получившемся LV.

```bash
root@vagrant:~# mkfs.ext4 /dev/vg35/lv35-100
root@vagrant:~# blkid | grep lv35
/dev/mapper/vg35-lv35--100: UUID="818eadea-9e85-4620-a346-a7b4435c9731" TYPE="ext4"
```

12. Смонтируйте этот раздел в любую директорию, например, `/tmp/new`.

```bash
root@vagrant:~# mkdir /tmp/new
root@vagrant:~# mount /dev/mapper/vg35-lv35--100 /tmp/new/

root@vagrant:~# mount | grep vg35
/dev/mapper/vg35-lv35--100 on /tmp/new type ext4 (rw,relatime,stripe=256)
root@vagrant:~#
```

13. Поместите туда тестовый файл, например `wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz`.

```bash
root@vagrant:~# cd /tmp/new/
root@vagrant:/tmp/new# wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz
--2022-10-07 19:58:16--  https://mirror.yandex.ru/ubuntu/ls-lR.gz
Resolving mirror.yandex.ru (mirror.yandex.ru)... 213.180.204.183, 2a02:6b8::183
Connecting to mirror.yandex.ru (mirror.yandex.ru)|213.180.204.183|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 22387291 (21M) [application/octet-stream]
Saving to: ‘/tmp/new/test.gz’

/tmp/new/test.gz               100%[=================================================>]  21.35M  4.49MB/s    in 4.5s

2022-10-07 19:58:21 (4.76 MB/s) - ‘/tmp/new/test.gz’ saved [22387291/22387291]
```

14. Прикрепите вывод `lsblk`.

```bash
root@vagrant:/tmp/new# lsblk
NAME                      MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
sda                         8:0    0   64G  0 disk
├─sda1                      8:1    0    1M  0 part
├─sda2                      8:2    0  1.5G  0 part  /boot
└─sda3                      8:3    0 62.5G  0 part
  └─ubuntu--vg-ubuntu--lv 253:0    0 31.3G  0 lvm   /
sdb                         8:16   0  2.5G  0 disk
├─sdb1                      8:17   0    2G  0 part
│ └─md0                     9:0    0    2G  0 raid1
└─sdb2                      8:18   0  511M  0 part
  └─md1                     9:1    0 1018M  0 raid0
    └─vg35-lv35--100      253:1    0  100M  0 lvm   /tmp/new
sdc                         8:32   0  2.5G  0 disk
├─sdc1                      8:33   0    2G  0 part
│ └─md0                     9:0    0    2G  0 raid1
└─sdc2                      8:34   0  511M  0 part
  └─md1                     9:1    0 1018M  0 raid0
    └─vg35-lv35--100      253:1    0  100M  0 lvm   /tmp/new
```

15. Протестируйте целостность файла:

    ```bash
    root@vagrant:~# gzip -t /tmp/new/test.gz
    root@vagrant:~# echo $?
    0
    ```
```bash
# Test ok
root@vagrant:/tmp/new# gzip -t test.gz
root@vagrant:/tmp/new# echo $?
0
```

16. Используя pvmove, переместите содержимое PV с RAID0 на RAID1.

```bash
root@vagrant:/tmp/new# pvmove -n lv35-100 /dev/md1 /dev/md0
/dev/md1: Moved: 28.00%
/dev/md1: Moved: 100.00%

root@vagrant:/tmp/new# lvs -o +devices
  LV        VG        Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert Devices
  ubuntu-lv ubuntu-vg -wi-ao---- <31.25g                                                     /dev/sda3(0)
  lv35-100  vg35      -wi-ao---- 100.00m                                                     /dev/md0(0)
```

17. Сделайте `--fail` на устройство в вашем RAID1 md.

```shell
root@vagrant:/tmp/new# mdadm --fail /dev/md0 /dev/sdb1
mdadm: set /dev/sdb1 faulty in /dev/md0
```

18. Подтвердите выводом `dmesg`, что RAID1 работает в деградированном состоянии.

```bash
root@vagrant:/tmp/new# dmesg | grep md0 | tail -n 2
[ 6449.720068] md/raid1:md0: Disk failure on sdb1, disabling device.
               md/raid1:md0: Operation continuing on 1 devices.
```

19. Протестируйте целостность файла, несмотря на "сбойный" диск он должен продолжать быть доступен:

    ```bash
    root@vagrant:~# gzip -t /tmp/new/test.gz
    root@vagrant:~# echo $?
    0
    ```
```bash
# Файл всё еще ок
root@vagrant:/tmp/new# gzip -t test.gz
root@vagrant:/tmp/new# echo $?
0
```
20. Погасите тестовый хост, `vagrant destroy`.
- [x] Печеньки захвачены, мой генерал (с)!
