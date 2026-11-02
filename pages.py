"""Copy for the standalone pages. Single source of truth: build.py renders
these into static HTML and also ships them to the client in data.js."""
INFO = {
    'about': [
        'A field guide for connected minds.',
        'Packetly brings practical IT references into one calm, searchable workspace. Explore Windows, Active Directory, Microsoft Graph, Entra ID, Exchange Online, Azure, FortiGate, Sophos, Cisco, Juniper, Ubiquiti, HPE, Dell and Data Domain, alongside Linux and cloud fundamentals. The name combines packets with an approachable “ly” ending.',
        'Our aim is to help you find the right command, understand its purpose and carry a useful reference to your desk. All guides are free to browse. Bookmarks are stored on your own device.',
    ],
    'editorial': [
        'Useful references, clear scope.',
        'Our guides prioritize inspection commands and explain their purpose in original walkthroughs. Each sheet includes its platform scope, update date and a link to primary documentation. Always consult the documentation for your deployed version.',
        'We do not claim that every command has been tested on every platform. We revise references when an error or version difference is identified. Vendor names belong to their respective owners. Sponsored placements, if introduced, will be labeled separately from editorial references.',
    ],
    'privacy': [
        'Privacy, in plain language.',
        'Packetly stores bookmarks and your theme preference in your browser’s local storage. These preferences are not submitted to a server by this website. You can clear them through your browser’s site-data settings.',
        'This website does not collect issue reports itself. The Report an issue button opens a pre-filled form on GitHub; anything you submit there becomes a public issue and is handled under GitHub’s own privacy terms. Hosting providers may process normal request logs. Google Fonts receives font requests, including normal network metadata.',
        'This site uses Google Analytics to measure traffic and Google AdSense to display advertising. Both are operated by Google, which may set cookies or similar identifiers in your browser and may process data including your IP address, device and browser details, and the pages you view. Google may use this data to personalise advertising. You can read how Google handles it at policies.google.com/technologies/partner-sites, choose your advertising settings at adssettings.google.com, and block or clear cookies through your browser’s settings. Analytics and advertising cookies stay switched off until you accept them in the banner shown on your first visit; use Change cookie choice below to answer again.',
    ],
    'terms': [
        'Use the guide with context.',
        'Packetly provides educational references without a warranty of completeness or compatibility. Verify commands against your platform documentation and your organization’s change process. Use commands only on systems you are authorized to administer.',
        'Fortinet, Cisco and other product names are trademarks of their respective owners. Packetly is independent and does not imply endorsement. Print references for personal learning and internal operational use.',
    ],
    'contact': [
        'Help make the next sheet better.',
        'Found an issue or need a tailored reference? Prepare a request with the sheet title, platform version, expected behavior and any correction. Do not include passwords, access tokens or private configuration.',
        'Use the button below to download a request brief you can share with your IT team. To report a correction, open the affected sheet and select Report an issue; it opens a pre-filled public issue on GitHub.',
    ],
}
