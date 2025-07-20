class Solution(object):
    def kthCharacter(self, k, operations):
        """
        :type k: int
        :type operations: List[int]
        :rtype: str
        """
        word ="a"
        idd=0
        while len(word)<k and idd<len(operations):
                if operations[idd] == 0:
                    word+=word
                    
                elif operations[idd] == 1:
                    new=''.join('a' if c=='z' else chr(ord(c)+1)
                    for c in word)
                    word+=new
                idd +=1
        return word[k-1]

sol= Solution()

s= sol.kthCharacter(9499052,[0,0,0,1,1,0,1,1,1,0,1,0,1,1,1,0,0,1,1,1,0,0,0,1,1])
print(s)