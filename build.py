from pandas import DataFrame
from py2neo import Graph, Node, Relationship, NodeMatcher
import pandas as pd

# MATCH p=(m)-[]->(n) WHERE m.`股票名称`='N龙芯' or n.`股票名称`='N龙芯' return p
# MATCH p=(m)-[]->(n) WHERE m.`股票名称`='海陆重工' or n.`股票名称`='海陆重工' return p
# MATCH p=(m)-[]->(n) WHERE m.`股票名称`='深 赛 格' or n.`股票名称`='深 赛 格' return p
# MATCH p=(m)-[]->(n) WHERE m.`股票名称`='飞荣达' or n.`股票名称`='飞荣达' return p
# MATCH p=(m)-[]->(n) WHERE m.`股票名称`='丰元股份' or n.`股票名称`='丰元股份' return p
graph = Graph('http://localhost:7474/db/data/',
              auth=("neo4j", "xxxxxxxxxxxxxxxxxxxxxxxxxx"))

graph.run('MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r')

stock = pd.read_csv('stock_basic.csv', encoding="UTF-8")
holder = pd.read_csv('stock_holders.csv', encoding="UTF-8")
concept = pd.read_csv('stock_concept.csv', encoding="UTF-8")
type = pd.read_csv('stock_type.csv', encoding="UTF-8")
announcements = pd.read_csv('stock_announcements.csv', encoding="UTF-8")

stock["行业"] = stock["行业"].fillna("未知")
holder = holder.drop_duplicates(inplace=False)

for i in stock.values:
    a = Node('股票', TS代码=i[0], 股票名称=i[2], 行业=i[3])
    print('TS代码:'+str(i[0]), '股票名称:'+str(i[2]), '行业:'+str(i[3]))
    graph.create(a)

for i in holder.values:
    a = Node('股东', TS代码=i[0], 股东名称=i[1], 持有数量=i[2], 持股占比=i[3])
    graph.create(a)

concept_list = []
for i in concept.values:
    if i[0] in concept_list:
        continue
    concept_list.append(i[0])
    a = Node('概念', 编号=i[0], 概念=i[1])
    graph.create(a)

for i in announcements.values:
    a = Node('公告', TS代码=i[0], 公告标题=i[1], 发布日期=i[2])
    graph.create(a)

a = Node("深股通", 名称="深股通")
graph.create(a)
a = Node("沪股通", 名称="沪股通")
graph.create(a)

pre = 0
matcher = NodeMatcher(graph)
for i in holder.values:
    if i[0] == pre:
        continue
    a = matcher.match("股票", TS代码=i[0]).first()
    b = matcher.match("股东", TS代码=i[0])
    for j in b:
        r = Relationship(j, '参股', a)
        graph.create(r)
    pre = i[0]

for i in type.values:
    a = matcher.match("深股通", 名称="深股通").first()
    b = matcher.match("沪股通", 名称="沪股通").first()
    c = matcher.match("股票", TS代码=i[0]).first()
    if i[1] == 'SZ':
        r = Relationship(c, '成分股属于', a)
    else:
        r = Relationship(c, '成分股属于', b)
    graph.create(r)

for i in concept.values:
    a = matcher.match("股票", TS代码=i[2]).first()
    b = matcher.match("概念", 编号=i[0]).first()
    r = Relationship(b, '概念属于', a)
    graph.create(r)

pre = 0
for i in announcements.values:
    if i[0] == pre:
        continue
    a = matcher.match("股票", TS代码=i[0]).first()
    b = matcher.match("公告", TS代码=i[0])
    for j in b:
        r = Relationship(a, '发布公告', j)
        graph.create(r)
    pre = i[0]
