s# Crear diccionario
contactos = {}

# Agregar datos
contactos["Juan"] = "0991111111"
contactos["Maria"] = "0982222222"

# Mostrar contactos
print("Contactos guardados:")
for nombre, numero in contactos.items():
    print(nombre, ":", numero)

# Buscar contacto (sin input)
buscar = "Juan"
print("\nBuscando:", buscar)

if buscar in contactos:
    print("Número:", contactos[buscar])
else:
    print("No encontrado")

# Eliminar contacto (sin input)
eliminar = "Maria"
print("\nEliminando:", eliminar)

if eliminar in contactos:
    del contactos[eliminar]
    print("Contacto eliminado")
else:
    print("No existe")

# Mostrar lista final
print("\nLista final:")
for nombre, numero in contactos.items():
    print(nombre, ":", numero)