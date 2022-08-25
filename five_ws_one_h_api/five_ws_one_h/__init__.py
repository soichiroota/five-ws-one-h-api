import unidic2ud.cabocha as CaboCha
from pyknp import KNP
import re


def main(text):
    When = []
    Where = []
    What = []
    Why = []
    Who = []
    How = []
    c = CaboCha.Parser()

    words = []
    poss = []
    chunkId = []
    toId = []
    ID = -1
    scores = []
    howId = []


    nani = ['は','が','を','の'] # Whatの後に続く助詞
    naze =['だから', 'それで', 'そのため', 'このため', 'そこで', 'したがって', 'ゆえに', 'それゆえに','から','んで','ため']# Whyの後に続く接続助詞


    tree =  c.parse(text)
    knp = KNP(option='-tab')     # Default is JUMAN++. If you use JUMAN, use KNP(jumanpp=False)
    result = knp.parse(text)

    for i in range(0, tree.size()):
        token = tree.token(i)
        # 単語を取得
        word = token.surface
        words.append(word) # 文字をスタック
        # 品詞を取得
        pos = token.feature.split(",")
        poss.append(pos) # 品詞をスタック
        #チャンクIDを取得
        if token.chunk != None:
                ID += 1
        chunkId.append(ID)
        # かかり先IDを取得
        if token.chunk != None:
            ID2 = token.chunk.link

        toId.append(ID2)
            # スコアを取得
        if token.chunk != None:
            score  = token.chunk.score
        scores.append(score)


    for mrph in result.mrph_list(): # 各形態素へのアクセス

        so_f = re.split("[-:]", mrph.imis) # feature分割

        if mrph.bunrui == '地名' or '場所' in so_f:
            Where.append(mrph.midasi)

        elif '人' in so_f or '人名' in so_f or mrph.bunrui == '人名':
            Who.append(mrph.midasi)

    for bnst in result.bnst_list(): # 各文節へのアクセス2
        setu_f = re.split("[><]", bnst.fstring)
        del setu_f[::2]
        if '時間' in setu_f:
            When.append("".join(mrph.midasi for mrph in bnst.mrph_list()))

    num = len(words)-1
    while num > -1:

    ##Why##
        for c in naze:
            if words[num] == c: #続く助詞がWhyの後に続くものの場合
                Why.append(words[num])
                nowId = chunkId[num] # 最初のチャンクIDを保存

                while num>0:

                    if chunkId[num-1] != nowId and toId[num-1] > nowId and words[num-1] != '(': #今のチャンクIdが最初のIdでなく, かかり先Idが最初のId出ない
                        break
                    num -=1
                    Why.insert(0,words[num])

        if words[num] == 'に' and words[num-1] == 'ため':
            words.insert(num,'Why)')
            nowId = chunkId[num] # 最初のチャンクIDを保存

            while num>0:

                if chunkId[num-1] != nowId and toId[num-1] > nowId and words[num-1] != '(': #今のチャンクIdが最初のIdでなく, かかり先Idが最初のId出ない
                    break

                num -=1

    ####


    ##How##
            """
            if toId[num] == -1:
                while num > 0:
                    How.insert(0, words[num])
                    howId.append(chunkId[num])
                    if (poss[num][0] =='名詞' and poss[num][1] != '非自立' and poss[num][1] != '接尾' and poss[num-1][6] != 'という'):
                        break
                    num -= 1
            """
        elif toId[num] == -1:
            w = []
            w.insert(0, words[num])
            howId.append(chunkId[num])
            num -= 1
            while num > -1:
                if poss[num][0] =='助詞':
                    break
                w.insert(0,words[num])
                howId.append(chunkId[num])
                num -=1

            How.insert(0, ''.join(w))
            w = []
    ####


    ##What##
            """
            for c in nani:
                if poss[num][0] == '助詞' and words[num] == c and toId[num] in howId: #続く助詞がWhatの後に続くものの場合1
                    while num > 0:
                        num -= 1
                        What.insert(0, words[num])
                        if (poss[num][0] =='名詞' and poss[num][1] != '非自立' and poss[num][1] != '接尾') or (poss[num][1] == '自立'  and poss[num][6] != 'する' and poss[num][6] != 'なる'):
                            break


        #            num += 1
            """
        elif toId[num] in howId and (poss[num][1] == '係助詞' or poss[num][1] == '格助詞') and (words[num] in nani): 
            w = []
            w.insert(0,words[num])
            whatId = chunkId[num]
            num -= 1
            while chunkId[num] == chunkId[num-1]:
                w.insert(0, words[num])
                num -= 1

            w.insert(0, words[num])
            What.insert(0,''.join(w))
            w = []
    ####
        else:
            num -= 1

    print('Who:%s' %(Who))
    print('Where:%s' %(Where))
    print('When:%s' %(When))
    print('What:%s' %(What))
    print('How:%s' %("".join(How)))
    return dict(
        who=Who,
        where=Where,
        when=When,
        what=What,
        how=How
    )