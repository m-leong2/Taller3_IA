"""Punto 3. Muestreo a priori y su extensión por rechazo."""
import random
from algorithms.probability import normalize


def prior_sample(network, rng: random.Random) -> dict:
    """Genera un mundo completo, muestreando padres antes que hijos.

    Entradas: network es la red y rng el generador aleatorio.
    Salida: un diccionario {nombre de variable: 0 o 1} con todos los nodos.

    Tips:
    - Use exclusivamente rng.random(); X=1 si r < P(X=1 | padres).
    - No fije evidencia aquí: esta función genera muestras a priori.
    - network.variables ya está en orden topológico. Consulte la CPT con
      network.probability(variable, 1, event), usando el evento parcial.
    """
    
    """
    Primera version
    
    sample = {}
    for variable in network.variables:
        p = network.probability(variable, 1, network.variables)
        if rng.random() > p:
            sample[variable] = 0
        else:
            sample[variable] = 1
    return sample
    
    Errores identificados:
    - Se pasaba 'network.variables' completo en lugar del evento parcial acumulado ('sample') 
      a la función de probabilidad, lo que impedía evaluar correctamente los valores de los padres.
    - La condición de comparación con rng.random() evaluaba la lógica al revés para la asignación de 1 o 0.
    - Faltaba claridad en la construcción progresiva del diccionario de muestreo topológico.
    """

    sample = {}
    for variable in network.variables:
        # Consulta la probabilidad P(variable=1 | padres) usando los valores ya muestreados en el evento parcial
        p = network.probability(variable, 1, sample)
        val = 1 if rng.random() < p else 0
        sample[variable] = val
    return sample

    # FIN DEL BLOQUE DEL ESTUDIANTE


def sampling_ask(network, query, evidence, samples, rng, reject=False):
    """Estima una marginal o una condicional, usando exactamente samples intentos.

    Entradas: query es un nombre de variable; evidence es {variable: 0 o 1};
    samples es el número de intentos; rng es el generador aleatorio;
    reject indica si se descartan muestras incompatibles con la evidencia.
    Salida: (distribución estimada, número de muestras aceptadas).
    Use (None, 0) si ninguna muestra es compatible con la evidencia.

    Tips:
    - Reutilice prior_sample. Sin rechazo solo se permite evidence vacío.
    - Con rechazo cuente únicamente mundos compatibles con toda la evidencia.
    - Normalice los conteos aceptados, no divida entre intentos totales.
    - Si no acepta muestras, distribution=None; no invente ceros ni uniformes.
    """
    """ 
    Primera version
    
    network.validate_query(query, evidence)
    if samples < 1:
        raise ValueError("Muestras invalidas")
    
    counts = {0: 0, 1: 0}
    accepted = 0

    for i in range(samples):
        sample = prior_sample(network, rng)
        if reject:
            for var, val in evidence.items():
                if sample[var] == val:
                    accepted += 1
                    counts[sample[query]] += 1
        else:
            accepted += 1
            counts[sample[query]] += 1

    if accepted == 0:
        return None, 0
        
    return counts, accepted
    
    Errores identificados:
    - En el muestreo por rechazo, la validación evaluaba condición por condición suelta en lugar 
      de verificar que *toda* la evidencia fuera compatible simultáneamente (faltaba un all()).
    - El bucle de rechazo incrementaba la variable 'accepted' y los conteos por cada llave que coincidiera 
      en lugar de por cada muestra válida completa, inflando artificialmente los conteos.
    - Al final se retornaban los 'counts' directamente sin aplicar la función 'normalize' requerida 
      para convertir los conteos en una distribución de probabilidad válida.
    """

    # Validación de las entradas; no modificar.
    network.validate_query(query, evidence)
    if samples < 1:
        raise ValueError("El número de muestras debe ser positivo")
    if evidence and not reject:
        raise ValueError("Muestreo a priori estima marginales; use rechazo con evidencia")
    
    counts = {0: 0.0, 1: 0.0}
    accepted = 0

    for _ in range(samples):
        sample = prior_sample(network, rng)
        if reject:
            # Comprueba si la muestra generada es compatible con toda la evidencia observada
            compatible = all(sample[var] == val for var, val in evidence.items())
            if compatible:
                counts[sample[query]] += 1.0
                accepted += 1
        else:
            # Sin rechazo (requiere evidencia vacía por validación previa)
            counts[sample[query]] += 1.0
            accepted += 1

    if accepted == 0:
        return None, 0

    distribution = normalize(counts)
    return distribution, accepted
    # FIN DEL BLOQUE DEL ESTUDIANTE
