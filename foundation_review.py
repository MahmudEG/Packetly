"""Specific teaching findings for the introductory guides, reviewed 2026-11-25.

All observations are constructed examples. No device access or lab execution is
implied. These cases teach how to discriminate between competing explanations.
"""

REVIEWS = {
 'fortigate-cli-essentials': {
  'evidence': 'Example observations: users report a short interruption at 09:10. A resource sample at 09:20 is normal, the expected default route is present, and the inspected interfaces are enabled. No resource sample or interface history from 09:10 has been collected.',
  'interpretation': 'The later healthy snapshot cannot explain the earlier interruption. The useful result is a gap in the incident timeline. Collect interface events and monitoring samples around 09:10, then separate a forwarding interruption from a resource problem. A present default route describes the current routing decision; it does not validate upstream DNS or the application.',
  'verification': 'Compare a timed resource baseline with the next affected interval and a controlled application test. Record whether the same users, interface and destination are affected. Close the incident against a documented repair and successful original operation, rather than a normal resource snapshot.',
  'details': [
   'Tie this incident to the recorded model, firmware and VDOM. A screenshot from another appliance would invalidate the comparison even if its hostname looked similar.',
   'Write the collection time next to the sample. A quiet period after the complaint is a baseline, not evidence that the firewall was healthy during the failure.',
   'Compare the expected inside and outside interfaces. Separate an enabled interface from a working physical link and from a valid downstream path.',
   'Record the selected destination prefix and next hop. If the route is present, carry the investigation toward the next hop and service instead of repeatedly collecting the same route table.'
  ],
 },
 'cisco-ios-essentials': {
  'evidence': 'Example observations from approved console access: the management SVI is up/up, its address matches the design, and the switch uplink is operational. A management session from the local subnet works, while one from the remote operations subnet times out.',
  'interpretation': 'This comparison narrows the failure to something that differs between the local and remote paths. It does not justify changing the SVI address. Compare the return route, management access restrictions and intervening network path for the remote source. An up/up interface establishes local interface state, not permission for remote administration.',
  'verification': 'After a scoped repair, repeat the same management protocol from both recorded source subnets. Confirm the device identity and expected access policy remain correct. Keep the before-and-after path evidence in the incident ticket.',
  'details': [
   'Record the chassis and release from the console session. Select command documentation for that device; do not infer its feature set from another switch in the site.',
   'Locate the management interface itself. Compare both status columns and the configured address before treating every down port as part of the incident.',
   'Inspect the actual uplink carrying management traffic. If its counters are stable across a timed interval, distinguish that result from the remote management timeout.',
   'Review the relevant addressing and management access configuration against the approved design. Avoid exporting the full configuration when a bounded excerpt answers the question.'
  ],
 },
 'fortigate-routing-arp': {
  'evidence': 'Example observations: the selected route points to an on-link gateway on port2. Two observations during an approved service test show an unresolved neighbor for that gateway. The remote destination itself is outside the directly attached subnet.',
  'interpretation': 'The next useful boundary is the local link to the gateway. Asking for an ARP entry for the remote destination would test the wrong assumption: routed traffic normally resolves its local next hop. Compare gateway ownership, interface/VLAN placement and the adjacent device. Neighbor failure does not by itself distinguish a cabling fault from a wrong gateway address.',
  'verification': 'After correcting the documented local problem, confirm the intended gateway resolves on the intended interface and the original service works. Check the return route separately. A newly populated neighbor table is useful evidence, but is not the final application test.',
  'details': [
   'Establish the selected egress interface before evaluating a neighbor. Compare the interface for this destination with the actual local subnet and topology.',
   'Use the most specific applicable destination route, not merely the existence of a default route. Preserve the selected prefix and gateway in the ticket.',
   'Look for the directly connected gateway and its interface. Do not expect the remote service address to appear as a local neighbor across a routed boundary.',
   'Compare two observations taken around an approved connection attempt. An idle missing entry is weaker evidence than repeated resolution failure while traffic needs that gateway.'
  ],
 },
 'cisco-interface-diagnostics': {
  'evidence': 'Example observations: the affected port stays up. Its input error count increases from 18 to 91 during one minute of the reported failure. A comparison port remains unchanged. The existing counter values before that minute are not treated as new errors.',
  'interpretation': 'The change during the complaint supports investigating the affected link. It does not prove which component is faulty. Compare the peer port, negotiated settings and the physical path. Change one approved component at a time so the next sample can distinguish the cable, transceiver or endpoint from the original state.',
  'verification': 'Record the counter interval and user test after the repair. Compare error growth under similar traffic; a quiet link can hide an unresolved problem. Confirm the original application remains usable and retain the old baseline rather than clearing counters just to make them look clean.',
  'details': [
   'Identify the affected port and its current administrative/operational state. Separate an intentionally disabled port from a live port that is dropping or corrupting traffic.',
   'Record the link mode and operational status alongside the endpoint identity. A neighboring port is a useful comparison only if its role and traffic are understood.',
   'Take two timestamped error samples on the same interface. Calculate the change during the incident instead of attributing a cumulative total to the current user complaint.',
   'Compare the interface description with the actual patched endpoint. If they disagree, confirm the cable path before testing or replacing the wrong device.'
  ],
 },
 'fortigate-vpn-health': {
  'evidence': 'Example observations during an approved test: the intended tunnel has an active IKE gateway and matching IPsec security associations. Transmit counters rise, while receive counters stay unchanged. Another tunnel on the firewall has unrelated bidirectional traffic.',
  'interpretation': 'This is evidence of a one-way observation on the intended tunnel, not proof that the remote firewall is broken. Ask the peer administrator to match the same test endpoints, time window and selectors. Compare remote receipt, destination service access and return routing. Global IPsec totals cannot replace counters for this specific tunnel.',
  'verification': 'Retest the application from the same authorized source and correlate traffic on both peers. Confirm the intended selectors and service path. A tunnel returning to an established state is insufficient if the original request still receives no response.',
  'details': [
   'Choose the named tunnel used by the affected source and destination. Several established tunnels can coexist; a healthy total does not identify this traffic path.',
   'Compare association details and counters before and after a controlled request. Record endpoints and timing so the other administrator can find the same exchange.',
   'Use IKE state to distinguish peer negotiation from the data path. An active gateway is useful context but cannot validate delivery to the protected application.',
   'Compare the route for the protected destination with the intended tunnel interface. If forwarding chooses another path, resolve that discrepancy before changing negotiation settings.'
  ],
 },
 'cisco-vlans-trunks': {
  'evidence': 'Example observations: an access port is assigned to VLAN 30, and VLAN 30 exists locally. The expected uplink is operational as a trunk, but VLAN 30 is missing from its allowed list on one end. A different VLAN crosses the same uplink successfully.',
  'interpretation': 'The discrepancy supports a VLAN-specific trunk investigation rather than a physical-link outage. Compare the approved allowed list and the peer end before changing configuration. VLAN existence, trunk permission and spanning-tree forwarding are different gates. A VLAN allowed on one switch does not establish that it is carried end to end.',
  'verification': 'After the approved trunk correction, check both ends, forwarding state and MAC learning for VLAN 30. Retest the workstation-to-gateway path. Also confirm a previously working VLAN still behaves as expected, so the repair has not displaced existing traffic.',
  'details': [
   'Confirm VLAN 30 is present and the workstation is on its intended access port. Keep the endpoint MAC and physical interface tied to the test.',
   'Read operational trunk information on the actual uplink. Compare the allowed, active and forwarding VLAN information instead of treating a configured trunk as sufficient.',
   'Compare administrative and operational switchport settings. An access/trunk expectation mismatch needs to be reconciled with the design at both ends.',
   'Use the learned MAC location to check whether frames from the test endpoint are reaching the expected port. A stale or absent entry requires traffic and timing context.'
  ],
 },
 'fortigate-ha-system-health': {
  'evidence': 'Example observations after maintenance: the expected primary and secondary members are visible, but synchronization is reported as incomplete. Both members report the intended firmware. No production traffic failure has yet been tied to the warning.',
  'interpretation': 'Member visibility and firmware agreement do not establish complete configuration synchronization. Preserve the warning and compare the reported member/health details with the maintenance record. Investigate the specific mismatch before considering disruptive recovery. A forced failover would change the condition being investigated and is not a diagnostic substitute for understanding it.',
  'verification': 'Confirm the documented mismatch is resolved and repeated observations show the intended member roles and synchronization state. Record the application health check. A failover exercise is a separate approved test with its own rollback plan, not a required step for this inspection.',
  'details': [
   'Match the visible members and roles with the inventory. A missing member and a visible but unsynchronized member require different evidence and should not share a generic fix.',
   'Record synchronization and time state without assuming that a clock warning explains every HA warning. Correlate timestamps with the maintenance activity.',
   'Compare the exact release and appliance identity for each member through approved access. A cluster-level summary can hide which member a supporting screenshot came from.',
   'Preserve the health details that identify the affected member or subsystem. Escalate that bounded finding rather than collecting unrelated debug output or triggering a failover.'
  ],
 },
 'cisco-routing-basics': {
  'evidence': 'Example observations: a specific destination lookup selects the intended next hop, its directly connected neighbor is resolved, and the outgoing interface is up. The destination responds to a nearby source but not to the affected client subnet.',
  'interpretation': 'The local route is one side of the exchange. Compare the destination-side return route and source-specific security rules for the affected subnet. Success from a different source is a controlled comparison only when the destination, service and time window match. A present route cannot rule out a later forwarding or application problem.',
  'verification': 'Repeat the same service request from the affected source after the responsible team corrects the documented issue. Preserve the forward lookup, return-path evidence and test time. A router-originated test with a different source address is additional evidence, not an equivalent user test.',
  'details': [
   'Record the route table context and selected destination prefix. A broad default route can coexist with a more specific route that sends the actual request elsewhere.',
   'Use the affected destination address for the lookup and keep its selected next hop. Compare that result with the intended path before discussing route redistribution or protocol resets.',
   'Inspect the on-link next hop in the neighbor table. If it resolves, continue along the packet path instead of equating neighbor success with end-to-end delivery.',
   'Tie the outgoing interface to the selected route and its expected address. Then ask the destination-side owner for return-path evidence for the original source subnet.'
  ],
 },
 'fortigate-session-inspection': {
  'evidence': 'Example observations: the failing application flow started before a policy change. Its existing session records a policy/context that differs from a newly created approved test flow. The table also contains many unrelated users and destinations.',
  'interpretation': 'The old and new flows must be evaluated separately. Session timing is a plausible reason for different behavior, but the session listing alone does not establish why traffic was permitted or denied at every stage. Match source, destination, translated addresses and policy with the exact test. Clearing the entire table would disrupt unrelated users and destroy useful comparison evidence.',
  'verification': 'Under the approved change procedure, retest a fresh connection and compare its identity and application outcome with the intended policy. If a scoped session action is approved, record its target and result. Do not use a drop in global session count as proof that the application was repaired.',
  'details': [
   'Record the appliance-wide baseline to understand incident load. Keep it separate from the identity and outcome of the individual application flow under review.',
   'Compare statistics during the reported interval. A change in totals may indicate activity but cannot identify whether this one connection used the intended policy.',
   'Locate the bounded flow using the release-appropriate inspection filter. Match both endpoints, translated addresses, policy and timing before calling it the affected session.',
   'Compare the current route for the same destination with the session context. Treat a discrepancy as a reason to investigate timing and forwarding history, not as an instruction to clear sessions.'
  ],
 },
 'cisco-neighbor-discovery': {
  'evidence': 'Example observations: the uplink description says SW-B port 1. CDP details on that local uplink advertise SW-C port 24; the physical patch record also points to SW-C. LLDP has no entry on that link.',
  'interpretation': 'Two independent observations support correcting the inventory, but neither the interface description nor an advertisement is an authoritative statement of ownership. Confirm the physical path and inventory identity before editing records. The absent LLDP entry does not contradict a CDP neighbor: protocol support and enablement can differ between peers.',
  'verification': 'After the physical path is confirmed, update the approved cabling/inventory record and any authorized interface description. Recheck the same local and remote port identifiers. Keep an unexplained identity discrepancy open rather than inventing an intermediate switch.',
  'details': [
   'Start with the local interface carrying the uplink. A neighbor elsewhere on the switch cannot validate this cable merely because its device name looks familiar.',
   'Compare the advertised identity and remote port with the existing patch record. Capture collection time because entries can remain briefly after a topology change.',
   'Treat LLDP as a separate observation. Confirm whether it is enabled and supported before interpreting the absence of an advertisement as a physical failure.',
   'Compare the manually maintained description with the discovery and cable evidence. Request physical confirmation if the sources disagree; do not silently choose the most convenient name.'
  ],
 },
 'linux-network-essentials': {
  'evidence': 'Example observations: the server has 192.0.2.10/24 on the expected interface, and its default route uses 192.0.2.1. During an approved connectivity test the gateway neighbor remains FAILED. A service listening on 127.0.0.1 is unrelated to reaching that gateway.',
  'interpretation': 'Addressing and route selection are consistent with an on-link gateway, so neighbor resolution is the next local boundary. Compare interface/VLAN placement and gateway ownership with the adjacent network. A failed neighbor state does not identify which device is at fault. A local listening socket answers a different question and cannot validate gateway reachability.',
  'verification': 'After the documented local-path repair, confirm neighbor resolution on the expected interface and retest the original destination. Compare link counters over a timed interval and check the return path if the remote operation still fails. Preserve the original evidence before restarting networking.',
  'details': [
   'Tie the address and prefix to the interface used by the affected traffic. An address on a different interface or network namespace does not establish the server path under test.',
   'Compare the selected gateway with the interface subnet and design. Avoid adding another default route merely because a connection attempt failed.',
   'Check the directly connected gateway during the approved test. Distinguish an idle missing entry from repeated failed resolution while the host needs that next hop.',
   'Compare errors and drops on the same interface before and after the interval. Stable counters narrow one question but do not rule out VLAN placement or a nonresponding peer.'
  ],
 },
 'cloud-network-fundamentals': {
  'evidence': 'Example observations in a constructed two-subnet design: the service name resolves to its intended private address, the source selects the intended route, and the destination security rules lack the source subnet for the application port. The return route has not yet been checked.',
  'interpretation': 'The missing rule is a concrete configuration discrepancy against the intended communication, but it should not conceal the untested return path. Compare the provider-specific security model before proposing a rule. Stateful connection handling and stateless subnet filtering are different controls; an AWS example does not establish the behavior of every cloud provider.',
  'verification': 'After an approved rule scoped to the required source and service, test the application from the original workload. Confirm return routing and any subnet filter requirements. Record the effective rule and application result rather than treating a route-table screenshot as completion.',
  'details': [
   'Write the source and destination address ranges first. Confirm whether the attempted destination is private and whether the ranges overlap before selecting a route.',
   'Identify the exact source workload and destination service attachment. A subnet label alone does not establish which network interface or security control carries the request.',
   'Trace the selected forward route and record the missing return-path check. Keep uncertainty visible rather than drawing an end-to-end path from one route table.',
   'Compare the required source, protocol and service port with the effective rules at the destination. State whether the provider treats this control as stateful or stateless.',
   'Resolve the same service name inside the affected workload environment. A laptop lookup outside that network may use a different resolver and address.'
  ],
 },
}

def apply_foundation_review(sheets):
    for sheet in sheets:
        review = REVIEWS.get(sheet['id'])
        if not review:
            continue
        case = sheet['case']
        assert len(case['steps']) == len(review['details']), sheet['id']
        for step, detail in zip(case['steps'], review['details']):
            step['detail'] = detail
        for field in ('evidence', 'interpretation', 'verification'):
            case[field] = review[field]
        case['escalation'] = ('Include the affected source and destination, collection times, relevant device release, '
                              'the observations above and the remaining untested boundary. Remove sensitive identifiers '
                              'before sharing outside the responsible support team.')
        sheet['updated'] = '2026-11-25'
        if sheet['id'] == 'cloud-network-fundamentals':
            sheet['prerequisites'] = ('Sketch the source workload, destination service, address ranges and required port. '
                                      'Use the provider-specific documentation for your environment; the reference rows '
                                      'are concepts, not commands to paste into a terminal.')
