#
#
# Algoritmo AP4_ARR
#
# Baseado no trabalho de Ruan D Gomes - Setembro/2020
#
# Frederico A M Saraiva - PPGI/UFPB
#
# Ex. ativacao: cat ./traces/A_1_G.txt | python3 simulador_sun_AP4_ARR.py 5 0.9
#

import random
import sys
import time


# Return increased's pwr
def inc_pwr(pot_p, l_p):
    for i in range(len(l_p)):
        if pot_p == l_p[i]:
            if i <= len(l_p) - 2:
                return l_p[i + 1]
    return pot_p

# Return decreased's pwr
def dec_pwr(pot_p, l_p):
    for i in range(len(l_p)):
        if pot_p == l_p[i]:
            if i >= 1:
                return l_p[i - 1]
    return pot_p

if __name__ == "__main__":

    number_of_retries = int(sys.argv[1])
    t = float(sys.argv[2])

    l_pwr = [5, 8, 11, 14]  # |---> enabled pwr

    packet_counter = 0
    retry = 0

    rx_counter = 0
    retry_counter = 0
    prev_packet = -1

    cont_window = 0
    window_size = 10

    tx_counter = 0
    ack_counter = 0

    act_pwr = l_pwr[0]  # |---> actual pwr

    time_arr = 0 # |---> controls the time to decrease pwr

    arr = t

    verbose = False

    try:
        random.seed()
        current_config = 0

        while True:

            if retry == 0:
                if cont_window == 0:
                    ent = input().split(' ')

                    cont_window = 20

                cont_window -= 1

            # calculating ARR
            if tx_counter == window_size:
                arr = (ack_counter / tx_counter)
                print("\nARR of {}dBm = {}: ".format(act_pwr, arr) + "t=" + str(t))
                if arr < t:
                    act_pwr = inc_pwr(act_pwr, l_pwr)
                    print("-------------> increase pwr to "+str(act_pwr)+"dBm")
                    time_arr = 0
                else:
                    time_arr += 1
                tx_counter = 0
                ack_counter = 0

                print("POT SELEC: " + str(act_pwr) + "dBm" + "\n")
                time.sleep(1) # time to watch :-)

            # decrease pwr if ARR >=t for a long time
            if time_arr == 8:
                act_pwr = dec_pwr(act_pwr, l_pwr)
                print("-------------> time: decrease pwr to "+str(act_pwr)+"dBm")
                time_arr = 0

            trial = random.random()
            pdr_phy = 0.8

            if verbose:
                print("Transmitting packet {} retry {}".format(packet_counter, retry))
            retry_counter += 1
            tx_counter += 1

            # packet delivered
            if trial <= pdr_phy:
                if verbose:
                    print("Receiving packet {} retry {}".format(packet_counter, retry))
                ack_counter += 1
                if packet_counter != prev_packet:
                    rx_counter += 1
                prev_packet = packet_counter

                # send ACK
                trial = random.random()
                if trial <= pdr_phy:
                    if verbose:
                        print("Receiving ACK {} retry {}".format(packet_counter, retry))
                    packet_counter += 1
                    retry = 0
                else:
                    if verbose:
                        print("ACK not received {} retry {}".format(packet_counter, retry))
                        # transmit again?
                    if retry < number_of_retries:
                        retry += 1
                    else:
                        packet_counter += 1
                        retry = 0

            # transmission failed
            else:
                # transmit again?
                if retry < number_of_retries:
                    retry += 1
                else:
                    packet_counter += 1
                    retry = 0

    except EOFError as e:
        print("{},{}".format(rx_counter / packet_counter, retry_counter / packet_counter))
