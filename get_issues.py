#!/usr/bin/python3

import requests
import subprocess
import sys
import json

issues = []

count = 100
url = 'https://api.github.com/repos/python/mypy/issues?state=all&filter=all&per_page=%d' % count

issues = []
maxcount = 200

while url is not None:
    print(url)
    r = requests.get(url)
    if 'Link' not in r.headers:
        print(r)
        print(r.headers)
        break
    link = r.headers['Link']
    nexturl = None
    for l in link.split(', '):
        if l.endswith('; rel="next"'):
            nexturl = l.split('>')[0][1:]
            break
    issues.extend(r.json())
    url = nexturl

    if maxcount is not None and len(issues) > maxcount:
        break

if len(issues) == 0:
    print(":(")
    sys.exit(1)

with open('all_issues.json', 'w') as f:
    json.dump(issues, f)

def is_runnable_python(x):
    try:
        with open('x.py', 'w') as f:
            f.write(x)

        subprocess.check_output(['python', '-m', 'py_compile', 'x.py'],
                                stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError as e:
        return False

with_python = []

for issue in issues:
    print()
    print()
    # print(issue)
    print(issue['number'])
    print(issue['html_url'])
    if 'label' in issue:
        print(issue['label'])
    print(issue['title'])
    print(issue['body'])

    any_python = False
    for part in issue['body'].split("```"):
        if is_runnable_python(part):
            any_python = True
            break

    if any_python:
        print('contains Python')
        with_python.append(issue)

print(len(with_python))

with open('with_python.json', 'w') as f:
    json.dump(with_python, f)
