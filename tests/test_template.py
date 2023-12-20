from string import Template

s = Template("$who 在 $do")
ts = s.substitute(who="张三", do="赏花")
print(ts)
