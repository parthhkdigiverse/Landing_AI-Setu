with open(r'c:\Users\HP\Downloads\Landing_AI-Setu\aisetu_erp\website\models.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_about = False
for i in range(len(lines)):
    if '# class AboutPageContent(models.Model):' in lines[i]:
        in_about = True
        
    if in_about:
        if lines[i].startswith('# '):
            lines[i] = lines[i][2:]
        elif lines[i].startswith('#'):
            lines[i] = lines[i][1:]
            
    if in_about and 'return "About Page Content"' in lines[i]:
        in_about = False

with open(r'c:\Users\HP\Downloads\Landing_AI-Setu\aisetu_erp\website\models.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Models successfully uncommented.")
