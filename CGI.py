# FILE: CGI (Cat Girl Intelligence)
VERSION_ = "prototype v0.1.4"

"""
SPECIFICATION:
CGI (Cat Girl Intelligence) is a simple question-answer program, similar but different from 1960s ELIZA.
It answers everything with some specified word embedded as the answer.
That word is "meow" by default.
- Wh- questions get answered with meow:
    - "What?" "Meow."
    - "Who?" "Meow."
    - "Why?" "Because of meowing."
    - "When?" "At meow."
    - "When are we going?" "We are going at meow."
    - "When is the party?" "The party is at meow."
    - "Who is that?" "That is meow."
    - "Who are we watching?" "We are watching meow."
    - "Who are we thinking about?" "We are thinking about meow."
    - "Why are we thinking?" "We are thinking because of meowing."
    - "Why are we walking by the seashore?" "We are walking by the seashore because of meowing."
    - "What are we doing?" "We are doing meow."
    - "What is the dog doing?" "The dog is doing meow."
    - "What is that?" "That is meow."
    - "What is that doing?" "That is doing meow."
    - "What is that doing over there?" "That is doing meow over there."
    - "What are we doing over there?" "We are doing meow over there."
    - "What are you doing over there?" "I am doing meow over there."
    - "What do you like doing?" "I like doing meow."
    - "Who does that?" "Meow does that."
    - "Who do we think?" "We think meow."
    - "What are you thinking about doing?" "I am thinking about doing meow."
    - "What are you thinking about doing over there?" "I am thinking about doing meow over there."
    - "Where are you thinking about sleeping at Johnson's?" "I am thinking about sleeping at meow at Johnson's."
    - "What am I thinking?" "You are thinking meow."
    - "Who am I?" "You are meow."
    - "Why am I?" "You are because of meowing."
    - "Who likes me?" "Meow likes you."
    - "What makes a loud purring noise?" "Meow makes a loud purring noise?"
    - "What does he do?" "He does meow?"
    - "What does he do for a living?" "He does meow for a living?"
    - "What do you think?" "I think meow."
    - "How do you do?" "I do meowing."
    - "How do you do it?" "I do it meowing."
    - "How are you?" "I am meowing."
    - "Where do you sleep?" "I sleep at meow."
    - "Where do you do your chores?" "I do my chores at meow."

    The handling of other tenses comes later. At first, I only do Present Simple and Present Continuous.
    [- "How did you do?" "I did meowing."
    - "When did we go?" "We went at meow."
    - "Who liked me?" "Meow liked you."
    - "Why were we walking by the seashore?" "We were walking by the seashore because of meowing."
    - "Why did we walk by the seashore?" "We walked by the seashore because of meowing."

    - "Where will you have been thinking about sleeping at Johnson's?" "I will have been thinking about sleeping at meow at Johnson's."]
    STRUCTURAL ANALYSIS:
    - WH BE SUBJ (COMPLEMENT1) (LAST -ing VERB) (COMPLEMENT2) -> SUBJ(INVERSE) BE(MATCHING) (COMPLEMENT1) (LAST -ing VERB) MEOW-ANSWER (COMPLEMENT2)
    - WH DO SUBJ VERB COMPLEMENT -> SUBJ(INVERSE) VERB(MATCHING) COMPLEMENT MEOW-ANSWER
    - WH VERBS COMPLEMENT -> MEOW-ANSWER VERBS COMPLEMENT
    - MEOW-ANSWERS:
        - What, who -> meow
        - When, where -> at meow
        - Why -> because of meowing
        - Which -> meow
        - How -> meowing
- Yes/No questions - everything is answered randomly with "Yes, meow." or "No, meow."
    - "Do you like tea?" "Yes, meow."
    - "Is there a tower?" "No, meow."
    - "Are we philosophical?" "Yes, meow."
    - "Do you like me?" "No, meow." "Really?" "No, meow."
- Unrecognized grammatical structures, if detected, are answered with random affirmations, or questioned:
    - "Unequivocally speaking, programming is a difficult task." "That's meow!"
    - "The clouds are nice." "Me-ow!"
    - "That is not correct." "Yes, meow!"
    - "Interesting..." "Why, meow?"
    - "I like it." "Meow?"


PROJECT STATE:
Can handle reversing subject and be, cannot handle reversing verb. It also cannot handle LIKE TO VERB structures (it handles them wrong).
Which means only the first 2 sentence structures have been semi-implemented.
"""

