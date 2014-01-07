/srv/cloud:
  file.directory

cloud:
  group.present:
    - gid: 10000

oneadmin:
  user.present:
    - uid: 10000
    - gid: 10000
    - home: /srv/cloud/one
    - shell: /bin/bash
    - require:
      - group: cloud
      - file: /srv/cloud

/srv/cloud/one/.ssh:
  file.directory:
    - user: oneadmin
    - group: cloud
    - mode: 700
    - require:
      - user: oneadmin

/srv/cloud/one/.ssh/authorized_keys:
  file.managed:
    - source: salt://opennebula/files/ssh/{{ pillar['on_authorized_keys'] }}
    - user: oneadmin
    - group: cloud
    - mode: 644
    - require:
      - file: /srv/cloud/one/.ssh

/srv/cloud/one/.ssh/{{ pillar['on_private_key_name'] }}:
  file.managed:
    - source: salt://opennebula/files/ssh/{{ pillar['on_private_key'] }}
    - user: oneadmin
    - group: cloud
    - mode: 600
    - require:
      - file: /srv/cloud/one/.ssh

/srv/cloud/one/.ssh/config:
  file.managed:
    - source: salt://opennebula/files/ssh/config
    - user: oneadmin
    - group: cloud
    - mode: 644
    - require:
      - file: /srv/cloud/one/.ssh
