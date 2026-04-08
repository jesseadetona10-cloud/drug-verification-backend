with open('apps/drugs/views.py', 'r') as f:
    content = f.read()

content = content.replace(
    'batch = serializer.save(drug=drug)',
    'batch = serializer.save(drug=drug)'
)

content = content.replace(
    "        validated_data[\"manufacturer\"] = self.context[\"request\"].user\n        return super().create(validated_data)",
    "        validated_data[\"manufacturer\"] = self.context[\"request\"].user\n        drug = super().create(validated_data)\n        notify_regulators(drug)\n        return drug"
)

with open('apps/drugs/views.py', 'w') as f:
    f.write(content)
print('Done')
