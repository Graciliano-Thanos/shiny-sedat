from math import exp

a= [0,9.9992293295E+02, 2.0341179217E-02,  -6.1624591598E-03,  2.2614664708E-05,-4.6570659168E-08]
b= [0, 8.0200240891E+02, -2.0005183488E+00, 1.6771024982E-02, -3.0600536746E-05, -1.6132224742E-05]
c= [0, 5.0792E-04, -3.4168E-06, 5.6931E-08, -3.7263E-10, 1.4465E-12, -1.7058E-15, -1.3389E-06, 4.8603E-09, -6.8039E-13]
d= [0, -1.1077e-06, 5.5584e-09, -4.2539e-11, 8.3702e-09]
P0=0.101325

def s(S):
  return S/1000


def rho_w(Tf):
  return a[1] + a[2] * Tf + a[3] * Tf^2 + a[4] * Tf^3 + a[5] * Tf^4

def D_rho(Tf, S):
  return b[1] * s(S) + b[2] * s(S) * Tf + b[3] * s(S) * Tf^2 + b[4] * s(S) * Tf^3 + b[5] * (s(S))^2 * Tf^2

def rho_sw_sharq(Tf, S):
  return rho_w(Tf) + D_rho(Tf, S)

def kT(Tf, S, P):
  saidakT=c[1] + c[2]*Tf + c[3]*Tf^2 + c[4]*Tf^3 + c[5]*Tf^4 + c[6]*Tf^5 + P*(c[7] + c[8]*Tf + c[9]*Tf^3) + S*(d[1] + d[2]*Tf + d[3]*Tf^2 + d[4]*P)
  return(saidakT)

def F_P(Tf, S, P):
  saidafp=exp((P-P0) * (c[1] + c[2]*Tf + c[3]*Tf^2 + c[4]*Tf^3 + c[5]*Tf^4 + c[6]*Tf^5 + S*(d[1] + d[2]*Tf + d[3]*Tf^2 )) + 0.5* (P^2 - P0^2) * (c[7] + c[8]*Tf + c[9]*Tf^3 + d[4]*S))
  return(saidafp)

def SW_Density(Tf, S, P):
  return rho_sw_sharq(Tf, S) * F_P(Tf, S, P)

def A(S):
  saidaA=5.328 - 9.76E-02 * S + 4.04E-04*S^2
  return(saidaA)


def B(S):
  saidaB=-6.913E-03 + 7.351E-04 *S - 3.15E-06*S^2
  return(saidaB)

def C(S):
  saidaC=9.6E-06 -1.927E-06*S + 8.23E-09*S^2
  return(saidaC)

def D(S):
  saidaD=2.5E-09 +1.666E-09*S - 7.125E-12*S^2
  return(saidaD)

c1 = [0,-3.1118, 0.0157, 5.1014E-05, -1.0302E-06, 0.0107, -3.9716E-05, 3.2088E-08, 1.0119E-09]

def T68(Tf):
  saidaT68=1.00024 * (Tf + 273.15)
  return(saidaT68)

def cp_sw_P0(Tf, S):
  saidacpsw=1000 * (A(S) + B(S)*Tf + C(S)*(Tf)^2 + D(S)*(Tf)^3)
  return(saidacpsw)

def cp_sw_P(Tf, S, P):
  saidacpswp=(P-P0) * ((c1[1] + c1[2]*Tf + c1[3]*Tf^2 + c1[4]*Tf^3) + S * (c1[5] + c1[6]*Tf + c1[7]*Tf^2 + c1[8]*Tf^3))
  return(saidacpswp)

def SW_SpcHeat(Tf, P, S):
  saidacp=cp_sw_P0(Tf, S) + cp_sw_P(Tf, S, P)
  return(saidacp)


a1 = [0 , 2.5008991412E+06, -2.3691806479E+03, 2.6776439436E-01, -8.1027544602E-03, -2.0799346624E-05]
def hfg_w(Tf):
  saidahfgw=a1[1] + a1[2]*Tf + a1[3]*Tf^2 + a1[4]*Tf^3 + a1[5]*Tf^4
  return(saidahfgw)

