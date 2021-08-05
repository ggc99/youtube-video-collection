from PyInquirer import prompt, Separator, style_from_dict, Token
from prompt_toolkit.validation import Validator, ValidationError

ACTION_INPUT_NAME = 'action'
WORDS_CONFIRMATION_NAME = 'keywords_continue'
TABS_INPUT_NAME = 'number_of_tabs'

class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end

action_options = {
        'search':'Search for videos',
        'open':'Open videos',
        'quit': 'Quit'
     }

prompts = {
        'action': [
            {
                'type':'list',
                'name': ACTION_INPUT_NAME,
                'message':'Select an action',
                'choices': list(action_options.values())
            }
        ],
        'keywords_confirmation': [
            {
                'type': 'confirm',
                'message': 'Do you want to continue with these keywords',
                'name': WORDS_CONFIRMATION_NAME,
                'default': True,
            }
        ],
        'number_of_tabs':[
            {
                'type': 'input',
                'name': TABS_INPUT_NAME,
                'message': 'How many videos opened?',
                'validate': NumberValidator,
                'filter': lambda val: int(val)
            }
        ],
        'translate_flag': [
            {
                'type': 'confirm',
                'message': 'Do you want to translate these keywords',
                'name': 'translate_flag',
                'default': True,
            }
        ],
        'number_of_results':[
            {
                'type': 'input',
                'name': 'number_of_results',
                'message': 'How many results do you want?',
                'validate': NumberValidator,
                'filter': lambda val: int(val)
            }
        ],
    }            
        

def prompt_question(prompt_type):
    
    prompt_styles = style_from_dict({
        Token.Separator: '#cc5454',
        Token.QuestionMark: '#673ab7 bold',
        Token.Selected: '#cc5454',  # default
        Token.Pointer: '#673ab7 bold',
        Token.Instruction: '',  # default
        Token.Answer: '#f44336 bold',
        Token.Question: '',
    })

    questions = prompts[prompt_type]

    answers = prompt(questions, style=prompt_styles)

    return answers

def print_msg(content, header='', subheader='', list_content=[]):
    if header:
        print('='*30)
        print(header)
        print('='*30)
    if subheader: 
        print('\n' + subheader + '\n')
    if len(list_content) > 0:
        for item in list_content:
            print(item)
    if content:
        print(content + '\n')

