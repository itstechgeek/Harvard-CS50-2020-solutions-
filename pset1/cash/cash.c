#include<stdio.h>
#include<cs50.h>
#include<math.h>

int main(void)
{
    float input = get_float("Change owed: ");
    while (input < 0)
    {
        input = get_float("Change owed: ");
    }
    int coins = round(input * 100);

    int count = 0;
    while (coins >= 25)
    {
        // if still denomination with 25c change
        coins = coins - 25;
        count++;
    }
    while (coins >= 10)
    {
        // if still denomination with 10c change
        coins = coins - 10;
        count++;
    }
    while (coins >= 5)
    {
        // if still denomination with 5c change
        coins = coins - 5;
        count++;
    }
    while (coins >= 1)
    {
        // if still denomination with 1c change
        coins = coins - 1;
        count++;
    }
    printf("%d\n", count);
}