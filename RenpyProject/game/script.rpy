init python:

    import requests, random

    #Sustituimos el carácter ? en la oración para evitar problemas
    def prepareSentence(sentence):
        newSentence = ""
        for i in sentence:
            if i == '?':
                i = '_'
            newSentence += i        
        return newSentence    

    #Añadimos un punto al final de la oración en caso de no haberlo
    def prepareMessage(message):
        if not '.' in message and not '!' in message and not '?' in message and not '_' in message:
            message += '.'
        return message

    #Obtenemos respuesta de la IA
    def responseIAprepareSentence(sentence):
        sentence = sentence.strip()
        sentence = prepareMessage(sentence)        
        sentence = prepareSentence(sentence)   
        return sentence

    def responseIAprepareConversation(sentence, conversation, model, version):
        if version == "english" or version == "openai":
            conversation += "\nPolice: " + sentence + "\nSuspect:"    
        else:
            conversation += "\nPolicía: " + sentence + "\nSospechoso:"  
        return conversation 

    def reponseIAgetMessage(conversation, model, version):
        response = requests.get('http://localhost:4000/' + model + '/' + version + '/' + conversation).json()
        message = response["message"] 
        message = message.strip()
        return message
    
    def responseSumConversation (message, conversation, model):
        if model == "gpt2":
            conversation += ' ' + message  
            conversation = deletePartConversation(conversation)
        else:
            conversation += message 
        conversation = prepareMessage(conversation)
        conversation = prepareSentence(conversation)
        return conversation  

    #Reducimos el número de líneas de diálogo para evitar problemas con el max_length
    def deletePartConversation(sequence):

        linesTotal = sequence.split('\n')   

        if len(linesTotal) >= 6:

            linesConver = []
            for line in linesTotal:
                if line.split(':')[0] == "Suspect" or line.split(':')[0] == "Sospechoso" or line.split(':')[0] == "Police" or line.split(':')[0] == "Policía" or line.split(':')[0] == "Robot":
                    linesConver.append(line)

            counter = 0
            while len(linesTotal) >= 6:
                linesTotal.remove(linesConver[counter])
                linesTotal.remove(linesConver[counter+1])
                counter = counter + 2

        else:
            return sequence

        linesTotal = '\n'.join(linesTotal) 
        return linesTotal      

image bg room dark:
    "Bedroom_Night_Dark.png"

image bg room:
    "Bedroom_Night.png"

image bg interrogation:
    "club room a day.png"
    zoom 1.0

image bg train:
    "Train_Night.png"

