import math

def factorize_with_known_primes(n, small_primes):
    factors = dict()
    
    # Use trial division on the known, ordered prime factor list
    for p in small_primes:
        mult = 0
        if p * p > n:
            break
        while n % p == 0:
            mult += 1
            n //= p
        if mult > 0:
            factors[p] = mult
            
    if n > 1:
        factors[n] = 1
        
    return factors

def generate_primes_up_to(limit):
    primes = []
    for num in range(2, limit + 1):
        is_prime = True
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes

def phi_factors(curr_factors, small_primes):
    factors = dict()
    for (p, mult) in curr_factors.items():
        new_factors = factorize_with_known_primes(p-1, small_primes)
        if mult > 1:
            new_factors[p] = mult-1
        for (fact, mult) in new_factors.items():
            if fact in factors:
                factors[fact] += mult
            else:
                factors[fact] = mult
            
    return factors

def compute_phis(factors, num_exps, primes):
    phis = [None]*num_exps
    curr_factors = factors.copy()

    for i in range(0, num_exps):
        curr_factors = phi_factors(curr_factors, primes)
        phis[i] = math.prod([fact**mult for (fact,mult) in curr_factors.items()])
        
    return phis

def power_tower_mod_n(exps, n, phis):
    """Computes exps[0]^(exps[1]^(...^(exps[k]))) (mod n)
    where phis gives phi(n), phi^2(n), ..., phi^k(n)
    """
    if len(exps) == 1:
        return exps[0] % n
    elif len(exps) == 2:
        return pow(exps[0], exps[1] % phis[0], n)
    else:
        curr_phi = phis[-1]
        phis = phis[:-1]
        return power_tower_mod_n(exps[:-2] + [pow(exps[-2], exps[-1] % curr_phi, phis[-1])], n, phis)
    
def power_tower_mod_n_naive(exps, n, phi_n):
    if len(exps) == 1:
        return exps[0] % n
    elif len(exps) == 2:
        return pow(exps[0], exps[1] % phi_n, n)
    else:
        return power_tower_mod_n_naive(exps[:-2] + [pow(exps[-2], exps[-1])], n, phi_n)