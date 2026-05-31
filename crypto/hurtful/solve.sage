from Crypto.Util.number import long_to_bytes, bytes_to_long

# adapted from: https://github.com/maximmasiutin/rsa-coppersmith-stereotyped-message/blob/master/rsa-coppersmith-stereotyped-message.sage

def message_recover(prefix, sec_len, c, n, e):
    ZmodN = Zmod(n)
    P.<x> = PolynomialRing(ZmodN)
    # * (2 ^ ((sec_len + suffix_len) * 8)) shifts it to the left by (sec_len + suffix_len) bytes
    a = ZmodN(
        (bytes_to_long(prefix) * (2 ^ ((sec_len) * 8)))
    )
    c = ZmodN(c) # the ciphertext
    f = (a + x) ^ e - c # this is the equation that has a root that we want, aka f(x) = (m + x)^e - c
    f = f.monic() # divides out the leading coefficient to make it monic
    roots = f.small_roots(epsilon=1 / 20) # how 'small' the root is = epislon
    rc = len(roots)
    if rc == 0:
        return None
    elif rc == 1:
        message = a + (roots[0])
        return long_to_bytes(int(message))
    else:
        print(
            "Don't know how to handle situation when multiple roots are returned:", rc
        )
        raise Exception("Multiple roots")
        # sys.exit(1)

N = 19182059951550152194262985844167261329837098855450236222013760659170349018734494923926666667501340706425872438287170720903583823667756573458142648513352590833858660174432217965277179911355266513452278961332550556503321884404062276956158547580042536477663767813759729649129106469265655223451223809232904112545827951067852204320979668072724299447815067365854856364324801062529616146166750509449375848647583211376445559824835125899135120190217678172503092284624762383334136004808603157447096333303878501320079019667203448434374213128608508633749312972902710408469284343758812291029591531968790328542459486100584232853831
e = 3
c = 13131547353643964269974696530621442484862362408226564561566116636024604640465295092296980626925666439675971217402946439141553202254604849457188007454699538682918891457187624359386003061118876434043817877482088092956606930950252859797028902120711953259812881632304429935981366831846294320052038062427759377027934955686954417314137019396600765995589656261890382943632109387431016394449936269098790317502797885039391511502199770624977868648873042353283870936117111244787113481287058480173941942328575776017868390649935214113443493330011242794012152900909400012708779788657388488378264146239463590037604839491578237209775


# turns out this breaks SUPER easily if it's a bigger e value...
prefix = b"Congrats on making it all the way here. If you're looking at this challenge you obviously know a lot, just find the flag: "

# if you want to speed this up, flag len is 35
secret_len = 10
while True:
    print("Trying to recover the message", secret_len, "byte(s) long...")
    message = message_recover(prefix, secret_len, c, N, e)
    if message is not None:
        break
    else:
        if secret_len > 40:
            print("Could not recover the message, sorry!")
            sys.exit(1)
    secret_len += 1

# Result
print("Decrypted message:", message)

