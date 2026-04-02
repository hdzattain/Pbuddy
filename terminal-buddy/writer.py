def w(p, l):
    with open(p, 'w') as f:
        f.write(chr(10).join(l))
    print('Created ' + p)
