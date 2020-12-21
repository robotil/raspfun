#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#include <net/if.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/ioctl.h>

#include <linux/can.h>
#include <linux/can/raw.h>

int
main(int argc, char *argv[])
{
	int s;
	int nbytes;
	struct sockaddr_can addr;
	struct can_frame frame;
	struct ifreq ifr;
	int i;

	char *ifname[150]; 

	if (argc > 1){
		sprintf(ifname, "%s", argv[1]);
	} else {
		sprintf(ifname, "%s","vcan0");
	}
    printf("Receive data on if %s\n", ifname);

	if((s = socket(PF_CAN, SOCK_RAW, CAN_RAW)) == -1) {
		perror("Error while opening socket");
		return -1;
	}

	strcpy(ifr.ifr_name, ifname);
	ioctl(s, SIOCGIFINDEX, &ifr);
	
	addr.can_family  = AF_CAN;
	addr.can_ifindex = ifr.ifr_ifindex;

	printf("%s at index %d\n", ifname, ifr.ifr_ifindex);

	if(bind(s, (struct sockaddr *)&addr, sizeof(addr)) == -1) {
		perror("Error in socket bind");
		return -2;
	}

    while (1){
		nbytes = read(s, &frame, sizeof(struct can_frame));
		if (nbytes < 0) {
   			perror("Too Bad");
   			return 1;
		}

		printf("0x%03X [%d] ",frame.can_id, frame.can_dlc);
		for (i = 0; i < frame.can_dlc; i++)
   			printf("%02X ",frame.data[i]);
		printf("\r\n");
	}


	return 0;
}