# <b>Sokoban-ai-project</b>

## Introduction

### <b>Sokoban</b>
Created by: Hiroyuki Imabayashi in 1981<br>
Sokoban is a puzzle game in which the player pushes boxes or crates around in a warehouse, trying to get them to storage locations. The puzzle is usually implemented as a video game, but can also be found in printed format. The name Sokoban is Japanese, meaning warehouse keeper. (<a href="https://en.wikipedia.org/wiki/Sokoban" rel="nofollow">Wikipedia</a>)

### <b>A* algorithm</b>
A* is a computer algorithm that is widely used in pathfinding and graph traversal, which is the process of plotting an efficiently traversable path between multiple points, called nodes. It enjoys widespread use due to its performance and accuracy. (<a href="https://en.wikipedia.org/wiki/A*_search_algorithm" rel="nofollow">Wikipedia</a>)

#### <b>Search algorithms implemented</b>

1) Breadth First Search
2) Depth First Search
3) Depth Limited Search
4) Iterative Deepening Search
5) A* Search and Greedy Best First Search

#### <b>Heuristics implemented</b>

1) Boxes out of place/goal
2) Euclidean distance
3) Manhattan distance
4) Pull distance + Hungarian assignment algorithm (Reference: <a href="https://www.google.co.in/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwj88rWs8tf7AhVcSmwGHWUCBl4QFnoECBkQAQ&url=https%3A%2F%2Fbaldur.iti.kit.edu%2Ftheses%2FSokobanPortfolio.pdf&usg=AOvVaw3y1Djow_CacnaVpAS5_HHF" rel="nofollow">Solving Sokoban with a Hungarian Assignment Algorithm</a>)

## <b>How to run</b>
1) Clone the repository and create a virtual environment 
2) Install the requirements with <br>
```pip install -r requirements.txt```
3) Run search.py and test file name as argument<br>
```python search.py testExamples.txt```
4) Choose the algorithm you want to run and the heuristic you want to use<br><i>For best results use A* with the Pull heuristic (Greedy search)</i>

## <b>Requirements</b>

- Python 3.6
- Ipython 8.7.0
- Numpy 1.22.3
- Pandas 1.4.2
- Scipy 1.7.3


