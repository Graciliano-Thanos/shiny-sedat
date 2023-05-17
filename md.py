from sec import *


class MD():
  
  def __innit__(self,):
    self.SD1 = 26.42
    self.PT1 = 79.25
    self.CMD1 = 30
    self.CM1 = 103
    self.UT1 = 42.27
    self.CO1 = 140

    self.INS1 = 44.9
    self.EE1 = 0.0132
    self.FT1 = 0.0132
    self.QI1 = 0.018
    self.PR1 = 0.033

    self.MOR1 = 0.03
    self.RM1 = 0.2
    self.RF = 0.667
    self.f = 0.9
    self.RFR1 = 0.4
    self.CRO1 = 30

    self.CRPV1 =250
    self.NPVROM1 = 100
    self.td = 8
    self.ty = 2920
    self.CCH = 0.018

    self.CCF = 30
    self.NCF = 10

    # RO
    self.RFR = 0.7
    self.CRO1 = 30
    self.NPVROM = 100
    self.CRPV = 250
    self.td = 8
    self.ty = 2920
    self.CCH = 0.018
    self.CE = 0.10
    self.CCF1 = 30
    self.NCF = 20
  
  def ie(self, abc):
    return int(abc)
  
  def tx(self,tx2):
    if tx2 == "2%": return 0.02
    elif tx2 == "5%": return 0.05
    elif tx2 == "7%": return 0.07
    elif tx2 == "10%": return 0.10

  def SD(self, Cap2, Remote):
    if Remote == "Sim":
      return 3*1.245 * float(Cap2) * self.RF * self.SD1
    else:
      return 1.245 * float(Cap2) * self.RF * self.SD1

  def HX1(self,Cap2, PTE):
    if PTE == "Calor Residual":
      if Cap2 == "10":return 0.02
      elif Cap2 == "100":return 0.01
      elif Cap2 == "1000":return 0.10
    
    elif PTE =="Motor Diesel":
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
    
    elif PTE == "caso1":
      if Cap2 == "10": return 0.02
      elif Cap2 == "100": return 0.01
      elif Cap2 == "1000": return 0.02
    elif PTE == "caso2":
      if Cap2 == "10": return 0.01
      elif Cap2 == "100": return 0.02
      elif Cap2 == "1000": return 0.03
    elif PTE == "caso3":
      if Cap2 == "10": return 0.02
      elif Cap2 == "100": return 0.01
      elif Cap2 == "1000": return 0.06
  
  def Pt(self, Cap2):
    return 1.245 *float(Cap2) * self.RF * self.PT1


  def Cm(self,Cap2):

    if Cap2 <100:
      return 6*26*self.CMD1
    elif Cap2 in range(100,1000):
      return 26*24*self.CMD1
    elif Cap2 >= 1000:
      return 28*36*self.CMD1

  def Mm(self,Cap2):
    return 1.245 * float(Cap2) * self.RF * self.CM1

  def Ut(self,Cap2):
    return 1.245 * float(Cap2) * self.RF * self.UT1

  def Cpes(self, Cap2):
    return 1.245 * float(Cap2) * self.RF * self.CO1
  
  def Si(self, Cap2):
    return 1.245 * float(Cap2) * self.RF * self.INS1
  
  def Ere(self, Cap2):
    return 1.245 *float(Cap2) * self.RF * self.EE1
  
  def Tdcc(self, Cap2, PTE, Remote):
    return self.Ere(Cap2) + self.Si(Cap2) + self.Cpes(Cap2) + self.Ut(Cap2) + self.Mm(Cap2)+ self.Cm(Cap2) + self.Pt(Cap2) + self.SD(Cap2, Remote)

  def Icc(self, Cap2, PTE, Remote):
    return 0.1 * self.Tdcc(Cap2, PTE, Remote)

  def Tcc(self, Cap2, PTE, Remote):
    return self.Tdcc(Cap2, PTE, Remote) + self.Icc(Cap2, PTE, Remote)
  
  def at(self, tx2,abc):
    if abc == "5":
      return self.tx(tx2)*(1+self.tx(tx2))^5/((1+self.tx(tx2))^5-1)
    elif abc == "10":
      return self.tx(tx2)*(1+self.tx(tx2))^10/((1+self.tx(tx2))^10-1)
    elif abc == "20":
      return self.tx(tx2)*(1+self.tx(tx2))^20/((1+self.tx(tx2))^20-1)
    elif abc == "30":
      return self.tx(tx2)*(1+self.tx(tx2))^30/((1+self.tx(tx2))^30-1)
  
  def Nacc(self, Cap2, PTE, tx2, abc, Remote):
    return self.HX1(Cap2, PTE) + self.Tcc(Cap2, PTE, Remote) *self.at(tx2, abc)/ (float(Cap2) * self.f *365)
  
  def Mp(self, Cap2):
    saidamp =float(Cap2) * 0.9 * 8760
    if Cap2 == "10": return saidamp*0.0005
    elif Cap2 == "100": return saidamp*0.0002
    elif Cap2 == "1000": return saidamp*0.000055

