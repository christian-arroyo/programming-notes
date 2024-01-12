def group_anagrams(strings):
    anagram_groups = {}
    
    for string in strings:
        cannonical = ''.join(sorted(string))
        if cannonical in anagram_groups:
            anagram_groups[cannonical].append(string)
        else:
            anagram_groups[cannonical] = [string]
    return list(anagram_groups.values())


print("1st set:")
print( group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]) )

print("\n2nd set:")
print( group_anagrams(["abc", "cba", "bac", "foo", "bar"]) )