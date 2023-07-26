import re


def is_ip_with_mask(ip: str) -> bool:
    return bool(re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d+$', ip))


def is_public_ip(ip: str) -> bool:
    """
    Checks if the ip is a public ip
    it is not:
     * 10.0.0.0/8 => (10.0.0.0 – 10.255.255.255)
     * 172.16.0.0/12 => (172.16.0.0 – 172.31.255.255)
     * 192.168.0.0/16 => (192.168.0.0 – 192.168.255.255)
     * 169.254.0.0/16 => (169.254.0.0 – 169.254.255.255)
    :param ip:
    :return:
    """
    return not ip.startswith('10.') \
        and not re.match(r'^172\.(1[6-9]|2\d|3[0-1])\.', ip) \
        and not ip.startswith('192.168.') \
        and not ip.startswith('169.254.')


def is_broadcast_ip(ip: str) -> bool:
    return ip.startswith('255.255.255.255')

