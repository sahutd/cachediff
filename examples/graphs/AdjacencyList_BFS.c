#include<stdio.h>
#include<stdlib.h>
#define VISITED 1
#define NOTVISITED 0
 
struct queue
{
    int *arr;
    int front;
    int rear;
};

struct node
{
	int node;
	int weight;
	struct node *next;
};

void populate(struct node **adj_list, int size);
void init(struct queue* temp, int v);
int is_empty(struct queue* temp);
void insert(struct queue* temp, int element);
int delete(struct queue* temp);
void bfs(struct node **adj_list, int v);
void bfs_(struct node **adj_list, int *visited_matrix, int v,
     int start_node);

int main()
{
	int size;
	scanf("%d",&size);

	struct node **adj_list = (struct node **)malloc((sizeof(struct node *)) * size);
	int i;
	for(i = 0; i < size; ++i)
	{
		adj_list[i] = NULL;
	}
	populate(adj_list,size);
	bfs(adj_list,size);
	
	return 0;
}


void populate(struct node **adj_list, int size)
{
	int i,j;
    int adjacent_node;
	for(i = 0; i < size; ++i)
	{
        int adjacency_count;
        scanf("%d", &adjacency_count);
		for( j = 0; j  < adjacency_count; ++j)
		{
			scanf("%d", &adjacent_node);

            struct node *temp = (struct node *)malloc(sizeof(struct node));
            temp -> node = j + 1;
            temp -> next = NULL;
            if(adj_list[i] == NULL)
            {
                adj_list[i] = temp;
            }
            else
            {
                temp -> next = adj_list[i];
                adj_list[i] = temp;
            }
		}
	}
}
void init(struct queue* temp, int v)
{
    temp->arr = (int*) malloc(sizeof(int) * v);
    temp->front = 0;
    temp->rear = -1;
}
 
int is_empty(struct queue* temp)
{
    return (temp->front > temp->rear);
}
 
void insert(struct queue* temp, int element)
{
    ++temp->rear;
    temp->arr[temp->rear] = element;
}
 
int delete(struct queue* temp)
{
    if (!(is_empty(temp)))
    {
        int ele = temp->arr[temp->front];
        temp->front++;
        return ele;
    }
}

void bfs(struct node **adj_list, int v)
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
            bfs_(adj_list, visited_matrix, v, i);
            ++count;
        }
    }
}
 
void bfs_(struct node **adj_list, int *visited_matrix, int v,
     int start_node)
{
    struct queue my_queue;
    struct node *p;
    int temp_node;
    int i;
    int edge_exists;
    int val = 0;
 
    init(&my_queue, v);
    if (visited_matrix[start_node] == NOTVISITED)
    {
        insert(&my_queue, start_node);
    }
    while (! is_empty(&my_queue))
    {
        temp_node = delete(&my_queue);
	   p = adj_list[temp_node];
        visited_matrix[temp_node] = VISITED;
        for (i = 0; i < v; ++i)
        {
		while(p!=NULL && !val)
		{
			if((p->node)-1 == i)
			{
				val = 1;
			}
			p = p -> next;
		}

            if (i != temp_node && visited_matrix[i] == NOTVISITED)
            {
                edge_exists = val;
                if (edge_exists)
                {
                    insert(&my_queue, i);
                }
            }
        }
    }
}
