import math

## write a set of functions that check whether certain constraints are meant given a set of parameters.


Vdd = 2.5 #volts
Vss = -2.5 #volts
Vthn = 0.5 #volts
uCoxp = 25*10^-6
uCoxn = 50*10^-6
l = 0.1

Iref = 100 * 10^-6 # can play with this value


### not used quite yet ###
Wl1 = 2 * 10^-6 # unchanged from spice
Ll1 = 2 * 10^-6
Wl2 = 2 * 10^-6
Ll2 = 1 * 10^-6

W1 = 2 * 10^-6 # unchanged from spice
L1 = 1 * 10^-6
W2 = 2 * 10^-6
L2 = 1 * 10^-6
W3 = 2 * 10^-6
L3 = 1 * 10^-6

#### isolated device params ####
Wi1 = 2 * 10^-6 # unchanged from spice
Li1 = 2 * 10^-6
Wi2 = 2 * 10^-6
Li2 = 2 * 10^-6
Wi3 = 2 * 10^-6
Li3 = 2 * 10^-6

Wb1b = 2 * 10^-6 # unchanged from spice
Lb1b = 2 * 10^-6
Wb2b = 2 * 10^-6
Lb2b = 2 * 10^-6
Wb3b = 2 * 10^-6
Lb3b = 2 * 10^-6

def check_constraints(Ru, Rd):
    # currents
    i1_WL = Wi1/Li1 # this is the ratio of W/L for the current reference
    Ib1 = ((Wb1b/Lb1b)/i1_WL)*Iref # branch 1 current
    Ib2 = ((Wb2b/Lb2b)/i1_WL)*Iref # branch 2 current
    Ib3 = ((Wb3b/Lb3b)/i1_WL)*Iref # branch 3 current
    Iref2 = ((Wi2/Li2/i1_WL))*Iref # current reference 2
  
    Vov1 = math.sqrt((2/uCoxn)*Iref*(Li1/Wi1))
    Vov2 = math.sqrt((2/uCoxp)*Iref2*(Li3/Wi3))

    Vx = (Rd/(Ru+Rd))*(Vdd-Vss) # node x
    Vy = (Vdd-Vthn)/3 # node y

    status = True
    # saturation constraints:
    if (Vx) <= -Vthn:
        print("M1 not in saturation")
        status = False
    if (Vy) <= (Vx-Vthn):
        print("M2 not in saturation")
        status = False
    if (Vdd-Vx) <= Vov2:
        print("Ml-1 not in saturation")
        status = False
    
    Vs_1 = -math.sqrt((2/uCoxn)*Ib1*(L1/W1)) - Vthn
    Vs_2 = math.sqrt(2/uCoxn*Ib2*(L2/W2)) + Vx + Vthn
    Vs_3 = Vy - Vthn - math.sqrt(2/uCoxn*Ib3*(L3/W3))
    if (Vs_1 - Vss <= Vov1):
        print("Mbias_1 not in saturation")
        status = False
    if (Vs_2 - Vss <= Vov1):
        print("Mbias_2 not in saturation")
        status = False
    if (Vs_3 - Vss <= Vov1):
        print("Mbias_3 not in saturation")
        status = False
    if (4.5 - Vov2 <+ Vov1):
        print("Mi2 not in saturation")
        status = False
    if (status):
        print("All constraints met")

    return status

check_constraints(10000, 10000)
    
