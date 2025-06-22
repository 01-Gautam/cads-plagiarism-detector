#include <stdio.h> struct sjfs{     int at, id, bt;     int wt, ct, st,tat,rt; 
}; 
int main(){ 
    int n; 
    printf ("enter the number of proccess :"); scanf("%d",&n);     struct sjfs p[n]; 
    printf("enter the arrival time and burst time :");     int iscom[n];     for(int i = 0 ;i<n;i++){ 
        p[i].id = i;         iscom[i] = 0; 
        scanf("%d %d",&p[i].at,&p[i].bt);         p[i].rt = p[i].bt; 
    } 
    float awt = 0 ,atat = 0 ;     int time = 0,completed = 0 ; 
    while(completed < n){ 
        int idx = -1;         int minbt = 999; 
        for(int i = 0 ; i< n;i++){ 
            if(p[i].at<time && iscom[i]==0 && p[i].rt < minbt){                 minbt = p[i].rt; 
                idx = i; 
            }      } 
        if(idx!= -1){ 
            printf("P%d |",p[idx].id); 
            p[idx].rt--;             time++;             if(p[idx].rt ==0){                 p[idx].ct = time; 
                p[idx].tat = p[idx].ct-p[idx].at;                 p[idx].wt = p[idx].tat - p[idx].bt;                 awt += p[idx].wt;                 atat += p[idx].tat;                 iscom[idx] = 1; 
                completed++; 
            } 
        }else{             time++; 
        } 
} 
printf("\nID\tAT\tBT \tCT\tWT\tTAT\n"); for(int i = 0 ; i< n;i++){ 
    printf("%d\t%d\t%d\t%d\t%d\t%d\n",p[i].id,p[i].at,p[i].bt,p[i].ct,p[i].wt,p[i].tat); } 
printf("the average watiting time is :%f\n",awt/n); 
printf("the average turn around time is :%f\n",atat/n);     }



#include<stdio.h> 
#include<stdlib.h> 
 
int main() 
{ 
  FILE *file1,*file2;   file1= fopen("file1.txt","w");   fprintf(file1,"Ram\n"); 
  fclose(file1);   file2= fopen("file2.txt","w");   fprintf(file2,"Kishan \n");   fclose(file2);   printf("comparing"); 
  system("grep -Ff file1.txt file2.txt");   return 0; 
}