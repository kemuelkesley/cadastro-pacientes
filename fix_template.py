import os

file_path = os.path.join('templates', 'agendamento', 'detalhes.html')
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("ag.status=='", "ag.status == '")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed")
