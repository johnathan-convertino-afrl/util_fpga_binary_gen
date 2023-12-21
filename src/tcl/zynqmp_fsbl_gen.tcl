setws vitis/

platform create -name {zynqmp} -hw {system_wrapper.xsa} -proc {psu_cortexa53_0} -arch {64-bit}  -os {standalone} -out {./vitis}

platform write

platform read {./vitis/zynqmp/platform.spr}

platform active {zynqmp}

domain create -name {fsbl_domain} -os {standalone} -proc {psu_cortexa53_0} -runtime {cpp} -arch {64-bit} -support-app {zynqmp_fsbl}

platform write

domain active {zynqmp_fsbl}

domain active {fsbl_domain}

platform generate

exit
