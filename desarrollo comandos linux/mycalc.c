#include "mycalc.h"
// code is got from first laboratory work
#include <stdlib.h>//atoi() function
#include <string.h>//strlen() function
#include <fcntl.h> //open function
#include <unistd.h> //write() and close() functions
#include <stdio.h>  // printf
#include <string.h> // strlen

int mycalc(int argc, char *argv[]) {
  ssize_t bw;
    //MODE INTERACTIVE CALCULATOR
    if (argc==4){
    //Namely, we have 3 arguments
    //in argv[] we have text data, but we need to treat them as numbers
    if (!is_number(argv[1]) || !is_number(argv[3])) {
        char *e_arg="Error: Arguments must be integers\n";
        bw=write(2,e_arg,strlen(e_arg));
        (void)bw;
        return -1;}

    int num1 = atoi(argv[1]);
    // since the operator is a string, it is actually an array of characters composed by the operator and /0
    char operator= argv[2][0];
    int num2 = atoi(argv[3]);
    //set a variable to store the result of the operation
    int result;
    //now that we have everything we need, we just define the different cases and handle them
    if (operator=='+'){
        result = num1 + num2;
    } else if (operator=='-'){
        result = num1 - num2;
    } else if (operator=='x'){
        result = num1 * num2;
    } else if (operator=='/'){
        //we should also take into account the case of division by 0
        if (num2==0){
            char *error1="Division by 0\n";
            bw=write(2,error1,strlen(error1));
            (void)bw;
            return -1;
        } else {
            result = num1 / num2;
        }
    } else {
        // if none of the previous operators are found, raise an error
        char *error2="Invalid operator\n";
        bw=write(2,error2,strlen(error2));
        (void)bw;
        return -1;
    }
    printf("Operation: %d%c%d = %d\n", num1,operator,num2,result);
} else{
    char *error3="Incorrect number of arguments";
    bw=write(2,error3,strlen(error3));
    (void)bw;
    return -1;
}
return 0;
}