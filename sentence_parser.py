# -*- coding: utf-8 -*-
"""
Created on Thu May 30 17:05:42 2019

@author: barak
"""

from __future__ import unicode_literals


#from spacy.vocab import Vocab
#from spacy.language import Language
#from spacy.lang.en import English
#from spacy.pipeline import DependencyParser
import en_core_web_sm

NUMBERS_DICT = {"zero":"0",
                "one": "1",
                "two": "2",
                "three": "3",
                "four": "4",
                "five": "5",
                "six": "6",
                "seven": "7",
                "eight": "8",
                "nine": "9"}

WORDS_THAT_SOUND_LIKE_NUMBERS = {
    "to" : "2",
    "free" : "3",
    "for" : "4",
    "ate" : "8",
    "sics" : "6",
    "sex" : "6",
    "nein" : "9",
    "sick" : "6",
}

VERB_2_VERB_DICT = {
        "update" : "set"}


SPECIAL_NUM_SYMBOLS = {".":".", "point":".", "dot":".", "period": ".", ",":'.', 'comma':'.'}
    
nlp = en_core_web_sm.load()
#parser = DependencyParser(nlp.vocab)


def string_to_numerical_string (num_named_string):

    num_named_string = num_named_string.lower()
    print(num_named_string)
    out_string = ""
    for sub_str in num_named_string.split():
        if(sub_str == ""):
            continue
        if(sub_str in NUMBERS_DICT):
            out_string += NUMBERS_DICT[sub_str]
        elif(sub_str in SPECIAL_NUM_SYMBOLS):
            out_string += SPECIAL_NUM_SYMBOLS[sub_str]
        elif(sub_str in  WORDS_THAT_SOUND_LIKE_NUMBERS):
            out_string += WORDS_THAT_SOUND_LIKE_NUMBERS[sub_str]
        else:
            try:
                num = float(sub_str)
                out_string += sub_str
            except:
                print(">>>Error! Found that string %s cant be parsed because it has the char %s" %(num_named_string, sub_str))
    return out_string

def getAction(spacy_sentence):
    for token in spacy_sentence:
        if token.pos_ == "VERB":
            return token
    print(">>> Error: Cannot find action")
    return nlp(" ")[0]

def getObject(spacy_sentence, action):
    for token in spacy_sentence:
        if token.head == action and not token.dep_ == "ROOT":
            if token.dep_ in ['dobj', 'iobj']:
                return token
    
    if action.lemma_ in ["read"]:
        return spacy_sentence[1]
    
    return nlp(" ")[0]

def getFrequency(spacy_sentence, token):
    current_token = spacy_sentence[token.i + 1]
    value = ""
    #If given the first token is a number
    #then we assume it means that our frequency is number based
    if current_token.pos_ == "NUM":
        value = getNumberedFrequency(current_token, spacy_sentence, value)
        return {"freq": string_to_numerical_string(value)}
    #Otherwise it is net based
    else:
        return getCallsignAndNumber(spacy_sentence, token)

def getNumberedFrequency(current_token, spacy_sentence, value):
    while (current_token.pos_ == "NUM" or
           current_token.lower_ in SPECIAL_NUM_SYMBOLS.keys() or
           current_token.lower_ in WORDS_THAT_SOUND_LIKE_NUMBERS.keys() or
           current_token.pos_ == "PUNCT" or
           current_token.pos_ == "SPACE"):

        if current_token.pos_ != "SPACE":
            value = "%s %s" % (value, current_token.lower_)

        if current_token.i != len(spacy_sentence) - 1:
            current_token = spacy_sentence[current_token.i + 1]
        else:
            break

        print(current_token.lower_)
    print("***")
    return value


def getValue(spacy_sentence, action, sentence_object):
    MODIFIER_CMD = ["set", "update"]
    GETTERS_COMMAND = ["get"]
    
#   Choose the word closest to the original meaning    
#    for cmd in ["Set", "Read", "Get"]:
#        x = spacy_sentence.text.split()
#        y = cmd + " "+" ".join(x[1:])
#        z = nlp(y)
#        print("%s similarity to %s is %s" % 
#              (action.text,
#               cmd.upper(),
#               z.similarity(spacy_sentence)))
#        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    if action.lemma_.lower() in MODIFIER_CMD + GETTERS_COMMAND:
        for token in spacy_sentence:
            if token.dep_ == 'prep':
                if token.head in [action, sentence_object]:
                    if action.lemma_.lower() in ["set", "update"]:
                        return getFrequency(spacy_sentence, token)
                    elif action.lemma_.lower() in ["get"]:
                        return getCallsignAndNumber(spacy_sentence, token)

    if action.lemma_.lower() in ["read"]:
        number = string_to_numerical_string(spacy_sentence[sentence_object.i+1].lemma_)
        return {'id': number}
                    
    return {'val':"zero"}


def getCallsignAndNumber(spacy_sentence, token):
    net = spacy_sentence[token.i + 1]
    num_in_net = spacy_sentence[token.i + 2]
    return {'callsign': net.text.lower(),
            'number': string_to_numerical_string(num_in_net.text)}


def syntesize_sentence(sentence):
    pre_out_json= {}
    value = ""

    processed_tokens = list()
    doc = nlp(sentence)

    if len(doc) == 1:
        return {'action': doc[0].lemma_}

    pre_out_json['action'] = getAction(doc)
    pre_out_json['object'] = getObject(doc, pre_out_json['action'])
    value = getValue(doc, pre_out_json['action'], pre_out_json['object'])
    
    for token in doc:   
        processed_tokens.append({'token':token,
                                 'tag': token.tag_,
                                 'lemma': token.lemma_,
                                 'dep': token.dep_,
                                 'orth': token.orth_,
                                 'parent': token.head,
                                 'entity_type': token.ent_type_,
                                 'norm' :token.norm_,
                                 'pos': token.pos_})

    #for token in non_obj_children:
        #if(value_to_set != "" and token.tag_ == 'CD'):
            #    print(">>>Error! Cannot parse... Built value %s but got confused since also saw %s"%(value_to_set,token.lower_))
     #   for desc_token in token.subtree:
      #      if(desc_token.tag_ == 'CD' or desc_token.lower_ in ["point", "dot"]):
       #         value = " ".join([value, desc_token.lower_])
    
    
     #print(pre_out_json)
    print("**************")
    print(processed_tokens)
    out_json = { field: token.lemma_.lower() for field, token in pre_out_json.items()}
    if out_json['action'] in VERB_2_VERB_DICT.keys():
        out_json['action'] = VERB_2_VERB_DICT[out_json['action']]
    out_json['value'] = value
    return out_json

if(__name__  == "__main__"):
    test_examples = ["Set the frequency to six five point two five",
                     #"Update the frequency to two two one dot five zero",
                     #"Get the frequency of Shodedim one",
                     #"Read text three"
                     "Set the frequency from pirates one",
                     "Undo"
                     ]

    for example in test_examples:
        print("Running with example '%s'"% example)
        print("Result:")
        x = syntesize_sentence(example)
        print(syntesize_sentence(example))
        print("==========")
