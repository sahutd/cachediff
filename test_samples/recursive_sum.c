#include <stdio.h>
int sum(int x)
{
    if (x == 0)
    {
        return x;
    }
    return x + sum(x - 1);
}

int main()
{
    int x;
    scanf("%d", &x);
    int result = sum(x);
    printf("%d", sum);
}
