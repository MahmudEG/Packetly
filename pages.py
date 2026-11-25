"""Copy for the standalone pages. Single source of truth: build.py renders
these into static HTML and also ships them to the client in data.js."""
INFO = {
    'about': [
        'A practical reference for the next support ticket.',
        'Packetly is maintained through the public MahmudEG/Packetly GitHub repository. It serves IT administrators and technicians who need to choose an inspection command, understand the evidence it returns, and decide what to check next.',
        'Each guide combines platform scope, prerequisites, a command reference, an explanation and a worked investigation. The added value is the connection between an observation and the next decision: a reachable port, an established session and a successful application operation establish different things.',
        'Worked incidents are fictional teaching scenarios unless a page explicitly identifies a captured lab result. They are not customer testimonials or claims that every command was executed on every supported release. Vendor documentation remains the authority for version-specific syntax and behavior.',
        'The SMB investigation planner turns your selected observations into next checks and a downloadable handoff. The IPv4 calculator explains address boundaries. These tools run locally in the page and need no account. They do not inspect your network or submit your selections to Packetly.',
        'You can inspect the source, revision history and correction discussions using the links below. Packetly is independent of the vendors covered; all references are free to browse.',
    ],
    'editorial': [
        'Evidence before a proposed fix.',
        'A guide starts with a bounded problem and a stated platform scope. Commands must have a purpose in that investigation. We prioritize primary documentation and distinguish an inspection command from a test that sends traffic or a change that modifies a system.',
        'A useful explanation states what the result establishes and what remains uncertain. An old cumulative counter is not a current error rate; a listening port is not proof of successful authentication. Cases explain those distinctions and end with a retest of the original operation.',
        'Example observations are constructed for teaching and are labeled as fictional. We do not present generated examples as production logs, benchmarks or personal lab validation. A command documented by a vendor is not a claim that it was tested on every model, firmware or tenant configuration.',
        'A material correction or expansion updates the affected guide date. A routine rebuild does not make every page newly reviewed. GitHub records the source changes; the guide links to the documentation used for its scope.',
        'To report a correction, include the guide URL, relevant software version, the specific command or explanation, the observed problem, and a supporting primary reference when available. Do not post credentials, internal configurations or customer data. The public issue tracker and revision history are linked below.',
        'Advertising does not establish technical correctness or vendor endorsement. Sponsored material, if introduced, must be distinguished from the independent reference. The privacy page describes external scripts and browser storage choices.',
    ],
    'privacy': [
        'Privacy, in plain language.',
        'Packetly stores bookmarks and your theme preference in your browser’s local storage. These preferences are not submitted to a server by this website. You can clear them through your browser’s site-data settings.',
        'This website does not collect issue reports itself. The Report an issue button opens a pre-filled form on GitHub; anything you submit there becomes a public issue and is handled under GitHub’s own privacy terms. Hosting providers may process normal request logs. Google Fonts receives font requests, including normal network metadata.',
        'This site uses Google Analytics to measure traffic and Google AdSense to display advertising. Both are operated by Google, which may set cookies or similar identifiers in your browser and may process data including your IP address, device and browser details, and the pages you view. Google may use this data to personalise advertising. You can read how Google handles it at policies.google.com/technologies/partner-sites, choose your advertising settings at adssettings.google.com, and block or clear cookies through your browser’s settings. Storage consent defaults to denied. Accept permits analytics and advertising storage; Decline keeps storage consent denied. Google scripts still load and may make network requests with consent denied. Use Change cookie choice below to answer again.',
    ],
    'terms': [
        'Use the guide with context.',
        'Packetly provides educational references without a warranty of completeness or compatibility. Verify commands against your platform documentation and your organization’s change process. Use commands only on systems you are authorized to administer.',
        'Fortinet, Cisco and other product names are trademarks of their respective owners. Packetly is independent and does not imply endorsement. Print references for personal learning and internal operational use.',
    ],
    'contact': [
        'Help make the next sheet better.',
        'Found an incorrect command, unclear explanation or missing topic? Report the guide URL, software version, expected behavior, observed result and proposed correction. Do not include passwords, access tokens or private configuration.',
        'Use the button below to download a request brief you can share with your IT team. To report a correction, open the affected sheet and select Report an issue; it opens a pre-filled public issue on GitHub.',
    ],
}