label start:

    $num_pregs1 = 0
    $num_pregs2 = 0
    $num_pregs3 = 0

    scene bg room dark  
    play music "audio/613178__sound-designer-from-turkey__music-box-g-4-4-60-bpm.ogg" volume 0.5 fadein 0.5

    "Select the language you want to use in the game."
    #model = "gpt2" #gpt3, gpt2
    #version = "openai" #openai, maria-large, maria-base

    define police_EN = Character("Police Chief")
    define you_EN = Character("You")
    define telephone_EN = Character("Telephone")
    define think_EN = Character("Your thoughts")

    define police_ES = Character("Jefe de policías")
    define you_ES = Character("Tú")
    define telephone_ES = Character("Teléfono")
    define think_ES = Character("Tus pensamientos")

    define firstSuspect = Character("Anna")
    define secondSuspect = Character("Daniel")
    define thirdSuspect = Character("Emma")

    transform centerleft:
        xalign 0.25
        yalign 1.0
    transform centerright:        
        xalign 0.75
        yalign 1.0

    menu:
        "English (recommend)":            
            "Which Artificial Intelligence do you want to play with?"    
            menu:
                "GPT-3 (recommend)":
                    $model = "gpt3"   
                    $version = "english"                 
                "GPT-2":                    
                    $model = "gpt2"   
                    $version = "openai"                 
        "Spanish":            
            "¿Con qué Inteligencia Artificial quieres jugar?"
            menu:
                "GPT-3 (recomendado)":
                    $model = "gpt3"
                    $version = "spanish"
                "MarIA Large":
                    $model = "gpt2"
                    $version = "maria-large"
                "MarIA Base":
                    $model = "gpt2"
                    $version = "maria-base"                    

    if version == "maria-large" or version == "maria-base" or version == "spanish":
        show text "Cargando... 0%"
    else:
        show text "Loading... 0%"
    pause 0.01

    python:        
        conversation = ''
        numsToKill =  [1, 2, 3]
        killerRand = random.choice(numsToKill)

        if version == "maria-large" or version == "maria-base" or version == "spanish":
            question1 = "¿Conocías al vecino asesinado?"
            question2 = "¿Alguna vez has visto al vecino por la calle?"
            question3 = "¿Alguna vez has oído hablar del vecino?"
            question4 = "¿Qué estuviste haciendo anoche?"
            question5 = "¿Sueles salir por la noche?"
            question6 = "¿No tienes miedo de salir a esas horas?"
            question7 = "¿Por qué pasaste por el vecindario?"
            question8 = "¿Conocías a alguna persona del vecindario?"
            question9 = "¿El vecindario es un lugar de tránsito frecuente para ti?"
            question10 = "¿Tienes antecedentes penales?"
            question11 = "¿Alguna vez han detenido a algún conocido tuyo?"
            question12 = "¿Sabes cúal es la condena por asesinar a alguien?"
        else:
            question1 = "Did you know the murdered neighbor?"
            question2 = "Have you ever seen the neighbor on the street?"
            question3 = "Have you ever heard of the neighbor?"
            question4 = "What were you doing last night?"
            question5 = "Do you usually go out at night?"
            question6 = "Aren't you afraid to go out at that time?"
            question7 = "Why did you go through the neighborhood?"
            question8 = "Did you know anyone in the neighborhood?"
            question9 = "Is the neighborhood a frequent traffic place for you?"
            question10 = "Do you have a criminal record?"
            question11 = "Has anyone you know ever been arrested?"
            question12 = "Do you know what the sentence is for murdering someone?"

        # PREGUNTA 1
        sentence1 = responseIAprepareSentence(question1) 
        conversation1 = responseIAprepareConversation(sentence1, conversation, model, version)
        message1 = reponseIAgetMessage(conversation1, model, version)
        conversation1 = responseSumConversation(message1, conversation1, model)
        percentage = 100 * 1 / 12

    hide text 
    if version == "maria-large" or version == "maria-base" or version == "spanish":
        show text "Cargando... " + str(percentage) + "%"
    else:
        show text "Loading... " + str(percentage) + "%"
    pause 0.01

    # PREGUNTA 2
    python:
        sentence2 = responseIAprepareSentence(question2)
        conversation2 = responseIAprepareConversation(sentence2, conversation1, model, version)
        message2 = reponseIAgetMessage(conversation2, model, version)
        conversation2 = responseSumConversation(message2, conversation2, model)
        percentage = 100 * 2 / 12

    hide text 
    if version == "maria-large" or version == "maria-base" or version == "spanish":
        show text "Cargando... " + str(percentage) + "%"
    else:
        show text "Loading... " + str(percentage) + "%"
    pause 0.01

    # PREGUNTA 3
    python:        
        sentence3 = responseIAprepareSentence(question3)
        conversation3 = responseIAprepareConversation(sentence3, conversation2, model, version)
        message3 = reponseIAgetMessage(conversation3, model, version)
        conversation3 = responseSumConversation(message3, conversation3, model)
        percentage = 100 * 3 / 12

    hide text 
    if version == "maria-large" or version == "maria-base" or version == "spanish":
        show text "Cargando... " + str(percentage) + "%"
    else:
        show text "Loading... " + str(percentage) + "%"
    pause 0.01

    # PREGUNTA 4    
    python:        
        sentence4 = responseIAprepareSentence(question4)
        conversation4 = responseIAprepareConversation(sentence4, conversation3, model, version)
        message4 = reponseIAgetMessage(conversation4, model, version)
        conversation4 = responseSumConversation(message4, conversation4, model)
        percentage = 100 * 4 / 12

    hide text 
    if version == "maria-large" or version == "maria-base" or version == "spanish":
        show text "Cargando... " + str(percentage) + "%"
    else:
        show text "Loading... " + str(percentage) + "%"
    pause 0.01
    
    # PREGUNTA 5
    python:        
        sentence5 = responseIAprepareSentence(question5)
        conversation5 = responseIAprepareConversation(sentence5, conversation4, model, version)
        message5 = reponseIAgetMessage(conversation5, model, version)
        conversation5 = responseSumConversation(message5, conversation5, model)
        percentage = 100 * 5 / 12

    hide text 
    if version == "maria-large" or version == "maria-base" or version == "spanish":
        show text "Cargando... " + str(percentage) + "%"
    else:
        show text "Loading... " + str(percentage) + "%"
    pause 0.01

    # PREGUNTA 6
    python:        
        sentence6 = responseIAprepareSentence(question6)
        conversation6 = responseIAprepareConversation(sentence6, conversation5, model, version)
        message6 = reponseIAgetMessage(conversation6, model, version)
        conversation6 = responseSumConversation(message6, conversation6, model)
        percentage = 100 * 6 / 12

    hide text 
    if version == "maria-large" or version == "maria-base" or version == "spanish":
        show text "Cargando... " + str(percentage) + "%"
    else:
        show text "Loading... " + str(percentage) + "%"
    pause 0.01

    # PREGUNTA 7
    python:        
        sentence7 = responseIAprepareSentence(question7)
        conversation7 = responseIAprepareConversation(sentence7, conversation6, model, version)
        message7 = reponseIAgetMessage(conversation7, model, version)
        conversation7 = responseSumConversation(message7, conversation7, model)
        percentage = 100 * 7 / 12

    hide text 
    if version == "maria-large" or version == "maria-base" or version == "spanish":
        show text "Cargando... " + str(percentage) + "%"
    else:
        show text "Loading... " + str(percentage) + "%"
    pause 0.01

    # PREGUNTA 8
    python:        
        sentence8 = responseIAprepareSentence(question8)
        conversation8 = responseIAprepareConversation(sentence8, conversation7, model, version)
        message8 = reponseIAgetMessage(conversation8, model, version)
        conversation8 = responseSumConversation(message8, conversation8, model)
        percentage = 100 * 8 / 12

    hide text 
    if version == "maria-large" or version == "maria-base" or version == "spanish":
        show text "Cargando... " + str(percentage) + "%"
    else:
        show text "Loading... " + str(percentage) + "%"
    pause 0.01

    # PREGUNTA 9
    python:        
        sentence9 = responseIAprepareSentence(question9)
        conversation9 = responseIAprepareConversation(sentence9, conversation8, model, version)
        message9 = reponseIAgetMessage(conversation9, model, version)
        conversation9 = responseSumConversation(message9, conversation9, model)
        percentage = 100 * 9 / 12

    hide text 
    if version == "maria-large" or version == "maria-base" or version == "spanish":
        show text "Cargando... " + str(percentage) + "%"
    else:
        show text "Loading... " + str(percentage) + "%"
    pause 0.01

    # PREGUNTA 10
    python:        
        sentence10 = responseIAprepareSentence(question10)
        conversation10 = responseIAprepareConversation(sentence10, conversation9, model, version)
        message10 = reponseIAgetMessage(conversation10, model, version)
        conversation10 = responseSumConversation(message10, conversation10, model)
        percentage = 100 * 10 / 12

    hide text 
    if version == "maria-large" or version == "maria-base" or version == "spanish":
        show text "Cargando... " + str(percentage) + "%"
    else:
        show text "Loading... " + str(percentage) + "%"
    pause 0.01

    # PREGUNTA 11
    python:        
        sentence11 = responseIAprepareSentence(question11)
        conversation11 = responseIAprepareConversation(sentence11, conversation10, model, version)
        message11 = reponseIAgetMessage(conversation11, model, version)
        conversation11 = responseSumConversation(message11, conversation11, model)
        percentage = 100 * 11 / 12

    hide text 
    if version == "maria-large" or version == "maria-base" or version == "spanish":
        show text "Cargando... " + str(percentage) + "%"
    else:
        show text "Loading... " + str(percentage) + "%"
    pause 0.01

    # PREGUNTA 12
    python:        
        sentence12 = responseIAprepareSentence(question12)
        conversation12 = responseIAprepareConversation(sentence12, conversation11, model, version)
        message12 = reponseIAgetMessage(conversation12, model, version)
        conversation12 = responseSumConversation(message12, conversation12, model)
        percentage = 100 * 12 / 12

    hide text 
    if version == "maria-large" or version == "maria-base" or version == "spanish":
        show text "Cargando... " + str(percentage) + "%"
    else:
        show text "Loading... " + str(percentage) + "%"
    pause 0.01

    $response1 = message1
    $response2 = message2
    $response3 = message3
    $response4 = message4
    $response5 = message5
    $response6 = message6
    $response7 = message7
    $response8 = message8
    $response9 = message9
    $response10 = message10
    $response11 = message11
    $response12 = message12
    $killer = killerRand

    #RESPUESTA HUMANA 1
    python:

        #TEMA 1 
        choices_T1 =  ["1", "2", "3", "4", "5"]
        numRespuestaHumana1_T1 = random.choice(choices_T1)
        choices_T1.remove(numRespuestaHumana1_T1)
        numRespuestaHumana2_T1 = random.choice(choices_T1)
        choices_T1.remove(numRespuestaHumana2_T1)
        numRespuestaHumana3_T1 = random.choice(choices_T1)

        #TEMA 2 
        choices_T2 =  ["1", "2", "3", "4", "5"]
        numRespuestaHumana1_T2 = random.choice(choices_T2)
        choices_T2.remove(numRespuestaHumana1_T2)
        numRespuestaHumana2_T2 = random.choice(choices_T2)
        choices_T2.remove(numRespuestaHumana2_T2)
        numRespuestaHumana3_T2 = random.choice(choices_T2)

        #TEMA 3 
        choices_T3 =  ["1", "2", "3", "4", "5"]
        numRespuestaHumana1_T3 = random.choice(choices_T3)
        choices_T3.remove(numRespuestaHumana1_T3)
        numRespuestaHumana2_T3 = random.choice(choices_T3)
        choices_T3.remove(numRespuestaHumana2_T3)
        numRespuestaHumana3_T3 = random.choice(choices_T3)

        #TEMA 4 
        choices_T4 =  ["1", "2", "3", "4", "5"]
        numRespuestaHumana1_T4 = random.choice(choices_T4)
        choices_T4.remove(numRespuestaHumana1_T4)
        numRespuestaHumana2_T4 = random.choice(choices_T4)
        choices_T4.remove(numRespuestaHumana2_T4)
        numRespuestaHumana3_T4 = random.choice(choices_T4)

        if version == "maria-large" or version == "maria-base" or version == "spanish":
            #¿Conocías al vecino asesinado?
            pregunta1respuesta1_P = "Es un vecino de mis abuelos, le conocía de vista."
            pregunta1respuesta2_P = "Me suena su nombre pero nada más."
            pregunta1respuesta3_P = "Personalmente no lo conocía."     
            pregunta1respuesta4_P = "No lo conocía de nada." 
            pregunta1respuesta5_P = "Sí, era un buen amigo." 
            #¿Alguna vez has visto al vecino por la calle?"
            pregunta2respuesta1_P = "Lo veo frecuentemente en el supermercado."            
            pregunta2respuesta2_P = "Sólo lo he visto en la puerta de su casa."
            pregunta2respuesta3_P = "Diría que una vez lo vi paseando a su perro."    
            pregunta2respuesta4_P = "Juraría no haberle visto nunca."         
            pregunta2respuesta5_P = "Sí, suele salir todos los días."      
            #¿Alguna vez has oído hablar del vecino?
            pregunta3respuesta1_P = "Sí, creo que fue con mi padre al instituto."
            pregunta3respuesta2_P = "No me suena haber hablado de él."            
            pregunta3respuesta3_P = "Decían que era alcohólico."
            pregunta3respuesta4_P = "Nadie me ha hablado de él nunca."
            pregunta3respuesta5_P = "Claro, él es una persona muy popular."
            #¿Qué estuviste haciendo anoche?
            pregunta4respuesta1_P = "Estuve cenando en casa de mi abuela."
            pregunta4respuesta2_P = "Ayer estuve estudiando matemáticas."
            pregunta4respuesta3_P = "Me fui a pasar la tarde a casa de un amigo."       
            pregunta4respuesta4_P = "Anoche salí de fiesta."    
            pregunta4respuesta5_P = "Salí a dar una vuelta."         
            #¿Sueles salir por la noche?
            pregunta5respuesta1_P = "No tengo la costumbre."            
            pregunta5respuesta2_P = "Alguna vez salgo con mis amigos."
            pregunta5respuesta3_P = "Depende de si tengo planes o no."       
            pregunta5respuesta4_P = "Sí, suelo salir los sábados."    
            pregunta5respuesta5_P = "Prácticamente salgo todos los días."    
            #¿No tienes miedo de salir a esas horas?
            pregunta6respuesta1_P = "Sí, tengo miedo a la oscuridad."
            pregunta6respuesta2_P = "No, casi siempre voy acompañado."
            pregunta6respuesta3_P = "No tengo miedo a ninguna hora."
            pregunta6respuesta4_P = "No, cuando salgo me lo paso bien."
            pregunta6respuesta5_P = "Bastante, uno nunca sabe lo que le puede ocurrir."
            #¿Por qué pasaste por el vecindario?
            pregunta7respuesta1_P = "Estaba yendo a casa a dormir."
            pregunta7respuesta2_P = "Salí a tirar la basura."
            pregunta7respuesta3_P = "El vecindario me pillaba camino a casa."  
            pregunta7respuesta4_P = "Pasé por allí porque estaba acompañando a un amigo."  
            pregunta7respuesta5_P = "Tenía que hacer un recado."  
            #¿Conocías a alguna persona del vecindario?
            pregunta8respuesta1_P = "Claro, allí viven amigos míos."            
            pregunta8respuesta2_P = "Sólo a mi profesora."
            pregunta8respuesta3_P = "No he hablado con nadie de allí." 
            pregunta8respuesta4_P = "Conocía a un par de amigos y a sus familiares."     
            pregunta8respuesta5_P = "Sí, mi exnovia vivía allí."          
            #¿El vecindario es un lugar de tránsito frecuente para ti?
            pregunta9respuesta1_P = "Suelo pasar por allí."
            pregunta9respuesta2_P = "No, frecuente no."
            pregunta9respuesta3_P = "Alguna vez tengo que cruzarlo pero no todos los días."
            pregunta9respuesta4_P = "Puede que pase por allí una vez a la semana."
            pregunta9respuesta5_P = "Hace años me pasaba más por allí que ahora."
            #¿Tienes antecedentes penales?
            pregunta10respuesta1_P = "No, nunca he hecho nada malo."
            pregunta10respuesta2_P = "Una vez me pillaron con el coche a más velocidad de la permitida."
            pregunta10respuesta3_P = "No tengo nada, puede comprobarlo."  
            pregunta10respuesta4_P = "No he cometido nunca un delito."  
            pregunta10respuesta5_P = "Cuando era un chaval me pillaron robando en una tienda." 
            #¿Alguna vez han detenido a algún conocido tuyo?
            pregunta11respuesta1_P = "Me suena que detuvieron al padre de un amigo hace años."
            pregunta11respuesta2_P = "No, no conozco a nadie que haya sido detenido."
            pregunta11respuesta3_P = "Creo que no pero no estoy seguro."        
            pregunta11respuesta4_P = "Una vez pillaron a un amigo robando en una tienda."    
            pregunta11respuesta5_P = "Mi pareja estuvo en el calabozo seis meses."    
            #¿Sabes cúal es la condena por asesinar a alguien?
            pregunta12respuesta1_P = "Entiendo que son muchos años preso."
            pregunta12respuesta2_P = "Sí, conozco la ley."            
            pregunta12respuesta3_P = "Deberá ser mucho tiempo en la cárcel."
            pregunta12respuesta4_P = "Supongo que serán mínimo un par de años."
            pregunta12respuesta5_P = "Estoy seguro de que es más de lo que imagino."
        else:
            #Did you know the murdered neighbor?
            pregunta1respuesta1_P = "He is a neighbor of my grandparents, I knew him by sight."
            pregunta1respuesta2_P = "Your name sounds familiar to me but nothing else."
            pregunta1respuesta3_P = "Personally I didn't know him."
            pregunta1respuesta4_P = "I didn't know him at all."
            pregunta1respuesta5_P = "Yes, he was a good friend."
            #Have you ever seen the neighbor down the street?"
            pregunta2respuesta1_P = "I see it frequently in the supermarket."
            pregunta2respuesta2_P = "I have only seen him at the door of his house."
            pregunta2respuesta3_P = "I would say that I once saw him walking his dog."
            pregunta2respuesta4_P = "I could swear I never saw him."
            pregunta2respuesta5_P = "Yes, he usually goes out every day."
            #Have you ever heard of the neighbor?
            pregunta3respuesta1_P = "Yes, I think he went to high school with my father."
            pregunta3respuesta2_P = "I don't think I've talked about him."
            pregunta3respuesta3_P = "They said he was an alcoholic."
            pregunta3respuesta4_P = "No one has ever told me about him."
            pregunta3respuesta5_P = "Of course, he is a very popular person."
            #What were you doing last night?
            pregunta4respuesta1_P = "I was having dinner at my grandmother's house."
            pregunta4respuesta2_P = "Yesterday I was studying mathematics."
            pregunta4respuesta3_P = "I went to spend the afternoon at a friend's house."
            pregunta4respuesta4_P = "Last night I went out partying."
            pregunta4respuesta5_P = "I went out for a walk."
            #Do you usually go out at night?
            pregunta5respuesta1_P = "I'm not used to it."
            pregunta5respuesta2_P = "Sometimes I go out with my friends."
            pregunta5respuesta3_P = "Depends on whether I have plans or not."
            pregunta5respuesta4_P = "Yes, I usually go out on Saturdays."
            pregunta5respuesta5_P = "I practically go out every day."
            #Aren't you afraid to go out at that time?
            pregunta6respuesta1_P = "Yes, I'm afraid of the dark."
            pregunta6respuesta2_P = "No, I'm almost always accompanied."
            pregunta6respuesta3_P = "I'm not afraid at any time."
            pregunta6respuesta4_P = "No, when I go out I have a good time."
            pregunta6respuesta5_P = "Quite a lot, you never know what can happen to you."
            #Why did you go through the neighborhood?
            pregunta7respuesta1_P = "I was going home to sleep."
            pregunta7respuesta2_P = "I went out to throw the garbage."
            pregunta7respuesta3_P = "The neighborhood caught me on the way home."
            pregunta7respuesta4_P = "I passed by because I was accompanying a friend."
            pregunta7respuesta5_P = "I had to run an errand."
            #Did you know anyone in the neighborhood?
            pregunta8respuesta1_P = "Of course, my friends live there."
            pregunta8respuesta2_P = "Only my teacher."
            pregunta8respuesta3_P = "I haven't talked to anyone there."
            pregunta8respuesta4_P = "I knew a couple of friends and their relatives."
            pregunta8respuesta5_P = "Yes, my ex-girlfriend lived there."
            #Is the neighborhood a frequent traffic place for you?
            pregunta9respuesta1_P = "I usually pass by there."
            pregunta9respuesta2_P = "No, not often."
            pregunta9respuesta3_P = "Sometimes I have to cross it but not every day."
            pregunta9respuesta4_P = "I might come by once a week."
            pregunta9respuesta5_P = "Years ago I spent more time there than now."
            #Do you have a criminal record?
            pregunta10respuesta1_P = "No, I have never done anything wrong."
            pregunta10respuesta2_P = "Once I was caught with the car going faster than allowed."
            pregunta10respuesta3_P = "I don't have anything, you can check it."
            pregunta10respuesta4_P = "I have never committed a crime."
            pregunta10respuesta5_P = "When I was a kid I was caught shoplifting."
            #Has anyone you know ever been arrested?
            pregunta11respuesta1_P = "It sounds to me like a friend's father was arrested years ago."
            pregunta11respuesta2_P = "No, I don't know anyone who has been arrested."
            pregunta11respuesta3_P = "I think not but I'm not sure."
            pregunta11respuesta4_P = "Once a friend was caught shoplifting."
            pregunta11respuesta5_P = "My partner was in jail for six months."
            #Do you know what the sentence is for murdering someone?
            pregunta12respuesta1_P = "I understand that there are many years in prison."
            pregunta12respuesta2_P = "Yes, I know the law."
            pregunta12respuesta3_P = "It must be a long time in jail."
            pregunta12respuesta4_P = "I guess it will be at least a couple of years."
            pregunta12respuesta5_P = "I'm sure it's more than I imagine."

    $pregunta1respuesta1 = pregunta1respuesta1_P
    $pregunta1respuesta2 = pregunta1respuesta2_P
    $pregunta1respuesta3 = pregunta1respuesta3_P
    $pregunta1respuesta4 = pregunta1respuesta4_P
    $pregunta1respuesta5 = pregunta1respuesta5_P

    $pregunta2respuesta1 = pregunta2respuesta1_P
    $pregunta2respuesta2 = pregunta2respuesta2_P
    $pregunta2respuesta3 = pregunta2respuesta3_P
    $pregunta2respuesta4 = pregunta2respuesta4_P
    $pregunta2respuesta5 = pregunta2respuesta5_P

    $pregunta3respuesta1 = pregunta3respuesta1_P
    $pregunta3respuesta2 = pregunta3respuesta2_P
    $pregunta3respuesta3 = pregunta3respuesta3_P
    $pregunta3respuesta4 = pregunta3respuesta4_P
    $pregunta3respuesta5 = pregunta3respuesta5_P

    $pregunta4respuesta1 = pregunta4respuesta1_P
    $pregunta4respuesta2 = pregunta4respuesta2_P
    $pregunta4respuesta3 = pregunta4respuesta3_P
    $pregunta4respuesta4 = pregunta4respuesta4_P
    $pregunta4respuesta5 = pregunta4respuesta5_P

    $pregunta5respuesta1 = pregunta5respuesta1_P
    $pregunta5respuesta2 = pregunta5respuesta2_P
    $pregunta5respuesta3 = pregunta5respuesta3_P
    $pregunta5respuesta4 = pregunta5respuesta4_P
    $pregunta5respuesta5 = pregunta5respuesta5_P

    $pregunta6respuesta1 = pregunta6respuesta1_P
    $pregunta6respuesta2 = pregunta6respuesta2_P
    $pregunta6respuesta3 = pregunta6respuesta3_P
    $pregunta6respuesta4 = pregunta6respuesta4_P
    $pregunta6respuesta5 = pregunta6respuesta5_P

    $pregunta7respuesta1 = pregunta7respuesta1_P
    $pregunta7respuesta2 = pregunta7respuesta2_P
    $pregunta7respuesta3 = pregunta7respuesta3_P
    $pregunta7respuesta4 = pregunta7respuesta4_P
    $pregunta7respuesta5 = pregunta7respuesta5_P

    $pregunta8respuesta1 = pregunta8respuesta1_P
    $pregunta8respuesta2 = pregunta8respuesta2_P
    $pregunta8respuesta3 = pregunta8respuesta3_P
    $pregunta8respuesta4 = pregunta8respuesta4_P
    $pregunta8respuesta5 = pregunta8respuesta5_P

    $pregunta9respuesta1 = pregunta9respuesta1_P
    $pregunta9respuesta2 = pregunta9respuesta2_P
    $pregunta9respuesta3 = pregunta9respuesta3_P
    $pregunta9respuesta4 = pregunta9respuesta4_P
    $pregunta9respuesta5 = pregunta9respuesta5_P

    $pregunta10respuesta1 = pregunta10respuesta1_P
    $pregunta10respuesta2 = pregunta10respuesta2_P
    $pregunta10respuesta3 = pregunta10respuesta3_P
    $pregunta10respuesta4 = pregunta10respuesta4_P
    $pregunta10respuesta5 = pregunta10respuesta5_P

    $pregunta11respuesta1 = pregunta11respuesta1_P
    $pregunta11respuesta2 = pregunta11respuesta2_P
    $pregunta11respuesta3 = pregunta11respuesta3_P
    $pregunta11respuesta4 = pregunta11respuesta4_P
    $pregunta11respuesta5 = pregunta11respuesta5_P

    $pregunta12respuesta1 = pregunta12respuesta1_P
    $pregunta12respuesta2 = pregunta12respuesta2_P
    $pregunta12respuesta3 = pregunta12respuesta3_P
    $pregunta12respuesta4 = pregunta12respuesta4_P
    $pregunta12respuesta5 = pregunta12respuesta5_P

    $numRespuestaHumana1__T1 = numRespuestaHumana1_T1
    $numRespuestaHumana2__T1 = numRespuestaHumana2_T1
    $numRespuestaHumana3__T1 = numRespuestaHumana3_T1
    $numRespuestaHumana1__T2 = numRespuestaHumana1_T2
    $numRespuestaHumana2__T2 = numRespuestaHumana2_T2
    $numRespuestaHumana3__T2 = numRespuestaHumana3_T2
    $numRespuestaHumana1__T3 = numRespuestaHumana1_T3
    $numRespuestaHumana2__T3 = numRespuestaHumana2_T3
    $numRespuestaHumana3__T3 = numRespuestaHumana3_T3
    $numRespuestaHumana1__T4 = numRespuestaHumana1_T4
    $numRespuestaHumana2__T4 = numRespuestaHumana2_T4
    $numRespuestaHumana3__T4 = numRespuestaHumana3_T4    

    stop music fadeout 1
    play sound "audio/457869__inchadney__british-telephone.ogg" volume 1 fadein 0.5   
    hide text 
        
    label begin:

        #Introduction 
        if version == "maria-large" or version == "maria-base" or version == "spanish":
            telephone_ES "Riiiiiing riiiiiiiing riiiiiing"
            stop sound fadeout 1
            scene bg room with dissolve

            show sprite3 sad small with dissolve
            police_ES "Buenos días, Sr. Detective. Necesitamos su ayuda inmediatamente. Ha habido un asesinato en el vecindario."
            hide sprite3 sad small with dissolve
            you_ES "¿Cómo? ¿Un asesinato?"
            show sprite3 sad small with dissolve
            police_ES "Sí, un asesinato. Estás escuchando bien. Ayer un androide asesinó a su dueño y huyó de casa. Menos mal que teníamos cámaras de seguridad y hemos podido encontrar a algunos sospechosos."
            hide sprite3 sad small with dissolve
            think_ES "Afortunadamente me escucharon con el tema de las cámaras, esto es algo que sabía que algún día podría ocurrir..."
            show sprite3 sad small with dissolve
            police_ES "Vamos rápidamente a la oficina, tenemos allí a los detenidos y hay que interrogarlos."
            hide sprite3 sad small with dissolve
            you_ES "En seguida estoy allí, voy directo con el tranvía."

            scene bg train with dissolve
            play sound "audio/346573__inspectorj__train-door-beep-a.ogg" volume 1 fadein 0.5
            pause 2.0
            stop sound fadeout 1

            scene bg interrogation with dissolve
            show sprite3 sad small with dissolve
            police_ES "Has llegado a tiempo. Tenemos a tres sospechosos que interrogar."
            hide sprite3 sad small with dissolve
            show sprite1 sad small at centerleft with dissolve
            show sprite4 sad small at center with dissolve  
            show sprite2 sad small at centerright with dissolve                      
            police_ES "Estos tres estaban por la zona a la hora del asesinato. No les juzgues por su apariencia, el androide puede ser cualquiera. Nosotros únicamente conocemos sus nombres: Anna, Daniel y Emma."
            hide sprite1 sad small at centerleft with dissolve
            hide sprite4 sad small at center with dissolve  
            hide sprite2 sad small at centerright with dissolve  
            you_ES "Por favor, que pase el primer sospechoso."
            think_ES "¿Qué debería preguntar?"

        else:
            telephone_EN "Riiiiiing riiiiiiiing riiiiiing"
            stop sound fadeout 1
            scene bg room with dissolve

            show sprite3 sad small with dissolve
            police_EN "Good morning, Mr. Detective. We need your help immediately. There has been a murder in the neighborhood."
            hide sprite3 sad small with dissolve
            you_EN "How? A murder?"
            show sprite3 sad small with dissolve
            police_EN "Yes, a murder. You are listening well. Yesterday an android murdered its owner and fled. Good thing we had security cameras and we spotted several suspects."
            hide sprite3 sad small with dissolve
            think_EN "Luckily they listened to me with the cameras, I knew that one day something would happen..."
            show sprite3 sad small with dissolve
            police_EN "Let's go quickly to the office, we have the detainees there and you have to question them."
            hide sprite3 sad small with dissolve
            you_EN "I'm there right away, I'm going straight with the tram."

            scene bg train with dissolve
            play sound "audio/346573__inspectorj__train-door-beep-a.ogg" volume 1 fadein 0.5
            pause 2.0
            stop sound fadeout 1

            scene bg interrogation with dissolve
            show sprite3 sad small with dissolve
            police_EN "You have arrived on time. We have three suspects to question."
            hide sprite3 sad small with dissolve
            show sprite1 sad small at centerleft with dissolve
            show sprite4 sad small at center with dissolve  
            show sprite2 sad small at centerright with dissolve     
            police_EN "These three were in the area at the time of the murder. Don't judge them by their appearance, the android can be anyone. We only know their names: Anna, Daniel and Emma."
            hide sprite1 sad small at centerleft with dissolve
            hide sprite4 sad small at center with dissolve  
            hide sprite2 sad small at centerright with dissolve   
            you_EN "Please, let the first suspect come through."
            think_EN "What should I ask now?"

        show sprite1 angry small with dissolve               

        #Interrogation
        label interrogation:     

            if version == "maria-large" or version == "maria-base" or version == "spanish":
                #PRIMER INTERROGADO CASTELLANO
                menu:
                    "Preguntar acerca del vecino":
                        label tema1sospechoso1castellano:
                            menu:
                                "¿Conocías al vecino asesinado?":
                                    if killer != 1:
                                        if numRespuestaHumana1__T1 == "1":                                                                                
                                            firstSuspect "[pregunta1respuesta1]" 
                                        elif numRespuestaHumana1__T1 == "2": 
                                            firstSuspect "[pregunta1respuesta2]" 
                                        elif numRespuestaHumana1__T1 == "3": 
                                            firstSuspect "[pregunta1respuesta3]" 
                                        elif numRespuestaHumana1__T1 == "4": 
                                            firstSuspect "[pregunta1respuesta4]" 
                                        elif numRespuestaHumana1__T1 == "5": 
                                            firstSuspect "[pregunta1respuesta5]" 
                                    else:
                                        firstSuspect "[response1]" 
                                    $num_pregs1 = num_pregs1 + 1   
                                    jump tema1sospechoso1castellano
                                "¿Alguna vez has visto al vecino por la calle?":
                                    if killer != 1:
                                        if numRespuestaHumana1__T1 == "1":                                       
                                            firstSuspect "[pregunta2respuesta1]" 
                                        elif numRespuestaHumana1__T1 == "2": 
                                            firstSuspect "[pregunta2respuesta2]" 
                                        elif numRespuestaHumana1__T1 == "3": 
                                            firstSuspect "[pregunta2respuesta3]" 
                                        elif numRespuestaHumana1__T1 == "4": 
                                            firstSuspect "[pregunta2respuesta4]" 
                                        elif numRespuestaHumana1__T1 == "5": 
                                            firstSuspect "[pregunta2respuesta5]" 
                                    else:
                                        firstSuspect "[response2]"
                                    $num_pregs1 = num_pregs1 + 1   
                                    jump tema1sospechoso1castellano
                                "¿Alguna vez has oído hablar del vecino?":
                                    if killer != 1:
                                        if numRespuestaHumana1__T1 == "1":                                       
                                            firstSuspect "[pregunta3respuesta1]" 
                                        elif numRespuestaHumana1__T1 == "2": 
                                            firstSuspect "[pregunta3respuesta2]" 
                                        elif numRespuestaHumana1__T1 == "3": 
                                            firstSuspect "[pregunta3respuesta3]" 
                                        elif numRespuestaHumana1__T1 == "4": 
                                            firstSuspect "[pregunta3respuesta4]" 
                                        elif numRespuestaHumana1__T1 == "5": 
                                            firstSuspect "[pregunta3respuesta5]" 
                                    else:
                                        firstSuspect "[response3]"
                                    $num_pregs1 = num_pregs1 + 1   
                                    jump tema1sospechoso1castellano
                                "Volver atrás":
                                    jump interrogation
                    "Preguntar acerca de la noche":
                        label tema2sospechoso1castellano:
                            menu:
                                "¿Qué estuviste haciendo anoche?":
                                    if killer != 1:
                                        if numRespuestaHumana1__T2 == "1":                                       
                                            firstSuspect "[pregunta4respuesta1]" 
                                        elif numRespuestaHumana1__T2 == "2": 
                                            firstSuspect "[pregunta4respuesta2]" 
                                        elif numRespuestaHumana1__T2 == "3": 
                                            firstSuspect "[pregunta4respuesta3]" 
                                        elif numRespuestaHumana1__T2 == "4": 
                                            firstSuspect "[pregunta4respuesta4]" 
                                        elif numRespuestaHumana1__T2 == "5": 
                                            firstSuspect "[pregunta4respuesta5]" 
                                    else:
                                        firstSuspect "[response4]" 
                                    $num_pregs1 = num_pregs1 + 1   
                                    jump tema2sospechoso1castellano
                                "¿Sueles salir por la noche?":
                                    if killer != 1:
                                        if numRespuestaHumana1__T2 == "1":                                       
                                            firstSuspect "[pregunta5respuesta1]" 
                                        elif numRespuestaHumana1__T2 == "2":   
                                            firstSuspect "[pregunta5respuesta2]" 
                                        elif numRespuestaHumana1__T2 == "3": 
                                            firstSuspect "[pregunta5respuesta3]" 
                                        elif numRespuestaHumana1__T2 == "4": 
                                            firstSuspect "[pregunta5respuesta4]" 
                                        elif numRespuestaHumana1__T2 == "5": 
                                            firstSuspect "[pregunta5respuesta5]" 
                                    else:
                                        firstSuspect "[response5]"
                                    $num_pregs1 = num_pregs1 + 1   
                                    jump tema2sospechoso1castellano
                                "¿No tienes miedo de salir a esas horas?":
                                    if killer != 1:
                                        if numRespuestaHumana1__T2 == "1":                                       
                                            firstSuspect "[pregunta6respuesta1]" 
                                        elif numRespuestaHumana1__T2 == "2": 
                                            firstSuspect "[pregunta6respuesta2]" 
                                        elif numRespuestaHumana1__T2 == "3": 
                                            firstSuspect "[pregunta6respuesta3]" 
                                        elif numRespuestaHumana1__T2 == "4": 
                                            firstSuspect "[pregunta6respuesta4]" 
                                        elif numRespuestaHumana1__T2 == "5": 
                                            firstSuspect "[pregunta6respuesta5]" 
                                    else:
                                        firstSuspect "[response6]"
                                    $num_pregs1 = num_pregs1 + 1   
                                    jump tema2sospechoso1castellano  
                                "Volver atrás":
                                    jump interrogation
                    "Preguntar acerca del vecindario":
                        label tema3sospechoso1castellano:
                            menu:
                                "¿Por qué pasaste por el vecindario?":
                                    if killer != 1:
                                        if numRespuestaHumana1__T3 == "1":                                       
                                            firstSuspect "[pregunta7respuesta1]" 
                                        elif numRespuestaHumana1__T3 == "2": 
                                            firstSuspect "[pregunta7respuesta2]" 
                                        elif numRespuestaHumana1__T3 == "3": 
                                            firstSuspect "[pregunta7respuesta3]" 
                                        elif numRespuestaHumana1__T3 == "4": 
                                            firstSuspect "[pregunta7respuesta4]" 
                                        elif numRespuestaHumana1__T3 == "5": 
                                            firstSuspect "[pregunta7respuesta5]" 
                                    else:
                                        firstSuspect "[response7]" 
                                    $num_pregs1 = num_pregs1 + 1   
                                    jump tema3sospechoso1castellano
                                "¿Conocías a alguna persona del vecindario?":
                                    if killer != 1:
                                        if numRespuestaHumana1__T3 == "1":                                       
                                            firstSuspect "[pregunta8respuesta1]" 
                                        elif numRespuestaHumana1__T3 == "2": 
                                            firstSuspect "[pregunta8respuesta2]" 
                                        elif numRespuestaHumana1__T3 == "3": 
                                            firstSuspect "[pregunta8respuesta3]" 
                                        elif numRespuestaHumana1__T3 == "4": 
                                            firstSuspect "[pregunta8respuesta4]" 
                                        elif numRespuestaHumana1__T3 == "5": 
                                            firstSuspect "[pregunta8respuesta5]" 
                                    else:
                                        firstSuspect "[response8]"
                                    $num_pregs1 = num_pregs1 + 1   
                                    jump tema3sospechoso1castellano
                                "¿El vecindario es un lugar de tránsito frecuente para ti?":
                                    if killer != 1:
                                        if numRespuestaHumana1__T3 == "1":                                       
                                            firstSuspect "[pregunta9respuesta1]" 
                                        elif numRespuestaHumana1__T3 == "2": 
                                            firstSuspect "[pregunta9respuesta2]" 
                                        elif numRespuestaHumana1__T3 == "3": 
                                            firstSuspect "[pregunta9respuesta3]"
                                        elif numRespuestaHumana1__T3 == "4": 
                                            firstSuspect "[pregunta9respuesta4]" 
                                        elif numRespuestaHumana1__T3 == "5": 
                                            firstSuspect "[pregunta9respuesta5]"  
                                    else:
                                        firstSuspect "[response9]"
                                    $num_pregs1 = num_pregs1 + 1   
                                    jump tema3sospechoso1castellano  
                                "Volver atrás":
                                    jump interrogation
                    "Preguntar acerca del sospechoso":
                        label tema4sospechoso1castellano:
                            menu:
                                "¿Tienes antecedentes penales?":
                                    if killer != 1:
                                        if numRespuestaHumana1__T4 == "1":                                       
                                            firstSuspect "[pregunta10respuesta1]" 
                                        elif numRespuestaHumana1__T4 == "2": 
                                            firstSuspect "[pregunta10respuesta2]" 
                                        elif numRespuestaHumana1__T4 == "3": 
                                            firstSuspect "[pregunta10respuesta3]" 
                                        elif numRespuestaHumana1__T4 == "4": 
                                            firstSuspect "[pregunta10respuesta4]" 
                                        elif numRespuestaHumana1__T4 == "5": 
                                            firstSuspect "[pregunta10respuesta5]" 
                                    else:
                                        firstSuspect "[response10]" 
                                    $num_pregs1 = num_pregs1 + 1   
                                    jump tema4sospechoso1castellano
                                "¿Alguna vez han detenido a algún conocido tuyo?":
                                    if killer != 1:
                                        if numRespuestaHumana1__T4 == "1":                                       
                                            firstSuspect "[pregunta11respuesta1]" 
                                        elif numRespuestaHumana1__T4 == "2": 
                                            firstSuspect "[pregunta11respuesta2]" 
                                        elif numRespuestaHumana1__T4 == "3": 
                                            firstSuspect "[pregunta11respuesta3]" 
                                        elif numRespuestaHumana1__T4 == "4": 
                                            firstSuspect "[pregunta11respuesta4]" 
                                        elif numRespuestaHumana1__T4 == "5": 
                                            firstSuspect "[pregunta11respuesta5]" 
                                    else:
                                        firstSuspect "[response11]"
                                    $num_pregs1 = num_pregs1 + 1   
                                    jump tema4sospechoso1castellano
                                "¿Sabes cúal es la condena por asesinar a alguien?":
                                    if killer != 1:
                                        if numRespuestaHumana1__T4 == "1":                                       
                                            firstSuspect "[pregunta12respuesta1]" 
                                        elif numRespuestaHumana1__T4 == "2": 
                                            firstSuspect "[pregunta12respuesta2]" 
                                        elif numRespuestaHumana1__T4 == "3": 
                                            firstSuspect "[pregunta12respuesta3]" 
                                        elif numRespuestaHumana1__T4 == "4": 
                                            firstSuspect "[pregunta12respuesta4]" 
                                        elif numRespuestaHumana1__T4 == "5": 
                                            firstSuspect "[pregunta12respuesta5]" 
                                    else:
                                        firstSuspect "[response12]"
                                    $num_pregs1 = num_pregs1 + 1   
                                    jump tema4sospechoso1castellano
                                "Volver atrás":
                                    jump interrogation
                    "Suficientes preguntas. Pasemos al siguiente sospechoso.":
                        you_ES "Por favor, deja pasar al segundo sospechoso."
                        hide sprite1 angry small with dissolve
                        think_ES "¿Qué debería preguntar ahora?"
                        show sprite4 angry small with dissolve 
                        jump next_suspect      
            else:
                #PRIMER INTERROGADO INGLÉS
                menu:
                    "Ask about the neighbor":
                        label tema1sospechoso1ingles:
                            menu:
                                "Did you know the murdered neighbor?":
                                    if killer != 1:
                                        if numRespuestaHumana1__T1 == "1":                                       
                                            firstSuspect "[pregunta1respuesta1]" 
                                        elif numRespuestaHumana1__T1 == "2": 
                                            firstSuspect "[pregunta1respuesta2]" 
                                        elif numRespuestaHumana1__T1 == "3": 
                                            firstSuspect "[pregunta1respuesta3]" 
                                        elif numRespuestaHumana1__T1 == "4": 
                                            firstSuspect "[pregunta1respuesta4]" 
                                        elif numRespuestaHumana1__T1 == "5": 
                                            firstSuspect "[pregunta1respuesta5]" 
                                    else:
                                        firstSuspect "[response1]" 
                                    $num_pregs1 = num_pregs1 + 1   
                                    jump tema1sospechoso1ingles
                                "Have you ever seen the neighbor on the street?":
                                    if killer != 1:
                                        if numRespuestaHumana1__T1 == "1":                                       
                                            firstSuspect "[pregunta2respuesta1]" 
                                        elif numRespuestaHumana1__T1 == "2": 
                                            firstSuspect "[pregunta2respuesta2]" 
                                        elif numRespuestaHumana1__T1 == "3": 
                                            firstSuspect "[pregunta2respuesta3]" 
                                        elif numRespuestaHumana1__T1 == "4": 
                                            firstSuspect "[pregunta2respuesta4]" 
                                        elif numRespuestaHumana1__T1 == "5": 
                                            firstSuspect "[pregunta2respuesta5]" 
                                    else:
                                        firstSuspect "[response2]"
                                    $num_pregs1 = num_pregs1 + 1   
                                    jump tema1sospechoso1ingles
                                "Have you ever heard of the neighbor?":
                                    if killer != 1:
                                        if numRespuestaHumana1__T1 == "1":                                       
                                            firstSuspect "[pregunta3respuesta1]" 
                                        elif numRespuestaHumana1__T1 == "2": 
                                            firstSuspect "[pregunta3respuesta2]" 
                                        elif numRespuestaHumana1__T1 == "3": 
                                            firstSuspect "[pregunta3respuesta3]" 
                                        elif numRespuestaHumana1__T1 == "4": 
                                            firstSuspect "[pregunta3respuesta4]" 
                                        elif numRespuestaHumana1__T1 == "5": 
                                            firstSuspect "[pregunta3respuesta5]" 
                                    else:
                                        firstSuspect "[response3]"
                                    $num_pregs1 = num_pregs1 + 1   
                                    jump tema1sospechoso1ingles
                                "Go back":
                                    jump interrogation  
                    "Ask about tonight":
                        label tema2sospechoso1ingles:
                            menu:
                                "What were you doing last night?":
                                    if killer != 1:
                                        if numRespuestaHumana1__T2 == "1":                                       
                                            firstSuspect "[pregunta4respuesta1]" 
                                        elif numRespuestaHumana1__T2 == "2": 
                                            firstSuspect "[pregunta4respuesta2]" 
                                        elif numRespuestaHumana1__T2 == "3": 
                                            firstSuspect "[pregunta4respuesta3]" 
                                        elif numRespuestaHumana1__T2 == "4": 
                                            firstSuspect "[pregunta4respuesta4]" 
                                        elif numRespuestaHumana1__T2 == "5": 
                                            firstSuspect "[pregunta4respuesta5]" 
                                    else:
                                        firstSuspect "[response4]" 
                                    $num_pregs1 = num_pregs1 + 1   
                                    jump tema2sospechoso1ingles
                                "Do you usually go out at night?":
                                    if killer != 1:
                                        if numRespuestaHumana1__T2 == "1":                                       
                                            firstSuspect "[pregunta5respuesta1]" 
                                        elif numRespuestaHumana1__T2 == "2": 
                                            firstSuspect "[pregunta5respuesta2]" 
                                        elif numRespuestaHumana1__T2 == "3": 
                                            firstSuspect "[pregunta5respuesta3]" 
                                        elif numRespuestaHumana1__T2 == "4": 
                                            firstSuspect "[pregunta5respuesta4]" 
                                        elif numRespuestaHumana1__T2 == "5": 
                                            firstSuspect "[pregunta5respuesta5]" 
                                    else:
                                        firstSuspect "[response5]"
                                    $num_pregs1 = num_pregs1 + 1   
                                    jump tema2sospechoso1ingles
                                "Aren't you afraid to go out at that time?":
                                    if killer != 1:
                                        if numRespuestaHumana1__T2 == "1":                                       
                                            firstSuspect "[pregunta6respuesta1]" 
                                        elif numRespuestaHumana1__T2 == "2": 
                                            firstSuspect "[pregunta6respuesta2]" 
                                        elif numRespuestaHumana1__T2 == "3": 
                                            firstSuspect "[pregunta6respuesta3]" 
                                        elif numRespuestaHumana1__T2 == "4": 
                                            firstSuspect "[pregunta6respuesta4]" 
                                        elif numRespuestaHumana1__T2 == "5": 
                                            firstSuspect "[pregunta6respuesta5]" 
                                    else:
                                        firstSuspect "[response6]"
                                    $num_pregs1 = num_pregs1 + 1   
                                    jump tema2sospechoso1ingles  
                                "Go back":
                                    jump interrogation  
                    "Ask about the neighborhood":
                        label tema3sospechoso1ingles:
                            menu:
                                "Why did you go through the neighborhood?":
                                    if killer != 1:
                                        if numRespuestaHumana1__T3 == "1":                                       
                                            firstSuspect "[pregunta7respuesta1]" 
                                        elif numRespuestaHumana1__T3 == "2": 
                                            firstSuspect "[pregunta7respuesta2]" 
                                        elif numRespuestaHumana1__T3 == "3": 
                                            firstSuspect "[pregunta7respuesta3]" 
                                        elif numRespuestaHumana1__T3 == "4": 
                                            firstSuspect "[pregunta7respuesta4]" 
                                        elif numRespuestaHumana1__T3 == "5": 
                                            firstSuspect "[pregunta7respuesta5]" 
                                    else:
                                        firstSuspect "[response7]" 
                                    $num_pregs1 = num_pregs1 + 1   
                                    jump tema3sospechoso1ingles
                                "Did you know anyone in the neighborhood?":
                                    if killer != 1:
                                        if numRespuestaHumana1__T3 == "1":                                       
                                            firstSuspect "[pregunta8respuesta1]" 
                                        elif numRespuestaHumana1__T3 == "2": 
                                            firstSuspect "[pregunta8respuesta2]" 
                                        elif numRespuestaHumana1__T3 == "3": 
                                            firstSuspect "[pregunta8respuesta3]" 
                                        elif numRespuestaHumana1__T3 == "4": 
                                            firstSuspect "[pregunta8respuesta4]" 
                                        elif numRespuestaHumana1__T3 == "5": 
                                            firstSuspect "[pregunta8respuesta5]" 
                                    else:
                                        firstSuspect "[response8]"
                                    $num_pregs1 = num_pregs1 + 1   
                                    jump tema3sospechoso1ingles
                                "Is the neighborhood a frequent traffic place for you?":
                                    if killer != 1:
                                        if numRespuestaHumana1__T3 == "1":                                       
                                            firstSuspect "[pregunta9respuesta1]" 
                                        elif numRespuestaHumana1__T3 == "2": 
                                            firstSuspect "[pregunta9respuesta2]" 
                                        elif numRespuestaHumana1__T3 == "3": 
                                            firstSuspect "[pregunta9respuesta3]" 
                                        elif numRespuestaHumana1__T3 == "4": 
                                            firstSuspect "[pregunta9respuesta4]" 
                                        elif numRespuestaHumana1__T3 == "5": 
                                            firstSuspect "[pregunta9respuesta5]" 
                                    else:
                                        firstSuspect "[response9]"
                                    $num_pregs1 = num_pregs1 + 1   
                                    jump tema3sospechoso1ingles  
                                "Go back":
                                    jump interrogation  
                    "Ask about the suspect":
                        label tema4sospechoso1ingles:
                            menu:
                                "Do you have a criminal record?":
                                    if killer != 1:
                                        if numRespuestaHumana1__T4 == "1":                                       
                                            firstSuspect "[pregunta10respuesta1]" 
                                        elif numRespuestaHumana1__T4 == "2": 
                                            firstSuspect "[pregunta10respuesta2]" 
                                        elif numRespuestaHumana1__T4 == "3": 
                                            firstSuspect "[pregunta10respuesta3]" 
                                        elif numRespuestaHumana1__T4 == "4": 
                                            firstSuspect "[pregunta10respuesta4]" 
                                        elif numRespuestaHumana1__T4 == "5": 
                                            firstSuspect "[pregunta10respuesta5]" 
                                    else:
                                        firstSuspect "[response10]" 
                                    $num_pregs1 = num_pregs1 + 1   
                                    jump tema4sospechoso1ingles
                                "Has anyone you know ever been arrested?":
                                    if killer != 1:
                                        if numRespuestaHumana1__T4 == "1":                                       
                                            firstSuspect "[pregunta11respuesta1]" 
                                        elif numRespuestaHumana1__T4 == "2": 
                                            firstSuspect "[pregunta11respuesta2]" 
                                        elif numRespuestaHumana1__T4 == "3": 
                                            firstSuspect "[pregunta11respuesta3]" 
                                        elif numRespuestaHumana1__T4 == "4": 
                                            firstSuspect "[pregunta11respuesta4]" 
                                        elif numRespuestaHumana1__T4 == "5": 
                                            firstSuspect "[pregunta11respuesta5]" 
                                    else:
                                        firstSuspect "[response11]"
                                    $num_pregs1 = num_pregs1 + 1   
                                    jump tema4sospechoso1ingles
                                "Do you know what the sentence is for murdering someone?":
                                    if killer != 1:
                                        if numRespuestaHumana1__T4 == "1":                                       
                                            firstSuspect "[pregunta12respuesta1]" 
                                        elif numRespuestaHumana1__T4 == "2": 
                                            firstSuspect "[pregunta12respuesta2]" 
                                        elif numRespuestaHumana1__T4 == "3": 
                                            firstSuspect "[pregunta12respuesta3]" 
                                        elif numRespuestaHumana1__T4 == "4": 
                                            firstSuspect "[pregunta12respuesta4]" 
                                        elif numRespuestaHumana1__T4 == "5": 
                                            firstSuspect "[pregunta12respuesta5]" 
                                    else:
                                        firstSuspect "[response12]"
                                    $num_pregs1 = num_pregs1 + 1   
                                    jump tema4sospechoso1ingles
                                "Go back":
                                    jump interrogation  
                    "Enough questions. We move on to the next suspect.":
                        you_EN "Please, let the second suspect come through."
                        hide sprite1 angry small with dissolve
                        think_EN "What should I ask now?"
                        show sprite4 angry small with dissolve 
                        jump next_suspect               
                                                             
            label next_suspect:            

                if version == "maria-large" or version == "maria-base" or version == "spanish":
                    #SEGUNDO INTERROGADO CASTELLANO
                    menu:
                        "Preguntar acerca del vecino":
                            label tema1sospechoso2castellano:
                                menu:
                                    "¿Conocías al vecino asesinado?":
                                        if killer != 2:
                                            if numRespuestaHumana2__T1 == "1":                                        
                                                secondSuspect "[pregunta1respuesta1]" 
                                            elif numRespuestaHumana2__T1 == "2": 
                                                secondSuspect "[pregunta1respuesta2]" 
                                            elif numRespuestaHumana2__T1 == "3": 
                                                secondSuspect "[pregunta1respuesta3]" 
                                            elif numRespuestaHumana2__T1 == "4": 
                                                secondSuspect "[pregunta1respuesta4]" 
                                            elif numRespuestaHumana2__T1 == "5": 
                                                secondSuspect "[pregunta1respuesta5]"                                                
                                        else:
                                            secondSuspect "[response1]" 
                                            $num_pregs2 = num_pregs2 + 1   
                                        jump tema1sospechoso2castellano
                                    "¿Alguna vez has visto al vecino por la calle?":
                                        if killer != 2:
                                            if numRespuestaHumana2__T1 == "1":                                        
                                                secondSuspect "[pregunta2respuesta1]" 
                                            elif numRespuestaHumana2__T1 == "2": 
                                                secondSuspect "[pregunta2respuesta2]" 
                                            elif numRespuestaHumana2__T1 == "3": 
                                                secondSuspect "[pregunta2respuesta3]" 
                                            elif numRespuestaHumana2__T1 == "4": 
                                                secondSuspect "[pregunta2respuesta4]" 
                                            elif numRespuestaHumana2__T1 == "5": 
                                                secondSuspect "[pregunta2respuesta5]" 
                                        else:
                                            secondSuspect "[response2]"
                                        $num_pregs2 = num_pregs2 + 1   
                                        jump tema1sospechoso2castellano
                                    "¿Alguna vez has oído hablar del vecino?":
                                        if killer != 2:
                                            if numRespuestaHumana2__T1 == "1":                                        
                                                secondSuspect "[pregunta3respuesta1]" 
                                            elif numRespuestaHumana2__T1 == "2": 
                                                secondSuspect "[pregunta3respuesta2]" 
                                            elif numRespuestaHumana2__T1 == "3": 
                                                secondSuspect "[pregunta3respuesta3]" 
                                            elif numRespuestaHumana2__T1 == "4": 
                                                secondSuspect "[pregunta3respuesta4]" 
                                            elif numRespuestaHumana2__T1 == "5": 
                                                secondSuspect "[pregunta3respuesta5]" 
                                        else:
                                            secondSuspect "[response3]"
                                        $num_pregs2 = num_pregs2 + 1   
                                        jump tema1sospechoso2castellano
                                    "Volver atrás":
                                        jump next_suspect
                        "Preguntar acerca de la noche":
                            label tema2sospechoso2castellano:
                                menu:
                                    "¿Qué estuviste haciendo anoche?":
                                        if killer != 2:
                                            if numRespuestaHumana2__T2 == "1":                                        
                                                secondSuspect "[pregunta4respuesta1]" 
                                            elif numRespuestaHumana2__T2 == "2": 
                                                secondSuspect "[pregunta4respuesta2]" 
                                            elif numRespuestaHumana2__T2 == "3": 
                                                secondSuspect "[pregunta4respuesta3]" 
                                            elif numRespuestaHumana2__T2 == "4": 
                                                secondSuspect "[pregunta4respuesta4]" 
                                            elif numRespuestaHumana2__T2 == "5": 
                                                secondSuspect "[pregunta4respuesta5]" 
                                        else:
                                            secondSuspect "[response4]" 
                                        $num_pregs2 = num_pregs2 + 1   
                                        jump tema2sospechoso2castellano
                                    "¿Sueles salir por la noche?":
                                        if killer != 2:
                                            if numRespuestaHumana2__T2 == "1":                                        
                                                secondSuspect "[pregunta5respuesta1]" 
                                            elif numRespuestaHumana2__T2 == "2": 
                                                secondSuspect "[pregunta5respuesta2]" 
                                            elif numRespuestaHumana2__T2 == "3": 
                                                secondSuspect "[pregunta5respuesta3]" 
                                            elif numRespuestaHumana2__T2 == "4": 
                                                secondSuspect "[pregunta5respuesta4]" 
                                            elif numRespuestaHumana2__T2 == "5": 
                                                secondSuspect "[pregunta5respuesta5]" 
                                        else:
                                            secondSuspect "[response5]"
                                        $num_pregs2 = num_pregs2 + 1   
                                        jump tema2sospechoso2castellano
                                    "¿No tienes miedo de salir a esas horas?":
                                        if killer != 2:
                                            if numRespuestaHumana2__T2 == "1":                                        
                                                secondSuspect "[pregunta6respuesta1]" 
                                            elif numRespuestaHumana2__T2 == "2": 
                                                secondSuspect "[pregunta6respuesta2]" 
                                            elif numRespuestaHumana2__T2 == "3": 
                                                secondSuspect "[pregunta6respuesta3]"
                                            elif numRespuestaHumana2__T2 == "4": 
                                                secondSuspect "[pregunta6respuesta4]" 
                                            elif numRespuestaHumana2__T2 == "5": 
                                                secondSuspect "[pregunta6respuesta5]"  
                                        else:
                                            secondSuspect "[response6]"
                                        $num_pregs2 = num_pregs2 + 1   
                                        jump tema2sospechoso2castellano  
                                    "Volver atrás":
                                        jump next_suspect
                        "Preguntar acerca del vecindario":
                            label tema3sospechoso2castellano:
                                menu:
                                    "¿Por qué pasaste por el vecindario?":
                                        if killer != 2:
                                            if numRespuestaHumana2__T3 == "1":                                        
                                                secondSuspect "[pregunta7respuesta1]" 
                                            elif numRespuestaHumana2__T3 == "2": 
                                                secondSuspect "[pregunta7respuesta2]" 
                                            elif numRespuestaHumana2__T3 == "3": 
                                                secondSuspect "[pregunta7respuesta3]" 
                                            elif numRespuestaHumana2__T3 == "4": 
                                                secondSuspect "[pregunta7respuesta4]" 
                                            elif numRespuestaHumana2__T3 == "5": 
                                                secondSuspect "[pregunta7respuesta5]" 
                                        else:
                                            secondSuspect "[response7]" 
                                        $num_pregs2 = num_pregs2 + 1   
                                        jump tema3sospechoso2castellano
                                    "¿Conocías a alguna persona del vecindario?":
                                        if killer != 2:
                                            if numRespuestaHumana2__T3 == "1":                                        
                                                secondSuspect "[pregunta8respuesta1]" 
                                            elif numRespuestaHumana2__T3 == "2": 
                                                secondSuspect "[pregunta8respuesta2]" 
                                            elif numRespuestaHumana2__T3 == "3": 
                                                secondSuspect "[pregunta8respuesta3]"
                                            elif numRespuestaHumana2__T3 == "4": 
                                                secondSuspect "[pregunta8respuesta4]" 
                                            elif numRespuestaHumana2__T3 == "5": 
                                                secondSuspect "[pregunta8respuesta5]"  
                                        else:
                                            secondSuspect "[response8]"
                                        $num_pregs2 = num_pregs2 + 1   
                                        jump tema3sospechoso2castellano
                                    "¿El vecindario es un lugar de tránsito frecuente para ti?":
                                        if killer != 2:
                                            if numRespuestaHumana2__T3 == "1":                                        
                                                secondSuspect "[pregunta9respuesta1]" 
                                            elif numRespuestaHumana2__T3 == "2": 
                                                secondSuspect "[pregunta9respuesta2]" 
                                            elif numRespuestaHumana2__T3 == "3": 
                                                secondSuspect "[pregunta9respuesta3]"
                                            elif numRespuestaHumana2__T3 == "4": 
                                                secondSuspect "[pregunta9respuesta4]" 
                                            elif numRespuestaHumana2__T3 == "5": 
                                                secondSuspect "[pregunta9respuesta5]"  
                                        else:
                                            secondSuspect "[response9]"
                                        $num_pregs2 = num_pregs2 + 1   
                                        jump tema3sospechoso2castellano  
                                    "Volver atrás":
                                        jump next_suspect
                        "Preguntar acerca del sospechoso":
                            label tema4sospechoso2castellano:
                                menu:
                                    "¿Tienes antecedentes penales?":
                                        if killer != 2:
                                            if numRespuestaHumana2__T4 == "1":                                        
                                                secondSuspect "[pregunta10respuesta1]" 
                                            elif numRespuestaHumana2__T4 == "2": 
                                                secondSuspect "[pregunta10respuesta2]" 
                                            elif numRespuestaHumana2__T4 == "3": 
                                                secondSuspect "[pregunta10respuesta3]" 
                                            elif numRespuestaHumana2__T4 == "4": 
                                                secondSuspect "[pregunta10respuesta4]" 
                                            elif numRespuestaHumana2__T4 == "5": 
                                                secondSuspect "[pregunta10respuesta5]" 
                                        else:
                                            secondSuspect "[response10]" 
                                        $num_pregs2 = num_pregs2 + 1   
                                        jump tema4sospechoso2castellano
                                    "¿Alguna vez han detenido a algún conocido tuyo?":
                                        if killer != 2:
                                            if numRespuestaHumana2__T4 == "1":                                        
                                                secondSuspect "[pregunta11respuesta1]" 
                                            elif numRespuestaHumana2__T4 == "2": 
                                                secondSuspect "[pregunta11respuesta2]" 
                                            elif numRespuestaHumana2__T4 == "3": 
                                                secondSuspect "[pregunta11respuesta3]" 
                                            elif numRespuestaHumana2__T4 == "4": 
                                                secondSuspect "[pregunta11respuesta4]" 
                                            elif numRespuestaHumana2__T4 == "5": 
                                                secondSuspect "[pregunta11respuesta5]" 
                                        else:
                                            secondSuspect "[response11]"
                                        $num_pregs2 = num_pregs2 + 1   
                                        jump tema4sospechoso2castellano
                                    "¿Sabes cúal es la condena por asesinar a alguien?":
                                        if killer != 2:
                                            if numRespuestaHumana2__T4 == "1":                                        
                                                secondSuspect "[pregunta12respuesta1]" 
                                            elif numRespuestaHumana2__T4 == "2": 
                                                secondSuspect "[pregunta12respuesta2]" 
                                            elif numRespuestaHumana2__T4 == "3": 
                                                secondSuspect "[pregunta12respuesta3]" 
                                            elif numRespuestaHumana2__T4 == "4": 
                                                secondSuspect "[pregunta12respuesta4]" 
                                            elif numRespuestaHumana2__T4 == "5": 
                                                secondSuspect "[pregunta12respuesta5]" 
                                        else:
                                            secondSuspect "[response12]"
                                        $num_pregs2 = num_pregs2 + 1   
                                        jump tema4sospechoso2castellano  
                                    "Volver atrás":
                                        jump next_suspect 
                        "Suficientes preguntas. Pasemos al siguiente sospechoso.":
                            you_ES "Por favor, deja pasar al tercer sospechoso."
                            hide sprite4 angry small with dissolve
                            think_ES "¿Qué debería preguntar ahora?"
                            show sprite2 angry small with dissolve                   
                            jump last_suspect 
                        "Volver al sospechoso anterior.":
                            hide sprite4 angry small with dissolve
                            show sprite1 angry small with dissolve
                            jump interrogation
                else:                
                    #SEGUNDO INTERROGADO INGLÉS
                    menu:
                        "Ask about the neighbor":
                            label tema1sospechoso2ingles:
                                menu:
                                    "Did you know the murdered neighbor?":
                                        if killer != 2:
                                            if numRespuestaHumana2__T1 == "1":                                        
                                                secondSuspect "[pregunta1respuesta1]" 
                                            elif numRespuestaHumana2__T1 == "2": 
                                                secondSuspect "[pregunta1respuesta2]" 
                                            elif numRespuestaHumana2__T1 == "3": 
                                                secondSuspect "[pregunta1respuesta3]" 
                                            elif numRespuestaHumana2__T1 == "4": 
                                                secondSuspect "[pregunta1respuesta4]" 
                                            elif numRespuestaHumana2__T1 == "5": 
                                                secondSuspect "[pregunta1respuesta5]" 
                                        else:
                                            secondSuspect "[response1]" 
                                        $num_pregs2 = num_pregs2 + 1   
                                        jump tema1sospechoso2ingles
                                    "Have you ever seen the neighbor on the street?":
                                        if killer != 2:
                                            if numRespuestaHumana2__T1 == "1":                                        
                                                secondSuspect "[pregunta2respuesta1]" 
                                            elif numRespuestaHumana2__T1 == "2": 
                                                secondSuspect "[pregunta2respuesta2]" 
                                            elif numRespuestaHumana2__T1 == "3": 
                                                secondSuspect "[pregunta2respuesta3]" 
                                            elif numRespuestaHumana2__T1 == "4": 
                                                secondSuspect "[pregunta2respuesta4]" 
                                            elif numRespuestaHumana2__T1 == "5": 
                                                secondSuspect "[pregunta2respuesta5]" 
                                        else:
                                            secondSuspect "[response2]"
                                        $num_pregs2 = num_pregs2 + 1   
                                        jump tema1sospechoso2ingles
                                    "Have you ever heard of the neighbor?":
                                        if killer != 2:
                                            if numRespuestaHumana2__T1 == "1":                                        
                                                secondSuspect "[pregunta3respuesta1]" 
                                            elif numRespuestaHumana2__T1 == "2": 
                                                secondSuspect "[pregunta3respuesta2]" 
                                            elif numRespuestaHumana2__T1 == "3": 
                                                secondSuspect "[pregunta3respuesta3]" 
                                            elif numRespuestaHumana2__T1 == "4": 
                                                secondSuspect "[pregunta3respuesta4]" 
                                            elif numRespuestaHumana2__T1 == "5": 
                                                secondSuspect "[pregunta3respuesta5]" 
                                        else:
                                            secondSuspect "[response3]"
                                        $num_pregs2 = num_pregs2 + 1   
                                        jump tema1sospechoso2ingles
                                    "Go back":
                                        jump next_suspect  
                        "Ask about tonight":
                            label tema2sospechoso2ingles:
                                menu:
                                    "What were you doing last night?":
                                        if killer != 2:
                                            if numRespuestaHumana2__T2 == "1":                                        
                                                secondSuspect "[pregunta4respuesta1]" 
                                            elif numRespuestaHumana2__T2 == "2": 
                                                secondSuspect "[pregunta4respuesta2]" 
                                            elif numRespuestaHumana2__T2 == "3": 
                                                secondSuspect "[pregunta4respuesta3]" 
                                            elif numRespuestaHumana2__T2 == "4": 
                                                secondSuspect "[pregunta4respuesta4]" 
                                            elif numRespuestaHumana2__T2 == "5": 
                                                secondSuspect "[pregunta4respuesta5]" 
                                        else:
                                            secondSuspect "[response4]" 
                                        $num_pregs2 = num_pregs2 + 1   
                                        jump tema2sospechoso2ingles
                                    "Do you usually go out at night?":
                                        if killer != 2:
                                            if numRespuestaHumana2__T2 == "1":                                        
                                                secondSuspect "[pregunta5respuesta1]" 
                                            elif numRespuestaHumana2__T2 == "2": 
                                                secondSuspect "[pregunta5respuesta2]" 
                                            elif numRespuestaHumana2__T2 == "3": 
                                                secondSuspect "[pregunta5respuesta3]" 
                                            elif numRespuestaHumana2__T2 == "4": 
                                                secondSuspect "[pregunta5respuesta4]" 
                                            elif numRespuestaHumana2__T2 == "5": 
                                                secondSuspect "[pregunta5respuesta5]" 
                                        else:
                                            secondSuspect "[response5]"
                                        $num_pregs2 = num_pregs2 + 1   
                                        jump tema2sospechoso2ingles
                                    "Aren't you afraid to go out at that time?":
                                        if killer != 2:
                                            if numRespuestaHumana2__T2 == "1":                                        
                                                secondSuspect "[pregunta6respuesta1]" 
                                            elif numRespuestaHumana2__T2 == "2": 
                                                secondSuspect "[pregunta6respuesta2]" 
                                            elif numRespuestaHumana2__T2 == "3": 
                                                secondSuspect "[pregunta6respuesta3]" 
                                            elif numRespuestaHumana2__T2 == "4": 
                                                secondSuspect "[pregunta6respuesta4]" 
                                            elif numRespuestaHumana2__T2 == "5": 
                                                secondSuspect "[pregunta6respuesta5]" 
                                        else:
                                            secondSuspect "[response6]"
                                        $num_pregs2 = num_pregs2 + 1   
                                        jump tema2sospechoso2ingles  
                                    "Go back":
                                        jump next_suspect  
                        "Ask about the neighborhood":
                            label tema3sospechoso2ingles:
                                menu:
                                    "Why did you go through the neighborhood?":
                                        if killer != 2:
                                            if numRespuestaHumana2__T3 == "1":                                        
                                                secondSuspect "[pregunta7respuesta1]" 
                                            elif numRespuestaHumana2__T3 == "2": 
                                                secondSuspect "[pregunta7respuesta2]" 
                                            elif numRespuestaHumana2__T3 == "3": 
                                                secondSuspect "[pregunta7respuesta3]" 
                                            elif numRespuestaHumana2__T3 == "4": 
                                                secondSuspect "[pregunta7respuesta4]" 
                                            elif numRespuestaHumana2__T3 == "5": 
                                                secondSuspect "[pregunta7respuesta5]" 
                                        else:
                                            secondSuspect "[response7]" 
                                        $num_pregs2 = num_pregs2 + 1   
                                        jump tema3sospechoso2ingles
                                    "Did you know anyone in the neighborhood?":
                                        if killer != 2:
                                            if numRespuestaHumana2__T3 == "1":                                        
                                                secondSuspect "[pregunta8respuesta1]" 
                                            elif numRespuestaHumana2__T3 == "2": 
                                                secondSuspect "[pregunta8respuesta2]" 
                                            elif numRespuestaHumana2__T3 == "3": 
                                                secondSuspect "[pregunta8respuesta3]" 
                                            elif numRespuestaHumana2__T3 == "4": 
                                                secondSuspect "[pregunta8respuesta4]" 
                                            elif numRespuestaHumana2__T3 == "5": 
                                                secondSuspect "[pregunta8respuesta5]" 
                                        else:
                                            secondSuspect "[response8]"
                                        $num_pregs2 = num_pregs2 + 1   
                                        jump tema3sospechoso2ingles
                                    "Is the neighborhood a frequent traffic place for you?":
                                        if killer != 2:
                                            if numRespuestaHumana2__T3 == "1":                                        
                                                secondSuspect "[pregunta9respuesta1]" 
                                            elif numRespuestaHumana2__T3 == "2": 
                                                secondSuspect "[pregunta9respuesta2]" 
                                            elif numRespuestaHumana2__T3 == "3": 
                                                secondSuspect "[pregunta9respuesta3]" 
                                            elif numRespuestaHumana2__T3 == "4": 
                                                secondSuspect "[pregunta9respuesta4]" 
                                            elif numRespuestaHumana2__T3 == "5": 
                                                secondSuspect "[pregunta9respuesta5]" 
                                        else:
                                            secondSuspect "[response9]"
                                        $num_pregs2 = num_pregs2 + 1   
                                        jump tema3sospechoso2ingles  
                                    "Go back":
                                        jump next_suspect  
                        "Ask about the suspect":
                            label tema4sospechoso2ingles:
                                menu:
                                    "Do you have a criminal record?":
                                        if killer != 2:
                                            if numRespuestaHumana2__T4 == "1":                                        
                                                secondSuspect "[pregunta10respuesta1]" 
                                            elif numRespuestaHumana2__T4 == "2": 
                                                secondSuspect "[pregunta10respuesta2]" 
                                            elif numRespuestaHumana2__T4 == "3": 
                                                secondSuspect "[pregunta10respuesta3]" 
                                            elif numRespuestaHumana2__T4 == "4": 
                                                secondSuspect "[pregunta10respuesta4]" 
                                            elif numRespuestaHumana2__T4 == "5": 
                                                secondSuspect "[pregunta10respuesta5]" 
                                        else:
                                            secondSuspect "[response10]" 
                                        $num_pregs2 = num_pregs2 + 1   
                                        jump tema4sospechoso2ingles
                                    "Has anyone you know ever been arrested?":
                                        if killer != 2:
                                            if numRespuestaHumana2__T4 == "1":                                        
                                                secondSuspect "[pregunta11respuesta1]" 
                                            elif numRespuestaHumana2__T4 == "2": 
                                                secondSuspect "[pregunta11respuesta2]" 
                                            elif numRespuestaHumana2__T4 == "3": 
                                                secondSuspect "[pregunta11respuesta3]" 
                                            elif numRespuestaHumana2__T4 == "4": 
                                                secondSuspect "[pregunta11respuesta4]" 
                                            elif numRespuestaHumana2__T4 == "5": 
                                                secondSuspect "[pregunta11respuesta5]" 
                                        else:
                                            secondSuspect "[response11]"
                                        $num_pregs2 = num_pregs2 + 1   
                                        jump tema4sospechoso2ingles
                                    "Do you know what the sentence is for murdering someone?":
                                        if killer != 2:
                                            if numRespuestaHumana2__T4 == "1":                                        
                                                secondSuspect "[pregunta12respuesta1]" 
                                            elif numRespuestaHumana2__T4 == "2": 
                                                secondSuspect "[pregunta12respuesta2]" 
                                            elif numRespuestaHumana2__T4 == "3": 
                                                secondSuspect "[pregunta12respuesta3]" 
                                            elif numRespuestaHumana2__T4 == "4": 
                                                secondSuspect "[pregunta12respuesta4]" 
                                            elif numRespuestaHumana2__T4 == "5": 
                                                secondSuspect "[pregunta12respuesta5]" 
                                        else:
                                            secondSuspect "[response12]"
                                        $num_pregs2 = num_pregs2 + 1   
                                        jump tema4sospechoso2ingles      
                                    "Go back":
                                            jump next_suspect                         
                        "Enough questions. We move on to the next suspect.":
                            you_EN "Please, let the third suspect come through."
                            hide sprite4 angry small with dissolve
                            think_EN "What should I ask now?"
                            show sprite2 angry small with dissolve 
                            jump last_suspect   
                        "Go back to the previous suspect.":
                            hide sprite4 angry small with dissolve
                            show sprite1 angry small with dissolve
                            jump interrogation     

                label last_suspect:            

                    if version == "maria-large" or version == "maria-base" or version == "spanish":
                        #TERCER INTERROGADO CASTELLANO                        
                        menu:
                            "Preguntar acerca del vecino":
                                label tema1sospechoso3castellano:
                                    menu:
                                        "¿Conocías al vecino asesinado?":
                                            if killer != 3:
                                                if numRespuestaHumana3__T1 == "1":                                        
                                                    thirdSuspect "[pregunta1respuesta1]" 
                                                elif numRespuestaHumana3__T1 == "2": 
                                                    thirdSuspect "[pregunta1respuesta2]" 
                                                elif numRespuestaHumana3__T1 == "3": 
                                                    thirdSuspect "[pregunta1respuesta3]" 
                                                elif numRespuestaHumana3__T1 == "4": 
                                                    thirdSuspect "[pregunta1respuesta4]" 
                                                elif numRespuestaHumana3__T1 == "5": 
                                                    thirdSuspect "[pregunta1respuesta5]" 
                                            else:
                                                thirdSuspect "[response1]" 
                                            $num_pregs3 = num_pregs3 + 1   
                                            jump tema1sospechoso3castellano
                                        "¿Alguna vez has visto al vecino por la calle?":
                                            if killer != 3:
                                                if numRespuestaHumana3__T1 == "1":                                        
                                                    thirdSuspect "[pregunta2respuesta1]" 
                                                elif numRespuestaHumana3__T1 == "2": 
                                                    thirdSuspect "[pregunta2respuesta2]" 
                                                elif numRespuestaHumana3__T1 == "3": 
                                                    thirdSuspect "[pregunta2respuesta3]" 
                                                elif numRespuestaHumana3__T1 == "4": 
                                                    thirdSuspect "[pregunta2respuesta4]" 
                                                elif numRespuestaHumana3__T1 == "5": 
                                                    thirdSuspect "[pregunta2respuesta5]"
                                            else:
                                                thirdSuspect "[response2]"
                                            $num_pregs3 = num_pregs3 + 1   
                                            jump tema1sospechoso3castellano
                                        "¿Alguna vez has oído hablar del vecino?":
                                            if killer != 3:
                                                if numRespuestaHumana3__T1 == "1":                                        
                                                    thirdSuspect "[pregunta3respuesta1]" 
                                                elif numRespuestaHumana3__T1 == "2": 
                                                    thirdSuspect "[pregunta3respuesta2]" 
                                                elif numRespuestaHumana3__T1 == "3": 
                                                    thirdSuspect "[pregunta3respuesta3]" 
                                                elif numRespuestaHumana3__T1 == "4": 
                                                    thirdSuspect "[pregunta3respuesta4]" 
                                                elif numRespuestaHumana3__T1 == "5": 
                                                    thirdSuspect "[pregunta3respuesta5]"
                                            else:
                                                thirdSuspect "[response3]"
                                            $num_pregs3 = num_pregs3 + 1   
                                            jump tema1sospechoso3castellano
                                        "Volver atrás":
                                            jump last_suspect
                            "Preguntar acerca de la noche":
                                label tema2sospechoso3castellano:
                                    menu:
                                        "¿Qué estuviste haciendo anoche?":
                                            if killer != 3:
                                                if numRespuestaHumana3__T2 == "1":                                        
                                                    thirdSuspect "[pregunta4respuesta1]" 
                                                elif numRespuestaHumana3__T2 == "2": 
                                                    thirdSuspect "[pregunta4respuesta2]" 
                                                elif numRespuestaHumana3__T2 == "3": 
                                                    thirdSuspect "[pregunta4respuesta3]" 
                                                elif numRespuestaHumana3__T2 == "4": 
                                                    thirdSuspect "[pregunta4respuesta4]" 
                                                elif numRespuestaHumana3__T2 == "5": 
                                                    thirdSuspect "[pregunta4respuesta5]"
                                            else:
                                                thirdSuspect "[response4]" 
                                            $num_pregs3 = num_pregs3 + 1   
                                            jump tema2sospechoso3castellano
                                        "¿Sueles salir por la noche?":
                                            if killer != 3:
                                                if numRespuestaHumana3__T2 == "1":                                        
                                                    thirdSuspect "[pregunta5respuesta1]" 
                                                elif numRespuestaHumana3__T2 == "2": 
                                                    thirdSuspect "[pregunta5respuesta2]" 
                                                elif numRespuestaHumana3__T2 == "3": 
                                                    thirdSuspect "[pregunta5respuesta3]" 
                                                elif numRespuestaHumana3__T2 == "4": 
                                                    thirdSuspect "[pregunta5respuesta4]" 
                                                elif numRespuestaHumana3__T2 == "5": 
                                                    thirdSuspect "[pregunta5respuesta5]"
                                            else:
                                                thirdSuspect "[response5]"
                                            $num_pregs3 = num_pregs3 + 1   
                                            jump tema2sospechoso3castellano
                                        "¿No tienes miedo de salir a esas horas?":
                                            if killer != 3:
                                                if numRespuestaHumana3__T2 == "1":                                        
                                                    thirdSuspect "[pregunta6respuesta1]" 
                                                elif numRespuestaHumana3__T2 == "2": 
                                                    thirdSuspect "[pregunta6respuesta2]" 
                                                elif numRespuestaHumana3__T2 == "3": 
                                                    thirdSuspect "[pregunta6respuesta3]" 
                                                elif numRespuestaHumana3__T2 == "4": 
                                                    thirdSuspect "[pregunta6respuesta4]" 
                                                elif numRespuestaHumana3__T2 == "5": 
                                                    thirdSuspect "[pregunta6respuesta5]"
                                            else:
                                                thirdSuspect "[response6]"
                                            $num_pregs3 = num_pregs3 + 1   
                                            jump tema2sospechoso3castellano  
                                        "Volver atrás":
                                            jump last_suspect
                            "Preguntar acerca del vecindario":
                                label tema3sospechoso3castellano:
                                    menu:
                                        "¿Por qué pasaste por el vecindario?":
                                            if killer != 3:
                                                if numRespuestaHumana3__T3 == "1":                                        
                                                    thirdSuspect "[pregunta7respuesta1]" 
                                                elif numRespuestaHumana3__T3 == "2": 
                                                    thirdSuspect "[pregunta7respuesta2]" 
                                                elif numRespuestaHumana3__T3 == "3": 
                                                    thirdSuspect "[pregunta7respuesta3]"
                                                elif numRespuestaHumana3__T3 == "4": 
                                                    thirdSuspect "[pregunta7respuesta4]" 
                                                elif numRespuestaHumana3__T3 == "5": 
                                                    thirdSuspect "[pregunta7respuesta5]" 
                                            else:
                                                thirdSuspect "[response7]" 
                                            $num_pregs3 = num_pregs3 + 1   
                                            jump tema3sospechoso3castellano
                                        "¿Conocías a alguna persona del vecindario?":
                                            if killer != 3:
                                                if numRespuestaHumana3__T3 == "1":                                        
                                                    thirdSuspect "[pregunta8respuesta1]" 
                                                elif numRespuestaHumana3__T3 == "2": 
                                                    thirdSuspect "[pregunta8respuesta2]" 
                                                elif numRespuestaHumana3__T3 == "3": 
                                                    thirdSuspect "[pregunta8respuesta3]" 
                                                elif numRespuestaHumana3__T3 == "4": 
                                                    thirdSuspect "[pregunta8respuesta4]" 
                                                elif numRespuestaHumana3__T3 == "5": 
                                                    thirdSuspect "[pregunta8respuesta5]"
                                            else:
                                                thirdSuspect "[response8]"
                                            $num_pregs3 = num_pregs3 + 1   
                                            jump tema3sospechoso3castellano
                                        "¿El vecindario es un lugar de tránsito frecuente para ti?":
                                            if killer != 3:
                                                if numRespuestaHumana3__T3 == "1":                                        
                                                    thirdSuspect "[pregunta9respuesta1]" 
                                                elif numRespuestaHumana3__T3 == "2": 
                                                    thirdSuspect "[pregunta9respuesta2]" 
                                                elif numRespuestaHumana3__T3 == "3": 
                                                    thirdSuspect "[pregunta9respuesta3]" 
                                                elif numRespuestaHumana3__T3 == "4": 
                                                    thirdSuspect "[pregunta9respuesta4]" 
                                                elif numRespuestaHumana3__T3 == "5": 
                                                    thirdSuspect "[pregunta9respuesta5]"
                                            else:
                                                thirdSuspect "[response9]"
                                            $num_pregs3 = num_pregs3 + 1   
                                            jump tema3sospechoso3castellano  
                                        "Volver atrás":
                                            jump last_suspect
                            "Preguntar acerca del sospechoso":
                                label tema4sospechoso3castellano:
                                    menu:
                                        "¿Tienes antecedentes penales?":
                                            if killer != 3:
                                                if numRespuestaHumana3__T4 == "1":                                        
                                                    thirdSuspect "[pregunta10respuesta1]" 
                                                elif numRespuestaHumana3__T4 == "2": 
                                                    thirdSuspect "[pregunta10respuesta2]" 
                                                elif numRespuestaHumana3__T4 == "3": 
                                                    thirdSuspect "[pregunta10respuesta3]" 
                                                elif numRespuestaHumana3__T4 == "4": 
                                                    thirdSuspect "[pregunta10respuesta4]" 
                                                elif numRespuestaHumana3__T4 == "5": 
                                                    thirdSuspect "[pregunta10respuesta5]"
                                            else:
                                                thirdSuspect "[response10]" 
                                            $num_pregs3 = num_pregs3 + 1   
                                            jump tema4sospechoso3castellano
                                        "¿Alguna vez han detenido a algún conocido tuyo?":
                                            if killer != 3:
                                                if numRespuestaHumana3__T4 == "1":                                        
                                                    thirdSuspect "[pregunta11respuesta1]" 
                                                elif numRespuestaHumana3__T4 == "2": 
                                                    thirdSuspect "[pregunta11respuesta2]" 
                                                elif numRespuestaHumana3__T4 == "3": 
                                                    thirdSuspect "[pregunta11respuesta3]" 
                                                elif numRespuestaHumana3__T4 == "4": 
                                                    thirdSuspect "[pregunta11respuesta4]" 
                                                elif numRespuestaHumana3__T4 == "5": 
                                                    thirdSuspect "[pregunta11respuesta5]"
                                            else:
                                                thirdSuspect "[response11]"
                                            $num_pregs3 = num_pregs3 + 1   
                                            jump tema4sospechoso3castellano
                                        "¿Sabes cúal es la condena por asesinar a alguien?":
                                            if killer != 3:
                                                if numRespuestaHumana3__T4 == "1":                                        
                                                    thirdSuspect "[pregunta12respuesta1]" 
                                                elif numRespuestaHumana3__T4 == "2": 
                                                    thirdSuspect "[pregunta12respuesta2]" 
                                                elif numRespuestaHumana3__T4 == "3": 
                                                    thirdSuspect "[pregunta12respuesta3]" 
                                                elif numRespuestaHumana3__T4 == "4": 
                                                    thirdSuspect "[pregunta12respuesta4]" 
                                                elif numRespuestaHumana3__T4 == "5": 
                                                    thirdSuspect "[pregunta12respuesta5]"
                                            else:
                                                thirdSuspect "[response12]"
                                            $num_pregs3 = num_pregs3 + 1   
                                            jump tema4sospechoso3castellano   
                                        "Volver atrás":
                                            jump last_suspect    
                            "Suficientes preguntas. Creo que ya se quién es el androide.":
                                hide sprite2 angry small with dissolve                       
                                jump resolve_case 
                            "Volver al sospechoso anterior.":
                                hide sprite2 angry small with dissolve   
                                show sprite4 angry small with dissolve 
                                jump next_suspect          
                    else:                
                        #TERCER INTERROGADO INGLÉS
                        menu:
                            "Ask about the neighbor":
                                label tema1sospechoso3ingles:
                                    menu:
                                        "Did you know the murdered neighbor?":
                                            if killer != 3:
                                                if numRespuestaHumana3__T1 == "1":                                        
                                                    thirdSuspect "[pregunta1respuesta1]" 
                                                elif numRespuestaHumana3__T1 == "2": 
                                                    thirdSuspect "[pregunta1respuesta2]" 
                                                elif numRespuestaHumana3__T1 == "3": 
                                                    thirdSuspect "[pregunta1respuesta3]" 
                                                elif numRespuestaHumana3__T1 == "4": 
                                                    thirdSuspect "[pregunta1respuesta4]" 
                                                elif numRespuestaHumana3__T1 == "5": 
                                                    thirdSuspect "[pregunta1respuesta5]"
                                            else:
                                                thirdSuspect "[response1]" 
                                            $num_pregs3 = num_pregs3 + 1   
                                            jump tema1sospechoso3ingles
                                        "Have you ever seen the neighbor on the street?":
                                            if killer != 3:
                                                if numRespuestaHumana3__T1 == "1":                                        
                                                    thirdSuspect "[pregunta2respuesta1]" 
                                                elif numRespuestaHumana3__T1 == "2": 
                                                    thirdSuspect "[pregunta2respuesta2]" 
                                                elif numRespuestaHumana3__T1 == "3": 
                                                    thirdSuspect "[pregunta2respuesta3]" 
                                                elif numRespuestaHumana3__T1 == "4": 
                                                    thirdSuspect "[pregunta2respuesta4]" 
                                                elif numRespuestaHumana3__T1 == "5": 
                                                    thirdSuspect "[pregunta2respuesta5]"
                                            else:
                                                thirdSuspect "[response2]"
                                            $num_pregs3 = num_pregs3 + 1   
                                            jump tema1sospechoso3ingles
                                        "Have you ever heard of the neighbor?":
                                            if killer != 3:
                                                if numRespuestaHumana3__T1 == "1":                                        
                                                    thirdSuspect "[pregunta3respuesta1]" 
                                                elif numRespuestaHumana3__T1 == "2": 
                                                    thirdSuspect "[pregunta3respuesta2]" 
                                                elif numRespuestaHumana3__T1 == "3": 
                                                    thirdSuspect "[pregunta3respuesta3]" 
                                                elif numRespuestaHumana3__T1 == "4": 
                                                    thirdSuspect "[pregunta3respuesta4]" 
                                                elif numRespuestaHumana3__T1 == "5": 
                                                    thirdSuspect "[pregunta3respuesta5]"
                                            else:
                                                thirdSuspect "[response3]"
                                            $num_pregs3 = num_pregs3 + 1   
                                            jump tema1sospechoso3ingles
                                        "Go back":
                                            jump last_suspect
                            "Ask about tonight":
                                label tema2sospechoso3ingles:
                                    menu:
                                        "What were you doing last night?":
                                            if killer != 3:
                                                if numRespuestaHumana3__T2 == "1":                                        
                                                    thirdSuspect "[pregunta4respuesta1]" 
                                                elif numRespuestaHumana3__T2 == "2": 
                                                    thirdSuspect "[pregunta4respuesta2]" 
                                                elif numRespuestaHumana3__T2 == "3": 
                                                    thirdSuspect "[pregunta4respuesta3]" 
                                                elif numRespuestaHumana3__T2 == "4": 
                                                    thirdSuspect "[pregunta4respuesta4]" 
                                                elif numRespuestaHumana3__T2 == "5": 
                                                    thirdSuspect "[pregunta4respuesta5]"
                                            else:
                                                thirdSuspect "[response4]" 
                                            $num_pregs3 = num_pregs3 + 1   
                                            jump tema2sospechoso3ingles
                                        "Do you usually go out at night?":
                                            if killer != 3:
                                                if numRespuestaHumana3__T2 == "1":                                        
                                                    thirdSuspect "[pregunta5respuesta1]" 
                                                elif numRespuestaHumana3__T2 == "2": 
                                                    thirdSuspect "[pregunta5respuesta2]" 
                                                elif numRespuestaHumana3__T2 == "3": 
                                                    thirdSuspect "[pregunta5respuesta3]" 
                                                elif numRespuestaHumana3__T2 == "4": 
                                                    thirdSuspect "[pregunta5respuesta4]" 
                                                elif numRespuestaHumana3__T2 == "5": 
                                                    thirdSuspect "[pregunta5respuesta5]"
                                            else:
                                                thirdSuspect "[response5]"
                                            $num_pregs3 = num_pregs3 + 1   
                                            jump tema2sospechoso3ingles
                                        "Aren't you afraid to go out at that time?":
                                            if killer != 3:
                                                if numRespuestaHumana3__T2 == "1":                                        
                                                    thirdSuspect "[pregunta6respuesta1]" 
                                                elif numRespuestaHumana3__T2 == "2": 
                                                    thirdSuspect "[pregunta6respuesta2]" 
                                                elif numRespuestaHumana3__T2 == "3": 
                                                    thirdSuspect "[pregunta6respuesta3]"
                                                elif numRespuestaHumana3__T2 == "4": 
                                                    thirdSuspect "[pregunta6respuesta4]" 
                                                elif numRespuestaHumana3__T2 == "5": 
                                                    thirdSuspect "[pregunta6respuesta5]"
                                            else:
                                                thirdSuspect "[response6]"
                                            $num_pregs3 = num_pregs3 + 1   
                                            jump tema2sospechoso3ingles  
                                        "Go back":
                                            jump last_suspect
                            "Ask about the neighborhood":
                                label tema3sospechoso3ingles:
                                    menu:
                                        "Why did you go through the neighborhood?":
                                            if killer != 3:
                                                if numRespuestaHumana3__T3 == "1":                                        
                                                    thirdSuspect "[pregunta7respuesta1]" 
                                                elif numRespuestaHumana3__T3 == "2": 
                                                    thirdSuspect "[pregunta7respuesta2]" 
                                                elif numRespuestaHumana3__T3 == "3": 
                                                    thirdSuspect "[pregunta7respuesta3]" 
                                                elif numRespuestaHumana3__T3 == "4": 
                                                    thirdSuspect "[pregunta7respuesta4]" 
                                                elif numRespuestaHumana3__T3 == "5": 
                                                    thirdSuspect "[pregunta7respuesta5]"
                                            else:
                                                thirdSuspect "[response7]" 
                                            $num_pregs3 = num_pregs3 + 1   
                                            jump tema3sospechoso3ingles
                                        "Did you know anyone in the neighborhood?":
                                            if killer != 3:
                                                if numRespuestaHumana3__T3 == "1":                                        
                                                    thirdSuspect "[pregunta8respuesta1]" 
                                                elif numRespuestaHumana3__T3 == "2": 
                                                    thirdSuspect "[pregunta8respuesta2]" 
                                                elif numRespuestaHumana3__T3 == "3": 
                                                    thirdSuspect "[pregunta8respuesta3]" 
                                                elif numRespuestaHumana3__T3 == "4": 
                                                    thirdSuspect "[pregunta8respuesta4]" 
                                                elif numRespuestaHumana3__T3 == "5": 
                                                    thirdSuspect "[pregunta8respuesta5]"
                                            else:
                                                thirdSuspect "[response8]"
                                            $num_pregs3 = num_pregs3 + 1   
                                            jump tema3sospechoso3ingles
                                        "Is the neighborhood a frequent traffic place for you?":
                                            if killer != 3:
                                                if numRespuestaHumana3__T3 == "1":                                        
                                                    thirdSuspect "[pregunta9respuesta1]" 
                                                elif numRespuestaHumana3__T3 == "2": 
                                                    thirdSuspect "[pregunta9respuesta2]" 
                                                elif numRespuestaHumana3__T3 == "3": 
                                                    thirdSuspect "[pregunta9respuesta3]" 
                                                elif numRespuestaHumana3__T3 == "4": 
                                                    thirdSuspect "[pregunta9respuesta4]" 
                                                elif numRespuestaHumana3__T3 == "5": 
                                                    thirdSuspect "[pregunta9respuesta5]"
                                            else:
                                                thirdSuspect "[response9]"
                                            $num_pregs3 = num_pregs3 + 1   
                                            jump tema3sospechoso3ingles  
                                        "Go back":
                                            jump last_suspect
                            "Ask about the suspect":
                                label tema4sospechoso3ingles:
                                    menu:
                                        "Do you have a criminal record?":
                                            if killer != 3:
                                                if numRespuestaHumana3__T4 == "1":                                        
                                                    thirdSuspect "[pregunta10respuesta1]" 
                                                elif numRespuestaHumana3__T4 == "2": 
                                                    thirdSuspect "[pregunta10respuesta2]" 
                                                elif numRespuestaHumana3__T4 == "3": 
                                                    thirdSuspect "[pregunta10respuesta3]" 
                                                elif numRespuestaHumana3__T4 == "4": 
                                                    thirdSuspect "[pregunta10respuesta4]" 
                                                elif numRespuestaHumana3__T4 == "5": 
                                                    thirdSuspect "[pregunta10respuesta5]"
                                            else:
                                                thirdSuspect "[response10]" 
                                            $num_pregs3 = num_pregs3 + 1   
                                            jump tema4sospechoso3ingles
                                        "Has anyone you know ever been arrested?":
                                            if killer != 3:
                                                if numRespuestaHumana3__T4 == "1":                                        
                                                    thirdSuspect "[pregunta11respuesta1]" 
                                                elif numRespuestaHumana3__T4 == "2": 
                                                    thirdSuspect "[pregunta11respuesta2]" 
                                                elif numRespuestaHumana3__T4 == "3": 
                                                    thirdSuspect "[pregunta11respuesta3]" 
                                                elif numRespuestaHumana3__T4 == "4": 
                                                    thirdSuspect "[pregunta11respuesta4]" 
                                                elif numRespuestaHumana3__T4 == "5": 
                                                    thirdSuspect "[pregunta11respuesta5]"
                                            else:
                                                thirdSuspect "[response11]"
                                            $num_pregs3 = num_pregs3 + 1   
                                            jump tema4sospechoso3ingles
                                        "Do you know what the sentence is for murdering someone?":
                                            if killer != 3:
                                                if numRespuestaHumana3__T4 == "1":                                        
                                                    thirdSuspect "[pregunta12respuesta1]" 
                                                elif numRespuestaHumana3__T4 == "2": 
                                                    thirdSuspect "[pregunta12respuesta2]" 
                                                elif numRespuestaHumana3__T4 == "3": 
                                                    thirdSuspect "[pregunta12respuesta3]" 
                                                elif numRespuestaHumana3__T4 == "4": 
                                                    thirdSuspect "[pregunta12respuesta4]" 
                                                elif numRespuestaHumana3__T4 == "5": 
                                                    thirdSuspect "[pregunta12respuesta5]"
                                            else:
                                                thirdSuspect "[response12]"
                                            $num_pregs3 = num_pregs3 + 1   
                                            jump tema4sospechoso3ingles  
                                        "Go back":
                                            jump last_suspect  
                            "Enough questions. I think I know who the android is.":
                                hide sprite2 angry small with dissolve                       
                                jump resolve_case    
                            "Go back to the previous suspect.":
                                hide sprite2 angry small with dissolve   
                                show sprite4 angry small with dissolve 
                                jump next_suspect      

                    label resolve_case:
                        show sprite3 sad small with dissolve

                        if version == "maria-large" or version == "maria-base" or version == "spanish":
                            police_ES "No hay más sospechosos, detective. Bien, ¿quién crees que puede ser el asesino?"
                            menu:
                                "Anna":
                                    $election = 1
                                "Daniel":
                                    $election = 2
                                "Emma":
                                    $election = 3
                            police_ES "De acuerdo, puedes irte a casa. Ojalá hayamos tomado la decisión correcta."
                            
                        else:                        
                            police_EN "There are no more suspects, detective. Well, who do you think is the killer?"
                            menu:
                                "Anna":
                                    $election = 1
                                "Daniel":
                                    $election = 2
                                "Emma":
                                    $election = 3
                            police_EN "Okay, you can go home. Hopefully the decision is correct."

                        scene bg train with dissolve
                        play sound "audio/346573__inspectorj__train-door-beep-a.ogg" volume 1 fadein 0.5
                        pause 2.0
                        stop sound fadeout 1

                        hide sprite3 sad small with dissolve
                        scene bg room dark with dissolve 
                        play sound "audio/613178__sound-designer-from-turkey__music-box-g-4-4-60-bpm.ogg" volume 0.5 fadein 0.5
                        pause 3
                        stop sound fadeout 1
                        play sound "audio/457869__inchadney__british-telephone.ogg" volume 1 fadein 0.5    

                        if version == "maria-large" or version == "maria-base" or version == "spanish":
                            telephone_ES "Riiiiiing riiiiiiiing riiiiiing"
                            stop sound fadeout 0.5
                            scene bg room with dissolve
                            if election != killer:
                                $result = 'L'
                                show sprite3 angry small with dissolve                     
                                police_ES "Detective, ha habido un nuevo asesinato. El asesino aún está libre."
                                hide sprite3 angry small with dissolve                                 
                                play sound "audio/362204__taranp__horn-fail-wahwah-3.ogg" volume 0.5 fadein 0.25                                 
                                scene bg room dark with Dissolve(0.75)        
                                pause 0.1    
                                if killer == 1:
                                    show sprite1 happy small with Dissolve(0.25)  
                                    "Has perdido... El androide era Anna..."
                                elif killer == 2:
                                    show sprite4 happy small with Dissolve(0.25)   
                                    "Has perdido... El androide era Daniel..."
                                elif killer == 3:
                                    show sprite2 happy small with Dissolve(0.25)  
                                    "Has perdido... El androide era Emma..."                                
                                jump end
                            else:
                                $result = 'W'
                                show sprite3 happy small with dissolve
                                police_ES "Detective, hemos pasado una noche tranquila. No ha habido más asesinatos. Creo que hemos acertado descubriendo al asesino."                        
                                play sound "audio/521646__fupicat__winmutedguitar.ogg" volume 1 fadein 0.25                                
                                hide sprite3 happy small with dissolve 
                                pause 0.2
                                if killer == 1:
                                    show sprite1 sad small with Dissolve(0.25)  
                                    "¡Has ganado! ¡El androide era Anna!"
                                elif killer == 2:
                                    show sprite4 sad small with Dissolve(0.25)   
                                    "¡Has ganado! ¡El androide era Daniel!"
                                elif killer == 3:
                                    show sprite2 sad small with Dissolve(0.25)  
                                    "¡Has ganado! ¡El androide era Emma!"                                
                                jump end
                        else:
                            telephone_EN "Riiiiiing riiiiiiiing riiiiiing"
                            stop sound fadeout 0.5
                            scene bg room with dissolve
                            if election != killer:
                                $result = 'L'
                                show sprite3 angry small with dissolve                     
                                police_EN "Detective, there's been a new murder. The killer is still free."
                                hide sprite3 angry small with dissolve                                 
                                play sound "audio/362204__taranp__horn-fail-wahwah-3.ogg" volume 0.5 fadein 0.25                                 
                                scene bg room dark with Dissolve(0.75)        
                                pause 0.1                
                                if killer == 1:
                                    show sprite1 happy small with Dissolve(0.25)  
                                    "You lost... The android was Anna..."
                                elif killer == 2:
                                    show sprite4 happy small with Dissolve(0.25)   
                                    "You lost... The android was Daniel..."
                                elif killer == 3:
                                    show sprite2 happy small with Dissolve(0.25)  
                                    "You lost... The android was Emma..."                                
                                jump end
                            else:
                                $result = 'W'
                                show sprite3 happy small with dissolve
                                police_EN "Detective, we've had a quiet night. There have been no more murders. I think we succeeded in discovering the murderer."
                                play sound "audio/521646__fupicat__winmutedguitar.ogg" volume 1 fadein 0.25                                
                                hide sprite3 happy small with dissolve  
                                pause 0.2
                                if killer == 1:
                                    show sprite1 sad small with Dissolve(0.25)  
                                    "You win! The android was Anna!"
                                elif killer == 2:
                                    show sprite4 sad small with Dissolve(0.25)   
                                    "You win! The android was Daniel!"
                                elif killer == 3:
                                    show sprite2 sad small with Dissolve(0.25) 
                                    "You win! The android was Emma!"                                
                                jump end

                        label end:   
                            stop sound fadeout 0.25  
                            window hide
                            if election != killer:
                                play sound "audio/613178__sound-designer-from-turkey__music-box-g-4-4-60-bpm.ogg" volume 0.25 fadein 1
                                if killer == 1:
                                    hide sprite1 happy small with Dissolve(0.25)  
                                elif killer == 2:
                                    hide sprite4 happy small with Dissolve(0.25)   
                                elif killer == 3:
                                    hide sprite2 happy small with Dissolve(0.25)  
                            else:
                                if killer == 1:
                                    hide sprite1 sad small with Dissolve(0.25)  
                                elif killer == 2:
                                    hide sprite4 sad small with Dissolve(0.25)  
                                elif killer == 3:
                                    hide sprite2 sad small with Dissolve(0.25) 
                            pause 0.5
                            if version == "maria-large" or version == "maria-base" or version == "spanish":
                                if election == killer:
                                    show text "{color=#000000}{b}CRÉDITOS\n\n\n\n\n\n{/b}{/color}" with Dissolve(0.5) 
                                    pause 2
                                    show text "{color=#000000}{b}Diseñado, escrito y programado por\n\nFrancesc Bellido Delgado\n\n\n\n{/b}{/color}" with Dissolve(0.5) 
                                else:
                                    show text "{b}CRÉDITOS\n\n\n\n\n\n{/b}" with Dissolve(0.5) 
                                    pause 2
                                    show text "{b}Diseñado, escrito y programado por\n\nFrancesc Bellido Delgado\n\n\n\n{/b}" with Dissolve(0.5) 
                            else:
                                if election == killer:
                                    show text "{color=#000000}{b}CREDITS\n\n\n\n\n\n{/b}{/color}" with Dissolve(0.5) 
                                    pause 2
                                    show text "{color=#000000}{b}Designed, written and programmed by\n\nFrancesc Bellido Delgado\n\n\n\n{/b}{/color}" with Dissolve(0.5) 
                                else:
                                    show text "{b}CREDITS\n\n\n\n\n\n{/b}" with Dissolve(0.5) 
                                    pause 2
                                    show text "{b}Designed, written and programmed by\n\nFrancesc Bellido Delgado\n\n\n\n{/b}" with Dissolve(0.5)
                            python:
                                nameFile = 'test.txt'
                                contentFile = str(killer) + ':' + result + ';' + str(num_pregs1) + ';' + str(num_pregs2) + ';' + str(num_pregs3)
                                requests.get('http://localhost:4000/file/' + nameFile + '/' + contentFile)       
                            pause 1
                            if version == "maria-large" or version == "maria-base" or version == "spanish":
                                if election == killer:
                                    show text "{color=#000000}{b}Imágenes de usuarios de itch.io\n\nFülli\nNoranekoGames\nPotat0Master\nKonett\n{/b}{/color}" with Dissolve(0.5) 
                                    pause 3
                                    show text "{color=#000000}{b}Sonidos de usuarios de Fresound\n\ninchadney\nsound_designer_from_Turkey\nInspectorJ\nFupicat\nTaranP{/b}{/color}" with Dissolve(0.5) 
                                else:
                                    show text "{b}Imágenes de usuarios de itch.io\n\nFülli\nNoranekoGames\nPotat0Master\nKonett\n{/b}" with Dissolve(0.5) 
                                    pause 3
                                    show text "{b}Sonidos de usuarios de Fresound\n\ninchadney\nsound_designer_from_Turkey\nInspectorJ\nFupicat\nTaranP{/b}" with Dissolve(0.5) 
                            else:
                                if election == killer:
                                    show text "{color=#000000}{b}Images by itch.io users\n\nFülli\nNoranekoGames\nPotat0Master\nKonett\n{/b}{/color}" with Dissolve(0.5) 
                                    pause 3
                                    show text "{color=#000000}{b}Sounds by Fresound users\n\ninchadney\nsound_designer_from_Turkey\nInspectorJ\nFupicat\nTaranP{/b}{/color}" with Dissolve(0.5) 
                                else:
                                    show text "{b}Images by itch.io users\n\nFülli\nNoranekoGames\nPotat0Master\nKonett\n{/b}" with Dissolve(0.5) 
                                    pause 3
                                    show text "{b}Sounds by Fresound users\n\ninchadney\nsound_designer_from_Turkey\nInspectorJ\nFupicat\nTaranP{/b}" with Dissolve(0.5)                              
                            pause 1
                            if election != killer:
                                stop sound fadeout 0.5     
                            pause 1                                           
                            return

