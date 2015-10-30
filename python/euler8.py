#! /usr/bin/env python3.4

"""Find the largest product formed from 13 adjacent digits in a 1000 digit number."""

import time


def euler8():
    start = time.time()
    mega_num = str("7316717653133062491922511967442657474235534919493496983520312774506326239578318016984801869478851843858615607891129494954595017379583319528532088055111254069874715852386305071569329096329522744304355766896648950445244523161731856403098711121722383113622298934233803081353362766142828064444866452387493035890729629049156044077239071381051585930796086670172427121883998797908792274921901699720888093776657273330010533678812202354218097512545405947522435258490771167055601360483958644670632441572215539753697817977846174064955149290862569321978468622482839722413756570560574902614079729686524145351004748216637048440319989000889524345065854122758866688116427171479924442928230863465674813919123162824586178664583591245665294765456828489128831426076900422421902267105562632111110937054421750694165896040807198403850962455444362981230987879927244284909188845801561660979191338754992005240636899125607176060588611646710940507754100225698315520005593572972571636269561882670428252483600823257530420752963450")
    print("\n\n>>> Initial 1000 digit number::\n\n" + mega_num)
    mega_num_components = mega_num.split('0')
    print('\n>>> Splitting into component parts::\n')
    selected_components = []
    product_list = []
    for c in enumerate(mega_num_components):
        # -- If the element is not null
        if c[1]:
            # -- Reject all elements of fewer that 13 characters
            if len(c[1]) >= 13:
                print('Component '+str(c[0])+'::  '+c[1]+' selected.')
                selected_components.append(c[1])
            else:
                print('Component ' + str(c[0]) + '::  ' + c[1] + ' REJECTED.')
    print('\n>>> Components of at least 13 characters::\n')
    print(selected_components)
    print('\n>>> Calculating products of consecutive values...')
    for c in selected_components:
        excess = len(c) - 13
        print('\n\n' + c + ' has a spare ' + str(excess) + ' digits')
        for e in range(excess + 1):
            product = 1
            components = []
            for digit in range(13):
                components += c[digit + e]
                product *= int(c[digit + e])
            print('Multiplying: ' + str(components))
            print('>>> ' + str(product))
            product_list.append(product)
    print('\n>>> Products found: ' + str(product_list))
    max_prod = max(product_list)
    print('\n>>> Greatest product found is ' + str(max_prod))
    finish = (time.time() - start)
    print("Solution found in " + str("{0:.5f}".format(finish)) + " seconds.")

if __name__ == "__main__":
    euler8()
