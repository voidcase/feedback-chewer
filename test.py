import wordset

def test_wordset():
    data = [
        {
            'a': 'I hate bees!',
            'b': 'Stop, hammer time'
        },
        {
            'a': 'Ceilings are fun',
            'b': 'Grass. tastes. bad.'
        }
    ]
    s = wordset.build_wordset(dataset=data,text_fields=['a','b'])
    assert(s == {'i','hate','bees','stop','hammer','time','ceilings','are','fun','grass','tastes','bad'})

if __name__ == '__main__':
    test_wordset()
    print('done!')