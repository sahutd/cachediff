#include<stdio.h>
#include<stdlib.h>

#define TRUE 1
#define FALSE 0
#define HASH_SIZE 1000
#define HASH_CONST 31

struct node
{
    int value;
    struct node *next;
};

int hash(int value);
void insert_l(int *HASH_MAP, int value);
void insert_s(struct node **HASH_MAP, int value);
int search_l(int *HASH_MAP, int value);
int search_s(struct node **HASH_MAP, int value);
void process_linear();
void process_seperate();

int main()
{
    process_linear();
}

void process_linear()
{
    int *HASH_MAP = (int *)calloc(sizeof(int), HASH_SIZE);
    int N;
    scanf("%d",&N);
    int i;
    int num;
    for(i=0;i<N;i++)
    {
        scanf("%d",&num);
        insert_l(HASH_MAP, num);
    }
    int S;
    scanf("%d",&S);
    for(i=0;i<S;i++)
    {
        scanf("%d",&num);
        printf("Is value %d present in HASH_MAP : %d\n",
                num, search_l(HASH_MAP, num));
    }
}

void process_seperate()
{
    struct node **HASH_MAP = (struct node **)
        calloc(sizeof(struct node *), HASH_SIZE);
    int N;
    scanf("%d",&N);
    int i;
    for(i=0;i<HASH_SIZE;i++)
    {
        HASH_MAP[i] =  NULL;
    }
    int num;
    for(i=0;i<N;i++)
    {
        scanf("%d",&num);
        insert_s(HASH_MAP, num);
    }
    int S;
    scanf("%d",&S);
    for(i=0;i<S;i++)
    {
        scanf("%d",&num);
        printf("Is value %d present in HASH_MAP : %d\n",
                num, search_s(HASH_MAP, num));
    }
}

int hash(int value)
{
    return ((value * HASH_CONST) % HASH_SIZE);
}

void insert_l(int *HASH_MAP, int num)
{
    int probe = hash(num);
    while(HASH_MAP[probe] != 0)
    {
        probe = (probe + 1) % HASH_SIZE;
    }
    HASH_MAP[probe] = num;
}

int search_l(int *HASH_MAP, int num)
{
    int probe = hash(num);
    int i;
    for(i=0;i<HASH_SIZE;i++)
    {
        if(HASH_MAP[probe] == num)
        {
            return TRUE;
        }
    }
    return FALSE;
}

void insert_s(struct node **HASH_MAP, int num)
{
    int probe = hash(num);
    if(HASH_MAP[probe] == NULL)
    {
        HASH_MAP[probe] = (struct node *)
            malloc(sizeof(struct node));
        HASH_MAP[probe]->value = num;
        HASH_MAP[probe]->next = NULL;
    }
    else
    {
        struct node *temp = HASH_MAP[probe];
        while(temp->next != NULL)
        {
            temp = temp->next;
        }
        temp->next = (struct node *)
            malloc(sizeof(struct node));
        temp->next->value = num;
        temp->next->next = NULL;
    }
}

int search_s(struct node **HASH_MAP, int num)
{
    int probe = hash(num);
    struct node *temp = HASH_MAP[probe];
    while(temp != NULL)
    {
        if(temp->value == num)
        {
            return TRUE;
        }
        temp = temp->next;
    }
    return FALSE;
}
