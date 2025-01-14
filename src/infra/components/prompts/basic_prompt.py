
from src.core.components.prompt.interface.prompt_interface import InputBasicPromptDto, PromptInterface
from src.infra.components.tools.tokenizer.tokenizer_tiktoken import TokenizerTikToken



class BasicPrompt(PromptInterface):
    
    def prompt(self, input: InputBasicPromptDto) -> str:
        chunks = input.context
        topics = ['Definição e funcionamento', 'Cursos e serviços oferecidos', 'Gratuidade e custos', 'Perguntas gerais']
        
        has_history = isinstance(input.memory, list) and len(input.memory) != 0
        prompt = '''### Instruções:\n'''
        prompt += f'''Você é um assistente pessoal da SECRETARIA ENAP responsável por responder perguntas dos usuários, especificamente na parte de SECRETARIA da ENAP. O usuário é um estudante, portanto, você não deve utilizar emojis ou formatar o texto de forma engraçada. Utilize apenas caracteres textuais, sem emoticons em nenhuma ocasião.'''

        prompt += f"Você responderá perguntas referentes aos seguintes tópicos:\n"
        prompt += '\n'.join(f'* {topic}' for topic in topics)


        prompt += f'''\n Sua resposta deve ser em markdown, utilizando negritos para destacar tópicos, palavras-chave, títulos, etc, pois o usuário irá ler em uma tela web.'''

        prompt += '''\n\n### Restrições:
                - Jamais responda ou cite qualquer informação associado a editais ou regulamentos. NUNCA FAÇA ISSO!;
                '''


        prompt += '''\n\n### Critérios para formar sua resposta:
        - Responda a pergunta do usuário de forma completa e se baseando nos documentos, detalhe se for preciso;
        - Caso seja passado algum link, forneça-o para o usuário;
        - Veja se a pergunta do usuário necessita dos documentos ou se pode ser respondida sem eles;
        - Muitas vezes o usuário deseja continuar uma conversa, portanto, você deve se atentar ao histórico de mensagens fornecido;
        - Caso tenha link, faça com que ele seja acessível;
        - Faça respostas em tópicos e em formato markdown;'''

        prompt += f'''\n\n### Exemplo:
        - Pergunta Exemplo: "Os cursos a distância da EV.G são gratuitos? A quem se destinam?
        - Resposta Esperada: "**Todos os cursos online** da **Escola Virtual.Gov (EV.G)** são **gratuitos**, com emissão de **certificados gratuitamente**. No geral, são **cursos abertos**, **não apresentam limite de vagas** e podem ser cursados **a qualquer momento**, por **qualquer pessoa**, seja ela **servidora pública ou não**."'''

        if has_history:
            # quantidade de conversas anteriores que o modelo se lembra
            conversation_steps = 5
            history = input.memory[-conversation_steps:]

            prompt += '''\n\n### Histórico de mensagens:\n'''
            for message in history:
                history_chunks = message['content']
                history_query = message['query']
                history_response = message['response']

                prompt += f"Documentos:\n"
                prompt += ''.join(f"#* doc:\n{doc}\n\n" for i, doc in enumerate(reversed(history_chunks)))
                prompt += f'Pergunta: {history_query}.\n'
                prompt += f'Resposta: {history_response}.'


        prompt += f'''\n\n### Documentos:\n'''
        prompt += f'''Aqui estão documentos que podem te ajudar a responder a pergunta do usuário. O usuário não tem acesso à estes documentos, então, leia e responda a sua pergunta:\n\n\n\n'''
        # invertendo a ordem de chunks pois os chunks do final são mais vistos
        for i, chunk in enumerate(reversed(chunks)):
            prompt += f'* Doc:\n{chunk}\n\n'

        prompt += f'''\n\n### Utilizando os documentos e o histórico de mensagens, responda: \n'''
        if has_history:
            last_message = history[-1]
            prompt += f"Pergunta: {last_message['query']}\n"
            prompt += f"Resposta Final: {last_message['response']}\n"
            
        prompt += '''\n\n### Restrições:
            - LEMBRE-SE: Jamais responda ou cite qualquer informação associado a editais ou regulamentos. NUNCA FAÇA ISSO!;
            '''
        prompt += f"Pergunta: {input.query}\n"
        prompt += f"Resposta Final: "
        return prompt
        