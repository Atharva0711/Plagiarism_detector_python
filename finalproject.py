import math

#clean_text helper function
def clean_text(txt):
    """takes a string of text txt as a parameter and returns a list containing 
    the words in txt after it has been cleaned"""
    #cleaning all punctuation symbols
    for symbol in """.,?"'!;:""":
        txt = txt.replace(symbol, '')
    #making lowercase and splitting every word into list
    txt = txt.lower()
    words = txt.split()
    return words

#stem helper function
def stem(s):
    """returns the stem of a string s"""
    if len(s) > 3:
        #ending 'es'
        if s[-2:] == 'es':
            s = s[:-2]
        #plural 's'
        if s[-1] == 's':
            s = s[:-1]
        #ending y
        if s[-1] == 'y':
            s = s[:-1] + 'i'
        #ending 'er'
        elif s[-2:] == 'er':
            s = s[:-2]
       #plural 'ers'
        elif s[-3:] == 'ers':
            s = s[:-3]
        #ending 'ing'
        elif s[-3:] == 'ing':
            s = s[:-3]
        #ending 'ly'
        elif s[-2:] == 'ly':
            s = s[:-2]
        #ending 'ful'
        elif s[-3:] == 'ful':
            s = s[:-3]
        #ending 'able' or 'ible'
        elif s[-4:] == 'able' or s[-4:] == 'ible':
            s = s[:-4]
    return s
     
def compare_dictionaries(d1, d2):
    """takes two feature dictionaries d1 and d2 as inputs and returns their 
    log similarity score"""
    if d1 == {}:
        return -50
    else:
        score = 0
        total = sum(d1[vals] for vals in d1)
        for i in d2:
            if i not in d1:
                score += d2[i] * math.log(0.5/total)
            else:
                score += d2[i] * math.log(d1[i]/total)
        return round(score, 5)


#Text model class
class TextModel:
    
    def __init__(self, model_name):
        """constructs a new TextModel object"""
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.punctuations = {}  #chosen feature: punctuation count
        
    def __repr__(self):
        """Return a string representation of the TextModel"""
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of punctuation marks: ' + str(len(self.punctuations))
        return s
    
    def add_string(self, s):
        """adds a string of text s to the model by augmenting the feature 
        dictionaries defined in the constructor"""
        word_list = clean_text(s)
        #updating words dictionary 
        for w in word_list:
            if w not in self.words:
                self.words[w] = 0
            self.words[w] += 1
        #updating word_lengths dictionary
        for l in word_list:
            if len(l) not in self.word_lengths:
                self.word_lengths[len(l)] = 0
            self.word_lengths[len(l)] += 1
        #updating word stems dictionary
        for i in word_list:
            if stem(i) in self.stems:
                self.stems[stem(i)] += 1 
            else:
                self.stems[stem(i)] = 1
        #updating sentence lengths dictionary
        s_ = s.split()
        index_last = 0
        for i in range(len(s_)):
            if s_[i][-1] in '?!.':
                if (i + 1 - index_last) not in self.sentence_lengths:
                    self.sentence_lengths[(i + 1) + - index_last] = 1
                else:
                    self.sentence_lengths[(i + 1) + - index_last] += 1
                index_last = i + 1
        #updating punctuations dictionary
        for p in s:
            if p in '?.!':
                if p not in self.punctuations:
                    self.punctuations[p] = 0
                self.punctuations[p] += 1
        
    def add_file(self, filename):
        """adds all of the text in the file identified by filename to the model"""
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        text = f.read()
        self.add_string(text)
    
    def save_model(self):
        """saves the TextModel object self by writing its various feature 
        dictionaries to files"""
        filename = self.name + '_words'
        f_w = open(filename, 'w')      
        f_w.write(str(self.words))              
        f_w.close()

        filename = self.name + '_word_lengths'
        f_wl = open(filename, 'w')      
        f_wl.write(str(self.word_lengths))              
        f_wl.close()

        filename = self.name + '_stems'
        f_s = open(filename, 'w')      
        f_s.write(str(self.stems))              
        f_s.close()

        filename = self.name + '_sentence_lengths'
        f_sl = open(filename, 'w')      
        f_sl.write(str(self.sentence_lengths))              
        f_sl.close()

        filename = self.name + '_punctuations'
        f_p = open(filename, 'w')      
        f_p.write(str(self.punctuations))              
        f_p.close()
    
    
    def read_model(self):
        """reads the stored dictionaries for the called TextModel object from 
        their files and assigns them to the attributes of the called TextModel"""
        filename = self.name + '_words'
        f_w = open(filename, 'r')    
        d_str_w = f_w.read()          
        f_w.close()
        d_w = dict(eval(d_str_w))      
        self.words = d_w

        filename = self.name + '_word_lengths'
        f_word_lengths = open(filename, 'r')
        d_str_wl = f_word_lengths.read()
        f_word_lengths.close()
        d_word_lengths = dict(eval(d_str_wl))
        self.word_lengths = d_word_lengths

        filename = self.name +'_stems'
        f_s = open(filename, 'r')
        d_str_s = f_s.read()
        f_s.close()
        d_s = dict(eval(d_str_s))
        self.stems = d_s

        filename = self.name + '_sentence_lengths'
        f_sl = open(filename, 'r')
        d_str_sl = f_sl.read()
        f_sl.close()
        d_sl = dict(eval(d_str_sl))
        self.sentence_lengths = d_sl

        filename = self.name + '_punctuations'
        f_p = open(filename, 'r')
        d_str_p = f_p.read()
        f_p.close()
        d_p = dict(eval(d_str_p))
        self.punctuations = d_p
        
    
    def similarity_scores(self, other):
        """computes and returns a list of log similarity scores measuring the 
        similarity of self and other"""
        words_score = compare_dictionaries(other.words, self.words)
        word_lengths_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        stems_score = compare_dictionaries(other.stems, self.stems)
        sentence_lengths_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        punctuations_score = compare_dictionaries(other.punctuations, self.punctuations)
        return [words_score, word_lengths_score, stems_score, sentence_lengths_score, punctuations_score]
    
    def classify(self, source1, source2):
        """compares the called TextModel object (self) to source1 and source2 
        and determines which of these other TextModels is the more likely 
        source of the called TextModel"""
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        print('scores for source1: ', scores1)
        print('scores for source2: ', scores2)
        
        weighted_sum1 = 15*scores1[0] + 10*scores1[1] + 7*scores1[2] + 5*scores1[3] + 3*scores1[4]
        weighted_sum2 = 15*scores2[0] + 10*scores2[1] + 7*scores2[2] + 5*scores2[3] + 3*scores2[4]
        if weighted_sum1 > weighted_sum2:
            print(self.name + ' is more likely to have come from ' + source1.name)
        else:
            print(self.name + ' is more likely to have come from ' + source2.name)
            

def run_tests():
    """runs the tests for the program"""
    source1 = TextModel('Gandhi')
    source1.add_file('Gandhi Speech.txt')

    source2 = TextModel('Martin_Luther')
    source2.add_file('MLK Speech.txt')

    new1 = TextModel('WR120')
    new1.add_file('WR120_Essay.txt')
    new1.classify(source1, source2)
        
    source1_new = TextModel('Gandhi New')
    source1_new.add_file('Extract_M.txt')
    source2_new = TextModel('MLK New')
    source2_new.add_file('Extract_K.txt')
    
    new_2 = TextModel('Pr0')
    new_2.add_file('pr0.txt')
    new_2.classify(source1_new, source2_new)
    
    

        
        
        
    
