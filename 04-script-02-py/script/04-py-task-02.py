import os

target="C:\\GIT\\devops-netology"
print(f'Target path: {target}')
bash_command = ["cd "+target, "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
#is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '').replace('#','')
        print(os.path.join(target,prepare_result))
        #break
    elif result.find('new file') != -1:
        prepare_result = result.replace('\tnew file:   ', '').replace('#','')
        print(os.path.join(target, prepare_result))