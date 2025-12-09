setenv kernel_image zImage
setenv kernel_load_address 0x1000000
setenv devicetree_image devicetree.dtb
setenv devicetree_load_address 0x2000000
setenv fpga_bit_file quartus_bit.rbf
setenv fpga_load_address 0x3000000

setenv bootargs 'console=ttyS0,115200 root=/dev/mmcblk0p2 rw rootwait earlyprintk'
setenv mmc_boot 'echo Configure FPGA... && fatload mmc 0 ${fpga_load_address} ${fpga_bit_file} && fpga load 0 ${fpga_load_address} ${filesize} && echo Starting Linux... && fatload mmc 0 ${kernel_load_address} ${kernel_image} && fatload mmc 0 ${devicetree_load_address} ${devicetree_image} && bootz ${kernel_load_address} - ${devicetree_load_address}'
bridge enable
run mmc_boot
