"""Punto 1. Distribuciones discretas y decisiones de respuesta."""
import math


def normalize(weights: dict) -> dict:
    """Retorna un diccionario nuevo cuyas probabilidades suman uno.

    Entrada: weights = {resultado: peso}.
    Salida: {resultado: probabilidad}, con las mismas claves.

    Tips:
    - Conserve las claves y su orden; no modifique weights.
    - Rechace pesos negativos, no finitos, diccionarios vacíos y suma cero.
    
    
    Primera Version de mi codigo:
    
    IA usada: DeepSeek
    
    if not weights:
        return {}

    total = 0
    for w in weights:
        if w < 0 or not math.isfinite(w):
            raise ValueError("Pesos invalidos")
        total += w

    for k in weights:
        weights[k] = weights[k] / total

    return {k: v for k, v in weights.items() if v != 0}
    
    
    Errores identificadoas:
    - Cuando el diccionario esta vacio, el codigo devuelve un diccionario vacio. 
    Debe lanzar ValueError con el mensaje de diccionario vacio
    - El bucle recorria weights directamente, es decir q recorre las claves. Debe 
    recorrer weights.values() para trabajar con los pesos
    - La validacion de pesos estaba mal planteada porque validaba  claves en lugar de 
    valores. Se debe comprobar cada valor con math.isfinite y con la condicion 
    de q no sea negativo
    - No se comprueba si la suma total es cero antes de dividir
    - El codigo modificaba el diccionario original weights 
    pero se tiene q crear y devolver un diccionario nuevo sin modificar weights
    - El codigo malo filtra las claves cuyo valor sea cero al devolver el resultado, 
    eso elimina claves y no conserva todas las claves originales
    
    
    use la ia con el siguiente propmt: Cuales son los errores que existen en este codigo 
    y que no dejan que mi codigo funcione como deberia, dime como puedo solucionar eso 
    
    
    
    
    
    """
    # TODO: Add your code here
    if not weights:
        raise ValueError("El diccionario de pesos está vacío")
    if any(not math.isfinite(w) or w < 0 for w in weights.values()):
        raise ValueError("Pesos negativos o no finitos encontrados")
    total = sum(weights.values())
    if math.isclose(total, 0.0, abs_tol=1e-9) or total <= 0:
        raise ValueError("La suma de los pesos es cero")
    return {k: w / total for k, w in weights.items()}

    # FIN DEL BLOQUE DEL ESTUDIANTE


def expected_utility(distribution: dict, utilities: dict) -> float:
    """Calcula sum_s P(s) U(s) para una acción.

    Entradas: distribution = {resultado: probabilidad} y
    utilities = {resultado: utilidad} para una sola acción.
    Salida: un número con la utilidad esperada.

    Tips:
    - distribution ya debe estar normalizada; no normalice utilidades.
    - Ambas tablas deben contener los mismos resultados posibles.
    """

    # Validación de las entradas; no modificar.
    if set(distribution) != set(utilities) or not distribution:
        raise ValueError("Probabilidades y utilidades deben tener las mismas claves")
    if any(not math.isfinite(p) or p < 0 for p in distribution.values()):
        raise ValueError("Distribución inválida")
    if not math.isclose(sum(distribution.values()), 1, abs_tol=1e-9):
        raise ValueError("La distribución debe sumar uno")
    if any(not math.isfinite(u) for u in utilities.values()):
        raise ValueError("Utilidades no finitas")
    
    
    return sum( distribution [s] * utilities[s] for s in distribution )
    
    """
    para el desarrollo de esta lineal de codigo no fue necesario el uso de IA :)
    el codigo funciono sin necesidad de recurrir a ella
    
    """
    


def best_action(distribution: dict, actions: dict) -> tuple[str, dict]:
    """Retorna (nombre de acción, utilidades esperadas por acción).

    Entradas: distribution = {resultado: probabilidad} y
    actions = {acción: {resultado: utilidad}}.
    Salida: (acción elegida, {acción: utilidad esperada}).

    Tips:
    - actions asocia cada acción con su tabla de utilidades.
    - Reutilice expected_utility y conserve la primera acción en los empates.
    
    
    Primera Version de mi codigo:
        
    IA usada: DeepSeek
        
    esperadas = {}
    for accion in actions:
        esperadas[accion] = expected_utility(distribution, actions)

    mejor_accion = ""
    mejor_valor = 0

    for accion in actions:
        valor = esperadas[accion]
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_accion = accion
        esperadas[accion] = valor / sum(esperadas.values())

    actions[mejor_accion] = mejor_valor

    return mejor_valor, esperadas 

    
    
    
    Errores Identificados:
    
    - El bucle que calcula las utilidades esperadas recorre actions directamente
     osea q recorre las claves y al llamar a expected_utility le pasa actions entero 
     en vez de las utilidades de esa accion. Debe recorrer actions.items() y pasar 
     utilidades q son los valores asociados a cada accion
    - El segundo bucle debe recorrer esperadas.items() no actions, asi se obtiene
    directamente cada accion con su utilidad esperada y se evita acceder a esperadas
    por clave de forma innecesaria
    -mejor_valor debe inicializarse en menos infinito ya q si se inicializa en cero 
    cualquier accion con utilidad esperada negativa nunca se selecciona y mejor_accion 
    puede quedar vacia. 
    - No se debe normalizar esperadas dentro del bucle
    - No se debe modificar el diccionario original actions ya q contamina la entrada del llamador
    - El valor de retorno debe ser la tupla mejor_accion y esperadas en ese orden
    -El codigo malo no valida ni asume correctamente que las utilidades de cada accion
    
    
    use la ia con el siguiente prompt: me puedes ayudar a identificar y corregir los errores 
    de este codigo en base al contexto del pdf
    
    
     Reflexion Final de Uso de IA
            
        
    Esto me ayudo a comprender mejor cuales eran los errores de elogica q estaba cometiendo 
    y en muchos casos hasta pensaba que asi era la forma correcta de resolver mi codigo, 
    asi con el apoyo de la ia puedo identificar y corregir los errores para lograr obtener un codigo 
    funcional pero sin dejar de lado mla importancia de entender pq se dan dichos errores 
    y poque la version corregida le permite al codigo correr sin mayores errores, ademas, 
    de este modo puedo aprender y ganar conocimiento haciendo un uso responsable de la IA.

    
    
    
    """
    # Validación de las acciones; no modificar.
    if not actions:
        raise ValueError("Se requiere al menos una acción")
    
    
    esperadas = {}
    
    for accion, utilidades in actions.items():
        esperadas[accion] = expected_utility(distribution, utilidades)

    mejor_accion = None
    mejor_valor = -math.inf

    for accion, valor in esperadas.items():
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_accion = accion

    return mejor_accion, esperadas