import random
import sys


# Funcao que retorna a menor potencia a superar o limiar t. Caso nenhuma consiga, escolhe a potencia com maior pdr
def get_p(lpp, t_p):
    res_p = [[0], [0]]
    for i in range(len(lpp[0])):
        if lpp[0][i] >= t_p:
            res_p[0][0] = lpp[0][i]
            res_p[1][0] = lpp[1][i]
            return res_p
    m_pdr = max(lpp[0])
    res_p[0][0] = m_pdr
    res_p[1][0] = lpp[1][lpp[0].index(m_pdr)]
    return res_p


if __name__ == "__main__":

    number_of_retries = int(sys.argv[1])
    t = float(sys.argv[2])

    l_pp = [[0.0, 0.0, 0.0, 0.0], [5, 8, 11, 14]]
    result = [[0.0], [0]]

    packet_counter = 0
    retry = 0

    pdr_atual = 0.0

    rx_counter = 0
    retry_counter = 0
    prev_packet = -1

    cont_window = 0

    cont_trial = 0
    acc_trial = 0

    verbose = True

    try:
        random.seed()
        current_config = 0

        while True:
            # the the PDR to transmit the next packet
            if retry == 0:
                if cont_window == 0:
                    ent = input().split(' ')
                    cont_window = int(ent[0])

                    l_pp[0][0] = float(ent[1])
                    l_pp[0][1] = float(ent[2])
                    l_pp[0][2] = float(ent[3])
                    l_pp[0][3] = float(ent[4])

                    result = get_p(l_pp, t)
                    pdr_atual = result[0][0]
                    pot_atual = result[1][0]

                    if verbose:
                        print("\nPDR ATUAL: ", str(pdr_atual))
                        print("POT SELEC: ", str(pot_atual) + "dBm" + "\n")

                cont_window -= 1

            trial = random.random()
            pdr_phy = pdr_atual

            if verbose:
                print("Transmitting packet {} retry {}".format(packet_counter, retry))
            retry_counter += 1

            # pacote entregue
            if trial <= pdr_phy:
                if verbose:
                    print("Receiving packet {} retry {}".format(packet_counter, retry))
                if packet_counter != prev_packet:
                    rx_counter += 1
                prev_packet = packet_counter

                # envio de ACK
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
