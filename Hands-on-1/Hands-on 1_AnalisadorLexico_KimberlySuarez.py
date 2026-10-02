# Hands-on 1: Análisis Léxico y Autómatas

"""
    Compiladores

    Kimberly Lizbeth Suarez Camarena

    219515435
"""

# Objeto instrucción

class Instruccion:

    def __init__(self, operacion, registros, direccion):
        self.operacion = operacion
        self.registros = registros
        self.direccion = direccion

    def mostrar(self):
        print("{")
        print(f'  operacion: "{self.operacion}",')
        print(f"  registros: {self.registros},")
        print(f"  direccion: {self.direccion}")
        print("}")


# AFD
def analizar_afd(entrada):

    i = 0
    n = len(entrada)
    tokens = []

    # Estado inicial
    estado = "q0"

    # Q0: ignorar espacios iniciales
    while i < n and entrada[i] == " ":
        i += 1

    # Transición q0 -> q1
    estado = "q1"

    # Q1: leer mnemónico
    inicio = i

    while i < n and entrada[i] not in [" ", ","]:
        i += 1

    mnemónico = entrada[inicio:i]

    # Validar mnemónico
    if mnemónico not in ["MOV", "ADD", "STO", "END"]:
        estado = "RECHAZO"
        return None, f'Instrucción inválida: mnemónico "{mnemónico}" no reconocido.'

    tokens.append((mnemónico, mnemónico))

    # MOV
    if mnemónico == "MOV":

        # q1 -> q2
        estado = "q2"

        # Espacios después de MOV
        while i < n and entrada[i] == " ":
            i += 1

        # Q2: leer registro
        inicio = i

        while i < n and entrada[i] not in [" ", ","]:
            i += 1

        registro = entrada[inicio:i]

        if registro not in ["AL", "BL"]:
            estado = "RECHAZO"
            return None, f'Instrucción inválida: registro "{registro}" no permitido.'

        tokens.append(("REGISTRO", registro))

        # q2 -> q3
        estado = "q3"

        # Espacios antes de la coma
        while i < n and entrada[i] == " ":
            i += 1

        # Q3: coma obligatoria
        if i >= n or entrada[i] != ",":
            estado = "RECHAZO"
            return None, "Instrucción inválida: falta la coma entre el registro y la dirección."

        tokens.append(("COMA", ","))

        i += 1

        # q3 -> q4
        estado = "q4"

        # Espacios después de la coma
        while i < n and entrada[i] == " ":
            i += 1

        # Q4: leer dirección
        inicio = i

        while i < n and entrada[i].isdigit():
            i += 1

        if inicio == i:
            estado = "RECHAZO"
            return None, "Instrucción inválida: falta la dirección."

        direccion_texto = entrada[inicio:i]
        direccion = int(direccion_texto)

        tokens.append(("NUMERO", direccion_texto))

        # q4 -> q5
        estado = "q5"

        # Espacios finales
        while i < n and entrada[i] == " ":
            i += 1

        # Q5: aceptación
        if i != n:
            estado = "RECHAZO"
            return None, "Instrucción inválida: contiene operandos o caracteres adicionales."

        estado = "ACEPTACION"

        objeto = Instruccion(
            "MOV",
            [registro],
            direccion
        )

        return objeto, tokens


    # ADD
    if mnemónico == "ADD":

        # q1 -> q6
        estado = "q6"

        # Espacios después de ADD
        while i < n and entrada[i] == " ":
            i += 1

        # Q6: primer registro
        inicio = i

        while i < n and entrada[i] not in [" ", ","]:
            i += 1

        registro1 = entrada[inicio:i]

        if registro1 != "AL":
            estado = "RECHAZO"
            return None, 'Instrucción inválida: ADD requiere "AL" como primer registro.'

        tokens.append(("REGISTRO", registro1))

        # q6 -> q7
        estado = "q7"

        # Espacios antes de la coma
        while i < n and entrada[i] == " ":
            i += 1

        # Q7: coma obligatoria
        if i >= n or entrada[i] != ",":
            estado = "RECHAZO"
            return None, "Instrucción inválida: falta la coma entre los registros."

        tokens.append(("COMA", ","))

        i += 1

        # q7 -> q8
        estado = "q8"

        # Espacios después de la coma
        while i < n and entrada[i] == " ":
            i += 1

        # Q8: segundo registro
        inicio = i

        while i < n and entrada[i] not in [" ", ","]:
            i += 1

        registro2 = entrada[inicio:i]

        if registro2 != "BL":
            estado = "RECHAZO"
            return None, 'Instrucción inválida: ADD requiere "BL" como segundo registro.'

        tokens.append(("REGISTRO", registro2))

        # q8 -> q9
        estado = "q9"

        # Espacios finales
        while i < n and entrada[i] == " ":
            i += 1

        # Q9: aceptación
        if i != n:
            estado = "RECHAZO"
            return None, "Instrucción inválida: contiene operandos o caracteres adicionales."

        estado = "ACEPTACION"

        objeto = Instruccion(
            "ADD",
            [registro1, registro2],
            None
        )

        return objeto, tokens


    # STO
    if mnemónico == "STO":

        # q1 -> q10
        estado = "q10"

        # Espacios después de STO
        while i < n and entrada[i] == " ":
            i += 1

        # Q10: leer dirección
        inicio = i

        while i < n and entrada[i].isdigit():
            i += 1

        if inicio == i:
            estado = "RECHAZO"
            return None, "Instrucción inválida: falta la dirección."

        direccion_texto = entrada[inicio:i]
        direccion = int(direccion_texto)

        tokens.append(("NUMERO", direccion_texto))

        # q10 -> q11
        estado = "q11"

        # Espacios finales
        while i < n and entrada[i] == " ":
            i += 1

        # Q11: aceptación
        if i != n:
            estado = "RECHAZO"
            return None, "Instrucción inválida: contiene operandos o caracteres adicionales."

        estado = "ACEPTACION"

        objeto = Instruccion(
            "STO",
            [],
            direccion
        )

        return objeto, tokens



    # END
    if mnemónico == "END":

        # q1 -> q12
        estado = "q12"

        # Espacios finales
        while i < n and entrada[i] == " ":
            i += 1

        # Q12: END no debe tener operandos
        if i != n:
            estado = "RECHAZO"
            return None, "Instrucción inválida: END no debe tener operandos."

        estado = "ACEPTACION"

        objeto = Instruccion(
            "END",
            [],
            None
        )

        return objeto, tokens


    # Seguridad: el AFD siempre debe devolver dos valores
    estado = "RECHAZO"
    return None, "Instrucción inválida."


