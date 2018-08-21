/*
 * C program to input real numbers and find the mean, variance
 * and standard deviation
 */
#include <stdio.h>
#include <math.h>
#define MAXSIZE 10

int block[MAXSIZE] = {150, 450, 750, 1050, 1350};

float stddev(int *block, int blocksize) {
  int  i, n = blocksize/sizeof(*block);
  float average, variance, std_deviation, sum = 0, sum1 = 0;
  for (i = 0; i < n; i++)
  {
      sum = sum + block[i];
  }
  average = sum / (float)n;
  /*  Compute  variance  and standard deviation  */
  for (i = 0; i < n; i++)
  {
      sum1 = sum1 + pow((block[i] - average), 2);
  }
  variance = sum1 / (float)n;
  std_deviation = sqrt(variance);
  return std_deviation;
}

int main()
{
    float std = stddev(block, sizeof(block));
    printf("%f\n", std);
    // int  i, n = sizeof(block)/4;
    // float average, variance, std_deviation, sum = 0, sum1 = 0;
    //
    // // printf("Enter the value of N \n");
    // // scanf("%d", &n);
    // // printf("Enter %d real numbers \n", n);
    // // for (i = 0; i < n; i++)
    // // {
    // //     scanf("%f", &x[i]);
    // // }
    // /*  Compute the sum of all elements */
    // for (i = 0; i < n; i++)
    // {
    //     sum = sum + block[i];
    // }
    // average = sum / (float)n;
    // /*  Compute  variance  and standard deviation  */
    // for (i = 0; i < n; i++)
    // {
    //     sum1 = sum1 + pow((block[i] - average), 2);
    // }
    // variance = sum1 / (float)n;
    // std_deviation = sqrt(variance);
    // printf("Average of all elements = %.2f\n", average);
    // printf("variance of all elements = %.2f\n", variance);
    // printf("Standard deviation = %.2f\n", std_deviation);
}
