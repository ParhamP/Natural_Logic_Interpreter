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
                new_expression_object = Definer(i)
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
                new_expression_object = Definer(i)
                parsed_expression_list.append(new_expression_object)
            return parsed_expression_list

        elif self.operator_recognizer() == "Conditional":
            condt_matched = re.match(self.conditional_regex, self.expression)
            condt_object1 = Definer(condt_matched.group(1))
            condt_object2 = Definer(condt_matched.group(2))
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

# ------------------------------------------------------------------------------


class Definer(Expression):

    def __init__(self, expression):
        Expression.__init__(self, expression)

    def definer(self, knowledge_dict):
        if self.operator_recognizer() == "AND":
            for expression in self.expression_parser():
                if "NOT" not in expression.expression:
                    knowledge_dict[expression] = True
                else:
                    expression.negative_reverser()
                    knowledge_dict[expression] = False
            return True

        elif self.operator_recognizer() == "OR":
            expression_in_dict = False

            for expression in self.expression_parser():
                if expression in knowledge_dict:
                    expression_in_dict = True
                    break
            if expression_in_dict is True:
                for expression in self.expression_parser():
                    if expression not in knowledge_dict:
                        knowledge_dict[expression] = None
                # count to check if all elements are false
                count = 0
                for expression in self.expression_parser():
                    if knowledge_dict[expression] is True:
                        return True
                    if knowledge_dict[expression] is False:
                        count += 1
                if count == len(self.expression_parser()):
                    return False
                else:
                    return None
            else:
                for expression in self.expression_parser():
                    if expression not in knowledge_dict:
                        knowledge_dict[expression] = None
                return True

        elif self.operator_recognizer() == "Conditional":
            for expression in self.expression_parser():
                if "NOT" in self.expression_parser()[expression].expression:
                    continue
                if self.expression_parser()[expression] not in knowledge_dict:
                    knowledge_dict[self.expression_parser()[expression]] = None

            if "NOT" in self.expression_parser()["IF"].expression:
                self.expression_parser()["IF"].negative_reverser()

                if self.expression_parser()["IF"] not in knowledge_dict:
                    return None

                if knowledge_dict[self.expression_parser()["IF"]] is False:
                    if "NOT" in self.expression_parser()["THEN"].expression:
                        self.expression_parser()["THEN"].negative_reverser()
                        knowledge_dict[self.expression_parser()["THEN"]] = False
                    else:
                        knowledge_dict[self.expression_parser()["THEN"]] = True
                    return True
                elif knowledge_dict[self.expression_parser()["IF"]] is True:
                    return True
                else:
                    return None
            else:
                if knowledge_dict[self.expression_parser()["IF"]] is True:
                    if "NOT" in self.expression_parser()["THEN"].expression:
                        self.expression_parser()["THEN"].negative_reverser()
                        knowledge_dict[self.expression_parser()["THEN"]] = False
                    else:
                        knowledge_dict[self.expression_parser()["THEN"]] = True
                    return True
                elif knowledge_dict[self.expression_parser()["IF"]] is False:
                    return True
                else:
                    return None

    def special_definer(self, knowledge_dict):
        for expression in self.expression_parser():
            if expression not in knowledge_dict:
                knowledge_dict[expression] = None

        true_count = 0
        for expression in self.expression_parser():
            if knowledge_dict[expression] is None:
                return None
            if knowledge_dict[expression] is False:
                return False
            if knowledge_dict[expression] is True:
                true_count += 1
        if true_count == len(self.expression_parser()):
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
# ------------------------------------------------------------------------------


