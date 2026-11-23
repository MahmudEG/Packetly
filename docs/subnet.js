function calculateSubnet(input) {
    const match = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\/(\d{1,2})$/.exec(input.trim());
    if (!match) throw new Error('Enter an IPv4 address and a prefix, for example 192.0.2.70/26.');
    const parts = match.slice(1, 5).map(Number);
    const prefix = Number(match[5]);
    if (parts.some(part => part > 255) || prefix > 32) {
        throw new Error('Use octets from 0 to 255 and a prefix from 0 to 32.');
    }
    const address = parts.reduce((value, part) => value * 256 + part, 0);
    const size = 2 ** (32 - prefix);
    const first = Math.floor(address / size) * size;
    const last = first + size - 1;
    const ip = value => [24, 16, 8, 0].map(shift => (value >>> shift) & 255).join('.');
    return {
        'Network address': ip(first),
        'Subnet mask': ip(2 ** 32 - size),
        'Broadcast address': prefix < 31 ? ip(last) : 'Not applicable',
        'Usable range': prefix === 32 ? ip(first) : ip(first + Number(prefix < 31)) + ' – ' + ip(last - Number(prefix < 31)),
        'Total addresses': size.toLocaleString('en'),
        'Usable addresses': (prefix < 31 ? size - 2 : size).toLocaleString('en')
    };
}

function displaySubnet() {
    const result = document.querySelector('#cidr-result');
    try {
        const fields = calculateSubnet(document.querySelector('#cidr-input').value);
        const list = document.createElement('dl');
        for (const [label, value] of Object.entries(fields)) {
            const term = document.createElement('dt');
            const detail = document.createElement('dd');
            term.textContent = label;
            detail.textContent = value;
            list.append(term, detail);
        }
        result.replaceChildren(list);
    } catch (error) {
        result.textContent = error.message;
    }
}

document.querySelector('#cidr-form').addEventListener('submit', event => {
    event.preventDefault();
    displaySubnet();
});
displaySubnet();
