for line in out.split('\n'):
    # Only capture lines that have an IP address
    if re.search(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', line):
        host_name_list.append((line.split('|')[0]).strip())
        public_hostname_list.append((line.split('|')[1]).strip())
