"""Merge existing editorial expansions and incident cases into the Pages dataset."""
from cases import CASES
from case_details import DETAILS
from expansions import EXTRA
from new_guides import NEW_GUIDES
import math

BASE_NOTES = {
    'get system arp': 'Match the directly connected next hop to its IP and MAC address. Entries can age out when idle; a missing entry alone does not prove a fault. Compare the relevant interface and generate only an approved test before sampling again.',
    'show inventory': 'Record chassis, module and transceiver identities so the incident is tied to the correct hardware. Inventory presence does not establish operational health. Serial numbers can be sensitive; retain them in the internal ticket only.',
    'diagnose ip route list': 'Inspect the kernel forwarding entries for the affected destination and compare them with the routing-table output. Note prefix, interface and gateway. Differences require checking the active VDOM and routing context before drawing conclusions.',
    'diagnose vpn ipsec status': 'Inspect IPsec processing statistics and compare two timed samples during an approved test. Global counters may include multiple tunnels; correlate them with the named tunnel details instead of treating them as proof about one connection.',
    'show spanning-tree': 'Identify the root bridge, VLAN or instance and the uplink port roles. A blocked alternate path can be correct loop prevention. Investigate an unexpected root or role against the topology rather than trying to force a blocked port into forwarding.',
    'get system performance status': 'Capture CPU, memory, uptime and traffic/session indicators during the incident and again after a measured interval. A brief utilization spike and sustained pressure are different findings; compare with the same appliance under normal load.',
    'show ip protocols': 'Identify active routing protocols, advertised networks and known routing sources. Compare the expected protocol and neighbor information with the design. This summary does not prove that a particular destination was installed in the forwarding table.',
    'show lldp neighbors detail': 'Compare the remote chassis identity and port ID with the local uplink and cabling record. LLDP advertisements describe what the neighbor reports; stale entries or disabled discovery can complicate interpretation, so confirm the physical path separately.',
    'ss -tuln': 'Read the local address and port for TCP listeners and bound UDP sockets. A loopback-only listener cannot accept remote traffic. UDP does not establish a TCP-style listening session, and a bound socket alone does not prove the application is responding.',
}


def enrich(sheets):
    for s in sheets:
        title, symptom, order, interpretation, verification = CASES[s['id']]
        command, purpose, explanation = EXTRA[s['id']]
        if command not in [r[0] for r in s['rows']]:
            s['rows'].append([command, purpose])
            if s.get('walkthrough') is not None:
                s['walkthrough'].append(explanation)
        if not s.get('walkthrough'):
            notes = {s['rows'][index][0]: detail
                     for index, detail in zip(order, DETAILS[s['id']])}
            notes.update(BASE_NOTES)
            notes[command] = explanation
            s['walkthrough'] = [notes[row[0]] for row in s['rows']]
        s.setdefault('scope', {
            'Fortinet': 'FortiOS 7.4 inspection reference. Confirm your firmware, privileges and active VDOM; command availability varies by platform.',
            'Cisco': 'Cisco IOS / IOS XE inspection reference. Confirm device model, release and EXEC privileges; switch-specific commands may not exist on routers.',
            'Linux': 'Linux with iproute2. Some process and interface details require elevated read privileges.',
            'Vendor neutral': 'Provider-neutral networking concepts. This sheet contains reference concepts rather than executable shell commands.',
        }[s['vendor']] if s['vendor'] in ('Fortinet', 'Cisco', 'Linux', 'Vendor neutral') else '')
        s.setdefault('prerequisites', 'Confirm the target device and software release using approved access. Replace angle-bracket placeholders with local values; do not paste placeholders literally. Record the incident time and affected traffic path before collecting output.')
        s['case'] = dict(title=title, symptom=symptom,
                         steps=[dict(action=s['rows'][i][0], purpose=s['rows'][i][1],
                                     detail=DETAILS[s['id']][n] if s['id'] in DETAILS
                                     else s['walkthrough'][i])
                                for n, i in enumerate(order)],
                         interpretation=interpretation, verification=verification)
        s['updated'] = '2026-11-02'
    sheets.extend(NEW_GUIDES)
    for s in sheets:
        words = len(' '.join(s['walkthrough']).split())
        words += len(str(s['case']).split())
        s['time'] = max(6, math.ceil(words / 160))
    return sheets
