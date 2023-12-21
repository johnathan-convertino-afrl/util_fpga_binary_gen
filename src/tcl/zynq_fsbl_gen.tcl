setws vitis/

platform create -name {zynq} -hw {system_wrapper.xsa} -proc {ps7_cortexa9_0} -os {standalone} -out {./vitis}

platform write

platform read {./vitis/zynq/platform.spr}

platform active {zynq}

domain create -name {fsbl_domain} -os {standalone} -proc {ps7_cortexa9_0} -runtime {cpp} -arch {32-bit} -support-app {zynq_fsbl}

platform write

domain active {zynq_fsbl}

domain active {fsbl_domain}

platform generate

exit