### VER DNV
  def Cte(self,Cc, PTE, Cap2, TEI_r, TCI_r):
    saidacte = self.Mp(Cap2) * (STEC_AS7_allM(Cc,TEI_r,TCI_r) / 1000)
    
    if "TVC" in PTE: return saidacte * 0.00001
    elif "MVC" in PTE: return saidacte* 0.035
    elif PTE == "Rede Elétrica": return saidacte*0.063
    elif PTE == "Coletor Solar": return saidacte*0.008
    elif PTE == "caso1": return saidacte*0.0064
    elif PTE == "caso2": return saidacte*0.0048
    elif PTE == "caso3": return saidacte*0.0032
    return saidacte
  
  def Ce(self, SECe, Rede):
    saidace1 = SECe * 24 * 0.9 * 365
    if Rede == "Solar": return saidace1*0.08
    elif Rede == "Motor Gerador": return saidace1*0.15
    return saidace1
  
  def Ce1(self,SECe, Rede):
    return self.Ce(SECe,Rede)
  
  def Fi(self, Cap2):
    return float(Cap2) * self.RF * self.f * 365 * self.FT1

  def Ch(self,Cap2):
    return float(Cap2) * self.RF * self.f * 365 * self.QI1

  def Sp(self,Cap2):
    saidasp = float(Cap2) * self.RF * self.f * 365 * self.PR1
    
    if Cap2 == "1000":
      saidasp = saidasp*0.3
    return saidasp


  def La(self,Cap2):
    saidala = float(Cap2) * self.RF * self.f * 365 * self.MOR1
    if Cap2 == "1000":
      saidala = saidala*0.3
    return saidala

  def Mr(self, Cap2):
    return self.RM1 * self.Cm(Cap2)

  def Taom(self,Cap2, SECe, Rede):
    return (self.Mp(Cap2) + self.Ce(SECe, Rede) + self.Fi(Cap2) + self.Ch(Cap2) + self.Sp(Cap2) + self.La(Cap2) + self.Mr(Cap2))

  def Anomc(self,Cap2, Cc, SECe, PTE, Rede, TEI_r,TCI_r):
    return self.Cte(Cc, PTE, Cap2, TEI_r,TCI_r) + (self.Taom(Cap2, SECe, Rede))/(float(Cap2) * self.f * 365)

  def TWC(self,Cap2, Remote, Cc, PTE, Rede="", tx2=1, abc="5", TEI_r=1,TCI_r=1,SECe=1):
    if Cap2 < 50: Cap2 = 10
    elif Cap2 <500: Cap2 = 100
    else: Cap2 = 1000

    
    saidatwc = (self.Anomc(Cap2, Cc, SECe, PTE, Rede, TEI_r,TCI_r) + self.Nacc(Cap2, PTE, tx2, abc, Remote))
    return saidatwc
  

md = MD()