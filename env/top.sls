base:
  '*':
    - apt
    - base.root-key
  'ofe20-001':
    - opennebula.public
    - opennebula.cluster-node
  'ocn20-*':
    - opennebula.public
    - opennebula.cluster-node
