ruby1.8:
  pkg:
    - installed

genisoimage:
  pkg:
    - installed

qemu-kvm:
  pkg:
    - installed

bridge-utils:
  pkg:
    - installed

vlan:
  pkg:
    - installed

ifenslave-2.6:
  pkg:
    - installed

libvirt-bin:
  pkg:
    - installed
  service:
    - running
    - watch:
      - file: /etc/libvirt/libvirtd.conf
      - file: /etc/libvirt/qemu.conf

/etc/libvirt/libvirtd.conf:
  file.managed:
    - source: salt://opennebula/files/libvirtd.conf
    - require:
      - pkg: libvirt-bin

/etc/libvirt/qemu.conf:
  file.managed:
    - source: salt://opennebula/files/qemu.conf
    - require:
      - pkg: libvirt-bin

/etc/sudoers:
  file.managed:
    - source: salt://opennebula/files/sudoers
    - mode: 440

/etc/modules:
  file.managed:
    - source: salt://opennebula/files/modules

/datastores:
  file.directory:
    - user: oneadmin
    - group: cloud
