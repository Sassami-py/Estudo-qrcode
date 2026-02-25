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