import re
import random

def de_abbreviate_words(words: list) -> list:
    abbr = {
        "i'm": ["i", "am"],
        "you're": ["you", "are"],
        "he's": ["he", "is"],
        "she's": ["she", "is"],
        "it's": ["it", "is"],
        "we're": ["we", "are"],
        "they're": ["they", "are"],
        "what's": ["what", "is"],
        "who's": ["who", "is"],
        "when's": ["when", "is"],
        "where's": ["where", "is"],
        "which's": ["which", "is"],
        "how's": ["how", "is"],
        "why's": ["why", "is"],
        "whatcha": ["what", "are", "you"],
        "whutcha": ["what", "are", "you"],
        "ya": ["you"],
        #  "don't": ["do", "not"],
        "what're": ["what", "are"],
        "im": ["i", "am"],
        "youre": ["you", "are"],
        "hes": ["he", "is"],
        "shes": ["she", "is"],
        "theyre": ["they", "are"],
        "whats": ["what", "is"],
        "whos": ["who", "is"],
        "whens": ["when", "is"],
        "wheres": ["where", "is"],
        "whichs": ["which", "is"],
        "hows": ["how", "is"],
        "whys": ["why", "is"],
        "don't": ["do", "not"],
        "doesn't": ["does", "not"],
        "dont": ["do", "not"],
        "doesnt": ["does", "not"],
    }
    new_words = []
    for word in words:
        if word in abbr.keys():
            new_words.extend(abbr[word])
        else:
            new_words.append(word)
    return new_words

def conjugate_to_third_person(word: str):
    word = word.strip()
    # https://www.englishinterconnect.com/rules-for-3rd-person-singular-s/
    if word == "have":
        return "has"
    elif re.match(r"^\w+(?:s|sh|ch|x|o)$", word, re.IGNORECASE | re.UNICODE):
        return word + "es"
    elif re.match(r"^\w+[bcdfghjklmnpqrstvwxz]y$", word, re.IGNORECASE | re.UNICODE):
        return word.removesuffix("y") + "ies"
    else:
        return word + "s"

