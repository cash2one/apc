/etc/apt/sources.list:
  file.managed:
    - source: salt://apt/files/sources.list

/etc/apt/sources.list.d:
  file.recurse:
    - source: salt://apt/files/sources.list.d
