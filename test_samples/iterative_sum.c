#include <stdio.h>
int sum(int x)
{
    int result = 0;
    while (x--)
    {
        result += x;
    }
    return result;
}

int main()
{
    int x;
    scanf("%d", &x);
    int result = sum(x);
    printf("%d", sum);
}
