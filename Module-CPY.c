#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/netfilter.h>
#include <linux/netfilter_ipv4.h>
#include <linux/ip.h>
#include <linux/tcp.h>
#include <linux/string.h>

#define GREENDAY "pass" // The wanted password

static struct nf_hook_ops nfho; // Netfilter hook option struct?
static int intercept_enabled = 0;
static unsigned int intercepted_port = 0; // Port to intercept after password is found
static unsigned int IP_intercepted = 0;

// Function to check if the payload contains a password
int contains_password(unsigned char *payload, int payload_len) {
    if (payload_len >= strlen(GREENDAY)) {
        if (memcmp(payload, GREENDAY, strlen(GREENDAY)) == 0) {
            return 1; // Password found
        }
    }
    return 0; // Not Password
}

// Function
unsigned int intercept_func(void *priv, struct sk_buff *skb, const struct nf_hook_state *state) {
    struct iphdr *ip_header;
    struct tcphdr *tcp_header;
    unsigned char *payload;
    int payload_len;
    // Get IP ponter
    ip_header = ip_hdr(skb);
    // Check if it's a TCP packet
    if (ip_header->protocol == IPPROTO_TCP) {
        tcp_header = tcp_hdr(skb);
        // If interception is enabled or the password is found
        if (intercept_enabled || contains_password((unsigned char *)tcp_header, skb->len-(ip_header->ihl*4)-(tcp_header->doff*4))) {
            if (!intercept_enabled) {
                intercept_enabled = 1;
                intercepted_port = ntohs(tcp_header->source); // Set the intercepted port
                IP_intercepted = ntohl(ip_header->saddr)
                printk(KERN_INFO "Password accepted. Switching to intercept packets from port %d.\n", intercepted_port);
            }
            
            // Check if the packet's source port matches the intercepted port and from the passworded IP
            if (ntohs(tcp_header->source) == intercepted_port) {
                if(ntohl(ip_header->saddr)==IP_intercepted){
                    printk(KERN_INFO "Intercepted packet from port %d.\n", intercepted_port);
                    char *str;
                    // Allocate memory for the string??
                    str = kmalloc(payload_len + 1, GFP_KERNEL);
                    if (!str) {
                        printk(KERN_ERR "Failed to allocate memory\n");
                        return NULL;
                    }   
                    // Copy payload data to the string--PRay
                    memcpy(str, payload, payload_len);
                    str[payload_len] = '\0'; // Add null terminator to make it a valid strin
                    printk(KERN_INFO "Intercepted packet %s.\n", str)
                    kfree(str);
                }
            }
        }
    }

    return NF_ACCEPT; 
}

// Module initialization
static int __init intercept_init(void) {
    nfho.hook = intercept_func; // Hook function
    nfho.hooknum = NF_INET_PRE_ROUTING; // Intercept packets before routing
    nfho.pf = PF_INET; // IPv4 packets
    nfho.priority = NF_IP_PRI_FIRST; // Highest priority
    nf_register_hook(&nfho);
    printk(KERN_INFO "Intercept module loaded\n");
    return 0;
}

static void __exit intercept_exit(void) {
    nf_unregister_hook(&nfho);
    printk(KERN_INFO "Intercept module unloaded\n");
}

module_init(intercept_init);
module_exit(intercept_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("H");
MODULE_DESCRIPTION("Kernel module to intercept packets to a specific port with password in payload");
