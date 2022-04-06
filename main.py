from math import log, factorial
from itertools import combinations


def dfs_edit(	matrix, 
				start, 
				last_nodes,
				global_paths, local_path, 
				visited=None):
	if visited is None: 
		visited = [True]*len(matrix)

	if start in last_nodes:
		global_paths.append([i for i in local_path])
	
	visited[start] = False
	for col in range(len(matrix[start])):
		if matrix[start][col] == 1 and visited[col]:
			local_path.append(col)
			dfs_edit(matrix, col, last_nodes, global_paths, local_path, visited)
			local_path.remove(col)
	visited[start] = True
	return visited


def count_paths(matrix, paths, prob_arr):
	res = []
	for i in paths:
		t = 1
		universal = list(range(len(matrix)))
		for j in i:
			t *= prob_arr[j]
			universal.remove(j)
		for j in universal:
			t *= 1 - prob_arr[j]
		res.append(t)
	return res


# 4 v
#		 1  2  3  4  5  6  7  8  9
mtx = [	[0, 0, 1, 1, 0, 0, 0, 0, 0], 	# 1
		[0, 0, 1, 0, 1, 0, 0, 0, 0], 	# 2
		[0, 0, 0, 1, 1, 0, 0, 0, 0], 	# 3
		[0, 0, 0, 0, 0, 0, 1, 1, 0], 	# 4
		[0, 0, 0, 0, 0, 1, 0, 0, 0], 	# 5
		[0, 0, 0, 0, 0, 0, 1, 0, 1], 	# 6
		[0, 0, 0, 0, 0, 0, 0, 1, 1], 	# 7
		[0, 0, 0, 0, 0, 0, 0, 0, 0], 	# 8
		[0, 0, 0, 0, 0, 0, 0, 0, 0]]	# 9
p = [0.88, 0.42, 0.05, 0.62, 0.44, 0.13, 0.22, 0.63, 0.27]
TIME = 1703
PARAMS = [(False, True, 1), (True, True, 1)]
'''
# example
#		 1  2  3  4  5  6  7  8
mtx = [	[0, 1, 1, 0, 0, 0, 0, 0], 	# 1
		[0, 0, 0, 1, 1, 0, 0, 0], 	# 2
		[0, 0, 0, 1, 0, 1, 0, 1], 	# 3
		[0, 0, 0, 0, 1, 1, 0, 1], 	# 4
		[0, 0, 0, 0, 0, 1, 1, 0], 	# 5
		[0, 0, 0, 0, 0, 0, 1, 1], 	# 6
		[0, 0, 0, 0, 0, 0, 0, 0], 	# 7
		[0, 0, 0, 0, 0, 0, 0, 0]]	# 8
p = [0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.92, 0.94]
TIME = 1000
PARAMS = [(False, False, 1), (True, True, 1)]

# 22 v
#		 1  2  3  4  5  6  7  8
mtx = [	[0, 1, 1, 0, 0, 0, 0, 0], 	# 1
		[0, 0, 0, 1, 1, 1, 0, 0], 	# 2
		[0, 0, 0, 1, 1, 0, 1, 0], 	# 3
		[0, 0, 0, 0, 1, 1, 1, 0], 	# 4
		[0, 0, 0, 0, 0, 1, 1, 0], 	# 5
		[0, 0, 0, 0, 0, 0, 0, 1], 	# 6
		[0, 0, 0, 0, 0, 0, 0, 1], 	# 7
		[0, 0, 0, 0, 0, 0, 0, 0]]	# 8
p = [0.84, 0.84, 0.91, 0.6, 0.44, 0.74, 0.57, 0.79]
'''

paths = []

first_nodes = []
last_nodes = []
for i in range(len(mtx)):
	flag_first = True
	flag_last = True
	for j in range(len(mtx)):
		if mtx[j][i] == 1:
			flag_first = False
		if mtx[i][j] == 1:
			flag_last = False
			
	if flag_first:
		first_nodes.append(i)
	if flag_last:
		last_nodes.append(i)

for i in first_nodes:
	dfs_edit(mtx, i, last_nodes, paths, [i])

new_paths = [list(range(len(mtx))), *paths]
for i in paths:
	semi_universal = set(range(len(mtx))) - set(i)
	for j in range(len(semi_universal)):
		for k in combinations(semi_universal, j):
			if sorted(i + list(k)) not in new_paths:
				new_paths.append(sorted(i + list(k)))

new_paths.sort(key=len, reverse=True)

p_paths = count_paths(mtx, new_paths, p)

print("Всі шляхи від 1 до {}:".format(len(mtx)), 
		*["[{:s}]".format(", ".join(map(lambda x: str(x+1), paths[i]))) 
			for i in range(len(paths))], sep="\n")
print("\nТаблиця працездатних станів системи:", 
		*["[{:s}] = {:.10f}".format(", ".join(map(lambda x: str(x+1), new_paths[i])), p_paths[i]) 
			for i in range(len(new_paths))], sep="\n")

print("\nЙмовірність безвідмовної роботи P({}) = {:.10f}".format(TIME, sum(p_paths)))
print("Ймовірність відмови Q({}) = {:.10f}".format(TIME, 1 - sum(p_paths)))
print("Інтенсивність відмов λ({}) = {:.10f}".format(TIME, -log(sum(p_paths)) / TIME))
print("Середній наробіток до відмови T({}) = {:.10f}".format(TIME, -TIME / log(sum(p_paths))))

for div, weight, mlt in PARAMS:
	print("\nСистема з {} {}навантаженим резервуванням, з кратністю {}:"
			.format("роздільним" if div else "загальним", "" if weight else "не", mlt))
	
	if div:
		p_new = list(map(lambda x: 1-(1-x)**(mlt+1), p))
		print("Ймовірність відмови та безвідмовної роботи кожного елемента системи",
				*["\tQr{} = {:.4f},\tPr{} = {:.4f}".format(i+1, 1-p_new[i], i+1, p_new[i]) 
					for i in range(len(p_new))], sep="\n")
	else:
		p_new = [i for i in p]

	tmp_paths = count_paths(mtx, new_paths, p_new)

	if weight:
		prs = sum(tmp_paths) if div else (1 - (1 - sum(tmp_paths))**(mlt + 1))
		qrs = 1 - prs
	else:
		qrs = 1 / factorial(mlt + 1) * (1 - sum(tmp_paths))
		prs = 1 - qrs

	print("Ймовірність відмови Qrs({}) = {:.10f}".format(TIME, qrs))
	print("Ймовірність безвідмовної роботи Prs({}) = {:.10f}".format(TIME, prs))
	print("Середній наробіток до відмови Trs({}) = {:.10f}".format(TIME, -TIME / log(prs)))
	print("Виграш надійності\tза ймовірністю відмов Gq({}) = {:.10f}".format(TIME, qrs / (1 - sum(p_paths))))
	print("\t\t\tза ймовірністю безвідмовної роботи Gp({}) = {:.10f}".format(TIME, prs / sum(p_paths)))
	print("\t\t\tза середнім часом безвідмовної роботи Gt({}) = {:.10f}".format(TIME, log(sum(p_paths)) / log(prs)))
