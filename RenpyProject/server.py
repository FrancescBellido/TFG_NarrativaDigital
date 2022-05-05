from itertools import count
import re
import sys, os
from flask import Flask, jsonify

def override_where():
    return os.path.abspath("cacert.pem")

if hasattr(sys, "frozen"):
    import certifi.core

    os.environ["REQUESTS_CA_BUNDLE"] = override_where()
    certifi.core.where = override_where

    import requests.utils
    import requests.adapters
    requests.utils.DEFAULT_CA_BUNDLE_PATH = override_where()
    requests.adapters.DEFAULT_CA_BUNDLE_PATH = override_where()

app = Flask(__name__)

#Comprobamos si la cadena de texto es ASCII
def is_ascii(stri): 

    for s in stri:
        if s != 'A' and s != 'B' and s != 'C' and s != 'D' and s != 'E' and s != 'F' and s != 'G' and s != 'H' and s != 'I' and s != 'J' and s != 'K' and s != 'L' and s != 'M' and s != 'N' and s != 'O' and s != 'P' and s != 'Q' and s != 'R' and s != 'S' and s != 'T' and s != 'U' and s != 'V' and s != 'W' and s != 'X' and s != 'Y' and s != 'Z' and s != '.' and s != ',' and s != '\'' and s != '!':
            if s != 'a' and s != 'b' and s != 'c' and s != 'd' and s != 'e' and s != 'f' and s != 'g' and s != 'h' and s != 'i' and s != 'j' and s != 'k' and s != 'l' and s != 'm' and s != 'n' and s != 'o' and s != 'p' and s != 'q' and s != 'r' and s != 's' and s != 't' and s != 'u' and s != 'v' and s != 'w' and s != 'x' and s != 'y' and s != 'z' and s != ' ' and s != '' and s != '\n' and s != '\t' and s.isspace() == False:
                return False
    return True

def is_ascii2(stri, version): 

    for s in stri:
        if s != 'A' and s != 'B' and s != 'C' and s != 'D' and s != 'E' and s != 'F' and s != 'G' and s != 'H' and s != 'I' and s != 'J' and s != 'K' and s != 'L' and s != 'M' and s != 'N' and s != 'O' and s != 'P' and s != 'Q' and s != 'R' and s != 'S' and s != 'T' and s != 'U' and s != 'V' and s != 'W' and s != 'X' and s != 'Y' and s != 'Z' and s != '.' and s != ',' and s != '\'' and s != '!' and s != '¡' and s != ':':
            if s != 'a' and s != 'b' and s != 'c' and s != 'd' and s != 'e' and s != 'f' and s != 'g' and s != 'h' and s != 'i' and s != 'j' and s != 'k' and s != 'l' and s != 'm' and s != 'n' and s != 'o' and s != 'p' and s != 'q' and s != 'r' and s != 's' and s != 't' and s != 'u' and s != 'v' and s != 'w' and s != 'x' and s != 'y' and s != 'z' and s != ' ' and s != '' and s.isspace() == False:
                if version != "openai" and version != "english" and s != 'á' and s != 'é' and s != 'í' and s != 'ó' and s != 'ú' and s != 'ñ':
                    return False
    return True

#Comprobamos si la cadena de texto contiene un paréntesis
def thereIsParentesis(stri):

    for s in stri:
        if s == '[' or s == '[' or s == '(' or s == ')':
            return True
    return False

#Comprobar si todos los carácteres de la cadena son iguales
def isAllStringEqual(stri):

    characters = {""}

    for c in stri:
        encontrado = False
        for chVector in characters:
            if chVector == c:
                encontrado = True        
        if encontrado == False:
            characters.add(c)
    
    return len(characters) <= 3

#Sustituimos el carácter ? en la oración para evitar problemas
def constructSequence(sequence):

    newSentence = ""

    for i in sequence:
        if(i == '_'):
            i = '?'
        newSentence += i 

    return newSentence

#Añadimos un punto al final de la oración en caso de no haberlo
def finalizeTextExit(textExit):

    if len(textExit)-1 >= 0:
        if textExit[len(textExit)-1] == ',':
            textExit = textExit[:-1]
        if textExit[len(textExit)-1] != '?' and textExit[len(textExit)-1] != '!' and textExit[len(textExit)-1] != '.':
            textExit += '.' 

    return textExit

#Contamos cuantas veces ha hablado la IA de entrada   
def countOrderConversation(sequence):

    order = 0
    lines = sequence.split('\n')

    for line in lines:
        if line.split(':')[0] == "Suspect" or line.split(':')[0] == "Sospechoso" or  line.split(':')[0] == "Robot":            
            order += 1

    return order      

