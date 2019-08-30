#
# Copyright (c) 2011-2013 by Teradata Corporation. All rights reserved.
#
# For more information, please see COPYRIGHT in the top-level directory.
#

"""
Hadoop upgrade utilities
"""

import os
import time
import sys
import shutil
import subprocess
# local imports
import cliutils.configfile
import cliutils.misc
import cliutils.output as output
import cliutils.table as table
from AmbariControl import AmbariControl, AmbariControlError, AmbariUnavailable
import ambari
import pgmanage
import system
import section
import log
from socket import getfqdn
import plugins.config
import re

pluginVersion = "1.0"
nodefile = "/var/opt/teradata/hadoop-tools/nodelist"

# Thresholds in MB for disk space checks. Set from input of Hadoop GSC
SLES11_PARTITIONS = [

    {
        'name': '/',        # Partition size = 20 GB or 30 GB
        'warn': 7500,       # Warn when 7.5 GB free space left
        'error': 7000       # Error when 7 GB free space left
    },
    {
        'name': '/var',     # Partition size = 5 GB or 4.8 GB
        'warn': 1000,       # Warn when 1 GB free space left
        'error': 500        # Error when 500 MB free space left
    },
    {
        'name': '/var/opt/teradata',    # Partition size = 756 GB
        'warn': 10000,                  # Warn when 10 GB free space left
        'error': 5000                   # Error when 5 GB free space left
    }

]

SLES12_PARTITIONS = [

    {
        'name': '/',    # Partition size = 50 GB
        'warn': 7500,   # Warn when 7.5 GB free space left
        'error': 7000   # Error when 7 GB free space left
    },
    {
        'name': '/var',     # Partition size = 50 GB
        'warn': 1000,       # Warn when 1000 MB free space left
        'error': 500        # Error when 500 MB free space left
    },
    {
        'name': '/tmp',     # Partition size = 50 GB
        'warn': 5000,       # Warn when 5 GB free space left
        'error': 1000       # Error when 1 GB free space left
    },
    {
        'name': '/var/opt/teradata',    # Partition size = 756 GB
        'warn': 10000,                  # Warn when 10 GB free space left
        'error': 5000                   # Error when 5 GB free space left
    }

]

def getSection():
    s = section.Section('Hadoop upgrade functions')
    s.addWriteCmd('ambari', '', r'.*', 'Upgrade Ambari', ambari.upgrade_ambari)
    s.addWriteCmd('register_hdp', '', r'.*', 'Register New HDP Stack in Ambari', ambari.register_hdp)
    s.addWriteCmd('postgresql', '<postgresql-tarball.tar.gz>', r'.*', 'Upgrade PostgreSQL', pgmanage.upgrade_postgresql)
    s.setHidden(False)
    return s


def run_pdsh(command, getrc=True, logfile=None, nodes=None, timeout=900):
    """
    :param command: command to run on node list
    :param getrc: if set to False this command will not get the return code of pdsh,
                it will show 0 regardless of success.
    :param logfile: This is the file that stdout and stderr will write to.
                If not defined STDOUT is not show but STDERR is.
    :param nodes: a custom node list can be passed, otherwise will use the all node list based off nodeList file.
    :param timeout: a custom timeout value can be passed, else defaults to 900 seconds.
    :return: returns return code from Pdsh(affected by getRC parameter)
    """

    # verify pdsh exists on the node
    try:
        system.requireInPath("pdsh")
    except cliutils.misc.BadEnvironmentException:
        log.ERROR("pdsh is not installed on this node.")
        raise
    # Append additional options to ssh
    os.environ['PDSH_SSH_ARGS_APPEND'] = "-q -o StrictHostKeyChecking=no -o GlobalKnownHostsFile=/dev/null -o " \
                                         "UserKnownHostsFile=/dev/null -o CheckHostIP=no -o Batchmode=yes"
    # if no custom node list is given, use the nodeList stored in nodefile
    if nodes is None:
        nodes = getnodelist(nodefile)
    # if getRC is true, pass the -S flag to pdsh, which returns the highest exit code from any pdsh process
    if getrc:
        cmd = "pdsh -u {0} -S -R ssh -w {1} {2}" .format(timeout, ",".join(nodes), command)
        log.DEBUG(cmd)
    # otherwise get no return code from pdsh
    else:
        cmd = "pdsh -u {0} -R ssh -w {1} {2}" .format(timeout, ",".join(nodes), command)
        log.DEBUG(cmd)
    # if logFile is defined, write to it. create timestamped copy of old version if the file exists already.
    if logfile is not None:
        if os.path.isfile(logfile):
            timestr = time.strftime("%Y%m%d-%H%M%S")
            tmpfile = logfile + "." + timestr + ".bak"
            log.DEBUG("{0} already exists, moving old copy to {1}" .format(logfile, tmpfile))
            shutil.copyfile(logfile, tmpfile)
        userlog = True
    else:
        logfile = "/tmp/runPdsh-cmd.out"
        userlog = False
    try:
        fout = open(logfile, 'w')
        sys.stdout.write("Running pdsh command: {0}" .format(command))
        sys.stdout.flush()
        log.DEBUG("Execute: {0}" .format(cmd))
        pdshcmd = subprocess.Popen(cmd.split(), stdout=fout, stderr=fout)
        time.sleep(1)
        while pdshcmd.poll() is None:
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(2)
        sys.stdout.write("\n")
        fout.close()
        # print location output saved to if logFile was given
        if userlog:
            log.INFO("Saved output to {0}" .format(logfile))
        if pdshcmd.returncode != 0:
            # log and display error if returncode is bad
            log.ERROR("Return code {0} for pdsh command: {1}" .format(pdshcmd.returncode, command))
            with open(logfile, 'r') as fin:
                print fin.read()
        return pdshcmd.returncode
    except OSError as e:
        print e
        log.ERROR("Failed to execute pdsh command: {0}" .format(command))
        raise


