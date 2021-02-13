# Virtualbox

Assume the guest uses the network connection of the host system: Usage of network setting `NAT`.

## Export and import

- Appliance export: `*.ova` files
- Appliance import: Set option `Renew MAC-addresses`

### Network problems
If virtualbox guest system has network problems: Loggin als `root` and:
`mv /etc/udev/rules.d/70-persistent-net.rules /etc/udev/rules.d/70-persistent-net.rules.BACK && reboot`

## Remote access

* Stop VM
* Edit port forwarting in the VM manager: E.g. local port `2222` to remote port `22`
* Start VM
* Connect from host system to guest system via ssh: `ssh -p2222 chris@localhost`

### Requirements
* It is necessary that all echos and prints in .dotfiles are deactivated to avoid SCP error.
* `.bashrc` must not be sourced when shell is not running interactively.
* [SCP broken](https://superuser.com/questions/256530/scp-protocol-error-bad-mode)
* [Shell interactive](https://stackoverflow.com/questions/12440287/scp-doesnt-work-when-echo-in-bashrc/12442753#12442753)

### SCP local to remote
`scp -P 2222 /home/chris/local-test-file  chris@localhost:/home/chris/`

### SCP remote to local
`scp -P 2222 chris@localhost:/home/chris/remote-test-file .`


## Remote execution

### Local execution of remote commands

```bash
ssh -p2222 chris@localhost ls
chris@localhost's password:
CentOS Linux 7 (Core) running on vm
bin
howto
```

### Local execution of local scripts

[Execute local script and parameters on remote machine](https://unix.stackexchange.com/a/87406/314714)

```bash
ssh -p2222 chris@localhost "bash -s" -- < /path/to_local/bin/executable.sh [parameter]
chris@localhost's password:
CentOS Linux 7 (Core) running on vm
...
```

## VirtualBox guest additions

The installation of the guest additions is a requirement for having shared folder with the host system!

* Stop virtualbox
* Setting -> Storage -> Create new optical device controller
* Start virtualbox again
* Select `Devices` -> `Insert Guest Additions CD image...` (in running virtualbox window menu)
* Execute the following commands:

* Preconditions

```bash
rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
yum install perl gcc dkms kernel-devel kernel-headers make bzip2
yum update
```

* Installation of guest additions

```bash
mkdir -p /media/cdrom
mount /dev/sr0 /media/cdrom

mount: /dev/sr0 is write-protected, mounting read-only
sh /media/cdrom/VBoxLinuxAdditions.run
Verifying archive integrity... All good.
Uncompressing VirtualBox 6.0.22 Guest Additions for Linux........
VirtualBox Guest Additions installer
Copying additional installer modules ...
Installing additional modules ...
VirtualBox Guest Additions: Starting.
VirtualBox Guest Additions: Building the VirtualBox Guest Additions kernel 
modules.  This may take a while.
VirtualBox Guest Additions: To build modules for other installed kernels, run
VirtualBox Guest Additions:   /sbin/rcvboxadd quicksetup <version>
VirtualBox Guest Additions: or
VirtualBox Guest Additions:   /sbin/rcvboxadd quicksetup all
VirtualBox Guest Additions: Building the modules for kernel 
3.10.0-1127.13.1.el7.x86_64.

reboot
```

* Guest additions CD can be unmounted.

Now, there is a shared folder in the `/media` directory:
```bash
ll /media/sf_vbox_share
total 4
drwxrwx---. 1 root vboxsf 4096 Aug 23  2019 apache_www-ub-2018.aau.at/
-rwxrwx---. 1 root vboxsf    0 May  5  2019 test*
```

# Problems

From time to time - after many Linux Kernel updates - it may happen that the Virtualbox cannot run any Images.
The solution is to uninstall the current version and install the new version of Virtualbox:

1. Find Virtualbox packages on your system: `rpm -qa | ack -i virtual`.
2. Remove Packages: `dnf remove virtualbox-guest-additions-6.1.14-1.fc31.x86_64 VirtualBox-6.0-6.0.24_139119_fedora31-1.x86_64`.
3. Download new version + extension.
4. Install new version: `dnf install ~chris/Downloads/VirtualBox-6.1-6.1.16_140961_fedora31-1.x86_64.rpm`
5. Start Virtualbox and run Images :)


# Resize disk space of an virtual box drive

## on the host system

Reference: [virtualbox-clone-fixed-to-dynamic](https://gist.github.com/stormwild/6403128)

NOTE: Virtualbox must not be running!

1. Go into root-dir of the virtual machine: `cd ~/vbox_machines/CentOS-7.6-Minimal`
2. Create backup: `cd CentOS-7.6-Minimal-disk001.vdi CentOS-7.6-Minimal-disk001.vdi.backup`
3. Clone disk: `VBoxManage clonehd CentOS-7.6-Minimal-disk001.vdi CentOS-7.6-Minimal-disk-var.vdi --variant Standard`
4. Resize disk: `VBoxManage modifyhd CentOS-7.6-Minimal-disk-var.vdi --resize 16000`
5. Switch disk: VBox -> Settings -> Storage -> Select Disk -> Storage Devices: select disk -> Attributes: Choose new file `CentOS-7.6-Minimal-disk-var.vdi`
6. Start image

## on guest system

References:
* [Logical Volume Manager: How can I extend a Volume Group?](https://www.howtoforge.com/logical-volume-manager-how-can-i-extend-a-volume-group)
* [How to create primary partition using fdisk](https://www.thegeekdiary.com/linux-unix-how-to-create-primary-partition-using-fdisk/)

NOTE: All oerations need root privilegues!

* There is free disk space available

```bash
# fdisk -l

Disk /dev/sda: 16.8 GB, 16777216000 bytes, 32768000 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk label type: dos
Disk identifier: 0x000afdbc

   Device Boot      Start         End      Blocks   Id  System
/dev/sda1   *        2048     2099199     1048576   83  Linux
/dev/sda2         2099200    16777215     7339008   8e  Linux LVM
```

* But not uses:

```bash
# vgdisplay
  --- Volume group ---
  VG Name               centos
  System ID
  Format                lvm2
  Metadata Areas        1
  Metadata Sequence No  3
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                2
  Open LV               2
  Max PV                0
  Cur PV                1
  Act PV                1
  VG Size               <7.00 GiB
  PE Size               4.00 MiB
  Total PE              1791
  Alloc PE / Size       1791 / <7.00 GiB
  Free  PE / Size       0 / 0
  VG UUID               Gppbl7-jFG5-fRkG-MDvu-kWGg-kGHc-G6OWDO
```
And the free space is not usable yet...

* Create new primary partition:

Use all free space...

```bash
# fdisk /dev/sda
Welcome to fdisk (util-linux 2.23.2).

Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.


Command (m for help): m
Command action
   a   toggle a bootable flag
   b   edit bsd disklabel
   c   toggle the dos compatibility flag
   d   delete a partition
   g   create a new empty GPT partition table
   G   create an IRIX (SGI) partition table
   l   list known partition types
   m   print this menu
   n   add a new partition
   o   create a new empty DOS partition table
   p   print the partition table
   q   quit without saving changes
   s   create a new empty Sun disklabel
   t   change a partition's system id
   u   change display/entry units
   v   verify the partition table
   w   write table to disk and exit
   x   extra functionality (experts only)

Command (m for help): n
Partition type:
   p   primary (2 primary, 0 extended, 2 free)
   e   extended
Select (default p): p
Partition number (3,4, default 3):
First sector (16777216-32767999, default 16777216):
Using default value 16777216
Last sector, +sectors or +size{K,M,G} (16777216-32767999, default 32767999):
Using default value 32767999
Partition 3 of type Linux and of size 7.6 GiB is set

Command (m for help): p

Disk /dev/sda: 16.8 GB, 16777216000 bytes, 32768000 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk label type: dos
Disk identifier: 0x000afdbc

   Device Boot      Start         End      Blocks   Id  System
/dev/sda1   *        2048     2099199     1048576   83  Linux
/dev/sda2         2099200    16777215     7339008   8e  Linux LVM
/dev/sda3        16777216    32767999     7995392   83  Linux

Command (m for help): w
The partition table has been altered!

Calling ioctl() to re-read partition table.

WARNING: Re-reading the partition table failed with error 16: Device or resource busy.
The kernel still uses the old table. The new table will be used at
the next reboot or after you run partprobe(8) or kpartx(8)
Syncing disks.
```

* The new partition will be listet:

```bash
# fdisk -l

Disk /dev/sda: 16.8 GB, 16777216000 bytes, 32768000 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk label type: dos
Disk identifier: 0x000afdbc

   Device Boot      Start         End      Blocks   Id  System
/dev/sda1   *        2048     2099199     1048576   83  Linux
/dev/sda2         2099200    16777215     7339008   8e  Linux LVM
/dev/sda3        16777216    32767999     7995392   83  Linux
```

* Change the type of the new partition to `8e`:

```bash
fdisk /dev/sda
Welcome to fdisk (util-linux 2.23.2).

Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Command (m for help): t
Partition number (1-3, default 3): 3
Hex code (type L to list all codes): 8e
Changed type of partition 'Linux' to 'Linux LVM'

Command (m for help): w
The partition table has been altered!

Calling ioctl() to re-read partition table.

WARNING: Re-reading the partition table failed with error 16: Device or resource busy.
The kernel still uses the old table. The new table will be used at
the next reboot or after you run partprobe(8) or kpartx(8)
Syncing disks.
```

* The new partition will be listet:

```bash
# fdisk -l

Disk /dev/sda: 16.8 GB, 16777216000 bytes, 32768000 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk label type: dos
Disk identifier: 0x000afdbc

   Device Boot      Start         End      Blocks   Id  System
/dev/sda1   *        2048     2099199     1048576   83  Linux
/dev/sda2         2099200    16777215     7339008   8e  Linux LVM
/dev/sda3        16777216    32767999     7995392   8e  Linux LVM
```

NOTE: The modified partition table cannot be scanned right now!

* Run the `partprobe` command to scan the newly modified partition table: 

```bash
# partprobe
```

* Next step is to create a new PV that uses the new created partion:
This step is necessary to add the new PV to the Volume Group later.

```bash
# pvcreate /dev/sda3
  Physical volume "/dev/sda3" successfully created.
```

* Display the new volume group:

```bash
pvdisplay
  --- Physical volume ---
  PV Name               /dev/sda2
  VG Name               centos
  PV Size               <7.00 GiB / not usable 3.00 MiB
  Allocatable           yes (but full)
  PE Size               4.00 MiB
  Total PE              1791
  Free PE               0
  Allocated PE          1791
  PV UUID               EdXtlm-0CBS-Ft2h-WvKY-rOS5-Kxfs-FIYfSR

  "/dev/sda3" is a new physical volume of "7.62 GiB"
  --- NEW Physical volume ---
  PV Name               /dev/sda3
  VG Name
  PV Size               7.62 GiB
  Allocatable           NO
  PE Size               0
  Total PE              0
  Free PE               0
  Allocated PE          0
  PV UUID               DdGxTa-ymCK-08YH-eoGS-qyfk-6HCv-0pCjrl
```

* Extend the volume containing the root:

```bash
# vgextend /dev/centos /dev/sda3
  Volume group "centos" successfully extended

# vgdisplay
  --- Volume group ---
  VG Name               centos
  System ID
  Format                lvm2
  Metadata Areas        2
  Metadata Sequence No  4
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                2
  Open LV               2
  Max PV                0
  Cur PV                2
  Act PV                2
  VG Size               <14.62 GiB
  PE Size               4.00 MiB
  Total PE              3742
  Alloc PE / Size       1791 / <7.00 GiB
  Free  PE / Size       1951 / 7.62 GiB
  VG UUID               Gppbl7-jFG5-fRkG-MDvu-kWGg-kGHc-G6OWDO
```

* Now the root volume can be extended with the full size:

NOTE: Do not forget the `-r` option for cmd `lvextend`!

```bash
# df -h
Filesystem               Size  Used Avail Use% Mounted on
devtmpfs                 484M     0  484M   0% /dev
tmpfs                    496M     0  496M   0% /dev/shm
tmpfs                    496M  6.7M  489M   2% /run
tmpfs                    496M     0  496M   0% /sys/fs/cgroup
/dev/mapper/centos-root  6.2G  3.7G  2.6G  59% /
/dev/sda1               1014M  163M  852M  17% /boot
vbox_share               458G  404G   55G  89% /media/sf_vbox_share
tmpfs                    100M     0  100M   0% /run/user/0

# lvextend -l +100%FREE /dev/mapper/centos-root -r
  Size of logical volume centos/root changed from <6.20 GiB (1586 extents) to <13.82 GiB (3537 extents).
  Logical volume centos/root successfully resized.

# df -h
Filesystem               Size  Used Avail Use% Mounted on
devtmpfs                 484M     0  484M   0% /dev
tmpfs                    496M     0  496M   0% /dev/shm
tmpfs                    496M  6.7M  489M   2% /run
tmpfs                    496M     0  496M   0% /sys/fs/cgroup
/dev/mapper/centos-root   14G  3.7G   11G  27% /
/dev/sda1               1014M  163M  852M  17% /boot
vbox_share               458G  404G   55G  89% /media/sf_vbox_share
tmpfs                    100M     0  100M   0% /run/user/0
```

Now the root volume is resized and ready to use!