# Máquina de Moore

class MaquinaMoore:

    def __init__(self, instruccion):
        self.instruccion = instruccion
        self.estado = "INICIO"

    def siguientePaso(self):

        operacion = self.instruccion.operacion

        # MOV
        if operacion == "MOV":

            if self.estado == "INICIO":
                self.estado = "LEER_MEMORIA"
                return f"MAR ← {self.instruccion.direccion}"

            if self.estado == "LEER_MEMORIA":
                self.estado = "CARGAR_REGISTRO"
                return "MBR ← M[MAR]"

            if self.estado == "CARGAR_REGISTRO":
                self.estado = "FIN"
                return f"{self.instruccion.registros[0]} ← MBR"

        # ADD
        elif operacion == "ADD":

            if self.estado == "INICIO":
                self.estado = "FIN"
                return "ACC ← AL + BL"

        # STO
        elif operacion == "STO":

            if self.estado == "INICIO":
                self.estado = "LEER_MEMORIA"
                return f"MAR ← {self.instruccion.direccion}"

            if self.estado == "LEER_MEMORIA":
                self.estado = "ESCRIBIR_MEMORIA"
                return "MBR ← ACC"

            if self.estado == "ESCRIBIR_MEMORIA":
                self.estado = "FIN"
                return "M[MAR] ← MBR"

        # END
        elif operacion == "END":

            if self.estado == "INICIO":
                self.estado = "FIN"
                return "HALT ← 1"

        return None


    def generar_microoperaciones(self):

        microoperaciones = []

        while self.estado != "FIN":

            microoperacion = self.siguientePaso()

            if microoperacion is not None:
                microoperaciones.append(microoperacion)

        return microoperaciones


# Programa principal

entrada = input("ENTRADA\n").strip()

print("\nVALIDACIÓN MEDIANTE AFD")

resultado, informacion = analizar_afd(entrada)


# Instrucción inválida

if resultado is None:

    print(informacion)
    print("No se construye el objeto instrucción.")
    print("No se generan microoperaciones.")


# Instrucción válida

else:

    print("Instrucción válida.")

    print("\nTOKENS RECONOCIDOS")

    for token, lexema in informacion:
        print(f'{token}("{lexema}")')

    print("\nCOMPONENTES IDENTIFICADOS")

    print(f"Mnemónico: {resultado.operacion}")

    if resultado.operacion == "MOV":

        print(f"Registro destino: {resultado.registros[0]}")
        print(f"Dirección de memoria: {resultado.direccion}")
        print("Direccionamiento: directo")

    elif resultado.operacion == "ADD":

        print(f"Registro 1: {resultado.registros[0]}")
        print(f"Registro 2: {resultado.registros[1]}")

    elif resultado.operacion == "STO":

        print(f"Dirección de memoria: {resultado.direccion}")
        print("Direccionamiento: directo")

    elif resultado.operacion == "END":

        print("Sin operandos")


    # Objeto instrucción

    print("\nOBJETO INSTRUCCIÓN")

    resultado.mostrar()


    # Máquina de Moore

    print("\nMICROOPERACIONES GENERADAS POR MOORE")

    moore = MaquinaMoore(resultado)

    microoperaciones = moore.generar_microoperaciones()

    for numero, microoperacion in enumerate(microoperaciones, 1):
        print(f"{numero}. {microoperacion}")

    print("Generación terminada.")