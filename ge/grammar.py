import re
from ga.params import MAX_WRAPS, REPAIR


class Grammar(object):

    NT = "NT"
    T = "T"

    def __init__(self, file_name):
        self.rules = {}
        self.non_terminals, self.terminals = set(), set()
        self.start_rule = None

        self.read_bnf_file(file_name)

    def read_bnf_file(self, file_name):
        """
        Lectura del archivo que contiene la gramática BNF utilizada para resolver el problema.

        Se almacenan las reglas de producción y el tipo de símbolo (terminal o no terminal) de cada uno de los símbolos
        que las forman para usarlas posteriormente al descifrar el genoma de un individuo.

        :param file_name: nombre del archivo que contiene la gramática
        """
        # Patrones que deben seguir las reglas especificadas en el fichero de gramática
        rule_separator = "::="

        non_terminal_pattern = r"((?<!\\)<\S+?(?<!\\)>)"
        production_separator = r"(?<!\\)\|"

        for line in open(file_name, 'r'):
            if not line.startswith("#") and line.strip() != "":
                # Se encuentra una nueva regla y se separan el símbolo de la izquierda que la define y las reglas
                # de producción que la forman
                if line.find(rule_separator):
                    lhs, productions = line.split(rule_separator, 1)
                    lhs = lhs.strip()
                    # En caso de que el símbolo de la izquierda no sea no terminal, se lanza una excepción
                    if not re.search(non_terminal_pattern, lhs):
                        raise ValueError("lhs is not a NT:", lhs)
                    self.non_terminals.add(lhs)
                    # Si es la primera regla leída se almacena como regla de inicio
                    if self.start_rule is None:
                        self.start_rule = (lhs, self.NT)

                    tmp_productions = []
                    # Para cada producción de la regla actual se clasifican los símbolos que la forman como terminales
                    # o no terminales y se almacenan en una lista como tuplas (símbolo, tipo)
                    for production in re.split(production_separator, productions):
                        production = production.strip().replace(r"\|","|")
                        tmp_production = []
                        for symbol in re.split(non_terminal_pattern, production):
                            symbol = symbol.replace(r"\<", "<").replace(r"\>", ">")
                            if len(symbol) == 0:
                                continue
                            elif re.match(non_terminal_pattern, symbol):
                                tmp_production.append((symbol, self.NT))
                            else:
                                self.terminals.add(symbol)
                                tmp_production.append((symbol, self.T))

                        tmp_productions.append(tmp_production)
                    # Si la regla es nueva se guarda el símbolo que la define asociado a las reglas de producción
                    # que lo forman.
                    if lhs not in self.rules:
                        self.rules[lhs] = tmp_productions
                    else:
                        raise ValueError("lhs should be unique", lhs)
                else:
                    raise ValueError("Each rule must be on one line")

    def __str__(self):
        return "%s %s %s %s" % (self.terminals, self.non_terminals,
                                self.rules, self.start_rule)

    def decode(self, _input):
        """
        Función utilizada para el mapeo entre genotipo y fenotipo de cada individuo.

        :param _input: genotipo de un individuo
        :return: fenotipo del individuo
        """
        # Contador de codones utilizados
        used_input = 0
        # Contador de wrapping realizado
        wraps = 0
        # Lista con los símbolos terminales decodificados
        phen_output = []
        # Lista con las posibles producciones
        production_choices = []
        # Símbolos por utilizar
        unexpanded_symbols = [self.start_rule]
        # Se realiza la decodificación mientras queden símbolos no utilizados en la lista y no se haya realizado el
        # número máximo de wraps.
        while wraps <= MAX_WRAPS and len(unexpanded_symbols) > 0:
            if used_input % len(_input) == 0 and used_input > 0 and len(production_choices) > 1:
                wraps += 1
            # Se extrae el símbolo actual de la lista
            current_symbol = unexpanded_symbols.pop(0)
            # Si es terminal, se añade al fenotipo
            if current_symbol[1] != self.NT:
                phen_output.append(current_symbol[0])
            # Si es no terminal se guardan las opciones de producción de la regla y se utiliza un codón de la secuencia
            # para escoger entre ellas
            else:
                production_choices = self.rules[current_symbol[0]]
                current_production = _input[used_input % len(_input)] % len(production_choices)

                if len(production_choices) > 1:
                    used_input += 1
                # Se añade el símbolo seleccionado a la lista
                unexpanded_symbols = production_choices[current_production] + unexpanded_symbols

        # Si tras terminar el bucle de decodificación, esta no se ha completado, se repara el individuo
        # o se devuelve vacío el fenotipo
        if len(unexpanded_symbols) > 0:
            if REPAIR:
                return self.repair_individual(phen_output, unexpanded_symbols, _input)
            else:
                return None
        # La decodificación se ha completado correctamente y se transforma el fenotipo en una cadena de texto
        phen_output = "".join(phen_output)

        return phen_output

    def repair_individual(self, phen_output, unexpanded_symbols, _input):
        """
        Reparación de individuos inválidos.

        Un individuo se considera inválido en caso de que, tras aplicar el número de wrapps predefinido, no se haya podido
        completar su decodificación.
        La reparación de cada individuo se realiza de forma determinista, reutilizando sus codones de la siguiente forma:
        - Los símbolos no terminales '<expr>' se sustituyen por '<var>' y se utiliza el primer codón de la cadena para
        seleccionar el símbolo terminal correspondiente a esta última regla de producción.
        - Los símbolos no terminales '<op>' se sustituyen por el símbolo terminal correspondiente utilizando el segundo
        codón de la cadena.
        - Los símbolos no terminales '<pre-op>' se sustituyen por el símbolo terminal correspondiente utilizando el
        tercer codón de la cadena.
        - Los símbolos no terminales '<var>' se sustituyen por el símbolo terminal correspondiente utilizando el cuarto
        codón de la cadena.

        En caso de que la longitud del genoma no sea suficiente se utiliza el codón anterior en cada uno de los casos.

        De esta forma se mantiene la restricción de que con la misma secuencia de codones se obtenga siempre el mismo
        fenotipo.

        :param phen_output: fenotipo incompleto del individuo
        :param unexpanded_symbols: símbolos no terminales que no se han decodificado
        :param _input: genotipo del individuo
        :return: fenotipo del individuo
        """
        while len(unexpanded_symbols) > 0:
            current_symbol = unexpanded_symbols.pop(0)
            if current_symbol[1] != self.NT:
                phen_output.append(current_symbol[0])
            else:
                if current_symbol[0] == '<expr>':
                    production_choices = self.rules['<var>']
                    current_production = _input[0] % len(production_choices)

                if current_symbol[0] == '<op>':
                    production_choices = self.rules[current_symbol[0]]
                    if len(_input) == 1:
                        current_production = _input[0] % len(production_choices)
                    elif len(_input) > 1:
                        current_production = _input[1] % len(production_choices)

                if current_symbol[0] == '<pre-op>':
                    production_choices = self.rules[current_symbol[0]]
                    if len(_input) == 1:
                        current_production = _input[0] % len(production_choices)
                    elif len(_input) == 2 :
                        current_production = _input[1] % len(production_choices)
                    elif len(_input) > 2:
                        current_production = _input[2] % len(production_choices)

                if current_symbol[0] == '<var>':
                    production_choices = self.rules[current_symbol[0]]
                    if len(_input) == 1:
                        current_production = _input[0] % len(production_choices)
                    elif len(_input) == 2:
                        current_production = _input[1] % len(production_choices)
                    elif len(_input) == 3:
                        current_production = _input[2] % len(production_choices)
                    elif len(_input) > 3:
                        current_production = _input[3] % len(production_choices)

                current_symbol = production_choices[current_production][0]
                phen_output.append(current_symbol[0])

        phen_output = "".join(phen_output)
        return phen_output