def analyze(sentence):
    if sentence == "":
        return "Meow?"

    NOMINATIVE_PRONOUNS = ("i", "you", "he", "she", "it", "we", "they")
    REPLACEMENT_ANSWERS = {
        "what": "meow",
        "who": "Meow",
        "when": "at meow",
        "why": "because of meowing",
        "where": "at Meow",
        "which": "meow",
        "how": "meowly"
    }
    BODGED_RESULT_MEOW = "meow"  # when regex matching and REPLACEMENT_ANSWERS wh-word matching fails, this is the replacement answer
    YES_NO_MEOW_SENTENCE_ENDING = "meow"  # used at the end of yes/no sentences to make them have a meow
    REVERSE_SUBJECT = {  # when given a SUBJ, it spits out REVERSE_SUBJ
        "i": "you",
        "you": "I",  # has to be capitalized, as there is no algorithm for capitalizing I.
    }  # if not in list, use original
    REVERSE_BE_BY_REVERSE_SUBJ = {  # when given REVERSE_SUBJ, it spits out the correct be (which will be used by REVERSE_BE): reverse be matcher
        "I": "am",
        "you": "are"
    }  # this is actually MATCH_BE_TO_REVERSED_SUBJ
    REGEX_FLAGS = re.IGNORECASE | re.UNICODE
    ENQUIRY_TYPE_OPEN_ENDED = "open-ended question"
    ENQUIRY_TYPE_YES_NO_WITH_RAND_ANS = "yes/no question, random answer"
    REGEX = [
        {
            "ID": "WH BE SUBJ C1? LASTGERINF? C2?",
            "regex": re.compile(
                # v0.1.1: r"^(?P<wh>Wh(?:at|o|en|ere|y|ich)|How)\s+(?P<be>am|are|is)\s+(?P<subj>I|you|s?he|it|we|they|this|that|the\s+\S+(?:\s+of\s+(?:the\s+)?\S+)?)(?:(?P<c1>(?:\s+\S+)*(?=\s+\w+ing))?(?P<ing>\s+\w+ing)?(?P<c2>(?:\s+\S+)*)(?<!\?))\??$",
                r"^(?P<wh>Wh(?:at|o|en|ere|y|ich)|How)\s+(?P<be>am|are|is)\s+(?P<subj>I|you|s?he|it|we|they|this|that|the\s+\S+(?:\s+of\s+(?:the\s+)?\S+)?)(?:(?P<c1>(?:\s+\S+)*(?=\s+\w{2,}ing|\s+to\s+\w{2,}))?(?P<lastgerinf>\s+\w{2,}ing|\s+to\s+\w{2,})?(?P<c2>(?:\s+\S+)*)(?<!\?))\??$",
                REGEX_FLAGS
            ),
            "replacement_patterns_per_wh_word_matching": [
                {
                    "wh_words": ["what", "who", "where"],
                    "replacement": "{REVERSE_SUBJ} {REVERSE_BE}{C1}{LASTGERINF} {MEOW}{C2}."
                },
                {
                    "wh_words": ["why", "which", "how", "when"],
                    "replacement": "{REVERSE_SUBJ} {REVERSE_BE}{C1}{LASTGERINF}{C2} {MEOW}."
                }  # lastgerinf is last gerund or infinitive.
            ],
            "type": ENQUIRY_TYPE_OPEN_ENDED
        },
        {
            "ID": "WH DO SUBJ VERB C1?",
            "regex": re.compile(
                # v0.1.1: r"^(?P<wh>Wh(?:at|o|en|ere|y|ich)|How)\s+(?P<do>do(?:es)?)\s+(?P<subj>I|you|s?he|it|we|they|this|that|the\s+\S+(?:\s+of\s+(?:the\s+)?\S+)?)\s+(?P<verb>\w+)(?P<c1>(?:\s+\S+)*)(?<!\?)\??$",
                r"^(?P<wh>Wh(?:at|o|en|ere|y|ich)|How)\s+(?P<do>do(?:es)?)\s+(?P<subj>I|you|s?he|it|we|they|this|that|the\s+\S+(?:\s+of\s+(?:the\s+)?\S+)?)\s+(?P<verbs>\w{2,}(?:\s+\w{2,}ing|\s+to\s+\w{2,})?)(?P<c1>(?:\s+\S+)*)(?<!\?)\??$",
                REGEX_FLAGS
            ),
            "replacement_patterns_per_wh_word_matching": [
                {
                    "wh_words": ["what", "who", "where"],
                    "replacement": "{REVERSE_SUBJ} {MATCHED_VERBS} {MEOW}{C1}."
                },
                {
                    "wh_words": ["why", "which", "how", "when"],
                    "replacement": "{REVERSE_SUBJ} {MATCHED_VERBS}{C1} {MEOW}."
                }
            ],
            "type": ENQUIRY_TYPE_OPEN_ENDED
        },
        {
            "ID": "DO NOT1? SUBJ NOT2? VERB C1? (copy of above without WH)",
            # depending on where the person put not (through the deabbreviator: "don't you like it" turns into "do not you like it" and still has to be detected)
            # (but grammatically "do you not like it" is also correct)
            "regex": re.compile(
                r"^(?P<do>do(?:es)?)(?P<not1>\s+not)?\s+(?P<subj>I|you|s?he|it|we|they|this|that|the\s+\S+(?:\s+of\s+(?:the\s+)?\S+)?)(?P<not2>\s+not)?\s+(?P<verbs>\w{2,}(?:\s+\w{2,}ing|\s+to\s+\w{2,})?)(?P<c1>(?:\s+\S+)*)(?<!\?)\??$",
                REGEX_FLAGS
            ),
            "replacement_patterns_yes_no_question": [
                {
                    "replacement": "Yes, {REVERSE_SUBJ} {DO}{NOT1}{NOT2} {VERBS}{C1}, {MEOW}."
                },
                {
                    "replacement": "No, {REVERSE_SUBJ} {DO}{NOT1}{NOT2} not {VERBS}{C1}, {MEOW}."
                }  # yes this can cause "No, I do not not like it, meow." to be answered
            ],
            "type": ENQUIRY_TYPE_YES_NO_WITH_RAND_ANS
        }
    ]
    PUNCTUATION = ("?", ".", "!", ",", ";")

    sentence = sentence.lower()
    sentence_type = "unknown."  # sentence_type includes the punctuation at the end
    match sentence[-1]:
        case "?":
            sentence_type = "question?"
        case ".":
            sentence_type = "statement."
        case "!":
            sentence_type = "exclamation!"
    for p in PUNCTUATION:
        if sentence.count(p) >= 2 and sentence[-6:].count(p) != sentence.count(p):
            sentence_type = "not one sentence."

    raw_words = sentence
    for to_remove in PUNCTUATION:
        raw_words = raw_words.replace(to_remove, "")
    words = [w.strip() for w in raw_words.split(" ")]
    words = de_abbreviate_words(words)
    raw_sentence = sentence  # if I ever need the original input
    sentence = " ".join(words)

    regex_result = None
    for reg in REGEX:
        res = reg["regex"].match(sentence)
        if res is not None:
            regex_result = [reg, res]

    # BODGED RESULT: HANDLE NO KNOWN REGEX MATCH
    if regex_result is None:
        if sentence_type != "not one sentence.":
            if words[0] in REPLACEMENT_ANSWERS.keys():
                bodged_result = REPLACEMENT_ANSWERS[words[0]] + "."
            else:
                bodged_result = BODGED_RESULT_MEOW
                # add punctuation:
                bodged_result += sentence_type[-1]  # the sentence_type includes the punctuation at the end used for answering bodged_result always
            bodged_result = bodged_result[0].upper() + bodged_result[1:]
        else:  # multi-sentence handling
            # split sentences by PUNCTUATION and just say meow repeatedly to each with the same punctuations
            punctuations_at_positions = {}
            for p in PUNCTUATION:
                i = 0
                while i != -1 and i < len(raw_sentence):
                    i = raw_sentence.find(p, i)
                    if i != -1:
                        punctuations_at_positions[i] = p
                        i += 1  # start after current char (find doesn't throw an error for too high starting index)
            bodged_result = ""
            for i, p in sorted(punctuations_at_positions.items(), key=lambda x: x[0]):
                bodged_result += BODGED_RESULT_MEOW.capitalize() + p + " "
            bodged_result = bodged_result.strip()
        return bodged_result

    # PROPER RESULT: CONSTRUCT ANSWER (WH-, SUBJ AND DO ONLY)
    reg, res = regex_result
    string_substitutions = {}
    # 0. preliminary raw conversion (converts the res.groupdict() to string substitutions raw)
    for name, val in res.groupdict().items():
        string_substitutions["{" + name.upper() + "}"] = val
    # 1. match by wh IF THERE IS ANY and look up a response (which is string replacement/substitution pattern)
    replacement_pattern = None
    meow_answer = None
    if reg["type"] == ENQUIRY_TYPE_OPEN_ENDED:
        if "wh" in res.groupdict().keys():
            wh = res.group("wh")
            for r in reg["replacement_patterns_per_wh_word_matching"]:
                if wh in r["wh_words"]:
                    replacement_pattern = r["replacement"]
                    break
            # 2/a. Meow answer by wh
            for wh_to_test_for, m in REPLACEMENT_ANSWERS.items():
                if wh == wh_to_test_for:
                    meow_answer = m
                    break
    elif reg["type"] == ENQUIRY_TYPE_YES_NO_WITH_RAND_ANS:
        replacement_pattern = random.choice(reg["replacement_patterns_yes_no_question"])["replacement"]
        meow_answer = YES_NO_MEOW_SENTENCE_ENDING
    if replacement_pattern is None:
        return f"Error! Could not find correct replacement pattern for wh-word {wh} for regex match ID: {reg["ID"]}. Continuing execution."
    if meow_answer is None:
        return f"Error! Could not find correct meow answer for wh-word {wh} in REPLACEMENT_ANSWERS. Continuing execution."
    string_substitutions["{MEOW}"] = meow_answer
    # 3. reverse subj and be/verb IF NEEDED (default to not doing anything with them)
    reverse_subject = None
    if "subj" in res.groupdict().keys():
        subj = res.group("subj")
        reverse_subject = subj  # fallback default
        if subj in REVERSE_SUBJECT.keys():
            reverse_subject = REVERSE_SUBJECT[subj]
    reverse_be = None
    if "be" in res.groupdict().keys():
        be = res.group("be")
        reverse_be = be  # fallback default
        if reverse_subject in REVERSE_BE_BY_REVERSE_SUBJ.keys():
            reverse_be = REVERSE_BE_BY_REVERSE_SUBJ[reverse_subject]
    matched_verbs = None  # MATCHED_VERBS is matched to the REVERSE_SUBJECT (and English is simple so only third person is paid attention to)
    if "verbs" in res.groupdict().keys():
        verbs = res.group("verbs")
        matched_verbs = verbs  # fallback output
        if reverse_subject in ("he", "she", "it"):
            l = matched_verbs.split(" ")
            l[0] = conjugate_to_third_person(l[0])
            matched_verbs = " ".join(l)
    if reverse_subject is None:
        reverse_subject = "MISSING_REVERSE_SUBJECT"
    if reverse_be is None:
        reverse_be = "MISSING_REVERSE_BE"
    if matched_verbs is None:
        matched_verbs = "MISSING_MATCHED_VERBS"
    string_substitutions["{REVERSE_SUBJ}"] = reverse_subject
    string_substitutions["{REVERSE_BE}"] = reverse_be
    string_substitutions["{MATCHED_VERBS}"] = matched_verbs
    # 4. SUBSTITUTE TO REPLACEMENT PATTERN
    result = replacement_pattern
    for name, val in string_substitutions.items():
        result = result.replace(name, val if val is not None else "")

    result = result[0].upper() + result[1:]
    return result

