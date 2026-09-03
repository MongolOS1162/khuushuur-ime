y = "фцужэнгшүзкъещйыбөахролдпячёсмитьвю"
m = {}
print("Space - Another method to type (like x: h kh)")
for a in y:
   x = input(f"{a}: ").split()
   if len(x) == 1:
     m[x[0]] = a
   else:
     for i in m:
      m[i] = a
print(m)
