# My install process
## Reference - https://wiki.archlinux.org/index.php/Installation_guide
## Steps:
	1. boot with usb
	2. Check keyboard layout (defalut layout was working in small laptop so no need to do anything)
	3. Connect to internet:
		1. ping www.google.com
		2. if command does not work
            iwctl device list 
            iwctl station <device> scan
            iwctl station <device> get-networks
            iwctl --passphrase <passphrase> station <device> connect <SSID>
        3. ping www.google.com
    4. update system clock
        1. Run following:
            timedatectl set-ntp true
            timedatectl status
        2. Change timezone
            timedatectl list-timezones | less
            (find your timezone)
            timedatectl set-timezone <timezone from above command> (Asia/Kolkata in my case)
            timedatectl status
    5. partition the drives:
        1. Run:
            fdisk -l 
            (lists all drives. note the one that you want to use for partitioning)
        2. create partitions (1 for efi-boot, 1 for all data):
            fdisk <path to drive> ( /dev/mmcblk1 )
            m (help)
            g (to create gpt partition table)
            m (help)
            n (new partition)
            1 (partition number)
            <enter> (choose default sector)
            +550M (550MB partition for efi-boot) (filesystem type is 'Linux filesystem'. this needs to be changed) (remove vfat signature to wipe the partition of any data)
            n (new partition)
            2 (partition number)
            <enter> (by default sector is choosen after the previous partition ends)
            +12G (12G partition for swap partition(for 8GB ram).... this is not done for small laptop) (filesystem type is 'Linux filesystem'. this needs to be changed)
            n (new partition)
            3 (partition number)
            <enter> (by default sector is choosen after the previous partition ends)
            <enter> (takes all the remaining space in harddisk) (filesystem type is 'Linux filesystem'. this is correct for this partition)
        3. Change partition type
            m (for help)
            t (changing partition type)
            1 (choose the 1st partition)
            L (lists all partition types) (q to quit)
            1 (choose option for EFI system)
            t (changing partition type)  (steps not requried for small laptop)
            2 (choose the 2nd partition)
            L (lists all partition types) (q to quit)
            19 (choose option for linux swap)
            (No need to change the partition type for the remaining partition as it needs to be 'Linus Filesystem')
        4. Write the table to the disk
            w (writes the tables and exits out of fdisk)
        5. make filesystems
            fdisk -l (get the list of devices in the main harddisk) (mmcblk1p1, mmcblk1p2 in small laptop)
            mkfs.fat -F32 <path to partition> ( /dev/mmcblk1p1 ) (makes the efiboot partition FAT32 type)
            mkswap <path to partition> (not requried for small laptop) (makes swap partition)
            swapon <path to partition> (not requried for small laptop) (turns swap on)
            mkfs.ext4 <path to partition> ( /dev/mmcblk1p2 ) (makes linux filesystem partition .ext4 partition)
    6. Mount the linux file system partition to live image
        mount <path to linuxFilesystem partition ( /dev/mmcblk1p2 )> /mnt
    7. Install the system
        pacstrap /mnt base linux linux-firmware
    8. generate fstab (file system table)
        genfstab -U /mnt >> /mnt/etc/fstab
    9. change root into the new system
        arch-chroot /mnt
    10. Change timezone
        1. Find your timezone
            ls /usr/share/zoneinfo/  (lists all the regions. note the Region for next command)
            ls /usr/share/zoneinfo/<Region>/ (lists all the cities. note the city for next command)
        2. Change timezone
            ln -sf /usr/share/zoneinfo/<Region>/<City> /etc/localtime   (Asia/kolkata)
    11. Set hardware clock
        hwclock --systohc
    12. set the locale
        vim /etc/locale.gen (open the file) (may have to install vim if vi is not present. pacman -S vim)
        (uncomment your locale) (en_US.UTF-8 UTF-8 and en_IN UTF-8)
        :wq (save and exit)
        locale-gen
        vim /etc/locale.conf
        LANG=en_US.UTF-8 (or en_IN.UTF-8...not sure if this will work)
        :wq (save and quit)
    13. set the hostname
        vim /etc/hostname  (create the config file)
        (type the hostname of the computer)
        adimc02 (small laptop) or adimc01 (big laptop)
        :wq  (save and exit)
    14. Create hosts file
        vi /etc/hosts (open existing file)
        (type the following) (here <myhostname> == adimc01 or adimc02 (whatever is set in the hostname file)

        127.0.0.1 <Tab> localhost
        ::1 <Tab> localhost
        127.0.1.1 <Tab> <myhostname>.localdomain <Tab> <myhostname>
        
        :wq (save and quit)
    15. Set password for root user
        passwd
        (set new password)
        (retype new password)
    16. Add normal user and add him to groups so he has sudo privilages (create 2 users normal+backup with same permissions)
        useradd -m <username>  (adi02 or adi01)
        passwd <username>
        (set password for new user) (make it same as root user)
        usermod -aG wheel,audio,video,optical,storage <username> (can add more groups. find out more) (do for both users)
    17. install some packagessudo
        pacman -S sudo grub efibootmgr dosfstools os-prober mtools 
    18. Give wheel users all access when using sudo
        visudo  (if vi not present -- EDITOR=<your editor (vim)> visudo)
        (find the line about the wheel group (wheel ALL=(ALL) ALL))
        uncomment the above line to give users in the wheel group all privilages or root when they sudo
    19. create folders to point boot partition
        mkdir /boot/EFI
        mount <path to boot partition> /boot/EFI  (/dev/mmcblk1p1 for small laptop)
        grub-install --target=x86_64-efi --bootloader-id=grub_uefi --recheck
        grub-mkconfig -o /boot/grub/grub.cfg
    20. install and enable network NetworkManager, ntp, bluetooth
        pacman -Sy networkmanager ntp bluez bluez-utils
        systemctl enable NetworkManager
	systemctl enable ntpd
	systemctl enable bluetooth
	
	sudo systemctl daemon-reload (reload all daemons)
    21. exit out of chroot and reboot
        exit
        umount -l /mnt
        reboot now
        
    22. after reboot you should see a login screen
        <userrname> (adi02)
        <password> (pass)
    
    23. After restart check if internet is connected
        ping google.com
        if not connected
        nmcli device wifi list
        nmcli device wifi connect <SSID> password <password>
    24. install more packages (connect to internet first)
        sudo pacman -S code vlc git chromium speedcrunch pcmanfm ranger qtile p7zip unrar tar rsync alacritty feh picom base-devel
    25. install video drivers
        1. find what card you have
            lspci | grep -e VGA -e 3D
        2. install drivers
            sudo pacman -S xf86-video-vesa  (back up driver if specific driver not found or failed to load)
            sudo pacman -S xf86-video-intel (for intel cards)
            Check this page for complete list - https://wiki.archlinux.org/index.php/xorg
    26. install xorg
        sudo pacman -S xorg xorg-xinit
    27. edit .xinitrc file
        cp /etc/X11/xinit/xinitrc ~/.xinitrc  (copy to home as hidden file)
        open the file
        navigate to the bottom and comment out last 4-5 lines that start with 'twm &'
        add the following:
            exec qtile (launches window manager)
        :wq (write and quit)
    28. exit and restart
        sudo reboot
    29. login after reboot
        <username>
        <pass>
        startx (to launch wm)
    30. Set up brightness control (may or may not be required based on laptop keyboard functions)
        xrandr | grep " connected" | cut -f1 -d " " (find monitor name)
        xrandr --output <MonitorName> --brightness <BrightnessLvl> (from 0(min) to 1(max))
        (add the command to ~/.bashrc to make permanent alias)
        vim ~/.bashrc
        (at the bottom add aliases for yourself)
        ailas brit='xrandr --output <MonitorName> --brightness'
        :wq
        source ~/.bashrc
        (now you can change brightness by -- brit 0.7)        
    31. Set up volume control (may or may not be required based on laptop keyboard functions)
    32. set up bluetooth control (may or may not be required) (did not succeed)
        systemctl status bluetooth  (check if deamon is already running, if not.. got to next step
        systemctl start bluetooth (only requried if have not restarted post install of bluez bluez-utils laptop)
        (connecting to a bouetooth device)
        bluetoothctl power on
        bluetoothctl scan on (to start scanning)
        bluetoothctl devices (lists available devices)
        bluetoothctl pair <macAdd>
        bluetoothctl connect <macAdd>
        bluetoothctl trust <masAdd>
        
        write following script in a .sh file and run it to connect to a specific device everytime
        #!/bin/bash
        echo -e 'power on\nconnect 00:1B:66:03:11:09 \nquit' | bluetoothctl
        
    33. set up wifi control (may or may not be requried)
        1. nmcli device wifi list
        2. nmcli device wifi connect <SSID/wifiname> password <password>
    34. config files for following programs
        1. qtile
        2. alacritty
    35. Set up the following:
        1. VScode extensions
        2. Anaconda yaml file
        3. MegaUpload
    100. once all set up is done make wm autostart
        vim ~/.bash_profile
        at the bottom add the following
        [[ $(fgconsole 2>/dev/null) == 1 ]] && exec startx -- vt1    
        
    
to reload all daemons after install

