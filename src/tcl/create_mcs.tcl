# glob xpr, use it to find and open the project, export xsa

set project [glob *.xpr]

open_project $project

#parameterize set my_mem_device [lindex [get_cfgmem_parts {mt25ql128-spi-x1_x2_x4}] 0], interface, bit file stuffs. compression?
#     set_property BITSTREAM.GENERAL.COMPRESS TRUE [current_design]
#     set_property BITSTREAM.CONFIG.CONFIGRATE 33 [current_design]
#     set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]
write_cfgmem  -format mcs -size 16 -interface SPIx4 -loadbit {up 0x00000000 [get_property DIRECTORY [get_projects]]/*.bit } -file [get_property DIRECTORY [get_projects]]/system_bit.mcs

exit
