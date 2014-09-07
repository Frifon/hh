def main():
	def solve(n, k):
		dp = [[0 for i in range(k + 1)] for j in range(n + 1)]
		for i in range(n + 1):
			dp[i][1] = 1
		for j in range(2, k + 1):
			for i in range(j, n + 1):
				dp[i][j] = dp[i - 1][j - 1] + dp[i - j][j]
		return dp[n][k]

	fin = open("input.txt", "r")
	fout = open("output.txt", "w")

	n, k = map(int, fin.readline().split())
	fout.write(str(solve(n, k)))

	fin.close()
	fout.close()
main()
