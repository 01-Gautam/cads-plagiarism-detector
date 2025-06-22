#include<stdio.h> 
#include<stdlib.h> 
 
int main() 
{ 
  FILE *file1,*file2;   file1= fopen("file1.txt","w");   fprintf(file1,"Ram\n"); 
  fclose(file1);   file2= fopen("file2.txt","w");   fprintf(file2,"Kishan \n");   fclose(file2);   printf("comparing"); 
  system("grep -Ff file1.txt file2.txt");   return 0; 
}