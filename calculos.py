from fractions import Fraction
def calcularPosFinal_MRU (x0, v, t):
    x = x0+v*t
    return str(x)

def calcularPosFinal_MRUA (x0, v0, t, a):

    x= x0 + v0 * t + Fraction(1/2)* a * (t**2)
    return str(x)

def calcularVelocidadFinal_MRUA (v0, a, t):
    vf = v0 + a * t
    return str(vf)

def calcularVelocidadFinal_CaidaLibre (v0, g, t):
    vf = v0 + g * t
    return str(vf)

def calcularFuerzaNeta_Dinamica (m, a):
    F = m * a
    return str(F)

def calcularPeso_Dinamica (m, g):
    W = m * g
    return str(W)

def calcularFuerzaFriccion_Dinamica (μ, N):
    f = μ * N
    return str(f)

def calcularVelocidadAngularFinal_MCUA (ω0, α, t):
    ωf = ω0 + α * t
    return str(ωf)

def calcularDesplazamientoAngular_MCUA (ω0, t, α, ):
    θ = ω0 * t + 0.5 * α * t**2
    return str(θ)

