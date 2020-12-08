# Install using zen installer

## Steps:
 1. Use the USB that is already created. if not then follow below steps:
	* Download zen installer
	* plug in usb
	* find usb using lsblk
	* unmount usb (if already mounted)
		sudo umount /dev/sd<x>
	* make bootable USB:
		sudo dd bs=4M if=/<pathToZenInstaller> of=/dev/sd<x> status=progress oflag=sync
 2. Plug in usb and start liveuser session
 3. Connect to internet/wifi (this is important as the installer downloads the latest packages during installation)
 4. Start the installer.
 5. Partitioning:
	* Manual (it starts gparted)
	* delete existing partitions
	* create new partitions:
		* EFI system partition:
			* name - EFI
			* format - fat32
			* size - 1 GB
		* Root Partition:
			* name - Arch
			* format - ext4
			* size - 50GB
		* Home partition:
			* name - home
			* format - ext4
			* size - rest of HDD
	* add flags - (can do after the partitions are created)
		* EFI partition - boot, esp
 6. Note the sd<x> number for the harddisk where installation needs to happen 
 7. Select the partition to install arch(root partition)
 8. Select the country (IN) (for getting fastest mirrors)
 9. Select locale/language (en_US.UTF-8)
 10. Do you want to change keyboard? (NO) (select US if still asked to pick one)
 11. Do you want to change keyboard variant? (NO) (select US if still asked to pick one)
 12. Do you want to change keyboard layout? (NO) (select US if still aske to pick one)
 13. Select country/zone (ASIA)
 14. select subzone (KOLKATA)
 15. timezone (leave UTC)
 16. Provide hostname (adimc0<1/2>)
 17. Provide your username (adi0<1/2>)
 18. Enter Root password. Reenter again
 19. Enter user password. Reenter again (keep it same as Root)
 20. Select shell (Bash)
 21. Select kernel (linux)
 22. Do you want to add spookyrepo? (yes)
 23. Do you want to enable multilib? (yes)
 24. Do you want graphical package manager? (NO)
 25. Do you want support for AUR? (yes)
 26. Printer support? (No)
 27. Display manager? (sddm)
 28. Desktop? (plasma) (plama-kde applications has lot of bloat)
 29. Firefox? (No)
 30. language pack (en_gb for british english)
 31. libre-office? (yes - fresh)
 32. language pac (en_gb)
 33. Select apps to install:
	 * epdfviewerr
	 * Terminator(must! NO termial is installed by default)
	 * ntfs-3g 
	 * network-manager-applet
 34. Bootloader? (yes) (select EFI partition)
 35. Other operating systems? (no)
 36. Begin Installation. (let it complete)
 37. Restart (remove usb after complete shutdown)
 38. Install additional packages:
		sudo pacman -S code vlc git chromium speedcrunch dolphin ranger base-devel elisa notepadqq qutebrowser konsole yakuake kdeconnect shotwell
 39. Install stacer (download and install from website)
 40. copy backup data to laptop
 41. Set up config :
 		git config --global user.name 'Ram'
	 	git config --global user.email 'abc@abc.com'
		balooctl disable
 42. Set up chromium
 43. Set up konsole
 44. Set up VSCode
 45. Install anaconda

### packages installed by me
libre-office(fresh)
epdfviewer
terminator
code
vlc
git
chromium
speedcrunch 
dolphin 
ranger
base-devel
elisa
notepadqq
qutebrowser
konsole
yakuake
kdeconnect
shotwell