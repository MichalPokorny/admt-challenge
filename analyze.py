#!/usr/bin/python3

import os
import requests
import subprocess
import sys
import json

# 1363


with open('all_issues.json') as f:
    issues = json.load(f)

def is_runnable_python3(x):
    try:
        with open('x.py', 'w') as f:
            f.write(x)

        subprocess.check_output(['python3', '-m', 'py_compile', 'x.py'],
                                stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError as e:
        return False

def is_mypy_ok(x):
    try:
        with open('x.py', 'w') as f:
            f.write(x)

        # TODO: does this run it?
        e = os.environ.copy()
        e['PYTHONPATH'] = '/home/prvak/admt-challenge/mypy'
        e['MYPYPATH'] = '/home/prvak/admt-challenge/mypy/typeshed/stdlib/3'
        subprocess.check_output(['mypy/scripts/mypy', 'x.py'],
                                stderr=subprocess.STDOUT,
                                env=e)
        return True
    except subprocess.CalledProcessError as e:
        print(e.output)
        return False

def get_mypy_error(x):
    try:
        with open('x.py', 'w') as f:
            f.write(x)

        # TODO: does this run it?
        e = os.environ.copy()
        e['PYTHONPATH'] = '/home/prvak/admt-challenge/mypy'
        e['MYPYPATH'] = '/home/prvak/admt-challenge/mypy/typeshed/stdlib/3'
        subprocess.check_output(['mypy/scripts/mypy', 'x.py'],
                                stderr=subprocess.STDOUT,
                                env=e)
        return None
    except subprocess.CalledProcessError as e:
        return e.output

with_python = []

# 1363: false alert

for issue in issues:
    python_chunks = []
    for i, part in enumerate(issue['body'].split("```")):
        if i == 0:
            continue
        head = 'python'
        if part.startswith(head):
            part = part[len(head):]
        if is_runnable_python3(part):
            python_chunks.append(part)
            break

    if len(python_chunks) == 0:
        continue

    print()
    # print(issue)
    print(issue['number'], issue['html_url'], ':::', issue['title'])
    if 'label' in issue:
        print(issue['label'])
    #print(issue['body'])
    with_python.append(issue)

    for python_chunk in python_chunks:
        python_ok = is_runnable_python3(python_chunk)
        mp_ok = is_mypy_ok(python_chunk)

       # if python_ok and not mp_ok:
       #     mp_error = get_mypy_error(python_chunk)
       #     if mp_error in issue['body']:
                # Issue describes

        print("\t" + python_chunk)
        print("Python: %s MyPy: %s" % (python_ok, mp_ok))

    print('-------------------------')

print(len(with_python))

with open('with_python.json', 'w') as f:
    json.dump(with_python, f)