def getnodelist(filename):
    nodes = [line.rstrip('\n') for line in open(filename)]
    return nodes


def savenodelist():
    log.INFO("Saving node list to %s" % nodefile)
    if os.path.isfile(nodefile):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        tmpfile = nodefile + "." + timestr + ".bak"
        log.DEBUG("%s already exists, moving old copy to %s" % (nodefile, tmpfile))
        shutil.copyfile(nodefile, tmpfile)
    nodes = cliutils.misc.collectNodes()
    outfile = open(nodefile, 'w')
    for node in nodes:
        outfile.write("%s\n" % node)
    outfile.close()
    return True


def preflight(upgrade_ambari=False, register_hdp=False, upgrade_postgresql=False):
    """
    :param upgrade_ambari: Boolean indicating whether or not this function is being ran during an Ambari upgrade
    :param register_hdp: Boolean indicating whether or not this function is
                         being ran while registering new HDP version in Ambari
    :param upgrade_postgresql: Boolean indicating whether or not this function is being ran during a PostgreSQL upgrade

    Function to run various system checks to ensure cluster health including:

        - Verify that the Ambari server is running
        - Verify that all nodes in the cluster can be pinged
        - Verify that passwordless SSH is configured
        - Verify umask is set to 0022
        - Verify that all zypper repositories are healthy
        - Verify that installed Ambari and HDP zypper repositories have default values
        - Verify that all required python packages are installed
        - Check for disk space shortage
        - Verify hostnames match from 'hostname -f', '/etc/HOSTNAME' and 'hosts' table in postgreSQL cmf database
        - Verify checksum from /etc/hosts matches on all nodes
        - Check and warn if multiple Hadoop versions are installed
        - Check if any services are currently configured to log to /var/log
        - Check and error if there are custom files or directories in /usr/hdp

    :return: Tuple consisting of three values:
        - Boolean representing whether or not all checks passed
        - Integer representing the number of warnings that occurred
        - Integer representing the number of errors that occurred

    """
    local_hostname = getfqdn()

    conf = plugins.config.getInstallConf()
    master_node1 = conf.get('MASTER1')
    client = AmbariControl()
    hosts = client.get_all_hosts()

    # Determine Ambari repository name
    # Determine HDP repository name
    # Determine HDP Utils repository name

    # Check that the pre-flight check is being executed on Master Node #1
    if local_hostname.lower() != master_node1.lower():
        raise cliutils.misc.BadEnvironmentException("This command must run on Master Node 1")

    log.INFO("Running cluster health tests")
    error_count = 0
    warning_count = 0

    # Verify that zypper repositories for current HDP/Ambari versions have default values
    ambari_repo_alias = ""
    hdp_repo_alias = "HDP-2.3.4.0"
    hdp_utils_repo_alias = ""
    hdp_2_3_repo = {"Name": "HDP",
                    "URI": "http://n4-1-1.labs.teradata.com/HDP/suse11sp3/2.x/updates/2.3.4.0",
                    "Enabled": "Yes",
                    "Priority": "1",
                    "Auto-refresh": "No",
                    "Type": "rpm-md",
                    "GPG Check": "Off",
                    }
    if validate_zypper_repo(hdp_repo_alias, hdp_2_3_repo, master_node1):
        log.INFO("success")
    else:
        log.INFO("failure")
    exit(0)

    log.INFO("Testing 'source /etc/profile'")
    for node in plugins.config.getAllNodes():
        command = "source /etc/profile"
        cmd = cliutils.misc.getSshCmd(node, command)
        ret, res, err = cliutils.misc.runCmdGetOutput(cmd)
        if err:
            log.ERROR("The execution of the command: '{0}' has failed on node: {1} with the error message:{2}".
                      format(command, node, err))
            error_count += 1

    log.INFO("Verifying that Ambari Server is up and running")
    cmd = ["ambari-server", "status"]
    response, out, _ = cliutils.misc.runCmdGetOutput(cmd)
    print os.linesep.join([s for s in out.splitlines() if s])
    if response is not 0:
        error_count += 1
    try:
        AmbariControl()
    except AmbariUnavailable as e:
        print e
        log.FATAL("Cannot proceed unless the Ambari Server is running. Exiting...")
        exit(1)

    # Get hostnames of cluster's hosts
    savenodelist()
    nodes = getnodelist(nodefile)

    log.INFO("Verifying that all nodes in the cluster can be pinged")
    for node in nodes:
        cmd = ["/bin/ping", "-c 1", "%s" % node]
        response, out, _ = cliutils.misc.runCmdGetOutput(cmd)
        log.INFO("Testing connection to %s" % node)
        if response is not 0:
            log.ERROR("Cannot ping %s. Please check if the node is up." % node)
            error_count += 1

    log.INFO("Verifying passwordless SSH is configured")
    for node in nodes:
        ssh_failure_hosts = []
        log.INFO("Testing passwordless SSH functionality by SSHing to all the other nodes from '{0}'"
                 .format(node))
        command = "hcli node runonall date"
        cmd = cliutils.misc.getSshCmd(node, command)
        response, out, _ = cliutils.misc.runCmdGetOutput(cmd)
        for line in out.split('\n'):
            if re.search(r'Running', line):
                log.DEBUG("{0}".format(line))
        if response is not 0:
            for line in out.split('\n'):
                if re.search(r'ERROR: Could not connect to', line):
                    # Get only the hostname from the output and remove the last character '.'
                    ssh_failure_hosts.append(line.rsplit(' ', 1)[1][:-1])
            if not ssh_failure_hosts:
                ssh_failure_hosts = "All Hosts"
            else:
                ssh_failure_hosts = ','.join(ssh_failure_hosts)
            log.ERROR("Passwordless SSH failed: Unable to ssh from '{0}' to '{1}'".format(node, ssh_failure_hosts))
            error_count += 1

    if response == 0:  # Skip this test if the passwordless SSH test fails
        log.INFO("Verifying host keys in all nodes")
        node_list_str = ' '.join(nodes)
        cmd = 'for i in {0}; do ssh -o BatchMode=yes -l root "$i" date; done'.format(node_list_str)
        response = run_pdsh(cmd, True)
        if response is not 0:
            log.ERROR("The execution of the command '{0}' has failed on at least one host.\n"
                      "Please run 'hcli support establish_trust' to fix cluster host keys".format(cmd))
            error_count += 1
        else:
            log.INFO("Host key verification was successful in all nodes")

    log.INFO("Verifying umask settings")
    for node in nodes:
        command = "umask"
        cmd = cliutils.misc.getSshCmd(node, command)
        response, out, err = cliutils.misc.runCmdGetOutput(cmd)
        if response != 0:
            log.ERROR("The execution of the command '%s' has failed on host '%s': %s" % (command, node, err))
            error_count += 1
        elif out.strip() != "0022":
            log.ERROR("umask in local environment on {0} is {1}, but should be set to 0022".format(node, out.strip()))
            error_count += 1

    log.INFO("Verifying that proxy servers are disabled in /etc/sysconfig/proxy on all nodes")
    proxy_configured = False
    command = "grep ^PROXY_ENABLED /etc/sysconfig/proxy | cut -d \"=\" -f2 | tr -d '\"'"
    for node in nodes:
        cmd = cliutils.misc.getSshCmd(node, command)
        response, out, err = cliutils.misc.runCmdGetOutput(cmd)
        if response != 0:
            log.ERROR("The execution of command {0} failed on host {1}".format(command, node))
            error_count += 1
        else:
            if out.strip().lower() == "yes":
                log.ERROR("A proxy server is enabled in host {0}".format(node))
                proxy_configured = True
                error_count += 1
    if proxy_configured:
        log.INFO("Proxy servers are known to cause issues during Change Control activities, including being able to "
                 "refresh zypper repositories or Hadoop service checks failing. With the permission of the customer, "
                 "follow KCS019598 to temporarily disable the use of a proxy server on the affected nodes. The "
                 "setting may be disabled for the duration of the Change Control activity, and re-enabled "
                 "afterwards if the customer desires.")

    log.INFO("Verifying that all zypper repositories are healthy")
    zypper_health_commands = [
        "zypper --no-gpg-check refresh",
        "zypper --no-gpg-check verify",
        "zypper --no-gpg-check verify | grep 'Dependencies of all installed packages are satisfied.'"
    ]
    for cmd in zypper_health_commands:
        response = run_pdsh(cmd, True)
        if response != 0:
            log.ERROR("The execution of the command '%s' has failed on at least one host" % cmd)
            error_count += 1

    if upgrade_ambari or register_hdp:
        log.INFO("Verifying all required python packages are installed")
        os_version = ambari.get_os_version()
        if not os_version:
            log.ERROR("Unsupported OS version: No version detected")
            error_count += 1
            return False, warning_count, error_count
        elif os_version == "12":
            python_packages = ("python", "python-argparse", "python-base", "python-curses", "python-tk",
                               "python-xml", "rpm-python")
        elif os_version == "11":
            python_packages = ("python", "python-argparse", "python-base", "python-curses", "python-devel",
                               "python-mysql", "python-tk", "python-xml", "rpm-python")
        for node in nodes:
            command = "zypper -q se --installed-only --match-exact {0} 2>/dev/null " \
                      "| grep package " \
                      "| sort " \
                      "| uniq " \
                      "| grep -v \"No packages found.\"| " \
                      "wc -l".format(' '.join(python_packages))
            cmd = cliutils.misc.getSshCmd(node, command)
            response, out, err = cliutils.misc.runCmdGetOutput(cmd)
            if response == 0:
                missing_packages = len(python_packages) - int(out)
                if missing_packages != 0:
                    log.ERROR("Missing {0} python package(s) on host {1}"
                              "\nVerify the following packages are installed on host {1}"
                              "\n{2}".format(missing_packages, node, python_packages))
                    error_count += 1
            else:
                log.ERROR("The execution of the command '{0}' failed".format(' '.join(cmd)))
                error_count += 1

    # Check if there is enough disk space available and warn/error as per the specified thresholds
    disk_space_error_counter = 0
    disk_space_warn_counter = 0
    log.INFO("Verifying there is enough disk space available")
    for node in nodes:
        # Determine partition map as per running OS version
        os_version = ambari.get_os_version()
        if not os_version:
            log.ERROR("Unsupported OS version: No version detected")
            error_count += 1
            return False, warning_count, error_count
        elif os_version == "12":
            # Check if node was upgraded from SLES 11 by checking if /var is 5GB or less
            command = "df -h /var"
            cmd = cliutils.misc.getSshCmd(node, command)
            response, out, err = cliutils.misc.runCmdGetOutput(cmd)
            if response != 0:
                log.ERROR("The execution of the command '{0}' has failed on host '{1}': {2}".format(command, node, err))
                error_count += 1
                return False, warning_count, error_count
            else:
                list_of_lines = out.splitlines()
                var_line = list_of_lines[1]
                var_size = var_line.split()[1]
                var_value = float(var_size[:-1])
                if var_value <= 5.0:
                    partition_maps = SLES11_PARTITIONS
                else:
                    partition_maps = SLES12_PARTITIONS
        elif os_version == "11":
            partition_maps = SLES11_PARTITIONS

        command = "df -m"
        cmd = cliutils.misc.getSshCmd(node, command)
        response, out, err = cliutils.misc.runCmdGetOutput(cmd)
        if response != 0:
            log.ERROR("The execution of the command '{0}' has failed on host '{1}': {2}".format(command, node, err))
            error_count += 1
        else:
            list_of_lines = out.splitlines()
            for line in list_of_lines:
                # Clean headers from output of df -m
                if line.startswith("Filesystem"):
                    continue
                available_space = int(line.split()[3])
                partition = line.split()[5]
                for partition_map in partition_maps:
                    if partition == partition_map['name']:
                        if available_space <= partition_map['error']:
                            log.ERROR("{0} on node {1} has {2} MB available".format(partition, node, available_space))
                            disk_space_error_counter += 1
                            error_count += 1
                        elif available_space <= partition_map['warn']:
                            log.WARN("{0} on node {1} has {2} MB available.".format(partition, node, available_space))
                            disk_space_warn_counter += 1
                            warning_count += 1
    if disk_space_error_counter > 0:
        log.ERROR("There was at least one disk space check error. If this command is being executed as part of a Change"
                  " Control's \"Pre Operation Procedure\" step or is otherwise being ran outside of a maintenance "
                  "window, please open a S3 incident and collaborate it to the GSO Hadoop PST. If this command is "
                  "being executed inside a maintenance window, please open a S2 incident and engage the GSO Hadoop PST")
        error_count += 1

    elif disk_space_warn_counter > 0:
        log.WARN("There was at least one disk space check warning. If this command was executed within a maintenance "
                 "window, you may continue with the Change Control template. Please open a S3 incident with the GSO "
                 "Hadoop PST to clear disk space issues")
        warning_count += 1

    if not system.is_hpe_vm():
        log.INFO("Verifying storage configuration on data nodes")
        command = "hcli support checkDisks"
        cmd = cliutils.misc.getSshCmd(master_node1, command)
        ret, out, err, = cliutils.misc.runCmdGetOutput(cmd)
        if ret != 0:
            log.ERROR("The execution of the command '{0}' has failed on host '{1}': {2}".format(command, master_node1,
                                                                                                err))
            error_count += 1
        else:
            list_of_lines = out.splitlines()
            for line in list_of_lines:
                if "DATA" in line:
                    # Split by space, using odd numbers in the list to get values on the checkDisks table
                    splitted_line = line.split()
                    if "Online" not in splitted_line:
                        host, volume, volume_id, = splitted_line[1], splitted_line[3], splitted_line[5]
                        log.ERROR("Volume {0} with ID {1} is not online on host {2}".format(volume, volume_id, host))
                        error_count += 1

    log.INFO("Verifying the ability to execute commands on all hosts in the cluster")
    cmd = ["hcli", "node", "runonall", "date"]
    response, out, _ = cliutils.misc.runCmdGetOutput(cmd)
    if response is not 0:
        log.ERROR("The execution of the command 'hcli node runonall date' has failed:\n{0}".format(out))
        error_count += 1

    # Checking hostname mismatch from output of `hostname -f`, /etc/HOSTNAME, and Ambari Postgres 'hosts' table
    etc_hostname_lst = []
    hostname_f_lst = []
    hostname_f_cmd = "hostname -f"
    cat_etc_hostname_cmd = "cat /etc/HOSTNAME"

    log.INFO("Checking hostname mismatch on all nodes from \'hostname -f\', /etc/HOSTNAME, and Ambari Postgres "
             "\'hosts\' table")
    # Get outputs from `hostname -f` and `cat /etc/HOSTNAME` from all nodes
    for host in hosts:
        cmd = cliutils.misc.getSshCmd(host, hostname_f_cmd)
        response, out, err = cliutils.misc.runCmdGetOutput(cmd)
        if response is not 0:
            log.ERROR(
                "Unable to determine the hostname. The following command failed on host {0}: {1}.".format(host, cmd))
            error_count += 1
        hostname_f_lst.append(out.rstrip())

        cmd = cliutils.misc.getSshCmd(host, cat_etc_hostname_cmd)
        response, out, err = cliutils.misc.runCmdGetOutput(cmd)
        if response is not 0:
            log.ERROR(
                "Unable to determine the hostname. The following command failed on host {0}: {1}.".format(host, cmd))
            error_count += 1
        etc_hostname_lst.append(out.rstrip())

    # Get host_name and public_hostname values from Postgres DB. If .pgpass is missing prompt the user for the
    # PostgreSQL password. If the user does not have the postgres password, they are given the option to skip the
    # hostname check. If a hostname mismatch is encountered, print an error and a table with hostnames
    ignore_check = False
    pg_password = None

    if not ambari.pgpass_exists():
        answer = cliutils.misc.query_yes_no(
            "The Postgres password is needed to perform this hostname check. If you "
            "have the Postgres password in hand, type 'Y' to continue with this "
            "hostname check. Otherwise, type 'n' to ignore (Default:Y)")
        if answer == 'yes':
            pg_password = ambari.get_postgres_password()
        if answer == 'no':
            ignore_check = True

    if not ignore_check:
        postgres_hosts_lists = ambari.get_ambari_database_hosts_table(master_node1, pg_pass=pg_password)
        if postgres_hosts_lists:
            host_name_lst = postgres_hosts_lists[0]
            public_host_name_lst = postgres_hosts_lists[1]

            if set(etc_hostname_lst) == set(hostname_f_lst) == set(host_name_lst) == set(public_host_name_lst):
                log.INFO("No hostname mismatch encountered between \'hostname -f\', /etc/HOSTNAME, and Ambari Postgres "
                         "\'hosts\' table")
            else:
                log.ERROR("Hostnames do not match. Please analyze the following table and resolve outstanding hostname "
                          "issues")
                error_count += 1

                # Sort lists since they are unordered in the ambari postgres hosts table, and print them into a table
                etc_hostname_lst.sort()
                hostname_f_lst.sort()
                host_name_lst.sort()
                public_host_name_lst.sort()
                t = table.Table(
                    headers=["hostname -f", "/etc/HOSTNAME", "host_name from hosts", "public_host_name from hosts"])
                for i in range(len(hostname_f_lst)):
                    t.addRow([hostname_f_lst[i], etc_hostname_lst[i], host_name_lst[i], public_host_name_lst[i]])
                t.printTable()
                output.printResult()
        else:
            log.ERROR("Error trying to connect to get values from the ambari Postgres database hosts table")
            error_count += 1
    else:
        log.WARN("No Postgres password provided. Ignoring hostname service check")
        warning_count += 1

    # Compare checksum of network-related files, warn and print a table if they differ
    file_paths = [
        '/etc/hosts',
        '/etc/resolv.conf'
    ]
    for file_path in file_paths:
        if not get_checksum(file_path, hosts):
            log.WARN("Checksum of {0} does not match on all hosts or command was not executed properly on at least "
                     "one host. Mismatch of this file between different hosts may be expected depending on different "
                     "network configurations. Although, it is common to see an issue caused by conflicting entries in "
                     "the {0} file. If a network issue is encountered in the future, analyze {0} differences on all "
                     "hosts".format(file_path))
            warning_count += 1

    # Check and warn if multiple Hadoop versions are installed
    log.INFO("Checking installation of multiple Hadoop versions")
    command = "zypper se -i hadoop*-hdfs"
    versions_counter = 0
    cmd = cliutils.misc.getSshCmd(master_node1, command)
    response, out, err = cliutils.misc.runCmdGetOutput(cmd)
    if response != 0:
        log.ERROR(
            "The execution of the command '{0}' has failed on host '{1}': {2}".format(command, master_node1, err))
        error_count += 1
    else:
        for line in out.split('\n'):
            # Only capture lines with hadoop<version>-hdfs and increase the versions counter
            if re.search(r'hadoop.+-hdfs', line):
                versions_counter += 1

    if versions_counter == 1:
        log.INFO("Only one version of Hadoop is installed")
    elif versions_counter > 1:
        log.WARN("There are multiple Hadoop versions installed on this cluster. Please open a S4 incident and "
                 "send a collaboration request to the GSO Big Data team to remove unused Hadoop versions. Please "
                 "associate Knowledge Article KCS007878 to the incident")
        warning_count += 1
    else:
        log.ERROR("No Hadoop versions detected when executing '{0}'".format(command))
        error_count += 1

    # Check if any services are currently configured to log to /var/log
    log.INFO("Checking if Hadoop services are logging to /var/log")
    prop_sets = client.get_propsets()
    log_dirs_flagged = {}
    for prop_set in prop_sets:
        prop_set_configs = client.get_propset(prop_set, skip_not_found=True)
        if prop_set_configs:
            for prop, val, in prop_set_configs.iteritems():
                if "log_dir" in prop and val.startswith("/var/log"):
                    log_dirs_flagged[prop] = {
                        'prop_set': prop_set,
                        'path': val,
                        'size_mb': {}
                    }

    # Check if flagged log directories exist and take up > 1 MB of space on each host
    log_dirs_warn_counter = 0
    for host in hosts:
        for prop, val in log_dirs_flagged.iteritems():
            directory_space_cmd = "du -s --block-size=1MB {0}".format(val['path'])
            directory_space_ssh_cmd = cliutils.misc.getSshCmd(host, directory_space_cmd)
            response, out, err = cliutils.misc.runCmdGetOutput(directory_space_ssh_cmd)
            if response == 0 and "No such file or directory" not in out:
                dir_size_mb = int(out.split()[0])
                if dir_size_mb > 1:
                    log_dirs_flagged[prop]['size_mb'][host] = dir_size_mb
                    if dir_size_mb >= 1024:
                        dir_size_str = "{0} GB".format(round(float(dir_size_mb) / 1024, ndigits=2))
                    else:
                        dir_size_str = "{0} MB".format(dir_size_mb)
                    log.WARN("{0} takes up ~{1} on {2} ({3} -> {4})"
                             .format(val['path'], dir_size_str, host, val['prop_set'], prop))
                    log_dirs_warn_counter += 1
                    warning_count += 1
    if log_dirs_warn_counter:
        log.INFO("Consider updating log directory properties using HCLI or Ambari so logs are written to "
                 "/var/opt/teradata instead of /var/log. See KCS019430 for instructions.")

    # Check and error if there are custom files or directories in /usr/hdp
    usr_hdp_dir = "/usr/hdp"
    ls_command = "ls {0}".format(usr_hdp_dir)
    custom_files_dirs_in_usr_hdp = False
    log.INFO("Checking for custom files or directories in {0}".format(usr_hdp_dir))
    for host in hosts:
        ls_command_ssh = cliutils.misc.getSshCmd(host, ls_command)
        response, out, err = cliutils.misc.runCmdGetOutput(ls_command_ssh)
        if response == 0 and "No such file or directory" not in out:
            list_of_files_and_dirs = out.split()
            for path in list_of_files_and_dirs:
                if path == "current":
                    continue
                # Search for HDP versions in string such as 2.6.0.3-8
                if re.search(r'^\d\.\d\.\d\.\d-\d+', path) is None:
                    log.ERROR("Non-standard file or directory found in {0} in host {1}: {2}"
                              .format(usr_hdp_dir, host, path))
                    custom_files_dirs_in_usr_hdp = True
                    error_count += 1
    if custom_files_dirs_in_usr_hdp:
        log.INFO("The contents of {0} should contain a directory named 'current', and one or more directories "
                 "named after HDP versions (e.g. 2.6.0.3-8). Check the contents of {0} on the affected host(s) "
                 "to see if any non-standard files/directories can be migrated or deleted.".format(usr_hdp_dir))
    else:
        log.INFO("No custom files or directories detected in {0}".format(usr_hdp_dir))

    # Check for old kernels
    log.INFO("Checking for unused kernel packages")
    running_kernel_cmd = "uname -r"
    unused_kernel_packages_cmd = "lskern -a"
    unused_kernels_detected = False
    unused_kernels_host_count = 0
    for host in hosts:
        # Check the current running kernel version
        running_kernel_ssh_cmd = cliutils.misc.getSshCmd(host, running_kernel_cmd)
        response, out, err = cliutils.misc.runCmdGetOutput(running_kernel_ssh_cmd)
        if response == 0:
            running_kernel_version = out.split("-default")[0]
        else:
            log.ERROR("Unable to detect current running kernel version on {0} using the following command: {1}"
                      .format(host, running_kernel_cmd))
            error_count += 1
            break

        # Check what kernel package versions are installed
        unused_kernel_versions = []
        unused_kernel_packages_ssh_cmd = cliutils.misc.getSshCmd(host, unused_kernel_packages_cmd)
        response, out, err = cliutils.misc.runCmdGetOutput(unused_kernel_packages_ssh_cmd)
        unused_kernel_packages_out = out.strip()
        if response == 0 and "Could not get next boot kernel version" not in unused_kernel_packages_out:
            if unused_kernel_packages_out:
                # Create list of detected versions
                index = 0
                unused_kernel_packages = [package for package in unused_kernel_packages_out.split("\n")]
                for package in unused_kernel_packages:
                    for index, char in enumerate(package):
                        if char.isdigit():
                            break
                    if index != 0:
                        unused_kernel_versions.append(package[index::])

                # Remove duplicates from list
                unused_kernel_versions = list(set(unused_kernel_versions))

                # Remove running kernel version from list
                for version in unused_kernel_versions:
                    if running_kernel_version in version:
                        unused_kernel_versions.remove(version)

            # Check if unused kernel package versions were detected
            if unused_kernel_versions:
                log.INFO("Unused kernel packages detected on {0}".format(host))
                unused_kernels_detected = True
                unused_kernels_host_count += 1
        else:
            log.ERROR("Unable to detect unused kernel packages on {0} using the following command: {1}"
                      .format(host, unused_kernel_packages_cmd))
            error_count += 1

    # Warn if unused kernel packages were detected
    if unused_kernels_detected:
        log.WARN("Unused kernel packages detected on {0} host(s). "
                 "To remove the unused kernel packages, please refer to KCS002416.".format(unused_kernels_host_count))
        warning_count += 1
    else:
        log.INFO("No unused kernel packages detected!")

    if error_count > 0:
        return False, warning_count, error_count
    else:
        log.OKGREEN("All cluster health tests have passed!")
        return True, warning_count, error_count


