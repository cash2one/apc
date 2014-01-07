{% if grains['fqdn_ip4'][-1].startswith('10.10') %}
  on_authorized_keys: "authorized_keys_idc10"
  on_private_key_name: "id_rsa"
  on_private_key: "private_key_idc10"
{% else %}
  on_authorized_keys: "authorized_keys_idc20"
  on_private_key_name: "id_dsa"
  on_private_key: "private_key_idc20"
{% endif %}
