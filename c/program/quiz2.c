#include <stdio.h>
#include "libcheckprime.h"

void main() {
  while(1)
  {
  int n;
  printf("input integer => ");
  scanf("%d", &n);
  if (n == 0 ) break;
  if(checkprime(n) == n)
    printf("%d is a prime number~ \n", n);
  else
    printf("%d is not number~!! \n", n);
  }
}