def validate_zypper_repo(repo_alias, repo_properties_dict, host):
    """
    :param repo_alias: zypper repository alias
    :param repo_properties_dict: dictionary of zypper repository properties and values
    :param host: host to validate zypper repository
    :return: True if zypper repository matches default values
             False if zypper repository does not match default values
    """

    command = "zypper lr {0}".format(repo_alias)
    cmd = cliutils.misc.getSshCmd(host, command)
    response, out, _ = cliutils.misc.runCmdGetOutput(cmd)

    if response == 0:
        if repo_alias not in out:
            log.INFO("Repository {0} does not exist in host {1}".format(repo_alias, host))
            return False

        # Creating dictionary from output of `zypper lr repo_alias` above
    else:
        log.ERROR("Failed to execute {0} in host {1}".format(command, host))
        return False

    exit(0)


def get_checksum(file_path, hosts_lst):
    """
    :param file_path: file to execute cksum command on
    :param hosts_lst: list of hosts to execute cksum command on
    :return: True if checksums match on all hosts
             False if there is a mismatch of checksums or if checksum command cannot be executed on at least one host

    Execute `cksum <file>` on a list of nodes. Return true if the checksums match. Return False and print a table with
    hosts and checksums if all results do not match
    """
    log.INFO("Comparing checksum of {0} on all hosts".format(file_path))
    cksum_cmd = "cksum {0}".format(file_path)
    cksum_set = set()
    cksum_hosts_dict = {}

    for host in hosts_lst:
        cmd = cliutils.misc.getSshCmd(host, cksum_cmd)
        response, out, err = cliutils.misc.runCmdGetOutput(cmd)
        if response is not 0:
            log.ERROR(
                "Unable to determine checksum of {0}. The following command failed on host {1}: {2}.".format(
                    file_path, host, cksum_cmd))
            # Add "Unknown" to cksum dictionary and set which will then cause the checksum compares to return False
            cksum_hosts_dict[host] = "Unknown"
            cksum_set.add("Unknown")
        else:
            cksum = out.split()[0]
            cksum_set.add(cksum)
            cksum_hosts_dict[host] = cksum

    # Get an element from cksum_set which will be used by the first check below
    elem = cksum_set.pop()
    cksum_set.add(elem)
    if len(cksum_set) == 1 and elem != "Unknown":
        log.INFO("Checksum of {0} matches on all hosts".format(file_path))
        return True
    elif len(cksum_set) == 0:
        log.ERROR("Unable to determine checksum of {0} on all hosts".format(file_path))
        return False
    else:
        t = table.Table(headers=['Host', 'Checksum'])
        # Sort by hostname
        key_lst = cksum_hosts_dict.keys()
        key_lst.sort()
        for k in key_lst:
            t.addRow([k, cksum_hosts_dict[k]])
        t.printTable()
        output.printResult()
        return False
