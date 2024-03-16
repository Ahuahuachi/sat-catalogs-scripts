INSERT INTO llx_c_mxsatcatalogs_products_services(code, label, active)
VALUES
{% for v in values -%}
    ('{{ v.code }}', '{{ v.label}}', {{ v.active }})
    {%- if loop.last %};{% else %},{% endif %}
{% endfor %}
