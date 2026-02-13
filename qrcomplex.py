cod = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"
texto = input("insira um link ou texto: ").upper()
nome_arquivo = input("insira o nome do arquivo: ")
modo = "0010"
varnum = []
alfa_valido = ""

for char in texto:
    if char in cod:
        alfa_valido += char
        varnum.append(cod.index(char))

# 1. Codificação Alfanumérica
ncod = [varnum[i:i+2] for i in range(0, len(varnum), 2)]
icod = ""
for grupo in ncod:
    if len(grupo) == 2:
        icod += f"{(grupo[0] * 45) + grupo[1]:011b}"
    else:
        icod += f"{grupo[0]:06b}"

tamanho = len(alfa_valido)
mensagem_final = modo + f"{tamanho:09b}" + icod + "0000"

# Padding para chegar em 72 bits (V1-H)
while len(mensagem_final) % 8 != 0:
    mensagem_final += "0"
pad_bytes = ["11101100", "00010001"]
i = 0
while len(mensagem_final) < 72:
    mensagem_final += pad_bytes[i % 2]
    i += 1
mensagem_final = mensagem_final[:72]

# 2. Matemática de Galois
exp = [0] * 512
log = [0] * 256
x = 1
for i in range(256):
    exp[i] = x
    log[x] = i
    x *= 2
    if x > 255: x ^= 285
for i in range(256, 512):
    exp[i] = exp[i - 255]

def gf_mult(a, b):
    if a == 0 or b == 0: return 0
    return exp[log[a] + log[b]]

def gf_poly_mul(p1, p2):
    res = [0] * (len(p1) + len(p2) - 1)
    for i in range(len(p1)):
        for j in range(len(p2)):
            res[i + j] ^= gf_mult(p1[i], p2[j])
    return res

# 3. Correção de Erros
lista_bytes = [int(mensagem_final[i:i+8], 2) for i in range(0, 72, 8)]
g = [1]
for i in range(17): g = gf_poly_mul(g, [1, exp[i]])

bytetotal = lista_bytes + [0]*17
for i in range(len(lista_bytes)):
    coef = bytetotal[i]
    if coef != 0:
        for j in range(len(g)):
            bytetotal[i + j] ^= gf_mult(g[j], coef)

codigov1 = lista_bytes + bytetotal[len(lista_bytes):]
bits_para_inserir = "".join(f"{b:08b}" for b in codigov1)

# 4. Construção da Matriz
matriz = [[0 for _ in range(21)] for _ in range(21)]
reservado = [[False for _ in range(21)] for _ in range(21)]

def desenhar_componente(x, y, v, reser=True):
    matriz[x][y] = v
    if reser: reservado[x][y] = True

# Finder Patterns
def desenhar_ancora(x, y):
    for i in range(7):
        for j in range(7):
            val = 1 if (i==0 or i==6 or j==0 or j==6 or (2<=i<=4 and 2<=j<=4)) else 0
            desenhar_componente(x+i, y+j, val)
    # Separadores
    for i in range(-1, 8):
        for j in range(-1, 8):
            if 0 <= x+i < 21 and 0 <= y+j < 21:
                if not reservado[x+i][y+j]: desenhar_componente(x+i, y+j, 0)

desenhar_ancora(0, 0)
desenhar_ancora(0, 14)
desenhar_ancora(14, 0)

# Linhas de Timing
for i in range(8, 13):
    desenhar_componente(6, i, 1 if i % 2 == 0 else 0)
    desenhar_componente(i, 6, 1 if i % 2 == 0 else 0)
desenhar_componente(14, 6, 1) # Ponto preto solitário na V1

# Informação de Formato
fmt = "001011010011001"
for i in range(6): desenhar_componente(i, 8, int(fmt[i]))
desenhar_componente(7, 8, int(fmt[6]))
desenhar_componente(8, 8, int(fmt[7]))
desenhar_componente(8, 7, int(fmt[8]))
for i in range(6): desenhar_componente(8, 5-i, int(fmt[9+i]))

# 5. Preenchimento Zig-Zag
bit_index = 0
subindo = True
for col in range(19, -1, -2):
    if col == 6: col -= 1 
    rows = range(20, -1, -1) if subindo else range(21)
    for row in rows:
        for c in (col + 1, col):
            if not reservado[row][c]:
                val = int(bits_para_inserir[bit_index]) if bit_index < len(bits_para_inserir) else 0
                matriz[row][c] = val
                bit_index += 1
    subindo = not subindo

# 6. Geração do Arquivo BMP
def gerar_bmp(matriz_dados, arquivo, escala=20):
    tamanho_n = 21 * escala
    padding = (4 - (tamanho_n * 3) % 4) % 4
    tam_arq = 54 + (tamanho_n * 3 + padding) * tamanho_n
    h = b'BM' + tam_arq.to_bytes(4, 'little') + b'\x00'*4 + (54).to_bytes(4, 'little')
    d = (40).to_bytes(4, 'little') + tamanho_n.to_bytes(4, 'little') + tamanho_n.to_bytes(4, 'little') + (1).to_bytes(2, 'little') + (24).to_bytes(2, 'little') + b'\x00'*24
    with open(arquivo, "wb") as f:
        f.write(h); f.write(d)
        for y in range(20, -1, -1):
            for _ in range(escala):
                for x in range(21):
                    f.write((b'\x00\x00\x00' if matriz_dados[y][x] == 1 else b'\xff\xff\xff') * escala)
                f.write(b'\x00' * padding)

gerar_bmp(matriz, nome_arquivo + ".bmp")
print(f"Sucesso! {nome_arquivo}.bmp gerado. Escaneie agora!")
