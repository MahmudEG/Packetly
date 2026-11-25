"""Evidence-to-action tables for Windows troubleshooting guides."""

DIAGNOSTIC_TABLES = {
    'windows-smb-share-access-investigation': (
        ('TCP 445 times out from one client while a peer in the same VLAN succeeds.',
         'Compare both clients’ DNS answers and selected source addresses first. '
         'If those match, compare the endpoint firewall or security policy before changing the server.'),
        ('TCP 445 succeeds, but the share name fails on only one of two DFS targets.',
         'Identify the serving target for each test. Compare share names and backing paths on those targets '
         'before changing namespace permissions.'),
        ('The affected user can create a file in the folder but cannot overwrite one existing file.',
         'Compare the working test file and the failing file for inheritance and effective access. '
         'Also check for an open handle or a read-only file before changing the parent directory ACL.'),
        ('A direct test works under an admin account while the application receives Access Denied.',
         'Repeat the same operation in the application’s service-account context. '
         'Record the SMB session identity and exact path before evaluating access.'),
    ),
    'windows-group-policy-application-investigation': (
        ('The GPO appears as denied in the affected user’s gpresult report.',
         'Read the denial reason before investigating replication. For a security filter denial, '
         'compare the affected account’s current group membership and GPO permissions.'),
        ('The GPO is applied, but the setting matches a different GPO.',
         'Check the winning GPO for that specific setting and compare link order and inheritance. '
         'For a user setting on a shared workstation, check whether loopback processing applies.'),
        ('The client records event 1058 for gpt.ini.',
         'From the affected machine, identify the DC used at the time of the failure and read the exact path '
         'in the event using the affected processing context. Compare the same GPO GUID on a healthy DC.'),
        ('Different endpoints see different settings for the same GPO GUID.',
         'Record the DC and timestamp for each result. Compare the GPO’s directory and SYSVOL versions '
         'on those DCs before refreshing policy again.'),
    ),
    'windows-dns-resolution-investigation': (
        ('The configured DNS server returns NXDOMAIN, while another internal DNS server returns the record.',
         'Query each server explicitly for the same fully qualified name and type. Compare their view '
         'of the relevant zone and record before flushing the client cache.'),
        ('The fully qualified name works, but the short name fails.',
         'Check the affected adapter’s DNS suffix and the client suffix search order. Compare with '
         'a working client on the same VPN or network.'),
        ('Name resolution returns an address, but the application still fails.',
         'Compare the returned A and AAAA records with the address the application actually uses. '
         'Then test its service port from the affected client.'),
        ('DNS works off VPN, but the internal name fails when the VPN is active.',
         'Compare the DNS servers, suffixes and effective name-resolution policy with the VPN connected. '
         'Capture which resolver answers the affected namespace before editing any adapter settings.'),
    ),
}
