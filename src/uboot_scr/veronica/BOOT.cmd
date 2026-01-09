setenv kernel_image Image
setenv kernel_load_address 0x80400000
setenv kernel_gz_image Image.gz
setenv kernel_gz_load_address 0x82000000
setenv devicetree_image devicetree.dtb
setenv devicetree_load_address 0x87400000
setenv rootfs_image rootfs.cpio.uboot
setenv rootfs_image_load_address 0x87401000
setenv fdt_high 0xffffffff
setenv initrd_high 0x88000000

setenv bootargs 'console=ttyUL0,115200 earlycon'

setenv mmc_boot 'echo Loading Linux... && fatload mmc 0 ${kernel_gz_load_address} ${kernel_gz_image} && unzip ${kernel_gz_load_address} ${kernel_load_address} && echo Loading Devicetree... && fatload mmc 0 ${devicetree_load_address} ${devicetree_image} && echo Loading File System... && fatload mmc 0 ${rootfs_image_load_address} ${rootfs_image} && booti ${kernel_load_address} ${rootfs_image_load_address}:${filesize} ${devicetree_load_address}'
