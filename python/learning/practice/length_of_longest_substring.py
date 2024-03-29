class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        longest = counter = 0
        hash_set = set()
        print(len(s))
        for i in range(len(s)):
            if s[i] not in hash_set:
                hash_set.add(s[i])
                counter += 1
                if counter > longest:
                    longest = counter
            else:
                if counter > longest:
                    longest = counter
                counter = 1
                hash_set = set()
                hash_set.add(s[i])
        return longest

test = " "
s = Solution()
print(s.lengthOfLongestSubstring(test))
