import os; path='/home/mettaclaw/scripts/test_kb_20.nal'; f=open(path,'r'); data=f.read(); f.close(); data=data.replace('dummy
',''); target='0.85)(--> organism'; idx=data.find(target); newdata=data[:idx+5]+'
'+data[idx+5:] if idx>=0 else data; f=open(path,'w'); f.write(newdata); f.close(); lines=newdata.strip().split('
'); print(f'Written {len(lines)} lines')