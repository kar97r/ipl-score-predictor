import random
import pandas
import glob


def search_batsman_cluster(player_name):
        for i in glob.glob('../clusters_batsmen/*'):
                player_list=pandas.DataFrame.from_csv(i).index.tolist()
                if player_name in player_list:
                        return i.split('/')[2].split("cluster")[1]

def search_bowler_cluster(player_name):
        for i in glob.glob('../clusters_bowlers/*'):
                player_list=pandas.DataFrame.from_csv(i).index.tolist()
                if player_name in player_list:
                        return i.split('/')[2].split("cluster")[1]

#def find_clustervscluster(batsman_cluster,bowler_cluster):
	
def prob_list(cluster_name):
	df=pandas.DataFrame.from_csv("../clusters_probability.csv")
	for i in df.iterrows():
		if cluster_name == i[0]:
			return list(i[1]) 
def findOutput(batsmanName,bowlerName):
	batsman_cluster=search_batsman_cluster(batsmanName)
	bowler_cluster=search_bowler_cluster(bowlerName)
#	p=find_clustervscluster(batsman_cluster,bowler_cluster) #input from csv
#.	p=list(map(float,input().split()))
	p=prob_list("%svs%s"%(batsman_cluster,bowler_cluster))
	global wicket_prob	
	wicket_prob=p[7]
	global notout_probability
	notout_probability=1-wicket_prob
		
	del p[7]
	t=[]
	k=0
	tot=int(sum(p)*100)
	d={}
	start_ind=0
	for i in range(len(p)):
		d[i]=list(range(start_ind,start_ind+int(p[i]*100)))
		start_ind=start_ind+int(p[i]*100)		
	j=random.randint(0,tot-2)
	for k in d.keys():
		if j in d[k]:
			return k

def squad(team_code):
	print("Select playing eleven in their batting order")
	players_list=glob.glob('../p2p/%s/*.csv'%team_code)
	players_list=list(map(lambda x: x.split('/')[3].split(".csv")[0],players_list))
	count=0
	for i in players_list:
		print(count,i)
		count+=1
	l=[]
	for i in range(11):
		l.append(players_list[int(input())])
	return l



#Team Input
team1_name=input("Enter the first team of the match: ")
team2_name=input("Enter the second team of the match: ")
team1=(squad(team1_name))
team2=(squad(team2_name))
print("Enter the bowlers for "+team1_name)
for nm in range(11):
	print(nm,team1[nm])
temp1_bowlers=list(map(int,input().split()))
team1_bowlers={}
for nm in range(len(temp1_bowlers)):
	team1_bowlers[team1[temp1_bowlers[nm]]]=4
print("Enter the  bowlers for "+team2_name)
for nm in range(11):
        print(nm,team2[nm])
temp2_bowlers=list(map(int,input().split()))
team2_bowlers={}
for o in range(len(temp2_bowlers)):
	team2_bowlers[team2[temp2_bowlers[o]]]=4
striker=team1[0]
non_striker=team1[1]
next_down=2
cur_run=0
total_score=0
wicket_prob=0
notout_probability1=1-wicket_prob
notout_probability2=1-wicket_prob


def next_batsman(balls):
	global striker
	global non_striker
	global notout_probability1
	global notout_probability2
	if cur_run%2==1 and balls!=0:
		striker,non_striker=non_striker,striker
		notout_probability1,notout_probability2=notout_probability2,notout_probability1
	elif cur_run%2==0 and balls==0:
		striker,non_striker=non_striker,striker
		notout_probability1,notout_probability2=notout_probability2,notout_probability1
	return striker


def next_bowler():
	r=random.choice(list(team2_bowlers.keys()))
	team2_bowlers[r]-=1
	return r
def next_team1_bowler():
	r=random.choice(list(team1_bowlers.keys()))
	team1_bowlers[r]-=1
	return r













for loop1 in range(20):
	nxt_bowler=next_bowler()
	if team2_bowlers[nxt_bowler]==0:
		del team2_bowlers[nxt_bowler]
	for loop2 in range(6):
		if next_down==10:
			print("All out!")
			break			
		striker=next_batsman(loop2)
		print("Ball: %s.%s"%(loop1,loop2+1))
		print("Batsman: "+striker)
		print("Bowler: "+nxt_bowler)
		print("Non striker: "+non_striker)		
		notout_probability1*=(1-wicket_prob)
		if notout_probability1<0.4 and next_down!=10:
			striker=team1[next_down]
			next_down+=1
			cur_run=0
			notout_probability1=1-wicket_prob
			print("Out!")
		else:
			cur_run=findOutput(striker,nxt_bowler)
			total_score+=cur_run
			print("Ball score:"+str(cur_run))
		print("Total Score:"+str(total_score)+"/"+str(next_down-2))
		print("-"*50)
print("First innings score:"+str(total_score))
print("-"*50)
print("-"*50)
target=total_score


striker=team2[0]
non_striker=team2[1]
next_down=2
cur_run=0
total_score=0
wicket_prob=0
notout_probability1=1-wicket_prob
notout_probability2=1-wicket_prob
flag=0
for loop1 in range(20):
	nxt_bowler=next_team1_bowler()
	if team1_bowlers[nxt_bowler]==0:
		del team1_bowlers[nxt_bowler]
	for loop2 in range(6):
		if flag:
			print("All out!")
			break
		elif total_score>target:
			flag=1
			break
		striker=next_batsman(loop2)
		print("Ball: %s.%s"%(loop1,loop2+1))
		print("Batsman: "+striker)
		print("Bowler: "+nxt_bowler)
		print("Non striker: "+non_striker)		
		notout_probability1*=(1-wicket_prob)
		if notout_probability1<0.4 and next_down!=11:
			striker=team2[next_down]
			next_down+=1
			cur_run=0
			notout_probability1=1-wicket_prob
			print("Out!")
		elif notout_probability1<0.4 and next_down==11:
			print("Out!")
			next_down+=1
			
			flag=1
		else:
			cur_run=findOutput(striker,nxt_bowler)
			total_score+=cur_run
			print("Ball score:"+str(cur_run))
		print("Total Score:"+str(total_score)+"/"+str(next_down-2))
		print("Target: "+str(target))
		print("-"*50)
	if flag==1:
		break
print("Second innings score:"+str(total_score)+"/"+str(next_down-2))
print("-"*50)
print("-"*50)
if(total_score>target):
	print("%s won against %s by %s wickets"%(team2_name,team1_name,str(12-next_down)))
elif total_score<target:
	print("%s won against %s by %s runs"%(team1_name,team2_name,str(target-total_score)))
else:
	print("Draw!")
