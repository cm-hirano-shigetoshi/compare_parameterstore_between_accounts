#!/usr/bin/env python
import sys
import json
import argparse
import subprocess
from subprocess import PIPE

p = argparse.ArgumentParser()
p.add_argument('profile_1', help='1つ目のアカウントプロファイル')
p.add_argument('profile_2', help='2つ目のアカウントプロファイル')
p.add_argument('-p', '--prefix', default='', help='比較対象パスのプレフィックス')
p.add_argument('-d',
               '--compare_depth',
               type=int,
               default=0,
               help='COMPARE_DEPTH番目より深いパスで同一比較')
args = p.parse_args()
depth = args.compare_depth


def get_names(profile, prefix):
    cmd = 'aws --profile {} ssm get-parameters-by-path --path {} --recursive'.format(
        profile, prefix)
    proc = subprocess.run(cmd, shell=True, stdout=PIPE, text=True)
    response = json.loads(proc.stdout)
    return [x['Name'] for x in response['Parameters']]


names_1 = get_names(args.profile_1, args.prefix)
names_2 = get_names(args.profile_2, args.prefix)

if depth == 0:
    compare_1 = set(names_1)
    compare_2 = set(names_2)
else:
    compare_1 = set('/'.join(n.split('/')[depth:]) for n in names_1)
    compare_2 = set('/'.join(n.split('/')[depth:]) for n in names_2)

if compare_1 == compare_2:
    pass
else:
    only_1 = compare_1 - compare_2
    if len(only_1) > 0:
        print('{}だけに存在'.format(args.profile_1))
        print(only_1)
    only_2 = compare_2 - compare_1
    if len(only_2) > 0:
        print('{}だけに存在'.format(args.profile_2))
        print(only_2)
    sys.exit(1)
