import math

Vdd = 2.5  # volts
Vss = -2.5  # volts
Vthn = 0.5  # volts
uCoxp = 25 * math.pow(10, -6)
uCoxn = 50 * math.pow(10, -6)
l = 0.1

# Iref = 100 * math.pow(10, -6)  # microamps

Wl1 = 2 * math.pow(10, -6)
Ll1 = 2 * math.pow(10, -6)
#Wl2 = 2 * math.pow(10, -6)
Ll2 = 1 * math.pow(10, -6)

W1 = 2 * math.pow(10, -6)
L1 = 1 * math.pow(10, -6)
#W2 = 2 * math.pow(10, -6)
L2 = 1 * math.pow(10, -6)
#W3 = 2 * math.pow(10, -6)
L3 = 1 * math.pow(10, -6)

#Wi1 = 2 * math.pow(10, -6)
Li1 = 2 * math.pow(10, -6)
#Wi2 = 2 * math.pow(10, -6)
Li2 = 2 * math.pow(10, -6)
Wi3 = 2 * math.pow(10, -6)
Li3 = 2 * math.pow(10, -6)

# Wb1b = 2 * math.pow(10, -6)
# Lb1b = 2 * math.pow(10, -6)
# Wb2b = 2 * math.pow(10, -6)
Lb2b = 2 * math.pow(10, -6)
# Wb3b = 2 * math.pow(10, -6)
Lb3b = 2 * math.pow(10, -6)

# Rd = 10000
# Ru = 10000
Rl = 20000



def check_constraints(Iref, Wb1b, Wb2b, Wb3b, W2, W3, Wl2, Wi1, Wi2, Ru, Rd, Lb1b):
    status = True

    # checked
    Vx = ((Rd/(Ru+Rd))*(Vdd-Vss)) + Vss # node x
    if (Vx) <= -Vthn:
        # print("M1 not in saturation")
        status = False

    Vy = (Vdd-Vthn)/3 # node y
    if (Vy) <= (Vx-Vthn):
        # print("M2 not in saturation")
        status = False

    # currents
    i1_WL = Wi1/Li1 # this is the ratio of W/L for the current reference
    Ib1 = ((Wb1b/Lb1b)/i1_WL)*Iref # branch 1 current
    Ib2 = ((Wb2b/Lb2b)/i1_WL)*Iref # branch 2 current
    Ib3 = ((Wb3b/Lb3b)/i1_WL)*Iref # branch 3 current
    Iref2 = ((Wi2/Li2/i1_WL))*Iref # current reference 2
  
    Vov1 = math.sqrt((2/uCoxn)*Iref*(Li1/Wi1))
    Vov2 = math.sqrt((2/uCoxp)*Iref2*(Li3/Wi3))

    # gain constraint (first order)
    muCox = math.pow(50, -6)
    gm2 = math.sqrt(2*Ib2*muCox*W2/L2)
    gml2 = math.sqrt(2*Ib2*muCox*Wl2/Ll2)
    gm3 = math.sqrt(2*Ib3*muCox*W3/L3)
    gmb3 = math.sqrt(2*Ib3*muCox*Wb3b/Lb3b)

    cg_gain = Ru*Rd/(Ru+Rd)
    cs_gain = gm2/gml2 # scale W2 to increase gain of this term
    cd_gain = gm3/(gm3 + 1/(((Rl/2)*(1/gmb3))/((Rl/2)+(1/gmb3))))
    gain = cg_gain*cs_gain*cd_gain

    if gain < 1000:
        #print("Gain constraint not met")
        status = False

    # saturation constraints:
   
    
    if (Vdd-Vx) <= Vov2:
        # print("Ml-1 not in saturation")
        status = False
    
    Vs_1 = -math.sqrt((2/uCoxn)*Ib1*(L1/W1)) - Vthn
    Vs_2 = math.sqrt(2/uCoxn*Ib2*(L2/W2)) + Vx + Vthn
    Vs_3 = Vy - Vthn - math.sqrt(2/uCoxn*Ib3*(L3/W3))
    if (Vs_1 - Vss <= Vov1):
        # print("Mbias_1 not in saturation")
        status = False
    if (Vs_2 - Vss <= Vov1):
        # print("Mbias_2 not in saturation")
        status = False
    if (Vs_3 - Vss <= Vov1):
        # print("Mbias_3 not in saturation")
        status = False
    if (4.5 - Vov2 <+ Vov1):
        # print("Mi2 not in saturation")
        status = False

    I_total = 2*(Ib1 + Ib2 + Ib3) + Iref + Iref2 + 2*((Vdd - Vss)/(Ru + Rd))
    P_total = (Vdd - Vss)*I_total
    # print(f"total power {P_total} watts, total current {I_total} amps")
    # print(f"Vov1 {Vov1} volts, Vov2 {Vov2} volts")
    # print(f"Ib1 {Ib1} amps, Ib2 {Ib2} amps, Ib3 {Ib3} amps")
    # print(f"Iref {Iref} amps, Iref2 {Iref2} amps")

    if (P_total > 3 * math.pow(10, -3)):
        # print("Power constraint not met")
        status = False

    if (status):
        print("All constraints met")
        # print(f"total power {P_total} watts, total current {I_total} amps")
        # print(f"Vov1 {Vov1} volts, Vov2 {Vov2} volts")
        # print(f"Ib1 {Ib1} amps, Ib2 {Ib2} amps, Ib3 {Ib3} amps")
        # print(f"Iref {Iref} amps, Iref2 {Iref2} amps")

    return status


