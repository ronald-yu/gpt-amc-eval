# reformat a copied and pasted AMC Exam text from the AoPS website into proper json format 

# amc12a 2023
solutions='EAAEBDEDCDCDBEABEDCCABBCC'
# amc12b 2023
solutions='CBDCCCEDBEDEDAEDEAEEEEECB'
# amc12a 2022
solutions='DEBBCDDAAEEBACDDAADBEADEE'
# amc12b 2022
solutions='ADABBBDDBDEDDECCDCAEECACB'

# amc12a 2023 inclusions
inclusion = [0,0,0,0,0,1,0,0,0,1,1,1,0,1,1,1,1,0,1,1,0,1,1,1,1]
# amc12b 2023 inclusions
inclusion = [0,0,0,0,0,0,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,0]
# amc12a 2022 inclusions
inclusion = [0,0,1,0,1,0,0,1,0,0,1,1,1,1,0,1,1,0,0,0,1,1,1,0,1]
# amc12b 2022 inclusions
inclusion = [0,0,0,0,1,0,0,1,1,1,1,1,0,1,0,1,1,0,1,0,0,0,0,1,1]

with open('temp.json', 'r') as f, open('out.json','w') as f2:
    problems = []
    s = ''
    for line in f.readlines():
        if line.startswith('Problem'):
            continue
        if line.startswith('Solution'):
            s = s.replace('"', "'")
            for c in "ABCDE":
                s = s.replace(f"\\textbf{{({c})}}", f"{c})")
                s = s.replace(f"\\textbf{{({c}) }}", f"{c})")
                s = s.replace(f"{c})", f"{c}) ")
                s = s.replace(f"{c})  ", f"{c}) ")
                s = s.replace(f"{c})", f" {c})")
                s = s.replace(f"  {c})", f" {c})")
                s = s.replace("\\qquad","")
                s = s.replace("\\ ","")
                s = s.replace(f"{c})\\ ", f"{c}) ")
            problems.append(s.strip())
            s=''
            continue
        s += line.strip() + ' '
    for i,p in enumerate(problems):
        if not inclusion[i]:
            continue
        print('\n\n----\n\n')
        print(i, p)
        f2.write(f'{{"question":"{p}", "answer": "{solutions[i]}"}}\n')
    print(len(solutions))
