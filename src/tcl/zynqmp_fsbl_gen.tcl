setws vitis/

platform create -name {zynqmp} -hw {system_wrapper.xsa} -proc {psu_cortexa53_0} -arch {64-bit}  -os {standalone} fsbl-target {psu_cortexa53_0} -out {./vitis}

platform write

platform read {./vitis/zynqmp/platform.spr}

platform active {zynqmp}

# platform pmufw -extra-compiler-flags {-MMD -MP -mlittle-endian -mxl-barrel-shift -mxl-pattern-compare -mcpu=v9.2 -mxl-soft-mul -Os -flto -ffat-lto-objects -DDEBUG_MODE -DXPFW_DEBUG_DETAILED }
# 
# platform write
# 
# platform pmufw -extra-linker-flags {}
# 
# platform write
# 
# platform fsbl -extra-compiler-flags {-MMD -MP -Wall -fmessage-length=0 -DARMA53_64 -Og -DFSBL_DEBUG -DFSBL_DEBUG_INFO -DFSBL_DEBUG_DETAILED}
# 
# platform write
# 
# platform fsbl -extra-linker-flags {}
# 
# platform write

domain create -name {fsbl_domain} -os {standalone} -proc {psu_cortexa53_0} -runtime {cpp} -arch {64-bit} -support-app {zynqmp_fsbl}

platform write

domain active {zynqmp_fsbl}

domain active {fsbl_domain}

platform generate

exit
