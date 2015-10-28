#include <stdio.h>
#include <stdlib.h>


int cmpfunc (const void * a, const void * b)
{
   return ( *(int*)a - *(int*)b );
}

int main()
{
    int n;
    int i;
    scanf("%d", &n);
    int values[n];
    for (i = 0; i < n; ++i)
    {
        values[i] = n - i;
    }
    qsort(values, n, sizeof(int), cmpfunc);
    printf("\nAfter sorting the list is: \n");
    for (i = 0; i < n; ++i)
    {
        printf("%d ", values[i]);
    }
}
