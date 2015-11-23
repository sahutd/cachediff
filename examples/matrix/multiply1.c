#include<stdio.h>
#include<stdlib.h>

void read_matrix(int *a, int N);
void display_matrix(int *a, int N);
void multiply_matrix_1(int *a, int *b, int *c, int N);
void multiply_matrix_2(int *a, int *b, int *c, int N);
void multiply_matrix_3(int *a, int *b, int *c, int N);

int main()
{
    int N;
    scanf("%d",&N);
    int *matrix_a = (int *)malloc(N * N * sizeof(int));
    int *matrix_b = (int *)malloc(N * N * sizeof(int));
    int *matrix_c = (int *)malloc(N * N * sizeof(int));
    read_matrix(matrix_a, N);
    read_matrix(matrix_b, N);
    multiply_matrix_1(matrix_a, matrix_b, matrix_c, N);
    display_matrix(matrix_c, N);
}

void read_matrix(int *a, int N)
{
    int i;
    int j;
    for(i=0;i<N;i++)
    {
        for(j=0;j<N;j++)
        {
            scanf("%d", ( (a + i * N) + j) );
        }
    }
}

void display_matrix(int *a, int N)
{
    int i;
    int j;
    for(i=0;i<N;i++)
    {
        for(j=0;j<N;j++)
        {
            printf("%d ", *( (a + i * N) + j) );
        }
        printf("\n");
    }
}

void multiply_matrix_1(int *a, int *b, int *c, int N)
{
    int i;
    int j;
    for(i=0;i<N;i++)
    {
        for(j=0;j<N;j++)
        {
            int sum = 0;
            int k;
            for(k=0;k<N;k++)
            {
                sum += *((a+i*N)+k) * *((b+k*N)+j);
            }
            *((c+i*N)+j) = sum;
        }
    }
}

void multiply_matrix_2(int *a, int *b, int *c, int N)
{
    int k;
    int i;
    for(k=0;k<N;k++)
    {
        for(i=0;i<N;i++)
        {
            int r = *((a+i*N)+k);
            int j;
            for(j=0;j<N;j++)
            {
                *((c+i*N)+j) += r * *((b+k*N)+j);
            }
        }
    }
}

void multiply_matrix_3(int *a, int *b, int *c, int N)
{
    int j;
    int k;
    for(j=0;j<N;j++)
    {
        for(k=0;k<N;k++)
        {
            int r = *((b+k*N)+j);
            int i;
            for(i=0;i<N;i++)
            {
                *((c+i*N)+j) += *((a+i*N)+k) * r;
            }
        }
    }
}
