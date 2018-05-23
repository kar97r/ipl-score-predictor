import pandas
import glob


def search_team(player_name):
	for i in glob.glob('../p2p/*'):
		for j in glob.glob('%s/*'%i):
			j=j.split('/')
			if j[len(j)-1].split('.')[0]==player_name:
				return i.split('/')[2]
def cluster_prob():
	for i in glob.glob('../clusters_batsmen/*'):
		for j in glob.glob('../clusters_bowlers/*'):
			df={"0":[0],"1":[0],"2":[0],"3":[0],"4":[0],"5":[0],"6":[0],"wickets":[0]}
			batsmen=pandas.DataFrame.from_csv(i).index.tolist()
			bowlers=pandas.DataFrame.from_csv(j).index.tolist()
			for u in batsmen:
				for v in bowlers:
					if v in pandas.DataFrame.from_csv("../p2p/%s/%s.csv"%(search_team(u),u)).index.tolist():
						p2p=pandas.DataFrame.from_csv("../p2p/%s/%s.csv"%(search_team(u),u))
#						print(p2p,u,v,p2p["Z Khan"])
						df["0"][0]+=p2p["0"][v]
						df["1"][0]+=p2p["1"][v]
						df["2"][0]+=p2p["2"][v]
						df["3"][0]+=p2p["3"][v]
						df["4"][0]+=p2p["4"][v]
						df["5"][0]+=p2p["5"][v]
						df["6"][0]+=p2p["6"][v]
						df["wickets"][0]+=p2p["Dismissal"][v]
			cprob=pandas.DataFrame.from_csv("../clusters_prob.csv")
			cprob=cprob.append(pandas.DataFrame(df,index=["%svs%s"%(i.split('/')[2].split('cluster')[1],j.split('/')[2].split('cluster')[1])]))
			cprob=cprob.to_csv("../clusters_prob.csv")
cluster_prob()
