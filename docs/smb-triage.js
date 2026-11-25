'use strict';

// Deterministic evidence mapping. No network, storage, command execution or log uploads.
function planSmbInvestigation(observed) {
    const choices = {
        dns: ['unknown', 'expected', 'wrong'], tcp: ['unknown', 'pass', 'fail'],
        access: ['unknown', 'path', 'share', 'denied', 'ok', 'other'],
        session: ['unknown', 'yes', 'no'], scope: ['unknown', 'one', 'all']
    };
    for (const [key, allowed] of Object.entries(choices)) {
        if (!allowed.includes(observed[key])) throw new Error('Choose a valid observation for ' + key + '.');
    }
    const checks = [], limits = [];
    let focus = 'Collect a baseline before assigning a cause';
    if (observed.dns === 'wrong') {
        focus = 'Reconcile the target identity first';
        checks.push('Compare the exact UNC server name, DNS answers, expected address and the RemoteAddress reported by Test-NetConnection. An open port on an unintended endpoint does not validate the intended server.');
    } else if (observed.tcp === 'fail') {
        focus = 'Investigate the failed TCP path';
        checks.push('Record the destination address, source interface and incident time. Compare the route and permitted TCP 445 path with a working client; ask the server administrator to check the listener and matching network policy. A failed TCP test alone cannot locate the drop.');
    } else if (observed.access === 'ok') {
        focus = 'Confirm the original operation and document the working state';
        checks.push('Verify the originally failing folder or file operation as the affected user. Record the successful path and time. If the failure was intermittent, compare the failing and working timestamps.');
    } else if (observed.access === 'denied') {
        focus = 'Check the operation and effective identity';
        checks.push('Record the exact denied operation and the identity used by the SMB connection. Ask the server administrator to compare share access, filesystem permissions and relevant authentication or policy events. Do not infer the responsible permission layer from the error text alone.');
    } else if (observed.access === 'share') {
        focus = 'Verify the published share and exact path';
        checks.push('Compare the complete UNC path with the server share inventory. Confirm whether an alias or DFS namespace is involved. Keep share naming, referrals and server policy open until the corresponding evidence is collected.');
    } else if (observed.tcp === 'pass') {
        focus = 'Investigate the SMB stage beyond TCP';
        checks.push('Record SMBClient events at the failure time and inspect the LanmanWorkstation service. Have an authorized server administrator compare SMB server events. TCP success does not validate negotiation, authentication or access to the named share.');
    }
    if (observed.dns === 'unknown') checks.push('Resolve the exact server name used in the UNC path and compare every returned address with the intended endpoint.');
    if (observed.tcp === 'unknown') checks.push('Run a TCP 445 test from the affected client and record RemoteAddress and TcpTestSucceeded. Keep it in the same incident window as the folder access test.');
    if (observed.access === 'unknown') checks.push('Record the result of the exact UNC folder or file operation under the affected user, including the full error text.');
    if (observed.session === 'unknown') checks.push('Inspect Get-SmbConnection in the affected user context and compare ServerName, ShareName, UserName and Dialect.');
    if (observed.session === 'yes') limits.push('An existing connection is evidence of established state in the listed context; it does not prove a new session or every file operation succeeds.');
    if (observed.session === 'no') limits.push('No matching connection was listed. That does not by itself identify whether transport, negotiation, authentication or the share failed.');
    if (observed.scope === 'one') checks.push('Compare the two clients while keeping user, server name, share and timing consistent. Record differences in resolved address, route, Windows build, SMB policy and existing sessions.');
    if (observed.scope === 'all') checks.push('Check common dependencies, including the endpoint, server share and shared network path. Two failing clients do not establish that every client fails or that the server is the cause.');
    if (observed.scope === 'unknown') checks.push('If available, repeat the same path with the same authorized user on a comparison client. Change one variable at a time.');
    if (observed.access === 'ok' && (observed.tcp === 'fail' || observed.dns === 'wrong')) {
        limits.push('These observations need reconciliation: folder access succeeded while the target or TCP check failed. Compare timestamp, destination address, cached session and operation before combining the results.');
    }
    if (observed.session === 'yes' && observed.tcp === 'fail') limits.push('A listed session and failed new TCP test may reflect different timing or connection state. Retest in one time window; do not treat them as proof of a healthy current path.');
    limits.push('This plan is based only on your selections. It has not inspected the network and does not establish a root cause.');
    return { focus, checks, limits };
}

if (typeof document !== 'undefined') {
    const form = document.querySelector('#smb-form');
    if (form) {
        const result = document.querySelector('#smb-result');
        const download = document.querySelector('#smb-download');
        let handoff = '';
        const clear = () => {
            handoff = ''; download.disabled = true;
            result.replaceChildren();
            const p = document.createElement('p');
            p.textContent = 'Observations changed. Build a new plan to use the current selections.';
            result.append(p);
        };
        form.addEventListener('change', clear);
        form.addEventListener('reset', clear);
        form.addEventListener('submit', event => {
            event.preventDefault();
            const observed = Object.fromEntries(new FormData(form));
            const plan = planSmbInvestigation(observed);
            result.replaceChildren();
            const heading = document.createElement('h2'); heading.textContent = plan.focus; result.append(heading);
            for (const [title, items] of [['Next checks', plan.checks], ['Limits of this evidence', plan.limits]]) {
                const h = document.createElement('h3'); h.textContent = title; result.append(h);
                const list = document.createElement('ul');
                items.forEach(text => { const li = document.createElement('li'); li.textContent = text; list.append(li); });
                result.append(list);
            }
            const observations = [...form.querySelectorAll('select')].map(select => select.previousElementSibling.textContent + ': ' + select.selectedOptions[0].textContent);
            handoff = '# SMB access investigation handoff\n\nCreated: ' + new Date().toISOString() + '\n\n## Recorded observations\n\n'
                + observations.map(line => '- ' + line).join('\n') + '\n\n## Investigation focus\n\n' + plan.focus
                + '\n\n## Next checks\n\n' + plan.checks.map(line => '- ' + line).join('\n')
                + '\n\n## Limits\n\n' + plan.limits.map(line => '- ' + line).join('\n')
                + '\n\n## Add before escalation\n\n- Incident timestamp and time zone:\n- Client and server build:\n- Exact UNC path and affected identity:\n- Expected, resolved and contacted addresses:\n- Relevant event IDs and timestamps:\n- Controlled comparison result:\n- Original operation retest after repair:\n\nMethod: https://packetly.ly/tools/smb-access-planner/\n';
            download.disabled = false;
        });
        document.querySelector('#smb-example').addEventListener('click', () => {
            for (const [key, value] of Object.entries({ dns: 'expected', tcp: 'pass', access: 'path', session: 'no', scope: 'one' })) form.elements.namedItem(key).value = value;
            form.requestSubmit();
        });
        download.addEventListener('click', () => {
            if (!handoff) return;
            const url = URL.createObjectURL(new Blob([handoff], { type: 'text/markdown;charset=utf-8' }));
            const link = document.createElement('a'); link.href = url; link.download = 'packetly-smb-investigation.md';
            link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
        });
        document.querySelector('#smb-print').addEventListener('click', () => window.print());
    }
}
