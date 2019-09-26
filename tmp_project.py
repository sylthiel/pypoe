def allocate_gems(groups, gems):
	itemgems=[]
	tmp=''
	for group in groups:
		print (len(group), len(gems))
		if(len(group) and len(gems)):
			if (len(gems)>=len(group)):
				tmp=''.join(sorted((gems[:len(group)])))
				gems=gems[len(group):]
				itemgems.append(tmp)
			elif(len(gems) < len(group)):
				itemgems.append(''.join(sorted(gems)))
	return itemgems
gr=["RGGG"]
ge="RGG"
print(allocate_gems(gr, ge))