class Resolver(Expression):
    def __init__(self, expression):
        Expression.__init__(self, expression)

    def and_resolver(self, knowledge_dict):
        for expression in self.expression_parser():
            if "NOT" in expression.get():
                continue
            if expression not in knowledge_dict or expression is None:
                return None  # Can't be determined

        true_count = 0
        for expression in self.expression_parser():
            if "NOT" in expression.get():
                expression.negative_reverser()
                if knowledge_dict[expression] is True:
                    return False
                if knowledge_dict[expression] is False:
                    true_count += 1
            else:
                if knowledge_dict[expression] is False:
                    return False
                if knowledge_dict[expression] is True:
                    true_count += 1
        if true_count == len(self.expression_parser()):
            return True

    def or_resolver(self, knowledge_dict):
        for expression in self.expression_parser():
            if "NOT" in expression.get():
                continue
            if expression not in knowledge_dict or expression is None:
                return None  # Can't be determined

        # count to check if all elements are false
        count = 0
        for expression in self.expression_parser():
            if "NOT" in expression.get():
                expression.negative_reverser()
                if knowledge_dict[expression] is False:
                    return True
                if knowledge_dict[expression] is True:
                    count += 1
            else:
                if knowledge_dict[expression] is True:
                    return True
                if knowledge_dict[expression] is False:
                    count += 1

        if count == len(self.expression_parser()):
            return False
        else:
            return None

    def conditional_resolver(self, knowledge_dict):
        if_statement = self.expression_parser()["IF"]
        then_statement = self.expression_parser()["THEN"]

        if then_statement not in knowledge_dict:
            knowledge_dict[then_statement] = None

        if "NOT" in if_statement.get() and "NOT" not in then_statement.get():
            if_statement.negative_reverser()
            if if_statement not in knowledge_dict:
                return None
            if knowledge_dict[if_statement] is False and knowledge_dict[
                    then_statement] is False:
                return False
            elif knowledge_dict[if_statement] is True:
                return True
            elif knowledge_dict[if_statement] is False and knowledge_dict[
                    then_statement] is True:
                return True
            else:
                return None

        elif "NOT" in if_statement.get() and "NOT" in then_statement.get():
            if_statement.negative_reverser()
            then_statement.negative_reverser()
            if if_statement not in knowledge_dict:
                return None
            if knowledge_dict[if_statement] is False and knowledge_dict[
                    then_statement] is True:
                return False
            elif knowledge_dict[if_statement] is True:
                return True
            elif knowledge_dict[if_statement] is False and knowledge_dict[
                    then_statement] is False:
                return True
            else:
                return None

        elif "NOT" not in if_statement.get() and "NOT" in then_statement.get():
            then_statement.negative_reverser()
            if if_statement not in knowledge_dict:
                return None
            if knowledge_dict[if_statement] is True and knowledge_dict[
                    then_statement] is True:
                return False
            elif knowledge_dict[if_statement] is False:
                return True
            elif knowledge_dict[if_statement] is True and knowledge_dict[
                    then_statement] is False:
                return True
            else:
                return None

        else:
            if knowledge_dict[if_statement] is True and knowledge_dict[
                    then_statement] is False:
                return False
            elif knowledge_dict[if_statement] is False:
                return True
            elif knowledge_dict[if_statement] is True and knowledge_dict[
                    then_statement] is True:
                return True
            else:
                return None
# ------------------------------------------------------------------------------


def interpreter(expression):
    # Let's check to see if we have an AND operator that was part of an AND
    flag = False
    if expression[-1] == "@":
        flag = True
        # Flag has become True and we can normalize the expression again
        expression = expression[0:-1]

    expression_object = Definer(expression)

    if expression_object.operator_recognizer() == "Pure":
        if "NOT" not in expression_object.get():
            knowledge_dict[expression_object] = True
        else:
            expression_object.negative_reverser()
            knowledge_dict[expression_object] = False

    elif expression_object.is_pure_proposition():
        if flag:
            knowledge_dict[expression_object] = expression_object.special_definer(
                knowledge_dict)
        else:
            knowledge_dict[expression_object] = expression_object.definer(
                knowledge_dict)

    else:
        parsed_expression = expression_object.expression_parser()

        if flag:
            knowledge_dict[expression_object] = expression_object.special_definer(
                knowledge_dict)
        else:
            knowledge_dict[expression_object] = expression_object.definer(
                knowledge_dict)

        # Check to see if it is conditional so we can mark its IF proposition
        if expression_object.operator_recognizer() == "Conditional":
            for expression in parsed_expression.values():

                expression_type = expression.operator_recognizer()

                if expression.conditional_and_checker() is True:
                    parsed_expression["IF"].and_temp_transformer()

                if expression_type != "Pure" and expression_type != "Broken":
                    interpreter(expression.get())

        else:
            for expression in parsed_expression:
                expression_type = expression.operator_recognizer()

                # Check to see if any AND  was part of an OR proposition
                if expression.and_in_or_checker(expression_object) is True:
                    expression.and_temp_transformer()

                if expression_type != "Pure" and expression_type != "Broken":
                    interpreter(expression.get())
# ------------------------------------------------------------------------------


def validator(expression):
    expression_object = Resolver(expression)
    expression_object_type = expression_object.operator_recognizer()

    if expression_object_type == "Pure":
        if expression_object not in knowledge_dict:
            return None
        else:
            return knowledge_dict[expression_object]

    elif expression_object.is_pure_proposition() is True:
        if expression_object_type == "AND":
            return expression_object.and_resolver(knowledge_dict)
        elif expression_object_type == "OR":
            return expression_object.or_resolver(knowledge_dict)
        elif expression_object_type == "Conditional":
            return expression_object.conditional_resolver(knowledge_dict)
    else:
        pass