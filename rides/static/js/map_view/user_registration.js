function driverEnabled() {
    const e = document.getElementById("exec");

    e.className="form-inline";
}

const d = document.getElementById("driver-enable");

if(d.checked == true)
    driverEnabled();