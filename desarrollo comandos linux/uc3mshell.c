#include "mycalc.h" // Includes mycalc.h
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>
#include <stdlib.h>

const int max_line = 1024;
#define max_commands 10
#define max_redirections 3 // stdin, stdout, stderr
#define max_args 15

/* VARS TO BE USED FOR THE STUDENTS */
char *argvv[max_commands][max_args]; // 2D array to store args for each command in a pipe
char *filev[max_redirections];
int background = 0;

/**
 * This function splits a char* line into different tokens based on a given
 * character
 * @return Number of tokens
 */
int tokenizar_linea(char *linea, char *delim, char *tokens[], int max_tokens) {
  int i = 0;
  char *token = strtok(linea, delim);
  while (token != NULL && i < max_tokens - 1) {
    tokens[i++] = token;
    token = strtok(NULL, delim);
  }
  tokens[i] = NULL;
  return i;
}

/**
 * This function processes the command line to evaluate if there are
 * redirections. If any redirection is detected, the destination file is
 * indicated in filev[i] array. filev[0] for STDIN filev[1] for STDOUT filev[2]
 * for STDERR
 */
void procesar_redirecciones(char *args[]) {
  int i = 0, first_red = -1;

  // Store the pointer to the filename if needed.
  for (i = 0; args[i] != NULL; i++) {

    if (strcmp(args[i], "<") == 0) {
      filev[0] = args[i + 1];
      if (first_red == -1)
        first_red = i;
    } else if (strcmp(args[i], ">") == 0) {
      filev[1] = args[i + 1];
      if (first_red == -1)
        first_red = i;
    } else if (strcmp(args[i], "!>") == 0) {
      filev[2] = args[i + 1];
      if (first_red == -1)
        first_red = i;
    }
  }

  // starting from the first redirectorion, all fields are set to NULL
  if (first_red != -1)
    for (i = first_red; args[i] != NULL; i++) {
      args[i] = NULL;
    }
}

/**
 * This function processes the input command line and returns in global
 * variables: argvv -- command an args as argv filev -- files for redirections.
 * NULL value means no redirection. background -- 0 means foreground; 1
 * background.
 */
int procesar_linea(char *linea) {

  char *comandos[max_commands];
  int num_comandos = tokenizar_linea(linea, "|", comandos, max_commands);
  background = 0;

  // Check if background is indicated
  if (strchr(comandos[num_comandos - 1], '&')) {
    background = 1;
    char *pos = strchr(comandos[num_comandos - 1], '&');
    // removes character &
    *pos = '\0';
  }

  filev[0] = NULL;
  filev[1] = NULL;
  filev[2] = NULL;
  // Finish processing
  for (int i = 0; i < num_comandos; i++) {
    tokenizar_linea(comandos[i], " \t\n", argvv[i], max_args);
    procesar_redirecciones(argvv[i]);
  }
  return num_comandos;
}

int is_number(char *str) {
  if (str == NULL || *str == '\0') {
      return 0;
  }

  int i = 0;
  if (str[0]=='-'){
      if (str[1]=='\0') return 0;
      i=1;
  }

  for (;str[i]!='\0';i++){
      //if they are not a number
      if (str[i]<'0'|| str[i]>'9') return 0;
  }
  return 1;
}