## parameter sweeps of Wb1b, Wb2b, Wb3b and Wi1, Wi2, Wi3


# for Wb1b in range(2, 30, 1):
#     for Wb2b in range(2, 30, 1):
#         for Wb3b in range(2, 30, 1):
#             for Wi1 in range(2, 30, 1):
#                 for Wi2 in range(2, 30, 1):
#                     for Lb1b in range(2, 30, 1):
#                         for Lb2b in range(2, 30, 1):
#                             for Lb3b in range(2, 30, 1):
#                                 Wb1b = Wb1b * math.pow(10, -6)
#                                 Wb2b = Wb2b * math.pow(10, -6)
#                                 Wb3b = Wb3b * math.pow(10, -6)
#                                 Wi1 = Wi1 * math.pow(10, -6)
#                                 Wi2 = Wi2 * math.pow(10, -6)
#                                 Lb1b = Lb1b * math.pow(10, -6)
#                                 Lb2b = Lb2b * math.pow(10, -6)
#                                 Lb3b = Lb3b * math.pow(10, -6)
#                                 status = check_constraints(Wb1b, Wb2b, Wb3b, Wi1, Wi2, Lb1b, Lb2b, Lb3b)
#                                 Wb1b = Wb1b * math.pow(10, 6)
#                                 Wb2b = Wb2b * math.pow(10, 6)
#                                 Wb3b = Wb3b * math.pow(10, 6)
#                                 Wi1 = Wi1 * math.pow(10, 6)
#                                 Wi2 = Wi2 * math.pow(10, 6)
#                                 Lb1b = Lb1b * math.pow(10, 6)
#                                 Lb2b = Lb2b * math.pow(10, 6)
#                                 Lb3b = Lb3b * math.pow(10, 6)
#                                 if (status):
#                                     print("Wb1b", Wb1b, "Wb2b", Wb2b, "Wb3b", Wb3b, "Wi1", Wi1, "Wi2", Wi2, "Lb1b", Lb1b, "Lb2b", Lb2b, "Lb3b", Lb3b)

for Iref in range(30, 50, 1):
    for Wb1b in range(2, 10, 1):
        for Wb2b in range(2, 10, 1):
            for Wb3b in range(2, 10, 1):

                for W2 in range(2, 10, 1):
                    for W3 in range(2, 10, 1):
                        for Wl2 in range(2, 10, 1):
                            for Wi1 in range (2, 10, 1):
                                for Wi2 in range (2, 10, 1):

                                    for Ru in range(1000, 10000, 1000):
                                        for Rd in range(1000, 10000, 1000):
                                            for Lb1b in range(2, 10, 1):
                                                # for Lb2b in range(2, 10, 1):
                                                #     for Lb3b in range(2, 10, 1):
                                                        Iref = Iref * math.pow(10, -6)
                                                        Wb1b = Wb1b * math.pow(10, -6)
                                                        Wb2b = Wb2b * math.pow(10, -6)
                                                        Wb3b = Wb3b * math.pow(10, -6)
                                                        Lb1b = Lb1b * math.pow(10, -6)

                                                        W2 = W2 * math.pow(10, -6)
                                                        W3 = W3 * math.pow(10, -6)
                                                        Wl2 = Wl2 * math.pow(10, -6)
                                                        Wi1 = Wi1 * math.pow(10, -6)
                                                        Wi2 = Wi2 * math.pow(10, -6)

                                                        # Lb2b = Lb2b * math.pow(10, -6)
                                                        # Lb3b = Lb3b * math.pow(10, -6)
                                                        status = check_constraints(Iref, Wb1b, Wb2b, Wb3b, W2, W3, Wl2, Wi1, Wi2, Ru, Rd, Lb1b)
                                                        Iref = Iref * math.pow(10, 6)
                                                        Wb1b = Wb1b * math.pow(10, 6)
                                                        Wb2b = Wb2b * math.pow(10, 6)
                                                        Wb3b = Wb3b * math.pow(10, 6)
                                                        Lb1b = Lb1b * math.pow(10, 6)

                                                        W2 = W2 * math.pow(10, 6)
                                                        W3 = W3 * math.pow(10, 6)
                                                        Wl2 = Wl2 * math.pow(10, 6)
                                                        Wi1 = Wi1 * math.pow(10, 6)
                                                        Wi2 = Wi2 * math.pow(10, 6)

                                                        # Lb2b = Lb2b * math.pow(10, 6)
                                                        # Lb3b = Lb3b * math.pow(10, 6)
                                                        if (status):
                                                            #print("Iref", Iref, "Wb1b", Wb1b, "Wb2b", Wb2b, "Wb3b", Wb3b, "Ru", Ru, "Rd", Rd, "Lb1b", Lb1b, "Lb2b")
                                                            print("Iref", Iref, "Wb1b", Wb1b, "Wb2b", Wb2b, "Wb3b", Wb3b, "W2", W2, "W3", W3, "Wl2", Wl2, "Wi1", Wi1, "Wi2", Wi2, "Ru", Ru, "Rd", Rd, "Lb1b", Lb1b)

