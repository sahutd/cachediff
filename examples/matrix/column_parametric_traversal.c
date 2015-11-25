#include <stdio.h>
#define SIZE 100
#define ROW 1
#define COLUMN 0

void function(int size; int array[][size], int slice, int direction, int size)
{
    int i;
    int index1, index2;
    for(i = 0; i < size; ++i)
    {
        index1 = direction * slice + !direction * i;
        index2 = !direction * slice + direction * i;
        printf("%d ", array[index1][index2]);
    }
}

int main()
{
    int i, j;
    int a[SIZE][SIZE];
    for (i = 0; i < SIZE; ++i)
    {
        for (j=0; j < SIZE; ++j)
        {
            a[i][j] = (i+1) * 100 + j;
        }
    }
    for (i = 0; i < SIZE; ++i)
    {
        function(a, i, COLUMN, SIZE);
        printf("\n");
    }
}
