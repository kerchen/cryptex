#!/bin/bash

set -e

# command line parameters
command="$1" # "hid" or "rndis"

rndis_gadget="/sys/kernel/config/usb_gadget/pwlocker.rndis"
hid_gadget="/sys/kernel/config/usb_gadget/pwlocker.hid"


hid_up() {
    mkdir -p ${hid_gadget}
    cd ${hid_gadget}

    echo 0x0200 > bcdUSB # USB2
    echo "2"    > bDeviceClass
    echo 0x1d6b > idVendor # Linux Foundation
    echo 0x0104 > idProduct # Multifunction Composite Gadget
    echo 0x3001 > bcdDevice # Increment whenever this script changes!

    mkdir -p strings/0x409
    echo "0000000000001" > strings/0x409/serialnumber
    echo "Paul Kerchen" > strings/0x409/manufacturer
    echo "Password Locker HID Device" > strings/0x409/product

    # Config 1: HID
    mkdir -p configs/c.1
    echo "200" > configs/c.1/MaxPower
    mkdir -p configs/c.1/strings/0x409
    echo "HID" > configs/c.1/strings/0x409/configuration

    mkdir -p functions/hid.usb0
    echo 1 > functions/hid.usb0/protocol
    echo 1 > functions/hid.usb0/subclass
    echo 8 > functions/hid.usb0/report_length
    echo -ne \\x05\\x01\\x09\\x06\\xa1\\x01\\x05\\x07\\x19\\xe0\\x29\\xe7\\x15\\x00\\x25\\x01\\x75\\x01\\x95\\x08\\x81\\x02\\x95\\x01\\x75\\x08\\x81\\x03\\x95\\x05\\x75\\x01\\x05\\x08\\x19\\x01\\x29\\x05\\x91\\x02\\x95\\x01\\x75\\x03\\x91\\x03\\x95\\x06\\x75\\x08\\x15\\x00\\x25\\x65\\x05\\x07\\x19\\x00\\x29\\x65\\x81\\x00\\xc0 > functions/hid.usb0/report_desc

    ln -s functions/hid.usb0 configs/c.1

    ls /sys/class/udc > UDC
}

hid_down() {
    if [ ! -d ${hid_gadget} ]; then
        echo "HID gadget is already down."
        return
    fi
    echo "Taking down HID gadget..."

    # Have to unlink and remove directories in reverse order.
    # Checks allow to finish takedown after error.

    if [ "$(cat ${hid_gadget}/UDC)" != "" ]; then
        echo "" > ${hid_gadget}/UDC
    fi
    rm -f ${hid_gadget}/configs/c.1/hid.usb0
    [ -d ${hid_gadget}/functions/hid.usb0 ] && rmdir ${hid_gadget}/functions/hid.usb0
    [ -d ${hid_gadget}/configs/c.1/strings/0x409 ] && rmdir ${hid_gadget}/configs/c.1/strings/0x409
    [ -d ${hid_gadget}/configs/c.1 ] && rmdir ${hid_gadget}/configs/c.1
    [ -d ${hid_gadget}/strings/0x409 ] && rmdir ${hid_gadget}/strings/0x409
    rmdir ${hid_gadget}

    echo "Done."
}

