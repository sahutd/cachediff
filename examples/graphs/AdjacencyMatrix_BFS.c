#include <stdio.h>
#include <stdlib.h>
#define VISITED 1
#define NOTVISITED 0

struct queue
{
    int *arr;
    int front;
    int rear;
};

void init(struct queue* temp, int v);
int is_empty(struct queue* temp);
void insert(struct queue* temp, int element);
int delete(struct queue* temp);

void populate(int **adjacency_matrix, int v);
void bfs(int **adjacency_matrix, int v);
void bfs_(int** adjacency_matrix, int *visited_matrix, int v, int i);

int
main()
{
    int v;
    int i;
    scanf("%d", &v);
    int **adjacency_matrix = (int**)malloc(sizeof(int *) * v);
    for(i = 0; i < v; ++i)
    {
        adjacency_matrix[i] = (int *) malloc(sizeof(int) * v);
    }
    populate(adjacency_matrix, v);
    bfs(adjacency_matrix, v);
}

void
init(struct queue* temp, int v)
{
    temp->arr = (int*) malloc(sizeof(int) * v);
    temp->front = 0;
    temp->rear = -1;
}

int
is_empty(struct queue* temp)
{
    return (temp->front > temp->rear);
}

void
insert(struct queue* temp, int element)
{
    ++temp->rear;
    temp->arr[temp->rear] = element;
}

int
delete(struct queue* temp)
{
    if (!(is_empty(temp)))
    {
        int ele = temp->arr[temp->front];
        temp->front++;
        return ele;
    }
}
void
populate(int **adjacency_matrix, int v)
{
    int i, j;
    for (i = 0; i < v; ++i)
    {
        for (j = 0; j < v; ++j)
        {
            scanf("%d", &adjacency_matrix[i][j]);
        }
    }
}

void
bfs(int **adjacency_matrix, int v)
{
    int i;
    int visited_matrix[v];
    int count = 0;
    for (i = 0; i < v; ++i)
    {
        visited_matrix[v] = NOTVISITED;
    }
    for (i = 0; i < v; ++i)
    {
        if (visited_matrix[i] == NOTVISITED)
        {
            bfs_(adjacency_matrix, visited_matrix, v, i);
            ++count;
        }
    }
}

void
bfs_(int **adjacency_matrix, int *visited_matrix, int v,
     int start_node)
{
    struct queue my_queue;
    int temp_node;
    int i;
    int edge_exists;

    init(&my_queue, v);
    if (visited_matrix[start_node] == NOTVISITED)
    {
        insert(&my_queue, start_node);
    }
    while (! is_empty(&my_queue))
    {
        temp_node = delete(&my_queue);
        visited_matrix[temp_node] = VISITED;
        for (i = 0; i < v; ++i)
        {
            if (i != temp_node && visited_matrix[i] == NOTVISITED)
            {
                edge_exists = adjacency_matrix[temp_node][i];
                if (edge_exists)
                {
                    insert(&my_queue, i);
                }
            }
        }
    }
}
