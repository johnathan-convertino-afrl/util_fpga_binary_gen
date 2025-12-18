# glob xpr, use it to find and open the project, export xsa

set project [glob *.xpr]
set bitfile [glob *.bit]

set isize [lindex $argv 0]
set iface [lindex $argv 1] 

open_project $project

set root_dir [get_property DIRECTORY [get_projects]]

write_cfgmem  -format mcs -size $isize -force -interface $iface -loadbit "up 0x00000000 $root_dir/$bitfile" -file $root_dir/system_bit.mcs

set_property PROGRAM.FILES $root_dir/system_bit.mcs

exit