STYLING = {  # substitutions are processed in order of listing, so order matters
    "casual": ["lower", {".": "", ",": "", " do not ": " don't ", " does not ": " doesn't ", "i am ": "i'm ", " you are ": " you're "}],
    "nyaa": ["lower", {".": "", ",": "", "meow": "nyaa", "na": "nya", "ne": "nye", "ni": "nyi", "no": "nyo", "nu": "nyu"}],
    "lolcat": ["upper", {".": "", ",": " ",
                         "S": "Z", "BECAUZE": "BECOS", " A ": " ", " THE ": " A ", " LIKE ": " LIEK ", "ER ": "UR ", " YOU ": " U ",
                         "TH ": "F ", "THIN": "FIN", " DO NOT ": " DONT ", "ING": "IN", "?": " PLZ?", "PLEASE": "PLZ",
                         " HAVE ": " HAZ ", " AM ": " IS%% ", " ARE ": " IS%% ", " IS ": " R ", "Y ": "IE ",
                         "%%": ""}]  # source: https://lingojam.com/LOLcatTranslator
    # more substitutions can also be entered later
}
def stylize(result, style):
    if style in STYLING:
        data = STYLING[style]
        if data[0] == "lower":
            stylized = result.lower()
        elif data[0] == "upper":
            stylized = result.upper()
        else:
            stylized = result
        for from_, to in data[1].items():
            stylized = stylized.replace(from_, to)
    else:
        return result
    return stylized