int main(int argc, char *argv[]) {

  if (argc!=2){
    perror("Usage: ./uc3mshell file");
    return -1;
  }
  char *ex_file =argv[1];
  int fd;

  //open the input file
  if ((fd=open(ex_file, O_RDONLY))<0){
    perror("Error opening file");
    return -1;
  }

  //check if the header is ## Uc3mshell P2 reading the first line character by character
  char header[max_line];
  char ch;
  int i=0;

  while(read(fd,&ch,1)>0){
    if(ch!='\n'){
      header[i++]=ch;
    }
    else{
      break;
    }
  } // end while

  header[i++]='\0'; 
  if (strcmp(header,"## Uc3mshell P2")!=0){
    perror("Input file doesn't contain a header ");
    return -1;
  } // end if

  //After reading the first line the reading pointer will be placed in the second line so we continue reading
  //now we have to read the entire file
  //initialize the buffer that will contain the corresponding line
  char r_buff[max_line];
  //using while loop to read the file
  i=0;
  // reuse variables i and ch to read a file content
  while(read(fd,&ch,1)>0){
    if (ch!='\n'){
      //check if the line has excede the maximun line size
      if (i>max_line-1){
        perror("line too long");
        exit(-1);
      }
      //store the read character in the buffer
      else{
        r_buff[i++]=ch;
        }
      }
    else{
      //when character is '\n'
      r_buff[i]='\0';
      //deal with the content read in this line
      //if the line start with # it is a comment we should skip it
      if (r_buff[0]!='#' && i>0){
        //the execution will only be consider when the line is not a comment or empty one
        //see how many command there are
        int n_commands=procesar_linea(r_buff);
        if (n_commands > max_commands){
          char*msg="Error: line contains too many commands";
          ssize_t bw1= write(STDERR_FILENO, msg, strlen(msg));
          (void)bw1;
        }
        else{
          //run the commands
          if(n_commands==1){
            //single commands
            //store the command name
            char *comm_name=argvv[0][0];

            if (strcmp(comm_name, "exit")==0){
              //internal command exit
              //check if the argument is a integer value and not null
              if(argvv[0][1] == NULL){
                char*msg="[Error] The exit code must be an integer\n";
                ssize_t bw2= write(STDERR_FILENO,msg,strlen(msg));
                (void)bw2;
              }
              else if (is_number(argvv[0][1])==0){
                char*msg="[Error] The exit code must be an integer\n";
                ssize_t bw3= write(STDERR_FILENO,msg,strlen(msg));
                (void)bw3;
              }
              else{
                //wait for the processes running in the background and delete zombies processes
                while(wait(NULL)>0);
                printf("Goodbye %d\n",atoi(argvv[0][1]));
                close(fd);
                exit(0);
              }
            } //end if for exit

            else if (strcmp(comm_name, "mycalc")==0){
              //internal command mycalc
              //count argc
              int argc_count=0;
              while(argvv[0][argc_count]!= NULL){
                argc_count++;
              }
              //check if it is a valid input for mycalc
              if (argc_count!=4){
                char*msg="[Error]mycalc requires 3 arguments: operand1 operator operand2\n";
                ssize_t bw4= write(STDERR_FILENO,msg,strlen(msg));
                (void) bw4;
              }
              else{
                //call mycalc function
                mycalc(argc_count, argvv[0]);
              }
            } //end if for mycalc

            else{
              //external commands
              pid_t pid=fork();

              if(pid==0){
                //child process
                //if exist some redirections
                if (filev[0]) {
                  int fd_in = open(filev[0], O_RDONLY);
                  dup2(fd_in, 0);
                  close(fd_in);
                }
                if (filev[1]) {
                  int fd_out = open(filev[1], O_CREAT | O_WRONLY | O_TRUNC, 0664);
                  dup2(fd_out, 1);
                  close(fd_out);
                }
                if (filev[2]) {
                  int fd_err = open(filev[2], O_CREAT | O_WRONLY | O_TRUNC, 0664);
                  dup2(fd_err, 2);
                  close(fd_err);
                }
                //execute command
                if(execvp(argvv[0][0],argvv[0])<0){
                  perror("Error executing command");
                  exit(-1);
                }
              }// end child

              else if (pid>0){
                //parent process
                if (background==0){
                  //wait for the child to finish
                  waitpid(pid,NULL,0);
                } 
                else{
                  printf("%d\n",pid);
                }                
              }

              else{
                //pid<0
                perror("Fork failed");
              }
            }// end else for external command
          }// end if for single command

          else{
            //sequence of commands (pipeline)
            int pd[n_commands-1][2];
            //create pipes
            for(int j = 0; j < n_commands - 1; j++){
              if (pipe(pd[j])<0){
                perror("Pipe creation failed");
                exit(-1);
              }
            }
            for(int j = 0; j < n_commands; j++){
              if (fork()==0){
                // Child: Connect to previous pipe
                if (j > 0) {dup2(pd[j-1][0], STDIN_FILENO);}
                // Child: Connect to next pipe
                if (j < n_commands - 1) {dup2(pd[j][1], STDOUT_FILENO);}

                // Close all pipe FDs in child
                for(int k = 0; k < n_commands - 1; k++) {
                    close(pd[k][0]);
                    close(pd[k][1]);
                }

                // Handle Redirections (Only for first/last commands)
                if (i == 0 && filev[0]) {
                  int fd_in = open(filev[0], O_RDONLY);
                  dup2(fd_in, 0);
                  close(fd_in);
                }
                if (i == n_commands - 1) {
                  if (filev[1]) { 
                    int fd_out = open(filev[1], O_CREAT | O_WRONLY | O_TRUNC, 0664);
                    dup2(fd_out, 1);
                    close(fd_out);
                  }
                  if (filev[2]) { 
                    int fd_err = open(filev[2], O_CREAT | O_WRONLY | O_TRUNC, 0664);
                    dup2(fd_err, 2);
                    close(fd_err);
                  }
                }

                // EXECUTE
                execvp(argvv[i][0], argvv[i]);
                perror("Exec failed");
                exit(-1);
              }
            }
            for(int j=0; j<n_commands;j++){
              wait(NULL);
            }
          }
        } 
      }  
      //restart the counter i for the new line
      i=0;
    } // end else
  } //end while  
  close(fd);
  return 0;
} //end main
  
