#include<stdio.h>
#include<cs50.h>

int main(void)
{
    int n;
    n = get_int("Height: ");
    while (n > 8 || n < 1)
    {
        n = get_int("Height: ");
    }
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n ; j++)
        {
            if ((j + i + 1) >= n)
            {
                printf("#");
            }
            else
            {
                printf(" ");
            }
        }
        printf("\n");
    }
}