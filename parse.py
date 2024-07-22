def parse(tokens):
            # Inicialização da pilha com símbolo final e inicial
            stack = ['$', 'MAIN']

            index = 0
            step_number = 0

            #Inicialização da árvore de derivação 
            derivation_steps = [{'step': step_number, 'production': 'Start', 'current_string': 'MAIN', 'stack': ' '.join(reversed(stack))}]

            parse_tree = {'value': 'MAIN', 'children': []}
            parse_stack = [{'node': parse_tree, 'token': 'MAIN'}]
            count_linhas = 0  # para ajudar a debugar no console

            # Enquanto a pilha conter mais de um elemento e o indice estar dentro do limite do vetor de tokens
            while len(stack) > 1 or index < len(tokens) - 1:

                if count_linhas > 1000:
                    print("Dando break para evitar loop infinito")
                    break

                # Obtenção do token atual
                token = tokens[index]
                print(f"{count_linhas} Stack: {stack}, Token: {token}")
                count_linhas += 1
                
                # Atualizando o ultimo elemento da pilha
                top = stack.pop()

                #print(f"Stack: {stack}, Token: {token}")
                current_parse_node = parse_stack.pop()

                if top == token:
                    index += 1
                elif top in parsing_table and token in parsing_table[top]:
                    production = parsing_table[top][token]
                    if production == ['ELSE_DANGLING']:
                        if token == 'else':
                            production = ['else', 'STMT'] 
                        else:
                            production = ['ε']
                    stack.extend(reversed([x for x in production if x != 'ε']))

                    # Para desenhar á arvore de derivação
                    derivation_steps.append({'step': step_number, 'production': f"{top} → {' '.join(production)}", 'current_string': ''.join(stack), 'stack': ' '.join(reversed(stack))})
                    
                    #Atualização da árvore de análise sintática
                    for symbol in reversed(production):
                        if symbol != 'ε':
                            new_node = {'value': symbol, 'children': []}
                            current_parse_node['node']['children'].append(new_node)
                            parse_stack.append({'node': new_node, 'token': symbol})
                else:
                    # Tratamento de erros
                    return {'result': f"Syntax error: expected '{top}' but found '{token}' at position {index}", 'derivation_steps': derivation_steps, 'parse_tree': parse_tree}
                step_number += 1

            # Para desenhar á arvore de derivação
            derivation_steps.append({'step': step_number + 1, 'production': 'End', 'current_string': ''.join(stack), 'stack': ' '.join(reversed(stack))})

            return {'result': "Accepted", 'derivation_steps': derivation_steps, 'parse_tree': parse_tree}