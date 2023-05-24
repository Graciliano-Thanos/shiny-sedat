from sec import *

SD1 = 26.42
PT1 = 79.25
CMD1 = 30
CM1 = 103
UT1 = 42.27
CO1 = 140

INS1 = 44.9
EE1 = 0.0132
FT1 = 0.0132
QI1 = 0.018
PR1 = 0.033

MOR1 = 0.03
RM1 = 0.2
RF = 0.667
f = 0.9
RFR1 = 0.4
CRO1 = 30

CRPV1 =250
NPVROM1 = 100
td = 8
ty = 2920
CCH = 0.018

CCF = 30
NCF = 10

    # RO
RFR = 0.7
CRO1 = 30
NPVROM = 100
CRPV = 250
td = 8
ty = 2920
CCH = 0.018
CE = 0.10
CCF1 = 30
NCF = 20


class MD():
  
  def ie(self, abc):
    return int(abc)
  
  def tx(self,tx2):
    if "2" in str(tx2): return 0.02
    elif "5" in str(tx2): return 0.05
    elif "7" in str(tx2): return 0.07
    elif "10" in str(tx2): return 0.10

  def SD(self, Cap2, Remote):
    if Remote == "Sim":
      return 3*1.245 * float(Cap2) * RF * SD1
    else:
      return 1.245 * float(Cap2) * RF * SD1

  def HX1(self,Cap, PTE):
    Cap2 = str(Cap)
    if type(PTE) == float:
      if Cap2 == "10": return 0.02
      elif Cap2 == "100": return 0.01
      elif Cap2 == "1000": return 0.06
    if "MVC" in PTE:
      if Cap2 == "10":return 0.02
      elif Cap2 == "100":return 0.01
      elif Cap2 == "1000":return 0.10
    
    elif "TVC" in PTE or "HTE" in PTE or "VPE" in PTE or "STE" in PTE:
      if Cap2 == "10": return 0.02
      elif Cap2 == "100": return 0.01
      elif Cap2 == "1000": return 0.01
    
    elif PTE == "Rede Elétrica":
      if Cap2 == "10": return 0.02
      elif Cap2 == "100": return 0.01
      elif Cap2 == "1000": return 0.01
    
    elif PTE == "Coletor Solar":
      if Cap2 == "10": return 0.02
      elif Cap2 == "100": return 0.01
      elif Cap2 == "1000": return 0.01
    
    elif "Flash" in PTE:
      if Cap2 == "10": return 0.02
      elif Cap2 == "100": return 0.01
      elif Cap2 == "1000": return 0.02
    elif PTE == "caso2":
      if Cap2 == "10": return 0.01
      elif Cap2 == "100": return 0.02
      elif Cap2 == "1000": return 0.03
    else: 
      if Cap2 == "10": return 0.02
      elif Cap2 == "100": return 0.01
      elif Cap2 == "1000": return 0.06

  def Pt(self, Cap2):
    return 1.245 *float(Cap2) * RF * PT1


  def Cm(self,Cap2):

    if Cap2 <100:
      return 6*26*CMD1
    elif Cap2 in range(100,1000):
      return 26*24*CMD1
    elif Cap2 >= 1000:
      return 28*36*CMD1

  def Mm(self,Cap2):
    return 1.245 * float(Cap2) * RF * CM1

  def Ut(self,Cap2):
    return 1.245 * float(Cap2) * RF * UT1

  def Cpes(self, Cap2):
    return 1.245 * float(Cap2) * RF * CO1
  
  def Si(self, Cap2):
    return 1.245 * float(Cap2) * RF * INS1
  
  def Ere(self, Cap2):
    return 1.245 *float(Cap2) * RF * EE1
  
  def Tdcc(self, Cap2, PTE, Remote):
    return self.Ere(Cap2) + self.Si(Cap2) + self.Cpes(Cap2) + self.Ut(Cap2) + self.Mm(Cap2)+ self.Cm(Cap2) + self.Pt(Cap2) + self.SD(Cap2, Remote)

  def Icc(self, Cap2, PTE, Remote):
    return 0.1 * self.Tdcc(Cap2, PTE, Remote)

  def Tcc(self, Cap2, PTE, Remote):
    return self.Tdcc(Cap2, PTE, Remote) + self.Icc(Cap2, PTE, Remote)
  
  def at(self, tx2,abc):
    abc = str(abc)
    if abc == "5":
      return self.tx(tx2)*(1+self.tx(tx2))**5/((1+self.tx(tx2))**5-1)
    elif abc == "10":
      return self.tx(tx2)*(1+self.tx(tx2))**10/((1+self.tx(tx2))**10-1)
    elif abc == "20":
      return self.tx(tx2)*(1+self.tx(tx2))**20/((1+self.tx(tx2))**20-1)
    elif abc == "30":
      return self.tx(tx2)*(1+self.tx(tx2))**30/((1+self.tx(tx2))**30-1)
  
  def Nacc(self, Cap2, PTE, tx2, abc, Remote):
    return self.HX1(str(Cap2), PTE) + self.Tcc(Cap2, PTE, Remote) *self.at(tx2, abc)/ (float(Cap2) * f *365)
  
  def Mp(self, Cap2):
    saidamp =float(Cap2) * 0.9 * 8760
    if int(Cap2) == 10: return saidamp*0.0005
    elif int(Cap2) == 100: return saidamp*0.0002
    elif int(Cap2) == 1000: return saidamp*0.000055

