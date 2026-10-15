#!/usr/bin/env python3
"""Fetch public GitHub contribution-day levels from Github's HTML calendar.
Fails loudly if GitHub changes the markup; never invents contribution counts.
"""
import argparse,json,re,sys
from datetime import date
from pathlib import Path
import requests
from bs4 import BeautifulSoup


def fetch(username):
    url=f'https://github.com/users/{username}/contributions'
    r=requests.get(url,headers={'User-Agent':'Mozilla/5.0 (compatible; Nattt-Profile-Art/1.0)','Accept':'text/html'},timeout=30)
    r.raise_for_status()
    soup=BeautifulSoup(r.text,'html.parser')
    days={}
    for tag in soup.select('[data-date][data-level]'):
        d=tag.get('data-date');l=tag.get('data-level')
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}',d or '') and re.fullmatch(r'\d+',str(l)):
            days[d]=min(4,max(0,int(l)))
    if len(days)<250:
        raise RuntimeError(f'Only {len(days)} days parsed from GitHub; markup or response changed. Keeping existing SVG.')
    return {'username':username,'retrieved_at':date.today().isoformat(), 'days':days,'source':url}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--username',default='RahmatHadinata23758051');p.add_argument('--output',default='data/contributions.json');args=p.parse_args()
    try:
        data=fetch(args.username)
    except Exception as e:
        sys.exit(f'Could not fetch contributions: {e}')
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(data,indent=2),encoding='utf-8');print('Saved',len(data['days']),'days to',out)
