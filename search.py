_2Darray = [list(map(int, input().split())) for _ in range(128)]

visited = [[0 for _ in range(129)] for __ in range(129)]
pixel = 0
def dfs(i, j):
    global pixel
    if i < 0 or j < 0: return 0
    if i >= 128 or j >= 128: return 0
    if visited[i][j] or not _2Darray[i][j]: return 0
    visited[i][j] = 1
    pixel += 1
    for row, column in [(-1, 0), (1, 0), (0, 1), (0, -1), (1,1), (-1, -1), (-1, 1), (1, -1)]:
        dfs(i+row, j+column)


nuclei = 0
pixels = []
for i in range(128):
    for j in range(128):
        if _2Darray[i][j] and not visited[i][j]:
            nuclei += 1
            dfs(i, j)
            pixels.append(pixel)
            pixel = 0
print(nuclei)
print("Count of pixels:")
print(*pixels)