#Reducimos el número de líneas de diálogo para evitar problemas con el max_length
def deletePartConversation(sequence, counterEmpty):

    linesTotal = sequence.split('\n')   

    if len(linesTotal) >= 6 or counterEmpty > 0:

        linesConver = []
        for line in linesTotal:
            if line.split(':')[0] == "Suspect" or line.split(':')[0] == "Sospechoso" or line.split(':')[0] == "Police" or line.split(':')[0] == "Policía" or line.split(':')[0] == "Robot":
                linesConver.append(line)

        if counterEmpty > 0 and len(linesConver) > 2:
            linesTotal.remove(linesConver[0])
            linesTotal.remove(linesConver[1])
        elif len(linesConver) > 2:
            counter = 0
            while len(linesTotal) >= 6:
                linesTotal.remove(linesConver[counter])
                linesTotal.remove(linesConver[counter+1])
                counter = counter + 2

        else:
            return sequence
    else:
        return sequence

    linesTotal = '\n'.join(linesTotal) 
    return linesTotal

#Buscamos el texto de respuesta de la IA que toca
def searchResponseCountOrder(sequence, order):

    lines = sequence.split('\n')
    lineaIterator = 0
    response = ""

    for line in lines:
        if line.split(':')[0] == "Suspect" or line.split(':')[0] == "Sospechoso" or  line.split(':')[0] == "Robot":       
            lineaIterator += 1     
            if lineaIterator == order:
                if len(line.split(': ')) - 1 > 0:
                    response = line.split(': ')[1]
                else:
                    response = line.split(':')[1]
                break            

    return response

#Nos quedamos con la oración hasta el último punto
def searchEndSentence(textExit):

    if '.' in textExit or '?' in textExit or '!' in textExit:

        lastPoint1 = textExit.rfind('.')
        lastPoint2 = textExit.rfind('?')
        lastPoint3 = textExit.rfind('!')
        lastPoint4 = textExit.find('\n')

        maxPoint = lastPoint1
        if lastPoint2 > maxPoint:
            maxPoint = lastPoint2
        if lastPoint3 > maxPoint:
            maxPoint = lastPoint3

        if '\n' in textExit and maxPoint > lastPoint4:
            maxPoint = lastPoint4

        copyText = ""

        for i in range(0, maxPoint+1):
            copyText += textExit[i]

        textExit = copyText

    return textExit

#Contamos el número de puntos en la oración
def maxPoints(textExit):
    return textExit.count('.')

#Comprobamos si el texto comienza con mayúscula
def startWithMayus(text):
    if text[0] == ' ' or text[0] == 'A' or text[0] == 'B' or text[0] == 'C' or text[0] == 'D' or text[0] == 'E' or text[0] == 'F' or text[0] == 'G' or text[0] == 'H' or text[0] == 'I' or text[0] == 'J' or text[0] == 'K' or text[0] == 'L' or text[0] == 'M' or text[0] == 'N' or text[0] == 'O' or text[0] == 'P' or text[0] == 'Q' or text[0] == 'R' or text[0] == 'S' or text[0] == 'T' or text[0] == 'U' or text[0] == 'V' or text[0] == 'W' or text[0] == 'X' or text[0] == 'Y' or text[0] == 'Z':
        return True
    return False

#Cortamos la oración en el primer punto
def truncarHastaPrimerPunto(text):
    finalText = ""
    for s in text:
        finalText = finalText + s
        if s == ".":
           break
    return finalText

#Comprobamos cúales de las condiciones del while son correctas
def comprobarCondiciones(text, version):
    print("CONDICION 1: " + str(text == ""))
    print("CONDICION 2: " + str(len(text) < 7))
    print("CONDICION 3: " + str(len(text) > 200))
    if text != "":
        print("CONDICION 4: " + str(startWithMayus(text) == False))
        print("CONDICION 5: " + str(isAllStringEqual(text) == True))
        print("CONDICION 6: " + str(maxPoints(text) > 1))  
        print("CONDICION 7: " + str(thereIsParentesis(text)))
        print("CONDICION 8: " + str(version == "openai" and is_ascii(text) == False))
        print("CONDICION 9: " + str((version == "maria-large" or version == "maria-base") and is_ascii2(text, version) == False))   

#Comprobamos si la nueva línea es igual a alguna anterior
def lineasIguales(sequence, text):

    b = False
    lines = sequence.split('\n')

    for line in lines:
        if line == text:
            b = True

    return b

