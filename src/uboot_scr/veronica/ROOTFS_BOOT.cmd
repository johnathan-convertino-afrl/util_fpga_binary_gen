setenv kernel_image Image
setenv kernel_load_address 0x80400000
setenv kernel_gz_image Image.gz
setenv kernel_gz_load_address 0x82000000
setenv devicetree_image devicetree.dtb
setenv devicetree_load_address 0x83000000

setenv bootargs 'console=ttyUL0,115200 root=/dev/mmcblk0p2 rw earlycon rootfstype=ext4 rootwait'
setenv mmc_boot 'echo Loading Linux... && fatload mmc 0 ${kernel_gz_load_address} ${kernel_gz_image} && unzip ${kernel_gz_load_address} ${kernel_load_address} && fatload mmc 0 ${devicetree_load_address} ${devicetree_image} && booti ${kernel_load_address} - ${devicetree_load_address}'
