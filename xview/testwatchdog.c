
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <linux/ioctl.h>
#include <linux/types.h>
#include <linux/watchdog.h>
#include <errno.h>
//#include <stdlib.h>
//#include <unistd.h>
//#include <libgen.h>
//#include <string.h>
//#include <getopt.h>
//In order to cancel the watchdog, 
int main(int argc, char *argv[])
{
    int fd, ret;
    int timeout = 0;
    int opt;
    char *wtd[120];
    int tmo;
    printf("argc=%d\n", argc);
    for( int i = 0; i < argc; i++ )
	{
		printf( "arg %d: %s\n", i, argv[i] );
	}
    if (argc >1){
        strcpy(wtd, argv[1]);
        printf("wtd=%s\n", wtd);
    }
    if (argc > 2){
        tmo=atoi(argv[2]);
        printf("tmo=%d\n", tmo);
    }
    
    /* open WDT0 device (WDT0 enables itself automatically) */
    fd = open(wtd, O_RDWR);
    if(fd < 0) {
        /**fprintf(stderr, "Open watchdog device failed!\n");**/
        perror("Open watchdog device failed!");
        return -1; 
    }
    
    /* WDT0 is counting now,check the default timeout value */
    ret = ioctl(fd, WDIOC_GETTIMEOUT, &timeout);
    if(ret) {
        //fprintf(stderr, "Get watchdog timeout value failed!\n");
        perror("Get watchdog timeout value failed!\n");
        return -1; 
    }
    // ret = close(fd);
    // if(ret) {
    //     perror("Cannot close watchdog\n");
    // }
    fprintf(stdout, "Watchdog timeout value: %d\n", timeout);
    return 0;
    /* set new timeout value 60s */
    /* Note the value should be within [5, 1000] */
    timeout = tmo;
    ret = ioctl(fd, WDIOC_SETTIMEOUT, &timeout);
    if(ret) {
        perror("Set watchdog timeout value failed!\n");
        //fprintf(stderr, "Set watchdog timeout value failed!\n");
        return -1;
    }
    fprintf(stdout, "New watchdog timeout value: %d\n", timeout);  
    
    /*Kick WDT0, this should be running periodically */
    ret = ioctl(fd, WDIOC_KEEPALIVE, NULL);
    if(ret) {
        perror("Kick watchdog failed!\n");
        //fprintf(stderr, "Kick watchdog failed!\n");
        return -1;
    }
}
