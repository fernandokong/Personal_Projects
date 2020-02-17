def compareTime(time1,time2): #O(m)
	hour1, minute1 = time1.split(':')
	hour2, minute2 = time2.split(':')
		
	time1 = int(hour1)*60 + int(minute1)
	time2 = int(hour2)*60 + int(minute2)
	
	if time1 > time2: #greater than
		return 1
	elif time1 == time2: #equal
		return 0
	else: #less than
		return -1

def chooseBound (p1B,p2B,result): #choose upper or lower bound, O(m)
	if compareTime(p1B, p2B) == result:
		return p1B
	else:
		return p2B

def diffBetween (time1, time2): #O(m)
	hour1, minute1 = time1.split(':')
	hour2, minute2 = time2.split(':')
	
	time1 = int(hour1)*60 + int(minute1)
	time2 = int(hour2)*60 + int(minute2)
	
	return time1-time2

def equalStart(booked_times, p1, p2, end1,end2): #compute edge case when starts are equal, O(m)
	if compareTime(end2,end1) == 1:
		booked_times[p1][1] = end2
	booked_times[p2] = ['empty','empty']

def addLeftovers(pS, p, booked_times): #O(n)
	while p < len(pS):
		booked_times.append(pS[p])
		p += 1

def availTime(p1S,p2S,p1B,p2B,duration): #O(n+m)
	booked_times = []
	avail_times = []
	
	#merge into one list of non-availabilities O(n)
	p1 = 0;
	p2 = 0;
	while p1 < len(p1S) and p2 < len(p2S):
		if compareTime(p1S[p1][0], p2S[p2][0]) == -1:
			booked_times.append(p1S[p1])
			p1 += 1
		else:
			booked_times.append(p2S[p2])
			p2 += 1
	
	#add leftover non-availabilities O(n)
	addLeftovers(p1S,p1,booked_times) 
	addLeftovers(p2S,p2,booked_times) 
	
	#merge non-availabilities together if they overlap
	p1 = 0
	p2 = 1
	for i in range (len(booked_times)-1): #O(n)
		start1 = booked_times[p1][0]
		end1 = booked_times[p1][1]
		start2 = booked_times[p2][0]
		end2 = booked_times[p2][1]
				
		if start2 != 'empty' and compareTime(end1,start2) == 1: #merge if end1 greater than start2
			if compareTime(start1,start2) == 0: #edge case if both start times are equal
				equalStart(booked_times,p1,p2,end1,end2)					
			else:
				booked_times[p1] = [start1,end2] #normal case when both start times are different
				booked_times[p2] = ['empty','empty'] #leave empty, consolidate later
		else:
			p1 = p2
		p2 += 1
		
	#check merged list
	#print (booked_times)
			
	#choose bounds, O(m)
	lBound = chooseBound(p1B[0],p2B[0], 1)
	hBound = chooseBound(p1B[1],p2B[1], -1)
	
	#check bounds
	#print (lBound)
	#print (hBound)
	
	#add lower bound, O(m)
	if compareTime(booked_times[0][0], lBound) == 1:
		if diffBetween(booked_times[0][0], lBound) >= duration:
			avail_times.append([lBound, booked_times[0][0]])
	
	#check output list
	#print (avail_times)
	
	#add from unavailability list, O(n)
	p1 = 0;
	p2 = 1;
	for i in range (len(booked_times)-1):	
		end1 = booked_times[p1][1]
		start2 = booked_times[p2][0]
		
		if (start2 != 'empty'):
			if diffBetween(start2, end1) >= duration:
				avail_times.append([end1,start2])
			p1 = p2
		p2 += 1
		
	#check output list
	#print (avail_times)
	
	#add upper bound, O(n)
	pEnd = len(booked_times)-1 #pointer to the ending element
	while booked_times[pEnd][0] == 'empty' and pEnd != 0: #find the last element which is not empty
		pEnd -= 1
		
	if compareTime(hBound, booked_times[pEnd][1]) == 1:
		if diffBetween(hBound, booked_times[pEnd][1]) >= duration:
			avail_times.append([booked_times[pEnd][1], hBound])
	
	return avail_times

p1Schedule = [['9:00','10:30'],['12:00','13:00'],['16:00','18:00']]
p2Schedule = [['10:00','11:30'],['12:30','14:30'],['14:30','15:00'],['16:00','17:00']]
p1Bound = ['9:00','20:00']
p2Bound = ['10:00','18:30']
meetingDuration = 30;
print(availTime(p1Schedule,p2Schedule,p1Bound,p2Bound,meetingDuration))
