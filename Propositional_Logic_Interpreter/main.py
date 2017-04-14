import re

knowledge_dict = dict()


class Expression:

    def __init__(self, expression):
        self.expression = expression
        self.keywords = ["OR", "AND", "IF", "THEN"]
        self.and_regex = r"(\(+.*?\)+) AND (\(+.*\)+)( AND \(+.*\)+)*$"
        self.or_regex = r"(\(+.*?\)+) OR (\(+.*\)+)( OR \(+.*\)+)*$"
        self.conditional_regex = r"IF (\(.*\)) THEN (\(.*\))$"

    def get(self):
        return self.expression

    def set(self, new_expression):
        self.expression = new_expression

    def __eq__(self, other):
        return self.get() == other.get()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.expression)

    def __str__(self):
        return self.expression

    def operator_recognizer(self):

        if re.match(self.or_regex, self.expression):
            p = re.compile(self.or_regex)
            m = re.match(p, self.expression)
            for i in m.groups()[:-1]:
                if "))" in i and "((" not in i or "((" in i and "))" not in i:
                    return "AND"
            return "OR"
        elif re.match(self.and_regex, self.expression):
            p = re.compile(self.and_regex)
            m = re.match(p, self.expression)
            for i in m.groups()[:-1]:
                if "))" in i and "((" not in i or "((" in i and "))" not in i:
                    return "OR"
            return "AND"
        elif re.match(self.conditional_regex, self.expression):
            return "Conditional"
        else:
            flag = True
            for i in self.keywords:
                if i in self.expression:
                    flag = False
                    break
            if flag:
                return "Pure"
            else:
                return "Broken"

    def expression_parser(self):
        if self.operator_recognizer() == "AND":
            parsed_expression = []
            match = re.match(self.and_regex, self.expression)
            groups = match.groups()[:-1]
            for expression in groups:
                parsed_expression.append(expression)

            for i in parsed_expression:
                if "))" in i and "((" in i:
                    list_index = parsed_expression.index(i)
                    i = i[1:-1]
                    parsed_expression[list_index] = i
                elif "((" in i:
                    list_index = parsed_expression.index(i)
                    double_paren_index = i.index("((")
                    i = i[:double_paren_index] + i[double_paren_index + 1:]
                    parsed_expression[list_index] = i
                elif "))" in i:
                    list_index = parsed_expression.index(i)
                    double_paren_index = i.index("))")
                    i = i[:double_paren_index + 1] + i[double_paren_index + 2:]
                    parsed_expression[list_index] = i
            parsed_expression_list = []
            for i in parsed_expression:
                new_expression_object = Expression(i)
                parsed_expression_list.append(new_expression_object)
            return parsed_expression_list

        elif self.operator_recognizer() == "OR":
            parsed_expression = []
            match = re.match(self.or_regex, self.expression)
            groups = match.groups()[:-1]
            for expression in groups:
                parsed_expression.append(expression)
            for i in parsed_expression:
                if "))" in i and "((" in i:
                    list_index = parsed_expression.index(i)
                    i = i[1:-1]
                    parsed_expression[list_index] = i
                elif "((" in i:
                    list_index = parsed_expression.index(i)
                    i = i[1:]
                    parsed_expression[list_index] = i
                elif "))" in i:
                    list_index = parsed_expression.index(i)
                    i = i[:-1]
                    parsed_expression[list_index] = i
            parsed_expression_list = []
            for i in parsed_expression:
                new_expression_object = Expression(i)
                parsed_expression_list.append(new_expression_object)
            return parsed_expression_list

        elif self.operator_recognizer() == "Conditional":
            condt_matched = re.match(self.conditional_regex, self.expression)
            condt_object1 = Expression(condt_matched.group(1))
            condt_object2 = Expression(condt_matched.group(2))
            parsed_expression = {"IF": condt_object1,
                                 "THEN": condt_object2}
            return parsed_expression

    def is_pure_proposition(self):
        if self.operator_recognizer() == "Conditional":
            parsed_expression = self.expression_parser()
            for expression in parsed_expression:
                if parsed_expression[expression].operator_recognizer() != "Pure":
                    return False
            return True

        else:
            for i in self.expression_parser():
                if i.operator_recognizer() != "Pure":
                    return False
            return True

    def negative_reverser(self):
        expression = self.expression
        expression = expression[0] + expression[5:]
        self.expression = expression

    def definer(self, knowledge_dict):
        if self.operator_recognizer() == "AND":
            parsed_expression = self.expression_parser()
            for expression in parsed_expression:
                if "NOT" not in expression.expression:
                    knowledge_dict[expression] = True
                else:
                    expression.negative_reverser()
                    knowledge_dict[expression] = False
            return True
            #
            # # Else means that at some point the expression's parts have been updated
            # else:
            #     for expression in parsed_expression:
            #         if expression not in knowledge_dict:
            #             knowledge_dict[expression] = None
            #
            #     # Let's check if all the expression are True
            #     true_count = 0
            #     for expression in parsed_expression:
            #         if knowledge_dict[expression] is None:
            #             return None
            #         if knowledge_dict[expression] is False:
            #             return False
            #         if knowledge_dict[expression] is True:
            #             true_count += 1
            #
            #     if true_count == len(parsed_expression):
            #         return True

        elif self.operator_recognizer() == "OR":
            parsed_expression = self.expression_parser()

            expression_in_dict = False

            for expression in parsed_expression:
                if expression in knowledge_dict:
                    expression_in_dict = True
                    break
            if expression_in_dict is True:
                for expression in parsed_expression:
                    if expression not in knowledge_dict:
                        knowledge_dict[expression] = None
                # count to check if all elements are false
                count = 0
                for expression in parsed_expression:
                    if knowledge_dict[expression] is True:
                        return True
                    if knowledge_dict[expression] is False:
                        count += 1
                if count == len(parsed_expression):
                    return False
                else:
                    return None
            else:
                for expression in parsed_expression:
                    if expression not in knowledge_dict:
                        knowledge_dict[expression] = None
                return True

        elif self.operator_recognizer() == "Conditional":
            parsed_expression = self.expression_parser()
            for expression in parsed_expression:
                if "NOT" in parsed_expression[expression].expression:
                    continue
                if parsed_expression[expression] not in knowledge_dict:
                    knowledge_dict[parsed_expression[expression]] = None

            if "NOT" in parsed_expression["IF"].expression:
                parsed_expression["IF"].negative_reverser()

                if parsed_expression["IF"] not in knowledge_dict:
                    return None

                if knowledge_dict[parsed_expression["IF"]] is False:
                    if "NOT" in parsed_expression["THEN"].expression:
                        parsed_expression["THEN"].negative_reverser()
                        knowledge_dict[parsed_expression["THEN"]] = False
                    else:
                        knowledge_dict[parsed_expression["THEN"]] = True
                    return True
                elif knowledge_dict[parsed_expression["IF"]] is True:
                    return True
                else:
                    return None
            else:
                if knowledge_dict[parsed_expression["IF"]] is True:
                    if "NOT" in parsed_expression["THEN"].expression:
                        parsed_expression["THEN"].negative_reverser()
                        knowledge_dict[parsed_expression["THEN"]] = False
                    else:
                        knowledge_dict[parsed_expression["THEN"]] = True
                    return True
                elif knowledge_dict[parsed_expression["IF"]] is False:
                    return True
                else:
                    return None

    def special_definer(self, knowledge_dict):
        parsed_expression = self.expression_parser()
        for expression in parsed_expression:
            if expression not in knowledge_dict:
                knowledge_dict[expression] = None
        # for expression in parsed_expression:
        #     if knowledge_dict[expression] is None:
        #         return None
        #     if knowledge_dict[expression] is False:
        #         return False
        #     else:
        #         return True

        true_count = 0
        for expression in parsed_expression:
            if knowledge_dict[expression] is None:
                return None
            if knowledge_dict[expression] is False:
                return False
            if knowledge_dict[expression] is True:
                true_count += 1
        if true_count == len(parsed_expression):
            return True


    def and_in_or_checker(self, or_expression):

        if self.operator_recognizer() == "AND" and or_expression.operator_recognizer() == "OR":
            return True
        else:
            return None

    def conditional_and_checker(self):
        if self.operator_recognizer() == "AND":
            return True
        else:
            return None

    def and_temp_transformer(self):
        self.expression = self.expression + "@"


