"""Punto 2. Inferencia exacta por enumeración."""
from algorithms.probability import normalize


def enumeration_ask(network, query: str, evidence: dict) -> dict:
    """Calcula P(query | evidence) sobre la conjunta factorizada.

    Entradas: network es la red; query es el nombre de la
    variable consultada; evidence es {nombre de variable: 0 o 1}.
    Salida: {0: probabilidad, 1: probabilidad}.

    Tips:
    - Recorra network.variables en orden topológico.
    - Para una variable fijada multiplique su probabilidad; para una oculta
      sume las dos alternativas 0 y 1. Normalice al terminar.
    - Use copias del evento y no modifique evidence.
    - network.probability(variable, valor, evento) consulta la CPT;
      el evento debe contener los valores de todos los padres.
    - Puede usar una función auxiliar recursiva. Al terminar el recorrido,
      el producto sin factores restantes vale 1.
    - Evidencia imposible: ValueError. Consulta observada: distribución puntual
      solo si la evidencia es posible.
    """
    network.validate_query(query, evidence)

    def enumerate_all(variables, event):
        if not variables:
            return 1.0
        variable = variables[0]
        rest = variables[1:]
        if variable in event:
            probability = network.probability(variable, event[variable], event)
            return probability * enumerate_all(rest, event)
        total = 0.0
        for value in (0, 1):
            new_event = event.copy()
            new_event[variable] = value

            probability = network.probability(variable, value, new_event)
            total += probability * enumerate_all(rest, new_event)
        return total

    weights = {}
    for value in (0, 1):
        if query in evidence and evidence[query] != value:
            weights[value] = 0.0
        else:
            new_evidence = evidence.copy()
            new_evidence[query] = value
            weights[value] = enumerate_all(network.variables, new_evidence)
    if sum(weights.values()) == 0:
        raise ValueError("Evidencia imposible")

    return normalize(weights)
  
  

"""
  CODIGO INICIAL 
  def enumeration_ask(network, query: str, evidence: dict) -> dict:

    network.validate_query(query, evidence)

    def enumerate_all(variables, event):
        if len(variables) == 0:
            return 1
        variable = variables[0]
        rest = variables[1:]
        if variable in event:
            probability = network.probability(
                variable, event[variable], event
            )
            return probability * enumerate_all(rest, event)
        total = 0
        for value in (0, 1):
            new_event = event.copy()
            new_event[variable] = value
            probability = network.probability(
                variable, value, new_event
            )
            total = probability * enumerate_all(rest, new_event)
        return total
    weights = {}

    for value in (0, 1):
        new_evidence = evidence.copy()
        new_evidence[query] = value
        weights[value] = enumerate_all(
            network.variables, new_evidence
        )
    return normalize(weights)
    
    
- Se cambiaron variables, porque antes no estaba
  sumando los resultados de las dos posibilidades,
  sino que reemplazaba el valor anterior.

- Se agregó una condición para comprobar si la
  variable que estamos consultando ya tenía un valor
  en la evidencia, porque antes se cambiaba ese valor
  sin tenerlo en cuenta.

- Se agregó la comprobación de que la suma de los
  pesos no fuera cero, ya que faltaba manejar el
  caso en el que la evidencia no es posible.
  """



