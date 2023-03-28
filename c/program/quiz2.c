<<<<<<< Updated upstream
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
=======
<<<<<<< HEAD
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
=======
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
>>>>>>> 8010c763e56641d7b1d4944701bc237a3fa48dbb
>>>>>>> Stashed changes
