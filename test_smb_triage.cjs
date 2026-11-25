const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const context = vm.createContext({});
vm.runInContext(fs.readFileSync('docs/smb-triage.js', 'utf8'), context);
const plan = input => context.planSmbInvestigation(input);
const base = { dns:'unknown', tcp:'unknown', access:'unknown', session:'unknown', scope:'unknown' };
const unknown = plan(base);
assert.match(unknown.focus, /Collect a baseline/);
assert.equal(unknown.checks.length, 5);
assert.match(plan({...base, dns:'wrong', tcp:'pass'}).focus, /target identity/);
assert.match(plan({...base, dns:'expected', tcp:'fail'}).focus, /TCP path/);
assert.match(plan({...base, dns:'expected', tcp:'pass', access:'path'}).focus, /beyond TCP/);
assert.match(plan({...base, access:'denied'}).focus, /effective identity/);
assert.match(plan({...base, access:'share'}).focus, /exact path/);
assert.match(plan({...base, tcp:'fail', access:'ok'}).limits.join(' '), /need reconciliation/);
assert.match(plan({...base, tcp:'fail', session:'yes'}).limits.join(' '), /different timing/);
assert.throws(() => plan({...base, access:'<script>'}), /valid observation/);
let count = 0;
for (const dns of ['unknown','expected','wrong']) for (const tcp of ['unknown','pass','fail'])
for (const access of ['unknown','path','share','denied','ok','other']) for (const session of ['unknown','yes','no'])
for (const scope of ['unknown','one','all']) {
    const outcome = plan({dns,tcp,access,session,scope});
    assert(outcome.focus && outcome.checks.length > 0 && outcome.limits.length > 0);
    assert.equal(new Set(outcome.checks).size, outcome.checks.length);
    count++;
}
console.log(`PASS: ${count} observation combinations, unknown evidence, target mismatch, denied access and conflicting results`);
