#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>

int main(int argc, char **argv) {
  if (argc != 3) {
    printf("Usage: %s <source_file> <destination_file>\n", argv[0]);
    return -1;
  }
  //open source file
  int fd_source=open(argv[1],O_RDONLY);
  if (fd_source<0){
    perror("Error opening source file");
    return -1;
  }
  //open destination file
  int fd_destination=open(argv[2],O_WRONLY|O_CREAT|O_TRUNC,0664);
  if (fd_destination<0){
    perror("Error opening destination file");
    return -1;
  }

  //transfer data
  char buffer[1024];
  ssize_t bytes_read;
  ssize_t bytes_written;

  bytes_read=read(fd_source,buffer,sizeof(buffer));
  while (bytes_read>0){
    bytes_written=write(fd_destination,buffer,(size_t)bytes_read);
    (void)bytes_written;
    if (bytes_written < 0) {
      perror("Error writing to destination file");
      close(fd_source);
      close(fd_destination);
      return -1;
  }
  (void)bytes_written;
}
  if (bytes_read < 0) {
    perror("Error reading from source file");
  }

  close(fd_source);
  close(fd_destination);
  return 0;
}