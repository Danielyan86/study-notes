#!/usr/bin/env bash
a='I am a simple string with digits 1234'
pat='(.*) ([0-9]+)'
[[ "$a" =~ $pat ]]  # 构建正则匹配
# 匹配的字符存在一个 BASH_REMATCH 的数组里面
echo "${BASH_REMATCH[0]}"
echo "${[1]}"
echo "${BASH_REMATCH[2]}"