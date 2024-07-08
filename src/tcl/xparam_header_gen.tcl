# from Xilinx forum member, stephenm

set file_name xparameters.h
set hw_file [glob -nocomplain -directory [pwd] -type f *.xsa]

hsi::open_hw_design $hw_file

set fileId [open $file_name "w"]

foreach ip [hsi::get_cells -filter {IP_TYPE==PERIPHERAL}] {
	puts $fileId "/* Definitions for driver [string toupper $ip] */"
	set baseaddr [string toupper [hsi::get_property CONFIG.C_BASEADDR [hsi::get_cells $ip]]]
	if {$baseaddr == ""} {
		set baseaddr [string toupper [hsi::get_property CONFIG.C_S_AXI_BASEADDR [hsi::get_cells $ip]]]
	}
	set highaddr [string toupper [hsi::get_property CONFIG.C_HIGHADDR [hsi::get_cells $ip]]]
	if {$highaddr == ""} {
		set highaddr [string toupper [hsi::get_property CONFIG.C_S_AXI_HIGHADDR [hsi::get_cells $ip]]]
	}
	puts $fileId "#define XPAR_[string toupper $ip]_BASEADDR $baseaddr"
	puts $fileId "#define XPAR_[string toupper $ip]_HIGHADDR $highaddr \n"
}

close $fileId

puts "Info: header file ($file_name) created!!"

hsi::close_hw_design [hsi::current_hw_design]
