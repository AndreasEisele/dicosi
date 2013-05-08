


from dicosi import serve_forever



def reverse(x): return x[::-1]
def double(x): return x+x


serve_forever([reverse, double])
