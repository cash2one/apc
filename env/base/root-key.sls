/root/.ssh:
  file.directory:
    - user: root
    - group: root
    - mode: 700

/root/.ssh/authorized_keys:
  file.managed:
    - source: salt://base/files/authorized_keys
    - user: root
    - group: root
    - mode: 644
    - require:
      - file: /root/.ssh

/root/.ssh/config:
  file.managed:
    - source: salt://base/files/ssh_config
    - user: root
    - group: root
    - mode: 644
    - require:
      - file: /root/.ssh
