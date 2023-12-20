setws BOOTFS/vitis/

platform create -name {zynq} -hw {BOOTFS/system_wrapper.xsa} -proc {ps7_cortexa9_0} -os {standalone} -out {./BOOTFS/vitis}

platform write

platform read {./BOOTFS/vitis/zynq/platform.spr}

platform active {zynq}

domain create -name {fsbl_domain} -os {standalone} -proc {ps7_cortexa9_0} -runtime {cpp} -arch {32-bit} -support-app {zynq_fsbl}

platform write

domain active {zynq_fsbl}

domain active {fsbl_domain}

platform generate -quick

app create -name zynq_fsbl -template {Zynq FSBL} -platform zynq -domain fsbl_domain -sysproj zynq

app build -name zynq_fsbl

exit
