import heapq
def foo():
    '''
    num_ppl = int(input())
    p_to_song = dict()
    for p in range(1, num_ppl + 1):
        p_to_song[p] = set()
    cur_song = ord('1')
    for i in range(int(input())):
        # print('> night: ', i)
        line = list(map(int, input().split()))
        p_tonignt = line[1:]
        # print('ppl: ', p_tonignt)
        if 1 in p_tonignt:
            # print('>> bard presents')
            for p in p_tonignt:
                # print('teach p', p)
                p_to_song[p].add(chr(cur_song))
                # print('p', p, 'knows', p_to_song[p])
            cur_song += 1
        else:
            # print('>> share')
            total = set()
            for p in p_tonignt:
                # print('p', p, 'teaches', p_to_song[p])
                total = total.union(p_to_song[p])
            for p in p_tonignt:
                p_to_song[p] = total.copy()
    
    res = [i+1 for i in range(num_ppl) if len(p_to_song[i+1]) == int(chr(cur_song-1))]
    res = sorted(res)
    for p in res:
        print(p)
    '''
    pass

foo()
