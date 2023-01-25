import parsedatetime
import re
import datetime
import nltk
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import state_union
import spacy
import en_core_web_sm
from spacy.matcher import Matcher
# nltk.download('state_union')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

def time_final(content):
#Below is a python function that takes an input string and prints date and time extracted from it using the regular expression patterns
    s=content
    def date_time_extract(s):
        #1-Jan-2018
        pattern1 = r'((?:\d{1,2}[- ,./]*)(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[- ,./]*\d{4})'
        #1-jan-2018
        pattern2 = r'((?:\d{1,2}[- ,./]*)(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*[- ,./]*\d{4})'
        #1-jan-18
        pattern3= r'((?:\d{1,2}[- ,./]*)(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*[- ,./]*\d{2})'
        #1-Jan-18
        pattern4 = r'((?:\d{1,2}[- ,./]*)(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[- ,./]*\d{2})'
        # 1 st jan 2018
        pattern5=r'((?:\d{1,2}[- ,./]*)(?:st|st of|th|of|th of )[a-z]*[- ,./]*(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*[- ,./]*\d{4})'
        # 1 st  of Jan
        pattern6=r'((?:\d{1,2}[- ,./]*)(?:th|st|st of|of|th of )[a-z]*[- ,./]*(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[- ,./]*\d{4})'
        #dd/mm/yyyy
        pattern7=r'((?:\d{1,2}[- ,./]*)(?:\d{1,2}[- ,./]*)[- ,./]*\d{4})'

        #time
        pattern8=r'([01]?[0-9][:.][0-9]{2}?\s?[ap]m)'

        pattern=pattern1+"|"+pattern2+"|"+pattern3+"|"+ pattern4+"|"+pattern5+"|"+pattern6+"|"+pattern7+"|"+pattern8



        mydate=re.compile(pattern)
        mydate=mydate.findall(s,re.I)


        for match in mydate:
            for item in match:
                if item!='':
                    return(item)
    def time_extract(s):
        pattern8=r'([01]?[0-9][:.][0-9]{2}?\s?[ap]m)'


        pattern=pattern8
        mydate=re.compile(pattern)
        mydate=mydate.findall(s,re.IGNORECASE)


        for match in mydate:

            return(match)


    y=date_time_extract(s)

    if (y==None):
        cal = parsedatetime.Calendar()
        date_timestruct=cal.parse(s)
        temp=list(date_timestruct)
        res=temp[0]
        year=str(res.tm_year)
        month=str(res.tm_mon)
        day=str(res.tm_mday)
        hour=str(res.tm_hour)
        minute=str(res.tm_min)
        sec=str(res.tm_sec)

        return((month+"-"+day+"-"+year+'   '+hour+":"+ minute + ":" + sec))


    else:
        print(y)
        print(time_extract(s))
        return y+'   '+(time_extract(s))


def process_content(content):
        s=content
        train_text = state_union.raw("2005-GWBush.txt")
        custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
        tokenized = custom_sent_tokenizer.tokenize(s)
        i=(tokenized[0])
        words=nltk.word_tokenize(i)
        ref=["mrs","mr","miss", "with", 'hi']+['a', 'an', 'the', 'and', 'it', 'for', 'or', 'but', 'in', 'my', 'your', 'our', 'their']
        for a in words :
            if a.lower() in ref:
                no=words.index(a)
                del words[no]
        tagged = nltk.pos_tag(words)
        chunkGram = r"""NP: {(<DT>?<JJ>*(<NN>|<NNS>|<NNP>)+<JJ>*<C.>*<IN>*<TO>*(<PRP>|<PRP.>)*<RB.>*)*}
                        """
        chunkParser = nltk.RegexpParser(chunkGram)
        chunked = chunkParser.parse(tagged)
        def filt(x):
            return x.label()=='NP'

        for subtree in chunked.subtrees(filter =  filt):
             n= (len(subtree))
             a=list((subtree[n-1]))
             if ((a[1]) == "IN"):
                 remove=True
             else :
                 remove=False
             output=' '.join([w for w, t in subtree.leaves()])
             if remove:
                 output=output.rsplit(' ', 1)[0]
             return(output)
             break

# def main():
#     s = input()
#     print(time_final(s))
#     print(process_content(s))

# if __name__ == '__main__':
#     main()