def SW_LatentHeat(Tf, S):
  hfg=hfg_w(Tf) * (1-0.001*S)
  return(hfg)


MNaCl=58.44247
Area_small=7.2
Area_big=24
#float(TEI_r) =80 # Evaporator channel inlet temperature (ºC)
#TCI_r =25 # Condenser channel inlet temperature (ºC)
FFR_r =582.7 # Feed flow rate (l/h)
def FeedC_r(Cc):
    return int(Cc) # Feed concentration (g/L)

def TEI_c(TEI_r):
   saidaTEC=0.1 * float(TEI_r) - 7
   return(saidaTEC)

FFR_c =-1.61904761904762 + 0.00107142857142857 * FFR_r + 1.19047619047619E-06 * FFR_r^2

def TCI_c(TCI_r):
   saidatci=0.2 * float(TCI_r) -5
   return(saidatci)

def FeedC_rM(Cc):
  saidafeed=FeedC_r(Cc) / MNaCl
  return(saidafeed)

def FeedC_c (Cc):
    saidafeedcc=1.666666667 * FeedC_rM(Cc) - 2
    return(saidafeedcc)

a10=5.1736633875212
a11=1.30735853812174
a12=1.92497787391827
a13=-0.452032651637654
a14=-0.236018840235782
a15=0.508528516411701
a16=-0.533945395042034

def PFlux_AS7_allM(Cc,TEI_r, TCI_r):
  return a10 + a11 * TEI_c(TEI_r) + a12 * FFR_c + a13 * TCI_c(TCI_r) + a14 * FeedC_c(Cc) + a15 * TEI_c(TEI_r) * FFR_c + a16 * FFR_c^2

a20=59.3878010910582
a21=8.16074166971919
a22=-2.60915661582559
a23=1.32417975241345
a24=-0.19364409802822
a25=-0.869096051478881
a26=0.344756994802462
a27=0.249090304647952
a28=0.545163097718411 

def TCO_AS7_allM(Cc,TEI_r,TCI_r):
  return a20 + a21 * TEI_c(TEI_r) + a22 * FFR_c + a23 * TCI_c(TCI_r) + a24 * FeedC_c(Cc) + a25 * TEI_c(TEI_r) * FFR_c + a26 * TCI_c(TCI_r) * FFR_c + a27 * FFR_c * FeedC_c(Cc) + a28 * FFR_c^2



def RhoF(Cc,TEI_r,TCI_r):
  return SW_Density((float(TEI_r) + TCO_AS7_allM(Cc,TEI_r,TCI_r))/2, (0.93644908*FeedC_r(Cc)+0.56530373), 0.101325)

def CpF(Cc,TEI_r,TCI_r):
    return SW_SpcHeat((float(TEI_r) + TCO_AS7_allM(Cc,TEI_r,TCI_r))/2, (0.93644908*FeedC_r(Cc)+0.56530373), 0.101325)
  
def RhoP(TEI_r,TCI_r):
    return SW_Density((float(TEI_r)+float(TCI_r))/2, 0 , 0.101325)



def AHvP(TEI_r,TCI_r):
    return SW_LatentHeat((float(TEI_r)+float(TCI_r))/2,  0.101325)

# Thermal power (kWth)
def ThPower_AS7_allM(Cc,TEI_r,TCI_r):
    return (FFR_r * CpF(Cc,TEI_r,TCI_r) * (float(TEI_r) - TCO_AS7_allM(Cc,TEI_r,TCI_r))) * (RhoF(Cc,TEI_r,TCI_r) / (1000*3600*1000))


# STEC (kWhth/m3)
def STEC_AS7_allM(Cc,TEI_r,TCI_r):
    return (ThPower_AS7_allM(Cc,TEI_r,TCI_r)) / ((PFlux_AS7_allM(Cc,TEI_r,TCI_r) * Area_small)/1000)