def interpreter(expression):
    # Let's check to see if we have an AND operator that was part of an AND
    flag = False
    if expression[-1] == "@":
        flag = True
        # Flag has become True and we can normalize the expression again
        expression = expression[0:-1]

    expression_object = Expression(expression)

    if expression_object.operator_recognizer() == "Pure":
        if "NOT" not in expression_object.expression:
            knowledge_dict[expression_object] = True
        else:
            expression_object.negative_reverser()
            knowledge_dict[expression_object] = False
    elif expression_object.is_pure_proposition():
        if flag:
            knowledge_dict[expression_object] = expression_object.special_definer(
                knowledge_dict)
        else:
            knowledge_dict[expression_object] = expression_object.definer(knowledge_dict)

    else:
        parsed_expression = expression_object.expression_parser()

        if flag:
            knowledge_dict[expression_object] = expression_object.special_definer(
                knowledge_dict)
        else:
            knowledge_dict[expression_object] = expression_object.definer(knowledge_dict)

        # Check to see if it is conditional so we can mark its IF proposition
        if expression_object.operator_recognizer() == "Conditional":
            for i in parsed_expression.values():

                expression_type = i.operator_recognizer()

                if i.conditional_and_checker() is True:
                    parsed_expression["IF"].and_temp_transformer()

                if expression_type != "Pure" and expression_type != "Broken":
                    interpreter(i.expression)

        else:
            for i in parsed_expression:
                expression_type = i.operator_recognizer()

                # Check to see if any AND  was part of an OR proposition
                if i.and_in_or_checker(expression_object) is True:
                    i.and_temp_transformer()

                if expression_type != "Pure" and expression_type != "Broken":
                    interpreter(i.expression)


def validator(expression):
    expression_object = Expression(expression)

    if expression_object.operator_recognizer() == "Pure":
        if expression_object not in knowledge_dict:
            return None
        else:
            return knowledge_dict[expression_object]

    elif expression_object.is_pure_proposition() is True:
        pass
