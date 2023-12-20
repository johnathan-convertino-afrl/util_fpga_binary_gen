# glob xpr, use it to find and open the project, export xsa

set project [glob *.xpr]

open_project $project

write_hw_platform -fixed -include_bit -force -file [get_property DIRECTORY [get_projects]]/system_wrapper.xsa

exit
