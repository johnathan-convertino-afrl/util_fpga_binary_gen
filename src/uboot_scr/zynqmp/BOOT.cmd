setenv kernel_image Image
setenv kernel_load_address 0x3000000
setenv devicetree_image devicetree.dtb
setenv devicetree_load_address 0x2A00000

setenv bootargs 'bootargs=earlycon=cdns,mmio,0xFF000000,115200n8 console=ttyPS0,115200n8 root=/dev/mmcblk0p2 rw rootwait cma=128M'
setenv mmc_boot 'echo Starting Linux... && fatload mmc 0 ${kernel_load_address} ${kernel_image} && fatload mmc 0 ${devicetree_load_address} ${devicetree_image} && booti ${kernel_load_address} - ${devicetree_load_address}'
