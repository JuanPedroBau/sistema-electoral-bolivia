import bcrypt

# Lista de contraseñas originales
passwords = [
    "admin123",
    "inv123",
    "Tuto2025!",
    "Libre2025!",
    "Analista2025$",
]

# Generar hashes manualmente usando bcrypt
hashed_passwords = [bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode() for p in passwords]

# Mostrar los resultados
for original, hashed in zip(passwords, hashed_passwords):
    print(f"{original} => {hashed}")