def full_response(in_: str, style: str) -> str:
    return stylize(analyze(in_), style)

def main():
    print(f"=== CGI (Cat Girl Intelligence) {VERSION_} ===")
    print("Type '\\help' for general information AND the accepted sentence types. It's recommended to start with this.\n"
          "Type '\\help commands' to get a list of commands (things starting with '\\').\n"
          "Type '\\help <insert command name here without the '\\'> to get information about a specific command.")
    style = 'grammatical'

    print(f"Current speaking style: {style}. (Use the '\\style' command to change the style.)")
    while True:
        in_ = input("> ")
        args = in_.split(" ")
        command = args[0]
        args.pop(0)  # args are indexed from 0
        if command == "\\help":
            if len(args) >= 1:
                if args[0] == "commands":
                    print("COMMAND LIST\n"
                          "\\help <parameter>\t Prints help messages.\n"
                          "                  \t If no parameter is given, it prints the default help message containing ACCEPTED SENTENCE STRUCTURES.\n"
                          "                  \t If 'command' is written in the parameter, then it prints this list.\n"
                          "                  \t Placing a command's name in the parameter *without the backslash ('\\') will write out the help info for that command, like accepted parameter values.\n"
                          "                  \t (Note: There is no '\\help help'.)\n"
                          "\\style <style name>\t Switches CGI's way of speaking. Default is 'grammatical'. For the list of styles type '\\help style'.\n"
                          "\\exit\t Exits the program.")
                elif args[0] == "style":
                    print("STYLE HELP\n"
                          "CGI can talk in multiple manners.\n"
                          "Sentences are processed normally at first, and then these styles are applied like filters on text.\n"
                          "The default is 'grammatical', which shows the raw processing result.\n"
                          "- grammatical: A more grammatical (to a certain extent) way to talk with attention to punctuation and capitalization.\n"
                          "- casual: Same as grammatical, but everything is in lowercase and there are no full stops or commas used.\n"
                          "- nyaa: Same as casual, but every instance of 'meow' is replaced with 'nyaa' and 'n+vowel' sequences are 'ny+vowel'.\n"
                          "- lolcat: (simplified lolcat) Same as casual, but everything is in UPPERCASE, and certain sequences of characters are replaced\n"
                          "          with homophone sequences which are used by LOLCAT memes. The end result may not be correct in lolspeak, but it's something.")
                elif args[0] == "exit":
                    print("EXIT HELP\n"
                          "Exits the program.\n"
                          "No, I will not tell you what easter eggs exist.\n")
                else:
                    print("Unknown parameter for command '\\help'.")
            else:
                print("** There are multiple commands that can be used.\n"
                      "** Use '\\help commands' for a comprehensive list of commands.\n\n"
                  "There are two grammatical structures supported:\n"
    "- WH-QUESTION BE[CONJUGATED] SUBJECT (COMPLEMENT1) (the last -ING VERB OR last INFINITIVE with to) (COMPLEMENT2) (question mark)\n"
    "- WH-QUESTION DO[CONJUGATED] SUBJECT VERBS[any singular word, conjugating it is not yet implemented + -ing verb or infinitive with to] (COMPLEMENT) (question mark)\n"
    "- DO[CONJUGATED]('NT) SUBJECT (NOT) VERB (COMPLEMENT1) (same as above one, but without WH and with NOT support)"
                  "WH-QUESTIONS supported: what, who, where, why, when, which, how\n"
                  "SUBJECTs supported: all personal pronouns in base form, this, that, the X (of (the) Y)\n"
                  "'Complement' just means that the software will match the rest of the words in that region regardless of their meaning.\n"
                  "Sentences mustn't necessarily end with a question mark.\n\n"
                  "(There can be many cases of incorrect matching to these structures.\n"
                  "In those cases, the output will most likely be incorrect.\n"
                  "But as we are talking about Cat Girl Intelligence, it's not a bug, it's a feature.\n"
                  "Future versions may fix things up gradually.)\n\n"
                  "If the given sentence doesn't match these grammatical structures, then\n"
                  "fallback methods are employed:\n"
                  "1. If the unknown sentence starts with a WH-WORD, then only that word is answered\n"
                  "   and the rest of the words are completely ignored.\n"
                  "2. If that's not the case, but only 1 sentence was given, then it asks back 'Meow' with the same tone as the given sentence\n"
                  "   (so if the original was a question, it asks back 'Meow?').\n\n"
                  "For all cases when there are MULTIPLE SENTENCES detected (using simple punctuation detection), then\n"
                  "all of them get a similar 'Meow' treatment as in described in 2. However, the sentence endings are not tone-matched, but literally punctuation matched\n"
                  "(if you end a sentence with ; it will also ask back 'Meow;').\n"
                  "Again, you could say this is a bug, but it's not a bug, it's a feature.\n\n"
                  "Have fun!\n"
                  "[Note: If you would like to play with a better chatbot akin to this one that doesn't use LLMs, check out the ELIZA program from 1966.]")
        elif command == "\\style":
            if len(args) >= 1:
                style = args[0]
                print(f"Current speaking style: {style}. (If this is not programmed in the stylize() function, then 'grammatical' is used.)")
            else:
                print(f"ERROR: No style given. Please include a valid stylename after the command name. Current speaking style: {style}.")
        elif command == "\\cat":
            print("ENTERING CAT MODE TYPE 'no cat' TO DO NOT THE CAT" + "".join([random.choice("!!!!!!!!!!!!!!!!!!!!!!!!!!1111111111111123456789QWERTZYUIOPAJDNLCM") for i in range(random.randrange(4, 15))]))
            while (__:=input()) != "no cat":
                print(__)
            print("This was the 'cat' command easter egg.")
        elif command == "\\exit":
            print("Exiting.")
            return
        elif command.startswith("\\"):
            print("Unknown command. Type '\\help commands' for a comprehensive list of commands.")
        else:  # ACTUAL RESPONSE
            print(full_response(in_, style))


if __name__ == "__main__":
    main()