rndis_up() {
    ms_vendor_code="0xcd" # Microsoft vendor code
    ms_qw_sign="MSFT100"
    ms_compat_id="RNDIS"
    ms_subcompat_id="5162001" # Windows RDNIS 6.0 Driver

    mkdir -p ${rndis_gadget}
    cd ${rndis_gadget}

    echo 0x0200 > bcdUSB # USB2
    echo "2"    > bDeviceClass
    echo 0x1d6b > idVendor # Linux Foundation
    echo 0x0104 > idProduct # Multifunction Composite Gadget
    echo 0x3002 > bcdDevice # Increment whenever this script changes!

    mkdir -p strings/0x409
    echo "0000000000001" > strings/0x409/serialnumber
    echo "Paul Kerchen"  > strings/0x409/manufacturer
    echo "Cryptex RNDIS Device" > strings/0x409/product

    # Config 1: CDC
    mkdir -p configs/c.1
    echo "200" > configs/c.1/MaxPower
    mkdir -p configs/c.1/strings/0x409
    echo "CDC" > configs/c.1/strings/0x409/configuration

    mkdir -p functions/ecm.usb0
    # Arbitrary(?) USB addresses
    ECMHOST="42:6F:6C:64:50:43" # "BoldPC"
    ECMSELF="52:61:64:55:53:42" # "RadUSB"
    echo $ECMHOST > functions/ecm.usb0/host_addr
    echo $ECMSELF > functions/ecm.usb0/dev_addr

    # Config 2: RNDIS
    mkdir -p configs/c.2
    echo "200" > configs/c.2/MaxPower
    mkdir -p configs/c.2/strings/0x409
    echo "RNDIS" > configs/c.2/strings/0x409/configuration

    # Use Microsoft USB extension to make sure we use the 6.0 RNDIS driver
    echo "1" > os_desc/use
    echo "${ms_vendor_code}" > os_desc/b_vendor_code
    echo "${ms_qw_sign}" > os_desc/qw_sign

    mkdir -p functions/rndis.usb0
    RNDISHOST="48:6F:74:74:50:43" # "HottPC"
    RNDISSELF="42:61:64:55:53:42" # "BadUSB"
    echo $RNDISHOST > functions/rndis.usb0/host_addr
    echo $RNDISSELF > functions/rndis.usb0/dev_addr
    echo "${ms_compat_id}" > functions/rndis.usb0/os_desc/interface.rndis/compatible_id
    echo "${ms_subcompat_id}" > functions/rndis.usb0/os_desc/interface.rndis/sub_compatible_id

    ln -s functions/ecm.usb0 configs/c.1
    ln -s functions/rndis.usb0 configs/c.2
    ln -s configs/c.2 os_desc

    ls /sys/class/udc > UDC
}


rndis_down() {
    if [ ! -d ${rndis_gadget} ]; then
        echo "RNDIS gadget is already down."
        return
    fi
    echo "Taking down RNDIS gadget..."

    # Have to unlink and remove directories in reverse order.
    # Checks allow to finish takedown after error.

    if [ "$(cat ${rndis_gadget}/UDC)" != "" ]; then
        echo "" > ${rndis_gadget}/UDC
    fi
    rm -f ${rndis_gadget}/os_desc/c.2
    rm -f ${rndis_gadget}/configs/c.2/rndis.usb0
    rm -f ${rndis_gadget}/configs/c.1/ecm.usb0
    [ -d ${rndis_gadget}/functions/ecm.usb0 ] && rmdir ${rndis_gadget}/functions/ecm.usb0
    [ -d ${rndis_gadget}/functions/rndis.usb0 ] && rmdir ${rndis_gadget}/functions/rndis.usb0
    [ -d ${rndis_gadget}/configs/c.2/strings/0x409 ] && rmdir ${rndis_gadget}/configs/c.2/strings/0x409
    [ -d ${rndis_gadget}/configs/c.2 ] && rmdir ${rndis_gadget}/configs/c.2
    [ -d ${rndis_gadget}/configs/c.1/strings/0x409 ] && rmdir ${rndis_gadget}/configs/c.1/strings/0x409
    [ -d ${rndis_gadget}/configs/c.1 ] && rmdir ${rndis_gadget}/configs/c.1
    [ -d ${rndis_gadget}/strings/0x409 ] && rmdir ${rndis_gadget}/strings/0x409
    rmdir ${rndis_gadget}

    echo "Done."
}


case ${command} in

hid)
    hid_down
    rndis_down
    hid_up
    ;;
rndis)
    rndis_down
    hid_down
    rndis_up
    ;;
*)
    echo "Usage: switch-mode.sh hid|rndis"
    exit 1
    ;;
esac
