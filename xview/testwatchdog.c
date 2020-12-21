
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <linux/ioctl.h>
#include <linux/types.h>
#include <linux/watchdog.h>
#include <errno.h>

int main()
{
    int fd, ret;
    int timeout = 0;
    /* open WDT0 device (WDT0 enables itself automatically) */
    fd = open("/dev/watchdog0", O_RDWR);
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
    fprintf(stdout, "Watchdog timeout value: %d\n", timeout);
    
    /* set new timeout value 60s */
    /* Note the value should be within [5, 1000] */
    timeout = 60;
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
