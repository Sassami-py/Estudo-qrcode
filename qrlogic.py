class qrcode:
  def __init__(self,link,filename):
    self.filename = filename
    self.link = link.upper()
    self.group = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"
    self.mode =  "0010"
    self.exp, self.log = self._setup_gf()
    
  def _setup_gf(self):
    exp = [0]*512
    log = [0]*256
    x = 1
    for i in range(256):
      exp[i] = x
      log[x] = i
      x *= 2
      if x >= 256:
        x ^= 285
    for i in range(256,512):
     exp[i] = exp[i - 255]
    return exp, log
    
  def _encode_text(self):
    index = []
    for char in self.link:
      if char in self.group:
        index.append(self.group.index(char))
    bit_stream = ""
    for i in range(0, len(index), 2):
      group = index[i:i+2]
      if len(group) == 2:
        value = (group[0]*45)+group[1]
        bit_stream += f"{value:11b}"
      else:
        bit_stream = f"{group[0]:06b}"
    size_bin = f"{len(self.link):09b}"
    return self.mode+size_bin+bit_stream

  def _padding_apply (self, bit_stream):
    bit_stream += "0000"
    bit_stream = bit_stream[:72]
    while len(bit_stream) %8 != 0:
      bit_stream += "0"
    pad_bytes = ["11101100", "00010001"]
    i = 0
    while len(bit_stream) < 72:
      bit_stream += pad_bytes[i%2]
      i += 1
    return bit_stream

  def _gf_mult (self,a, b):
    if a == 0 or b == 0: return 0
    return self.exp[self.log[a] + self.log[b]]

  def _gf_poly_mul(self,p1,p2):
    res = [0]*(len(p1)+len(p2)-1)
    for i in range(len(p1)):
      if p1[i] != 0:
        for j in range(len(p2)):
          res[i+j] ^= self._gf_mult(p1[i], p2[j])
    return res

  def _generate_error_correction (self, padded_bits):
    data_bytes = [int(padded_bits[i:i+8],2) for i in range(0,72,8)]
    g=[1]
    for i in range(17):
      g = self._gf_poly_mul(g,[1,self.exp[i]])
    message = data_bytes+[0]*17
    for i in range(len(data_bytes)):
      coef = message[i]
      if coef != 0:
        for j in range(len(g)):
          message[i+j] ^= self._gf_mult(g[j],coef)
    return message[len(data_bytes):]

  def get_final_bits (self):
    raw_bits = self._encode_text()
    padded = self._padding_apply(raw_bits)
    error_bytes = self._generate_error_correction(padded)
    error_bits = "".join(f"{b:08b}" for b in error_bytes)
    return padded + error_bits