### VER DNV
  def Cte(self,Cc, PTE, Cap2, TEI_r, TCI_r):
    saidacte = self.Mp(Cap2) * (STEC_AS7_allM(Cc,TEI_r,TCI_r) / 1000)
    if type(PTE) == float: return saidacte
    if "TVC" in PTE: return saidacte * 0.00001
    elif "MVC" in PTE: return saidacte* 0.035
    elif PTE == "Rede Elétrica": return saidacte*0.063
    elif PTE == "Coletor Solar": return saidacte*0.008
    elif PTE == "caso1": return saidacte*0.0064
    elif PTE == "caso2": return saidacte*0.0048
    elif PTE == "caso3": return saidacte*0.0032
    return saidacte
  
  def Ce(self, SECe, Rede):
    saidace1 = float(SECe) * 24 * 0.9 * 365
    if Rede == "Solar": return saidace1*0.08
    elif Rede == "Motor Gerador": return saidace1*0.15
    return saidace1
  
  def Ce1(self,SECe, Rede):
    return self.Ce(SECe,Rede)
  
  def Fi(self, Cap2):
    return float(Cap2) * RF * f * 365 * FT1

  def Ch(self,Cap2):
    return float(Cap2) * RF * f * 365 * QI1

  def Sp(self,Cap2):
    saidasp = float(Cap2) * RF * f * 365 * PR1
    
    if Cap2 == "1000":
      saidasp = saidasp*0.3
    return saidasp


  def La(self,Cap2):
    saidala = float(Cap2) * RF * f * 365 * MOR1
    if Cap2 == "1000":
      saidala = saidala*0.3
    return saidala

  def Mr(self, Cap2):
    return RM1 * self.Cm(Cap2)

  def Taom(self,Cap2, SECe, Rede):
    return (self.Mp(Cap2) + self.Ce(SECe, Rede) + self.Fi(Cap2) + self.Ch(Cap2) + self.Sp(Cap2) + self.La(Cap2) + self.Mr(Cap2))

  def Anomc(self,Cap2, Cc, SECe, PTE, Rede, TEI_r,TCI_r):
    return self.Cte(Cc, PTE, Cap2, TEI_r,TCI_r) + (self.Taom(Cap2, SECe, Rede))/(float(Cap2) * f * 365)

  def TWC(self,Cap2, Remote, Cc, PTE, tx2=1, abc="5", TEI_r=1,TCI_r=1,SECe=1):
    if Cap2 < 50: Cap2 = 10
    elif Cap2 <500: Cap2 = 100
    else: Cap2 = 1000
    Rede = ""

    
    saidatwc = (self.Anomc(Cap2, Cc, SECe, PTE, Rede, TEI_r,TCI_r) + self.Nacc(Cap2, PTE, tx2, abc, Remote))
    return saidatwc
  
  def full_return(self,Cap2, Remote, Cc, PTE, tx2, abc, TEI_r,TCI_r,SECe):
    
    if Cap2 < 50: 
      Cap2 = 10
    elif Cap2 <500: 
      Cap2 = 100
    else: 
      Cap2 = 1000
    
    Rede = ""
    twc = self.TWC(Cap2, Remote, Cc, PTE, tx2, abc, TEI_r,TCI_r,SECe)
    nacc = self.Nacc(Cap2, PTE, tx2, abc, Remote)
    anomc = self.Anomc(Cap2, Cc, SECe, PTE, Rede, TEI_r,TCI_r)
    print(round(twc,2),round(nacc,2),round(anomc,2))
    return round(twc,2),round(nacc,2),round(anomc,2)

md = MD()
