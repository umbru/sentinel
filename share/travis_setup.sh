#!/bin/bash
set -evx

mkdir ~/.umbru

# safety check
if [ ! -f ~/.umbru/.umbru.conf ]; then
  cp share/umbru.conf.example ~/.umbru/umbru.conf
fi
