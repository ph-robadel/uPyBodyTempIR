from uos import urandom

n_reads_MLX90615 = 0
def Read_MLX90615_Temperatures():
    global n_reads_MLX90615
    n_reads_MLX90615 += 1
    
    if (n_reads_MLX90615 % 34) < 17:    # 17 medidas com temperatura ambiente, 17 com temperature de pessoa
        tObject = 3760 + urandom(1)[0] % 11  # valores inteiros aleatório de 3760 à 3770
        tAmbient = 2500 + urandom(1)[0] % 11 # valores inteiros aleatório de 2500 à 2510
        return (tObject, tAmbient)
    else:
        return (2500, 2500)   # Tobject = 25.00 C, Tambient = 25.00 C