@app.route('/gpt2/<string:version>/<string:sequence>')
def getSentenceGPT2(version, sequence):   

    import torch
    if version == "openai":        
        from transformers import GPT2LMHeadModel, GPT2Tokenizer
        tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        model = GPT2LMHeadModel.from_pretrained('gpt2', pad_token_id=tokenizer.eos_token_id)
    elif version == "maria-large":
        from transformers import AutoTokenizer, AutoModelForCausalLM 
        tokenizer = AutoTokenizer.from_pretrained("PlanTL-GOB-ES/gpt2-large-bne")
        model = AutoModelForCausalLM.from_pretrained("PlanTL-GOB-ES/gpt2-large-bne", pad_token_id=tokenizer.eos_token_id)
    elif version == "maria-base":
        from transformers import AutoTokenizer, AutoModelForCausalLM 
        tokenizer = AutoTokenizer.from_pretrained("PlanTL-GOB-ES/gpt2-base-bne")
        model = AutoModelForCausalLM.from_pretrained("PlanTL-GOB-ES/gpt2-base-bne", pad_token_id=tokenizer.eos_token_id)

    #sequence: "Me: What are you doing? Jackie:"
    sequence = constructSequence(sequence)

    initialSequence = "The following conversation is the police interrogation of a murder suspect. The suspect answers very sure of his innocence and in perfect English.\n"
    if version == "maria-large" or version == "maria-base":
        initialSequence = "La siguiente conversación es el interrogatorio de la policía a un sospechoso por asesinato. El sospechoso responde muy seguro de su inocencia y en un perfecto castellano.\n"

    sequence = initialSequence + sequence   
    order = countOrderConversation(sequence)

    text = ""
    counterEmpty = -1
    preSequence = sequence
    while text == "" or len(text) < 7 or len(text) > 200 or startWithMayus(text) == False or isAllStringEqual(text) == True or lineasIguales(preSequence, text) == True or maxPoints(text) > 1 or thereIsParentesis(text) or (version == "openai" and is_ascii(text) == False) or ((version == "maria-large" or version == "maria-base") and is_ascii2(text, version) == False):         

        if text == "":
            counterEmpty = counterEmpty + 1
        preSequence = sequence
        sequence = deletePartConversation(sequence, counterEmpty)
        order = countOrderConversation(sequence)
        if preSequence != sequence:
            counterEmpty = -1

        if version != "maria-large" and version != "maria-base" and version != "spanish":
            inputs = tokenizer.encode(sequence, return_tensors='pt', add_special_tokens=False, return_overflowing_tokens=False, return_special_tokens_mask=False)
            outputs = model.generate(inputs, max_length=len(sequence)+10, do_sample=True) 
        else:
            inputs = tokenizer.encode(sequence, return_tensors='pt', return_overflowing_tokens=False, return_special_tokens_mask=False)
            outputs = model.generate(inputs, max_length=len(sequence)+120, do_sample=True)             
         
        text = tokenizer.decode(outputs[0], skip_special_tokens=True)        
        text = searchResponseCountOrder(text, order)
        text = searchEndSentence(text)  
        text = truncarHastaPrimerPunto(text)    
        #comprobarCondiciones(text, version) 

    textExit = ' ' + text
    textExit = finalizeTextExit(textExit)    
    return jsonify({"message": textExit})

@app.route('/gpt3/<string:version>/<string:sequence>')
def getSentenceGPT3(version, sequence):  

    import openai
      
    OPENAI_API_KEY="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"
    openai.organization = "org-HBdIePLkSXQJKL3DVKc07ING"
    openai.api_key = OPENAI_API_KEY
    openai.Engine.list()

    sequence = constructSequence(sequence)

    if version == "spanish":
        initialSequence = "La siguiente conversación es el interrogatorio de la policía a un sospechoso por asesinato. El sospechoso responde muy seguro de su inocencia y en un perfecto castellano.\n"
    else:
        initialSequence = "The following conversation is the police interrogation of a murder suspect. The suspect answers very sure of his innocence and in perfect English.\n"
    sequence = initialSequence + sequence

    text = ""
    preSequence = sequence
    while text == "" or len(text) < 7 or startWithMayus(text) == False or isAllStringEqual(text) == True or lineasIguales(preSequence, text) == True or maxPoints(text) > 1 or thereIsParentesis(text) or (version == "english" and is_ascii(text) == False) or (version == "spanish" and is_ascii2(text, version) == False):

        if version == "english":
            response = openai.Completion.create(
                engine="davinci",
                prompt=sequence,
                temperature=1,
                max_tokens=100,
                top_p=1,
                n=1,
                frequency_penalty=0,
                presence_penalty=0,
                stop=["\n","Police:","Suspect:","Text:"]
            )
        else:
            response = openai.Completion.create(
                engine="davinci",
                prompt=sequence,
                temperature=1,
                max_tokens=100,
                top_p=1,
                n=1,
                frequency_penalty=0,
                presence_penalty=0,
                stop=["\n","Policía:","Sospechoso:","Texto:"]
            )
        
        text = response.choices[0].text

    textExit = text.strip()
    textExit = finalizeTextExit(textExit) 
    textExit = " ".join( textExit.split() )
    
    return jsonify({"message": textExit})

if __name__ == '__main__':
    app.run(debug=False, port=4000)