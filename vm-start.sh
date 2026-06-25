#!/bin/bash

if [ -e "./vm/john.img" ]; then
    rm ./vm/john.img
fi



if not [ -e "./vm/john.img" ]; then
    cp ./vm/john_base.img ./vm/john.img
fi

qemu-system-x86_64 -m 4096 -hda ./vm/john.img -cpu max  -device virtio-net,netdev=net0 -netdev user,id=net0 -serial pty -display none
