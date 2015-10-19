#include <stdio.h>
void foo()
{
    printf("hello world");
}
int main()
{

    int i, j;
    int a[100][100];
    for (i = 0; i < 100; ++i)
    {
        for (j = 0; j < 100; ++j)
        {
            printf("%d ", a[j][i]);
        }
    }
}
