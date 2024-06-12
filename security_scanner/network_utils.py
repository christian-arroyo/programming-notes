def is_valid_ipv4_address(ip_address: str) -> tuple:
    if not isinstance(ip_address, str):
        return False, f"ip not a string: {ip_address}"
    parts = ip_address.split('.')
    if len(parts) != 4:
        return False, f"ip not a dotted quad: {ip_address}"
    for num_s in parts:
        try:
            num = int(num_s)
        except ValueError:
            return False, "ip dotted-quad components not all integers: {ip_address}"
        if num < 0 or num > 255:
            return False, f"ip dotted-quad component not between 0 and 255: {ip_address}"
    return True, ""


def is_valid_ipv4_list(ip_list: list) -> bool:
    for ip_address in ip_list:
        if not is_valid_ipv4_address(ip_address):
            return False
    return True
